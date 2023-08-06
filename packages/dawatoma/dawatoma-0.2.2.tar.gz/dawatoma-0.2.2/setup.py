from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='dawatoma',
      version='0.2.2',
      packages=find_packages(),
      description='DAW Automation - music idea generation software',
      long_description=long_description,
      long_description_content_type='text/markdown',
      package_dir={'':'.'},
      install_requires=[
        "MIDIUtil>=1.2.1",
        "attrs>=21.2.0"
        ],
      author='MrMultiMediator',
      author_email='mrmultimediator@gmail.com',
      url='https://www.mrmultimediator.github.io/',
     )

"""
setup(name='dawatoma',
      version='0.2.1b3',
      description='DAW Automation: music idea generation software',
      package_dir={'':'dawatoma'},
      packages=find_packages('dawatoma'),
      install_requires=[
        "MIDIUtil>=1.2.1",
        "attrs>=21.2.0"
        ],
      author='MrMultiMediator',
      author_email='mrmultimediator@gmail.com',
      url='https://www.mrmultimediator.github.io/',
     )
"""
