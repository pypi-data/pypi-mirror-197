# g3t
Fork of Antonio Ragagnin's g3t repository (https://github.com/kyleaoman/g3t), turning it into an installable python package.

**Installation:**
From pypi:
 - 'pip install g3t'

From github:
 - Download via web UI, or 'git clone https://github.com/kyleaoman/g3t.git'
 - Install dependencies if necessary (see setup.py).
 - Global install (Linux): 
   - cd to directory with 'setup.py'
   - run 'sudo pip install -e .' (-e installs via symlink, so pulling repository will do a 'live' update of the installation)
 - User install (Linux):
   - cd to directory with 'setup.py'
   - ensure '~/lib/python3.7/site-packages' or similar is on your PYTHONPATH (e.g. 'echo $PYTHONPATH'), if not, add it (perhaps in .bash_profile or similar)
   - run 'pip install --prefix ~ -e .' (-e installs via symlink, so pulling repository will do a 'live' update of the installation)
 - cd to a directory outside the module and launch python; you should be able to do 'from g3t import *'
