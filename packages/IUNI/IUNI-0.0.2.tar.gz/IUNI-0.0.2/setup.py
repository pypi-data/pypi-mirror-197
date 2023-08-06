from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'IUNI is a reliable, highly versatile and comprehensive testing framework'
LONG_DESCRIPTION = '''The IUNI framework is a highly versatile and comprehensive testing framework designed to provide developers with a
robust toolset for testing software code. The framework offers a unit testing, Web API performance testing and Security
Testing modules.

### More information:
https://github.com/dcohen52/iuni

### Contribution

This project is open source, and contributions from the community are highly valued and appreciated. If you are
interested in contributing to the development of this project, please feel free to reach out or submit a pull request on GitHub.
'''

# Setting up
setup(
    name="IUNI",
    version=VERSION,
    author="Dekel Cohen",
    author_email="<dcohen52@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'testing', 'assertions', 'unit tests', 'functional tests', 'web', 'api testing', 'api',
              'security testing', 'test'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
