import os
import shutil
import subprocess
from distutils.command.build import build

from setuptools import setup

PACKAGE_PATH = 'rhvoice_wrapper_data'
RHVOICE = 'RHVoice'
RHVOICE_GIT_TAG = '1.0.0'
RHVOICE_GIT_URL = 'https://github.com/Olga-Yakovleva/RHVoice.git'
DATA_DIR = 'data'


def check_build(data_paths):
    for target in data_paths:
        if not os.path.isdir(target):
            return 'Directory {} not found'.format(target)


def ignore_install(src, names):
    # Only 24000 adding
    if '16000' in names and os.path.isdir(os.path.join(src, '16000')) and '24000' in names:
        return ['16000']
    return []


def executor(cmd, cwd):
    err = None
    try:
        run = subprocess.call(cmd, cwd=cwd)
    except Exception as e:
        err = e
    else:
        if run != 0:
            err = 'code: {}'.format(run)
    if err is not None:
        raise RuntimeError('Error executing {} in {}. {}'.format(cmd, str(cwd), err))


class RHVoiceBuild(build):
    def run(self):
        rhvoice_path = os.path.join(self.build_base, RHVOICE)
        build_lib_data = os.path.join(self.build_lib, PACKAGE_PATH, DATA_DIR)

        self.mkpath(self.build_base)
        self.mkpath(self.build_lib)
        self.mkpath(build_lib_data)

        data_paths = [
            os.path.join(rhvoice_path, os.path.join('data', 'languages')),
            os.path.join(rhvoice_path, os.path.join('data', 'voices'))
        ]

        clone = [['git', 'clone', '--depth=1', '--branch', RHVOICE_GIT_TAG, RHVOICE_GIT_URL, rhvoice_path], None]

        if not os.path.isdir(rhvoice_path):
            self.execute(executor, clone, 'Clone {}'.format(RHVOICE_GIT_URL))
        else:
            self.warn('Use existing source data from {}'.format(rhvoice_path))

        msg = check_build(data_paths)
        if msg is not None:
            raise RuntimeError(msg)

        if not self.dry_run:  # copy data folders
            self.debug_print('Starting data copying...')
            for target in data_paths:
                dst = os.path.join(build_lib_data, os.path.basename(target))
                if os.path.exists(dst):
                    self.debug_print('Existing path {}. deleting...'.format(dst))
                    shutil.rmtree(dst, ignore_errors=True)
                self.debug_print('copying {} to {}...'.format(target, dst))
                dst = shutil.copytree(target, dst, ignore=ignore_install)
                self.debug_print('copy {} to {}'.format(target, dst))

        build.run(self)


def get_version() -> str:
    version_file = 'version'

    def version_to_file(ver):
        with open(version_file, mode='w') as fd:
            fd.write(ver)

    def version_from_file():
        with open(version_file) as fd:
            return fd.read().splitlines()[0]

    def version_from_git():
        cmd = ['git', 'describe', '--abbrev=0', '--tags']
        try:
            return subprocess.check_output(cmd).decode().splitlines()[0]
        except Exception as e:
            print('ERROR! Execute {}: {}'.format(cmd, e))
            return None
    version = version_from_git()
    if not version:
        version = version_from_file()
        print('WARNING! Get version from a file: {}'.format(version))
    else:
        version_to_file(version)
    return version


def get_long_description():
    with open('README.md') as fh:
        return fh.read()


setup(
    name='rhvoice-wrapper-data',
    version=get_version(),
    packages=[PACKAGE_PATH],
    package_data={PACKAGE_PATH: [os.path.join(DATA_DIR, '*')]},
    url='https://github.com/Aculeasis/rhvoice-wrapper-data',
    license='GPLv3+',
    author='Aculeasis',
    author_email='amilpalimov2@ya.ru',
    description='Provides RHVoice data for rhvoice-wrapper-bin',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    python_requires='>=3.4',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
    ],
    zip_safe=False,
    cmdclass={'build': RHVoiceBuild},
    include_package_data=True,
)
