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
__version__ = "$Revision: 3.0.b3 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
import os, sys

# from ccpnmodel.ccpncore.lib.spectrum.Spectrum import checkIsotope
# from memops.qtgui.MessageDialog import showError

from array import array

FILE_TYPE = 'NMRView'

def readParams(paramFileName):

  byteOrderFlags = { ('34','18','AB','CD') : 'big',
                     ('CD','AB','18','34') : 'little'}

  #
  
  wordSize = 4
  isBigEndian = sys.byteorder == 'big'
  isFloatData = True
  headerSize = 2048
  blockHeaderSize = 0
  sampledValues = []
  sampledSigmas = []
  pulseProgram = None
  dataScale = 1.0
  
  dataFile = os.path.splitext(paramFileName)[0] + '.nv'
  
  fileObj = open(dataFile, 'rb')  
  headData = fileObj.read(headerSize)
  if len(headData) < headerSize:
    msg = 'NmrView file %s appears to be truncated'
    # showError('Error', msg % dataFile)
    return

  fileObj.close()
  
  intVals = array('i')
  floatVals = array('f')
  cBuffer = array('B')
  
  intVals.fromstring(headData)
  floatVals.fromstring(headData)
  cBuffer.fromstring(headData)
  
  magicBytes = tuple(["%02X" % byte for byte in cBuffer[:4]])
      
  if magicBytes not in byteOrderFlags:
    msg = 'NmrView file %s appears to be corrupted: does not start with the expected magic bytes'
    # showError('Error', msg % dataFile)
    return

  if sys.byteorder != byteOrderFlags[magicBytes]:
    intVals.byteswap()
    floatVals.byteswap()
  
  ndim = intVals[6]
  
  numPoints = [0] * ndim
  blockSizes = [0] * ndim
  refPpms = [0] * ndim
  refPoints = [0] * ndim
  specWidths = [1000.0] * ndim
  specFreqs = [500.0] * ndim
  isotopes = [None] * ndim
  
  dimBase = 256
  dimRecordSize = 32
  dimSizeOffset = 0
  dimBlockSizeOffest = 1
  dimSFOffest = 6
  dimSWOffest = 7
  dimRefPointOffset = 8
  dimRefValueOffset = 9  
  
  duffDims = []
  
  for i in range(ndim):
    points = intVals[dimBase + (i*dimRecordSize) + dimSizeOffset]
    
    if points < 1:
      duffDims.append(i)
      continue
    
    numPoints[i] = points
    blockSizes[i] = intVals[dimBase + (i*dimRecordSize) + dimBlockSizeOffest]
    specFreqs[i] = floatVals[dimBase + (i*dimRecordSize) + dimSFOffest]
    specWidths[i] = floatVals[dimBase + (i*dimRecordSize) + dimSWOffest]
    refPpms[i]  = floatVals[dimBase + (i*dimRecordSize) + dimRefPointOffset]+1
    refPpms[i] = floatVals[dimBase + (i*dimRecordSize) + dimRefValueOffset]
  
  for i in duffDims[::-1]:
    del numPoints[i]
    del blockSizes[i]
    del specFreqs[i]
    del specWidths[i]
    del refPpms[i]
    del refPpms[i]
  
  isotopes = _guessConsistentNuclei(specFreqs)

  data = (FILE_TYPE, dataFile, numPoints, blockSizes,
          wordSize, isBigEndian, isFloatData,
          headerSize, blockHeaderSize,
          isotopes, specFreqs,
          specWidths, refPoints, refPpms,
          sampledValues, sampledSigmas,
          pulseProgram, dataScale)

  return data
  
def _guessConsistentNuclei(sf):

  ndim = len(sf)
  isotopes = [None] * ndim
  ratios = [1.0, 0.4052, 0.2512, 0.1013]
  nuclei = ['1H', '31P', '13C', '15N']
  
  sfs  = list(set(sf))
  if len(sfs) > 1:  # at least two type of nuclei
    sfs.sort(reverse=True)
    bestSets  = {}

    sfsTop = sfs[0]
    sfs = sfs[1:]
    while len(ratios) >= ndim:
      topNucleus  = nuclei[0]
      ratiosTop = ratios[0]

      # remaining nuclei and spec frequencies
      ratios = ratios[1:]
      nuclei = nuclei[1:]
      targetRatio = sfsTop/ratiosTop
    
      currentSet  = [(sfsTop,topNucleus)]         
      bestSum  = 0

      for sf in sfs:          
        best  = int(float(sys.maxsize))
        
        for i,pair in enumerate(zip(ratios,nuclei)):
        
          ratio =pair[0]
          nucleus = pair[1]
          error  = abs((sf/ratio) - targetRatio)
        
          if error < best:
            best = error
            bestIndex  = i
               
        currentSet.append((sf,nuclei[bestIndex]))
        bestSum += best
      
      bestSets[bestSum] = currentSet
  
    keys = sorted(bestSets.keys())
  
    nucleiLookup = {}
    for matches in bestSets[keys[0]]:
      nucleiLookup[matches[0]]=matches[1]
    
    sfs = [sfsTop]+sfs
    for i in range(ndim):
      isotopes[i] = nucleiLookup[sfs[i]]

  else: 
    for i in range(ndim):
      isotopes[i] = '1H'
  
  return isotopes
