"""Functions for insertion into ccp.nmr.Nmr.PeakList

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:11 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import numpy

from ccpn.util import Undo
from ccpnmodel.ccpncore.api.ccp.nmr.Nmr import PeakList

from typing import Sequence

def _cumulativeArray(array):
  """ get total size and strides array.
      NB assumes fastest moving index first """

  ndim = len(array)
  cumul = ndim * [0]
  n = 1
  for i, size in enumerate(array):
    cumul[i] = n
    n = n * size

  return (n, cumul)

def _arrayOfIndex(index, cumul):
  """ Get from 1D index to point address tuple
  NB assumes fastest moving index first
  """

  ndim = len(cumul)
  array = ndim * [0]
  for i in range(ndim-1, -1, -1):
    c = cumul[i]
    array[i], index = divmod(index, c)

  return numpy.array(array)

def pickNewPeaks(self:PeakList, startPoint:Sequence[int], endPoint:Sequence[int],
                 posLevel:float=None, negLevel:float=None,
                 minLinewidth=None, exclusionBuffer=None,
                 minDropfactor:float=0.1, checkAllAdjacent:bool=True,
                 fitMethod:str=None, excludedRegions=None,
                 excludedDiagonalDims=None, excludedDiagonalTransform=None):

  # startPoint and endPoint are 0-based not 1-based

  from ccpnc.peak import Peak as CPeak

  undo = self.root._undo
  if undo is not None:
    undo.increaseBlocking()
  try:

    if fitMethod:
      assert fitMethod in ('gaussian', 'lorentzian'), 'fitMethod = %s, must be one of ("gaussian", "lorentzian")' % fitMethod
      method = 0 if fitMethod == 'gaussian' else 1

    peaks = []

    if posLevel is None and negLevel is None:
      return peaks

    dataSource = self.dataSource
    numDim = dataSource.numDim

    if not minLinewidth:
      minLinewidth = [0.0] * numDim

    if not exclusionBuffer:
      exclusionBuffer =  [1] * numDim

    nonAdj = 1 if checkAllAdjacent else 0

    if not excludedRegions:
      excludedRegions = []

    if not excludedDiagonalDims:
      excludedDiagonalDims = []

    if not excludedDiagonalTransform:
      excludedDiagonalTransform = []

    startPoint = numpy.array(startPoint)
    endPoint = numpy.array(endPoint)

    startPoint, endPoint = numpy.minimum(startPoint, endPoint), numpy.maximum(startPoint, endPoint)

    # extend region by exclusionBuffer
    bufferArray = numpy.array(exclusionBuffer)
    startPointBuffer = startPoint - bufferArray
    endPointBuffer = endPoint + bufferArray

    regions = numDim*[0]
    npts = numDim*[0]
    for n in range(numDim):
      start = startPointBuffer[n]
      end = endPointBuffer[n]
      npts[n] = dataSource.findFirstDataDim(dim=n+1).numPointsOrig
      tile0 = start // npts[n]
      tile1 = (end-1) // npts[n]
      region = regions[n] = []
      if tile0 == tile1:
        region.append((start, end, tile0))
      else:
        region.append((start, (tile0+1)*npts[n], tile0))
        region.append((tile1*npts[n], end, tile1))
      for tile in range(tile0+1, tile1):
        region.append((tile*npts[n], (tile+1)*npts[n], tile))

    peaks = []
    objectsCreated = []

    nregions = [len(region) for region in regions]
    nregionsTotal, cumulRegions = _cumulativeArray(nregions)
    for n in range(nregionsTotal):
      array = _arrayOfIndex(n, cumulRegions)
      chosenRegion = [regions[i][array[i]] for i in range(numDim)]
      startPointBufferActual = numpy.array([cr[0] for cr in chosenRegion])
      endPointBufferActual = numpy.array([cr[1] for cr in chosenRegion])
      tile = numpy.array([cr[2] for cr in chosenRegion])
      startPointBuffer = numpy.array([startPointBufferActual[i]-tile[i]*npts[i] for i in range(numDim)])
      endPointBuffer = numpy.array([endPointBufferActual[i]-tile[i]*npts[i] for i in range(numDim)])

      dataArray, intRegion = dataSource.getRegionData(startPointBuffer, endPointBuffer)
      startPointInt, endPointInt = intRegion
      startPointInt = numpy.array(startPointInt)
      endPointInt = numpy.array(endPointInt)
      startPointIntActual = numpy.array([startPointInt[i]+tile[i]*npts[i] for i in range(numDim)])
      numPointInt = endPointInt - startPointInt
      startPointBuffer = numpy.maximum(startPointBuffer, startPointInt)
      endPointBuffer = numpy.minimum(endPointBuffer, endPointInt)
      if numpy.any(numPointInt <= 2): # return if any of the dimensions has <= 2 points
        continue

      #startPointBuffer = numpy.array(startPointBuffer, dtype='float32')
      excludedRegionsList = [numpy.array(excludedRegion, dtype='float32')-startPointBuffer for excludedRegion in excludedRegions]

      excludedDiagonalDimsList = []
      excludedDiagonalTransformList = []
      for n in range(len(excludedDiagonalDims)):
        dim1, dim2 = excludedDiagonalDims[n]
        a1, a2, b12, d = excludedDiagonalTransform[n]
        b12 += a1*startPointBuffer[dim1] - a2*startPointBuffer[dim2]
        excludedDiagonalDimsList.append(numpy.array((dim1, dim2), dtype='int32'))
        excludedDiagonalTransformList.append(numpy.array((a1, a2, b12, d), dtype='float32'))

      """
      existingPeaks = getRegionPeaks(peakList, startPointInt, endPointInt)
      existingPoints = set()
      for peak in existingPeaks:
        keys = [[],]

        for i, point in enumerate(peak.getPoints()):
          p1 = int(point)
          p2 = p1+1

          for key in keys[:]:
            keys.append(key + [p2],)
            key.append(p1)

        existingPoints.update([tuple(k) for k in keys])
      """
      doPos = posLevel is not None
      doNeg = negLevel is not None
      posLevel = posLevel or 0.0
      negLevel = negLevel or 0.0

      peakPoints = CPeak.findPeaks(dataArray, doNeg, doPos,
                                   negLevel, posLevel, exclusionBuffer,
                                   nonAdj, minDropfactor, minLinewidth,
                                   excludedRegionsList, excludedDiagonalDimsList, excludedDiagonalTransformList)

      peakPoints = [(numpy.array(position), height) for position, height in peakPoints]

      # only keep those points which are inside original region, not extended region
      peakPoints = [(position, height) for position, height in peakPoints if ((startPoint-startPointIntActual) <= position).all() and (position < (endPoint-startPointIntActual)).all()]

      # check new found positions against existing ones
      existingPositions = []
      for peak in self.peaks:
        position = numpy.array([peakDim.position for peakDim in peak.sortedPeakDims()])  # ignores aliasing
        existingPositions.append(position-1) # -1 because API position starts at 1

      # NB we can not overwrite exclusionBuffer, because it may be used as a parameter in redong
      # and 'if not exclusionBuffer' does not work on nympy arrays.
      numpyExclusionBuffer = numpy.array(exclusionBuffer)

      for position, height in peakPoints:

        position += startPointBufferActual

        for existingPosition in existingPositions:
          delta = abs(existingPosition - position)
          if (delta < numpyExclusionBuffer).all():
            break
        else:
          if fitMethod:
            position -= startPointBufferActual
            numDim = len(position)
            firstArray = numpy.maximum(position - 2, 0)
            lastArray = numpy.minimum(position + 3, numPointInt)
            peakArray = position.reshape((1, numDim))
            peakArray = peakArray.astype('float32')
            firstArray = firstArray.astype('int32')
            lastArray = lastArray.astype('int32')
            regionArray = numpy.array((firstArray, lastArray))

            try:
              result = CPeak.fitPeaks(dataArray, regionArray, peakArray, method)
              height, center, linewidth = result[0]

              # TODO:ED constrain result to position +/- exclusionBuffer
              center = center.clip(min=position-exclusionBuffer
                                   , max=position+exclusionBuffer)
            except:
              # possibly should log error??
              dimCount = len(startPoint)
              height = float(dataArray[tuple(position[::-1])])
                # have to reverse position because dataArray backwards
                # have to float because API does not like numpy.float32
              center = position
              linewidth = dimCount * [None]
            position = center + startPointBufferActual

          peak = self.newPeak()

          dataDims = dataSource.sortedDataDims()
          peakDims = peak.sortedPeakDims()

          for i, peakDim in enumerate(peakDims):
            dataDim = dataDims[i]

            if dataDim.className == 'FreqDataDim':
              dataDimRef = dataDim.primaryDataDimRef
            else:
              dataDimRef = None

            if dataDimRef:
              peakDim.numAliasing = int(divmod(position[i], dataDim.numPointsOrig)[0])
              peakDim.position = float(position[i] + 1 - peakDim.numAliasing * dataDim.numPointsOrig)  # API position starts at 1

            else:
              peakDim.position = float(position[i] + 1)

            if fitMethod and linewidth[i] is not None:
              peakDim.lineWidth = dataDim.valuePerPoint * linewidth[i] # conversion from points to Hz

          peak.height = dataSource.scale * height
          peaks.append(peak)
          objectsCreated.extend(peakDims)

  finally:
    if undo is not None:
      undo.decreaseBlocking()

  if undo is not None:
    # undo.newItem(Undo.deleteAll, self.pickNewPeaks, undoArgs=(peaks,), redoKwargs={
    #   'startPoint':startPoint, 'endPoint':endPoint, 'posLevel':posLevel, 'negLevel':negLevel,
    #   'minLinewidth':minLinewidth, 'exclusionBuffer':exclusionBuffer, 'minDropfactor':minDropfactor,
    #   'checkAllAdjacent':checkAllAdjacent,  'fitMethod':fitMethod,
    #   'excludedRegions':excludedRegions, 'excludedDiagonalDims':excludedDiagonalDims,
    #   'excludedDiagonalTransform':excludedDiagonalTransform, })

    # NB we want the peaks before the peakdims as per normal crate/delete behaviour)
    objectsCreated = peaks + objectsCreated

    undo.newItem(Undo._deleteAllApiObjects, self.root._unDelete,
                 undoArgs=(objectsCreated,),
                 redoArgs=(objectsCreated,  set(x.topObject for x in peaks)))


  return peaks

def fitExistingPeakList(self:PeakList, fitMethod:str=None):

  if fitMethod:
    # import has to be inside function because of circular imports
    from ccpnmodel.ccpncore.lib.spectrum import Peak as LibPeak
    LibPeak.fitExistingPeaks(self.sortedPeaks(), fitMethod)
