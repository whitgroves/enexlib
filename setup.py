import setuptools

with open('README.md', 'r') as header:
	long_description = header.read()
	
setuptools.setup(
	name='enexlib',
	version='0.0.2',
	author='whitgroves',
	author_email='whitney.groves@gmail.com',
	description='Extract Evernote backup files (.enex) to plain text.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/whitgroves/enexlib',
	packages=setuptools.find_packages(),
	classifiers=[
		'License :: Public Domain',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.6'
	],
)