"""
======================COPYRIGHT/LICENSE START==========================

upgrade.py: Data compatibility handling

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
__author__ = 'rhf22'

versionSequence = ['2.0.a0', '2.0.a1', '2.0.a2', '2.0.a3', '2.0.b1', '2.0.b2', '2.0.b3',
                   '2.0.4',  '2.0.5',  '2.1.0',  '2.1.1', '2.1.2', '3.0.a1']
# NBNB version 2.0.6 is a side branch, not on the main version sequence

emptyDict = {}
emptyList = []

# guids of elements that should be treated as old
# Must be kept out of map fixing till the last, as they break it.
elemsTreatedAsOld = set(())

# pairs of element guids that should be treated as matching, e.g. when
# a single element must match with several elements in subclasses
elementPairings = []

# packages that have been moved - need special code for moving stored data:
# ~ Dictionary is {newName:oldName}
movedPackageNames = {
  'ccp.molecule.Symmetry':'molsim.Symmetry'
}

def extraMapChanges(globalMapping):
  """ Extra map changes specific for a given step
  """

  # Text type disappears and is replaced by String
  globalMapping['loadMaps']['IMPL.Text'] = globalMapping['loadMaps']['IMPL.String']
  globalMapping['IMPL']['abstractTypes']['Text'] = globalMapping['IMPL']['abstractTypes']['String']
  textTypeGuid = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00036'
  stringTypeGuid = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035'
  globalMapping['mapsByGuid'][textTypeGuid] = globalMapping['mapsByGuid'][stringTypeGuid]

  # Double type disappears and is replaced by Float
  globalMapping['loadMaps']['IMPL.Double'] = globalMapping['loadMaps']['IMPL.Float']
  globalMapping['IMPL']['abstractTypes']['Double'] = globalMapping['IMPL']['abstractTypes']['Float']
  doubleTypeGuid = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00030'
  floatTypeGuid = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031'
  globalMapping['mapsByGuid'][doubleTypeGuid] = globalMapping['mapsByGuid'][floatTypeGuid]

  #ShiftReference.indirectShiftRatio
  guid = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:12_00012'
  dd = globalMapping['mapsByGuid'].get(guid)
  if dd:
    dd['data'] = globalMapping['mapsByGuid']['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031']
    if 'proc' in dd:
      del dd['proc']  # should not be 'proc':'delay' after all.



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

  if pName == 'memops.Implementation':
    topObj._movedPackageNames = movedPackageNames
    topObj._upgradedFromV2 = True