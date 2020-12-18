#!/usr/bin/env python
"""A BURG (Bottom-Up Rewrite Grammar) instruction selection compiler generator
	for an AST (Abstract Syntax Tree)
"""

import setuptools

with open("README.md", "r") as fh:
	readme = fh.read()

setuptools.setup(name='pyburg-pkg-peresan',
	version='1.4',
	author='Pedro Reis dos Santos',
	author_email="reis.santos@tecnico.ulisboa.pt",
	description="A BURG (Bottom-Up Rewrite Grammar) instruction selection compiler generator",
	long_description=readme,
	license = 'MIT',
	url="https://github.com/pedroreissantos/pyburg",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Compilers',
		'Development Status :: 3 - Alpha',
		# 'Development Status :: 4 - Beta',
		'Environment :: Console',
	],
	python_requires='>=3.6',
	install_requires=[ 'ply', ],
	py_modules = ['pyburg','postfix','Tree','brg2py','strbuf'],
	packages=setuptools.find_packages(),
)
