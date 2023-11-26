# This package contain only data, `rhvoice-wrapper-bin` will install it itself

[![RHVoice](https://img.shields.io/badge/RHVoice-1.14.0-lightgrey.svg)](https://github.com/RHVoice/RHVoice/tree/1.14.0)
[![PyPI version](https://img.shields.io/pypi/v/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/)
[![Python versions](https://img.shields.io/badge/python-3.4%2B-blue.svg)](https://pypi.org/project/rhvoice-wrapper-data/)
[![PyPI - Format](https://img.shields.io/pypi/format/rhvoice-wrapper-data.svg)](https://pypi.org/project/rhvoice-wrapper-data/)
[![Build](https://github.com/Aculeasis/rhvoice-wrapper-data/actions/workflows/python-package.yml/badge.svg)](https://github.com/Aculeasis/rhvoice-wrapper-data/actions/workflows/python-package.yml)

Provides [RHVoice](https://github.com/RHVoice/RHVoice) voices and languages for [rhvoice-wrapper-bin](https://github.com/Aculeasis/rhvoice-wrapper-bin). Also, you may set data_path in [rhvoice-wrapper](https://github.com/Aculeasis/rhvoice-proxy) instead.

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
