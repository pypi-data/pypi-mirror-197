#!/usr/bin/env python

from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

NAME = 'quadx88'

# Import version from file
version_file = open(os.path.join(here, 'VERSION'))
VERSION = version_file.read().strip()

DESCRIPTION = 'Configurable dynamical model of quadcopter'


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=['Ruairi Moran', 'Pantelis Sopasakis'],
      author_email='p.sopasakis@gmail.com',
      license='MIT License',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'numpy', 'scipy', 'pyquaternion', 'control'
      ],
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Science/Research',
          'Topic :: Software Development :: Libraries',
          'Topic :: Scientific/Engineering'
      ],
      keywords=['quadcopter'],
      url=(
          'https://github.com/alphaville/quadx88'
      ),
      zip_safe=False)
