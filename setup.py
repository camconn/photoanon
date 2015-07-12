#!/usr/bin/env python3

from setuptools import setup, find_packages
setup(
    name='photoanon',
    version='0.1.0b',
    packages=find_packages(exclude=['tests']),


    package_data={
        # If any package contains *.txt
        'photoanon': ['*.txt'],
    },

    entry_points={
        'console_scripts': [
            'photoanon = photoanon:main',
        ]
    },
    # test_suite='photoanon.test.test',

    # metadata for upload to PyPI
    author='Cameron Conn',
    description='Photo Anonymization Toolkit',
    license='GPLv3',
    keywords='metadata photo image privacy',
    url='http://camconn.cc/introducting-photoanon/',   # project home page, if any

    zip_safe=False,
)
