from setuptools import setup, find_packages

setup(
    name='project-code',
    version='0.1.0',
    packages=find_packages(include=['code', 'code.*']),
    install_requires=[
        'configparser'
    ]
)