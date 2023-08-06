from distutils.core import setup

setup(
	name = 'dbmig',
	version='1.6.2',
	author = 'Julien Demoor',
	author_email = 'julien@jdemoor.com',
        url = 'https://bitbucket.org/msldev/dbmig/',
	license = 'MIT',
	description = 'Simple tool to run SQL migration scripts against an RDBMS. dbmig supports PosgreSQL and should be easy to adapt to any backend supported by SQLAlchemy.',
	packages = ['dbmig'],
	entry_points = {
		'console_scripts': [
		    'dbmig = dbmig.main:main',
		]
    },
	install_requires = [
		'SQLAlchemy',
	],
	zip_safe = False,
	include_package_data = True,
	classifiers=[
	    "License :: OSI Approved :: MIT License",
	    "Programming Language :: Python :: 2",
	    "Programming Language :: Python :: 2.7",
	    "Programming Language :: Python :: 3",
	    "Programming Language :: Python :: 3.10",
        "Topic :: Database"
    ],
)
