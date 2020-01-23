"""Functions for insertion into memops.Implementation.MemopsRoot

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2020"
__credits__ = ("Ed Brooksbank, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license")
__reference__ = ("Skinner, S.P., Fogh, R.H., Boucher, W., Ragan, T.J., Mureddu, L.G., & Vuister, G.W.",
                 "CcpNmr AnalysisAssign: a flexible platform for integrated NMR analysis",
                 "J.Biomol.Nmr (2016), 66, 111-124, http://doi.org/10.1007/s10858-016-0060-y")

#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2020-01-23 11:59:50 +0000 (Thu, January 23, 2020) $"
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

def fetchDataUrl(self:'MemopsRoot', fullPath:str, name=None) -> 'DataUrl':
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
    params = {'url':Url(path=dirName)}
    if name:
      params.update({'name':name})
    dataUrl = standardStore.newDataUrl(**params)
    # dataUrl = standardStore.newDataUrl(url=Url(path=dirName))
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
