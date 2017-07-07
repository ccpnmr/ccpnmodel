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
__dateModified__ = "$dateModified: 2017-07-07 16:33:24 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
from ccpnmodel.ccpncore.memops.scripts.core.TypeInterface import TypeInterface

repositoryTag = '$Name: not supported by cvs2svn $'
repositoryId  = '$Id: PyType.py,v 1.13 2007-12-11 16:47:30 wb104 Exp $'

class PyType(TypeInterface):

  ###########################################################################
  
  ###########################################################################

  # implements TypeInterface
  def elementVarType(self, element):

    return ''

  ###########################################################################

  ###########################################################################

  # implements TypeInterface
  def collectionType(self, elementOrString=None, isUnique=None, isOrdered=None,
                     useCollection=False):

    return ''

  ###########################################################################

  ###########################################################################

  # implements TypeInterface
  def implementationType(self, element):

    return ''

  ###########################################################################

  ###########################################################################

  # implements TypeInterface
  def interfaceType(self, element):

    return ''

  ###########################################################################

  ###########################################################################

  # implements TypeInterface
  def dictInterfaceType(self, keyType = None, valueType = None):

    return ''

  ###########################################################################

  ###########################################################################

  # implements TypeInterface
  def listInterfaceType(self, listType = None):

    return ''

  ###########################################################################

  ###########################################################################

  # implements TypeInterface
  def collectionInterfaceType(self, collectionType = None):

    return ''

  ###########################################################################

  ###########################################################################

  # implements TypeInterface
  def stackInterfaceType(self, stackType = None):

    return ''

  ###########################################################################

  ###########################################################################

  # implements TypeInterface
  def fileInterfaceType(self, mode = 'r'):

    return ''
