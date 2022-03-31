from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

setup(console=['main.py'],
      options = {
          'py2exe': {
                'packages': ['vtkmodules.all', 'mat73', 'h5py', 'qtpy']
            }
      })