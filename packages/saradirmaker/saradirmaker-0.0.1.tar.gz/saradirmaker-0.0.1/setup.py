from setuptools import setup, find_packages
import os

# requirements = os.popen("/usr/local/bin/pipreqs mediaquery --print").read().splitlines()
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    
setup(
    name='saradirmaker',
    version='0.0.1',
    author='Saranya',
    author_email='saranyaveeradurai@gmail.com',
    description='It is about file maker cli tool',
    packages=find_packages(),
    install_requires=[
        'pandas'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'saradirmaker=saradirmaker.saradirmaker:main',
        ],
    },
)
