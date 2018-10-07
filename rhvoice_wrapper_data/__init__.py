import os

PATH = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(PATH, 'data')
if os.path.isdir(data_path):
    if os.path.isdir(os.path.join(data_path, 'voices')) and os.path.isdir(os.path.join(data_path, 'languages')):
        pass
    else:
        raise RuntimeError('Empty data: {}'.format(data_path))
else:
    raise RuntimeError('Data path not found: {}'.format(data_path))

