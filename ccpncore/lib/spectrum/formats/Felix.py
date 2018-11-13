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
__dateModified__ = "$dateModified: 2017-07-07 16:33:15 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b4 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
import os, sys

from ccpn.util.Common import checkIsotope
# from memops.qtgui.MessageDialog import showError

from array import array

FILE_TYPE = 'Felix'

def readParams(paramFileName):

  dataFile = paramFileName
  headerSize = 4*4096
  
  wordSize = 4
  isBigEndian = sys.byteorder == 'big'
  isFloatData = True
  blockHeaderSize = 0
  dataScale = 1.0

  sampledValues = []
  sampledSigmas = []
  pulseProgram = None

  fileObj = open(paramFileName, 'rb')
  headData = fileObj.read(headerSize)
  
  if len(headData) < headerSize:
    msg = "FELIX file %s appears truncated"
    # showError('Error', msg % paramFileName)
    return
  
  fileObj .close()
  
  intVals = array('i')
  floatVals = array('f')

  intVals.fromstring(headData)
  floatVals.fromstring(headData)

  matrix_type = intVals[1]
  if (matrix_type != 1):
    isBigEndian = not isBigEndian
    intVals.byteswap()
    floatVals.byteswap()
    
    if intVals[1] != 1:
      msg = "FELIX file %s appears to be corrupted"
      # showError('Error', msg % paramFileName)
      return 

  ndim = intVals[0]

  numPoints = [0] * ndim
  blockSizes = [0] * ndim
  refPpms = [0] * ndim
  refPoints = [0] * ndim
  specWidths = [0] * ndim
  specFreqs = [0] * ndim
  isotopes = [0] * ndim

  for i in range(ndim):
    numPoints[i] = intVals[20+1*ndim+i]
    blockSizes[i] = intVals[20+4*ndim+i]
    specFreqs[i] = floatVals[20+6*ndim+i]
    specWidths[i] = floatVals[20+7*ndim+i]
    refPoints[i] = floatVals[20+8*ndim+i]
    refPpms[i] = floatVals[20+9*ndim+i] / specFreqs[i]
    isotope = ''
    j = 0
    while ((j < 8) and intVals[220+8*i+j]):
      isotope = isotope + chr(intVals[220+8*i+j])
      j = j + 1
    isotopes[i] = checkIsotope(isotope)
  
  data = (FILE_TYPE, dataFile, numPoints, blockSizes,
          wordSize, isBigEndian, isFloatData,
          headerSize, blockHeaderSize,
          isotopes, specFreqs,
          specWidths, refPoints, refPpms,
          sampledValues, sampledSigmas,
          pulseProgram, dataScale)

  return data
