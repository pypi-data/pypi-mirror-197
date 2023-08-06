from setuptools import setup

import re
from pathlib import Path

dir = Path(__file__).parent
description = (dir / "README.md").read_text()

f = (dir / "superanime" / "__init__.py").read_text()
version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f, re.MULTILINE).group(1)

setup(
    name='superanime',
    description=("The best package in Python to get anime information and anime gifs!"),
    long_description=description,
    long_description_content_type='text/markdown',
    version=version,
    url='https://github.com/MoonlightGroup/anime.py',
    author='Noraa08',
    author_email='rafael.noraa08@gmail.com',
    py_modules=['superanime'],
)