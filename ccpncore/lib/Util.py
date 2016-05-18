"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Luca Mureddu, Simon Skinner, Geerten Vuister"
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

import os
import json
from collections import OrderedDict
from ccpnmodel.ccpncore.lib import Path
from ccpnmodel.ccpncore.memops.metamodel import Constants as metaConstants

apiTopModule = 'ccpnmodel.ccpncore.api'

# def _resetParentLink(apiObject, downLink:str, tag:str, value):
#   """Change single-attribute key of apiObject with property name tag to value
#
#   downLink is the name of the link from parent to obj"""
#
#   parent = apiObject.parent
#   siblings = getattr(parent, downLink)
#   if any(x for x in siblings if x is not apiObject and getattr(x, tag) == value):
#     raise ValueError("Cannot rename %s - pre-existing object with key %s:%s"
#         % apiObject, tag, value)
#
#   oldKey = getattr(apiObject, tag)
#   root = apiObject.root
#   root.__dict__['override'] = True
#
#   # Set up for undo
#   undo = root._undo
#   if undo is not None:
#     undo.increaseBlocking()
#
#   try:
#     parentDict = parent.__dict__[downLink]
#     del parentDict[oldKey]
#     setattr(apiObject, tag, value)
#     parentDict[value] = apiObject
#
#   finally:
#     # reset override and set isModified
#     root.__dict__['override'] = False
#     apiObject.topObject.__dict__['isModified'] = True
#     if undo is not None:
#       undo.decreaseBlocking()
#
#   if undo is not None:
#     undo.newItem(_resetParentLink, _resetParentLink, undoArgs=(apiObject, downLink, tag, oldKey),
#                  redoArgs=(apiObject, downLink, tag, value))
#
#   # call notifiers:


def _resetParentLink(apiObject, downLink:str, keys:OrderedDict):
  """Change apiObject with key attributes and values given in keys (OrderedDIct)

  downLink is the name of the link from parent to obj

  #CCPNINTERNAL
  Used in core.Data, core.Sample, core.SpectrumGroup, core.Substance,
  core.SampleComponent, core.SpectrumHit
  """

  parent = apiObject.parent
  siblings = getattr(parent, downLink)
  if any(x for x in siblings
         if x is not apiObject and all(getattr(x, y) == z for y,z in keys.items())):
    raise ValueError("Cannot rename %s - pre-existing object with keys %s"
        % apiObject, keys)

  undoKeys = OrderedDict((x, getattr(apiObject, x))for x in keys)
  if len(keys) == 1:
    tag = list(keys)[0]
    oldKey = undoKeys[tag]
    newKey = keys[tag]
  else:
    oldKey = tuple(undoKeys.values())
    newKey = tuple(keys.values())
  root = apiObject.root
  root.__dict__['override'] = True

  # Set up for undo
  undo = root._undo
  if undo is not None:
    undo.increaseBlocking()

  try:
    parentDict = parent.__dict__[downLink]
    del parentDict[oldKey]
    for tag, value in keys.items():
      setattr(apiObject, tag, value)
    parentDict[newKey] = apiObject

  finally:
    # reset override and set isModified
    root.__dict__['override'] = False
    apiObject.topObject.__dict__['isModified'] = True
    if undo is not None:
      undo.decreaseBlocking()

  if undo is not None:
    undo.newItem(_resetParentLink, _resetParentLink, undoArgs=(apiObject, downLink, undoKeys),
                 redoArgs=(apiObject, downLink,keys))


def getConfigParameter(name):
  """get configuration parameter, from reading configuration file
  """

  file = os.path.join(Path.getTopDirectory(),metaConstants.configFilePath)
  dd = json.load(open(file))
  return dd['configuration'].get(name)



def getClassFromFullName(qualifiedName):
  """ Get Api class from fully qualified (dot-separated) name
  """
  pathList = qualifiedName.split('.')
  mod = __import__('.'.join([apiTopModule] + pathList[:-1]),{},{},[pathList[-1]])
  return getattr(mod,pathList[-1])