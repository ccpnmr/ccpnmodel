"""
======================COPYRIGHT/LICENSE START==========================

Conversion.py: Data compatibility handling

Copyright (C) 2007-2014 Rasmus Fogh (CCPN project)

=======================================================================

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
from ccpncore.memops import Version
from ccpncore.memops.ApiError import ApiError

__author__ = 'rhf22'



def getConversionInfo(fromVersionString, toVersionString):
  """ get dictionary with elemsTreatedAsOld, extraMapChanges function
  and correctData function to go from fromVersion to toVersion
  """
  result = {}

  if isinstance(fromVersionString, Version.Version):
    fromVersion = fromVersionString
  else:
    fromVersion = Version.Version(fromVersionString)

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
      for mm in reversed(versionModules):
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
      try:
        oo = topObjByGuid[guid]
      except:
        raise ApiError("""%s.%s: NmrExpPrototype with guid %s not found or loaded"""
                       % (clazz.__name__, tag, guid))
    obj.__dict__[tag] = clazz.getByKey(oo, keyList[1:-1])
    del objDataDict[tag]