"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Sat Aug 19 14:47:15 2017
  from data model element ccpnmr.gui.Window

#######################################################################
======================COPYRIGHT/LICENSE START==========================

Window.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccpnmr.gui.Window

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
import ccpnmodel.ccpncore.api.ccpnmr.gui.Window

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package GUIW, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('GUIW').get('abstractTypes')
  exolinks = globalMap.get('GUIW').get('exolinks')

  # Class Window
  currentMap = {}
  abstractTypes['Window'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00001'] = currentMap
  loadMaps['GUIW.Window'] = currentMap
  currentMap['tag'] = 'GUIW.Window'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'windows'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccpnmr.gui.Window.Window
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute Window._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute Window.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute Window.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute Window.position
  currentMap = {}
  contentMap['position'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00015'] = currentMap
  loadMaps['GUIW.Window.position'] = currentMap
  currentMap['tag'] = 'GUIW.Window.position'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00015'
  currentMap['name'] = 'position'
  currentMap['hicard'] = 2
  currentMap['locard'] = 2
  currentMap['default'] = [0, 0]
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute Window.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00013'] = currentMap
  loadMaps['GUIW.Window.serial'] = currentMap
  currentMap['tag'] = 'GUIW.Window.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00013'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute Window.size
  currentMap = {}
  contentMap['size'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00001'] = currentMap
  loadMaps['GUIW.Window.size'] = currentMap
  currentMap['tag'] = 'GUIW.Window.size'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00001'
  currentMap['name'] = 'size'
  currentMap['hicard'] = 2
  currentMap['locard'] = 2
  currentMap['default'] = [400, 400]
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute Window.title
  currentMap = {}
  contentMap['title'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00014'] = currentMap
  loadMaps['GUIW.Window.title'] = currentMap
  currentMap['tag'] = 'GUIW.Window.title'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:30_00014'
  currentMap['name'] = 'title'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')
  # End of Window

  currentMap = abstractTypes.get('Window')
  aList = ['_ID', 'serial', 'title']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'position', 'size']
  currentMap['simpleAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class WindowStore
  currentMap = {}
  abstractTypes['WindowStore'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00003'] = currentMap
  loadMaps['GUIW.WindowStore'] = currentMap
  currentMap['tag'] = 'GUIW.WindowStore'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00003'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'windowStores'
  currentMap['isTop'] = True
  currentMap['objkey'] = 'nmrProject'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccpnmr.gui.Window.WindowStore
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute WindowStore._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute WindowStore._lastId
  contentMap['_lastId'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-05-13:04:27_00001')

  # Attribute WindowStore.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute WindowStore.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute WindowStore.createdBy
  contentMap['createdBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00002__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute WindowStore.guid
  contentMap['guid'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:26_00002')

  # Attribute WindowStore.isModifiable
  contentMap['isModifiable'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-17-14:16:26_00010__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute WindowStore.lastUnlockedBy
  contentMap['lastUnlockedBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00003__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Role WindowStore.mainWindow
  currentMap = {}
  contentMap['mainWindow'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00008'] = currentMap
  loadMaps['GUIW.WindowStore.mainWindow'] = currentMap
  currentMap['tag'] = 'GUIW.WindowStore.mainWindow'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00008'
  currentMap['name'] = 'mainWindow'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['implSkip'] = True
  currentMap['copyOverride'] = True

  # Role WindowStore.nmrProject
  currentMap = {}
  contentMap['nmrProject'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:36:29_00001'] = currentMap
  loadMaps['GUIW.WindowStore.nmrProject'] = currentMap
  currentMap['tag'] = 'GUIW.WindowStore.nmrProject'
  currentMap['type'] = 'exotop'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:29_00001'
  currentMap['name'] = 'nmrProject'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['copyOverride'] = False
  currentMap['content'] = globalMap.get('NMR').get('exolinks')

  # Role WindowStore.windows
  currentMap = {}
  contentMap['windows'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00003'] = currentMap
  loadMaps['GUIW.WindowStore.windows'] = currentMap
  currentMap['tag'] = 'GUIW.WindowStore.windows'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:40:01_00003'
  currentMap['name'] = 'windows'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('GUIW').get('abstractTypes')
  # End of WindowStore

  currentMap = abstractTypes.get('WindowStore')
  aList = ['_ID', '_lastId', 'createdBy', 'guid', 'isModifiable', 'lastUnlockedBy']
  currentMap['headerAttrs'] = aList
  aList = ['ccpnInternalData', 'mainWindow']
  currentMap['simpleAttrs'] = aList
  aList = ['windows', 'nmrProject', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['windows']
  currentMap['children'] = aList

  # Out-of-package link to Window
  currentMap = {}
  exolinks['Window'] = currentMap
  loadMaps['GUIW.exo-Window'] = currentMap
  currentMap['tag'] = 'GUIW.exo-Window'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00001'
  currentMap['name'] = 'Window'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccpnmr.gui.Window.Window
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to WindowStore
  currentMap = {}
  exolinks['WindowStore'] = currentMap
  loadMaps['GUIW.exo-WindowStore'] = currentMap
  currentMap['tag'] = 'GUIW.exo-WindowStore'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2014-10-31-16:36:26_00003'
  currentMap['name'] = 'WindowStore'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccpnmr.gui.Window.WindowStore
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
