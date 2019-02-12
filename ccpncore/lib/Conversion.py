"""
======================COPYRIGHT/LICENSE START==========================

Conversion.py: Data compatibility handling

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:09 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b5 $"
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
import importlib
import itertools
from ccpnmodel.ccpncore.memops import Version
from ccpnmodel.ccpncore.memops.ApiError import ApiError




def getConversionInfo(fromVersionString, toVersionString):
  """ get dictionary with elemsTreatedAsOld, extraMapChanges function
  and correctData function to go from fromVersion to toVersion
  """
  result = {}

  if isinstance(fromVersionString, Version.Version):
    fromVersion = fromVersionString
  else:
    fromVersion = Version.Version(fromVersionString)

  # HACK - 2,0,6 is  aside branch, and a lot of extra work to upgrade correctly.
  # Treating it as identical to 2.0.5 should (hopefully) work most of the time.
  # Alternatively one could try treating it as 2.1.0 instead
  if str(fromVersion) == '2.0.6':
    fromVersion = Version.Version('2.0.5')

  if toVersionString:
    if isinstance(toVersionString, Version.Version):
      toVersion = toVersionString
    else:
      toVersion = Version.Version(toVersionString)
  else:
    toVersion = Version.currentModelVersion

  if toVersion > fromVersion:

    # get modules to load code from
    imp = importlib.import_module
    toModule = imp('ccpnmodel.%s.upgrade' % toVersion.getDirName())
    versions = [Version.Version(x) for x in  toModule.versionSequence]
    i1 = versions.index(fromVersion)
    i2 = versions.index(toVersion)
    activeVersions = versions[i1+1:i2+1]
    versionModules = [imp('ccpnmodel.%s.upgrade' % x.getDirName()) for x in activeVersions]

    # make extraMapChanges function
    def extraMapChanges(globalMapping):
      """ mapping changes for series of version changes:"""
      for ii,mm in reversed(list(enumerate(versionModules))):
        mm.extraMapChanges(globalMapping)
    result['extraMapChanges'] = extraMapChanges

    # get correctData function
    def correctData(topObj, delayDataDict, toNewObjDict, mapping=None):
      """ get correctData function for version list"""
      for mm in versionModules:
        mm.correctData(topObj, delayDataDict, toNewObjDict, mapping=mapping)
    result['correctData'] = correctData

    # get elementPairings
    # result['elementPairings'] = toModule.elementPairings
    result['elementPairings'] = list(itertools.chain(*(mm.elementPairings
                                                       for mm in versionModules)))

    # get elemsTreatedAsOld
    result['elemsTreatedAsOld'] = set().union(*(mm.elemsTreatedAsOld for mm in versionModules))


  elif toVersion < fromVersion:
    raise NotImplementedError("Data downgrading from %s to %s not implemented yet"
                              % (fromVersion, toVersion))

  #
  return result


def setNmrExpPrototypeLink(obj, tag, topObjByGuid, delayDataDict,
                           linkmapper):
  """ redirect certain NmrExpPrototype links to other experiments
  """

  if tag == 'refExpDim':
    # After model changes this is no longer set
    return

  doGet = delayDataDict.get
  objDataDict = doGet(obj)
  inDataList = objDataDict.get(tag)
  if inDataList:
    keyList = inDataList[0]

    linkmapper(keyList)
    guid = keyList[0]

    # set link
    oo = topObjByGuid.get(guid)
    clazz = keyList[-1]['class']
    if oo is None:
      # NB naughty - _packageName is a private attribute.
      # But getPackageName is not static
      obj.root.refreshTopObjects(clazz._packageName)
      oo = topObjByGuid.get(guid)
    if oo is not None:
      # If the experiment is not found, hopefully it wil be picked up at a later
      # compatibility step.
      # Aftere V3 these links are derived, settable, and must be set properly
      # obj.__dict__[tag] = clazz.getByKey(oo, keyList[1:-1])
      setattr(obj,tag, clazz.getByKey(oo, keyList[1:-1]))
      del objDataDict[tag]
