"""Functions for insertion into memops.Implementaiton.MemopsRoot

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:12 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
import os
from ccpn.util import Path

def isProjectModified(self:'MemopsRoot') -> bool:
  """
  Checks whether any of project has been modified.
  """

  topObjects = (self,) + tuple(self.topObjects)

  for topObject in topObjects:
    if topObject.isModified:
      return True

  return False

def fetchDataUrl(self:'MemopsRoot', fullPath:str) -> 'DataUrl':
  """Get or create DataUrl that matches fullPath, prioritising insideData, alongsideDta, remoteData
  and existing dataUrls"""
  from ccpnmodel.ccpncore.api.memops.Implementation import Url
  standardStore = self.findFirstDataLocationStore(name='standard')
  fullPath = Path.normalisePath(fullPath, makeAbsolute=True)
  standardTags = ('insideData', 'alongsideData', 'remoteData')
  # Check standard DataUrls first
  checkUrls = [standardStore.findFirstDataUrl(name=tag) for tag in standardTags]
  # Then check other existing DataUrls
  checkUrls += [x for x in standardStore.sortedDataUrls() if x.name not in standardTags]
  for dataUrl in checkUrls:
    directoryPath = os.path.join(dataUrl.url.path, '')
    if fullPath.startswith(directoryPath):
      break
  else:
    # No matches found, make a new one
    dirName, path = os.path.split(fullPath)
    dataUrl = standardStore.newDataUrl(url=Url(path=dirName))
  #
  return dataUrl

def fetchNmrProject(self:'MemopsRoot', name:str=None) -> 'NmrProject':
  """Get existing NmrProject from MemopsRoot, or create one if there are no NmrProjects.

  If name is passed in, the function will return a matching NmrProject or throw an error
  If no name is passed, function takes the first NmrProject alphabetically by name
  """

  nmrProjects = self.sortedNmrProjects()
  if nmrProjects:
    if name:
      nmrProject = self.findFirstNmrProject(name=name)
      if nmrProject is None:
        raise ValueError("No NmrProject found with name: %s" % name)
    else:
      nmrProject = nmrProjects[0]
  else:
    nmrProject = self.newNmrProject(name=name or self.name)

  return nmrProject



def upgradeV2toV3(self:'NmrProject'):
  """Load entire project, set to isModified, and rename to name ending in '.ccpn'"""


  pass

  # Load all packages and set to isModified

  # change project name and path
