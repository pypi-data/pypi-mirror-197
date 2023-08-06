# VCLog

[![pypi version](https://img.shields.io/pypi/v/vclog?logo=pypi)](https://pypi.org/project/vclog/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)
[![docs](https://badgen.net/badge/readthedocs/documentation/blue)](https://vclog.readthedocs.io/en/latest/)

Vistor's Console Logger (VCLog) is a lightweight logger that aims to provide simple solutions for simple problems. The `Logger` class can be used either as a static class with static methods or it can be instanciated to provide a name to the logging.

## Installation

Follow the next steps for installing the simulation on your device.

**Requierements:**
- Python 3.10.0 or higher

> **Note**: VCLog works on Linux, Windows and Mac.

### Install miniconda (highly-recommended)
It is highly recommended to install all the dependencies on a new virtual environment. For more information check the conda documentation for [installation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) and [environment management](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). For creating the environment use the following commands on the terminal.

```bash
conda create -n vclog python==3.10.9
conda activate vclog
```
### Install from pip
VCLog is available as a pip package. For installing it just use:
```
pip install vclog
```

### Install from source
Firstly, clone the repository in your system.
```bash
git clone https://github.com/vistormu/vclog.git
```

Then, enter the directory and install the required dependencies
```bash
cd vclog
pip install -r requirements.txt
```

## Documentation
The official documentation of the package is available on [Read the Docs](https://vclog.readthedocs.io/en/latest/). Here you will find the [installation instructions](https://vclog.readthedocs.io/en/latest/src/installation.html), the [API reference](https://vclog.readthedocs.io/en/latest/src/api_reference.html) and some [minimal working examples](https://vclog.readthedocs.io/en/latest/src/examples.html).