import os
import json


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


