from setuptools import setup, find_packages

from pathlib import Path

dir = Path(__file__).parent
description = (dir / "README.md").read_text()

setup(
    name='superanime',
    description=("The best package in Python to get anime information and anime gifs!"),
    long_description=description,
    long_description_content_type='text/markdown',
    version="1.0.1",
    url='https://github.com/MoonlightGroup/anime.py',
    author='Noraa08',
    author_email='rafael.noraa08@gmail.com',
    #py_modules=['superanime'],
    package_dir = {"": "src"},
    packages = find_packages(where="src"),
)