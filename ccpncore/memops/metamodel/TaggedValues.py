"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
              "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                " or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================

from ccpnmodel.ccpncore.memops.metamodel import Constants as metaConstants
trueString = metaConstants.trueString
falseString = metaConstants.falseString

# used for packages with no packageGroup defined
defaultPackageGroup = 'core'

allowedTags = {
 'MetaModelElement':{
 },
 'ConstrainedElement':{
 },
 'ComplexDataType':{
  'specificImplementation':('db','file'),
 },
 'AbstractDataType':{
  # 'repositoryId':None,
  # 'repositoryTag':None,
 },
 'MetaDataObjType':{
 },
 'ClassElement':{
 },
 'AbstractValue':{'originalGuid':None,
 },
 'HasParameters':{
 },
 'MetaAttribute':{'forceUndoNotify':(falseString,),
 },
 'MetaClass':{
 },
 'MetaDataType':{
 },
 'MetaOperation':{'originalGuid':None,
 },
 'MetaPackage':{
  'docDiagramNames':None,
  'packageGroup':('nmr','pp',defaultPackageGroup),
  # 'repositoryId':None,
  # 'repositoryTag':None,
  'isDraft':(trueString,), # NBNB TODO do we need this?
  'isReferenceData':(trueString,), # NBNB TODO do we need this?
 },
 'MetaParameter':{
  'isSubdivided':(trueString,)  # slightly obscure. Used to identify
                                # collections of undeclared parameters
                                # in languages that support them.
                                # If the valueType is a stringKeyDict 
                                # the parameters are assumed to be keyword-value
                                # else they are assumed to be normal.
                                # In practice used for Python * and ** params
 },
 'MetaRole':{'forceUndoNotify':(falseString,),
 },
 'MetaConstraint':{
 },
 'MetaConstant':{
  # 'repositoryId':None,
  # 'repositoryTag':None,
 },
 'MetaException':{
  # 'repositoryId':None,
  # 'repositoryTag':None,
 }
} 
