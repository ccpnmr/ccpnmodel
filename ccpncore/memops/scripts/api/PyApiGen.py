from ccpnmodel.ccpncore.memops.metamodel import MetaModel
from ccpnmodel.ccpncore.memops.metamodel import Constants as metaConstants
from ccpnmodel.ccpncore.memops.metamodel import Util as metaUtil

from ccpnmodel.ccpncore.memops.scripts.core.PyLanguage import PyLanguage
from ccpnmodel.ccpncore.memops.scripts.core.PyType import PyType

from ccpnmodel.ccpncore.memops.scripts.api.ApiGen import ApiGen

basicDataTypes = metaConstants.baseDataTypeModule

# This class implements as much of ApiInterface as is independent of implementation details
# Overrides some of ApiGen for overrides that are independent of implementation details
# Need to have PyLanguage and PyType before ApiGen to pick up correct LanguageInterface
# and TypeInterface functions
class PyApiGen(PyLanguage, PyType, ApiGen):

  ###########################################################################

  ###########################################################################

  def __init__(self):
               
    self.addModelFlavour('language', 'python')
    super(PyApiGen, self).__init__()

  ###########################################################################

  ###########################################################################
  ###
  ### code overriding ModelTraverse
  ###
  ###########################################################################
  
  # overrides ModelTraverse
  def initLeafPackage(self, package):
    """ write API header for package containing actual code
    """

    self.openObjFile(package)

    self.writeFileHeader(package)

  ###########################################################################

  ###########################################################################

  # overrides ModelTraverse
  def endLeafPackage(self, package):

    self.closeFile()

  ###########################################################################

  ###########################################################################

  # overrides ModelTraverse
  def endClass(self, clazz):
    
    for elem in clazz.getAllAttributes():
      self.writeProperty(elem, clazz)
      
    for elem in clazz.getAllRoles():
      self.writeProperty(elem, clazz)

    self.indent -= self.INDENT

