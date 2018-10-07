## rhvoice-wrapper-data
[![PyPI version](https://img.shields.io/pypi/v/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/) [![Python versions](https://img.shields.io/pypi/pyversions/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/) [![PyPI - Format](https://img.shields.io/pypi/format/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/) [![Build Status](https://travis-ci.org/Aculeasis/rhvoice-wrapper-data.svg?branch=master)](https://travis-ci.org/Aculeasis/rhvoice-wrapper-data)

Provides RHVoice libraries and data for rhvoice-wrapper. Linux only.

If this package installed, rhvoice-wrapper will automatically use it by default.

## Install
`pip install rhvoice-wrapper-data --only-binary rhvoice-wrapper-data`

## Install from source
First, install dependencies to build:

`apt-get install --no-install-recommends scons build-essential python3-pip python3-setuptools python3-wheel`

Install package from source. This download and build RHVoice and may take many time:

`pip install rhvoice-wrapper-data --no-binary rhvoice-wrapper-data`

## Usage
rhvoice-wrapper will automatically use data path from rhvoice_wrapper_data.
You must set package library path for LD before run python scripts. You may set `LD_LIBRARY_PATH`, this must be works:
```bash
export LD_LIBRARY_PATH=$(pip3 show rhvoice-wrapper-data | grep Location | awk '{print $2}')/rhvoice_wrapper_data/lib/
python3 -u <script using rhvoice_wrapper>
```
#### Get info from library
```python
import rhvoice_wrapper_data
# All the paths will None in error

# Contains path to the RHVoice library
print(rhvoice_wrapper_data.lib_path)
# Contains path to the RHVoice data
print(rhvoice_wrapper_data.data_path)
# Contains path to the RHVoice libraries. Must be set as dynamic libraries path
print(rhvoice_wrapper_data.LIBS_PATH)
# Contains path to the rhvoice-wrapper-data
print(rhvoice_wrapper_data.PATH)
```
## Links

- [RHVoice](https://github.com/Olga-Yakovleva/RHVoice)
- [rhvoice-wrapper](https://github.com/Aculeasis/rhvoice-proxy)
