"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
              "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                " or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================
"""Scrips to (re)create project sphinx documentation"""

__author__ = 'rhf22'

from ccpn.util import Path as corePath
import subprocess
import os
import shutil
from sphinx import apidoc

joinPath = corePath.joinPath


# Relative path to documentation directory
documentationPath = 'doc'

def refreshSphinxDocumentation():
  """(Re)create sphinx documentation. Locations are hardwired"""

  pythonDirectory = corePath.getPythonDirectory()
  docDirectory = joinPath(corePath.getTopDirectory(), documentationPath)

  # Remove sphinx-apidoc files
  for ss in ('ccpn', 'ccpncore', 'application'):
    inDirectory = joinPath(docDirectory, 'source', ss)
    if os.path.exists(inDirectory):
      print ("Removing %s" % inDirectory)
      shutil.rmtree(inDirectory)
    os.mkdir(inDirectory)

  # clean builds
  subprocess.call(['make', '-C', docDirectory, 'clean'])

  # Recreate apidoc
  # The parameters are command, option, output directory, module to document, dirs to skip
  # First ccpncore
  ll = ['../doc/source/ccpncore', 'ccpncore',
        'ccpncore/memops/', 'ccpncore/testing/', 'ccpncore/xml/', 'ccpncore/api',
        'ccpncore/lib/Bmrb/unit_tests']
        #'ccpncore/gui', 'ccpncore/memops/', 'ccpncore/testing/', 'ccpncore/xml/']
  ll = ['sphinx-apidoc', '-o'] + [joinPath(pythonDirectory, xx) for xx in ll]
  apidoc.main(ll)
  #
  #
  # # then ccpn.ui.gui
  ll = ['../doc/source/application', 'application']
  ll = ['sphinx-apidoc', '-o'] + [joinPath(pythonDirectory, xx) for xx in ll]
  apidoc.main(ll)

  # then ccpn
  ll = ['../doc/source/ccpn', 'ccpn', 'ccpn/lib/wrapper']
  ll = ['sphinx-apidoc', '-o'] + [joinPath(pythonDirectory, xx) for xx in ll]
  apidoc.main(ll)
  #subprocess.call(ll)

  #subprocess.call(ll)

  # rebuild docs
  subprocess.call(['make', '-C', docDirectory, 'html'])

if __name__ == '__main__':
  refreshSphinxDocumentation()