
"""
======================COPYRIGHT/LICENSE START==========================

Path.py: Utility code for CCPN code generation framework

Copyright (C) 2014  (CCPN Project)

=======================================================================
# Licence, Reference and Credits

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
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2017"
__credits__ = ("Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for licence text")
__reference__ = ("For publications, please use reference from http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")
#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-07-07 16:33:16 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: rhf22 $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

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

  """Returns the 'top' directory of the containing repository (AnalysisV3)."""
  func = os.path.dirname
  from ccpn.util import Anchor
  return func(func(func(func(func(Anchor.__file__)))))


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

