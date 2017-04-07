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
__dateModified__ = "$dateModified: 2017-04-07 11:41:44 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
""" Version for Python version > 2.1
"""

import os
from ccpnmodel.ccpncore.memops.metamodel import MetaModel
MemopsError = MetaModel.MemopsError
from ccpnmodel.ccpncore.memops.metamodel import Constants as metaConstants
from ccpnmodel.ccpncore.memops import Path

from ccpnmodel.ccpncore.memops.metamodel import TextWriter_py_2_1

settings = TextWriter_py_2_1.settings

class TextWriter(TextWriter_py_2_1.TextWriter_py_2_1, object):
  """
  """

  def __init__(self):
    """ parameters are mandatoryInitParams, optionalInitParams
    and the special optional
    """   
    
    for tag in TextWriter_py_2_1.mandatoryAttributes:
      if not hasattr(self, tag):
        raise MemopsError(" TextWriter lacks mandatory %s attribute" % tag)
    
    super(TextWriter, self).__init__()
      
    # special parameters: optional with default values
    if self.rootFileName is None:
      self.rootFileName = metaConstants.rootPackageDirName
      
    if self.rootDirName is None:
      self.rootDirName = os.path.join(Path.getCcpnmodelDirectory(), 'ccpncore')

    self.fp = None
    self.fileName = ''
    self.indent = 0
    self.indents = []

    self.errorMsg = ''

    self.previousLineEmpty = False # used so that do not print out two '\n' in a row
    
  ###########################################################################

  ###########################################################################