#     self.write("""
# from ccpn.util.ApiFunc import _addModuleFunctionsToApiClass
# _addModuleFunctionsToApiClass('%s', %s)
# """ % (clazz.qualifiedName(), clazz.name))
    self.write("""
from ccpnmodel.ccpncore.lib.ApiPath import _addModuleFunctionsToApiClass
_addModuleFunctionsToApiClass('%s', %s)
""" % (clazz.qualifiedName(), clazz.name))
  
  ###########################################################################

  ###########################################################################
  
  # internal function
  def initComplexDataType(self, clazz):
  
    package = clazz.container
  
    # class declaration baseClass
    superclass = clazz.supertype
    if superclass is None:
      ss = 'object'
    else:
      ss = self.getImportName(superclass, package)

    self.writeNewline()
  
    if clazz in (self.baseClass, self.baseDataType):
      self.write("@functools.total_ordering")

    self.write("""###############################################################################
class %s(%s):
  r""\"%s
  ""\"
""" % (clazz.name, ss, metaUtil.breakString(clazz.documentation)))
  
    self.indent += self.INDENT
    
    # write source revision comment
    self.writeComment("  from data model element %s"
                      % (clazz.qualifiedName()))
    
    self.setVar(self.varNames['metaclass'], 
                self.callFunc('getElement', 'metaPackage', 
                              self.toLiteral(clazz.name), doWrite=False))
    self.setVar(self.varNames['packageName'], 
                self.toLiteral(package.qualifiedName()),
                varType=self.stringType)
    self.setVar(self.varNames['packageShortName'], 
                self.toLiteral(package.shortName),
                varType=self.stringType)

    if clazz is  self.dataRoot:
      self.write('''
# Variables for special upgrade hacks (V2 to V3). Set default values
_movedPackageNames = {}
_upgradedFromV2 = False''')

  
  ###########################################################################
  
  ###########################################################################

  # overrides ModelTraverse
  def initDataObjType(self, clazz):
    
    self.initComplexDataType(clazz)
    ll =  clazz.getAllAttributes()
    self.newCollection(self.varNames['fieldNames'], isUnique=False, 
                       isOrdered=True, varType=self.stringType, 
                       initValues=tuple(x.name for x in ll), isFrozen=True)
    
    if clazz is self.baseDataType:
      # special code for topmost actual class

      self.addComparisonsForDataObj()

      self.addToStringForDataObj()
  
  ###########################################################################
  
  ###########################################################################

  # overrides ModelTraverse
  def initClass(self, clazz):
  
    self.initComplexDataType(clazz)
    ll = clazz.getAllAttributes() + clazz.getAllRoles()
    self.newCollection(self.varNames['fieldNames'], isUnique=False, 
                       isOrdered=True, varType=self.stringType, 
                       initValues=tuple(x.name for x in ll), isFrozen=True)
    
    if clazz is self.baseClass:
      # special code for topmost actual class
      
      self.addToStringForClass(clazz)

      self.addComparisonsForClass(clazz)
  
    # Initialise notification machinery
    if not clazz.isAbstract:
      self.write("""
_notifies = {'':[]}
""")


  ###########################################################################

  ###########################################################################

  # overrides ModelTraverse
  def endDataObjType(self, clazz):
    
    for elem in clazz.getAllAttributes():
      self.writeProperty(elem, clazz)

    self.indent -= self.INDENT
    
  ###########################################################################

  ###########################################################################
 
  # overrides ModelTraverse
  def processDataType(self, dataType):
    """Write basic data type import
 
    Data Types whose name equals their type code are basic data types
    """
    
    ss = dataType.typeCodes['python']
    if ss == dataType.name and dataType.container.getElement(ss) is not None:
      self.write("from ccpnmodel.ccpncore.%s.baseDataTypes import %s\n"
       % (metaConstants.modellingPackageName, ss)
      )

  ###########################################################################

  ###########################################################################
  ###
  ### code implementing ApiInterface
  ###
  ###########################################################################

  ###########################################################################

  # implements ApiInterface
  def checkComparableInstance(self, inClass, var, element, inCollection=None):
    """Writes instance type checking code for attributes and links
    Also converts attributes from compatible data types
    """

    if isinstance(element.valueType, MetaModel.MetaDataType):

      dataType = element.valueType

      n = dataType.typeCodes['python']
      basicType = getattr(basicDataTypes, n)
 
      impPackageName = '%s.%s' % (metaConstants.modellingPackageName,
                                  metaConstants.implementationPackageName)
      impPackage = element.metaObjFromQualName(impPackageName)
       
      if inClass.container is impPackage:
        p = ''
      else:
        p = self.getImportName(impPackage) + '.'
 
      self.startIf('isinstance(%s, %s%s.PythonType)' % (var, p, n))
      self.write('pass')

      if basicType.compatibleTypes:
        self.elseIf('[x for x in %s%s.compatibleTypes if isinstance(%s, x)]' % (p, n, var))
        if inCollection is None:
          self.write('%s = %s%s.create(%s)' % (var, p, n, var))
        else:
          self.setVar('castValue','%s%s.create(%s)' % (p, n, var))
          self.replaceInCollection(var, 'castValue', inCollection, 
                                   **self.collectionParams(element))
          self.setVar(var, 'castValue')
 
      self.elseIf()
      self.raiseApiError('%s input is not of a valid type' 
                         % dataType.qualifiedName(), var)
      self.endIf()

    elif isinstance(element, MetaModel.ClassElement):

      # handle import statements, if needed
      otherClass = element.valueType
      if otherClass.container is inClass.container:
        typeName = otherClass.name
      else:
        ss = self.getImportName(otherClass.container, inClass.container)
        typeName = 'importedType'
        self.write("from %s import %s as %s\n"
         % (ss, otherClass.name, typeName)
        )
      self.startIf('not isinstance(%s, %s)' % (var, typeName))        
      self.raiseApiError('value is not of class %s' 
                         % otherClass.qualifiedName(), var)
      self.endIf()

  ###########################################################################

  ###########################################################################

  # implements ApiInterface
  def writeNotifyCode(self, notifyName):

    if notifyName == '__init__':

      self.write('''
ll = self.__class__._notifies.get('__init__')
if ll:
  for notify in ll:
    notify(self)''')

    elif notifyName == 'postInit':

      self.write('''
ll = self.__class__._notifies.get('postInit')
if ll:
  for notify in ll:
    notify(self)''')

    elif notifyName == 'preDelete':

      self.write('''
for obj in reversed(objsToBeDeleted):
  for notify in obj.__class__._notifies.get('preDelete', ()):
    notify(obj)
''')

    elif notifyName == 'startDeleteBlock':

      self.write('''
for notify in self.__class__._notifies.get('startDeleteBlock', ()):
  notify(self)
''')

    elif notifyName == 'endDeleteBlock':

      self.write('''
for notify in self.__class__._notifies.get('endDeleteBlock', ()):
  notify(self)
''')

    elif notifyName == 'delete':

      self.write('''
for obj in reversed(objsToBeDeleted):
  for notify in obj.__class__._notifies.get('delete', ()):
    notify(obj)
''')

    elif notifyName == '_unDelete':

      self.write('''
for obj in %s:
  for notify in obj.__class__._notifies.get('undelete', ()):
    notify(obj)
''' %  self.varNames['objsToBeUnDeleted'])

    else:

      self.write('''
_notifies = self.__class__._notifies

ll1 = _notifies['']
for notify in ll1:
  notify(self)

ll = _notifies.get('%s')
if ll:
  for notify in ll:
    if notify not in ll1:
      notify(self)''' % notifyName)
 
  ###########################################################################

  ###########################################################################

  # implements ApiInterface
  def writeUndoCode(self, op, inClass):

    notifyName = op.name
    opType = op.opType
    elem = op.target
    otherRole = hasattr(elem, 'otherRole') and elem.otherRole

    isMemopsRoot = self.dataRoot in inClass.getAllSupertypes()

    if (otherRole and elem.hicard != 1 and otherRole.hicard == 1 and otherRole.locard == 0
          and not (elem.isDerived or  elem.changeability == 'frozen' or
                   otherRole.isDerived or otherRole.changeability == 'frozen')
        ):
      iftext = 'notIsReading'
    else:
      iftext = self.shouldDoUndos(op, inClass)

    if iftext:
      self.writeNewline()
      self.startIf(iftext)

    self.writeComment("register Undo functions")

    self.write('''
_undo = root._undo
if _undo is not None:''')

    if opType == 'init':

      # NB This is NOT enough when additional objects are created through postConstructor code.
      if isMemopsRoot:
        self.write('''
  _undo.clear()''')
      else:
        self.write('''
  _undo.newItem(deleteAllApiObjects, root._unDelete, undoArgs=(objectsCreated,),
                redoArgs=(objectsCreated, set(x.topObject for x in objectsCreated)))
''')

    elif opType == 'fullDelete':

      if isMemopsRoot:
        self.write('''
  _undo.clear()''')
      else:
        self.write('''
  _undo.newItem(root._unDelete, self.delete, undoArgs=(objsToBeDeleted, topObjectsToCheck))
''')

    elif opType == 'set':

      var = self.valueVar(op.target, doInstance=False)
      currentVar = self.valueVar(op.target, prefix=self.currentPrefix)

      if (otherRole and elem.hicard != 1 and otherRole.hicard == 1 and otherRole.locard == 0
            and not (elem.isDerived or  elem.changeability == 'frozen' or
                     otherRole.isDerived or otherRole.changeability == 'frozen')
          ):
            # Write special undo code for N<->1 links to reset oldSelves links on undo
            self.write('''
  _undo.newItem(restoreOriginalLinks, self.%s, undoArgs=(undoValueDict, %s),  redoArgs=(%s,))
''' % (notifyName, repr(otherRole.name), var))

      else:
        self.write('''
  _undo.newItem(self.%s, self.%s,
                undoArgs=(%s,), redoArgs=(%s,))
''' % (notifyName, notifyName, currentVar, var))

    elif opType in ('add', 'remove'):

      var = self.valueVar(op.target, doInstance=True)
      undoColVar = self.valueVar(op.target, prefix='undo')
      setter =  metaUtil.getOperation(op.target, 'set', inClass=inClass)
      setterName = metaUtil.getFuncname(setter, inClass=inClass)

      if opType == 'add':


        if (otherRole and elem.hicard != 1 and otherRole.hicard == 1 and otherRole.locard == 0
              and not (elem.isDerived or  elem.changeability == 'frozen' or
                       otherRole.isDerived or otherRole.changeability == 'frozen')
            ):
              # Write special undo code for N<->1 links to reset oldSelves links on undo
          self.write('''
  _undo.newItem(restoreOriginalLinks, self.%s, undoArgs=(undoValueDict, %s),  redoArgs=(%s,))
''' % (notifyName, repr(otherRole.name), var))
        else:

          self.write('''
  _undo.newItem(self.%s, self.%s,
                undoArgs=(%s,), redoArgs=(%s,))
 ''' % (setterName, notifyName, undoColVar, var))

      else:

        self.write('''
  _undo.newItem(self.%s, self.%s,
                undoArgs=(%s,), redoArgs=(%s,))
 ''' % (setterName, notifyName, undoColVar, var))

    if iftext:
      self.endIf()

  ###########################################################################

  ###########################################################################

  # implements ApiInterface
  def setCheckLinkKey(self, keyVar, objVar, role):

    self.write("%s = (%s, '%s')" % (keyVar, objVar, role.name))

  ###########################################################################

  ###########################################################################

  # implements ApiInterface
  def checkFindFirst(self, op, inClass):
    
    role = op.target
    
    currentVar = self.valueVar(role, prefix=self.currentPrefix)
  
    self.getValue(self.varNames['self'], role, currentVar, 
                  convertCollection=False, inClass=inClass)
    
    self.checkFindBody(op, inClass, funcType='findFirst')

  ###########################################################################

  ###########################################################################

  # implements ApiInterface
  def checkFindAll(self, op, inClass):
    
    currentVar = self.valueVar(op.target, prefix=self.currentPrefix)
    
    self.getValue(self.varNames['self'], op.target, currentVar, 
                  convertCollection=False, inClass=inClass)
    
    self.checkFindBody(op, inClass, funcType='findAll')

  ###########################################################################

  ###########################################################################
  
  def checkFindBody(self, op, inClass, funcType='findFirst'):
    """ internal function. called only from checkFindFirst/All
    """
    
    target = op.target
    
    resultVar = self.varNames['result']
    currentVar = self.valueVar(op.target, prefix=self.currentPrefix)
    
    if funcType =='findAll':

      resultParams = self.collectionParams(target)
      self.newCollection(resultVar, **resultParams)
      
      if resultParams['isOrdered']:
        resultCode = "%s.append(v)" % resultVar
      else:
        resultCode = "%s.add(v)" % resultVar
      
    elif funcType == 'findFirst':
      resultCode = "%s = v; break" % resultVar
    
      self.setVar(resultVar, self.noneValue)
      
    else:
      raise metaConstants.MemopsError(
             "checkFindBody called with invalid funcType: %s" % funcType)
    
    self.write("""
items = list(%s.items())
""" %  self.varNames['conditions'])
    
    self.startIf(self.logicalOp(self.varNames['nConditions'], 
                                '==', self.toLiteral(1)))
    
    self.write("(key, condition) = items[0]")
    self.checkFindSingleCondition(op, currentVar, resultCode)
       
    self.elseIf()
    
    self.write("""
for ii in range(%(nc)s):
  (key, condition) = items[ii]
  if isinstance(condition, list):
    items[ii] = (key, tuple(condition))
  elif isinstance(condition, set):
    items[ii] = (key, frozenset(condition))

for v in %(cv)s:

  for (key, condition) in items:
    if getattr(v, key, ApiError) != condition:
      # NB ApiError is a dummy object, never equal to condition
      break
  else:
    %(rc)s
""" % { 'cv': currentVar, 'rc':resultCode, 'nc':self.varNames['nConditions']})

    self.endIf()

  ###########################################################################

  ###########################################################################

  # Auxiliary function - overridden in PyFileAPiGen. Optimisation
  def checkFindSingleCondition(self, op, currentVar, resultCode):
    """ Do check for case where there is only one conditions
    Separated out to allow an optimisation in PyFileApiGen
    """
    self.write("""
if isinstance(condition, list):
  condition = tuple(condition)
elif isinstance(condition, set):
  condition = frozenset(condition)

for v in %(cv)s:
  if getattr(v, key, ApiError) == condition:
    # NB ApiError is a dummy object, never equal to condition
    %(rc)s
""" % {'cv': currentVar, 'rc':resultCode})
    

  ###########################################################################

  ###########################################################################

  # implements ApiInterface
  def writeSortedValue(self, op, inClass):
    """ write sorted element getter
    """
    element = op.target
    
    self.getValue(self.varNames['self'], element, 'll', inClass=inClass)
    
    valueType = element.valueType
    parentRole = valueType.parentRole
    supertype = valueType.supertype
    if (valueType.keyNames and parentRole and
        (parentRole.container is valueType or
        (supertype and not supertype.keyNames))):
      self.write("ll = [(x.getFullKey(),x) for x in ll]")
    else:
      self.write("ll = [(repr(x),x) for x in ll]")
      
    self.write("""
ll.sort()
%s = [x[1] for x in ll]""" % self.varNames['result'])

  ###########################################################################

  ###########################################################################

  # implements ApiInterface
  def callConstructor(self, op, inClass, params):

    target = op.target

    return '%s(%s)' % (target.name, ', '.join(params))

  ###########################################################################

  ###########################################################################
  ###
  ### code overriding ApiGen
  ###
  ###########################################################################

  ###########################################################################

  # implements ApiGen
  def writeInheritedOperation(self, op, inClass):
    if op.scope == metaConstants.instance_level:
      # copying down staticmethods messes up Python
      name = self.getFuncname(op)
      self.writeNewline()
      self.write('%s = %s.%s' %
       (name,  self.getImportName(op.container, inClass.container), name)
      )

  ###########################################################################

  ###########################################################################

  # overrides ApiGen
  def writeInitClass(self, op, inClass):

    if inClass.isAbstract: # Abstract classes can not be initialised
      self.write("""
def __init__(self, *args, **kw):
  raise ApiError("cannot instantiate abstract class '%s'")
""" % inClass.qualifiedName())

    else:
      ApiGen.writeInitClass(self, op, inClass)

  ###########################################################################

  ###########################################################################

  # overrides ApiGen
  def writeStartFunc(self, op, inClass):

    opType = op.opType

    ApiGen.writeStartFunc(self, op, inClass)

    if opType == 'new':
      target = op.target
      # handle import statements, if needed
      if target.container is not inClass.container:
        path = self.getImportName(target, inClass.container).split('.')
        self.write('from %s import %s' % ('.'.join(path[:-1]), target.name))

  ###########################################################################

  ###########################################################################

  # overrides ApiGen
  def writeEndFunc(self, op, inClass):
    
    ApiGen.writeEndFunc(self, op, inClass)
    if op.scope != metaConstants.instance_level:
      ss = self.getFuncname(op)
      self.writeNewline()
      self.write("%s = staticmethod(%s)" % (ss, ss))

  ###########################################################################

  ###########################################################################

  # overrides ApiGen
  def writeGetAttr(self, op, complexDataType):

    self.write('return getattr(self, name)')

  ###########################################################################

  ###########################################################################

  # overrides ApiGen
  def writeSetAttr(self, op, complexDataType):

    self.write('setattr(self, name, value)')

  ###########################################################################

  ###########################################################################

  # overrides ApiGen
  def writeInitCollection(self, element, initValues = None):

    # does the same, except in one step instead of two
    self.setValue(self.varNames['self'], element, value=self.newCollection(
     None, initValues=initValues, **self.collectionParams(element))
    )

  ###########################################################################

  ###########################################################################

  # overrides ApiGen
  def initCheckInstanceConstraints(self, element, inElement):
    
    self.startBlock()
    
    if isinstance(element, MetaModel.MetaRole):
      if element is not inElement:
        self.write("(%s, %s) = (%s, %s)" % (
         self.varNames['me'], self.varNames['other'],
         self.varNames['value'], self.varNames['self'])
        )

  ###########################################################################

  ###########################################################################

  # overrides ApiGen
  def endCheckInstanceConstraints(self, element, inElement):
    
    if isinstance(element, MetaModel.MetaRole):
      if element is not inElement:
        self.write("(%s, %s) = (%s, %s)" % (
         self.varNames['value'], self.varNames['self'],
         self.varNames['me'], self.varNames['other'])
        )
    
    self.endBlock()

  ###########################################################################

  ###########################################################################
  ###
  ### internal functions
  ###
  ###########################################################################

  ###########################################################################

  #internal function
  def writeFileHeader(self, package):
    
    implPackage = package.metaObjFromQualName(self.implPackageName)
    
    self.writeMultilineComment(
     (self.getVersionString(metaobj=package) + 
     '\n' + 
     self.getCreditsString(metaobj=package, programType='API')),
     compress=False
    )
 
    self.write("""
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
 
from ccpnmodel.ccpncore.%s.ApiError import ApiError
""" % metaConstants.modellingPackageName)
 
    # handle package imports
    self.write("\n# imported packages:\n")
    for pp1 in package.importedPackages:
      self.write("import %s\n" % self.getImportName(pp1, None))
 
    # handle metaPackage
    if package is implPackage:
      self.write("""
from ccpnmodel.ccpncore.%s.metamodel import XmlModelIo
topPackage = XmlModelIo.readModel(checkValidity=False)
metaPackage = topPackage.metaObjFromQualName('%s')
""" % (metaConstants.modellingPackageName, self.implPackageName))
    
    else:
      self.write("""
metaPackage = %s.topPackage.metaObjFromQualName('%s')
  """ % (self.getImportName(implPackage), package.qualifiedName()))
  
  ###########################################################################

  ###########################################################################

  # internal function 
  def writeProperty(self, element, inClass):

    if element.container is inClass:
    
      getter = self.getFuncname(metaUtil.getOperation(element, 'get', inClass))
      
      if element.isImplementation:
        setter = 'None'
      elif element.isDerived and element.changeability == metaConstants.frozen:
        setter = 'None'
      elif (isinstance(element,MetaModel.MetaRole)
       and element.hierarchy != metaConstants.no_hierarchy
      ):
        setter =' None'
      else:
        setter = self.getFuncname(metaUtil.getOperation(element, 'set', inClass))
  
      self.write("""
%s = property(%s, %s, None,
r""\"%s
""\")
""" % (element.name, getter, setter, metaUtil.breakString(element.documentation)))
    
    else:
      name = element.name
      self.writeNewline()
      self.write('%s = %s.%s' 
       % (name, self.getImportName(element.container, inClass.container), name)
      )
  
  ###########################################################################

  ###########################################################################

  # internal function 
  def getDataObjIdTuple(self, tag):
    
    raise metaConstants.MemopsError("getDataObjIdTuple not Implemented")

  ###########################################################################

  ###########################################################################
