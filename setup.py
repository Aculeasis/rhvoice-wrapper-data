import os
import shutil
import stat
import subprocess
import sys

from setuptools import setup
from setuptools.command.install import install

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = _bdist_wheel.get_tag(self)
            python, abi = 'py{}'.format(sys.version_info[0]), 'none'
            return python, abi, plat
except ImportError:
    bdist_wheel = None


PACKAGE_PATH = 'rhvoice_wrapper_data'
RHVOICE_PATH = 'RHVoice'
build_sh = './build.sh'
libraries_path = [
    os.path.join(RHVOICE_PATH, 'build/linux/core/libRHVoice_core.so'),
    os.path.join(RHVOICE_PATH, 'build/linux/lib/libRHVoice.so')
]
data_paths = [
    os.path.join(RHVOICE_PATH, 'data/languages'),
    os.path.join(RHVOICE_PATH, 'data/voices')
]


def _1_build():
    st = os.stat(build_sh)
    os.chmod(build_sh, st.st_mode | stat.S_IEXEC)
    run = subprocess.run([build_sh])
    if run.returncode != 0:
        return 'Failed RHVoice building: {}'.format(run.returncode)


def _2_check_build():
    for target in libraries_path:
        if not os.path.isfile(target):
            return 'File {} not found'.format(target)
    for target in data_paths:
        if not os.path.isdir(target):
            return 'Directory {} not found'.format(target)


def _3_copy_data(build_path, package_data_path):
    for target in libraries_path:
        dst = shutil.copy(target, build_path)
        st = os.stat(dst)
        os.chmod(dst, st.st_mode | stat.S_IEXEC)
    if os.path.isdir(package_data_path):
        shutil.rmtree(package_data_path, ignore_errors=True)
    os.mkdir(package_data_path)
    for target in data_paths:
        shutil.copytree(target, os.path.join(package_data_path, os.path.basename(target)), ignore=_ignore_install)


def _4_build_clear():
    shutil.rmtree(RHVOICE_PATH, ignore_errors=True)
    st = os.stat(build_sh)
    os.chmod(build_sh, st.st_mode ^ stat.S_IEXEC)


def _ignore_install(src, names):
    # Only 24000 adding
    if '16000' in names and os.path.isdir(os.path.join(src, '16000')) and '24000' in names:
        return ['16000']
    return []


class Install(install):
    def run(self):
        build_path = os.path.join(self.build_lib, PACKAGE_PATH)
        package_data_path = os.path.join(build_path, 'data')
        err = _1_build() or _2_check_build() or _3_copy_data(build_path, package_data_path)
        _4_build_clear()
        if err:
            RuntimeError(err)
        super().run()
        if os.path.isdir(build_path):
            shutil.rmtree(build_path, ignore_errors=True)


with open('README.md') as fh:
    long_description = fh.read()

with open('version') as fh:
    version = fh.read().splitlines()[0]

setup(
    name='rhvoice-wrapper-data',
    version=version,
    packages=[PACKAGE_PATH],
    url='https://github.com/Aculeasis/rhvoice-wrapper-data',
    platforms='linux',
    license='GPLv3+',
    author='Aculeasis',
    author_email='amilpalimov2@ya.ru',
    description='Provides RHVoice libraries and data for rhvoice-wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: C++'
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=False,
    cmdclass={'install': Install, 'bdist_wheel': bdist_wheel},
)
