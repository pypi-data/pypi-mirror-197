#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: PavukEdya, Sou1Guard
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2023 PavukEdya, Sou1Guard
"""

version = '1.0.3'

# with open('README.md', encoding='utf-8') as f:
#     long_description = f.read()


setup(
    name='imagesim',
    version=version,

    author='PavukEdya',
    author_email='slaefir@mail.ru',

    description=(
        u'Python module for get different between two images'
    ),
    long_description=(
        u'Python module for get different between two images'
        u'class ImagesDifferences with two functions:'
        u'1) get_median_frame(video_name)'
        u'2) check_differences(image1, image2, accuracy=0.85)'
    ),
    long_description_content_type='text/markdown',

    url='https://github.com/PavukEdya',
    download_url='https://github.com/PavukEdya',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['imagesim'],
    install_requires=['numpy', 'scikit-image', 'opencv-python'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        ]
    )
