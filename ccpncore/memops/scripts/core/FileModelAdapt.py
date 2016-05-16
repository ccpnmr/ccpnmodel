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
