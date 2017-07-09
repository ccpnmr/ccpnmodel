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
__dateModified__ = "$dateModified: 2017-07-07 16:33:31 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
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
from ccpnmodel.ccpncore.lib import Conversion


versionSequence = ['2.0.a0', '2.0.a1', '2.0.a2', '2.0.a3', '2.0.b1', '2.0.b2', '2.0.b3',
                   '2.0.4',  '2.0.5']
# NBNB version 2.0.6 is a side branch, not on the main version sequence

emptyDict = {}
emptyList = []

transferTypeMap = {'NOESY':'through-space',
                   'DipDip':'through-space',
                   'SpinDiff':'through-space',
                   'CP':'onebond',
                   'TOCSY':'relayed',
                   'Jnonlocal':'through-space',
                  }

# guids of elements that should be treated as old
# Must be kept out of map fixing till the last, as they break it.
elemsTreatedAsOld = set(())

# pairs of element guids that should be treated as matching, e.g. when
# a single element must match with several elements in subclasses
elementPairings = []

def extraMapChanges(globalMapping):
  """ Extra map changes specific for a given step
  """

  for guid in (
               # set transferType attributes to delay, to allow resetting
               "www.ccpn.ac.uk_Fogh_2006-08-16-18:22:58_00022",
               "www.ccpn.ac.uk_Fogh_2006-08-16-18:20:07_00001",
               # set links to ExpPrototype package to delay, to allow resetting
               "www.ccpn.ac.uk_Fogh_2006-08-16-18:20:06_00008",
               "www.ccpn.ac.uk_Fogh_2006-08-16-18:23:00_00002",
               "www.ccpn.ac.uk_Fogh_2006-08-16-18:20:05_00025",
               ):
    globalMapping['mapsByGuid'][guid]['proc'] = 'delay'

  for guid in ('www.ccpn.ac.uk_Fogh_2006-08-17-15:11:12_00001', #Macro.path
               'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:11_00011', # FixedResonance.name
               ):
    dd = globalMapping['mapsByGuid'].get(guid)
    if dd and 'proc' in dd:
      del dd['proc']  # should not be 'proc':'delay' after all.



def correctData(topObj, delayDataDict, toNewObjDict, mapping=None):
  """ update topObj object tree using information in delayDataDict
  May be used either to postprocess a file load (minor upgrade)
  or as part of an in-memory data transfer (major upgrade)

  topObj is the package TopObject in the new tree
  toNewObjDict is _ID:newObj for minor
    and oldObj/oldObjId:newObj for major upgrades
  """

  pName = topObj.packageName
  #
  if pName == 'ccp.nmr.Nmr':

    # Fix Nmr
    fixNmr(topObj, delayDataDict)

  elif pName == 'ccp.nmr.NmrExpPrototype':
    # Fix Nmr
    fixNmrExpPrototype(topObj, delayDataDict)


def fixNmr(topObj, delayDataDict):
  """
  """

  # modify transfer type
  doGet = delayDataDict.get

  memopsRoot = topObj.parent
  topObjByGuid = memopsRoot.__dict__.get('topObjects')

  for xpr in doGet(topObj, emptyDict).get('experiments', emptyList):
    expDict = doGet(xpr, emptyDict)
    for expTransfer in expDict.get('expTransfers', emptyList):
      transferType = doGet(expTransfer).get('transferType')
      if transferType:
        transferType = transferType[0]
      if transferType in transferTypeMap:
        transferType = transferTypeMap[transferType]
      setattr(expTransfer, 'transferType', transferType)

  # remap defunct RefExperiment
  for xpr in doGet(topObj, emptyDict).get('experiments', emptyList):

    expDict = doGet(xpr, emptyDict)

    # fix NmrExpPrototype mapping for defunct types
    Conversion.setNmrExpPrototypeLink(xpr, 'refExperiment', topObjByGuid, delayDataDict,
                                      remapPrototypeLink)
    for xd in expDict.get('expDims', emptyList):

      Conversion.setNmrExpPrototypeLink(xd, 'refExpDim', topObjByGuid, delayDataDict,
                                        remapPrototypeLink)
      for xdr in doGet(xd, emptyDict).get('expDimRefs', emptyList):

        Conversion.setNmrExpPrototypeLink(xdr, 'refExpDimRef', topObjByGuid, delayDataDict,
                                          remapPrototypeLink)


