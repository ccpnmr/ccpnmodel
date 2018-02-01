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
__dateModified__ = "$dateModified: 2017-07-07 16:33:14 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b3 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import numpy

from ccpnmodel.ccpncore.api.ccp.nmr.Nmr import Peak as ApiPeak

from typing import Sequence

def fitExistingPeaks(peaks:Sequence[ApiPeak], fitMethod:str=None):

  if not fitMethod:
    return
 
  assert fitMethod in ('gaussian', 'lorentzian'), 'fitMethod = %s, must be one of ("gaussian", "lorentzian")' % fitMethod
  method = 0 if fitMethod == 'gaussian' else 1

  from ccpnc.peak import Peak as CPeak

  for peak in peaks:
    dataSource = peak.peakList.dataSource
    numDim = dataSource.numDim
    dataDims = dataSource.sortedDataDims()

    peakDims = peak.sortedPeakDims()

    # generate a numpy array with the position of the peak in points rounded to integers
    position = [peakDim.position - 1 for peakDim in peakDims] # API position starts at 1
    position = numpy.round(numpy.array(position))

    # generate a numpy array with the number of points per dimension
    numPoints = [peakDim.dataDim.numPoints for peakDim in peakDims]
    numPoints = numpy.array(numPoints)

    # consider for each dimension on the interval [point-2,point+3>, account for min and max
    # of each dimension
    firstArray = numpy.maximum(position-2, 0)
    lastArray = numpy.minimum(position+3, numPoints)

    # Get the data; note that arguments has to be castable to int?
    dataArray, intRegion = dataSource.getRegionData(firstArray, lastArray)
    # Cast to int for subsequent call
    firstArray = firstArray.astype('int32')
    lastArray = lastArray.astype('int32')
    peakArray = (position-firstArray).reshape((1, numDim))
    peakArray = peakArray.astype('float32')
    regionArray = numpy.array((firstArray-firstArray, lastArray-firstArray))
    try:
      result = CPeak.fitPeaks(dataArray, regionArray, peakArray, method)
      height, center, linewidth = result[0]
    except CPeak.error as e:
      logger = peak.root._logger
      if logger:
        logger.error("Aborting peak fit, Error for peak: %s:\n\n%s " % (peak, e))
      return

    position = firstArray + center

    for i, peakDim in enumerate(peakDims):
      peakDim.position = position[i] + 1 # API position starts at 1
      peakDim.lineWidth = linewidth[i]

    peak.height = dataSource.scale * height
