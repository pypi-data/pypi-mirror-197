"""Install packages as defined in this file into the Python environment."""

from setuptools import setup, find_packages

# The version of this tool is based on the following steps:

# https://packaging.python.org/guides/single-sourcing-package-version/

VERSION = {}

with open("./beesly/__init__.py") as fp:

    # pylint: disable=W0122

    exec(fp.read(), VERSION)

setup(

    name="beesly",

    author="Sachin Sankar",

    author_email="mail.sachinsankar@gmail.com",

    url="https://github.com/Chicken1Geek/beesly",

    description="Web Scraping for Humans",
    long_description = 'Beesly is a web scraping framework with tool sets build upon Beautiful Soup.',

    version=VERSION.get("__version__", "0.0.0"),

    packages=find_packages(where=".", exclude=["tests"]),

    install_requires=[

        "beautifulsoup4",

        "requests",

        "user_agent",

    ],

    classifiers=[

        "Development Status :: 2 - Pre-Alpha",

    ],

)
