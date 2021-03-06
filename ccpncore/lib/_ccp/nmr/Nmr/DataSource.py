"""Functions for insertion into ccp.nmr.Nmr.DataSource

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
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import array
import numpy
import os
import sys
from typing import Sequence, Tuple
from ccpnmodel.ccpncore.lib.spectrum import Spectrum as spectrumLib
from ccpnmodel.ccpncore.lib.spectrum.Integral import Integral as spInt
from ccpnmodel.ccpncore.lib.Io import Formats

# 20190514: ED
from ccpn.util.Logging import getLogger


# Additional functions for ccp.nmr.Nmr.DataSource
#
# NB All functions must have a mandatory DataSource as the first parameter
# so they can be used as DataSource methods

def getDimCodes(self: 'DataSource'):
    """ Get dimcode of form hx1, hx2, x1, x2, where the x's are directly bound to def save
    the corresponding H. suffix '1' is given to the acquisition proton dimension.
    Dimensions not matching the specs are given code None
    """
    isotopeCodes = getIsotopeCodesList(self)

    acqExpDim = self.experiment.getAcqExpDim()
    dataDims = self.sortedDataDims()
    dimCodes = [None] * self.numDim
    for ii, dataDim in enumerate(dataDims):
        if isotopeCodes[ii] == '1H':
            if dataDim.expDim is acqExpDim:
                dimCodes[ii] = 'hx1'
                xCode = 'x1'
            else:
                dimCodes[ii] = 'hx2'
                xCode = 'x2'
            for tt in getOnebondDataDims(self):
                if tt[0] is dataDim:
                    xDim = tt[1]
                    dimCodes[dataDims.index(xDim)] = xCode
                    break
    #
    return dimCodes


def getXEasyDimCodes(self: 'DataSource'):
    """ Get Xeasy-style dimCodes in dim order for data Source
    For use in FormatConverter
    """
    #
    # Get isotopeCode info
    #
    isotopeCodes = getIsotopeCodesList(self)
    dimCodes = getDimCodes(self)
    reverse = bool('x2' in dimCodes and not 'x1' in dimCodes)
    found = set()
    for ii, code in enumerate(dimCodes):
        elementType = isotopeCodes[ii][-1]
        if code and (('2' in code) != reverse):
            dimCodes[ii] = elementType.lower()
        else:
            dimCodes[ii] = elementType

    #
    # Fix in homonuclear 2D case...
    #
    #firstDimCode = dimCodes[0]
    #if dimCodes.count(firstDimCode) == len(dimCodes):
    #  if firstDimCode == firstDimCode.lower():
    #    dimCodes[0] = firstDimCode.upper()
    #
    # and generally distinguish duplicates. Rasmus Fogh 15/6/12
    foundset = set()
    for ii, ss in enumerate(dimCodes):
        if ss in foundset:
            ss = ss.upper()
        if ss in foundset:
            ss = ss.lower()
        dimCodes[ii] = ss
        foundset.add(ss)
    #
    return dimCodes


# NB renamed from getSpectrumIsotopes getIsotopeCodesList
#def getSpectrumIsotopes(dataSource):
def getIsotopeCodesList(self: 'DataSource'):
    """
    Give isotope code strings pertaining to the dimensions of a given NMR dataSource

    .. describe:: Input

    Nmr.DataSource

    .. describe:: Output

    List of Strings (comma-joined Nmr.ExpDimRef.IsotopeCodes)
    """

    isotopes = []
    for dataDim in self.sortedDataDims():
        isotopeCodes = list(dataDim.getIsotopeCodes())
        isotopes.append(','.join(sorted(isotopeCodes)) or None)

    return isotopes


def getOnebondDataDims(self: 'DataSource'):
    """
    Get pairs of dataSource data dimensions that are connected by onebond transfers

    .. describe:: Input

    Nmr.DataSource

    .. describe:: Output

    List of 2-List of Nmr.DataDims
    """

    dataDims = []
    expDimRefs = self.experiment.getOnebondExpDimRefs()

    for expDimRef0, expDimRef1 in expDimRefs:
        dataDim0 = self.findFirstDataDim(expDim=expDimRef0.expDim)
        dataDim1 = self.findFirstDataDim(expDim=expDimRef1.expDim)

        if dataDim0 and dataDim1:
            dataDims.append([dataDim0, dataDim1])

    return dataDims


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
    ndim = len(cumul)
    array = ndim * [0]
    for i in range(ndim - 1, -1, -1):
        c = cumul[i]
        array[i], index = divmod(index, c)

    return numpy.array(array)


def getPlaneData(self: 'DataSource', position=None, xDim: int = 1, yDim: int = 2):
    """ Get plane data through position in dimensions xDim, yDim
        Returns 2D float32 NumPy array in order (y, x)
        Returns None if numDim < 2 or if there is no dataStore
        Positions are 1-based """

    # Import moved here to avoid circular import problems
    from ccpnmodel.ccpncore.lib.spectrum.formats import Hdf5, NmrPipe

    numDim = self.numDim
    if numDim < 2:
        return None

    dataStore = self.dataStore
    if not dataStore:
        return None

    if dataStore.fileType == 'NMRPipe':  # data is not blocked but multi-file in general
        if not hasattr(dataStore, 'template'):
            dataStore.template = NmrPipe._guessFileTemplate(self)
        if dataStore.template:
            return NmrPipe.getPlaneData(self, position, xDim, yDim)

    if dataStore.fileType == 'Hdf5':
        return Hdf5.getPlaneData(self, position, xDim, yDim)

    assert numDim == 2 or (position and len(position) == numDim), 'numDim = %d, position = %s' % (numDim, position)
    assert xDim != yDim, 'xDim = yDim = %d' % xDim
    assert 1 <= xDim <= numDim, 'xDim = %d' % xDim
    assert 1 <= yDim <= numDim, 'yDim = %d' % yDim

    xDim -= 1  # make 0 based instead of 1 based
    yDim -= 1

    if not position:
        position = numDim * [1]

    dataDims = self.sortedDataDims()
    numPoints = [dataDim.numPoints for dataDim in dataDims]
    xPoints = numPoints[xDim]
    yPoints = numPoints[yDim]

    for dim in range(numDim):
        point = position[dim] - 1
        if point >= numPoints[dim]:
            raise ValueError('Plane index %d in dimension %d not within dataSource bounds (%d)' % (point, dim + 1, numPoints[dim]))
        if point < 0:
            raise ValueError('Plane index %d in dimension %d less than 0' % (point, dim + 1))

    blockSizes = dataStore.blockSizes
    blockSize, cumulativeBlockSizes = _cumulativeArray(blockSizes)
    wordSize = dataStore.nByte
    isBigEndian = dataStore.isBigEndian
    isFloatData = dataStore.numberType == 'float'
    headerSize = dataStore.headerSize
    format = dataStore.fileType
    #blockHeaderSize = dataStore.blockHeaderSize  # TBD: take this into account
    blocks = [1 + (numPoints[dim] - 1) // blockSizes[dim] for dim in range(numDim)]
    numBlocks, cumulativeBlocks = _cumulativeArray(blocks)
    dtype = '%s%s%s' % (isBigEndian and '>' or '<', isFloatData and 'f' or 'i', wordSize)

    xblockSize = blockSizes[xDim]
    yblockSize = blockSizes[yDim]

    xblocks = 1 + (xPoints - 1) // xblockSize
    yblocks = 1 + (yPoints - 1) // yblockSize

    blockCoords = [(position[dim] - 1) // blockSizes[dim] for dim in range(numDim)]
    blockSlice = numDim * [0]

    for dim in range(numDim):
        if dim not in (xDim, yDim):
            p = (position[dim] - 1) % blockSizes[dim]
            blockSlice[numDim - dim - 1] = slice(p, p + 1)

    blockSizes = blockSizes[::-1]  # reverse (dim ordering backwards)

    data = numpy.zeros((yPoints, xPoints), dtype=numpy.float32)

    fileName = dataStore.fullPath
    if not os.path.exists(fileName):
        self.root._logger.warning("File does not exist: %s" % fileName)
        return data

    fp = open(fileName, 'rb')

    for xblock in range(xblocks):

        blockCoords[xDim] = xblock
        xlower = xblock * xblockSize
        xupper = min(xlower + xblockSize, xPoints)
        blockSlice[numDim - xDim - 1] = slice(xupper - xlower)

        for yblock in range(yblocks):

            blockCoords[yDim] = yblock
            ylower = yblock * yblockSize
            yupper = min(ylower + yblockSize, yPoints)
            blockSlice[numDim - yDim - 1] = slice(yupper - ylower)

            ind = sum(x[0] * x[1] for x in zip(blockCoords, cumulativeBlocks))
            offset = wordSize * (blockSize * ind) + headerSize
            fp.seek(offset, 0)
            # blockData = numpy.fromfile(file=fp, dtype=dtype, count=blockSize).reshape(blockSizes)  # data is in reverse order: e.g. z,y,x not x,y,z

            try:
                blockDataPre = numpy.fromfile(file=fp, dtype=dtype, count=blockSize)
                blockData = blockDataPre.reshape(blockSizes)  # data is in reverse order: e.g. z,y,x not x,y,z

                if blockData.dtype != numpy.float32:
                    blockData = numpy.array(blockData, numpy.float32)

                blockPlane = blockData[tuple(blockSlice)]

                if xDim > yDim:
                    blockPlane = blockPlane.transpose()

                #blockPlane = blockPlane.squeeze()  # removes 1, but sometimes block size is indeed 1 so do reshape instead
                data[ylower:yupper, xlower:xupper] = blockPlane.reshape((yupper - ylower, xupper - xlower))

            except Exception as es:
                getLogger().warning('getPlaneData: error loading last blockData')

    fp.close()

    # data *= self.scale

    return data


def getSliceData(self: 'DataSource', position=None, sliceDim: int = 1):
    # Get an actual array of data points,
    # spanning blocks as required
    # returns 1D array

    # Import moved here to avoid circular import problems
    from ccpnmodel.ccpncore.lib.spectrum.formats import Hdf5, NmrPipe

    numDim = self.numDim
    if numDim < 1:
        return None

    dataStore = self.dataStore
    if not dataStore:
        return None

    fileName = dataStore.fullPath
    if not os.path.exists(fileName):
        self.root._logger.warning("File does not exist: %s" % fileName)
        return None

    if dataStore.fileType == 'NMRPipe':  # data is not blocked but multi-file in general
        if not hasattr(dataStore, 'template'):
            dataStore.template = NmrPipe._guessFileTemplate(self)
        if dataStore.template:
            return NmrPipe.getSliceData(self, position, sliceDim)

    if dataStore.fileType == 'Hdf5':
        return Hdf5.getSliceData(self, position, sliceDim)

    sliceDim -= 1  # make 0 based instead of 1 based

    if not position:
        position = numDim * [1]
    dataDims = self.sortedDataDims()
    numPoints = [dataDim.numPoints for dataDim in dataDims]
    slicePoints = numPoints[sliceDim]

    data = numpy.zeros((slicePoints,), dtype=numpy.float32)
    for dim in range(numDim):
        point = position[dim] - 1
        if point >= numPoints[dim]:
            return None
            raise ValueError('Slice index %d not within dataSource bounds' % point)
        if point < 0:
            return None
            raise ValueError('Slice index %d less than 0' % point)

    blockSizes = dataStore.blockSizes
    blockSize, cumulativeBlockSizes = _cumulativeArray(blockSizes)
    wordSize = dataStore.nByte
    isBigEndian = dataStore.isBigEndian
    isFloatData = dataStore.numberType == 'float'
    headerSize = dataStore.headerSize
    format = dataStore.fileType
    #blockHeaderSize = dataStore.blockHeaderSize  # TBD: take this into account
    blocks = [1 + (numPoints[dim] - 1) // blockSizes[dim] for dim in range(numDim)]
    numBlocks, cumulativeBlocks = _cumulativeArray(blocks)
    dtype = '%s%s%s' % (isBigEndian and '>' or '<', isFloatData and 'f' or 'i', wordSize)

    sliceBlockSize = blockSizes[sliceDim]
    sliceBlocks = 1 + (slicePoints - 1) // sliceBlockSize
    blockCoords = [(position[dim] - 1) // blockSizes[dim] for dim in range(numDim)]
    blockSlice = numDim * [0]

    for dim in range(numDim):
        if dim != sliceDim:
            p = (position[dim] - 1) % blockSizes[dim]
            blockSlice[numDim - dim - 1] = slice(p, p + 1)

    blockSizes = blockSizes[::-1]  # reverse (dim ordering backwards)

    fp = open(fileName, 'rb')

    for sliceBlock in range(sliceBlocks):
        blockCoords[sliceDim] = sliceBlock
        sliceLower = sliceBlock * sliceBlockSize
        sliceUpper = min(sliceLower + sliceBlockSize, slicePoints)
        blockSlice[numDim - sliceDim - 1] = slice(sliceUpper - sliceLower)
        ind = sum(x[0] * x[1] for x in zip(blockCoords, cumulativeBlocks))
        offset = wordSize * (blockSize * ind) + headerSize
        fp.seek(offset, 0)
        # blockData = numpy.fromfile(file=fp, dtype=dtype, count=blockSize).reshape(blockSizes)  # data is in reverse order: e.g. z,y,x not x,y,z

        try:
            blockDataPre = numpy.fromfile(file=fp, dtype=dtype, count=blockSize)
            blockData = blockDataPre.reshape(blockSizes)  # data is in reverse order: e.g. z,y,x not x,y,z

            if blockData.dtype != numpy.float32:
                blockData = numpy.array(blockData, numpy.float32)
            data[sliceLower:sliceUpper] = blockData[blockSlice].squeeze()

        except Exception as es:
            getLogger().warning('getSliceData: error loading last blockData')

    fp.close()

    # data *= self.scale

    return data


def get1dSpectrumData(self: 'DataSource'):
    """Get position,scaledData numpy array for 1D spectrum"""

    dataDimRef = self.findFirstDataDim().findFirstDataDimRef()
    firstPoint = dataDimRef.pointToValue(1)
    pointCount = self.findFirstDataDim().numPoints
    lastPoint = dataDimRef.pointToValue(1 + pointCount)  # sw goes from 1 to n+1
    pointSpacing = (lastPoint - firstPoint) / pointCount
    position = numpy.array([firstPoint + n * pointSpacing for n in range(pointCount)], numpy.float32)
    sliceData = self.getSliceData()
    scaledData = sliceData  # *self.scale  (do not need this any more since getSliceData() does this)
    spectrumData = numpy.array([position, scaledData], numpy.float32)
    return numpy.array(spectrumData, numpy.float32)

    # NB Points start at 1; other changes are rationalisations.
    # dataDim = self.findFirstDataDim()
    # pointCount = dataDim.numPoints
    # dataDimRef = dataDim.primaryDataDimRef
    # firstPoint = dataDimRef.pointToValue(1)
    # pointSpacing = dataDimRef.valuePerPoint
    #
    # position = numpy.array([firstPoint + n*pointSpacing for n in range(pointCount)],numpy.float32)
    # scaledData = self.getSliceData()*self.scale
    # return numpy.array([position,scaledData], numpy.float32)


def getPositionValue(self: 'DataSource', position: Sequence[float]):
    """weighted average of values at grid points nearest position"""

    position = list(position)
    for i in range(len(position)):
        position[i] -= 1

    dataDims = self.sortedDataDims()
    numPoints = [dataDim.numPoints for dataDim in dataDims]
    startPoint = numpy.array([int(numpy.floor(p % numPoints[i])) for i, p in enumerate(position)])
    endPoint = startPoint + 2  # at top will only end up with +1 in effect, so doesn't wrap around

    data = getRegionData(self, startPoint, endPoint)
    if data:
        data = data[0]

        if data is not None and data.size != 0:
            n, cumShape = _cumulativeArray(data.shape)
            value = 0
            for i in range(n):  # generally 2^numDim (except with edge effect at top)
                array = _arrayOfIndex(i, cumShape)
                m = 1.0
                for j in range(len(array)):  # numDim
                    if data.shape[j] == 2:
                        k = self.numDim - j - 1
                        if array[j] == 0:
                            m *= 1 - position[k] + startPoint[k]
                        else:
                            m *= position[k] - startPoint[k]
                value += m * data[tuple(array)]

            return value


def getRegionData(self: 'DataSource', startPoint: Sequence[float], endPoint: Sequence[float]):
    # NBNB TBD BROKEN!!

    # Import moved here to avoid circular import problems
    from ccpnmodel.ccpncore.lib.spectrum.formats import Hdf5, NmrPipe

    dataStore = self.dataStore
    if not dataStore:
        return None

    numDim = self.numDim
    assert len(startPoint) == numDim, 'len(startPoint) = %d, numDim=%d' % (len(startPoint), numDim)
    assert len(endPoint) == numDim, 'len(endPoint) = %d, numDim=%d' % (len(endPoint), numDim)

    dataDims = self.sortedDataDims()
    numPoints = [dataDim.numPoints for dataDim in dataDims]
    startPoint = list(startPoint)
    endPoint = list(endPoint)
    for dim in range(numDim):
        start = min(startPoint[dim], endPoint[dim])
        end = max(startPoint[dim], endPoint[dim])

        start = min(max(0, int(start)), numPoints[dim])
        end = min(max(0, int(end)), numPoints[dim])

        startPoint[dim] = start
        endPoint[dim] = end

    intRegion = (startPoint, endPoint)

    if dataStore.fileType == 'NMRPipe':  # data is not blocked but multi-file in general
        if not hasattr(dataStore, 'template'):
            dataStore.template = NmrPipe._guessFileTemplate(self)
        if dataStore.template:
            return NmrPipe.getRegionData(self, startPoint, endPoint), intRegion

    if dataStore.fileType == 'Hdf5':
        return Hdf5.getRegionData(self, startPoint, endPoint), intRegion

    blockSizes = dataStore.blockSizes

    blockRanges = []
    rangeSizes = []
    regionSizes = []

    n = 1
    for dim in range(numDim):
        startBlockCoord = int((startPoint[dim]) // blockSizes[dim])
        endBlockCoord = 1 + int((endPoint[dim] - 1) // blockSizes[dim])
        blockRange = range(startBlockCoord, endBlockCoord)
        blockRanges.append(blockRange)
        m = len(blockRange)
        rangeSizes.append(m)
        regionSizes.append(int(endPoint[dim] - startPoint[dim]))
        n *= m

    blockCoords = [None] * n
    for i in range(n):
        blockCoord = []

        j = i
        for dim in range(numDim):
            index = j % rangeSizes[dim]
            blockCoord.append(blockRanges[dim][index])
            j = j // rangeSizes[dim]

        blockCoords[i] = tuple(blockCoord)

    data = numpy.zeros(regionSizes, dtype=numpy.float32)

    dataSlice = [0] * numDim
    blockSlice = [0] * numDim

    blockSize, cumulativeBlockSizes = _cumulativeArray(blockSizes)
    wordSize = dataStore.nByte
    isBigEndian = dataStore.isBigEndian
    isFloatData = dataStore.numberType == 'float'
    headerSize = dataStore.headerSize
    format = dataStore.fileType
    blocks = [1 + (numPoints[dim] - 1) // blockSizes[dim] for dim in range(numDim)]
    numBlocks, cumulativeBlocks = _cumulativeArray(blocks)
    dtype = '%s%s%s' % (isBigEndian and '>' or '<', isFloatData and 'f' or 'i', wordSize)

    blockSizesRev = blockSizes[::-1]  # reverse (dim ordering backwards)

    fileName = dataStore.fullPath
    if not os.path.exists(fileName):
        self.root._logger.warning("File does not exist: %s" % fileName)
        return data
    fp = open(fileName, 'rb')

    for blockCoord in blockCoords:

        for dim in range(numDim):
            first = blockCoord[dim] * blockSizes[dim]
            next = first + blockSizes[dim]
            offset = startPoint[dim]

            if first < offset:
                blockLow = offset - first
            else:
                blockLow = 0

            if next > endPoint[dim]:
                blockHigh = blockSizes[dim] + (endPoint[dim] - next)
            else:
                blockHigh = blockSizes[dim]

            dataLow = first - offset + blockLow
            dataHigh = dataLow + (blockHigh - blockLow)

            dataSlice[dim] = slice(dataLow, dataHigh)
            blockSlice[numDim - dim - 1] = slice(blockLow, blockHigh)

        ind = sum(x[0] * x[1] for x in zip(blockCoord, cumulativeBlocks))
        offset = wordSize * (blockSize * ind) + headerSize
        fp.seek(offset, 0)
        # blockData = numpy.fromfile(file=fp, dtype=dtype, count=blockSize).reshape(blockSizesRev)  # data is in reverse order: e.g. z,y,x not x,y,z

        try:
            blockDataPre = numpy.fromfile(file=fp, dtype=dtype, count=blockSize)
            blockData = blockDataPre.reshape(blockSizesRev)

            if blockData.dtype != numpy.float32:
                blockData = numpy.array(blockData, numpy.float32)

            data[dataSlice] = blockData[blockSlice].T

        except Exception as es:
            getLogger().warning('getRegionData: error loading last blockData')


    fp.close()

    # data *= self.scale

    return data.T, intRegion


def automaticIntegration(self: 'DataSource', spectralData, regions):
    #
    numDim = self.numDim
    if numDim != 1:
        return
    dataStore = self.dataStore
    if not dataStore:
        return None
    # dataSource.valueArray = [[]] * numDim
    # if len(valueArray[xDim]) != 0:
    #   valueArray = valueArray[xDim]
    valueArray = self.valueArray = spectralData
    noise = estimateNoise(self)
    level = noise * 6
    # if len(self.peakList) > 0:
    #   integrals = self.getPeakIntegralRegions(valueArray[1, :], noise, level)
    # else:
    integrals = spInt.getIntegralRegions(spectralData[1, :], noise, level)
    spInt.setIntegrals(self, integrals)

    # NBNB FIXME the use of spInt is BROKEN. It is imported as a class, never instantiated,
    # and methods are called on it as if it was an object.

    #
    for integral in self.integrals:
        integral.calculateBias(spectralData[1, :], noise)
        spInt.calculateIntegralValues(integral.points, spectralData[1, :], integral.bias * -1, integral.slope)

    if len(self.integrals) > 0:
        self.integralFactor = 1 / self.integrals[0].points[-1][0]
    else:
        self.integralFactor = None
    for integral in self.integrals:
        integral.calculateVolume()

    #
    # for a in dataSource.integrals:
    #   # print(dataSource.integralFactor)
    #
    return self.integrals


# def setIntegrals(dataSource, dim, values, factor = 1.0):
#
#     self.integrals = []
#     # append = self.integrals.append

def estimateNoise(self: 'DataSource') -> float:
    if self.noiseLevel:
        return self.noiseLevel

    if self.numDim > 1:
        planeData = getPlaneData(self, [1] * self.numDim, 1, 2)
        if planeData is None:
            value = 0.0
        else:
            value = 1.1 * numpy.std(planeData.flatten())  # multiplier a guess
    else:

        if hasattr(self, 'valueArray') and len(self.valueArray) != 0:
            sliceData = self.valueArray
        else:
            self.valueArray = sliceData = getSliceData(self)
        # print(sliceData)
        # print(sliceData[1])
        sliceDataStd = numpy.std(sliceData)
        sliceData = numpy.array(sliceData, numpy.float32)
        # Clip the data to remove outliers
        sliceData = sliceData.clip(-sliceDataStd, sliceDataStd)

        value = 1.1 * numpy.std(sliceData)  # multiplier a guess

    #value *= self.scale

    self.noiseLevel = float(value)

    return self.noiseLevel  # Qt can't serialise numpy float types


def getDefaultColours(self: 'DataSource') -> Tuple[str, str]:
    """Get default positivecontourcolour, negativecontourcolour for Spectrum
    (calculated by hashing spectrum properties to avoid always getting the same colours"""

    return ('#FF0000', '#FF0000')


def _saveNmrPipe2DHeader(self: 'DataSource', fp: 'file', xDim: int = 1, yDim: int = 2):
    xDim -= 1
    yDim -= 1

    ndim_index = 9
    npts_index = (99, 219, 15, 32)
    complex_index = (55, 56, 51, 54)
    order_index = (24, 25, 26, 27)
    sw_index = (229, 100, 11, 29)
    sf_index = (218, 119, 10, 28)
    origin_index = (249, 101, 12, 30)
    nuc_index = (18, 16, 20, 22)

    value_index = 199

    head = 512

    x = array.array('B')  # unsigned char
    for i in range(8):
        x.append(0)

    bytes = [0x40, 0x16, 0x14, 0x7b]
    if sys.byteorder != 'big':
        bytes.reverse()

    for byte in bytes:
        x.append(byte)

    y = array.array('f')  # float
    for n in range(head):
        y.append(0)

    y[ndim_index] = 2

    for n in range(2):
        y[order_index[n]] = n + 1

    dataDims = self.sortedDataDims()
    dataDims2D = (dataDims[xDim], dataDims[yDim])
    for n, dataDim in enumerate(dataDims2D):
        dataDimRef = dataDim.getPrimaryDataDimRef()  # will fail if a sampled data set
        expDimRef = dataDimRef.expDimRef
        y[npts_index[n]] = dataDim.numPoints
        y[complex_index[n]] = 1  # real
        y[sf_index[n]] = expDimRef.sf
        # note that spectralWidth is in ppm and NmrPipe wants it in Hz, so multiply by sf
        y[sw_index[n]] = dataDimRef.spectralWidth * expDimRef.sf
        y[origin_index[n]] = expDimRef.sf * (
                    dataDimRef.refValue + dataDimRef.refPoint * dataDimRef.spectralWidth / dataDim.numPoints - dataDimRef.spectralWidth)
        if expDimRef.isotopeCodes:
            isotopeCode = expDimRef.isotopeCodes[0][:4]
            isotopeCode += (4 - len(isotopeCode)) * ' '
            z = array.array('B')  # unsigned char
            # does this need swapping if not big endian??
            z.fromstring(isotopeCode)
            w = array.array('f')
            w.frombytes(z)
            y[nuc_index[n]] = w[0]

    x.tofile(fp)
    y[3:].tofile(fp)


# GWV 5/10/18: Replaced by routines in Core.Lib.SpectrumLib.py
#
# def projectedPlaneData(self:'DataSource', xDim:int=1, yDim:int=2, method:str='max', noise=None):
#
#   numDim = self.numDim
#
#   if numDim != 3:
#     raise Exception('Can only project from 3D currently')
#
#   if not (1 <= xDim <= numDim):
#     raise Exception('For projection, xDim = %d, must be in range 1 to $d' % (xDim, numDim))
#
#   if not (1 <= yDim <= numDim):
#     raise Exception('For projection, yDim = %d, must be in range 1 to $d' % (yDim, numDim))
#
#   if xDim == yDim:
#     raise Exception('For projection, must have xDim != yDim')
#
#   METHODS = ('max', 'max above noise', 'min', 'min below noise', 'sum', 'sum above noise')
#   if method not in METHODS:
#     raise Exception('For projection, method must be one of %s' % (METHODS,))
#
#   if method.endswith('noise') and noise is None:
#     raise Exception('For projection method "%s", noise parameter must be defined' % (method,))
#
#   dims = set(range(1,numDim+1))
#   dims.remove(xDim)
#   dims.remove(yDim)
#   zDim = dims.pop()
#
#   position = [1] * numDim
#   projectedData = None
#   dataDims = self.sortedDataDims()
#   numZPoints = dataDims[zDim-1].numPoints
#
#   for zPos in range(1,numZPoints+1):
#     position[zDim-1] = zPos
#     planeData = getPlaneData(self, position, xDim, yDim)
#     if method == 'sum above noise' or method == 'max above noise':
#       lowIndices = planeData < noise
#       planeData[lowIndices] = 0
#     elif method == 'min below noise':
#       lowIndices = planeData > -noise
#       planeData[lowIndices] = 0
#
#     if projectedData is None:
#       projectedData = planeData
#     else:
#       if method == 'max':
#         projectedData = numpy.maximum(projectedData, planeData)
#       elif method == 'min':
#         projectedData = numpy.minimum(projectedData, planeData)
#       else:
#         projectedData += planeData
#
#   return projectedData
#
# def projectedToFile(self:'DataSource', path:str, xDim:int=1, yDim:int=2, method:str='max', noise=None, format:str=Formats.NMRPIPE):
#
#   if format != Formats.NMRPIPE:
#     raise Exception('Can only project to %s format currently' % Formats.NMRPIPE)
#
#   projectedData = projectedPlaneData(self, xDim, yDim, method=method, noise=noise)
#
#   with open(path, 'wb') as fp:
#     _saveNmrPipe2DHeader(self, fp, xDim, yDim)
#     projectedData.tofile(fp)


def addDataStore(self: 'DataSource', spectrumPath, **params):
    """Create and set DataSource.dataStore.
    The values of params are given by the 'tags' tuple, below"""

    dirName, fileName = os.path.split(spectrumPath)
    dataUrl = self.root.fetchDataUrl(dirName)
    tags = ('numPoints', 'blockSizes', 'isBigEndian', 'numberType', 'headerSize', 'nByte',
            'fileType', 'complexStoredBy')
    attributeDict = dict((x, params.get(x)) for x in tags)

    blockMatrix = spectrumLib.createBlockedMatrix(dataUrl, spectrumPath, **attributeDict)
    self.dataStore = blockMatrix
