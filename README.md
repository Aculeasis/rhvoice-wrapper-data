# This package contain only data, `rhvoice-wrapper-bin` install it yourself

[![RHVoice](https://img.shields.io/badge/RHVoice-1.2.3-lightgrey.svg)](https://github.com/Olga-Yakovleva/RHVoice/tree/1.2.3)
[![PyPI version](https://img.shields.io/pypi/v/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/)
[![Python versions](https://img.shields.io/badge/python-3.4%2B-blue.svg)](https://pypi.org/project/rhvoice-wrapper-data/)
[![PyPI - Format](https://img.shields.io/pypi/format/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/)
[![Build Status](https://travis-ci.org/Aculeasis/rhvoice-wrapper-data.svg?branch=master)](https://travis-ci.org/Aculeasis/rhvoice-wrapper-data)
[![Build status](https://ci.appveyor.com/api/projects/status/0nnncu1pvbeqjqk1?svg=true)](https://ci.appveyor.com/project/Aculeasis/rhvoice-wrapper-data)

Provides [RHVoice](https://github.com/Olga-Yakovleva/RHVoice) voices and languages for [rhvoice-wrapper-bin](https://github.com/Aculeasis/rhvoice-wrapper-bin). Also, you may set data_path in [rhvoice-wrapper](https://github.com/Aculeasis/rhvoice-proxy) instead.

This package contains 24000 Hz voice sampling rate, excluded 16000 Hz for reduce size.

## Install
`pip3 install rhvoice-wrapper-data --only-binary rhvoice-wrapper-data`

## Install from source
Install git (`apt install git` or `run exe>next>next>done`)
```bash
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install rhvoice-wrapper-data --no-binary rhvoice-wrapper-data
```
## API
```python
import rhvoice_wrapper_data

# Contains path to the RHVoice data
print(rhvoice_wrapper_data.data_path)
# Contains path to the rhvoice-wrapper-data
print(rhvoice_wrapper_data.PATH)
```
## License
Some voices use non-free licenses, explore `echo $(python3 -c 'import rhvoice_wrapper_data as d; print(d.PATH)')/licenses` directory or\and RHVoice repo for more info.