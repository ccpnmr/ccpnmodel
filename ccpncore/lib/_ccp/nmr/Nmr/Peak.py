"""Functions for insertion into ccp.nmr.Nmr.Peak

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
__version__ = "$Revision: 3.0.b5 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from typing import Sequence

import numpy

def assignByDimensions(self:'Peak', value:Sequence[Sequence['Resonance']]):
  """Set per-dimension assignments on peak.
  value is a list of lists (one per dimension) of resonances.
  NB only works for single-PeakContrib, one-ref-per-dimension assignments
  NB resets PeakContribs
  """
  numDim =  self.peakList.dataSource.numDim
  if len(value) != numDim:
    raise ValueError("Assignment length does not match number of peak dimensions %s: %s"
                      % (numDim, value))

  for ii, val in enumerate(value):
    if len(set(val)) != len(val):
      raise ValueError("Assignments contain duplicates in dimension %s: %s" % (ii+1, val))

  peakContribs = self.sortedPeakContribs()
  if peakContribs:
    # Clear existing assignments, keeping first peakContrib
    peakContrib = peakContribs[0]
    for xx in peakContribs[1:]:
      xx.delete()
    for peakDim in self.peakDims:
      for peakDimContrib in peakDim.peakDimContribs:
        peakDimContrib.delete()

  else:
    # No assignments. Make peakContrib
    peakContrib = self.newPeakContrib()

  peakDims = self.sortedPeakDims()
  for ii,val in enumerate(value):
    peakDim = peakDims[ii]
    for resonance in val:
      peakDim.newPeakDimContrib(resonance=resonance, peakContribs=(peakContrib,))


def assignByContributions(self:'Peak', value:Sequence[Sequence['Resonance']]):
  """Set assignments on peak.
  value is a list of lists (one per combination) of resonances.
  NB only works for single-resonance, one-ref-per-dimension assignments
  NB sets one PeakContrib per combination
  """

  peakDims = self.sortedPeakDims()
  dimensionCount = len(peakDims)
  dimResonances = []
  for ii in range(dimensionCount):
    dimResonances.append([])

  # get per-dimension resonances
  for tt in value:
    for ii,resonance in enumerate(tt):
      if resonance is not None and resonance not in dimResonances[ii]:
        dimResonances[ii].append(resonance)

  # reassign dimension resonances
  assignByDimensions(self, dimResonances)

  # Get first PeakContrib before we add new ones
  firstPeakContrib = self.findFirstPeakContrib()

  if value:
    # set PeakContribs, one per assignment tuple, skipping the first one
    for tt in value[1:]:
      ll = [peakDim.findFirstPeakDimContrib(resonance=tt[ii])
            for ii,peakDim in enumerate(peakDims)]
      self.newPeakContrib(peakDimContribs=[x for x in ll if x is not None])

    # reset PeakDimContribs for first PeakContrib
    ll = [peakDim.findFirstPeakDimContrib(resonance=value[0][ii])
          for ii,peakDim in enumerate(peakDims)]
    firstPeakContrib.peakDimContribs = [x for x in ll if x is not None]


def snapToExtremum(self:'Peak', halfBoxSearchWidth:int=2, halfBoxFitWidth:int=2, fitMethod:str='gaussian'):

  # this assumes you have a peak position

  from ccpnc.peak import Peak as CPeak

  peakList = self.peakList
  dataSource = peakList.dataSource

  peakDims = self.sortedPeakDims()
  numDim = len(peakDims)

  position = [peakDim.position for peakDim in peakDims]
  height = dataSource.getPositionValue(position)  # no -1 because function does that
  position = [peakDim.position - 1 for peakDim in peakDims]  # -1 because points start at 1 in peakDim

  plower = [int(numpy.floor(p)) for p in position]
  pupper = [int(numpy.ceil(p)) for p in position]

  startPoint = numpy.array([max(plower[i] - halfBoxSearchWidth, 0) for i in range(numDim)])
  endPoint = numpy.array([min(pupper[i] + halfBoxSearchWidth + 1, peakDims[i].dataDim.numPoints) for i in range(numDim)])
  numPoint = endPoint - startPoint

  dataArray, intRegion = dataSource.getRegionData(startPoint, endPoint)

  scaledHeight = 0.5 * height  # this is so that have sensible pos/negLevel
  if height > 0:
    doPos = True
    doNeg = False
    posLevel = scaledHeight
    negLevel = 0 # arbitrary
  else:
    doPos = False
    doNeg = True
    posLevel = 0 # arbitrary
    negLevel = scaledHeight

  exclusionBuffer = [1] * numDim

  nonAdj = 0
  minDropfactor = 0.1
  minLinewidth = [0.0] * numDim

  excludedRegionsList = []
  excludedDiagonalDimsList = []
  excludedDiagonalTransformList = []

  peakPoints = CPeak.findPeaks(dataArray, doNeg, doPos,
                               negLevel, posLevel, exclusionBuffer,
                               nonAdj, minDropfactor, minLinewidth,
                               excludedRegionsList, excludedDiagonalDimsList, excludedDiagonalTransformList)

  if len(peakPoints) == 1:
    peakPoint, height = peakPoints[0]
    for i, peakDim in enumerate(peakDims):
      peakDim.position = float(startPoint[i] + peakPoint[i] + 1)  # +1 because points start at 1 in peakDim
        # float() because otherwise get numpy float which API does not allow

    self.fitPositionHeightLineWidths(halfBoxFitWidth, fitMethod)

def fitPositionHeightLineWidths(self:'Peak', halfBoxWidth:int=2, fitMethod:str='gaussian'):

  # this assumes you have a peak position

  from ccpnc.peak import Peak as CPeak

  peakList = self.peakList
  dataSource = peakList.dataSource

  peakDims = self.sortedPeakDims()
  numDim = len(peakDims)
  position = [peakDim.position - 1 for peakDim in peakDims]  # -1 because points start at 1 in peakDim

  plower = [int(numpy.floor(p)) for p in position]
  pupper = [int(numpy.ceil(p)) for p in position]

  startPoint = numpy.array([max(plower[i] - halfBoxWidth, 0) for i in range(numDim)])
  endPoint = numpy.array([min(pupper[i] + halfBoxWidth + 1, peakDims[i].dataDim.numPoints) for i in range(numDim)])
  numPoint = endPoint - startPoint

  dataArray, intRegion = dataSource.getRegionData(startPoint, endPoint)

  peakPoint = numpy.array(position) - startPoint
  firstArray = numpy.maximum(peakPoint - halfBoxWidth, 0)
  lastArray = numpy.minimum(peakPoint + halfBoxWidth + 1, numPoint)
  peakArray = numpy.array(peakPoint).reshape((1, numDim))
  peakArray = peakArray.astype('float32')
  firstArray = firstArray.astype('int32')
  lastArray = lastArray.astype('int32')
  regionArray = numpy.array((firstArray, lastArray))

  method = 0 if fitMethod == 'gaussian' else 1

  try:
    result = CPeak.fitPeaks(dataArray, regionArray, peakArray, method)
    height, center, linewidth = result[0]
  except:
    return

  position = center + startPoint

  dataDims = dataSource.sortedDataDims()

  for i, peakDim in enumerate(peakDims):
    dataDim = dataDims[i]

    if dataDim.className == 'FreqDataDim':
      dataDimRef = dataDim.primaryDataDimRef
    else:
      dataDimRef = None

    if dataDimRef:
      peakDim.numAliasing = int(divmod(position[i], dataDim.numPointsOrig)[0])
      peakDim.position = float(
        position[i] + 1 - peakDim.numAliasing * dataDim.numPointsOrig)  # API position starts at 1

    else:
      peakDim.position = float(position[i] + 1)

    if linewidth[i] is not None:
      peakDim.lineWidth = dataDim.valuePerPoint * linewidth[i]  # conversion from points to Hz

  self.height = dataSource.scale * height

# NBNB unit operations needed:
#
# clearAssignments
# _setToPerDimension
# _setToPerAssignment
# addAssignment
# assignDimension
