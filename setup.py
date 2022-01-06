from setuptools import setup, find_packages


setup(
	name='TeX Control',
	version='1.0',
    py_modules='txctrl',
	install_requires=[
		'Click',
	],
	entry_points="""
		[console_scripts]
        txctrl=txctrl.main:main
	""",
)
