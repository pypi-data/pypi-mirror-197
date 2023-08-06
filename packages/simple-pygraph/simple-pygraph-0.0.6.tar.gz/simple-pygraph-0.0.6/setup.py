from setuptools import setup, find_packages
import os
#import PyGraph
setup(name = 'simple-pygraph',
      version = '0.0.6',
      packages=find_packages(),
      package_data={'':['*']},
      author = 'Sébastien Hoarau',
      maintainer = 'Sébastien Hoarau',
      url='https://gitlab.com/sebhoa/pygraph',
      keywords = 'PyGraph package Python graph education',
      classifiers = ['Topic :: Education', 'Topic :: Documentation'],
      description = 'Un petit module pour créer des graphes (non orienté, orienté ou bi-partie)',
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
      license = 'CC BY-NC-SA 4.0',
      platforms = 'ALL',
      install_requires=['graphviz', 'networkx'],
     )