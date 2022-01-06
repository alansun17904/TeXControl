import json
import shutil


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


