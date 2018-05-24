from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='mysql_batch',
    version='1.2',
    description='Run large MySQL UPDATE and DELETE queries with small batches to prevent table/row-level locks',
    long_description=long_description,
    author='Gabriel Bordeaux',
    author_email='pypi@gab.lc',
    url='https://github.com/gabfl/mysql-batch',
    license='MIT',
    packages=['mysql_batch'],
    package_dir={'mysql_batch': 'src'},
    install_requires=['pymysql', 'argparse'],  # external dependencies
    entry_points={
        'console_scripts': [
            'mysql_batch = mysql_batch.mysql_batch:main',
        ],
    },
    classifiers=[  # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Topic :: Software Development',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        #  'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
    ],
)
