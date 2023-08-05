# Distributed Runner
This library allows for the easy construction and management of Dask clusters from a Git repository via a simple context manager.

![license](https://img.shields.io/gitlab/license/crossref/labs/distrunner) ![activity](https://img.shields.io/gitlab/last-commit/crossref/labs/distrunner) <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

![Dask](https://img.shields.io/badge/dask-%23092E20.svg?style=for-the-badge&logo=dask&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitLab](https://img.shields.io/badge/gitlab-%23121011.svg?style=for-the-badge&logo=gitlab&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Installation

    pip install distrunner

## Usage

In your scheduler (Airfow etc.) use this:

    from distrunner import DistRunner

    with DistRunner(
        workers=5,
        python_version="3.10",
        repo="https://gitlab.com/crossref/labs/task-test.git",
        entry_module="task",
        entry_point="entry_point",
        requirements_file="requirements.txt",
        local=False,
        retries=3,
        worker_memory=16384,
        worker_cpus=4096,
    ) as dr:
        logging.basicConfig(level=logging.INFO)

        dr.run()

The "local" flag will determine whether a remote cluster is created.

The code in the git repository at the module and entry point that you specify will be called, passing the DaskRunner object. You can use this, then, to obtain a Dask client by calling cldr.client.

You will need to set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables to use the Fargate clusters.

## Features
* Context manager handling of Dask Fargate clusters with scale-to-zero on complete
* Easy ability to switch between local and distributed/remote development
* Simple deployment from a git repository including all requirements
* Bugfixes to Dask AWS 2022.10.0 to suppress errors in weakref finalizers

## What it Does
This library allows you to bootstrap a git repository into a distributed computation environment. It will install all the needed dependencies into the current virtual environment and sync these with workers. Your code's entrypoint will be called with access to a Dask Client object.

## Credits

* [AWS/Boto](https://github.com/boto/botocore)
* [Dask](https://www.dask.org/)
* [Git](https://git-scm.com/)
* [GitPython](https://github.com/gitpython-developers/GitPython)

Copyright &copy; Crossref 2023 