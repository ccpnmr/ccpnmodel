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
__author__ = "$Author: wb104 $"
__date__ = "$Date: 2017-03-24 14:31:10 +0000 (Fri, March 24, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import os, re, sys
from typing import Sequence

import numpy

from ccpn.util.Common import checkIsotope
from ccpn.util.Logging import getLogger

# from memops.qtgui.MessageDialog import showError

from array import array

NDIM_INDEX = 9
NPTS_INDEX = (99, 219, 15, 32)
COMPLEX_INDEX = (55, 56, 51, 54)
ORDER_INDEX = (24, 25, 26, 27)
SW_INDEX = (229, 100, 11, 29)
SF_INDEX = (218, 119, 10, 28)
ORIGIN_INDEX = (249, 101, 12, 30)
ISOTOPE_INDEX = (18, 16, 20, 22)
VALUE_INDEX = 199
NFILES_INDEX = 442

FILE_TYPE = 'NMRPipe'

def readParams(filePath, getFileCount=False):

  dataFile = filePath
  wordSize = 4
  isFloatData = True
  headerSize = 4*512
  blockHeaderSize = 0
  sampledValues = []
  sampledSigmas = []
  pulseProgram = None
  dataScale = 1.0
  
  fileObj = open(filePath, 'rb')

  headData = fileObj.read(headerSize)
  fileObj.close()

  if len(headData) < headerSize:
    msg = 'NMRPipe file %s appears to be truncated'
    getLogger().warning(msg)
    # showError('Error', msg % filePath)
    return

  floatVals = array('f')
  floatVals.fromstring(headData)

  if floatVals[0] != 0.0:
    msg = 'NMRPipe file %s appears to be corrupted'
    getLogger().warning(msg)
    # showError('Error', msg % filePath)
    return

  byte_order = [ 0x40, 0x16, 0x14, 0x7b ]
  t = [ ord(chr(c)) for c in headData[8:12] ]
  if t == byte_order:
    isBigEndian = True
    
  else:
    t.reverse()
    if t == byte_order:
      isBigEndian = False
      
    else:
      msg = 'NMRPipe file %s appears to be corrupted'
      getLogger().warning(msg)
      # showError('Error', msg % filePath)
      return

  if isBigEndian is not (sys.byteorder == 'big'):
    floatVals.byteswap()

  ndim = int(floatVals[NDIM_INDEX])
  
  if not (0 < ndim < 5):
    msg = 'Can only handle NMRPipe files with between 1 and 4 dimensions'
    getLogger().warning(msg)
    # showError('Error', msg)
    return

  if getFileCount:
    data = int(floatVals[NFILES_INDEX])
    
  else:
    numPoints = [0] * ndim
    blockSizes = [0] * ndim
    refPpms = [0.0] * ndim
    refPoints = [0.0] * ndim
    specWidths = [1000.0] * ndim
    specFreqs = [500.0] * ndim
    isotopes = [None] * ndim

    # print indices
    # print([int(floatVals[i])-1 for i in ORDER_INDEX])
    # print([int(floatVals[i]) for i in COMPLEX_INDEX+(50,)])

    for i in range(ndim):
      j = int(floatVals[ORDER_INDEX[i]]) - 1
      c = int(floatVals[COMPLEX_INDEX[i]])
      if c == 0:
        msg = 'NMRPipe data is complex in dim %d, can only cope with real data at present' % i
        getLogger().warning(msg)
        # showError('Error', msg % (i+1))
        return
      
      numPoints[i] = int(floatVals[NPTS_INDEX[i]])
    
      if i == 0:
        blockSizes[i] = numPoints[i]
      else:
        blockSizes[i] = 1
      
      specWidths[i] = sw = floatVals[SW_INDEX[j]]
      if sw == 0:
        specWidths[i] = sw  = 1000 # ?
      
      specFreqs[i] = sf = floatVals[SF_INDEX[j]]
      o = floatVals[ORIGIN_INDEX[j]]
    
      refPpms[i] = (sw + o) / sf
      refPoints[i] = 0
      n = 4 * ISOTOPE_INDEX[j]
      isotope = headData[n:n+4].strip()

      # get rid of null termination
      m = isotope.find(0)
      if m >= 0:
        isotope = (isotope[:n])
      isotopes.append( checkIsotope(isotope.decode("utf-8")) )
      
      if isotope == 'ID': # ?
        isotopes[i] = None
      else:
        isotopes[i] = checkIsotope(isotope.decode("utf-8"))

    data = (FILE_TYPE, dataFile, numPoints, blockSizes,
            wordSize, isBigEndian, isFloatData,
            headerSize, blockHeaderSize,
            isotopes, specFreqs,
            specWidths, refPoints, refPpms,
            sampledValues, sampledSigmas,
            pulseProgram, dataScale)

  return data

