#!/opt/anaconda3/bin/python
# Alan Sun 
# LaTeX Linker: Links many directories containing TeX files and tags together.
# 12/21/21


import os
import sys, getopt, argparse
import glob

parser = argparse.ArgumentParser(description='A linker for TeXControl.')

# Creating a new project.
psub = parser.add_subparsers(title='project', help='Project management.', dest='command')
pname = psub.add_parser('project', help='Create a new project.')
pname.add_argument('name', help='Name of project.')

parser.add_argument('--viewtags', action='store_true', help='See all avaliable tags.')
parser.add_argument('-title', help='Title for the newly linked file.')
parser.add_argument('-tags', nargs='+', help='Chapters with these tags will be linked.')
parser.add_argument('-chpt', nargs='+', help='Individual chapters with these names will be linked.')


def parse_args():
	return parser.parse_args()

def viewtags(tags):
	tags = []
	for _dir in next(os.walk('.'))[1]:
		for file in os.listdir(_dir):
			if file.startswith('.') and file[1:] not in tags and file != '.DS_Store':
				tags.append(str(file)[1:])
	print('----- Tags -----')
	for tag in tags: print(f'* {tag}')
	sys.exit(0)	

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
	if name is None:
		sys.exit(1)
	# Make the root project directory.
	os.mkdir(name)
	# Make the main directory (where the main file will be compiled)
	# Make the project hidden files: storing tag maps
	os.mkdir(f'{name}/main')
	os.mkdir(f'{name}/templates')
	os.mkdir(f'{name}/.txctrl')	
	sys.exit(0)

def main():
	args = parse_args()
	# Create project
	if args.command and args.command == 'project':
		create_project(args.name)	
	# View all tags
	elif args.viewtags:
		viewtags()
	sys.exit(0)	

###### Parse all tag and file arguments ######
# title = f'{args.title}.tex' if args.title else 'main.tex'
# tags = args.tags
# chpt = args.chpt
# files = []
# 
# if chpt is not None:
# 	for chp in chpt:
# 		if chp in os.listdir('.') and str(chp) not in files:
# 			files.append(str(chp))
# if tags is not None:
# 	for tag in tags:
# 		for _dir in next(os.walk('.'))[1]:
# 			if f'.{tag}' in os.listdir(_dir) and str(_dir) not in files:
# 				files.append(str(_dir))
# 
# if len(files) == 0:
# 	print("No valid chapters provided.")
# 	sys.exit(1)
# 
# print("Chapters to be linked:")
# for file in files: print(f'* {file}')
# 
###### Link tags together. ######
# Create new static folder for static files.
# if 'static' in os.listdir('.'):
# 	os.rmdir('static')
