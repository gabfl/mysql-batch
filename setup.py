from setuptools import setup

import pypandoc

setup(
    name='mysql_batch',
    version='1.2.2',
    description='Run large MySQL UPDATE and DELETE queries with small batches to prevent table/row-level locks',
    long_description=pypandoc.convert_file('README.md', 'rst'),
    author='Gabriel Bordeaux',
    author_email='pypi@gab.lc',
    url='https://github.com/gabfl/mysql-batch',
    license='MIT',
    packages=['mysql_batch'],
    package_dir={'mysql_batch': 'src'},
    install_requires=[  # external dependencies
        'pymysql==1.1.*'
    ],
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
