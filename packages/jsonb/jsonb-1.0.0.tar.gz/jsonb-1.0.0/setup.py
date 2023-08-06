from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='jsonb',
	version='1.0.0',
	description='JSON Better - A Python Library Used to simplify encoding/decoding JSON while handling special types',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/ouroboroscoding/jsonb',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/jsonb',
		'Tracker': 'https://github.com/ouroboroscoding/jsonb/issues'
	},
	keywords=['jsonb'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['jsonb'],
	python_requires='>=3.10',
	install_requires=[],
	zip_safe=True
)