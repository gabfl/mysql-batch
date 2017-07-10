from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup (
    name = 'mysql_batch',
    version = '1.0.4',
    description = 'Run large MySQL UPDATE and DELETE queries with small batches to prevent table/row-level locks',
    long_description = long_description,
    author = 'Gabriel Bordeaux',
    author_email = 'pypi@gab.lc',
    url = 'https://github.com/gabfl/mysql-batch-update',
    license = 'MIT',
    packages = ['mysql_batch'],
    package_dir = { 'mysql_batch': 'src' },
    install_requires = ['pymysql', 'argparse'], # external dependencies
    entry_points = {
        'console_scripts': [
            'mysql_batch = mysql_batch.mysql_batch:main',
        ],
    },
)
