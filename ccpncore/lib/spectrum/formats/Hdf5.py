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

__author__ = "$Author: rhf22 $"
__date__ = "$Date: 2016-05-16 02:12:40 +0100 (Mon, 16 May 2016) $"
#=========================================================================================
# Start of code
#=========================================================================================
import os, sys
from typing import Sequence

import h5py
import numpy

from ccpn.util.Common import checkIsotope

FILE_TYPE = 'Hdf5'

SPECTRUM_DATASET_NAME = 'spectrumData'

def readParams(filePath):
  
  hdf5file = h5py.File(filePath, 'r')
  dataset = hdf5file[SPECTRUM_DATASET_NAME]
  attrs = dataset.attrs
  
  # Format invariant

  dataFile = filePath
  wordSize = 4 # arbitrary
  headerSize = 0 # arbitrary
  blockHeaderSize = 0 # arbitrary
  pulseProgram = None
  dataScale = 1.0
  sampledValues = []
  sampledSigmas = []
  isBigEndian = sys.byteorder == 'big' # arbitrary
  isFloatData = True # arbitrary

  # Params

  numPoints = attrs['pointCounts']
  blockSizes = attrs['blockSizes']
  refPpms = attrs['referenceValues']
  refPoints = attrs['referencePoints']
  specWidths = attrs['spectralWidths']
  specFreqs = attrs['spectrometerFrequencies']
  isotopes = attrs['isotopeCodes'] # comes out as bytes

  # the attrs are NumPy arrays but much of the rest of the code does
  # not work with such arrays so convert first to more normal types
  numPoints = [int(numPoint) for numPoint in numPoints]
  blockSizes = [int(blockSize) for blockSize in blockSizes]
  refPpms = [float(refPpm) for refPpm in refPpms]
  refPoints = [float(refPoint) for refPoint in refPoints]
  specWidths = [float(specWidth) for specWidth in specWidths]
  specFreqs = [float(specFreq) for specFreq in specFreqs]
  isotopes = [checkIsotope(isotope.decode("utf-8")) for isotope in isotopes]

  hdf5file.close()

  data = (FILE_TYPE, dataFile, numPoints, blockSizes,
          wordSize, isBigEndian, isFloatData,
          headerSize, blockHeaderSize,
          isotopes, specFreqs,
          specWidths, refPoints, refPpms,
          sampledValues, sampledSigmas,
          pulseProgram, dataScale)

  return data

def getPlaneData(dataSource:'DataSource', position:Sequence=None, xDim:int=1, yDim:int=2):

  numDim = dataSource.numDim

  assert 1 <= xDim <= numDim, 'xDim = %d, numDim=%d' % (xDim, numDim)
  assert 1 <= yDim <= numDim, 'yDim = %d, numDim=%d' % (yDim, numDim)
  assert xDim != yDim, 'xDim = yDim = %d' % (xDim, yDim)

  xDim -= 1
  yDim -= 1

  if not position:
    position = numDim*[1]

  dataDims = dataSource.sortedDataDims()

  dataStore = dataSource.dataStore

  # TODO Can dataStore ever be None?
  filePath = dataStore.fullPath

  with h5py.File(filePath, 'r') as hdf5file:
    dataset = hdf5file[SPECTRUM_DATASET_NAME]
  
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
 
    data = dataset[tuple(slices)]
 
  if xDim > yDim:
    # swap x and y
    axes = numpy.arange(numDim)
    axes[numDim-xDim-1] = numDim-yDim-1
    axes[numDim-yDim-1] = numDim-xDim-1
    data = data.transpose(axes)

  data = data.reshape((yNumPoints, xNumPoints))

  data *= dataSource.scale

  return data

def getSliceData(dataSource:'DataSource', position:Sequence=None, sliceDim:int=1):

  numDim = dataSource.numDim

  assert 1 <= sliceDim <= numDim, 'sliceDim = %d, numDim=%d' % (sliceDim, numDim)

  sliceDim -= 1

  if not position:
    position = numDim*[1]

  dataDims = dataSource.sortedDataDims()

  dataStore = dataSource.dataStore
  filePath = dataStore.fullPath

  with h5py.File(filePath, 'r') as hdf5file:
    dataset = hdf5file[SPECTRUM_DATASET_NAME]
  
    slices = numDim * [0]
    for dim, dataDim in enumerate(dataDims):
      if dim == sliceDim:
        numPoints = dataDim.numPoints
        slices[numDim-dim-1] = slice(numPoints)
      else:
        slices[numDim-dim-1] = slice(position[dim]-1, position[dim])
 
    data = dataset[tuple(slices)]

  data = data.reshape((numPoints,))

  data *= dataSource.scale

  return data
 
def getRegionData(dataSource:'DataSource', startPoint:Sequence[float], endPoint:Sequence[float]):

  numDim = dataSource.numDim
  dataStore = dataSource.dataStore
  filePath = dataStore.fullPath

  with h5py.File(filePath, 'r') as hdf5file:
    dataset = hdf5file[SPECTRUM_DATASET_NAME]

    slices = numDim * [0]
    for dim in range(numDim):
      slices[numDim - dim - 1] = slice(startPoint[dim], endPoint[dim])

    data = dataset[tuple(slices)]

  data *= dataSource.scale

  return data
