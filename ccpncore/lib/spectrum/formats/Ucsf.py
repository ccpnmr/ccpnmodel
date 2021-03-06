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
__version__ = "$Revision: 3.0.0 $"
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

UCSF_FILE_HEADER = 180
UCSF_DIM_HEADER = 128

FILE_TYPE = 'UCSF'

from array import array

def readParams(fileName):

  # Format invariant
  
  wordSize = 4
  dataFile = fileName
  isFloatData = True
  isBigEndian = True # Always
  blockHeaderSize = 0
  pulseProgram = None
  dataScale = 1.0
  sampledValues = []
  sampledSigmas = []
  
  # Params
  
  numPoints = []
  blockSizes = []
  refPpms = []
  refPoints = []
  specWidths = []
  specFreqs = []
  isotopes = []
  params = []
  sigmas = []
  
  fileObj = open(fileName, 'rb')
  
  headerData = fileObj.read(UCSF_FILE_HEADER)
  
  if len(headerData) < UCSF_FILE_HEADER:
    msg = "UCSF file %s appears truncated"
    # showError('Error', msg % fileName)
    print(msg)
    return
  
  if headerData[:8] != b'UCSF NMR':
    msg = "UCSF file %s not proper UCSF format"
    # showError('Error', msg % fileName)
    print(msg)
    return
  
  numDims = ord(chr(headerData[10]))
  headerSize = UCSF_FILE_HEADER + numDims*UCSF_DIM_HEADER
  
  dimData = fileObj.read(numDims*UCSF_DIM_HEADER)
  if len(dimData) < numDims*UCSF_DIM_HEADER:
    msg = "UCSF file %s appears truncated"
    print(msg)
    # showError('Error', msg % fileName)
    return
  
  fileObj.close()
  
  intVals = array('i')
  floatVals = array('f')
  
  intVals.fromstring(dimData)
  floatVals.fromstring(dimData)
  if sys.byteorder != 'big':
    intVals.byteswap()
    floatVals.byteswap()
  for dim in range(numDims):
    base = int(((numDims - dim - 1)*UCSF_DIM_HEADER) / 4)
    numPoint = intVals[base+2]
    numPoints.append( numPoint )
    blockSizes.append( intVals[base+4] )
    specFreqs.append( floatVals[base+5] )
    specWidths.append( floatVals[base+6] )
    refPpms.append( floatVals[base+7] )
    refPoints.append( 1.0 + 0.5 * numPoint)
    
    isotope = dimData[4*base:4*base+6]
    n = isotope.find(0)
    if n >= 0:
      isotope = (isotope[:n])
    isotopes.append( checkIsotope(isotope.decode("utf-8")) )
   
  fileObj.close()
  
  data = (FILE_TYPE, dataFile, numPoints, blockSizes,
          wordSize, isBigEndian, isFloatData,
          headerSize, blockHeaderSize, isotopes, specFreqs,
          specWidths, refPoints, refPpms,
          sampledValues, sampledSigmas, pulseProgram, dataScale)
  
  return data
