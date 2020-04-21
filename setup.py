from os import path
from codecs import open
from setuptools import setup, find_namespace_packages

# get current directory
here = path.abspath(path.dirname(__file__))

# get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# read the API version from disk
with open(path.join(here, 'vantage6', 'tools', 'VERSION')) as fp:
    __version__ = fp.read()

# setup the package
setup(
    name='vantage6-toolkit',
    version=__version__,
    description='vantage6 toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IKNL/vantage6-toolkit',
    packages=find_namespace_packages(),
    python_requires='>=3.6',
    install_requires=[
        'pyjwt'
        # 'vantage6-client'
    ],
    extras_require={
    },
    package_data={
        'vantage6.tools': [
            'VERSION'
        ],
    }
)
