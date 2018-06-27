

from setuptools import setup, find_packages

import setuptools.command.test
from linker.version import version

setup(
  name = 'LigoLib',
  packages = ['linking_ext',  'linker','test','test.linker','test.linking' ,'linker.linker_core', 'linker.plugins','linker.reports','linker.config'],
  version = version,
  description = 'PyPi pkg for Linking Library Ligo-lib',
  author = 'Suraiya Khan',
  author_email = 'suraiya.uvic@gmail.com',
  url = 'https://github.com/NovaVic/ligo-lib', # use the URL to the github repo
  keywords = ['Linking', 'Deduplication', 'Record Linkage'], # arbitrary keywords
  classifiers = [
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules",
  ],

   install_requires = [
     'jellyfish==0.5.6',
     'numpy==1.13.1',
     'numexpr==2.6.2',
     'pandas==0.20.3',
     'xhtml2pdf==0.2b1',
     'jinja2==2.9.6',
     'html5lib==1.0b10',
     'coveralls',
     'pytest==3.2.0',
     'pytest-cov==2.5.1',
     'coverage==4.4.1',
     'pep8==1.7.0',
     'pylint==1.7.2',
  ],
 
  include_package_data=True,
  package_dir={'linker': 'linker',
                'linker.linker_core':'linker/linker_core',
                'linker.plugins':'linker/plugins',
                'linker.reports':'linker/reports',
                'linking_ext': 'linking_ext',
                'test':'test',
                'test.linker':'test/linker',
                'test.linking': 'test/linking',
                'linker.config':'linker/config'
  },

  entry_points="""
        [linking.plugins]
        lev_alg = linking_ext.algorithms:Levenshtein
        jaro_alg =  linking_ext.algorithms:JaroWinkler
  """,


  setup_requires=['pytest-runner'],
  tests_require=['pytest'],

)

