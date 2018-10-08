# This package contain only data, [rhvoice-wrapper-bin](https://github.com/Aculeasis/rhvoice-wrapper-bin) install it yourself

[![PyPI version](https://img.shields.io/pypi/v/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/) [![Python versions](https://img.shields.io/pypi/pyversions/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/) [![PyPI - Format](https://img.shields.io/pypi/format/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/) [![Build Status](https://travis-ci.org/Aculeasis/rhvoice-wrapper-data.svg?branch=master)](https://travis-ci.org/Aculeasis/rhvoice-wrapper-data) [![Build status](https://ci.appveyor.com/api/projects/status/0nnncu1pvbeqjqk1?svg=true)](https://ci.appveyor.com/project/Aculeasis/rhvoice-wrapper-data)

Provides RHVoice voices and languages for `rhvoice-wrapper-bin`. Also, you may set data_path in `rhvoice-wrapper` instead.

## Install
`pip install rhvoice-wrapper-data --only-binary rhvoice-wrapper-data`

## Install from source
Install git (`apt install git` or `run exe>next>next>done`)
```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install rhvoice-wrapper-data --no-binary rhvoice-wrapper-data
```
### API
```python
import rhvoice_wrapper_data

# Contains path to the RHVoice data
print(rhvoice_wrapper_data.data_path)
# Contains path to the rhvoice-wrapper-data
print(rhvoice_wrapper_data.PATH)
```
## Links

- [RHVoice](https://github.com/Olga-Yakovleva/RHVoice)
- [rhvoice-wrapper](https://github.com/Aculeasis/rhvoice-proxy)
- [rhvoice-wrapper-bin](https://github.com/Aculeasis/rhvoice-wrapper-bin)
