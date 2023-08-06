#!/usr/bin/env python
from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from streamtask.version import __version__

setup(
    name='streamtask',
    version=__version__,
    description='Parallel Stream Task for Python',
    url='https://github.com/fuzihaofzh/streamtask',
    author='',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Parallel Stream Task',
    packages=find_packages(),
    install_requires=[
          'tqdm',
    ],
    #entry_points={
    #      'console_scripts': [
    #          'cam = cam.cam:main'
    #      ]
    #},
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)