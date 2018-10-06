import os

try:
    __PATH = os.path.dirname(os.path.abspath(__file__))

    lib_path = os.path.join(__PATH, 'RHVoice.dll' if os.name == 'nt' else 'libRHVoice.so')
    lib_path = lib_path if os.path.isfile(lib_path) else None

    data_path = os.path.join(__PATH, 'data')
    if os.path.isdir(data_path):
        if os.path.isdir(os.path.join(data_path, 'voices')) and os.path.isdir(os.path.join(data_path, 'languages')):
            pass
        else:
            data_path = None
    else:
        data_path = None
except Exception as e:
    print('Error in rhvoice-wrapper-data: {}'.format(e))
    data_path = None
    lib_path = None

