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
""" Python-specific version of ModelAdapt
"""

from ccpnmodel.ccpncore.memops.scripts.core.PyModelAdapt import PyModelAdapt
from ccpnmodel.ccpncore.memops.scripts.core.FileModelAdapt import FileModelAdapt


def processModel(modelPortal, **kw):
  """process model to adapt it for Python
  
  Only function that should be called directly by 'make' scripts etc.
  """
  pyFileModelAdapt = PyFileModelAdapt(modelPortal=modelPortal, **kw)
  pyFileModelAdapt.processModel()


class PyFileModelAdapt(PyModelAdapt, FileModelAdapt):
  """ Python-specific version of ModelAdapt
  """
  def __init__(self, **kw):
    """Class constructor.
    Automatically processes model.
    """
    
    for (tag, val) in kw.items():
      if not hasattr(self, tag):
        setattr(self, tag, val)
    
    # superclass init call
    super(PyFileModelAdapt, self).__init__()
