from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mysql_batch',
    version='1.3.0',
    description='Run large MySQL UPDATE and DELETE queries with small batches to prevent table/row-level locks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gabriel Bordeaux',
    author_email='pypi@gab.lc',
    url='https://github.com/gabfl/mysql-batch',
    license='MIT',
    packages=['mysql_batch'],
    package_dir={'mysql_batch': 'src'},
    python_requires='>=3.9',
    install_requires=[  # external dependencies
        'pymysql>=1.1.1,<2'
    ],
    entry_points={
        'console_scripts': [
            'mysql_batch = mysql_batch.mysql_batch:main',
        ],
    },
    classifiers=[  # see https://pypi.org/classifiers/
        'Topic :: Software Development',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Development Status :: 5 - Production/Stable',
    ],
)
