#!/usr/bin/env python
from setuptools import setup

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = ''

setup(
    name='xontrib-output-search',
    version='0.6.3',
    license='BSD',
    author='anki-code',
    author_email='author@example.com',
    description="Get identifiers, names, paths, URLs and words from the previous command output and use them for the next command in xonsh.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['tokenize-output'],
    packages=['xontrib'],
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['output_search/*.py']},
    platforms='any',
    url='https://github.com/anki-code/xontrib-output-search',
    project_urls={
        "Documentation": "https://github.com/anki-code/xontrib-output-search/blob/master/README.md",
        "Code": "https://github.com/anki-code/xontrib-output-search",
        "Issue tracker": "https://github.com/anki-code/xontrib-output-search/issues",
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
