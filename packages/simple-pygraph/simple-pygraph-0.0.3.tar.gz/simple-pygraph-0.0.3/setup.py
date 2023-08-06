from setuptools import setup, find_packages
import os
#import PyGraph
setup(name = 'simple-pygraph',
      version = '0.0.3',
      packages=find_packages(),
      package_data={'':['*']},
      author = 'Sébastien Hoarau',
      author_email = 'seb.hoarau@univ-reunion.fr',
      maintainer = 'Sébastien Hoarau',
      maintainer_email = 'seb.hoarau@univ-reunion.fr',
      keywords = 'PyGraph package Python graph education',
      classifiers = ['Topic :: Education', 'Topic :: Documentation'],
      description = 'Un petit module pour créer des graphes (non orienté, orienté ou bi-partie)',
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
      license = 'CC BY-NC-SA 4.0',
      platforms = 'ALL',
      install_requires=['graphviz', 'networkx'],
     )