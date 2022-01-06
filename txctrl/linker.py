import os
import re
import json
import sys, getopt, argparse
import glob
import shutil
from .parser import TeXBuilder, TeXParser


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
		
