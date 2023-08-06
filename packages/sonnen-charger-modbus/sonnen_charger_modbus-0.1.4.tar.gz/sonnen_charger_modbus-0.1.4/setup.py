from setuptools import setup, find_packages
import os


def read_file(file):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, file), mode='r', encoding='UTF-8') as file:
        return file.read()


def get_version(file):
    for line in read_file(file).splitlines():
        if line.startswith('__version__'):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError('Version not found!')

setup(
    name='sonnen_charger_modbus',
    version=get_version('sonnen_charger_modbus/__init__.py'),
    packages=find_packages(),
    url='https://github.com/abauske/sonnen_charger_modbus',
    license=read_file('LICENSE'),
    author='Adrian Bauske',
    author_email='adrian.bauske@gmail.com',
    description='Allows to access Sonnen Charger (or any other ETREL INCH) using TCP Modbus',
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    install_requires=[
        'pymodbus~=3.1.3',
    ]
)
