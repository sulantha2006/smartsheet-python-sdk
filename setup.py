from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

NAME = 'smartsheet-python-sdk'

REQUIRES = [
    'requests',
    'requests-toolbelt',
    'six >= 1.9',
    'certifi',
    'python-dateutil'
]

if sys.version_info < (3, 4):
    REQUIRES.append('enum34')

# test packages:
# https://github.com/pytest-dev/pytest

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        if isinstance(self.pytest_args, str ):
            self.pytest_args = [self.pytest_args]
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name=NAME,
    description='Library that uses Python to connect to Smartsheet services (using API 2.0).',
    author='Smartsheet',
    author_email='sdk@smartsheet.com',
    url='http://smartsheet-platform.github.io/api-docs/',
    license='Apache-2.0',
    keywords=['Smartsheet', 'Collaboration', 'Project Management', 'Excel', 'spreadsheet'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
    use_scm_version={
        'write_to': 'smartsheet/version.py'
    },
    setup_requires=['setuptools_scm'],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    extras_require={
        'test': [
            'coverage',
            'coveralls',
            'pytest'
        ],
        'develop': [
            'coverage',
            'coveralls[yaml]',
            'pytest',
            'pytest-instafail'
        ]
    },
    tests_require=['pytest', 'pytest-rerunfailures'],
    cmdclass={
        'test': PyTest
    }
)
