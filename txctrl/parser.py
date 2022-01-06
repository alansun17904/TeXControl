import re


class TeXBuilder:
	def __init__(self):
		self.tex = ''

	def __iadd__(self, s):
		self.tex += s
		return self

	@property
	def btex(self):
		return self.tex


class TeXParser:
	def __init__(self, tex):
		self.tex = tex

	def get_title(self):
		title = re.findall(r'\\title\{(.+)\}', self.tex)
		if len(title) == 0:
			return ''
		else:
			return title[0]

	def get_body(self):
		bsearch = re.search(r'\\begin\{document\}((.|\n)*)\\end\{document\}', self.tex)
		if bsearch is not None:
			return bsearch.group(1)
		return None

	def get_dependencies(self):
		dependencies = re.findall(r'\\usepackage.*\{.*\}', self.tex)
		return dependencies

	def replace_environments(self, environ, repl):
		self.tex = re.sub(r'\\' + environ, r'\\' + repl, self.tex)

	def reroute_static(self, repl):
		# Replace \include
		self.tex = re.sub(r'\\include{(.*)}', r'\\include{' + repl + '/\1}', self.tex)
		# Replace \input
		self.tex = re.sub(r'\\input{(.*)}', r'\\input{' + repl + '/\1}', self.tex)
		# Replace \includegraphics
		self.tex = re.sub(r'\\includegraphics{(.*)}', r'\\includegraphics{' + repl + '/\1}', self.tex)


