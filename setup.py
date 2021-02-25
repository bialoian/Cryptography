from setuptools import find_packages, setup
from os import path

NAME = "GS15_Blockchain_KASUMI"
DESC = "Projet GS15 de blockchain simplifiée et implémentation de KASUMI"
VERSION = "0.1"
AUTHOR = "Ian BIALO, Jacques COUDERC"
LICENCE = "MIT"
REQUIRES_PYTHON = ">=3.6.0"

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), 'r') as file:
    LONG_DESC = file.read()

with open(path.join(here, 'requirements.txt'), 'r') as file:
    INSTALL_REQUIRES = file.read().splitlines()

setup(
    name=NAME,
    description=DESC,
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    version=VERSION,
    author=AUTHOR,
    licence=LICENCE,
    python_requires=REQUIRES_PYTHON,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': [
            'gs15_cli=app.__main__:main'
        ]
    }
)
