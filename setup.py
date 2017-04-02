import io
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--pylint']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    author='Jonathan Sharpe',
    author_email='mail@jonrshar.pe',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat',
        'Topic :: Text Processing :: Linguistic',
    ],
    cmdclass={'test': PyTest},
    description='The code powering @eleanorrigbot',
    install_requires=['pronouncing', 'tweepy'],
    license='License :: OSI Approved :: ISC License (ISCL)',
    long_description=long_description,
    name='eleanorrigbot',
    packages=['eleanorrigbot'],
    platforms='any',
    scripts=['scripts/launch_rigbot.py'],
    tests_require=['mock', 'pytest', 'pytest-pylint'],
    url='https://github.com/textbook/eleanor-rigbot',
    version='0.3.0',
)
