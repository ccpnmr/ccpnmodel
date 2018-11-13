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
__version__ = "$Revision: 3.0.b4 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
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
