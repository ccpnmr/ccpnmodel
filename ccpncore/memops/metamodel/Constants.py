"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2017"
__credits__ = ("Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for licence text")
__reference__ = ("For publications, please use reference from http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-07-07 16:33:21 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b5 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
import string
import types

# Python 2.1 dual-use constants
try:
  IntType = types.IntType
  StringType = types.StringType
  TupleType = types.TupleType
except AttributeError:
  IntType = int
  StringType = str
  TupleType = tuple

# General constants

class DummyClass:
  pass
sentinel = DummyClass()


# Errors - must be here to avoid circular import problem from Util/MetaModel
class MemopsError(Exception):
  """ Base class for all Memops Errors
  """
  # TODO reorganise error system
  pass


trueString = 'True'
falseString = 'False'

# Special constants
infinity = -1



# Directory names for Python code api subdirectories
apiCodeDir = 'api'

# Directory names for Python code xml subdirectories
xmlCodeDir = 'xml'

# documentation directories
imageDir = 'doc/graphics'
docDir = 'apidoc'

configFilePath = 'config/ccpnConfig.json'


# names of basic data types
int_code = 'Int'
float_code = 'Float'
ieee_float_code = 'IeeeFloat'
string_code = 'String'
boolean_code = 'Boolean'
datetime_code = 'DateTime'
dict_code = 'Dict'
multiple_code = 'Multiple'
typeCode_enumeration = [int_code, float_code, ieee_float_code,
 string_code, boolean_code, datetime_code, dict_code, multiple_code,
]
typeCode_enumeration.sort()

# NB it might be better to avoid this as it puts (can cause circular imports with 'Multiple' data type)
baseDataTypeModule = __import__(
 'ccpnmodel.ccpncore.memops.baseDataTypes', globals(), locals(), typeCode_enumeration
)

# NBNB TBD the codes for 'Dict and List are short-term hacks

# names of jdbc data types.
# jdbcTypeCode_enumeration = [
#  'CLOB', 'VARCHAR', 'BIT', 'INTEGER', 'BIGINT', 'FLOAT', 'DOUBLE', 'TIMESTAMP',
#  'Dict','List'
# ]
# jdbcTypeCode_enumeration.sort()

# names of java data types.
javaTypeCode_enumeration = ['java.lang.Integer',
'java.lang.Float','java.lang.String','java.lang.Boolean',
'java.util.Map', 'java.util.Collection'
]
javaTypeCode_enumeration.sort()

# names of java simple data types.
# NB the simpleType for strings is the empty string
javaSimpleTypeCode_enumeration = [
# TBD: is excluding None (which is not allowed in Python 3 because of sort()) a problem?
# 'int','long','float','double','boolean', None
 'int,''float','boolean'
]
javaSimpleTypeCode_enumeration.sort()

# names of xml data types.
xmlTypeCode_enumeration = ['string', 'boolean', 'int', 'float', 'Dict','List']
xmlTypeCode_enumeration.sort()

# dictionary of all typeCodes and their enumeration, to simplify processing
typeCodes = {
 'typeCode':typeCode_enumeration,
 # 'jdbcTypeCode':jdbcTypeCode_enumeration,
 # 'javaTypeCode':javaTypeCode_enumeration,
 # 'javaSimpleTypeCode':javaSimpleTypeCode_enumeration,
 'xmlTypeCode':xmlTypeCode_enumeration
}


# MetaModel constants

# visibility enumeration
public_visibility = 'public_vis'
protected_visibility = 'protected_vis'
private_visibility = 'private_vis'
visibility_enumeration = ( public_visibility, protected_visibility,
 private_visibility
)

# scope enumeration
instance_level = 'instance_level'
classifier_level = 'classifier_level'
scope_enumeration = (instance_level, classifier_level)

# aggregation enumeration
no_aggregation = None
composite_aggregation = 'composite'
aggregation_enumeration = ( no_aggregation, composite_aggregation )

# direction enumeration
in_direction = 'in_dir'
out_direction = 'out_dir'
inout_direction = 'inout_dir'
return_direction = 'return_dir'
direction_enumeration = ( in_direction, out_direction, inout_direction, 
 return_direction
)

# changeability enumeration
changeable = 'changeable'
frozen = 'frozen'
add_only = 'add_only'
changeability_enumeration = (changeable, frozen, add_only)

# role hierarchy enumeration
parent_hierarchy = 'parent'
child_hierarchy = 'child'
no_hierarchy = None
hierarchy_enumeration = ( parent_hierarchy, child_hierarchy, no_hierarchy )


# valid characters for names. 
# NB avoiding string.ascii_xxx attributes 
#    as we need 2.1 compatibility for ObjectDomain
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
underscore = "_"
validNameChars = uppercase + lowercase + string.digits + underscore

# Putting this in a single string is incompatible with Emacs python mode 
# (wish they would fix it)
xmlDisallowedChars = "&'<>" + '"'


# tags for 'code' dictionaries, 
# with code for different languages/implementations
codeStubTags = ('python', 'java', 'xml')

# maximum length of various names.
maxTagLength = 32
maxClassNameLength = 32
maxShortNameLength = 4

# names of attributes with special treatment:
id_attribute = '_ID'
lastid_attribute = '_lastId'
serial_attribute = 'serial'
serialdict_attribute = 'serialDict'
details_attribute = 'details'
timestamp_attribute = 'timestamp'
guid_attribute = 'guid'
           
# Implementation directory, file, and class names:
rootPackageDirName = 'RootPackage'
modellingPackageName = 'memops'
implementationPackageName = 'Implementation'
rootPackageName = 'Root'

dataRootName = 'MemopsRoot'
baseClassName = 'MemopsObject'
rootClassName = 'ComplexDataType'
topObjClassName = 'TopObject'
dataObjClassName = 'DataObject'
implObjClassName = 'ImplementationObject'
baseDataTypeObjName = 'MemopsDataTypeObject'

repositoryRole = 'repositories'
packageLocatorRole = 'packageLocators'

implementationClassNames = [dataRootName, baseClassName, topObjClassName,
                            dataObjClassName, implObjClassName,]

