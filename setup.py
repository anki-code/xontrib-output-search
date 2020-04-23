#!/usr/bin/env python
from setuptools import setup

try:
    with open('README.md') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = ''

setup(
    name='xontrib-fishout',
    version='0.1.0',
    license='BSD',
    author='anki',
    author_email='author@example.com',
    description="Fish out new arguments from previous command output in xonsh",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['xontrib'],
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['fishout.py']},
    platforms='any',
    url='https://github.com/anki-code/xontrib-fishout',
    project_urls={
        "Documentation": "https://github.com/anki-code/xontrib-fishout/blob/master/README.md",
        "Code": "https://github.com/anki-code/xontrib-fishout",
        "Issue tracker": "https://github.com/anki-code/xontrib-fishout/issues",
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Unix Shell",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: BSD License"
    ]
)
