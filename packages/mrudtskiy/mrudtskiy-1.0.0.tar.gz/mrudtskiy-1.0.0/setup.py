from setuptools import setup, find_packages

setup(
    name = 'mrudtskiy',
    packages=find_packages(exclude=['mrudtskiy']),
    version = '1.0.0',
    py_modules = ['mrudtskiy'],
    author = 'Max',
    author_email = 'max@mail.ru',
    description = 'A simple printer of nested lists',
)