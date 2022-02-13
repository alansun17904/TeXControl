# Alan Sun 
# LaTeX Linker: Links many directories containing TeX files and tags together.
# 12/21/21


import os
import glob
import json
import sys, getopt, argparse

from .project import create_project
from .create import create_chapter
from .viewtags import viewtags
from .linker import link

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
linker.add_argument('-template', help='A template for the main linked document')
linker.add_argument('-chpts', nargs='+', help='Provide individual chapters to be linked')
linker.add_argument('--TOR', action='store_true', help='Changes tag linking to union rather than intersection.')
linker.add_argument('--TNOT', action='store_true', help='Changes tag linking to NOT the given tags rather than intersection')
linker.add_argument('--CNOT', action='store_true', help='Changes chapter linking to NOT the given chapters.')
linker.add_argument('--ALL', action='store_true', help='Link all avaliable chapters.')

def parse_args():
	return parser.parse_args()


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
			link(args.tags, args.chpts, args.TOR, args.TNOT, args.CNOT, args.ALL, args.template)
	sys.exit(0)	


if __name__ == '__main__':
    main()
