#!/opt/anaconda3/bin/python
# Alan Sun 
# LaTeX Linker: Links many directories containing TeX files and tags together.
# 12/21/21


import os
import re
import json
import sys, getopt, argparse
import glob
import shutil
from .parser import TeXBuilder, TeXParser

parser = argparse.ArgumentParser(description='A linker for TeXControl.')

# Creating a new project.
psub = parser.add_subparsers(title='commands', help='Project management.', dest='command')
pname = psub.add_parser('project', help='Create a new project.')
pname.add_argument('name', help='Name of project.')

# Creating a new chapter.
cname = psub.add_parser('create', help='Create a new chapter.')
cname.add_argument('filename', help='Name of the TeX file.')
cname.add_argument('title', help='Title for the chapter.')
cname.add_argument('template', help='Template TeX file for new chapter.')
cname.add_argument('tags', nargs='+', help='Name of tags for the new chapter.')

# View tags of a project.
vtags = psub.add_parser('viewtags', help='View tags.')
vtags.add_argument('--all', action='store_true', help='View all tags.')
vtags.add_argument('-chpts', nargs='+', help='Name of an individual chapters.')
vtags.add_argument('-tags', nargs='+', help='View all chapters with these tags.')

# Linking
linker = psub.add_parser('link', help='Link project')
linker.add_argument('-tags', nargs='+', help='Provide tags of chapters to be linked' \
					' here we note that unless the --TOR/--TNOT tag is provided then chapters are' \
					' linked according to their intersection of tags.')
linker.add_argument('-chpts', nargs='+', help='Provide individual chapters to be linked')
linker.add_argument('--TOR', action='store_true', help='Changes tag linking to union rather than intersection.')
linker.add_argument('--TNOT', action='store_true', help='Changes tag linking to NOT the given tags rather than intersection')
linker.add_argument('--CNOT', action='store_true', help='Changes chapter linking to NOT the given chapters.')
linker.add_argument('--ALL', action='store_true', help='Link all avaliable chapters.')

def parse_args():
	return parser.parse_args()

def viewtags(_all, chpts, tags):
	fp = open('.txctrl/meta.json', 'r')
	meta = json.load(fp)
	fp.close()
	# Display all tags and their subsequent chapters.
	if _all:
		if len(meta['tags']) == 0:
			print('No tags found.')
		print('---- Tags ----')
		for tag in meta['tags']:
			print(f'* {tag}')	
	if chpts is not None:
		for chpt in chpts:
			if chpt not in meta['chpts']:
				print(f'{chpt} not found.')
				continue
			elif len(meta['chpts'][chpt]['tags']) == 0:
				print(f'{chpt} has no tags.')
				continue
			else:
				print(f'---- {chpt} ----')
				for tag in meta['chpts'][chpt]['tags']:
					print(f'* {tag}')
	if tags is not None:
		for tag in tags:
			print(f'---- {tag} ----')
			for filename, metadata in meta['chpts'].items():
				if tag in metadata['tags']:
					print(f'* {filename}')

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

def create_chapter(filename, title, template, tags):
	"""
	(description): The create_chapter command can be called through 
	'txctrl create [filename] [title] [template] [tags [TAGS]]' each of 
	these are explained in the input section. The command will create a
	directory with the name [filename] with the following subfolders:
		- stys
		- static
	The former represents the stylesheets and the latter represents the static
	files used in the file.

	(input): The `filename` represents the name of the folder that is being
	created. `title` is the title of the TeX document being created. `template`
	is the template TeX file being used in the creation of the chapter. Lastly,
	`tags` is a list of string where each one represents a tag.

	(output): N/A

	TODO: Create a hashtable of tags and chapters.
	"""
	# Add chapter to metadata.
	chpt = {
		'title': title,
		'template': template,
		'tags': tags
	}
	fp = open('.txctrl/meta.json', 'r')
	meta = json.load(fp)
	fp.close()
	fp = open('.txctrl/meta.json', 'w')
	meta['chpts'][filename] = chpt	
	meta['tags'].extend(tags)
	meta['tags'] = list(set(meta['tags']))
	json.dump(meta, fp)
	fp.close()
	# Create chapter subdirectory.
	os.mkdir(filename)
	os.mkdir(f'{filename}/static')
	shutil.copytree('templates/stys/', f'{filename}/stys')
	# Create tags hidden files
	for tag in tags:
		f = open(f'{filename}/.txctrl-{tag}', 'w+')
		f.close()
	# Read template file
	tf = open(f'templates/{template}.tex', 'r')
	template = tf.read()
	tf.close()
	# Copy the template file into the current file and change the name.
	template = re.sub(r'\\title\{.*\}', f'\\\\title{{{title}}}', template)
	f = open(f'{filename}/{filename}.tex', 'w+')
	f.write(template)
	f.close()

