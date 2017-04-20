"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Thu Apr 13 07:15:42 2017
  from data model element ccp.general.Instrument

#######################################################################
======================COPYRIGHT/LICENSE START==========================

Instrument.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccp.general.Instrument

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
import ccpnmodel.ccpncore.api.ccp.general.Instrument

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package INST, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('INST').get('abstractTypes')
  exolinks = globalMap.get('INST').get('exolinks')

  # DataType NmrProbeType
  currentMap = {}
  abstractTypes['NmrProbeType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00002'] = currentMap
  loadMaps['INST.NmrProbeType'] = currentMap
  currentMap['tag'] = 'INST.NmrProbeType'
  currentMap['type'] = 'simple'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00002'
  currentMap['toStr'] = 'text'
  currentMap['cnvrt'] = 'text'

  # DataType SpectrometerFreq
  currentMap = {}
  abstractTypes['SpectrometerFreq'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00003'] = currentMap
  loadMaps['INST.SpectrometerFreq'] = currentMap
  currentMap['tag'] = 'INST.SpectrometerFreq'
  currentMap['type'] = 'simple'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00003'
  currentMap['toStr'] = 'text'
  currentMap['cnvrt'] = 'text'

  # Class AbstractInstrument
  currentMap = {}
  abstractTypes['AbstractInstrument'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:45_00039'] = currentMap
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:45_00039'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'instruments'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.AbstractInstrument
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute AbstractInstrument._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute AbstractInstrument.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute AbstractInstrument.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute AbstractInstrument.details
  currentMap = {}
  contentMap['details'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00005'] = currentMap
  loadMaps['INST.AbstractInstrument.details'] = currentMap
  currentMap['tag'] = 'INST.AbstractInstrument.details'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00005'
  currentMap['name'] = 'details'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['proc'] = 'direct'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035')

  # Attribute AbstractInstrument.model
  currentMap = {}
  contentMap['model'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00002'] = currentMap
  loadMaps['INST.AbstractInstrument.model'] = currentMap
  currentMap['tag'] = 'INST.AbstractInstrument.model'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00002'
  currentMap['name'] = 'model'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute AbstractInstrument.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00001'] = currentMap
  loadMaps['INST.AbstractInstrument.name'] = currentMap
  currentMap['tag'] = 'INST.AbstractInstrument.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00001'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute AbstractInstrument.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00003'] = currentMap
  loadMaps['INST.AbstractInstrument.serial'] = currentMap
  currentMap['tag'] = 'INST.AbstractInstrument.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00003'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute AbstractInstrument.serialNumber
  currentMap = {}
  contentMap['serialNumber'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00004'] = currentMap
  loadMaps['INST.AbstractInstrument.serialNumber'] = currentMap
  currentMap['tag'] = 'INST.AbstractInstrument.serialNumber'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00004'
  currentMap['name'] = 'serialNumber'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Role AbstractInstrument.contactPerson
  currentMap = {}
  contentMap['contactPerson'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00001'] = currentMap
  loadMaps['INST.AbstractInstrument.contactPerson'] = currentMap
  currentMap['tag'] = 'INST.AbstractInstrument.contactPerson'
  currentMap['type'] = 'exolink'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00001'
  currentMap['name'] = 'contactPerson'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['copyOverride'] = True
  currentMap['content'] = globalMap.get('AFFI').get('exolinks')

  # Role AbstractInstrument.manufacturer
  currentMap = {}
  contentMap['manufacturer'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00002'] = currentMap
  loadMaps['INST.AbstractInstrument.manufacturer'] = currentMap
  currentMap['tag'] = 'INST.AbstractInstrument.manufacturer'
  currentMap['type'] = 'exolink'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00002'
  currentMap['name'] = 'manufacturer'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['copyOverride'] = True
  currentMap['content'] = globalMap.get('AFFI').get('exolinks')
  # End of AbstractInstrument

  currentMap = abstractTypes.get('AbstractInstrument')
  aList = ['_ID', 'serial']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'details', 'model', 'name', 'serialNumber']
  currentMap['simpleAttrs'] = aList
  aList = ['manufacturer', 'contactPerson', 'applicationData']
  currentMap['cplxAttrs'] = aList

  # Class InstrumentStore
  currentMap = {}
  abstractTypes['InstrumentStore'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:19:49_00001'] = currentMap
  loadMaps['INST.InstrumentStore'] = currentMap
  currentMap['tag'] = 'INST.InstrumentStore'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:19:49_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'instrumentStores'
  currentMap['isTop'] = True
  currentMap['objkey'] = 'name'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.InstrumentStore
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute InstrumentStore._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute InstrumentStore._lastId
  contentMap['_lastId'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-05-13:04:27_00001')

  # Attribute InstrumentStore.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute InstrumentStore.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute InstrumentStore.createdBy
  contentMap['createdBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00002__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute InstrumentStore.guid
  contentMap['guid'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:26_00002')

  # Attribute InstrumentStore.isModifiable
  contentMap['isModifiable'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-17-14:16:26_00010__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute InstrumentStore.lastUnlockedBy
  contentMap['lastUnlockedBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00003__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute InstrumentStore.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:05_00004'] = currentMap
  loadMaps['INST.InstrumentStore.name'] = currentMap
  currentMap['tag'] = 'INST.InstrumentStore.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:05_00004'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Role InstrumentStore.instruments
  currentMap = {}
  contentMap['instruments'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:05_00001'] = currentMap
  loadMaps['INST.InstrumentStore.instruments'] = currentMap
  currentMap['tag'] = 'INST.InstrumentStore.instruments'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:05_00001'
  currentMap['name'] = 'instruments'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('INST').get('abstractTypes')
  # End of InstrumentStore

  currentMap = abstractTypes.get('InstrumentStore')
  aList = ['_ID', '_lastId', 'createdBy', 'guid', 'isModifiable', 'lastUnlockedBy']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'name']
  currentMap['simpleAttrs'] = aList
  aList = ['instruments', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['instruments']
  currentMap['children'] = aList

  # Class NmrProbe
  currentMap = {}
  abstractTypes['NmrProbe'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:45_00041'] = currentMap
  loadMaps['INST.NmrProbe'] = currentMap
  currentMap['tag'] = 'INST.NmrProbe'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:45_00041'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'instruments'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.NmrProbe
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute NmrProbe._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute NmrProbe.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute NmrProbe.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute NmrProbe.details
  contentMap['details'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00005')

  # Attribute NmrProbe.diameter
  currentMap = {}
  contentMap['diameter'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00004'] = currentMap
  loadMaps['INST.NmrProbe.diameter'] = currentMap
  currentMap['tag'] = 'INST.NmrProbe.diameter'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00004'
  currentMap['name'] = 'diameter'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute NmrProbe.instrumentType
  currentMap = {}
  contentMap['instrumentType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00002'] = currentMap
  loadMaps['INST.NmrProbe.instrumentType'] = currentMap
  currentMap['tag'] = 'INST.NmrProbe.instrumentType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00002'
  currentMap['name'] = 'instrumentType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['default'] = 'NmrProbe'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute NmrProbe.model
  contentMap['model'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00002')

  # Attribute NmrProbe.name
  contentMap['name'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00001')

  # Attribute NmrProbe.probeType
  currentMap = {}
  contentMap['probeType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00003'] = currentMap
  loadMaps['INST.NmrProbe.probeType'] = currentMap
  currentMap['tag'] = 'INST.NmrProbe.probeType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00003'
  currentMap['name'] = 'probeType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00002')

  # Attribute NmrProbe.serial
  contentMap['serial'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00003')

  # Attribute NmrProbe.serialNumber
  contentMap['serialNumber'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00004')

  # Role NmrProbe.citations
  currentMap = {}
  contentMap['citations'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00001'] = currentMap
  loadMaps['INST.NmrProbe.citations'] = currentMap
  currentMap['tag'] = 'INST.NmrProbe.citations'
  currentMap['type'] = 'exolink'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00001'
  currentMap['name'] = 'citations'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['copyOverride'] = True
  currentMap['content'] = globalMap.get('CITA').get('exolinks')

  # Role NmrProbe.contactPerson
  contentMap['contactPerson'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00001')

  # Role NmrProbe.manufacturer
  contentMap['manufacturer'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00002')
  # End of NmrProbe

  currentMap = abstractTypes.get('NmrProbe')
  aList = ['_ID', 'diameter', 'serial']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'details', 'instrumentType', 'model', 'name', 'probeType', 'serialNumber']
  currentMap['simpleAttrs'] = aList
  aList = ['manufacturer', 'contactPerson', 'citations', 'applicationData']
  currentMap['cplxAttrs'] = aList

  # Class Instrument
  currentMap = {}
  abstractTypes['Instrument'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00001'] = currentMap
  loadMaps['INST.Instrument'] = currentMap
  currentMap['tag'] = 'INST.Instrument'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'instruments'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.Instrument
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute Instrument._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute Instrument.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute Instrument.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute Instrument.details
  contentMap['details'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00005')

  # Attribute Instrument.instrumentType
  currentMap = {}
  contentMap['instrumentType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-11-08-10:15:19_00001'] = currentMap
  loadMaps['INST.Instrument.instrumentType'] = currentMap
  currentMap['tag'] = 'INST.Instrument.instrumentType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-11-08-10:15:19_00001'
  currentMap['name'] = 'instrumentType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute Instrument.model
  contentMap['model'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00002')

  # Attribute Instrument.name
  contentMap['name'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00001')

  # Attribute Instrument.serial
  contentMap['serial'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00003')

  # Attribute Instrument.serialNumber
  contentMap['serialNumber'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00004')

  # Role Instrument.contactPerson
  contentMap['contactPerson'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00001')

  # Role Instrument.manufacturer
  contentMap['manufacturer'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00002')
  # End of Instrument

  currentMap = abstractTypes.get('Instrument')
  aList = ['_ID', 'serial']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'details', 'instrumentType', 'model', 'name', 'serialNumber']
  currentMap['simpleAttrs'] = aList
  aList = ['manufacturer', 'contactPerson', 'applicationData']
  currentMap['cplxAttrs'] = aList

  # Class NmrSpectrometer
  currentMap = {}
  abstractTypes['NmrSpectrometer'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:45_00040'] = currentMap
  loadMaps['INST.NmrSpectrometer'] = currentMap
  currentMap['tag'] = 'INST.NmrSpectrometer'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:45_00040'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'instruments'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.NmrSpectrometer
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute NmrSpectrometer._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute NmrSpectrometer.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute NmrSpectrometer.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute NmrSpectrometer.details
  contentMap['details'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00005')

  # Attribute NmrSpectrometer.instrumentType
  currentMap = {}
  contentMap['instrumentType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00008'] = currentMap
  loadMaps['INST.NmrSpectrometer.instrumentType'] = currentMap
  currentMap['tag'] = 'INST.NmrSpectrometer.instrumentType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00008'
  currentMap['name'] = 'instrumentType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['default'] = 'NmrSpectrometer'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute NmrSpectrometer.model
  contentMap['model'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00002')

  # Attribute NmrSpectrometer.name
  contentMap['name'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00001')

  # Attribute NmrSpectrometer.nominalFreq
  currentMap = {}
  contentMap['nominalFreq'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00010'] = currentMap
  loadMaps['INST.NmrSpectrometer.nominalFreq'] = currentMap
  currentMap['tag'] = 'INST.NmrSpectrometer.nominalFreq'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00010'
  currentMap['name'] = 'nominalFreq'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00003')

  # Attribute NmrSpectrometer.protonFreq
  currentMap = {}
  contentMap['protonFreq'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00009'] = currentMap
  loadMaps['INST.NmrSpectrometer.protonFreq'] = currentMap
  currentMap['tag'] = 'INST.NmrSpectrometer.protonFreq'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00009'
  currentMap['name'] = 'protonFreq'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute NmrSpectrometer.serial
  contentMap['serial'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00003')

  # Attribute NmrSpectrometer.serialNumber
  contentMap['serialNumber'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00004')

  # Role NmrSpectrometer.citations
  currentMap = {}
  contentMap['citations'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00007'] = currentMap
  loadMaps['INST.NmrSpectrometer.citations'] = currentMap
  currentMap['tag'] = 'INST.NmrSpectrometer.citations'
  currentMap['type'] = 'exolink'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00007'
  currentMap['name'] = 'citations'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['copyOverride'] = True
  currentMap['content'] = globalMap.get('CITA').get('exolinks')

  # Role NmrSpectrometer.contactPerson
  contentMap['contactPerson'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00001')

  # Role NmrSpectrometer.manufacturer
  contentMap['manufacturer'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00002')
  # End of NmrSpectrometer

  currentMap = abstractTypes.get('NmrSpectrometer')
  aList = ['_ID', 'nominalFreq', 'protonFreq', 'serial']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'details', 'instrumentType', 'model', 'name', 'serialNumber']
  currentMap['simpleAttrs'] = aList
  aList = ['manufacturer', 'contactPerson', 'citations', 'applicationData']
  currentMap['cplxAttrs'] = aList

  # Class Column
  currentMap = {}
  abstractTypes['Column'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00004'] = currentMap
  loadMaps['INST.Column'] = currentMap
  currentMap['tag'] = 'INST.Column'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00004'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'instruments'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.Column
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute Column._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute Column.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute Column.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute Column.columnType
  currentMap = {}
  contentMap['columnType'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00009'] = currentMap
  loadMaps['INST.Column.columnType'] = currentMap
  currentMap['tag'] = 'INST.Column.columnType'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00009'
  currentMap['name'] = 'columnType'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Attribute Column.details
  contentMap['details'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00005')

  # Attribute Column.instrumentType
  contentMap['instrumentType'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2007-11-08-10:15:19_00001')

  # Attribute Column.model
  contentMap['model'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00002')

  # Attribute Column.name
  contentMap['name'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00001')

  # Attribute Column.serial
  contentMap['serial'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00003')

  # Attribute Column.serialNumber
  contentMap['serialNumber'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:03_00004')

  # Attribute Column.volume
  currentMap = {}
  contentMap['volume'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00010'] = currentMap
  loadMaps['INST.Column.volume'] = currentMap
  currentMap['tag'] = 'INST.Column.volume'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00010'
  currentMap['name'] = 'volume'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031')

  # Attribute Column.volumeDisplayUnit
  currentMap = {}
  contentMap['volumeDisplayUnit'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00011'] = currentMap
  loadMaps['INST.Column.volumeDisplayUnit'] = currentMap
  currentMap['tag'] = 'INST.Column.volumeDisplayUnit'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:04_00011'
  currentMap['name'] = 'volumeDisplayUnit'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Role Column.contactPerson
  contentMap['contactPerson'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00001')

  # Role Column.manufacturer
  contentMap['manufacturer'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-18:23:02_00002')
  # End of Column

  currentMap = abstractTypes.get('Column')
  aList = ['_ID', 'serial', 'volume', 'volumeDisplayUnit']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'columnType', 'details', 'instrumentType', 'model', 'name', 'serialNumber']
  currentMap['simpleAttrs'] = aList
  aList = ['manufacturer', 'contactPerson', 'applicationData']
  currentMap['cplxAttrs'] = aList

  # Out-of-package link to InstrumentStore
  currentMap = {}
  exolinks['InstrumentStore'] = currentMap
  loadMaps['INST.exo-InstrumentStore'] = currentMap
  currentMap['tag'] = 'INST.exo-InstrumentStore'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:19:49_00001'
  currentMap['name'] = 'InstrumentStore'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.InstrumentStore
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))

  # Out-of-package link to NmrProbe
  currentMap = {}
  exolinks['NmrProbe'] = currentMap
  loadMaps['INST.exo-NmrProbe'] = currentMap
  currentMap['tag'] = 'INST.exo-NmrProbe'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:45_00041'
  currentMap['name'] = 'NmrProbe'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.NmrProbe
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to Instrument
  currentMap = {}
  exolinks['Instrument'] = currentMap
  loadMaps['INST.exo-Instrument'] = currentMap
  currentMap['tag'] = 'INST.exo-Instrument'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00001'
  currentMap['name'] = 'Instrument'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.Instrument
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to NmrSpectrometer
  currentMap = {}
  exolinks['NmrSpectrometer'] = currentMap
  loadMaps['INST.exo-NmrSpectrometer'] = currentMap
  currentMap['tag'] = 'INST.exo-NmrSpectrometer'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:45_00040'
  currentMap['name'] = 'NmrSpectrometer'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.NmrSpectrometer
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to Column
  currentMap = {}
  exolinks['Column'] = currentMap
  loadMaps['INST.exo-Column'] = currentMap
  currentMap['tag'] = 'INST.exo-Column'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:46_00004'
  currentMap['name'] = 'Column'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.general.Instrument.Column
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
