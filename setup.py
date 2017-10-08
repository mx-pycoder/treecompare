#!/usr/bin/env python

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('VERSION') as f:
    version = f.read().lstrip().rstrip()

setup(
    name='treecompare',
    version=version,
    description="simple module and tool to compare two directories",
    url='https://github.com/mx-pycoder/treecompare',
    long_description=readme+"\n\n",
    author="Marnix Kaart",
    author_email='mx@pycoder.nl',
    packages=['treecompare'],
    license="MIT license",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        ],
    keywords='diff tree compare duplicate',
    entry_points={
        'console_scripts': ['treecompare=treecompare.cmdline:main'],
        },
    install_requires=[],
    zip_safe=False,
)
