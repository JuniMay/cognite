from setuptools import setup

setup(
    name='cognite',
    version='0.0.1',
    packages=['cognite'],
    entry_points={'console_scripts': ['cognite=cognite.main:main']},
)