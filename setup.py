import os
import shutil
import subprocess
import sys
from distutils.command.build import build

from setuptools import setup

ALL_VOICES = '--all-voices' in sys.argv and sys.argv.remove('--all-voices') is None
PACKAGE_PATH = 'rhvoice_wrapper_data'
RHVOICE = 'RHVoice'
RHVOICE_TAG = '1.14.0'
RHVOICE_URL = 'https://github.com/RHVoice/RHVoice.git'
DATA_DIR = 'data'
LICENSES_DIR = 'licenses'
BASE_VOICES = set('aleksandr anatol anna azamat bdl clb elena irina Leticia-F123 natalia natia nazgul slt spomenka '
                  'talgat'.split(' '))


def check_build(data_paths):
    for target in data_paths:
        if not os.path.isdir(target):
            return 'Directory {} not found'.format(target)


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
        if self.dry_run or not os.path.isfile(src):
            return
        if not os.path.exists(dst_path):
            self.mkpath(dst_path)
        dst = make_dst()
        self.debug_print('copying {} to {}...'.format(src, dst))
        dst = shutil.copy(src, dst)
        self.debug_print('copy {} to {}'.format(src, dst))

    def _remove_dst(self, dst: str):
        if not self.dry_run and os.path.exists(dst):
            self.debug_print('Existing path {}. deleting...'.format(dst))
            shutil.rmtree(dst, ignore_errors=True)

    def _copy_voices(self, src: str, dst: str) -> list:
        self.debug_print('Starting voices copying {} to {}...'.format(src, dst))
        voices = []
        with os.scandir(src) as itr:
            for x in itr:
                if (ALL_VOICES or x.name in BASE_VOICES) and os.path.isdir(x.path):
                    voices.append(x.name)
        self._remove_dst(dst)
        for voice in voices:
            self._copy_dir(os.path.join(src, voice), os.path.join(dst, voice))
        return voices

    def _copy_licenses(self, src: str, dst: str, src_voices: str, voices: list):
        self.debug_print('Starting licenses copying...')
        self._copy_dir(src, dst)
        for top_license in os.listdir(src):
            if top_license.lower().startswith('license'):
                self._copy_file(top_license, src, dst)
        for voice in voices:
            src_voice = os.path.join(src_voices, voice)
            for target in os.listdir(src_voice):
                if target.lower().startswith(('license', 'readme')):
                    self._copy_file(target, src_voice, os.path.join(dst, 'voices', voice))

    def _copy_dir(self, src: str, dst: str) -> str:
        def ignore(*_):
            return ['16000', '.gitattributes', '.gitignore', 'CMakeLists.txt', '.git']
        self.debug_print('Starting copying {} to {}...'.format(src, dst))
        self._remove_dst(dst)
        if not self.dry_run:
            dst = shutil.copytree(src, dst, ignore=ignore)
            self.debug_print('copied {} to {}'.format(src, dst))
        return dst

    def run(self):
        src_path = os.path.join(self.build_base, RHVOICE)
        dst_path = os.path.join(self.build_lib, PACKAGE_PATH)
        targets = {
            'voices': (os.path.join(src_path, DATA_DIR, 'voices'), os.path.join(dst_path, DATA_DIR, 'voices')),
            'languages': (os.path.join(src_path, DATA_DIR, 'languages'), os.path.join(dst_path, DATA_DIR, 'languages')),
            'licenses': (os.path.join(src_path, LICENSES_DIR), os.path.join(dst_path, LICENSES_DIR)),
        }

        self.mkpath(self.build_base)
        self.mkpath(self.build_lib)
        [self.mkpath(x) for (_, x) in targets.values()]

        clone = [
            ['git', 'clone', '--recurse-submodules', '--depth=1', '--branch', RHVOICE_TAG, RHVOICE_URL, src_path], None]

        if not os.path.isdir(src_path):
            self.execute(executor, clone, 'Clone {}'.format(RHVOICE_URL))
        else:
            self.warn('Use existing source data from {}'.format(src_path))

        msg = check_build([x for (x, _) in targets.values()])
        if msg is not None:
            raise RuntimeError(msg)

        voices = self._copy_voices(*targets['voices'])
        self._copy_licenses(*targets['licenses'], targets['voices'][0], voices=voices)
        self._copy_dir(*targets['languages'])

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
