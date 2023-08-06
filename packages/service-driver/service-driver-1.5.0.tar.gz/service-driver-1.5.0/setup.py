from __future__ import absolute_import
import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('service_driver/_version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('requirements.txt') as f:
    requirements = [line for line in f.read().splitlines() if line]

setup(
    name='service-driver',
    description='api test framework cli',
    version=version,
    author='CHNJX',
    author_email='360088940@qq.com',
    url='https://github.com/JxcChen/service-driver',
    packages=['service_driver','service_driver.utils'],
    package_data={'templates': ['service_driver/templates/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'sdrun=service_driver:cmd'
        ]
    },
    install_requires=requirements,
    tests_require=['pytest'],
)
