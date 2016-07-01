"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Fri Jul  1 02:26:26 2016
  from data model element ccp.general.Template

#######################################################################
======================COPYRIGHT/LICENSE START==========================

Template.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccp.general.Template

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
import ccpnmodel.ccpncore.api.ccp.general.Template

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package TEMP, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('TEMP').get('abstractTypes')
  exolinks = globalMap.get('TEMP').get('exolinks')

  # Class AbstractProbability
  currentMap = {}
  abstractTypes['AbstractProbability'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:19:50_00005'] = currentMap
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:19:50_00005'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Template.AbstractProbability
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute AbstractProbability._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute AbstractProbability.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute AbstractProbability.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute AbstractProbability.weight
  currentMap = {}
  contentMap['weight'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:38_00025'] = currentMap
  loadMaps['TEMP.AbstractProbability.weight'] = currentMap
  currentMap['tag'] = 'TEMP.AbstractProbability.weight'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:38_00025'
  currentMap['name'] = 'weight'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 1.0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')
  # End of AbstractProbability

  currentMap = abstractTypes.get('AbstractProbability')
  aList = ['_ID', 'ccpnInternalData', 'weight']
  currentMap['headerAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class MultiTypeValue
  currentMap = {}
  abstractTypes['MultiTypeValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-13-15:55:49_00003'] = currentMap
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-13-15:55:49_00003'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Template.MultiTypeValue
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute MultiTypeValue._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute MultiTypeValue.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute MultiTypeValue.booleanValue
  currentMap = {}
  contentMap['booleanValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-13-15:55:55_00008'] = currentMap
  loadMaps['TEMP.MultiTypeValue.booleanValue'] = currentMap
  currentMap['tag'] = 'TEMP.MultiTypeValue.booleanValue'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-13-15:55:55_00008'
  currentMap['name'] = 'booleanValue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00028')

  # Attribute MultiTypeValue.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute MultiTypeValue.floatValue
  currentMap = {}
  contentMap['floatValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-13-15:55:55_00007'] = currentMap
  loadMaps['TEMP.MultiTypeValue.floatValue'] = currentMap
  currentMap['tag'] = 'TEMP.MultiTypeValue.floatValue'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-13-15:55:55_00007'
  currentMap['name'] = 'floatValue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute MultiTypeValue.intValue
  currentMap = {}
  contentMap['intValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-13-15:55:55_00006'] = currentMap
  loadMaps['TEMP.MultiTypeValue.intValue'] = currentMap
  currentMap['tag'] = 'TEMP.MultiTypeValue.intValue'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-13-15:55:55_00006'
  currentMap['name'] = 'intValue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute MultiTypeValue.textValue
  currentMap = {}
  contentMap['textValue'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-13-15:55:55_00005'] = currentMap
  loadMaps['TEMP.MultiTypeValue.textValue'] = currentMap
  currentMap['tag'] = 'TEMP.MultiTypeValue.textValue'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-13-15:55:55_00005'
  currentMap['name'] = 'textValue'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')
  # End of MultiTypeValue

  currentMap = abstractTypes.get('MultiTypeValue')
  aList = ['_ID', 'booleanValue', 'ccpnInternalData', 'floatValue', 'intValue']
  currentMap['headerAttrs'] = aList
  aList = ['textValue']
  currentMap['simpleAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

