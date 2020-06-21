"""The setup.py file for ASANN."""

from setuptools import setup


with open("README.md", "r") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

SHORT_DESCRIPTION = """
Implementation of the ASANN algorithm.""".strip()

DEPENDENCIES = [
    'numpy',
    'six',
]

EXTRA_DEPENDENCIES = {
    'ASE': ['ase'],
    'Pymatgen': ['pymatgen'],
}

VERSION = '1.0.0'
URL = 'https://github.com/RubenStaub/ASANN'


setup(
    name="asann",
    version=VERSION,
    author="Ruben Staub",
    author_email="ruben.staub@ens-lyon.fr",
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
    extra_require=EXTRA_DEPENDENCIES,
    install_requires=DEPENDENCIES,
)
