"""

PDB files
---------
Reading and writing the PDB fiber tract file format.

"""

from distutils.core import setup

setup(name='pdb_files',
      packages = ['pdb_files'],
      package_dir = {'pdb_files':'.'},
      package_data={'pdb_files': ['./*.py']},
      scripts=['./bin/pdb2trk', './bin/trk2pdb'])
