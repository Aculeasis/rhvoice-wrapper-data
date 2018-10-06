## rhvoice-wrapper-data

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
rhvoice-wrapper will automatically use paths from rhvoice_wrapper_data:
```python
from rhvoice_wrapper import TTS
tts = TTS()
```
Or you may use this manually:
```python
from rhvoice_wrapper import TTS
import rhvoice_wrapper_data

# Contains path to the RHVoice library or None if errors
print(rhvoice_wrapper_data.lib_path)
# Contains path to the RHVoice data or None if errors
print(rhvoice_wrapper_data.data_path)

tts = TTS(lib_path=rhvoice_wrapper_data.lib_path, data_path=rhvoice_wrapper_data.data_path)
```
Or use installed RHVoice instead of rhvoice-wrapper-data
```python
from rhvoice_wrapper import TTS
tts = TTS(lib_path=None, data_path=None)
```
## Links

- [RHVoice](https://github.com/Olga-Yakovleva/RHVoice)
- [rhvoice-wrapper](https://github.com/Aculeasis/rhvoice-proxy)
