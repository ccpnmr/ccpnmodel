"""Functions for insertion into ccp.nmr.Nmr.AbstractDataDim

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
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:35 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

# Additional functions for ccp.nmr.Nmr.AbstractDataDim
#
# NB All functions must have a mandatory DataSource as the first parameter
# so they can be used as AbstractDataDim methods

from typing import Set


   
# NB change from getDataDimIsotopes
#def getDataDimIsotopes(dataDim):
def getIsotopeCodes(self:'AbstractDataDim') -> Set[str]:
  """
  Get the shift measurement isotopes for a spectrum data dim
  
  .. describe:: Input
  
  Nmr.AbstarctDataDim (or subtypes)
  
  .. describe:: Output

  Set of Words (Nmr.ExpDimRef.isotopeCodes)
  """

  isotopes = set()
    
  for expDimRef in self.expDim.expDimRefs:
    if expDimRef.measurementType in ('Shift','shift'):
      for isotopeCode in expDimRef.isotopeCodes:
        isotopes.add(isotopeCode)
 
  return isotopes

# Not needed after all
# def getDefaultPlaneSize(dataDim):
#   """get default plane size - currently one point"""
#   return dataDim.primaryDataDimRef.valuePerPoint
