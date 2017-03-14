"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Tue Mar  7 21:21:10 2017
  from data model element ccp.general.Annotation

#######################################################################
======================COPYRIGHT/LICENSE START==========================

Annotation.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccp.general.Annotation

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
import ccpnmodel.ccpncore.api.ccp.general.Annotation

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package ANNO, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('ANNO').get('abstractTypes')
  exolinks = globalMap.get('ANNO').get('exolinks')

  # Class Annotation
  currentMap = {}
  abstractTypes['Annotation'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00026'] = currentMap
  loadMaps['ANNO.Annotation'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00026'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'annotations'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Annotation.Annotation
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute Annotation._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute Annotation.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute Annotation.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute Annotation.date
  currentMap = {}
  contentMap['date'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00112'] = currentMap
  loadMaps['ANNO.Annotation.date'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation.date'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00112'
  currentMap['name'] = 'date'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00029')

  # Attribute Annotation.description
  currentMap = {}
  contentMap['description'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00110'] = currentMap
  loadMaps['ANNO.Annotation.description'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation.description'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00110'
  currentMap['name'] = 'description'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')

  # Attribute Annotation.details
  currentMap = {}
  contentMap['details'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00113'] = currentMap
  loadMaps['ANNO.Annotation.details'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation.details'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00113'
  currentMap['name'] = 'details'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')

  # Attribute Annotation.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00109'] = currentMap
  loadMaps['ANNO.Annotation.name'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00109'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute Annotation.path
  currentMap = {}
  contentMap['path'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00111'] = currentMap
  loadMaps['ANNO.Annotation.path'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation.path'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00111'
  currentMap['name'] = 'path'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00003')

  # Attribute Annotation.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00108'] = currentMap
  loadMaps['ANNO.Annotation.serial'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00108'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Role Annotation.author
  currentMap = {}
  contentMap['author'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:14_00003'] = currentMap
  loadMaps['ANNO.Annotation.author'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation.author'
  currentMap['type'] = 'exolink'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:14_00003'
  currentMap['name'] = 'author'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['copyOverride'] = True
  currentMap['content'] = globalMap.get('AFFI').get('exolinks')

  # Role Annotation.dataUrl
  currentMap = {}
  contentMap['dataUrl'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-09-10:09:29_00003'] = currentMap
  loadMaps['ANNO.Annotation.dataUrl'] = currentMap
  currentMap['tag'] = 'ANNO.Annotation.dataUrl'
  currentMap['type'] = 'exolink'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-09-10:09:29_00003'
  currentMap['name'] = 'dataUrl'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['copyOverride'] = True
  currentMap['content'] = globalMap.get('DLOC').get('exolinks')
  # End of Annotation

  currentMap = abstractTypes.get('Annotation')
  aList = ['_ID', 'date', 'serial']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'description', 'details', 'name', 'path']
  currentMap['simpleAttrs'] = aList
  aList = ['dataUrl', 'author', 'applicationData']
  currentMap['cplxAttrs'] = aList

  # Class AnnotationStore
  currentMap = {}
  abstractTypes['AnnotationStore'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-09-05-12:55:15_00001'] = currentMap
  loadMaps['ANNO.AnnotationStore'] = currentMap
  currentMap['tag'] = 'ANNO.AnnotationStore'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-09-05-12:55:15_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'annotationStores'
  currentMap['isTop'] = True
  currentMap['objkey'] = 'name'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Annotation.AnnotationStore
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute AnnotationStore._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute AnnotationStore._lastId
  contentMap['_lastId'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-05-13:04:27_00001')

  # Attribute AnnotationStore.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute AnnotationStore.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute AnnotationStore.createdBy
  contentMap['createdBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00002__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute AnnotationStore.guid
  contentMap['guid'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:26_00002')

  # Attribute AnnotationStore.isModifiable
  contentMap['isModifiable'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-17-14:16:26_00010__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute AnnotationStore.lastUnlockedBy
  contentMap['lastUnlockedBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00003__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute AnnotationStore.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-09-05-12:55:44_00004'] = currentMap
  loadMaps['ANNO.AnnotationStore.name'] = currentMap
  currentMap['tag'] = 'ANNO.AnnotationStore.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-09-05-12:55:44_00004'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Role AnnotationStore.annotations
  currentMap = {}
  contentMap['annotations'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-09-05-12:55:44_00003'] = currentMap
  loadMaps['ANNO.AnnotationStore.annotations'] = currentMap
  currentMap['tag'] = 'ANNO.AnnotationStore.annotations'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-09-05-12:55:44_00003'
  currentMap['name'] = 'annotations'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('ANNO').get('abstractTypes')

  # Role AnnotationStore.molFeatures
  currentMap = {}
  contentMap['molFeatures'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-09-05-12:55:44_00001'] = currentMap
  loadMaps['ANNO.AnnotationStore.molFeatures'] = currentMap
  currentMap['tag'] = 'ANNO.AnnotationStore.molFeatures'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-09-05-12:55:44_00001'
  currentMap['name'] = 'molFeatures'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('ANNO').get('abstractTypes')
  # End of AnnotationStore

  currentMap = abstractTypes.get('AnnotationStore')
  aList = ['_ID', '_lastId', 'createdBy', 'guid', 'isModifiable', 'lastUnlockedBy']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'name']
  currentMap['simpleAttrs'] = aList
  aList = ['molFeatures', 'annotations', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['annotations', 'molFeatures']
  currentMap['children'] = aList

  # Class MolFeature
  currentMap = {}
  abstractTypes['MolFeature'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00025'] = currentMap
  loadMaps['ANNO.MolFeature'] = currentMap
  currentMap['tag'] = 'ANNO.MolFeature'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00025'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'molFeatures'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Annotation.MolFeature
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute MolFeature._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute MolFeature.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute MolFeature.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute MolFeature.details
  currentMap = {}
  contentMap['details'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00099'] = currentMap
  loadMaps['ANNO.MolFeature.details'] = currentMap
  currentMap['tag'] = 'ANNO.MolFeature.details'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00099'
  currentMap['name'] = 'details'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')

  # Attribute MolFeature.featureType
  currentMap = {}
  contentMap['featureType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00098'] = currentMap
  loadMaps['ANNO.MolFeature.featureType'] = currentMap
  currentMap['tag'] = 'ANNO.MolFeature.featureType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00098'
  currentMap['name'] = 'featureType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute MolFeature.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00096'] = currentMap
  loadMaps['ANNO.MolFeature.serial'] = currentMap
  currentMap['tag'] = 'ANNO.MolFeature.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00096'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Role MolFeature.molResidue
  currentMap = {}
  contentMap['molResidue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:35_00005'] = currentMap
  loadMaps['ANNO.MolFeature.molResidue'] = currentMap
  currentMap['tag'] = 'ANNO.MolFeature.molResidue'
  currentMap['type'] = 'exolink'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:35_00005'
  currentMap['name'] = 'molResidue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['copyOverride'] = True
  currentMap['content'] = globalMap.get('MOLE').get('exolinks')
  # End of MolFeature

  currentMap = abstractTypes.get('MolFeature')
  aList = ['_ID', 'featureType', 'serial']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'details']
  currentMap['simpleAttrs'] = aList
  aList = ['molResidue', 'applicationData']
  currentMap['cplxAttrs'] = aList

  # Out-of-package link to Annotation
  currentMap = {}
  exolinks['Annotation'] = currentMap
  loadMaps['ANNO.exo-Annotation'] = currentMap
  currentMap['tag'] = 'ANNO.exo-Annotation'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00026'
  currentMap['name'] = 'Annotation'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Annotation.Annotation
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to AnnotationStore
  currentMap = {}
  exolinks['AnnotationStore'] = currentMap
  loadMaps['ANNO.exo-AnnotationStore'] = currentMap
  currentMap['tag'] = 'ANNO.exo-AnnotationStore'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-09-05-12:55:15_00001'
  currentMap['name'] = 'AnnotationStore'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Annotation.AnnotationStore
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))

  # Out-of-package link to MolFeature
  currentMap = {}
  exolinks['MolFeature'] = currentMap
  loadMaps['ANNO.exo-MolFeature'] = currentMap
  currentMap['tag'] = 'ANNO.exo-MolFeature'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00025'
  currentMap['name'] = 'MolFeature'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Annotation.MolFeature
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
