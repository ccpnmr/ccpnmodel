"""
Module Documentation here
"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
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
__dateModified__ = "$dateModified: 2017-07-07 16:33:22 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

""" Generate autogenerated files from model
All data are read from and written to a file tree of the structure given by
the code repository.
Default is to use the same file tree as the code is loaded from,
determined as the tree that contains memops.universal.constants.

======================COPYRIGHT/LICENSE START==========================

makePython.py: Code generation for CCPN framework

Copyright (C) 2005 Rasmus Fogh (CCPN Project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.
 
A copy of this license can be found in ../../../license/GPL.license
 
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.
 
You should have received a copy of the GNU General Public
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

import time


from ccpnmodel.ccpncore.memops.metamodel import XmlModelIo
from ccpnmodel.ccpncore.memops.metamodel.ModelPortal import ModelPortal

from ccpnmodel.ccpncore.memops.scripts.core import PyFileModelAdapt
from ccpnmodel.ccpncore.memops.scripts.api import PyFileApiGen
from ccpnmodel.ccpncore.memops.scripts.xmlio import PyXmlMapWrite

defaultIgnoreModules = []

def getModelPortal(dataModelVersion=None, includePackageNames=None,
                   excludePackageNames=None):
  """ get adapted ModelPortal
  
  - dataModelVersion object of version to generate(default: current)
  - includePackageNames: package qualified names to generate from;
    only leaf package names should be put in includePackageNames.
  - excludePackageNames: qualified names of packages that will be 
    ignored together with their contents.
  """
  # load model
  topPackage = XmlModelIo.readModel(dataModelVersion, includePackageNames=includePackageNames,
                                    excludePackageNames=excludePackageNames)
  
  start = time.time()
  modelPortal = ModelPortal(topPackage, dataModelVersion=dataModelVersion)
  end = time.time()
  print("""
  Memops made ModelPortal, time %s
  """ % (end-start))
  
  # pre-process model
  start = time.time()
  PyFileModelAdapt.processModel(modelPortal)
  end = time.time()
  print("""
  Memops done FileAdapt, time %s
  """ % (end-start))
  
  #
  return modelPortal

def makePython(modelPortal, rootDirName=None, rootFileName=None, 
               releaseVersion=None, ignoreModules=None):
  """ Generate all python relevant code for a version
  - rootDirName: topmost directory to write to (defaults to current cvsroot)
  - rootFileName: file/dir name for root package (defaults to 'RootPackage')
  - releaseVersion: release version object (defaults to  'unknown')
  """
  
  
  if ignoreModules is None:
    # modules known not to import - should not be checked
    ignoreModules = defaultIgnoreModules
    
  # generate XML map
  start = time.time()
  PyXmlMapWrite.writeXmlIo(modelPortal, rootDirName=rootDirName,
   rootFileName=rootFileName, releaseVersion=releaseVersion)
  end = time.time()
  print("""
  Memops done XML map generation, time %s
  """ % (end-start))
  
  # generate API
  start = time.time()
  PyFileApiGen.writeApi(modelPortal, rootDirName=rootDirName,
   rootFileName=rootFileName, releaseVersion=releaseVersion)
  end = time.time()
  print("""
  Memops done Api generation, time %s
  """ % (end-start))


        

if __name__ == '__main__':
  

  makePython(getModelPortal())
