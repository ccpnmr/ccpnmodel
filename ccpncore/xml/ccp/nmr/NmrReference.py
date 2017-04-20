"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Thu Apr 13 07:15:42 2017
  from data model element ccp.nmr.NmrReference

#######################################################################
======================COPYRIGHT/LICENSE START==========================

NmrReference.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccp.nmr.NmrReference

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
import ccpnmodel.ccpncore.api.ccp.nmr.NmrReference

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package NMRR, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('NMRR').get('abstractTypes')
  exolinks = globalMap.get('NMRR').get('exolinks')

  # Class ChemAtomNmrDistrib
  currentMap = {}
  abstractTypes['ChemAtomNmrDistrib'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'chemAtomNmrDistribs'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemAtomNmrDistrib
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute ChemAtomNmrDistrib._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute ChemAtomNmrDistrib.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute ChemAtomNmrDistrib.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute ChemAtomNmrDistrib.data
  currentMap = {}
  contentMap['data'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2011-03-30-18:03:29_00002__www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib.data'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib.data'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2011-03-30-18:03:29_00002__www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'
  currentMap['name'] = 'data'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2015-10-26-11:28:17_00001')

  # Attribute ChemAtomNmrDistrib.defaultValue
  currentMap = {}
  contentMap['defaultValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2011-03-30-18:03:29_00001__www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib.defaultValue'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib.defaultValue'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2011-03-30-18:03:29_00001__www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'
  currentMap['name'] = 'defaultValue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['proc'] = 'direct'
  currentMap['default'] = NaN
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2015-10-26-11:28:17_00001')

  # Attribute ChemAtomNmrDistrib.refPoints
  currentMap = {}
  contentMap['refPoints'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2010-05-14-15:28:27_00003'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib.refPoints'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib.refPoints'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-05-14-15:28:27_00003'
  currentMap['name'] = 'refPoints'
  currentMap['hicard'] = -1
  currentMap['locard'] = 2
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute ChemAtomNmrDistrib.refValues
  currentMap = {}
  contentMap['refValues'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2010-05-14-15:28:27_00004'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib.refValues'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib.refValues'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-05-14-15:28:27_00004'
  currentMap['name'] = 'refValues'
  currentMap['hicard'] = -1
  currentMap['locard'] = 2
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute ChemAtomNmrDistrib.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2010-05-14-15:28:27_00001'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib.serial'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-05-14-15:28:27_00001'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute ChemAtomNmrDistrib.shape
  currentMap = {}
  contentMap['shape'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2011-03-30-18:02:26_00016__www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib.shape'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib.shape'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2011-03-30-18:02:26_00016__www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'
  currentMap['name'] = 'shape'
  currentMap['hicard'] = -1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00011')

  # Attribute ChemAtomNmrDistrib.valuesPerPoint
  currentMap = {}
  contentMap['valuesPerPoint'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2012-04-13-13:40:44_00003'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib.valuesPerPoint'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib.valuesPerPoint'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2012-04-13-13:40:44_00003'
  currentMap['name'] = 'valuesPerPoint'
  currentMap['hicard'] = -1
  currentMap['locard'] = 2
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Role ChemAtomNmrDistrib.refAtoms
  currentMap = {}
  contentMap['refAtoms'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2010-05-14-17:17:46_00001'] = currentMap
  loadMaps['NMRR.ChemAtomNmrDistrib.refAtoms'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrDistrib.refAtoms'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-05-14-17:17:46_00001'
  currentMap['name'] = 'refAtoms'
  currentMap['hicard'] = -1
  currentMap['locard'] = 2
  currentMap['copyOverride'] = True
  # End of ChemAtomNmrDistrib

  currentMap = abstractTypes.get('ChemAtomNmrDistrib')
  aList = ['_ID', 'defaultValue', 'serial']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'data', 'refPoints', 'refValues', 'shape', 'valuesPerPoint', 'refAtoms']
  currentMap['simpleAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class ChemAtomNmrRef
  currentMap = {}
  abstractTypes['ChemAtomNmrRef'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00002'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00002'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'chemAtomNmrRefs'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemAtomNmrRef
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute ChemAtomNmrRef._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute ChemAtomNmrRef.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute ChemAtomNmrRef.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute ChemAtomNmrRef.distribution
  currentMap = {}
  contentMap['distribution'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00013'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.distribution'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.distribution'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00013'
  currentMap['name'] = 'distribution'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute ChemAtomNmrRef.meanValue
  currentMap = {}
  contentMap['meanValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00010'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.meanValue'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.meanValue'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00010'
  currentMap['name'] = 'meanValue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute ChemAtomNmrRef.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00008'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.name'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00008'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute ChemAtomNmrRef.randomCoilValue
  currentMap = {}
  contentMap['randomCoilValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00012'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.randomCoilValue'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.randomCoilValue'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00012'
  currentMap['name'] = 'randomCoilValue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute ChemAtomNmrRef.refPoint
  currentMap = {}
  contentMap['refPoint'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00015'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.refPoint'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.refPoint'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00015'
  currentMap['name'] = 'refPoint'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 1.0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute ChemAtomNmrRef.refValue
  currentMap = {}
  contentMap['refValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00016'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.refValue'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.refValue'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00016'
  currentMap['name'] = 'refValue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 0.0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute ChemAtomNmrRef.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00007'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.serial'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00007'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute ChemAtomNmrRef.stdDev
  currentMap = {}
  contentMap['stdDev'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00011'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.stdDev'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.stdDev'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00011'
  currentMap['name'] = 'stdDev'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute ChemAtomNmrRef.subType
  currentMap = {}
  contentMap['subType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00009'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.subType'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.subType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00009'
  currentMap['name'] = 'subType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['proc'] = 'direct'
  currentMap['default'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute ChemAtomNmrRef.valuePerPoint
  currentMap = {}
  contentMap['valuePerPoint'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00017'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.valuePerPoint'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.valuePerPoint'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00017'
  currentMap['name'] = 'valuePerPoint'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Role ChemAtomNmrRef.chemAtomShiftCorrs
  currentMap = {}
  contentMap['chemAtomShiftCorrs'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00006'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.chemAtomShiftCorrs'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.chemAtomShiftCorrs'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00006'
  currentMap['name'] = 'chemAtomShiftCorrs'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('NMRR').get('abstractTypes')

  # Role ChemAtomNmrRef.chemCompVarNmrRefs
  currentMap = {}
  contentMap['chemCompVarNmrRefs'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00033'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.chemCompVarNmrRefs'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.chemCompVarNmrRefs'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00033'
  currentMap['name'] = 'chemCompVarNmrRefs'
  currentMap['hicard'] = -1
  currentMap['locard'] = 1
  currentMap['copyOverride'] = True

  # Role ChemAtomNmrRef.shiftDistributions
  currentMap = {}
  contentMap['shiftDistributions'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2010-05-14-17:17:46_00002'] = currentMap
  loadMaps['NMRR.ChemAtomNmrRef.shiftDistributions'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomNmrRef.shiftDistributions'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-05-14-17:17:46_00002'
  currentMap['name'] = 'shiftDistributions'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['copyOverride'] = False
  # End of ChemAtomNmrRef

  currentMap = abstractTypes.get('ChemAtomNmrRef')
  aList = ['_ID', 'meanValue', 'name', 'randomCoilValue', 'refPoint', 'refValue', 'serial', 'stdDev', 'subType', 'valuePerPoint']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'distribution', 'chemCompVarNmrRefs', 'shiftDistributions']
  currentMap['simpleAttrs'] = aList
  aList = ['chemAtomShiftCorrs', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['chemAtomShiftCorrs']
  currentMap['children'] = aList

  # Class ChemAtomShiftCorr
  currentMap = {}
  abstractTypes['ChemAtomShiftCorr'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00005'] = currentMap
  loadMaps['NMRR.ChemAtomShiftCorr'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomShiftCorr'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00005'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'chemAtomShiftCorrs'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemAtomShiftCorr
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute ChemAtomShiftCorr._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute ChemAtomShiftCorr.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute ChemAtomShiftCorr.ccpCode
  currentMap = {}
  contentMap['ccpCode'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00028'] = currentMap
  loadMaps['NMRR.ChemAtomShiftCorr.ccpCode'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomShiftCorr.ccpCode'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00028'
  currentMap['name'] = 'ccpCode'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2007-09-12-18:31:28_00003')

  # Attribute ChemAtomShiftCorr.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute ChemAtomShiftCorr.molType
  currentMap = {}
  contentMap['molType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00027'] = currentMap
  loadMaps['NMRR.ChemAtomShiftCorr.molType'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomShiftCorr.molType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00027'
  currentMap['name'] = 'molType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00024')

  # Attribute ChemAtomShiftCorr.seqOffset
  currentMap = {}
  contentMap['seqOffset'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00029'] = currentMap
  loadMaps['NMRR.ChemAtomShiftCorr.seqOffset'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomShiftCorr.seqOffset'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00029'
  currentMap['name'] = 'seqOffset'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute ChemAtomShiftCorr.value
  currentMap = {}
  contentMap['value'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00030'] = currentMap
  loadMaps['NMRR.ChemAtomShiftCorr.value'] = currentMap
  currentMap['tag'] = 'NMRR.ChemAtomShiftCorr.value'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00030'
  currentMap['name'] = 'value'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')
  # End of ChemAtomShiftCorr

  currentMap = abstractTypes.get('ChemAtomShiftCorr')
  aList = ['_ID', 'ccpCode', 'molType', 'seqOffset', 'value']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData']
  currentMap['simpleAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class ChemCompNmrRef
  currentMap = {}
  abstractTypes['ChemCompNmrRef'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00001'] = currentMap
  loadMaps['NMRR.ChemCompNmrRef'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompNmrRef'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'chemCompNmrRefs'
  currentMap['objkey'] = 'sourceName'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemCompNmrRef
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute ChemCompNmrRef._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute ChemCompNmrRef.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute ChemCompNmrRef.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute ChemCompNmrRef.details
  currentMap = {}
  contentMap['details'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00001'] = currentMap
  loadMaps['NMRR.ChemCompNmrRef.details'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompNmrRef.details'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00001'
  currentMap['name'] = 'details'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')

  # Attribute ChemCompNmrRef.sourceName
  currentMap = {}
  contentMap['sourceName'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:36_00106'] = currentMap
  loadMaps['NMRR.ChemCompNmrRef.sourceName'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompNmrRef.sourceName'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:36_00106'
  currentMap['name'] = 'sourceName'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Role ChemCompNmrRef.chemAtomNmrDistribs
  currentMap = {}
  contentMap['chemAtomNmrDistribs'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2010-05-14-17:17:46_00004'] = currentMap
  loadMaps['NMRR.ChemCompNmrRef.chemAtomNmrDistribs'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompNmrRef.chemAtomNmrDistribs'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-05-14-17:17:46_00004'
  currentMap['name'] = 'chemAtomNmrDistribs'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('NMRR').get('abstractTypes')

  # Role ChemCompNmrRef.chemAtomNmrRefs
  currentMap = {}
  contentMap['chemAtomNmrRefs'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:36_00103'] = currentMap
  loadMaps['NMRR.ChemCompNmrRef.chemAtomNmrRefs'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompNmrRef.chemAtomNmrRefs'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:36_00103'
  currentMap['name'] = 'chemAtomNmrRefs'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('NMRR').get('abstractTypes')

  # Role ChemCompNmrRef.chemCompVarNmrRefs
  currentMap = {}
  contentMap['chemCompVarNmrRefs'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:36_00105'] = currentMap
  loadMaps['NMRR.ChemCompNmrRef.chemCompVarNmrRefs'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompNmrRef.chemCompVarNmrRefs'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:36_00105'
  currentMap['name'] = 'chemCompVarNmrRefs'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('NMRR').get('abstractTypes')
  # End of ChemCompNmrRef

  currentMap = abstractTypes.get('ChemCompNmrRef')
  aList = ['_ID']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'details', 'sourceName']
  currentMap['simpleAttrs'] = aList
  aList = ['chemCompVarNmrRefs', 'chemAtomNmrRefs', 'chemAtomNmrDistribs', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['chemAtomNmrDistribs', 'chemAtomNmrRefs', 'chemCompVarNmrRefs']
  currentMap['children'] = aList

  # Class ChemCompVarNmrRef
  currentMap = {}
  abstractTypes['ChemCompVarNmrRef'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00006'] = currentMap
  loadMaps['NMRR.ChemCompVarNmrRef'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompVarNmrRef'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00006'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'chemCompVarNmrRefs'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemCompVarNmrRef
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute ChemCompVarNmrRef._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute ChemCompVarNmrRef.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute ChemCompVarNmrRef.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute ChemCompVarNmrRef.descriptor
  currentMap = {}
  contentMap['descriptor'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00037'] = currentMap
  loadMaps['NMRR.ChemCompVarNmrRef.descriptor'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompVarNmrRef.descriptor'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00037'
  currentMap['name'] = 'descriptor'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['default'] = 'any'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute ChemCompVarNmrRef.linking
  currentMap = {}
  contentMap['linking'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00036'] = currentMap
  loadMaps['NMRR.ChemCompVarNmrRef.linking'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompVarNmrRef.linking'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00036'
  currentMap['name'] = 'linking'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 'any'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00025')

  # Role ChemCompVarNmrRef.chemAtomNmrRefs
  currentMap = {}
  contentMap['chemAtomNmrRefs'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00034'] = currentMap
  loadMaps['NMRR.ChemCompVarNmrRef.chemAtomNmrRefs'] = currentMap
  currentMap['tag'] = 'NMRR.ChemCompVarNmrRef.chemAtomNmrRefs'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:37_00034'
  currentMap['name'] = 'chemAtomNmrRefs'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['copyOverride'] = True
  # End of ChemCompVarNmrRef

  currentMap = abstractTypes.get('ChemCompVarNmrRef')
  aList = ['_ID', 'linking']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'descriptor', 'chemAtomNmrRefs']
  currentMap['simpleAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class NmrReferenceStore
  currentMap = {}
  abstractTypes['NmrReferenceStore'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:49_00008'] = currentMap
  loadMaps['NMRR.NmrReferenceStore'] = currentMap
  currentMap['tag'] = 'NMRR.NmrReferenceStore'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:49_00008'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'nmrReferenceStores'
  currentMap['isTop'] = True
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.NmrReferenceStore
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute NmrReferenceStore._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute NmrReferenceStore._lastId
  contentMap['_lastId'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-05-13:04:27_00001')

  # Attribute NmrReferenceStore.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute NmrReferenceStore.ccpCode
  currentMap = {}
  contentMap['ccpCode'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:22:24_00001'] = currentMap
  loadMaps['NMRR.NmrReferenceStore.ccpCode'] = currentMap
  currentMap['tag'] = 'NMRR.NmrReferenceStore.ccpCode'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:22:24_00001'
  currentMap['name'] = 'ccpCode'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2007-09-12-18:31:28_00003')

  # Attribute NmrReferenceStore.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute NmrReferenceStore.createdBy
  contentMap['createdBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00002__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute NmrReferenceStore.guid
  contentMap['guid'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:26_00002')

  # Attribute NmrReferenceStore.isModifiable
  contentMap['isModifiable'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-17-14:16:26_00010__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute NmrReferenceStore.lastUnlockedBy
  contentMap['lastUnlockedBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00003__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute NmrReferenceStore.molType
  currentMap = {}
  contentMap['molType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:22:23_00001'] = currentMap
  loadMaps['NMRR.NmrReferenceStore.molType'] = currentMap
  currentMap['tag'] = 'NMRR.NmrReferenceStore.molType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:22:23_00001'
  currentMap['name'] = 'molType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00024')

  # Attribute NmrReferenceStore.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:22:26_00001'] = currentMap
  loadMaps['NMRR.NmrReferenceStore.name'] = currentMap
  currentMap['tag'] = 'NMRR.NmrReferenceStore.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:22:26_00001'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['default'] = 'auto'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Role NmrReferenceStore.chemCompNmrRefs
  currentMap = {}
  contentMap['chemCompNmrRefs'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:22:22_00002'] = currentMap
  loadMaps['NMRR.NmrReferenceStore.chemCompNmrRefs'] = currentMap
  currentMap['tag'] = 'NMRR.NmrReferenceStore.chemCompNmrRefs'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:22:22_00002'
  currentMap['name'] = 'chemCompNmrRefs'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('NMRR').get('abstractTypes')
  # End of NmrReferenceStore

  currentMap = abstractTypes.get('NmrReferenceStore')
  aList = ['_ID', '_lastId', 'ccpCode', 'createdBy', 'guid', 'isModifiable', 'lastUnlockedBy', 'molType']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'name']
  currentMap['simpleAttrs'] = aList
  aList = ['chemCompNmrRefs', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['chemCompNmrRefs']
  currentMap['children'] = aList

  # Out-of-package link to ChemAtomNmrDistrib
  currentMap = {}
  exolinks['ChemAtomNmrDistrib'] = currentMap
  loadMaps['NMRR.exo-ChemAtomNmrDistrib'] = currentMap
  currentMap['tag'] = 'NMRR.exo-ChemAtomNmrDistrib'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-05-14-15:28:22_00001'
  currentMap['name'] = 'ChemAtomNmrDistrib'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemAtomNmrDistrib
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to ChemAtomNmrRef
  currentMap = {}
  exolinks['ChemAtomNmrRef'] = currentMap
  loadMaps['NMRR.exo-ChemAtomNmrRef'] = currentMap
  currentMap['tag'] = 'NMRR.exo-ChemAtomNmrRef'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00002'
  currentMap['name'] = 'ChemAtomNmrRef'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemAtomNmrRef
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to ChemAtomShiftCorr
  currentMap = {}
  exolinks['ChemAtomShiftCorr'] = currentMap
  loadMaps['NMRR.exo-ChemAtomShiftCorr'] = currentMap
  currentMap['tag'] = 'NMRR.exo-ChemAtomShiftCorr'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00005'
  currentMap['name'] = 'ChemAtomShiftCorr'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemAtomShiftCorr
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00024'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2007-09-12-18:31:28_00003'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to ChemCompNmrRef
  currentMap = {}
  exolinks['ChemCompNmrRef'] = currentMap
  loadMaps['NMRR.exo-ChemCompNmrRef'] = currentMap
  currentMap['tag'] = 'NMRR.exo-ChemCompNmrRef'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00001'
  currentMap['name'] = 'ChemCompNmrRef'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemCompNmrRef
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'))

  # Out-of-package link to ChemCompVarNmrRef
  currentMap = {}
  exolinks['ChemCompVarNmrRef'] = currentMap
  loadMaps['NMRR.exo-ChemCompVarNmrRef'] = currentMap
  currentMap['tag'] = 'NMRR.exo-ChemCompVarNmrRef'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:25:09_00006'
  currentMap['name'] = 'ChemCompVarNmrRef'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.ChemCompVarNmrRef
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:52_00025'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'))

  # Out-of-package link to NmrReferenceStore
  currentMap = {}
  exolinks['NmrReferenceStore'] = currentMap
  loadMaps['NMRR.exo-NmrReferenceStore'] = currentMap
  currentMap['tag'] = 'NMRR.exo-NmrReferenceStore'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:49_00008'
  currentMap['name'] = 'NmrReferenceStore'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.nmr.NmrReference.NmrReferenceStore
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
