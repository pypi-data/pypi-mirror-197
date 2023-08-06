from setuptools import setup

#from superanime import __version__
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='superanime',
    description=("The best package in Python to get anime information and anime gifs!"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    #version=__version__,
    url='https://github.com/MoonlightGroup/anime.py',
    author='Noraa08',
    author_email='rafael.noraa08@gmail.com',
    py_modules=['superanime'],
)