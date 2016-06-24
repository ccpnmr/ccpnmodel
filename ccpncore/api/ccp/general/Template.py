"""
#######################################################################

CCPN Data Model version 3.0.2

Autogenerated by PyFileApiGen on Thu Jun 23 05:37:50 2016
  from data model element ccp.general.Template

#######################################################################
======================COPYRIGHT/LICENSE START==========================

Template.py: python API for CCPN data model, MetaPackage ccp.general.Template

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

#import sets
import traceback
import types
import operator
import functools
import collections

# special function for fast whitespace checking.
# used in DataType Word and Token handcode
import re
containsWhitespace = re.compile('\s').search
containsNonAlphanumeric = re.compile('[^a-zA-Z0-9_]').search

# Global NaN constant
NaN = float('NaN')

from ccpn.util.Undo import deleteAllApiObjects, restoreOriginalLinks, no_op
 
from ccpnmodel.ccpncore.memops.ApiError import ApiError

# imported packages:
import ccpnmodel.ccpncore.api.memops.Implementation

metaPackage = ccpnmodel.ccpncore.api.memops.Implementation.topPackage.metaObjFromQualName('ccp.general.Template')

###############################################################################
class AbstractProbability(ccpnmodel.ccpncore.api.memops.Implementation.DataObject):
  r"""Abstract class defining classes used for probability lists. 
AbstractProbability objects have a parent that is the object that has 
the probability (e.g. a ResonanceGroup), a link 'possibility' to various 
possibilities (e.g. a ChemComp), and a weight to determine their 
relative probability. Probabilities are calculated by taking the weight 
of each AbstractProbability object and dividing by the sum of the 
weights in the (appropriate subset of) AbstractProbability objects 
linked to a given parent. 

