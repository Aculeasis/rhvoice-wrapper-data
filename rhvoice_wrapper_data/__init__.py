import os
from ctypes import cdll

try:
    PATH = os.path.dirname(os.path.abspath(__file__))
    LIBS_PATH = os.path.join(PATH, 'lib')

    lib_path = os.path.join(LIBS_PATH, 'RHVoice.dll' if os.name == 'nt' else 'libRHVoice.so')
    if not os.path.isfile(lib_path):
        raise RuntimeError('Library not found: {}'.format(lib_path))

    __core_path = os.path.join(LIBS_PATH, 'libRHVoice_core.so') if os.name != 'nt' else None

    data_path = os.path.join(PATH, 'data')
    if os.path.isdir(data_path):
        if os.path.isdir(os.path.join(data_path, 'voices')) and os.path.isdir(os.path.join(data_path, 'languages')):
            pass
        else:
            raise RuntimeError('Empty data: {}'.format(data_path))
    else:
        raise RuntimeError('Data path not found: {}'.format(data_path))

    if __core_path:  # preload core library
        cdll.LoadLibrary(__core_path)
except Exception as e:
    print('Error in rhvoice-wrapper-data: {}'.format(e))
    LIBS_PATH = None
    PATH = None
    data_path = None
    lib_path = None

