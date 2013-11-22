#!/usr/bin/env python
from setuptools import setup, find_packages
execfile('src/beansbooks/version.py')
setup(
    name = "beansbooks",
    version = __version__,
    # pypi stuff
    author = "Dexter Tad-y",
    author_email = "dtady@cpan.org",
    description = "Python Client to the BeansBooks REST API",
    license = "Revised BSD License",
    keywords = [ "beansbooks", "rest", "api", "client" ],
    url = "http://github.com/dexterbt1/beansbooks-py",

    packages = find_packages('src/'),
    package_dir = {
        '': 'src',
    },
    scripts = [],

    install_requires = [
        'requests',
    ],

    test_suite="tests",

    # could also include long_description, download_url, classifiers, etc.
    download_url = 'https://github.com/dexterbt1/beansbooks/tarball/%s' % __version__,
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