def link(tags, chpts, TOR, TNOT, CNOT, ALL):
	# Load metadata
	fp = open('.txctrl/meta.json', 'r')
	meta = json.load(fp)
	fp.close()
	# Figure out which chapters need to be linked.
	linking_chpts = []
	linking_tags = []
	if ALL:
		linking_chpts = meta['chpts'].keys()	
	if chpts:
		if not CNOT:
			for chpt in chpts:
				if chpt in meta['chpts']:
					linking_chpts.append(chpt)
		else:
			for chpt in meta['chpts'].keys():
				if chpt not in chpts:
					linking_chpts.append(chpt)
	if tags:
		if TNOT:
			for tag in meta['tags']:
				if tag not in tags:
					linking_tags.append(tag)
		else:
			linking_tags = tags
		# Find all chapters that have these tags given the logical flags.	
		if TOR:
			for filename, chpt in meta['chpts'].items():
				for tag in chpt['tags']:
					if tag in linking_tags:
						linking_chpts.append(filename)
						break
		else:
			for filename, chpt in meta['chpts'].items():
				flag = True
				for tag in linking_tags:
					if tag not in chpt['tags']:
						flag = False
				if flag:
					linking_chpts.append(filename)
	linking_chpts = set(linking_chpts)
	if len(linking_chpts) == 0:
		print('No chapters with this criterion found.')
		sys.exit(1)
	print('---- Chapters to be linked ----')
	for chpt in linking_chpts:
		print(f' * {chpt}')
	create_linking_environment(linking_chpts)
	create_main_tex(linking_chpts)

def create_main_tex(chpts):
	depend = []
	bodies = []
	# Collect all of the content from each chapter .tex file.
	for chpt in chpts:
		fp = open(f'{chpt}/{chpt}.tex', 'r')
		tex = fp.read()
		tex_parse = TeXParser(tex)
		fp.close()
		# Collect all of the dependencies.
		depend.extend(tex_parse.get_dependencies())
		# Get the title
		title = tex_parse.get_title() 
		# Demote all sections to subsections and subsections to subsubsections.
		tex_parse.replace_environments('subsection', 'subsubsection')
		tex_parse.replace_environments('section', 'subsection')
		# Replace all static links to the main directory static.
		tex_parse.reroute_static(f'static/{chpt}')
		body = tex_parse.get_body()
		bodies.append((title, body))
	bodies.sort(key=lambda x: x[0])
	depend = set(depend)

	# Build dependencies
	main = TeXBuilder()
	main += '\\documentclass[12pt]{article}\n'
	for d in depend:
		main += d + '\n'	
	main += '\\title{Main}\n'
	main += '\\begin{document}\n\maketitle\n'
	for title, bod in bodies:
		bod = re.sub(r'\\maketitle', '', bod)	
		main += r'\section{' + title + '}\n'
		main += bod
		main += '\n'
	main += '\\end{document}'	
	fp = open('main/main.tex', 'w+')
	fp.write(main.btex)
	fp.close()

def create_linking_environment(chpts):
	# Remove existing main directory and everything in it.
	shutil.rmtree('main')
	os.mkdir('main')
	# Copy all static files into the main static directory with
	# appropriate subfolder names.
	os.mkdir('main/static')
	for chpt in chpts:
		shutil.copytree(f'{chpt}/static', f'main/static/{chpt}')
	shutil.copytree('templates/stys', 'main/stys') 	
		
def main():
	args = parse_args()
	if args.command: 
		# Create a new project.
		if args.command == 'project':
			create_project(args.name)	
		# Create a new chapter.
		elif args.command == 'create':
			create_chapter(args.filename, args.title, args.template, args.tags)
		# View tags
		elif args.command == 'viewtags':
			viewtags(args.all, args.chpts, args.tags)
		elif args.command == 'link':
			link(args.tags, args.chpts, args.TOR, args.TNOT, args.CNOT, args.ALL)
	sys.exit(0)	

