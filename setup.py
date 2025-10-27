# setup.py
from setuptools import setup, find_packages

setup(
    name="foamfluent2D-cli",
    version="1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'ff2=CLI.main:foam_fluent_2D',
        ],
    },
)
