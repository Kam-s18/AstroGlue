# The version file is generated automatically by setuptools_scm
from AstroGlue._version import version as __version__
from .AstroGlue import AstroGlue
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')
  
c = AstroGlue()
c.run()
