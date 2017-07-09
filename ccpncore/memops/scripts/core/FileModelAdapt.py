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
__dateModified__ = "$dateModified: 2017-07-07 16:33:23 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
""" Python-specific version of ModelAdapt
"""

from ccpnmodel.ccpncore.memops.metamodel import Constants as metaConstants
from ccpnmodel.ccpncore.memops.scripts.core.ModelAdapt import ModelAdapt


class FileModelAdapt(ModelAdapt):
  """ Python-specific version of ModelAdapt
  """
  def __init__(self):
    """Class constructor.
    Automatically processes model.
    """
    
    # model flavour (must be done first) 
    self.addModelFlavour('implementation','file')
    
    # superclass init call
    super(FileModelAdapt, self).__init__()
    
    # add to varNames
  
    # parameters for specific functions and function types
    self.varNames['topObjectsToCheck'] = 'topObjectsToCheck'
    self.varNames['notIsReading'] = 'notIsReading'
  
    # Implementation links
  
    # Implementation attributes
    self.varNames['isReading'] = 'isReading'
    self.varNames['isLoaded'] = 'isLoaded'
    self.varNames['isModified'] = 'isModified'
    self.varNames['topObjects'] = 'topObjects'
    self.varNames['activeRepositories'] = 'activeRepositories'
    self.varNames[metaConstants.serialdict_attribute] = '_serialDict'
    self.varNames[metaConstants.lastid_attribute] = '_lastId'
    
    # adapt opData
    operationData = self.operationData
    # checkDelete
    opType ='checkDelete'
    for subOp in operationData[opType]['subOps'].values():
      subOp['parameters'].append(
       {'name':'topObjectsToCheck', 'direction':metaConstants.in_direction,
        'parDocumentation':"Set of topObjects to check for modifiability",
        'target':'memops.Implementation.MemopsObject', 
        'hicard':metaConstants.infinity, 'locard':0,
        'isOrdered':False, 'isUnique':True,
       },
      )
    
    # NBNB TBD check target for typed languages
            
  ###########################################################################