def remapPrototypeLink(keyList):

  guid = keyList[0]

  # map to different keys
  if guid in ('cam_wb104_2008-01-15-16-06-39_00003',
              "ccpn_rhf22_2009-04-16-18-01-38-822_00001"):
    # COSY variant - remap to [1]
    keyList[0] = "cam_wb104_2008-01-15-16-06-39_00001"

  elif guid == "ccpn_rhf22_2009-04-03-14-39-03-775_00001":
    # Remap COCA to CACO
    keyList[0] = "ccpn_rhf22_2009-04-03-14-37-40-370_00001"
    keyList[1] = 2

  elif guid == "cam_wb104_2008-01-15-16-06-40_00059":
    # C_C NOESY duplicate
    keyList[0] = "ccpn_rhf22_2009-04-02-16-22-29-921_00001"

  elif guid == "ccpn_rhf22_2009-04-17-17-47-01-401_00001":
    # Dept=135
    keyList[0] = "ccpn_rhf22_2009-04-09-17-35-30-819_00001"

  elif guid in ("cam_wb104_2008-01-15-16-06-40_00055",
                "cam_wb104_2008-01-15-16-06-40_00056",
                "cam_wb104_2008-01-15-16-06-40_00057"):
    # Superfluous relaxation variant
    if keyList[1] == 2:
      keyList[1] = 1

  elif guid == "ccpn_rhf22_2009-05-27-15-54-34-222_00001":
    # Superfluous duplicate
    keyList[0] = "ccpn_rhf22_2009-04-15-17-09-17-471_00001"
    refExpMap = {1:1, 40:38, 41:39, 42:2, 43:5, 44:6}
    keyList[1] = refExpMap[keyList[1]]

  elif guid == "ccpn_rhf22_2009-04-14-15-10-00-409_00001":
    # Change 2D filtered NOESY from exp 208 to exp 9
    if keyList[1] == 2:
      keyList[0] = "cam_wb104_2008-01-15-16-06-39_00009"
      keyList[1] = 1
    elif keyList[1] == 4:
      keyList[0] = "cam_wb104_2008-01-15-16-06-39_00009"
      keyList[1] = 3

  elif guid == "ccpn_rhf22_2009-04-14-15-18-59-112_00001":
    # Change 2D filtered NOESY from exp 210 to exp 74
    if keyList[1] == 3:
      keyList[0] = "cam_wb104_2008-01-15-16-06-40_00040"
      keyList[1] = 1

  elif guid == "Expts_vicky_2010-12-15-15-46-16-259_00001":
    # map exp 279 to exp 175
    keyList[0] =  "ccpn_rhf22_2009-04-09-17-59-59-074_00001"
    if keyList[1] == 3:
      keyList[1] = 4
    elif keyList[1] == 4:
      keyList[1] = 5

  elif guid == "Expts_vicky_2010-12-15-15-44-46-557_00001":
    # map exp 278 to exp 174
    keyList[0] =  "ccpn_rhf22_2009-04-09-17-57-16-877_00001"
    if keyList[1] == 3:
      keyList[1] = 4
    elif keyList[1] == 4:
      keyList[1] = 5

  elif guid == "Expts_vicky_2010-12-15-15-18-35-679_00001":
    # map exp 275 to exp 148
    keyList[0] =  "ccpn_rhf22_2009-04-03-14-27-15-011_00001"
    if keyList[1] == 3:
      keyList[1] = 4
    elif keyList[1] == 4:
      keyList[1] = 5

  elif guid == "Expts_vicky_2010-12-15-15-13-54-881_00001":
    # map exp 274 to exp 102
    keyList[0] =  "cam_wb104_2008-01-15-16-06-40_00063"


def fixNmrExpPrototype(topObj, delayDataDict):
  """ remap defunct RefExperiment
  """
  doGet = delayDataDict.get

  for xgr in doGet(topObj, emptyDict).get('expGraphs', emptyList):
    xgrDict = doGet(xgr, emptyDict)
    for expTransfer in xgrDict.get('expTransfers', emptyList):
      transferType = doGet(expTransfer).get('transferType')
      if transferType:
        transferType = transferType[0]
      if transferType in transferTypeMap:
        transferType = transferTypeMap[transferType]
      setattr(expTransfer, 'transferType',transferType)
