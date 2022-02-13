import os
import sys
import json


def create_project(name):
	"""
	(description): The create_project command can be called through 'txctrl project [name]'.
	It will create a folder called [name] in the calling directory. Then,
	it will create the `main` directory, where all of the compiled main files
	will live. The function will also create the hidden subdirectory that stores metadata.

	(input): String, name of the project.

	(output): N/A

	(error handling): If name is None, exit with non-zero status.
	"""
	meta = {
		'proj_name': name,
		'chpts': {},
		'tags': [],
	}

	if name is None:
		sys.exit(1)
	# Make the root project directory.
	os.mkdir(name)
	# Make the main directory (where the main file will be compiled)
	# Make the project hidden files: storing tag maps
	os.mkdir(f'{name}/main')
	os.mkdir(f'{name}/templates')
	os.mkdir(f'{name}/templates/stys')
	os.mkdir(f'{name}/.txctrl')	
	# Create json file to store metadata.
	fp = open(f'{name}/.txctrl/meta.json', 'w+')
	json.dump(meta, fp)
	fp.close()
	sys.exit(0)


