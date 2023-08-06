from setuptools import setup

import re
from pathlib import Path

with open('superanime/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='superanime',
    description=("The best package in Python to get anime information and anime gifs!"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    url='https://github.com/MoonlightGroup/anime.py',
    author='Noraa08',
    author_email='rafael.noraa08@gmail.com',
    py_modules=['superanime'],
)