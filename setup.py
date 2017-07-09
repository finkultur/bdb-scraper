""" A module that scrapes dayviews for images.
See:
https://github.com/finkultur/bdb-scraper
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bdb-scraper',
    version='1.0.2',
    description='Scrapes dayviews for images',
    long_description=long_description,
    url='https://github.com/finkultur/bdb-scraper',
    author='Viktor Nilsson',
    author_email='viktor.w.nilsson@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Sociology :: History',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='popare scraper images',
    packages=find_packages(),
    install_requires=['requests', 'requests_cache', 'simplejson'],

    entry_points={
        'console_scripts': [
            'bdb-scraper = bdb_scraper.__main__:main',
        ],
    },
)
