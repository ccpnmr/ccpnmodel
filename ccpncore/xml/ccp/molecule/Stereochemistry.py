"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Wed Jan  4 18:55:23 2017
  from data model element ccp.molecule.Stereochemistry

#######################################################################
======================COPYRIGHT/LICENSE START==========================

Stereochemistry.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccp.molecule.Stereochemistry

Copyright (C) 2007  (CCPN Project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

A copy of this license can be found in ../../../../../../../license/LGPL.license

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

If you are using this software for academic purposes, we suggest
quoting the following references:

===========================REFERENCE START=============================
Rasmus H. Fogh, Wayne Boucher, Wim F. Vranken, Anne
Pajon, Tim J. Stevens, T.N. Bhat, John Westbrook, John M.C. Ionides and
Ernest D. Laue (2005). A framework for scientific data modeling and automated
software development. Bioinformatics 21, 1678-1684.


This file was generated with the Memops software generation framework,
and contains original contributions embedded in the framework

===========================REFERENCE END===============================
"""

from ccpnmodel.ccpncore.memops.metamodel.Constants import baseDataTypeModule as basicDataTypes
NaN = float('NaN')
# 
#  Current package api
import ccpnmodel.ccpncore.api.ccp.molecule.Stereochemistry

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package STER, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('STER').get('abstractTypes')
  exolinks = globalMap.get('STER').get('exolinks')

  # Class RefStereochemistry
  currentMap = {}
  abstractTypes['RefStereochemistry'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00055'] = currentMap
  loadMaps['STER.RefStereochemistry'] = currentMap
  currentMap['tag'] = 'STER.RefStereochemistry'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00055'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'refStereochemistries'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.Stereochemistry.RefStereochemistry
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute RefStereochemistry._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute RefStereochemistry.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute RefStereochemistry.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute RefStereochemistry.details
  currentMap = {}
  contentMap['details'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00023'] = currentMap
  loadMaps['STER.RefStereochemistry.details'] = currentMap
  currentMap['tag'] = 'STER.RefStereochemistry.details'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00023'
  currentMap['name'] = 'details'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')

  # Attribute RefStereochemistry.numAtoms
  currentMap = {}
  contentMap['numAtoms'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00021'] = currentMap
  loadMaps['STER.RefStereochemistry.numAtoms'] = currentMap
  currentMap['tag'] = 'STER.RefStereochemistry.numAtoms'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00021'
  currentMap['name'] = 'numAtoms'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute RefStereochemistry.numCoreAtoms
  currentMap = {}
  contentMap['numCoreAtoms'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2011-03-22-17:23:26_00001'] = currentMap
  loadMaps['STER.RefStereochemistry.numCoreAtoms'] = currentMap
  currentMap['tag'] = 'STER.RefStereochemistry.numCoreAtoms'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2011-03-22-17:23:26_00001'
  currentMap['name'] = 'numCoreAtoms'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute RefStereochemistry.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00019'] = currentMap
  loadMaps['STER.RefStereochemistry.serial'] = currentMap
  currentMap['tag'] = 'STER.RefStereochemistry.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00019'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute RefStereochemistry.stereoClass
  currentMap = {}
  contentMap['stereoClass'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00020'] = currentMap
  loadMaps['STER.RefStereochemistry.stereoClass'] = currentMap
  currentMap['tag'] = 'STER.RefStereochemistry.stereoClass'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00020'
  currentMap['name'] = 'stereoClass'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute RefStereochemistry.values
  currentMap = {}
  contentMap['values'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00022'] = currentMap
  loadMaps['STER.RefStereochemistry.values'] = currentMap
  currentMap['tag'] = 'STER.RefStereochemistry.values'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00022'
  currentMap['name'] = 'values'
  currentMap['hicard'] = -1
  currentMap['locard'] = 2
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')
  # End of RefStereochemistry

  currentMap = abstractTypes.get('RefStereochemistry')
  aList = ['_ID', 'numAtoms', 'numCoreAtoms', 'serial', 'stereoClass']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'details', 'values']
  currentMap['simpleAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class StereochemistryStore
  currentMap = {}
  abstractTypes['StereochemistryStore'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:19:50_00001'] = currentMap
  loadMaps['STER.StereochemistryStore'] = currentMap
  currentMap['tag'] = 'STER.StereochemistryStore'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:19:50_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'stereochemistryStores'
  currentMap['isTop'] = True
  currentMap['objkey'] = 'name'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.Stereochemistry.StereochemistryStore
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute StereochemistryStore._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute StereochemistryStore._lastId
  contentMap['_lastId'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-05-13:04:27_00001')

  # Attribute StereochemistryStore.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute StereochemistryStore.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute StereochemistryStore.createdBy
  contentMap['createdBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00002__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute StereochemistryStore.guid
  contentMap['guid'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:26_00002')

  # Attribute StereochemistryStore.isModifiable
  contentMap['isModifiable'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-17-14:16:26_00010__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute StereochemistryStore.lastUnlockedBy
  contentMap['lastUnlockedBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00003__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute StereochemistryStore.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00026'] = currentMap
  loadMaps['STER.StereochemistryStore.name'] = currentMap
  currentMap['tag'] = 'STER.StereochemistryStore.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00026'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Role StereochemistryStore.refStereochemistries
  currentMap = {}
  contentMap['refStereochemistries'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00025'] = currentMap
  loadMaps['STER.StereochemistryStore.refStereochemistries'] = currentMap
  currentMap['tag'] = 'STER.StereochemistryStore.refStereochemistries'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:28_00025'
  currentMap['name'] = 'refStereochemistries'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('STER').get('abstractTypes')
  # End of StereochemistryStore

  currentMap = abstractTypes.get('StereochemistryStore')
  aList = ['_ID', '_lastId', 'createdBy', 'guid', 'isModifiable', 'lastUnlockedBy']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'name']
  currentMap['simpleAttrs'] = aList
  aList = ['refStereochemistries', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['refStereochemistries']
  currentMap['children'] = aList

  # Out-of-package link to RefStereochemistry
  currentMap = {}
  exolinks['RefStereochemistry'] = currentMap
  loadMaps['STER.exo-RefStereochemistry'] = currentMap
  currentMap['tag'] = 'STER.exo-RefStereochemistry'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00055'
  currentMap['name'] = 'RefStereochemistry'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.Stereochemistry.RefStereochemistry
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to StereochemistryStore
  currentMap = {}
  exolinks['StereochemistryStore'] = currentMap
  loadMaps['STER.exo-StereochemistryStore'] = currentMap
  currentMap['tag'] = 'STER.exo-StereochemistryStore'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:19:50_00001'
  currentMap['name'] = 'StereochemistryStore'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.Stereochemistry.StereochemistryStore
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
