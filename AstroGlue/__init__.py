# The version file is generated automatically by setuptools_scm
from AstroGlue._version import version as __version__
from .AstroGlue import AstroGlue
import os

os.environ["MPLBACKEND"] = "agg"
  
c = AstroGlue()
c.run()
