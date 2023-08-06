#!/usr/bin/env python

import urllib.request

from localstack_cli import __version__
from setuptools import setup

# download the README.md from the community repo
readme_content = ""
try:
    url = "https://raw.githubusercontent.com/localstack/localstack/master/README.md"
    response = urllib.request.urlopen(url)
    charset = response.info().get_content_charset()
    readme_content = response.read().decode(charset)
except Exception:
    print("Long Description could not be fetched from GitHub.")
    import traceback

    traceback.print_exc()

setup(
    name="lsv2test",
    version=__version__,
    long_description=readme_content,
    long_description_content_type="text/markdown",
    description="LocalStack - A fully functional local Cloud stack",
    author="LocalStack Contributors",
    author_email="info@localstack.cloud",
    url="https://github.com/localstack/localstack",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Internet",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Emulators",
    ],
    install_requires=["lsv2test-core", f"lsv2test-ext=={__version__}"],
    extras_require={
        "runtime": ["lsv2test-core[runtime]", f"lsv2test-ext[runtime]=={__version__}"],
        # TODO remove with 2.0 - full is deprecated, but might still be used
        "full": ["lsv2test-core[runtime]", f"lsv2test-ext[runtime]=={__version__}"],
    },
)
