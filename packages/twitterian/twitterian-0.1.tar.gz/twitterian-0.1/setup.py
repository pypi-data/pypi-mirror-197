from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='twitterian',
    version='0.1',
    description='An easy way to interact with twitter',
    author='Omid Roshani',
    author_email='omid@texoom.net',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[line.strip() for line in open('requirements.txt')],
)