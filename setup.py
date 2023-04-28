from setuptools import setup, find_packages

setup(
    name='CursedMage',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'pyinstaller',
        'pytest'
    ],
)