#!/usr/bin/env python3
from setuptools import setup, find_packages
setup(
    name='photoanon',
    version='0.1.0a',
    packages=find_packages(exclude=['tests']),
    scripts=['src/photoanon.py'],

    # We need numpy and scipy
    setup_requires=['numpy'],
    install_requires=['numpy', 'scipy>=0.15.1'],

    package_data={
        # If any package contains *.txt
        '': ['*.txt'],
        #'photoanon': ['src/photoanon/*'],
    },

    entry_points={
        'console_scripts': [
            'photoanon = photoanon.photoanon:_main',
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
