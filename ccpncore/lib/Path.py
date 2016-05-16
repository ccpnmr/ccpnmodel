
"""
======================COPYRIGHT/LICENSE START==========================

Path.py: Utility code for CCPN code generation framework

Copyright (C) 2014  (CCPN Project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published PyChatm30by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

A copy of this license can be found in ../../../license/LGPL.license

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


======================COPYRIGHT/LICENSE END============================

for further information, please contact :

- CCPN website (http://www.ccpn.ac.uk/)

- email: ccpn@bioc.cam.ac.uk

=======================================================================

If you are using this software for academic purposes, we suggest
quoting the following references:

===========================REFERENCE START=============================
R. Fogh, J. Ionides, E. Ulrich, W. Boucher, W. Vranken, J.P. Linge, M.
Habeck, W. Rieping, T.N. Bhat, J. Westbrook, K. Henrick, G. Gilliland,
H. Berman, J. Thornton, M. Nilges, J. Markley and E. Laue (2002). The
CCPN project: An interim report on a data model for the NMR community
(Progress report). Nature Struct. Biol. 9, 416-418.

Rasmus H. Fogh, Wayne Boucher, Wim F. Vranken, Anne
Pajon, Tim J. Stevens, T.N. Bhat, John Westbrook, John M.C. Ionides and
Ernest D. Laue (2005). A framework for scientific data modeling and automated
software development. Bioinformatics 21, 1678-1684.

===========================REFERENCE END===============================

"""

# NBNB must conform tp Python 2.1 (ObjectDomain)

__author__ = 'rhf22'

import os
from ccpnmodel.ccpncore.memops import Version

baseDir = 'versions'

def getPythonDirectory():
  """
  Returns the 'top' python directory, the one on the python path.

  NB equivalent to the function in ccpn.util.Path, but copied here
  in case the repository structure changes in teh future.
  """
  return os.path.dirname(getCcpnmodelDirectory())


def getTopDirectory():

  """Returns the 'top' directory of the containing repository (ccpn)."""
  func = os.path.dirname
  return func(func(getPythonDirectory()))


def getModelDirectory(versionTag):
  """get directory containing model description for versionTag"""
  if versionTag is None:
    version = Version.currentModelVersion
  else:
    version = Version.Version(versionTag)
  return os.path.join(getCcpnmodelDirectory(), baseDir, version.getDirName())

def getCcpnmodelDirectory():
  """get path to ccpnmodel directory"""#
  func = os.path.dirname
  return func(func(func(__file__)))


def _addModuleFunctionsToApiClass(relModuleName, apiClass, rootModuleName='ccpnmodel.ccpncore.lib'):

  # iomport must be here, as importlib is not known in Python 2.1
  import importlib

  moduleName = '%s.%s' % (rootModuleName, relModuleName)
  try:
    module = importlib.import_module(moduleName)
  except ImportError:
    ll = moduleName.split('.')
    ll[-1] += '.py'
    if os.path.exists(os.path.join(getPythonDirectory(), *ll)):
      # The file exists, so there must be an error we should know about
      raise
    else:
      # This happens when there is just no library code for a class - quite common
      pass
    return

  for key in dir(module):

    if key.startswith('_'):
      continue

    value = getattr(module, key)
    # second condition below excludes functions defined in imported modules (like os, etc.)
    # third condition checks whether this is a function (rather than a class, etc.)
    if hasattr(value, '__module__') and value.__module__ == moduleName and callable(value):
      setattr(apiClass, key, value)

