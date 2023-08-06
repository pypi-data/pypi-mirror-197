from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'database-code'
LONG_DESCRIPTION = 'database-code'

# Setting up
setup(
    name="database-code",
    version=VERSION,
    author="V. Kalinin",
    author_email="<vkalininz@mail.ru>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['psycopg2', 'psycopg2-binary'],
    keywords=['python', 'database', 'sqlite3', 'postgresql'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)