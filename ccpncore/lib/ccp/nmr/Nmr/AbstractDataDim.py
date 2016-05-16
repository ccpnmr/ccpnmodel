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