# -*- coding: utf-8 -*-

# Learn more: https://github.com/erwingforerocastro/mvfy_visual

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9'
]

setup(
    name='mvfy_visual',
    version='0.0.5',
    description='Package mvfy_visual',
    # long_description = readme,
    author='Erwing Forero',
    author_email='erwingforerocastro@gmail.com',
    url='https://github.com/erwingforerocastro/mvfy_visual',
    license=license,
    keywords = ['python', 'video', 'streaming', 'opencv', 'face recognition', 'mongodb'],
    classifiers=classifiers,
    py_modules=['mvfy'],
    package_dir={"": "mvfy"},
    packages=find_packages(where="mvfy", exclude=('test','docs'))
)