"""
======================COPYRIGHT/LICENSE START==========================

upgrade.py: Data compatibility handling

Copyright (C) 2007-2014 Rasmus Fogh (CCPN project)

=======================================================================
# Licence, Reference and Credits

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

A copy of this license can be found in ../../../../license/LGPL.license.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

======================COPYRIGHT/LICENSE END============================

To obtain more information about this code:

- CCPN website (http://www.ccpn.ac.uk)

- contact Rasmus Fogh (ccpn@bioc.cam.ac.uk)

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:32 +0100 (Fri, July 07, 2017) $"
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
quoting the following reference:

===========================REFERENCE START=============================
Rasmus H. Fogh, Wayne Boucher, Wim F. Vranken, Anne
Pajon, Tim J. Stevens, T.N. Bhat, John Westbrook, John M.C. Ionides and
Ernest D. Laue (2005). A framework for scientific data modeling and
automated software development. Bioinformatics 21, 1678-1684.
===========================REFERENCE END===============================

"""

versionSequence = ['2.0.a0', '2.0.a1', '2.0.a2', '2.0.a3']
# NBNB version 2.0.6 is a side branch, not on the main version sequence

emptyDict = {}
emptyList = []

# guids of elements that should be treated as old
# Must be kept out of map fixing till the last, as they break it.
elemsTreatedAsOld = set((
'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:49_00001',
'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:52_00008',
'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:52_00010',
'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:52_00006',
'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:52_00004',
'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:11_00004'
))

# pairs of element guids that should be treated as matching, e.g. when
# a single element must match with several elements in subclasses
elementPairings = []

def extraMapChanges(globalMapping):
  """ Extra map changes specific for a given step
  """

  # rename of StructureValidation package to Validation
  dd = globalMapping.get('VALD')
  if dd is not None:
    dd['exolinks']['.qName'] = 'ccp.molecule.StructureValidation'
    dd['abstractTypes']['.qName'] = 'ccp.molecule.StructureValidation'


def correctData(topObj, delayDataDict, toNewObjDict, mapping=None):
  """ update topObj object tree using information in delayDataDict
  May be used either to postprocess a file load (minor upgrade)
  or as part of an in-memory data transfer (major upgrade)

  topObj is the package TopObject in the new tree
  toNewObjDict is _ID:newObj for minor
    and oldObj/oldObjId:newObj for major upgrades
  """

  doGet = delayDataDict.get
  pName = topObj.packageName


  if pName == 'ccp.molecule.Validation':
    # Fix Validation
    fixValidation(topObj, delayDataDict)

  elif pName == 'memops.Implementation':

    # reset names in packageLocators
    for pl in doGet(topObj, emptyDict).get('packageLocators', emptyList):
      if pl.targetName == 'ccp.molecule.StructureValidation':
        pl.__dict__['targetName'] = 'ccp.molecule.Validation'

    topObjByGuid = topObj.__dict__.get('topObjects')
    validationStores = [x for x in topObjByGuid.values()
                        if x.packageShortName == 'VALD']
    for validationStore in validationStores:
      fullLoadValidationStore(validationStore)


fixingValidation = False

def fixValidation(topObj, delayDataDict):
  """ Trigger validation load from correct location
  Fix ValidationStore-Software link
  NB this triggers full load before partial load has finished
  """

  global fixingValidation

  if fixingValidation:
    # end of second pass. Do no more
    fixingValidation = False

  else:
    # end fo first pass.
    fixingValidation = True

    # fix software link
    root = topObj.root
    methodStore = root.currentMethodStore
    if methodStore is None:
      methodStore = root.newMethodStore(name='auto')
    software = methodStore.findFirstSoftware(name='unknown')
    if software is None:
      software = methodStore.newSoftware(name='unknown', version='unknown')
    #
    topObj.software = software

    # reload
    fullLoadValidationStore(topObj)

def fullLoadValidationStore(topObj):
  """hard load ValidationStore from old location
  """

  from ccpnmodel.ccpncore.lib import ApiPath
  from ccpn.util import Path
  from ccpnmodel.ccpncore.memops.format.xml import XmlIO
  root = topObj.memopsRoot
  locator = (root.findFirstPackageLocator(targetName='ccp.molecule.Validation')
             or root.findFirstPackageLocator(targetName='any'))
  repository = locator.findFirstRepository()
  #repository = topObj.activeRepositories[0]
  fileLocation = repository.getFileLocation('ccp.molecule.StructureValidation')
  filePath = Path.joinPath(fileLocation, ApiPath.getTopObjectFile(topObj))
  XmlIO.loadFromStream(open(filePath), topObject=topObj,
                       topObjId=topObj.guid, partialLoad=False)

