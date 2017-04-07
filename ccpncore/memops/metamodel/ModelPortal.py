"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2017"
__credits__ = ("Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan"
               "Simon P Skinner & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license"
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for licence text")
__reference__ = ("For publications, please use reference from http://www.ccpn.ac.uk/v3-software/downloads/license"
               "or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:43 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
""" Access to In-memory model. Independent of language and storage. 
All functions (except for __init__) are queries on the model
"""

from ccpnmodel.ccpncore.memops.metamodel import MetaModel
from ccpnmodel.ccpncore.memops.metamodel import Constants as metaConstants
from ccpnmodel.ccpncore.memops.metamodel import Util as metaUtil
from ccpnmodel.ccpncore.memops.Version import currentModelVersion
MemopsError = MetaModel.MemopsError

######################################################################
# hack for Python 2.1 compatibility  NBNB                            #
######################################################################
try:
  junk = True
  junk = False
except NameError:
  dd = globals()
  dd['True'] = not 0
  dd['False'] = not True
  del dd

class ModelPortal:
  """ Access to In-memory model. Independent of language and storage. 
  All functions (except for __init__) are queries on the model
  """
  
  def __init__(self, topPackage, dataModelVersion=None):
    """ set up data, precalculated for later function calls.
    """
    
    # set data model version
    if dataModelVersion is None:
      self.dataModelVersion = currentModelVersion
    else:
      self.dataModelVersion = dataModelVersion
    
    # check topPackage
    if  (isinstance(topPackage, MetaModel.MetaPackage) 
            and topPackage is topPackage.topPackage()
    ):
      self.topPackage = topPackage
    else:
      raise MetaModel.MemopsError(
       "ModelPortal initialised with %s, must be top package"
       % topPackage.qualifiedName()
      )
    
    # package selection
    leafPackages = []
    branchPackages = []
    packages = [topPackage]
    
    # take all packages
    for pp in packages:
      childPackages = pp.containedPackages
      if childPackages:
        branchPackages.append(pp)
        packages.extend(childPackages)
      else:
        leafPackages.append(pp)
    
    # sort and finalize branchPackages
    self._branchPackages = metaUtil.sortByMethodCall(branchPackages,
                                                    'qualifiedName')
    del branchPackages
    
    # sort leafPackages by import (imported before importing)
    self._leafPackages = metaUtil.topologicalSortSubgraph(leafPackages, 
                                                          'accessedPackages')
    del leafPackages
    
    self.resetObjectDicts()
  
    # add modelFlavours dictionary
    topPackage._modelFlavours = {}
  
  def resetObjectDicts(self):
  
    # get classes and dataTypes for leafPackages and store sorted by inheritance
    _classesDict = self._classesDict = {}
    _dataTypesDict = self._dataTypesDict = {}
    _dataObjTypesDict = self._dataObjTypesDict = {}
    _exceptionsDict = self._exceptionsDict = {}
    
    for pp in self._leafPackages:
      _dataTypesDict[pp] = metaUtil.sortByInheritance(pp.dataTypes)
      _dataObjTypesDict[pp] = metaUtil.sortByDataObjTypeDependency(
                              pp.dataObjTypes)
      _classesDict[pp] = metaUtil.sortByInheritance(pp.classes)
      _exceptionsDict[pp] = metaUtil.sortByInheritance(pp.exceptions)
  
  
  ###########################################################################

  ###########################################################################
  
  def branchPackages(self):
    """ branch packages, alphabetically sorted by name
    """
    return list(self._branchPackages)
  
  branchPackagesAlphabetic = branchPackages
  
  ###########################################################################

  ###########################################################################
  
  def twigPackages(self):
    """ branch packages directly containing leafPackages, alphabetically sorted by name
    """
    
    dd = {}
    for pp in self._leafPackages:
      dd[pp.container] = None
    
    result = metaUtil.sortByMethodCall(dd.keys(),'qualifiedName')
    #
    return result
  
  twigPackagesAlphabetic = twigPackages
  
  ###########################################################################

  ###########################################################################
  
  def leafPackagesByImport(self):
    """ leaf packages sorted by import (imported before importing)
    """
    return list(self._leafPackages)
  
  ###########################################################################

  ###########################################################################
  
  def leafPackagesAlphabetic(self):
    """ leaf packages sorted alphabetically
    """
    return metaUtil.sortByMethodCall(self._leafPackages,'qualifiedName')
  
  ###########################################################################

  ###########################################################################
  
  def dataTypesByInheritance(self, package):
    """ data types sorted by inheritance (supertype before subtype)
    """
    ll = self._dataTypesDict.get(package)
    if ll is not None:
      return list(ll)
  
  ###########################################################################

  ###########################################################################
  
  def dataObjTypesByInheritance(self, package):
    """ data types sorted by inheritance (supertype before subtype)
    """
    ll = self._dataObjTypesDict.get(package)
    if ll is not None:
      return list(ll)
  
  ###########################################################################

  ###########################################################################
  
  def classesByInheritance(self, package):
    """ classes sorted by inheritance (supertype before subtype)
    """
    ll = self._classesDict.get(package)
    if ll is not None:
      return list(ll)
  
  ###########################################################################

  ###########################################################################
  
  def exceptionsByInheritance(self, package):
    """ exceptions sorted by inheritance (supertype before subtype)
    """
    ll = self._exceptionsDict.get(package)
    if ll is not None:
      return list(ll)
  
  ###########################################################################

  ###########################################################################
  
  def dataTypesAlphabetic(self, package):
    """ data types sorted alphabetically by name
    """
    return metaUtil.sortByAttribute(package.dataTypes,'name')
  
  ###########################################################################

  ###########################################################################
  
  def dataObjTypesAlphabetic(self, package):
    """ data types sorted alphabetically by name
    """
    return metaUtil.sortByAttribute(package.dataObjTypes,'name')
  
  ###########################################################################

  ###########################################################################
  
  def classesAlphabetic(self, package):
    """ classes sorted alphabetically by name
    """
    return metaUtil.sortByAttribute(package.classes,'name')
  
  ###########################################################################

  ###########################################################################
  
  def exceptionsAlphabetic(self, package):
    """ exceptions sorted alphabetically by name
    """
    return metaUtil.sortByAttribute(package.exceptions,'name')
  
  ###########################################################################

  ###########################################################################
  
  def constantsAlphabetic(self, package):
    """ constants sorted alphabetically by name
    """
    return metaUtil.sortByAttribute(package.constants,'name')
  
  ###########################################################################

  ###########################################################################
  
  def requiredInputElements(self, complexDataType):
    """ Return elements that must be passed to the constructor
    Elements are sorted alpahabetically by name
    """
    
    elems = []

    for attr in complexDataType.getAllAttributes():
      if (not attr.isDerived and not attr.isImplementation and not attr.isAutomatic
          and attr.locard > 0 and not attr.defaultValue):
        elems.append(attr)

    if isinstance(complexDataType, MetaModel.MetaClass):
      for role in complexDataType.getAllRoles():
        if (not role.isDerived and not role.isImplementation and not role.isAutomatic
            and role.locard > 0 and (role.hierarchy == metaConstants.no_hierarchy)):
          elems.append(role)
    
    return metaUtil.sortByAttribute(elems,'name')
  
  ###########################################################################

  ###########################################################################
  
  def metaObjFromQualName(self, qname):
    """ find MetaObject given qualified name
    """
    
    return self.topPackage.metaObjFromQualName(qname)
  
  ###########################################################################

  ###########################################################################
  
  def setModelFlavour(self, key, val):
    """ set modelflavour tag, checking that it is not set already
    """
    flavours = self.topPackage._modelFlavours
    flav = flavours.get(key)
    if flav is not None and flav != val:
      raise MemopsError(
       "attempt to change model flavour from %s:%s to :%s" % (key,flav,val,)
      )
    else:
      flavours[key] = val
    
  
  ###########################################################################

  ###########################################################################
  
  def checkModelFlavour(self, key, val):
    """ check that modelflavour for key is indeed val
    """
    flavours = self.topPackage._modelFlavours
    flav = flavours.get(key)
    if flav != val:
      raise MemopsError(
       "found wrong model flavour %s:%s, should be :%s" % (key, flav,val,)
      )
    
  
  ###########################################################################

  ###########################################################################
