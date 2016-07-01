"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Fri Jul  1 02:26:27 2016
  from data model element ccp.molecule.ChemCompLabel

#######################################################################
======================COPYRIGHT/LICENSE START==========================

ChemCompLabel.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccp.molecule.ChemCompLabel

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
import ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package CCLB, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('CCLB').get('abstractTypes')
  exolinks = globalMap.get('CCLB').get('exolinks')

  # Class AtomLabel
  currentMap = {}
  abstractTypes['AtomLabel'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00018'] = currentMap
  loadMaps['CCLB.AtomLabel'] = currentMap
  currentMap['tag'] = 'CCLB.AtomLabel'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00018'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'atomLabels'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel.AtomLabel
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute AtomLabel._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute AtomLabel.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute AtomLabel.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute AtomLabel.isotopeCode
  currentMap = {}
  contentMap['isotopeCode'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00092'] = currentMap
  loadMaps['CCLB.AtomLabel.isotopeCode'] = currentMap
  currentMap['tag'] = 'CCLB.AtomLabel.isotopeCode'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00092'
  currentMap['name'] = 'isotopeCode'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute AtomLabel.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00003'] = currentMap
  loadMaps['CCLB.AtomLabel.name'] = currentMap
  currentMap['tag'] = 'CCLB.AtomLabel.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00003'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute AtomLabel.subType
  currentMap = {}
  contentMap['subType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00004'] = currentMap
  loadMaps['CCLB.AtomLabel.subType'] = currentMap
  currentMap['tag'] = 'CCLB.AtomLabel.subType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00004'
  currentMap['name'] = 'subType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['proc'] = 'direct'
  currentMap['default'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute AtomLabel.weight
  currentMap = {}
  contentMap['weight'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00093'] = currentMap
  loadMaps['CCLB.AtomLabel.weight'] = currentMap
  currentMap['tag'] = 'CCLB.AtomLabel.weight'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00093'
  currentMap['name'] = 'weight'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 1.0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00009')
  # End of AtomLabel

  currentMap = abstractTypes.get('AtomLabel')
  aList = ['_ID', 'ccpnInternalData', 'isotopeCode', 'name', 'subType', 'weight']
  currentMap['headerAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class ChemCompLabel
  currentMap = {}
  abstractTypes['ChemCompLabel'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00014'] = currentMap
  loadMaps['CCLB.ChemCompLabel'] = currentMap
  currentMap['tag'] = 'CCLB.ChemCompLabel'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00014'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'chemCompLabels'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel.ChemCompLabel
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute ChemCompLabel._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute ChemCompLabel.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute ChemCompLabel.ccpCode
  currentMap = {}
  contentMap['ccpCode'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00073'] = currentMap
  loadMaps['CCLB.ChemCompLabel.ccpCode'] = currentMap
  currentMap['tag'] = 'CCLB.ChemCompLabel.ccpCode'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00073'
  currentMap['name'] = 'ccpCode'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2007-09-12-18:31:28_00003')

  # Attribute ChemCompLabel.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute ChemCompLabel.molType
  currentMap = {}
  contentMap['molType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00072'] = currentMap
  loadMaps['CCLB.ChemCompLabel.molType'] = currentMap
  currentMap['tag'] = 'CCLB.ChemCompLabel.molType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00072'
  currentMap['name'] = 'molType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00024')

  # Role ChemCompLabel.isotopomers
  currentMap = {}
  contentMap['isotopomers'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:13_00001'] = currentMap
  loadMaps['CCLB.ChemCompLabel.isotopomers'] = currentMap
  currentMap['tag'] = 'CCLB.ChemCompLabel.isotopomers'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:13_00001'
  currentMap['name'] = 'isotopomers'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('CCLB').get('abstractTypes')
  # End of ChemCompLabel

  currentMap = abstractTypes.get('ChemCompLabel')
  aList = ['_ID', 'ccpCode', 'ccpnInternalData', 'molType']
  currentMap['headerAttrs'] = aList
  aList = ['isotopomers', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['isotopomers']
  currentMap['children'] = aList

  # Class Isotopomer
  currentMap = {}
  abstractTypes['Isotopomer'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:54_00001'] = currentMap
  loadMaps['CCLB.Isotopomer'] = currentMap
  currentMap['tag'] = 'CCLB.Isotopomer'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:54_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'isotopomers'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel.Isotopomer
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute Isotopomer._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute Isotopomer.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute Isotopomer.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute Isotopomer.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00005'] = currentMap
  loadMaps['CCLB.Isotopomer.serial'] = currentMap
  currentMap['tag'] = 'CCLB.Isotopomer.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00005'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute Isotopomer.weight
  currentMap = {}
  contentMap['weight'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00006'] = currentMap
  loadMaps['CCLB.Isotopomer.weight'] = currentMap
  currentMap['tag'] = 'CCLB.Isotopomer.weight'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00006'
  currentMap['name'] = 'weight'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 1.0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00009')

  # Role Isotopomer.atomLabels
  currentMap = {}
  contentMap['atomLabels'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00001'] = currentMap
  loadMaps['CCLB.Isotopomer.atomLabels'] = currentMap
  currentMap['tag'] = 'CCLB.Isotopomer.atomLabels'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00001'
  currentMap['name'] = 'atomLabels'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('CCLB').get('abstractTypes')
  # End of Isotopomer

  currentMap = abstractTypes.get('Isotopomer')
  aList = ['_ID', 'ccpnInternalData', 'serial', 'weight']
  currentMap['headerAttrs'] = aList
  aList = ['atomLabels', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['atomLabels']
  currentMap['children'] = aList

  # Class LabelingScheme
  currentMap = {}
  abstractTypes['LabelingScheme'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-24-12:23:14_00001'] = currentMap
  loadMaps['CCLB.LabelingScheme'] = currentMap
  currentMap['tag'] = 'CCLB.LabelingScheme'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-24-12:23:14_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'labelingSchemes'
  currentMap['isTop'] = True
  currentMap['objkey'] = 'name'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel.LabelingScheme
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute LabelingScheme._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute LabelingScheme._lastId
  contentMap['_lastId'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-05-13:04:27_00001')

  # Attribute LabelingScheme.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute LabelingScheme.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute LabelingScheme.createdBy
  contentMap['createdBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00002__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute LabelingScheme.details
  currentMap = {}
  contentMap['details'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00005'] = currentMap
  loadMaps['CCLB.LabelingScheme.details'] = currentMap
  currentMap['tag'] = 'CCLB.LabelingScheme.details'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00005'
  currentMap['name'] = 'details'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')

  # Attribute LabelingScheme.guid
  contentMap['guid'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:26_00002')

  # Attribute LabelingScheme.isModifiable
  contentMap['isModifiable'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-17-14:16:26_00010__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute LabelingScheme.lastUnlockedBy
  contentMap['lastUnlockedBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00003__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute LabelingScheme.longName
  currentMap = {}
  contentMap['longName'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00004'] = currentMap
  loadMaps['CCLB.LabelingScheme.longName'] = currentMap
  currentMap['tag'] = 'CCLB.LabelingScheme.longName'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00004'
  currentMap['name'] = 'longName'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute LabelingScheme.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00003'] = currentMap
  loadMaps['CCLB.LabelingScheme.name'] = currentMap
  currentMap['tag'] = 'CCLB.LabelingScheme.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00003'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Role LabelingScheme.chemCompLabels
  currentMap = {}
  contentMap['chemCompLabels'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00002'] = currentMap
  loadMaps['CCLB.LabelingScheme.chemCompLabels'] = currentMap
  currentMap['tag'] = 'CCLB.LabelingScheme.chemCompLabels'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00002'
  currentMap['name'] = 'chemCompLabels'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('CCLB').get('abstractTypes')
  # End of LabelingScheme

  currentMap = abstractTypes.get('LabelingScheme')
  aList = ['_ID', '_lastId', 'ccpnInternalData', 'createdBy', 'guid', 'isModifiable', 'lastUnlockedBy', 'name']
  currentMap['headerAttrs'] = aList
  aList = ['details', 'longName']
  currentMap['simpleAttrs'] = aList
  aList = ['chemCompLabels', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['chemCompLabels']
  currentMap['children'] = aList

  # Out-of-package link to AtomLabel
  currentMap = {}
  exolinks['AtomLabel'] = currentMap
  loadMaps['CCLB.exo-AtomLabel'] = currentMap
  currentMap['tag'] = 'CCLB.exo-AtomLabel'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00018'
  currentMap['name'] = 'AtomLabel'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel.AtomLabel
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00024'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2007-09-12-18:31:28_00003'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037'))

  # Out-of-package link to ChemCompLabel
  currentMap = {}
  exolinks['ChemCompLabel'] = currentMap
  loadMaps['CCLB.exo-ChemCompLabel'] = currentMap
  currentMap['tag'] = 'CCLB.exo-ChemCompLabel'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00014'
  currentMap['name'] = 'ChemCompLabel'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel.ChemCompLabel
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00024'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2007-09-12-18:31:28_00003'))

  # Out-of-package link to Isotopomer
  currentMap = {}
  exolinks['Isotopomer'] = currentMap
  loadMaps['CCLB.exo-Isotopomer'] = currentMap
  currentMap['tag'] = 'CCLB.exo-Isotopomer'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:54_00001'
  currentMap['name'] = 'Isotopomer'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel.Isotopomer
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00024'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2007-09-12-18:31:28_00003'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to LabelingScheme
  currentMap = {}
  exolinks['LabelingScheme'] = currentMap
  loadMaps['CCLB.exo-LabelingScheme'] = currentMap
  currentMap['tag'] = 'CCLB.exo-LabelingScheme'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-24-12:23:14_00001'
  currentMap['name'] = 'LabelingScheme'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.ChemCompLabel.LabelingScheme
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
