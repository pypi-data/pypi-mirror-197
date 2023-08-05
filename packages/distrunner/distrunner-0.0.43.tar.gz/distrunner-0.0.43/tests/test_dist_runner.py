import importlib
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType

import requests

from src.distrunner.distrunner import DistRunner


class DistRunnerTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        :return: None
        """
        self.repo = "https://gitlab.com/crossref/labs/task-test.git"
        self.requirement_test_item = "delorean"  # a third party library
        self.stdlib_test_item = "webbrowser"  # an unused standard library

        self._dist_runner = self._reset_dist_runner()
        self._dist_runner.start_cluster()

    def test_cluster_exists(self) -> None:
        """
        Tests the cluster has started
        :return: None
        """
        self.assertIsNotNone(self._dist_runner.client)

    def test_pull_git(self):
        """
        Tests the git pull routine works
        :return: None
        """
        with TemporaryDirectory() as tmp_dir:
            self._dist_runner._pull_git((self.repo, tmp_dir))

            path = Path(tmp_dir) / "repo"
            self.assertIn(
                "task.py", [f.name for f in path.iterdir() if f.is_file()]
            )

    def test_pull_git_fail(self):
        """
        Tests the git pull routine fails correctly
        :return: None
        """
        with TemporaryDirectory() as tmp_dir:
            with self.assertRaises(Exception):
                self._dist_runner._pull_git(("NOT A REPO", tmp_dir))

    def test_read_file(self):
        """
        Test the file read routine works
        :return: None
        """
        requirements_path = Path(Path("tests") / "requirements_tests.txt")

        self.assertIn(
            f"{self.requirement_test_item}\n",
            self._dist_runner._read_file_lines(requirements_path),
        )

    def test_handover(self):
        """
        Tests that the module handover routine works
        :return: None
        """
        this_module = sys.modules[__name__]
        self._dist_runner._test_flag = True
        self.assertTrue(self._dist_runner.handover(this_module))

        self._dist_runner._test_flag = False
        self.assertFalse(self._dist_runner.handover(this_module))

    def test_handover_fail(self):
        """
        Tests that the module handover routine fails correctly
        :return: None
        """
        this_module = sys.modules[__name__]
        self._dist_runner._entry_point = "doesnotexist"

        with self.assertRaises(AttributeError):
            self._dist_runner.handover(this_module)

        self._reset_dist_runner()

    def test_worker_observability(self):
        """
        Test that we can retrieve worker logs
        :return: None
        """
        with self.assertLogs(level="INFO") as log:
            logs = self._dist_runner.process_worker_logs(verbose=False)

            found_log = False

            for worker, log_entry in logs.items():
                if "distributed.worker" in log_entry[0][1]:
                    found_log = True
                    break
            self.assertTrue(found_log)

            # with verbose set to False we should not see any worker logs
            worker_logs = self._handle_worker_logs(log.output)
            self.assertTrue(len(worker_logs) == 0)

            self._dist_runner.process_worker_logs(verbose=True)

            worker_logs = self._handle_worker_logs(log.output)
            self.assertFalse(len(worker_logs) == 0)

    def test_worker_install_requirements(self):
        """
        Tests that the installation of requirements works on Workers
        :return: pass
        """
        self._reset_dist_runner()
        self._dist_runner.start_cluster()

        requirements = [self.requirement_test_item]

        self._dist_runner._process_worker_retries(
            self._uninstall_on_workers, (self.requirement_test_item,)
        )

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "uninstall",
                "--yes",
                self.requirement_test_item,
            ]
        )

        self._dist_runner._install_requirements(
            client=self._dist_runner.client,
            requirements=requirements,
        )

        # try to load the module again
        results = self._dist_runner._process_worker_retries(
            DistRunnerTestCase._load_module,
            (self.requirement_test_item,),
        )

        results = self._dist_runner._process_worker_retries(
            DistRunnerTestCase._is_module_loaded_on_worker,
            (self.requirement_test_item,),
        )

        for item, val in results.items():
            self.assertTrue(val)

        # remove the package (we can just do this on the host as this test
        # runs in local mode with all workers on the same machine)
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "uninstall",
                "--yes",
                self.requirement_test_item,
            ]
        )

    def test_gather_requirements(self):
        """
        Test the gather requirements function
        :return: None
        """
        with TemporaryDirectory() as tmp_dir:
            reqs = self._dist_runner._gather_requirements(
                repo=self.repo,
                temporary_directory=tmp_dir,
                requirements_file="requirements.txt",
            )

            self.assertIn(f"whatismyip", reqs)

    def test_gather_requirements_fails(self):
        """
        Test the gather requirements function fails correctly
        :return: None
        """
        with TemporaryDirectory() as tmp_dir:
            with self.assertRaises(FileNotFoundError):
                reqs = self._dist_runner._gather_requirements(
                    repo=self.repo,
                    temporary_directory=tmp_dir,
                    requirements_file="doesnotexist",
                )

    @staticmethod
    def _uninstall_on_workers(arguments: tuple):
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "uninstall",
                "--yes",
                arguments[0],
            ]
        )

    def test_download_file(self):
        """
        Test that the download file function works
        :return: None
        """
        with TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "git"

            self._dist_runner._download_file(
                "https://gitlab.com/crossref/labs/distrunner/-/"
                "raw/main/binary/git?inline=false",
                str(path),
            )

            self.assertIn(
                "git", [f.name for f in path.parent.iterdir() if f.is_file()]
            )

    def test_download_file_fail(self):
        """
        Test that the download file function fails correctly
        :return: None
        """
        with TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "git"

            with self.assertRaises(requests.exceptions.ConnectionError):
                self._dist_runner._download_file(
                    "https://thisFILEdoesnotexistffds423432.com",
                    str(path),
                )

    def test_bootstrap_git(self):
        """
        Test that the AWS bootstrapper works
        :return: None
        """
        with TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "git"
            path_core = Path(tmp_dir) / "git-http-backend"

            self._dist_runner.bootstrap_git_to_aws(
                git_file=self._dist_runner.GIT_FILE,
                git_core_file=self._dist_runner.GIT_CORE,
                working_directory=Path(tmp_dir),
            )

            self.assertTrue(path.exists())
            self.assertTrue(path_core.exists())

    def test_install_requirements(self):
        """
        Tests that the installation requirements/bootstrap routine works
        :return: None
        """
        requirements_path = Path(Path("tests") / "requirements_tests.txt")

        if requirements_path.exists():
            requirements_file = str(requirements_path.absolute())

            self.assertFalse(self._is_module_loaded(self.requirement_test_item))

            self._dist_runner._install_requirements_local(requirements_file)
            self._dist_runner._import_lib((self.requirement_test_item, False))

            self.assertTrue(self._is_module_loaded(self.requirement_test_item))

            # undo the installation
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "uninstall",
                    "--yes",
                    "-r",
                    str(requirements_file),
                ]
            )
        else:
            self.fail(
                "Could not find the requirements file: {}".format(
                    requirements_path.absolute()
                )
            )

    def test_error_handling(self):
        """
        Tests that error handling works correctly for the context manager
        :return: None
        """
        with self.assertRaises(Exception):
            self._dist_runner.__exit__(
                Exception, Exception("Test Exception"), None
            )

        self._reset_dist_runner()
        self._dist_runner.start_cluster()

        try:
            self._dist_runner.__exit__(None, None, None)
        except Exception:
            self.fail("Unexpected exception raised on shutdown")

        self._reset_dist_runner()
        self._dist_runner.start_cluster()

    def test_import_library(self):
        """
        Tests the library import routine works
        :return: None
        """
        self.assertFalse(self._is_module_loaded(self.stdlib_test_item))

        result = self._dist_runner._import_lib((self.stdlib_test_item, True))

        self.assertTrue(self._is_module_loaded(self.stdlib_test_item))
        self.assertIsInstance(result, ModuleType)

        result = self._dist_runner._import_lib((self.stdlib_test_item, False))

        self.assertIsNone(result)

    def test_import_library_fail(self):
        """
        Tests the library import routine fails correctly
        :return: None
        """
        with self.assertRaises(ModuleNotFoundError):
            result = self._dist_runner._import_lib(("NONEXISTENTMODULE", True))

    def test_system_path_append(self):
        """
        Tests the system path is appended to correctly
        :return: None
        """
        self.assertNotIn("test", sys.path)

        self._dist_runner._setup_system_path(("test",))

        self.assertIn("test", sys.path)

    def test_retry(self):
        """
        Tests the retry function retries calling the right number of times
        :return: None
        """
        results = self._dist_runner._process_worker_retries(
            func=self._retry_callback, arguments=(False,)
        )

        for result, val in results.items():
            self.assertEqual(val, True)

    def test_retry_fail(self):
        """
        Tests the retry function fails correctly after the max attempts
        :return: None
        """
        with self.assertRaises(Exception):
            self._dist_runner._process_worker_retries(
                func=self._retry_callback, arguments=(True,)
            )

    def tearDown(self):
        """
        Tears down the test suite
        :return: None
        """
        self._dist_runner.__exit__(None, None, None)

    def _reset_dist_runner(self) -> DistRunner:
        """
        Reset the dist runner to default state
        :return: None
        """
        if hasattr(self, "_dist_runner") and self._dist_runner is not None:
            self._dist_runner.__exit__(None, None, None)

        self._dist_runner = DistRunner(
            local=True,
            retries=3,
            repo=self.repo,
            entry_point="entry_point",
        )

        return self._dist_runner

    @staticmethod
    def _is_module_loaded(module: str) -> bool:
        """
        Test if a module is loaded
        :param module: the module name
        :return: True if loaded, False otherwise
        """
        return module in sys.modules

    @staticmethod
    def _is_module_loaded_on_worker(arguments: tuple) -> bool:
        """
        Test if a module is loaded on workers
        :param arguments: a tuple with the module name
        :return: True if loaded, False otherwise
        """
        return DistRunnerTestCase._is_module_loaded(arguments[0])

    @staticmethod
    def _handle_worker_logs(logs) -> list[str]:
        """
        Determine if worker logs have been displayed
        :param logs: the test suite's logs context manager's output
        :return: a list of worker log strings
        """
        return [item for item in logs if "distributed.worker" in item]

    @staticmethod
    def _load_module(module_name: str) -> ModuleType:
        """
        Load a module
        :param module_name: the module name
        :return: the loaded module
        """
        return importlib.import_module(module_name[0])

    @staticmethod
    def _retry_callback(arguments) -> bool:
        """
        A callback function to be used in the retry tests
        :param arguments: a tuple of arguments
        :return: a bool
        """
        always_fail = arguments[0]
        attempt = arguments[-1]

        if attempt < 3 or always_fail:
            attempt += 1
            raise Exception("Test exception")
        else:
            return True


def entry_point(dist_runner: DistRunner):
    """
    A test entry point
    :param dist_runner: the DistRunner instance
    :return: the _test_flag attribute of dist_runner
    """
    return dist_runner._test_flag


if __name__ == "__main__":
    unittest.main()
