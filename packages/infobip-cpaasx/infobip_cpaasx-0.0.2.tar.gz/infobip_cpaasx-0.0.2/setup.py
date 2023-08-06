# coding: utf-8

"""
    This class is auto generated from the Infobip OpenAPI specification
    through the OpenAPI Specification Client API libraries (Re)Generator (OSCAR),
    powered by the OpenAPI Generator (https://openapi-generator.tech).
"""

from pathlib import Path

from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "infobip_cpaasx"
VERSION = "0.0.2"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = ["urllib3 >= 1.25.3", "python-dateutil", "pydantic", "aenum"]

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name=NAME,
    version=VERSION,
    description="Infobip CPaaS X Python Client Library",
    author="Infobip Ltd.",
    author_email="support@infobip.com",
    url="https://github.com/infobip/infobip-cpaasx-python-client",
    keywords=[
        "sms",
        "mms",
        "numbers",
        "cpaas",
        "infobip"
    ],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="MIT",
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        "Intended Audience :: Telecommunications Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
)
