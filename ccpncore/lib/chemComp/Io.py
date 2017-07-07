"""!/O functions for ChemComp handling

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:13 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
"""Code for ChemComp I/O"""

#
# Convenient I/O functions
#

import os
import re
from ccpn.util import  Url

from ccpnmodel.ccpncore.lib.Io import Api as apiIo
from ccpn.util import Common as commonUtil
from ccpn.util import Path as corePath
from ccpnmodel.ccpncore.memops.format.xml import XmlIO

from ccpnmodel.ccpncore.lib.Constants import standardResidueCcpCodes


def fetchChemComp(project, molType, ccpCode, download=True, partialLoad=False):
  """ get ChemComp corresponding to molType,ccpCode, 
  looking 1) in memory, 2) in Repositories on lookup path,
  3)  downloading from PDBe ChemComp server.
  For 3) save new ChemComp in first Repository on PackageLocator lookup path
  Do 3) only if download==True

  partialLoad controls if only the TopObject (default) or the entire file is loaded
  
  copyFile can be set to False to avoid copying file from central archive (good for testing)
  
  Optimised to avoid mass reading.
  """
  
  
  # First get it if already loaded
  # 1 May 10: below returns None if chemComp not already loaded
  # and then XmlIO.loadFromFile sets chemComp.isModified to True
  # which means that chemComp is saved
  #chemComp = project.getByNavigation(('chemComps',(molType,ccpCode)))
  chemComp = project.findFirstChemComp(molType=molType,ccpCode=ccpCode)
  
  if chemComp is None:
    # try to load it from an existing repository - avoiding mass loading
    packageName = 'ccp.molecule.ChemComp'  
    chemCompFileSearchString = "%s+%s+*.xml" % (molType,commonUtil.getCcpFileString(ccpCode))
    
    chemCompXmlFile = apiIo.findCcpXmlFile(project, packageName, chemCompFileSearchString)
    if chemCompXmlFile:
      chemComp = XmlIO.loadFromFile(project, chemCompXmlFile, partialLoad=partialLoad)

    if chemComp is None:
      if molType == 'dummy':
        chemComp = project.newNonStdChemComp(molType=molType, ccpCode=ccpCode, code3Letter=ccpCode)
        chemComp.newChemCompVar(linking='dummy', descriptor='neutral', isDefaultVar=True,
                                formalCharge=0, isParamagnetic=False, isAromatic=False)
      elif download:

        ccLocator = (project.findFirstPackageLocator(targetName=packageName) or
                     project.findFirstPackageLocator(targetName='any'))
        repository = ccLocator.findFirstRepository()

        fileFound = downloadChemCompInfoFromCcpForge(repository, molType, ccpCode)
        if fileFound:
          chemComp = XmlIO.loadFromFile(project, fileFound,  partialLoad=partialLoad)
  #
  return chemComp
  
def getChemCompArchiveXmlFilePath(chemCompPath,molType,ccpCode):
    
  chemCompXmlFilePath = corePath.joinPath(chemCompPath,molType)
  
  if molType == 'other':
    chemCompXmlFilePath = corePath.joinPath(chemCompXmlFilePath,ccpCode[0])
  
  return chemCompXmlFilePath

 
def getChemCompCoordArchiveXmlFilePath(chemCompPath,sourceName,molType,ccpCode):
    
  chemCompXmlFilePath = corePath.joinPath(chemCompPath,sourceName,molType)
  
  if molType == 'other':
    chemCompXmlFilePath = corePath.joinPath(chemCompXmlFilePath,ccpCode[0])
  
  return chemCompXmlFilePath

def fetchChemCompCoord(project, sourceName, molType, ccpCode, download=True, partialLoad=False):
  """ get ChemComp corresponding to molType,ccpCode,
  looking 1) in memory, 2) in Repositories on lookup path,
  3) in allChemCompCoordPath directory, 4) downloading from PDBe ChemComp server.
  For 3) and 4) save new ChemComp in first Repository on PAckageLocator lookup path
  Do 4) only if download==True

  partialLoad controls if only the TopObject (default) or the entire file is loaded
  
  copyFile can be set to False to avoid copying file from central archive (good for testing)
  
  Optimised to avoid mass reading.
  """
  
  
  # First get it if already loaded
  chemCompCoord = project.getByNavigation(('chemCompCoords',(sourceName,molType,ccpCode)))
  
  if chemCompCoord is None:
    # try to load it from an existing repository - avoiding mass loading
    packageName = 'ccp.molecule.ChemCompCoord'  
    chemCompCoordFileSearchString = "%s+%s+%s+*.xml" % (commonUtil.getCcpFileString(sourceName),
                                                        molType, commonUtil.getCcpFileString(ccpCode))
    
    chemCompCoordXmlFile = apiIo.findCcpXmlFile(project, packageName,
                                                 chemCompCoordFileSearchString)
    if chemCompCoordXmlFile:
      chemCompCoord = XmlIO.loadFromFile(project, chemCompCoordXmlFile,
                                         partialLoad=partialLoad)

    if chemCompCoord is None and download:
        
      ccLocator = (project.findFirstPackageLocator(targetName=packageName) or
                   project.findFirstPackageLocator(targetName='any'))
      repository = ccLocator.findFirstRepository()

      fileFound = downloadChemCompInfoFromCcpForge(repository, molType, ccpCode,
                                                   sourceName=sourceName)
               
      if fileFound:
        chemCompCoord = XmlIO.loadFromFile(project, fileFound,  partialLoad=partialLoad)

  return chemCompCoord

def getCcpForgeUrls(molType,ccpCode,sourceName=None):
  
  """
  Creates the URL info for ChemComp(Coord) downloads from CcpForge
  """

  ccpForgeUrl = "http://ccpforge.cse.rl.ac.uk/gf/project/ccpn-chemcomp/scmcvs/?action=browse&root=ccpn-chemcomp&pathrev=MAIN&path=/"
  checkOutDir = "~checkout~"    
  archiveDir = "ccpn-chemcomp/data/pdbe/chemComp/archive/"
  
  #%2Acheckout%2A%2Fccpn-chemcomp%2Fdata%2Fpdbe%2FchemComp%2Farchive%2FChemComp%2Fprotein%2Fprotein%252B004%252Bpdbe_ccpnRef_2010-09-23-14-41-20-237_00001.xml&revision=1.1
  
  if not sourceName:
    fileType = 'ChemComp'
    subPath = getChemCompArchiveXmlFilePath("",molType,ccpCode)
  
  else:
    fileType = 'ChemCompCoord'
    subPath = getChemCompCoordArchiveXmlFilePath("",sourceName,molType,ccpCode)
  
  # wb104: 15 Dec 2010: need to use joinPath because otherwise does not
  # work on Windows, but cannot stick ccpForgeUrl in joinPath() because
  # that would convert http:// to http:/
  ccpForgeDirUrl = ccpForgeUrl+corePath.joinPath(archiveDir,fileType,subPath)
  ccpForgeDownloadUrl = ccpForgeUrl+corePath.joinPath(checkOutDir,archiveDir,fileType,subPath)
  
  return fileType, ccpForgeDirUrl, ccpForgeDownloadUrl

def findCcpForgeDownloadLink(dirData, fileType, ccpCode, ccpForgeDownloadUrl):
  
  """
  Finds the relevant XML file name and download link for the ChemComp(Coord) from the repository
  directory data off CcpForge.
  Works by ccpCode only, assuming that info comes from right directory!
  """

  fileHtmlPatt = re.compile("a name=\"([^\"]+)\"\s+href=\"([^\"]+)\"\s+title=\"")
  
  urlLocation = chemCompXmlFile = None

  for urlDirLine in dirData.split("\n"):
    
    fileHtmlSearch = fileHtmlPatt.search(urlDirLine)
    
    if fileHtmlSearch:
      chemCompXmlFile = fileHtmlSearch.group(1)
      
      if fileType == 'ChemComp':
        (tmpMolType,tmpCcpCode,suffix) = chemCompXmlFile.split("+")
      else:
        (tmpSourceName,tmpMolType,tmpCcpCode,suffix) = chemCompXmlFile.split("+")
                
      if ccpCode == tmpCcpCode:
        
        urlLocation = "%s/%s&content-type=text/plain" % (ccpForgeDownloadUrl,
                                                         chemCompXmlFile.replace('+','%252B'))
        break        
  
  return urlLocation, chemCompXmlFile

def downloadChemCompInfoFromCcpForge(repository, molType, ccpCode, sourceName=None):
  
  """
  Fetch chemComp 'molType', 'ccpCode' or, if sourceName given, the corresponding chemCompCoord, 
  to local repository 'repository'
  from chemCompServer
  contexts
  Returns name of copied file, or None if unsuccessful
  """

  logger = repository.root._logger
    
  result = None
  
  (fileType, ccpForgeDirUrl, ccpForgeDownloadUrl) = getCcpForgeUrls(molType,ccpCode,
                                                                    sourceName=sourceName)

  if sourceName:
    # For displaying error info
    sourceText = "%s, " % sourceName
  else:
    sourceText = ""
    
  try:

    try:
      # Get the file list, needs to be decomposed to get direct links
      dirData = Url.fetchUrl(ccpForgeDirUrl)

      urlLocation, chemCompXmlFile = findCcpForgeDownloadLink(dirData,fileType,ccpCode,
                                                                ccpForgeDownloadUrl)

      if urlLocation:

        try:
          data = Url.fetchUrl(urlLocation)

          try:
            saveChemCompPath = repository.getFileLocation('ccp.molecule.%s' % fileType)
            if not os.path.exists(saveChemCompPath):
              os.makedirs(saveChemCompPath)
  
            chemCompFile = corePath.joinPath(saveChemCompPath,chemCompXmlFile)
            fout = open(chemCompFile,'w')
            fout.write(data)
            fout.close()
  
            print ("Downloaded %s %s%s, %s from server %s, written to file %s!"
                   % (fileType,sourceText,molType,ccpCode,ccpForgeDownloadUrl,chemCompFile))
            result = chemCompFile
  
          except IOError as e:
            logger.error("Cannot write %s XML file %s%s, %s: %s"  %
                         (fileType,sourceText,molType,ccpCode,str(e)))
  
        except IOError as e:
          logger.error("Cannot read %s %s%s, %s: %s"
                       % (fileType,sourceText,molType,ccpCode,str(e)))
      
        
      else:
        logger.error("Cannot find %s XML file %s%s, %s."
                     % (fileType,sourceText,molType,ccpCode))
      
    except IOError as e:
      logger.error("Cannot read directory information for %s%s, %s: %s"
                   % (sourceText,molType,ccpCode,str(e)))

  except IOError as e:
    logger.error("Cannot connect to download server %s, or file does not exist...: %s "
                 % (ccpForgeDownloadUrl,str(e)))
    raise
  #
  return result

def fetchStdChemComps(project,molTypes=None):

  chemComps = []

  if not molTypes:
  
    molTypes = ['protein','RNA','DNA']

  for molType in molTypes:
  
    if standardResidueCcpCodes.has_key(molType):
  
      for ccpCode in standardResidueCcpCodes[molType]:
        chemComp = fetchChemComp(project, molType, ccpCode, download=False)
        if chemComp:
          chemComps.append(chemComp)

  return chemComps

