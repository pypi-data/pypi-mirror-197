from setuptools import setup, find_packages

setup(
    name="dunnosql",
    version="0.0.6",
    author="https://github.com/Dunno358",
    description="Module to make using MariaDB and PostgreSQL easier and faster",
    packages=find_packages(),
    install_requires=[
        'mariadb',
        'psycopg2'
    ],
)