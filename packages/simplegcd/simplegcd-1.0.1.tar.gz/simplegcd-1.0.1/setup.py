from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'A package for simple deployment of Google cloud instance groups'

# Setting up
setup(
    name="simplegcd",
    version=VERSION,
    author="Cabe Towers",
    author_email="<cabe.towers@gmail.com>",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['google-cloud-compute'],
    keywords=['python', 'google-cloud', 'google-cloud-compute'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)