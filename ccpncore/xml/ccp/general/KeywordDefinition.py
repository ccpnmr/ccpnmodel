"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Fri May 18 15:00:52 2018
  from data model element ccp.general.KeywordDefinition

#######################################################################
======================COPYRIGHT/LICENSE START==========================

KeywordDefinition.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccp.general.KeywordDefinition

Copyright (C) 2007  (CCPN Project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

A copy of this license can be found in ../../../../../../..//LGPL.license

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
import ccpnmodel.ccpncore.api.ccp.general.KeywordDefinition

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package KWDF, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('KWDF').get('abstractTypes')
  exolinks = globalMap.get('KWDF').get('exolinks')

  # Class KeywordDefinition
  currentMap = {}
  abstractTypes['KeywordDefinition'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-14-17:02:54_00002'] = currentMap
  loadMaps['KWDF.KeywordDefinition'] = currentMap
  currentMap['tag'] = 'KWDF.KeywordDefinition'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:02:54_00002'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'keywordDefinitions'
  currentMap['objkey'] = 'keyword'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.KeywordDefinition.KeywordDefinition
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute KeywordDefinition._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute KeywordDefinition.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute KeywordDefinition.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute KeywordDefinition.explanation
  currentMap = {}
  contentMap['explanation'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00003'] = currentMap
  loadMaps['KWDF.KeywordDefinition.explanation'] = currentMap
  currentMap['tag'] = 'KWDF.KeywordDefinition.explanation'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00003'
  currentMap['name'] = 'explanation'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')

  # Attribute KeywordDefinition.keyword
  currentMap = {}
  contentMap['keyword'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00001'] = currentMap
  loadMaps['KWDF.KeywordDefinition.keyword'] = currentMap
  currentMap['tag'] = 'KWDF.KeywordDefinition.keyword'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00001'
  currentMap['name'] = 'keyword'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute KeywordDefinition.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00002'] = currentMap
  loadMaps['KWDF.KeywordDefinition.name'] = currentMap
  currentMap['tag'] = 'KWDF.KeywordDefinition.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00002'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute KeywordDefinition.targetNames
  currentMap = {}
  contentMap['targetNames'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00004'] = currentMap
  loadMaps['KWDF.KeywordDefinition.targetNames'] = currentMap
  currentMap['tag'] = 'KWDF.KeywordDefinition.targetNames'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00004'
  currentMap['name'] = 'targetNames'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')
  # End of KeywordDefinition

  currentMap = abstractTypes.get('KeywordDefinition')
  aList = ['_ID', 'keyword']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'explanation', 'name', 'targetNames']
  currentMap['simpleAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class KeywordDefinitionStore
  currentMap = {}
  abstractTypes['KeywordDefinitionStore'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-14-17:02:54_00003'] = currentMap
  loadMaps['KWDF.KeywordDefinitionStore'] = currentMap
  currentMap['tag'] = 'KWDF.KeywordDefinitionStore'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:02:54_00003'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'keywordDefinitionStores'
  currentMap['isTop'] = True
  currentMap['objkey'] = 'context'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.KeywordDefinition.KeywordDefinitionStore
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute KeywordDefinitionStore._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute KeywordDefinitionStore._lastId
  contentMap['_lastId'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-05-13:04:27_00001')

  # Attribute KeywordDefinitionStore.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute KeywordDefinitionStore.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute KeywordDefinitionStore.context
  currentMap = {}
  contentMap['context'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00007'] = currentMap
  loadMaps['KWDF.KeywordDefinitionStore.context'] = currentMap
  currentMap['tag'] = 'KWDF.KeywordDefinitionStore.context'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00007'
  currentMap['name'] = 'context'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute KeywordDefinitionStore.createdBy
  contentMap['createdBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00002__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute KeywordDefinitionStore.guid
  contentMap['guid'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:26_00002')

  # Attribute KeywordDefinitionStore.isModifiable
  contentMap['isModifiable'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-17-14:16:26_00010__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute KeywordDefinitionStore.lastUnlockedBy
  contentMap['lastUnlockedBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00003__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Role KeywordDefinitionStore.keywordDefinitions
  currentMap = {}
  contentMap['keywordDefinitions'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00006'] = currentMap
  loadMaps['KWDF.KeywordDefinitionStore.keywordDefinitions'] = currentMap
  currentMap['tag'] = 'KWDF.KeywordDefinitionStore.keywordDefinitions'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:03:00_00006'
  currentMap['name'] = 'keywordDefinitions'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('KWDF').get('abstractTypes')
  # End of KeywordDefinitionStore

  currentMap = abstractTypes.get('KeywordDefinitionStore')
  aList = ['_ID', '_lastId', 'context', 'createdBy', 'guid', 'isModifiable', 'lastUnlockedBy']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData']
  currentMap['simpleAttrs'] = aList
  aList = ['keywordDefinitions', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['keywordDefinitions']
  currentMap['children'] = aList

  # Out-of-package link to KeywordDefinition
  currentMap = {}
  exolinks['KeywordDefinition'] = currentMap
  loadMaps['KWDF.exo-KeywordDefinition'] = currentMap
  currentMap['tag'] = 'KWDF.exo-KeywordDefinition'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:02:54_00002'
  currentMap['name'] = 'KeywordDefinition'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.KeywordDefinition.KeywordDefinition
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037'))

  # Out-of-package link to KeywordDefinitionStore
  currentMap = {}
  exolinks['KeywordDefinitionStore'] = currentMap
  loadMaps['KWDF.exo-KeywordDefinitionStore'] = currentMap
  currentMap['tag'] = 'KWDF.exo-KeywordDefinitionStore'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-14-17:02:54_00003'
  currentMap['name'] = 'KeywordDefinitionStore'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.KeywordDefinition.KeywordDefinitionStore
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
