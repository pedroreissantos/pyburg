#!/usr/bin/env python
"""A BURG (Bottom-Up Rewrite Grammar) instruction selection compiler generator
	for an AST (Abstract Syntax Tree)
"""

import setuptools

with open("README.md", "r") as fh:
	readme = fh.read()

setuptools.setup(name='pyburg-pkg-peresan',
	version='1.0',
	author='Pedro Reis dos Santos',
	author_email="reis.santos@tecnico.ulisboa.pt",
	description="A BURG (Bottom-Up Rewrite Grammar) instruction selection compiler generator",
	long_description=readme,
	license = 'MIT',
	url="https://github.com/pedroreissantos/pyburg",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
	py_modules = ['pyburg'],
	entry_points = {
		'pburg.1.0': ['pyburg = pyburg:gen',
			'brg2py = brg2py:convert',
			],
	},
)