Implementation note: The presence of the 
'possibility' link must be enforced by the data modeller, as it is not 
checked by the software. 
  """
  #   from data model element ccp.general.Template.AbstractProbability
  _metaclass = metaPackage.getElement('AbstractProbability')
  _packageName = 'ccp.general.Template'
  _packageShortName = 'TEMP'
  _fieldNames = ('_ID', 'applicationData', 'className', 'fieldNames', 'inConstructor', 'isDeleted', 'metaclass', 'packageName', 'packageShortName', 'qualifiedName', 'weight', 'root', 'topObject',)

  __init__ = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.__init__

  addApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.addApplicationData

  checkAllValid = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.checkAllValid

  checkValid = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.checkValid

  delete = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.delete

  findAllApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.findAllApplicationData

  findFirstApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.findFirstApplicationData

  getApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.getApplicationData

  getByNavigation = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.getByNavigation

  getClassName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getClassName

  getExpandedKey = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.getExpandedKey

  getFieldNames = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getFieldNames

  getInConstructor = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getInConstructor

  getIsDeleted = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.getIsDeleted

  getMetaclass = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getMetaclass

  getPackageName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getPackageName

  getPackageShortName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getPackageShortName

  getQualifiedName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getQualifiedName

  getRoot = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.getRoot

  getTopObject = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.getTopObject
  
  def getWeight(self):
    """
    Get for ccp.general.Template.AbstractProbability.weight
    """
    dataDict = self.__dict__
    result = dataDict.get('weight')
    return result

  get_ID = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.get_ID

  removeApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.removeApplicationData

  setApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.setApplicationData
  
  def setWeight(self, value):
    """
    Set for ccp.general.Template.AbstractProbability.weight
    """
    dataDict = self.__dict__
    if (isinstance(value, ccpnmodel.ccpncore.api.memops.Implementation.Float.PythonType)):
      pass
    elif ([x for x in ccpnmodel.ccpncore.api.memops.Implementation.Float.compatibleTypes if isinstance(value, x)]):
      value = ccpnmodel.ccpncore.api.memops.Implementation.Float.create(value)
    else:
      raise ApiError("""%s.setWeight:
       memops.Implementation.Float input is not of a valid type""" % self.qualifiedName
       + ": %s" % (value,)
      )

    if (not (value - value == 0.0)):
      raise ApiError("""%s.setWeight:
       Float constraint value_is_not_NaN_or_Infinity violated by value""" % self.qualifiedName
       + ": %s" % (value,)
      )

    topObject = dataDict.get('topObject')
    currentValue = dataDict.get('weight')
    notInConstructor = not (dataDict.get('inConstructor'))

    root = dataDict.get('topObject').__dict__.get('memopsRoot')
    notOverride = not (root.__dict__.get('override'))
    notIsReading = not (topObject.__dict__.get('isReading'))
    notOverride = (notOverride and notIsReading)
    if (notIsReading):
      if (notInConstructor):
        if (not (topObject.__dict__.get('isModifiable'))):
          raise ApiError("""%s.setWeight:
           Storage not modifiable""" % self.qualifiedName
           + ": %s" % (topObject,)
          )

    if (dataDict.get('isDeleted')):
      raise ApiError("""%s.setWeight:
       called on deleted object""" % self.qualifiedName
      )

    try:
      if (value == currentValue):
        return

    except ValueError as ex:
      pass
    if (notOverride):
      if (value is None):
        raise ApiError("""%s.setWeight:
         value cannot be None""" % self.qualifiedName
         + ": %s" % (self,)
        )

      pass

    dataDict['weight'] = value
    if (notIsReading):
      if (notInConstructor):
        topObject.__dict__['isModified'] = True

    # doNotifies

    if ((notInConstructor and notOverride)):
      
      _notifies = self.__class__._notifies
      
      ll1 = _notifies['']
      for notify in ll1:
        notify(self)
      
      ll = _notifies.get('setWeight')
      if ll:
        for notify in ll:
          if notify not in ll1:
            notify(self)

    if ((notInConstructor and notIsReading)):
      # register Undo functions
      
      _undo = root._undo
      if _undo is not None:
      
        _undo.newItem(self.setWeight, self.setWeight,
                      undoArgs=(currentValue,), redoArgs=(value,))

  set_ID = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.set_ID

  toDetailedString = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.toDetailedString

  _ID = ccpnmodel.ccpncore.api.memops.Implementation.DataObject._ID

  applicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.applicationData

  className = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.className

  fieldNames = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.fieldNames

  inConstructor = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.inConstructor

  isDeleted = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.isDeleted

  metaclass = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.metaclass

  packageName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.packageName

  packageShortName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.packageShortName

  qualifiedName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.qualifiedName
  
  weight = property(getWeight, setWeight, None,
  r"""weight (= non-normalised probability) that the parent is associated with 
  this particular possibility. 
  """)

  root = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.root

  topObject = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.topObject

from ccpnmodel.ccpncore.lib.ApiPath import _addModuleFunctionsToApiClass
_addModuleFunctionsToApiClass('ccp.general.Template.AbstractProbability', AbstractProbability)

###############################################################################
class MultiTypeValue(ccpnmodel.ccpncore.api.memops.Implementation.DataObject):
  r"""Typed value data
  """
  #   from data model element ccp.general.Template.MultiTypeValue
  _metaclass = metaPackage.getElement('MultiTypeValue')
  _packageName = 'ccp.general.Template'
  _packageShortName = 'TEMP'
  _fieldNames = ('_ID', 'applicationData', 'booleanValue', 'className', 'fieldNames', 'floatValue', 'inConstructor', 'intValue', 'isDeleted', 'metaclass', 'packageName', 'packageShortName', 'qualifiedName', 'textValue', 'root', 'topObject',)

  __init__ = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.__init__

  addApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.addApplicationData

  checkAllValid = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.checkAllValid

  checkValid = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.checkValid

  delete = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.delete

  findAllApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.findAllApplicationData

  findFirstApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.findFirstApplicationData

  getApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.getApplicationData
  
  def getBooleanValue(self):
    """
    Get for ccp.general.Template.MultiTypeValue.booleanValue
    """
    dataDict = self.__dict__
    result = dataDict.get('booleanValue')
    return result

  getByNavigation = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.getByNavigation

  getClassName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getClassName

  getExpandedKey = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.getExpandedKey

  getFieldNames = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getFieldNames
  
  def getFloatValue(self):
    """
    Get for ccp.general.Template.MultiTypeValue.floatValue
    """
    dataDict = self.__dict__
    result = dataDict.get('floatValue')
    return result

  getInConstructor = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getInConstructor
  
  def getIntValue(self):
    """
    Get for ccp.general.Template.MultiTypeValue.intValue
    """
    dataDict = self.__dict__
    result = dataDict.get('intValue')
    return result

  getIsDeleted = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.getIsDeleted

  getMetaclass = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getMetaclass

  getPackageName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getPackageName

  getPackageShortName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getPackageShortName

  getQualifiedName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.getQualifiedName

  getRoot = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.getRoot
  
  def getTextValue(self):
    """
    Get for ccp.general.Template.MultiTypeValue.textValue
    """
    dataDict = self.__dict__
    result = dataDict.get('textValue')
    return result

  getTopObject = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.getTopObject

  get_ID = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.get_ID

  removeApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.removeApplicationData

  setApplicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.setApplicationData
  
  def setBooleanValue(self, value):
    """
    Set for ccp.general.Template.MultiTypeValue.booleanValue
    """
    dataDict = self.__dict__
    if (value is not None):
      if (not (value in [True, False])):
        raise ApiError("""%s.setBooleanValue:
         memops.Implementation.Boolean input is not in enumeration [True, False]""" % self.qualifiedName
         + ": %s" % (value,)
        )

    topObject = dataDict.get('topObject')
    currentValue = dataDict.get('booleanValue')
    notInConstructor = not (dataDict.get('inConstructor'))

    root = dataDict.get('topObject').__dict__.get('memopsRoot')
    notOverride = not (root.__dict__.get('override'))
    notIsReading = not (topObject.__dict__.get('isReading'))
    notOverride = (notOverride and notIsReading)
    if (notIsReading):
      if (notInConstructor):
        if (not (topObject.__dict__.get('isModifiable'))):
          raise ApiError("""%s.setBooleanValue:
           Storage not modifiable""" % self.qualifiedName
           + ": %s" % (topObject,)
          )

    if (dataDict.get('isDeleted')):
      raise ApiError("""%s.setBooleanValue:
       called on deleted object""" % self.qualifiedName
      )

    try:
      if (value == currentValue):
        return

    except ValueError as ex:
      pass
    if (notOverride):
      pass

    dataDict['booleanValue'] = value
    if (notIsReading):
      if (notInConstructor):
        topObject.__dict__['isModified'] = True

    # doNotifies

    if ((notInConstructor and notOverride)):
      
      _notifies = self.__class__._notifies
      
      ll1 = _notifies['']
      for notify in ll1:
        notify(self)
      
      ll = _notifies.get('setBooleanValue')
      if ll:
        for notify in ll:
          if notify not in ll1:
            notify(self)

    if ((notInConstructor and notIsReading)):
      # register Undo functions
      
      _undo = root._undo
      if _undo is not None:
      
        _undo.newItem(self.setBooleanValue, self.setBooleanValue,
                      undoArgs=(currentValue,), redoArgs=(value,))

  def setFloatValue(self, value):
    """
    Set for ccp.general.Template.MultiTypeValue.floatValue
    """
    dataDict = self.__dict__
    if (value is not None):
      if (isinstance(value, ccpnmodel.ccpncore.api.memops.Implementation.Float.PythonType)):
        pass
      elif ([x for x in ccpnmodel.ccpncore.api.memops.Implementation.Float.compatibleTypes if isinstance(value, x)]):
        value = ccpnmodel.ccpncore.api.memops.Implementation.Float.create(value)
      else:
        raise ApiError("""%s.setFloatValue:
         memops.Implementation.Float input is not of a valid type""" % self.qualifiedName
         + ": %s" % (value,)
        )

      if (not (value - value == 0.0)):
        raise ApiError("""%s.setFloatValue:
         Float constraint value_is_not_NaN_or_Infinity violated by value""" % self.qualifiedName
         + ": %s" % (value,)
        )

    topObject = dataDict.get('topObject')
    currentValue = dataDict.get('floatValue')
    notInConstructor = not (dataDict.get('inConstructor'))

    root = dataDict.get('topObject').__dict__.get('memopsRoot')
    notOverride = not (root.__dict__.get('override'))
    notIsReading = not (topObject.__dict__.get('isReading'))
    notOverride = (notOverride and notIsReading)
    if (notIsReading):
      if (notInConstructor):
        if (not (topObject.__dict__.get('isModifiable'))):
          raise ApiError("""%s.setFloatValue:
           Storage not modifiable""" % self.qualifiedName
           + ": %s" % (topObject,)
          )

    if (dataDict.get('isDeleted')):
      raise ApiError("""%s.setFloatValue:
       called on deleted object""" % self.qualifiedName
      )

    try:
      if (value == currentValue):
        return

    except ValueError as ex:
      pass
    if (notOverride):
      pass

    dataDict['floatValue'] = value
    if (notIsReading):
      if (notInConstructor):
        topObject.__dict__['isModified'] = True

    # doNotifies

    if ((notInConstructor and notOverride)):
      
      _notifies = self.__class__._notifies
      
      ll1 = _notifies['']
      for notify in ll1:
        notify(self)
      
      ll = _notifies.get('setFloatValue')
      if ll:
        for notify in ll:
          if notify not in ll1:
            notify(self)

    if ((notInConstructor and notIsReading)):
      # register Undo functions
      
      _undo = root._undo
      if _undo is not None:
      
        _undo.newItem(self.setFloatValue, self.setFloatValue,
                      undoArgs=(currentValue,), redoArgs=(value,))

  def setIntValue(self, value):
    """
    Set for ccp.general.Template.MultiTypeValue.intValue
    """
    dataDict = self.__dict__
    if (value is not None):
      if (isinstance(value, ccpnmodel.ccpncore.api.memops.Implementation.Int.PythonType)):
        pass
      else:
        raise ApiError("""%s.setIntValue:
         memops.Implementation.Int input is not of a valid type""" % self.qualifiedName
         + ": %s" % (value,)
        )

    topObject = dataDict.get('topObject')
    currentValue = dataDict.get('intValue')
    notInConstructor = not (dataDict.get('inConstructor'))

    root = dataDict.get('topObject').__dict__.get('memopsRoot')
    notOverride = not (root.__dict__.get('override'))
    notIsReading = not (topObject.__dict__.get('isReading'))
    notOverride = (notOverride and notIsReading)
    if (notIsReading):
      if (notInConstructor):
        if (not (topObject.__dict__.get('isModifiable'))):
          raise ApiError("""%s.setIntValue:
           Storage not modifiable""" % self.qualifiedName
           + ": %s" % (topObject,)
          )

    if (dataDict.get('isDeleted')):
      raise ApiError("""%s.setIntValue:
       called on deleted object""" % self.qualifiedName
      )

    try:
      if (value == currentValue):
        return

    except ValueError as ex:
      pass
    if (notOverride):
      pass

    dataDict['intValue'] = value
    if (notIsReading):
      if (notInConstructor):
        topObject.__dict__['isModified'] = True

    # doNotifies

    if ((notInConstructor and notOverride)):
      
      _notifies = self.__class__._notifies
      
      ll1 = _notifies['']
      for notify in ll1:
        notify(self)
      
      ll = _notifies.get('setIntValue')
      if ll:
        for notify in ll:
          if notify not in ll1:
            notify(self)

    if ((notInConstructor and notIsReading)):
      # register Undo functions
      
      _undo = root._undo
      if _undo is not None:
      
        _undo.newItem(self.setIntValue, self.setIntValue,
                      undoArgs=(currentValue,), redoArgs=(value,))

  def setTextValue(self, value):
    """
    Set for ccp.general.Template.MultiTypeValue.textValue
    """
    dataDict = self.__dict__
    if (value is not None):
      if (isinstance(value, ccpnmodel.ccpncore.api.memops.Implementation.String.PythonType)):
        pass
      else:
        raise ApiError("""%s.setTextValue:
         memops.Implementation.String input is not of a valid type""" % self.qualifiedName
         + ": %s" % (value,)
        )

    topObject = dataDict.get('topObject')
    currentValue = dataDict.get('textValue')
    notInConstructor = not (dataDict.get('inConstructor'))

    root = dataDict.get('topObject').__dict__.get('memopsRoot')
    notOverride = not (root.__dict__.get('override'))
    notIsReading = not (topObject.__dict__.get('isReading'))
    notOverride = (notOverride and notIsReading)
    if (notIsReading):
      if (notInConstructor):
        if (not (topObject.__dict__.get('isModifiable'))):
          raise ApiError("""%s.setTextValue:
           Storage not modifiable""" % self.qualifiedName
           + ": %s" % (topObject,)
          )

    if (dataDict.get('isDeleted')):
      raise ApiError("""%s.setTextValue:
       called on deleted object""" % self.qualifiedName
      )

    try:
      if (value == currentValue):
        return

    except ValueError as ex:
      pass
    if (notOverride):
      pass

    dataDict['textValue'] = value
    if (notIsReading):
      if (notInConstructor):
        topObject.__dict__['isModified'] = True

    # doNotifies

    if ((notInConstructor and notOverride)):
      
      _notifies = self.__class__._notifies
      
      ll1 = _notifies['']
      for notify in ll1:
        notify(self)
      
      ll = _notifies.get('setTextValue')
      if ll:
        for notify in ll:
          if notify not in ll1:
            notify(self)

    if ((notInConstructor and notIsReading)):
      # register Undo functions
      
      _undo = root._undo
      if _undo is not None:
      
        _undo.newItem(self.setTextValue, self.setTextValue,
                      undoArgs=(currentValue,), redoArgs=(value,))

  set_ID = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.set_ID

  toDetailedString = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.toDetailedString

  _ID = ccpnmodel.ccpncore.api.memops.Implementation.DataObject._ID

  applicationData = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.applicationData
  
  booleanValue = property(getBooleanValue, setBooleanValue, None,
  r"""Boolean type value
  """)

  className = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.className

  fieldNames = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.fieldNames
  
  floatValue = property(getFloatValue, setFloatValue, None,
  r"""Float type value
  """)

  inConstructor = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.inConstructor
  
  intValue = property(getIntValue, setIntValue, None,
  r"""Integer type value
  """)

  isDeleted = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.isDeleted

  metaclass = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.metaclass

  packageName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.packageName

  packageShortName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.packageShortName

  qualifiedName = ccpnmodel.ccpncore.api.memops.Implementation.ComplexDataType.qualifiedName
  
  textValue = property(getTextValue, setTextValue, None,
  r"""Text type value
  """)

  root = ccpnmodel.ccpncore.api.memops.Implementation.MemopsObject.root

  topObject = ccpnmodel.ccpncore.api.memops.Implementation.DataObject.topObject

from ccpnmodel.ccpncore.lib.ApiPath import _addModuleFunctionsToApiClass
_addModuleFunctionsToApiClass('ccp.general.Template.MultiTypeValue', MultiTypeValue)
