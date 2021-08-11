import os
import shutil
import subprocess
from distutils.command.build import build

from setuptools import setup

PACKAGE_PATH = 'rhvoice_wrapper_data'
RHVOICE = 'RHVoice'
RHVOICE_GIT_TAG = '1.4.2'
RHVOICE_GIT_URL = 'https://github.com/Olga-Yakovleva/RHVoice.git'
DATA_DIR = 'data'
LICENSES_DIR = 'licenses'


def check_build(data_paths):
    for target in data_paths:
        if not os.path.isdir(target):
            return 'Directory {} not found'.format(target)


def ignore_install(src, names):
    # Only 24000 adding
    if '16000' in names and os.path.isdir(os.path.join(src, '16000')) and '24000' in names:
        return ['16000', 'CMakeLists.txt']
    return ['CMakeLists.txt']


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
    def _copy_file(self, filename, src_path, dst_path):
        def make_dst():
            dst__ = os.path.join(dst_path, filename)
            if os.path.exists(dst__):
                for x in range(1, 9999):
                    filename_2 = '{}-{}'.format(filename, x)
                    dst__ = os.path.join(dst_path, filename_2)
                    if not os.path.exists(dst__):
                        self.warn('File {} already exists in {}, save is as {}!'.format(filename, dst_path, filename_2))
                        break
                else:
                    raise RuntimeError('ok')
            return dst__

        src = os.path.join(src_path, filename)
        if not os.path.isfile(src):
            return
        if not os.path.exists(dst_path):
            self.mkpath(dst_path)
        dst = make_dst()
        self.debug_print('copying {} to {}...'.format(src, dst))
        dst = shutil.copy(src, dst)
        self.debug_print('copy {} to {}'.format(src, dst))

    def _copy_dirs(self, targets: list):
        self.debug_print('Starting data copying...')
        for src, dst in targets:
            if os.path.exists(dst):
                self.debug_print('Existing path {}. deleting...'.format(dst))
                shutil.rmtree(dst, ignore_errors=True)
            self.debug_print('copying {} to {}...'.format(src, dst))
            dst = shutil.copytree(src, dst, ignore=ignore_install)
            self.debug_print('copy {} to {}'.format(src, dst))

    def _copy_licenses(self, src_path, targets: list):
        self.debug_print('Starting licenses copying...')
        dst_licenses = targets[-1][1]
        src_voices = targets[0][0]
        for top_license in os.listdir(src_path):
            if top_license.lower().startswith('license'):
                self._copy_file(top_license, src_path, dst_licenses)
        for voice in os.listdir(src_voices):
            src_voice = os.path.join(src_voices, voice)
            if os.path.isdir(src_voice):
                for target in os.listdir(src_voice):
                    if target.lower().startswith(('license', 'readme')):
                        self._copy_file(target, src_voice, os.path.join(dst_licenses, 'voices', voice))

    def run(self):
        src_path = os.path.join(self.build_base, RHVOICE)
        dst_path = os.path.join(self.build_lib, PACKAGE_PATH)
        targets = [
            (os.path.join(src_path, x), os.path.join(dst_path, x))
            for x in [os.path.join(DATA_DIR, 'voices'), os.path.join(DATA_DIR, 'languages'), LICENSES_DIR]
        ]

        self.mkpath(self.build_base)
        self.mkpath(self.build_lib)
        [self.mkpath(x) for _, x in targets]

        clone = [['git', 'clone', '--depth=1', '--branch', RHVOICE_GIT_TAG, RHVOICE_GIT_URL, src_path], None]

        if not os.path.isdir(src_path):
            self.execute(executor, clone, 'Clone {}'.format(RHVOICE_GIT_URL))
        else:
            self.warn('Use existing source data from {}'.format(src_path))

        msg = check_build([x for x, _ in targets])
        if msg is not None:
            raise RuntimeError(msg)

        if not self.dry_run:
            self._copy_dirs(targets)
            self._copy_licenses(src_path, targets)

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
    package_data={PACKAGE_PATH: [os.path.join(x, '*') for x in (DATA_DIR, LICENSES_DIR)]},
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
