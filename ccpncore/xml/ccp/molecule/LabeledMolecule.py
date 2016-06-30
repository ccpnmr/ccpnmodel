"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyXmlMapWrite on Wed Jun 29 13:17:17 2016
  from data model element ccp.molecule.LabeledMolecule

#######################################################################
======================COPYRIGHT/LICENSE START==========================

LabeledMolecule.py: python XML-I/O-mapping for CCPN data model, MetaPackage ccp.molecule.LabeledMolecule

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
import ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule

def makeMapping(globalMap):
  """
  generates XML I/O mapping for package LMOL, adding it to globalMap
  """
  
  from ccpnmodel.ccpncore.xml.memops.Implementation import bool2str, str2bool

  # Set up top level dictionaries
  loadMaps = globalMap.get('loadMaps')
  mapsByGuid = globalMap.get('mapsByGuid')

  abstractTypes = globalMap.get('LMOL').get('abstractTypes')
  exolinks = globalMap.get('LMOL').get('exolinks')

  # Class AtomLabel
  currentMap = {}
  abstractTypes['AtomLabel'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00005'] = currentMap
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00005'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'atomLabels'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.AtomLabel
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute AtomLabel._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute AtomLabel.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute AtomLabel.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute AtomLabel.massNumber
  currentMap = {}
  contentMap['massNumber'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00005'] = currentMap
  loadMaps['LMOL.AtomLabel.massNumber'] = currentMap
  currentMap['tag'] = 'LMOL.AtomLabel.massNumber'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00005'
  currentMap['name'] = 'massNumber'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00001')

  # Attribute AtomLabel.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00004'] = currentMap
  loadMaps['LMOL.AtomLabel.serial'] = currentMap
  currentMap['tag'] = 'LMOL.AtomLabel.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00004'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Attribute AtomLabel.weight
  currentMap = {}
  contentMap['weight'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00006'] = currentMap
  loadMaps['LMOL.AtomLabel.weight'] = currentMap
  currentMap['tag'] = 'LMOL.AtomLabel.weight'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00006'
  currentMap['name'] = 'weight'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 1.0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00009')
  # End of AtomLabel

  currentMap = abstractTypes.get('AtomLabel')
  aList = ['_ID', 'ccpnInternalData', 'massNumber', 'serial', 'weight']
  currentMap['headerAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class LabeledMixture
  currentMap = {}
  abstractTypes['LabeledMixture'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00008'] = currentMap
  loadMaps['LMOL.LabeledMixture'] = currentMap
  currentMap['tag'] = 'LMOL.LabeledMixture'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00008'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'labeledMixtures'
  currentMap['objkey'] = 'name'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.LabeledMixture
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute LabeledMixture._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute LabeledMixture.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute LabeledMixture.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute LabeledMixture.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2010-04-30-17:48:49_00001'] = currentMap
  loadMaps['LMOL.LabeledMixture.name'] = currentMap
  currentMap['tag'] = 'LMOL.LabeledMixture.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2010-04-30-17:48:49_00001'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['default'] = 'Mixture1'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Role LabeledMixture.averageComposition
  currentMap = {}
  contentMap['averageComposition'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-24-12:23:56_00001'] = currentMap
  loadMaps['LMOL.LabeledMixture.averageComposition'] = currentMap
  currentMap['tag'] = 'LMOL.LabeledMixture.averageComposition'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-24-12:23:56_00001'
  currentMap['name'] = 'averageComposition'
  currentMap['hicard'] = 1
  currentMap['locard'] = 0
  currentMap['copyOverride'] = True

  # Role LabeledMixture.molLabelFractions
  currentMap = {}
  contentMap['molLabelFractions'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00010'] = currentMap
  loadMaps['LMOL.LabeledMixture.molLabelFractions'] = currentMap
  currentMap['tag'] = 'LMOL.LabeledMixture.molLabelFractions'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00010'
  currentMap['name'] = 'molLabelFractions'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('LMOL').get('abstractTypes')
  # End of LabeledMixture

  currentMap = abstractTypes.get('LabeledMixture')
  aList = ['_ID', 'ccpnInternalData']
  currentMap['headerAttrs'] = aList
  aList = ['name']
  currentMap['simpleAttrs'] = aList
  aList = ['averageComposition']
  currentMap['optLinks'] = aList
  aList = ['molLabelFractions', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['molLabelFractions']
  currentMap['children'] = aList

  # Class LabeledMolecule
  currentMap = {}
  abstractTypes['LabeledMolecule'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00002'] = currentMap
  loadMaps['LMOL.LabeledMolecule'] = currentMap
  currentMap['tag'] = 'LMOL.LabeledMolecule'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00002'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'labeledMolecules'
  currentMap['isTop'] = True
  currentMap['objkey'] = 'name'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.LabeledMolecule
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute LabeledMolecule._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute LabeledMolecule._lastId
  contentMap['_lastId'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-05-13:04:27_00001')

  # Attribute LabeledMolecule.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute LabeledMolecule.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute LabeledMolecule.createdBy
  contentMap['createdBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00002__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute LabeledMolecule.guid
  contentMap['guid'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:26_00002')

  # Attribute LabeledMolecule.isModifiable
  contentMap['isModifiable'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-17-14:16:26_00010__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute LabeledMolecule.lastUnlockedBy
  contentMap['lastUnlockedBy'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-12-31-09:00:59_00003__www.ccpn.ac.uk_Fogh_2007-10-03-14:53:27_00001__www.ccpn.ac.uk_Fogh_2006-09-14-16:28:57_00002')

  # Attribute LabeledMolecule.name
  currentMap = {}
  contentMap['name'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00013'] = currentMap
  loadMaps['LMOL.LabeledMolecule.name'] = currentMap
  currentMap['tag'] = 'LMOL.LabeledMolecule.name'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00013'
  currentMap['name'] = 'name'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['eType'] = 'cplx'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033')

  # Role LabeledMolecule.labeledMixtures
  currentMap = {}
  contentMap['labeledMixtures'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00010'] = currentMap
  loadMaps['LMOL.LabeledMolecule.labeledMixtures'] = currentMap
  currentMap['tag'] = 'LMOL.LabeledMolecule.labeledMixtures'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00010'
  currentMap['name'] = 'labeledMixtures'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('LMOL').get('abstractTypes')

  # Role LabeledMolecule.molLabels
  currentMap = {}
  contentMap['molLabels'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00008'] = currentMap
  loadMaps['LMOL.LabeledMolecule.molLabels'] = currentMap
  currentMap['tag'] = 'LMOL.LabeledMolecule.molLabels'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00008'
  currentMap['name'] = 'molLabels'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['implSkip'] = True
  currentMap['content'] = globalMap.get('LMOL').get('abstractTypes')
  # End of LabeledMolecule

  currentMap = abstractTypes.get('LabeledMolecule')
  aList = ['_ID', '_lastId', 'ccpnInternalData', 'createdBy', 'guid', 'isModifiable', 'lastUnlockedBy']
  currentMap['headerAttrs'] = aList
  aList = ['name']
  currentMap['simpleAttrs'] = aList
  aList = ['molLabels', 'labeledMixtures', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['labeledMixtures', 'molLabels']
  currentMap['children'] = aList

  # Class MolLabel
  currentMap = {}
  abstractTypes['MolLabel'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00003'] = currentMap
  loadMaps['LMOL.MolLabel'] = currentMap
  currentMap['tag'] = 'LMOL.MolLabel'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00003'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'molLabels'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.MolLabel
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute MolLabel._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute MolLabel.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute MolLabel.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute MolLabel.serial
  currentMap = {}
  contentMap['serial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00016'] = currentMap
  loadMaps['LMOL.MolLabel.serial'] = currentMap
  currentMap['tag'] = 'LMOL.MolLabel.serial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00016'
  currentMap['name'] = 'serial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032')

  # Role MolLabel.averageLabeledMixtures
  currentMap = {}
  contentMap['averageLabeledMixtures'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00006'] = currentMap
  loadMaps['LMOL.MolLabel.averageLabeledMixtures'] = currentMap
  currentMap['tag'] = 'LMOL.MolLabel.averageLabeledMixtures'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-24-12:23:55_00006'
  currentMap['name'] = 'averageLabeledMixtures'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['copyOverride'] = False

  # Role MolLabel.molLabelFractions
  currentMap = {}
  contentMap['molLabelFractions'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00014'] = currentMap
  loadMaps['LMOL.MolLabel.molLabelFractions'] = currentMap
  currentMap['tag'] = 'LMOL.MolLabel.molLabelFractions'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00014'
  currentMap['name'] = 'molLabelFractions'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['copyOverride'] = False

  # Role MolLabel.resLabels
  currentMap = {}
  contentMap['resLabels'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00015'] = currentMap
  loadMaps['LMOL.MolLabel.resLabels'] = currentMap
  currentMap['tag'] = 'LMOL.MolLabel.resLabels'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:14_00015'
  currentMap['name'] = 'resLabels'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('LMOL').get('abstractTypes')
  # End of MolLabel

  currentMap = abstractTypes.get('MolLabel')
  aList = ['_ID', 'ccpnInternalData', 'serial']
  currentMap['headerAttrs'] = aList
  aList = ['averageLabeledMixtures', 'molLabelFractions']
  currentMap['simpleAttrs'] = aList
  aList = ['resLabels', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['resLabels']
  currentMap['children'] = aList

  # Class MolLabelFraction
  currentMap = {}
  abstractTypes['MolLabelFraction'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00009'] = currentMap
  loadMaps['LMOL.MolLabelFraction'] = currentMap
  currentMap['tag'] = 'LMOL.MolLabelFraction'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00009'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'molLabelFractions'
  currentMap['objkey'] = 'molLabel'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.MolLabelFraction
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute MolLabelFraction._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute MolLabelFraction.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute MolLabelFraction.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute MolLabelFraction.weight
  currentMap = {}
  contentMap['weight'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00016'] = currentMap
  loadMaps['LMOL.MolLabelFraction.weight'] = currentMap
  currentMap['tag'] = 'LMOL.MolLabelFraction.weight'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00016'
  currentMap['name'] = 'weight'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 1.0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00009')

  # Role MolLabelFraction.molLabel
  currentMap = {}
  contentMap['molLabel'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00015'] = currentMap
  loadMaps['LMOL.MolLabelFraction.molLabel'] = currentMap
  currentMap['tag'] = 'LMOL.MolLabelFraction.molLabel'
  currentMap['type'] = 'link'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00015'
  currentMap['name'] = 'molLabel'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['copyOverride'] = True
  # End of MolLabelFraction

  currentMap = abstractTypes.get('MolLabelFraction')
  aList = ['_ID', 'ccpnInternalData', 'weight']
  currentMap['headerAttrs'] = aList
  aList = ['molLabel']
  currentMap['optLinks'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class ResLabel
  currentMap = {}
  abstractTypes['ResLabel'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00004'] = currentMap
  loadMaps['LMOL.ResLabel'] = currentMap
  currentMap['tag'] = 'LMOL.ResLabel'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00004'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'resLabels'
  currentMap['objkey'] = 'resId'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.ResLabel
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute ResLabel._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute ResLabel.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute ResLabel.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute ResLabel.resId
  currentMap = {}
  contentMap['resId'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:15_00005'] = currentMap
  loadMaps['LMOL.ResLabel.resId'] = currentMap
  currentMap['tag'] = 'LMOL.ResLabel.resId'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:15_00005'
  currentMap['name'] = 'resId'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00001')

  # Role ResLabel.atomLabels
  currentMap = {}
  contentMap['atomLabels'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:15_00001'] = currentMap
  loadMaps['LMOL.ResLabel.atomLabels'] = currentMap
  currentMap['tag'] = 'LMOL.ResLabel.atomLabels'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:15_00001'
  currentMap['name'] = 'atomLabels'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('LMOL').get('abstractTypes')

  # Role ResLabel.resLabelFractions
  currentMap = {}
  contentMap['resLabelFractions'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-26-13:01:04_00001'] = currentMap
  loadMaps['LMOL.ResLabel.resLabelFractions'] = currentMap
  currentMap['tag'] = 'LMOL.ResLabel.resLabelFractions'
  currentMap['type'] = 'child'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-26-13:01:04_00001'
  currentMap['name'] = 'resLabelFractions'
  currentMap['hicard'] = -1
  currentMap['locard'] = 0
  currentMap['eType'] = 'cplx'
  currentMap['content'] = globalMap.get('LMOL').get('abstractTypes')
  # End of ResLabel

  currentMap = abstractTypes.get('ResLabel')
  aList = ['_ID', 'ccpnInternalData', 'resId']
  currentMap['headerAttrs'] = aList
  aList = ['resLabelFractions', 'atomLabels', 'applicationData']
  currentMap['cplxAttrs'] = aList
  aList = ['atomLabels', 'resLabelFractions']
  currentMap['children'] = aList

  # Class ResLabelFraction
  currentMap = {}
  abstractTypes['ResLabelFraction'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-25-14:45:21_00001'] = currentMap
  loadMaps['LMOL.ResLabelFraction'] = currentMap
  currentMap['tag'] = 'LMOL.ResLabelFraction'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-25-14:45:21_00001'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'resLabelFractions'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.ResLabelFraction
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute ResLabelFraction._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute ResLabelFraction.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute ResLabelFraction.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute ResLabelFraction.isotopomerSerial
  currentMap = {}
  contentMap['isotopomerSerial'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-25-14:45:57_00007'] = currentMap
  loadMaps['LMOL.ResLabelFraction.isotopomerSerial'] = currentMap
  currentMap['tag'] = 'LMOL.ResLabelFraction.isotopomerSerial'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-25-14:45:57_00007'
  currentMap['name'] = 'isotopomerSerial'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00011')

  # Attribute ResLabelFraction.schemeName
  currentMap = {}
  contentMap['schemeName'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-25-14:45:57_00006'] = currentMap
  loadMaps['LMOL.ResLabelFraction.schemeName'] = currentMap
  currentMap['tag'] = 'LMOL.ResLabelFraction.schemeName'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-25-14:45:57_00006'
  currentMap['name'] = 'schemeName'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 'NaturalAbundance'
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute ResLabelFraction.weight
  currentMap = {}
  contentMap['weight'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2007-01-25-14:45:57_00008'] = currentMap
  loadMaps['LMOL.ResLabelFraction.weight'] = currentMap
  currentMap['tag'] = 'LMOL.ResLabelFraction.weight'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-25-14:45:57_00008'
  currentMap['name'] = 'weight'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['default'] = 1.0
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00009')
  # End of ResLabelFraction

  currentMap = abstractTypes.get('ResLabelFraction')
  aList = ['_ID', 'ccpnInternalData', 'isotopomerSerial', 'schemeName', 'weight']
  currentMap['headerAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class SingleAtomLabel
  currentMap = {}
  abstractTypes['SingleAtomLabel'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00006'] = currentMap
  loadMaps['LMOL.SingleAtomLabel'] = currentMap
  currentMap['tag'] = 'LMOL.SingleAtomLabel'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00006'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'atomLabels'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.SingleAtomLabel
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute SingleAtomLabel._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute SingleAtomLabel.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute SingleAtomLabel.atomName
  currentMap = {}
  contentMap['atomName'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00007'] = currentMap
  loadMaps['LMOL.SingleAtomLabel.atomName'] = currentMap
  currentMap['tag'] = 'LMOL.SingleAtomLabel.atomName'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00007'
  currentMap['name'] = 'atomName'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute SingleAtomLabel.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute SingleAtomLabel.massNumber
  contentMap['massNumber'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00005')

  # Attribute SingleAtomLabel.serial
  contentMap['serial'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00004')

  # Attribute SingleAtomLabel.weight
  contentMap['weight'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00006')
  # End of SingleAtomLabel

  currentMap = abstractTypes.get('SingleAtomLabel')
  aList = ['_ID', 'atomName', 'ccpnInternalData', 'massNumber', 'serial', 'weight']
  currentMap['headerAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Class UniformAtomLabel
  currentMap = {}
  abstractTypes['UniformAtomLabel'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00007'] = currentMap
  loadMaps['LMOL.UniformAtomLabel'] = currentMap
  currentMap['tag'] = 'LMOL.UniformAtomLabel'
  currentMap['type'] = 'class'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00007'
  currentMap['eType'] = 'cplx'
  currentMap['fromParent'] = 'atomLabels'
  currentMap['objkey'] = 'serial'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.UniformAtomLabel
  contentMap = {}
  currentMap['content'] = contentMap

  # Attribute UniformAtomLabel._ID
  contentMap['_ID'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2014-03-03-16:24:15_00001')

  # Attribute UniformAtomLabel.applicationData
  contentMap['applicationData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-09-14-18:48:27_00007')

  # Attribute UniformAtomLabel.ccpnInternalData
  contentMap['ccpnInternalData'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2016-06-28-10:49:27_00001')

  # Attribute UniformAtomLabel.elementName
  currentMap = {}
  contentMap['elementName'] = currentMap
  mapsByGuid['www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00008'] = currentMap
  loadMaps['LMOL.UniformAtomLabel.elementName'] = currentMap
  currentMap['tag'] = 'LMOL.UniformAtomLabel.elementName'
  currentMap['type'] = 'attr'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00008'
  currentMap['name'] = 'elementName'
  currentMap['hicard'] = 1
  currentMap['locard'] = 1
  currentMap['data'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037')

  # Attribute UniformAtomLabel.massNumber
  contentMap['massNumber'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00005')

  # Attribute UniformAtomLabel.serial
  contentMap['serial'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00004')

  # Attribute UniformAtomLabel.weight
  contentMap['weight'] = mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-10-24-11:30:57_00006')
  # End of UniformAtomLabel

  currentMap = abstractTypes.get('UniformAtomLabel')
  aList = ['_ID', 'ccpnInternalData', 'elementName', 'massNumber', 'serial', 'weight']
  currentMap['headerAttrs'] = aList
  aList = ['applicationData']
  currentMap['cplxAttrs'] = aList

  # Out-of-package link to LabeledMixture
  currentMap = {}
  exolinks['LabeledMixture'] = currentMap
  loadMaps['LMOL.exo-LabeledMixture'] = currentMap
  currentMap['tag'] = 'LMOL.exo-LabeledMixture'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00008'
  currentMap['name'] = 'LabeledMixture'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.LabeledMixture
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'))

  # Out-of-package link to LabeledMolecule
  currentMap = {}
  exolinks['LabeledMolecule'] = currentMap
  loadMaps['LMOL.exo-LabeledMolecule'] = currentMap
  currentMap['tag'] = 'LMOL.exo-LabeledMolecule'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00002'
  currentMap['name'] = 'LabeledMolecule'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.LabeledMolecule
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))

  # Out-of-package link to MolLabel
  currentMap = {}
  exolinks['MolLabel'] = currentMap
  loadMaps['LMOL.exo-MolLabel'] = currentMap
  currentMap['tag'] = 'LMOL.exo-MolLabel'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00003'
  currentMap['name'] = 'MolLabel'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.MolLabel
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to MolLabelFraction
  currentMap = {}
  exolinks['MolLabelFraction'] = currentMap
  loadMaps['LMOL.exo-MolLabelFraction'] = currentMap
  currentMap['tag'] = 'LMOL.exo-MolLabelFraction'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00009'
  currentMap['name'] = 'MolLabelFraction'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.MolLabelFraction
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00033'))
  aList.append(globalMap.get('LMOL').get('exolinks'))

  # Out-of-package link to ResLabel
  currentMap = {}
  exolinks['ResLabel'] = currentMap
  loadMaps['LMOL.exo-ResLabel'] = currentMap
  currentMap['tag'] = 'LMOL.exo-ResLabel'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00004'
  currentMap['name'] = 'ResLabel'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.ResLabel
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00001'))

  # Out-of-package link to ResLabelFraction
  currentMap = {}
  exolinks['ResLabelFraction'] = currentMap
  loadMaps['LMOL.exo-ResLabelFraction'] = currentMap
  currentMap['tag'] = 'LMOL.exo-ResLabelFraction'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2007-01-25-14:45:21_00001'
  currentMap['name'] = 'ResLabelFraction'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.ResLabelFraction
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00037'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00011'))

  # Out-of-package link to SingleAtomLabel
  currentMap = {}
  exolinks['SingleAtomLabel'] = currentMap
  loadMaps['LMOL.exo-SingleAtomLabel'] = currentMap
  currentMap['tag'] = 'LMOL.exo-SingleAtomLabel'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00006'
  currentMap['name'] = 'SingleAtomLabel'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.SingleAtomLabel
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))

  # Out-of-package link to UniformAtomLabel
  currentMap = {}
  exolinks['UniformAtomLabel'] = currentMap
  loadMaps['LMOL.exo-UniformAtomLabel'] = currentMap
  currentMap['tag'] = 'LMOL.exo-UniformAtomLabel'
  currentMap['type'] = 'exo'
  currentMap['guid'] = 'www.ccpn.ac.uk_Fogh_2006-10-24-11:28:55_00007'
  currentMap['name'] = 'UniformAtomLabel'
  currentMap['eType'] = 'cplx'
  currentMap['class'] = ccpnmodel.ccpncore.api.ccp.molecule.LabeledMolecule.UniformAtomLabel
  aList = list()
  currentMap['keyMaps'] = aList
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2008-06-30-16:30:50_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:54_00001'))
  aList.append(mapsByGuid.get('www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00032'))