def _guessFileTemplate(dataSource):
  """
  ##CCPNINTERNAL
  Called from ccpnmodel.ccpncore.lib._ccp.nmr.Nmr.DataSource
  """

  dataStore = dataSource.dataStore

  if not dataStore:
    return None
  
  fullPath = dataStore.fullPath
  fileCount = readParams(fullPath, getFileCount=True)
  if fileCount == 1: # single file
    return None
    
  fileName = os.path.basename(fullPath)
  directory = os.path.dirname(fullPath)
  numDim = dataSource.numDim

  if numDim < 3 or r'%' in fileName:
    template = fileName
    
  elif numDim == 3:
    template = re.sub('\d\d\d', '%03d', fileName)
    
  else: # numDim == 4
    # don't understand NmrPipe templates (how many 0's are allowed) so a hack here for now
    numPoints1, numPoints0 = [dataDim.numPoints for dataDim in dataSource.sortedDataDims()][-2:]

    # had an example where numPoints0 < 100 but had %03d%03d
    #if numPoints0 < 100:
    #  template = re.sub('\d\d\d\d\d', '%02d%03d', fileName)
    #else:
    #  template = re.sub('\d\d\d\d\d\d', '%03d%03d', fileName)

    for template in (re.sub('\d\d\d\d\d\d', '%03d%03d', fileName), ):
      filePath = os.path.join(directory, template % (numPoints0, numPoints1))
      if os.path.exists(filePath):
        break
    else:
      template = re.sub('\d\d\d\d\d', '%02d%03d', fileName)

  return os.path.join(directory, template)
  
def _getFileData(fullPath, numPoints, headerSize, dtype):
  
  if len(numPoints) == 1:
    n = numPoints[0]
  else:
    n = numPoints[0] * numPoints[1]
    
  fp = open(fullPath, 'rb')
  fp.seek(headerSize, 0)
  data = numpy.fromfile(file=fp, dtype=dtype, count=n).reshape(numPoints) # data is in reverse order: y,x not x,y
  fp.close()
  
  if data.dtype != numpy.float32:
    data = numpy.array(data, numpy.float32)
    
  return data
  
def readData(dataSource):
  
  dataStore = dataSource.dataStore
  if not dataStore:
    return None
  
  if not hasattr(dataStore, 'template'):
    dataStore.template = _guessFileTemplate(dataSource)
    # TBD: for now assume that above works
  
  fullPath = dataStore.fullPath
  wordSize = dataStore.nByte
  isBigEndian = dataStore.isBigEndian
  isFloatData = dataStore.numberType == 'float'
  headerSize = dataStore.headerSize
  
  dtype = '%s%s%s' % (isBigEndian and '>' or '<', isFloatData and 'f' or 'i', wordSize)
  
  numPoints = tuple(reversed([dataDim.numPoints for dataDim in dataSource.sortedDataDims()]))
  numDim = dataSource.numDim
  
  if numDim < 3:
    data = _getFileData(fullPath, numPoints, headerSize, dtype)
    
  elif numDim == 3:
    yxPoints = numPoints[-2:]
    data = numpy.zeros(numPoints, dtype='float32')
    template = dataStore.template
    for z in range(numPoints[0]):
      zdata = _getFileData(template % (z+1), yxPoints, headerSize, dtype)
      data[z,:,:] = zdata

  elif numDim == 4:
    yxPoints = numPoints[-2:]
    data = numpy.zeros(numPoints, dtype='float32')
    template = dataStore.template
    for w in range(numPoints[0]):
      for z in range(numPoints[1]):
        planedata = _getFileData(template % (w+1, z+1), yxPoints, headerSize, dtype)
        data[w, z, :, :] = planedata

  else:
    raise Exception('numDim > 4 not implemented yet')
    
  return data
  
def getPlaneData(dataSource:'DataSource', position:Sequence=None, xDim:int=1, yDim:int=2):
    
  xDim -= 1
  yDim -= 1
  
  if not hasattr(dataSource, 'data'):
    dataSource.data = readData(dataSource)
    
  numDim = dataSource.numDim
  
  if not position:
    position = numDim*[1]
  
  dataDims = dataSource.sortedDataDims()
  
  slices = numDim * [0]
  for dim, dataDim in enumerate(dataDims):
    if dim in (xDim, yDim):
      numPoints = dataDim.numPoints
      slices[numDim-dim-1] = slice(numPoints)
      if dim == xDim:
        xNumPoints = numPoints
      else:
        yNumPoints = numPoints
    else:
      slices[numDim-dim-1] = slice(position[dim]-1, position[dim])
  
  data = dataSource.data[tuple(slices)]
  
  if xDim > yDim:
    # swap x and y
    axes = numpy.arange(numDim)
    axes[numDim-xDim-1] = numDim-yDim-1
    axes[numDim-yDim-1] = numDim-xDim-1
    data = data.transpose(axes)
 
  data = data.reshape((yNumPoints, xNumPoints))

  # data *= dataSource.scale

  return data

def getSliceData(dataSource:'DataSource', position:Sequence=None, sliceDim:int=1):

  sliceDim -= 1

  if not hasattr(dataSource, 'data'):
    dataSource.data = readData(dataSource)

  numDim = dataSource.numDim

  if not position:
    position = numDim*[1]

  dataDims = dataSource.sortedDataDims()

  slices = numDim * [0]
  for dim, dataDim in enumerate(dataDims):
    if dim == sliceDim:
      numPoints = dataDim.numPoints
      slices[numDim-dim-1] = slice(numPoints)
    else:
      slices[numDim-dim-1] = slice(position[dim]-1, position[dim])

  data = dataSource.data[tuple(slices)]
  data = data.reshape((numPoints,))

  # data *= dataSource.scale

  return data

def getRegionData(dataSource:'DataSource', startPoint:Sequence[float], endPoint:Sequence[float]):


  if not hasattr(dataSource, 'data'):
    dataSource.data = readData(dataSource)

  numDim = dataSource.numDim
  slices = numDim * [0]
  for dim in range(numDim):
    slices[numDim-dim-1] = slice(startPoint[dim], endPoint[dim])

  data = dataSource.data[tuple(slices)]

  # data *= dataSource.scale

  return data
