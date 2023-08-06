from setuptools import setup

setup(
    name='apitut_nirmit',
    version='0.2.5',
    description='A tutorial package for creating APIs',
    author='Nirmit Sakre',
    author_email='nirmitsakre@gmail.com',
    packages=['apitut_nirmit'],
    install_requires=[
        'requests',
        'flask',
    ],
)
