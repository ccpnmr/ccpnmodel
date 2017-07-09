"""Utilities for dealing with blocked data files

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
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

# NBNB TBD must be replaced with numpy (array is deprecated from Python 3.4
import array as array

# def cumulativeArray(array):
#   """ get total size and strides array.
#   NB assumes fastest moving index first
#   """
#
#   ndim = len(array)
#   cumul = ndim * [0]
#   n = 1
#   for i,size in enumerate(array):
#     cumul[i] = n
#     n = n * size
#
#   return (n, cumul)
#
# def arrayOfIndex(index, cumul):
#   """ Get from 1D index to point address tuple
#   NB assumes fastest moving index first
#   """
#
#   ndim = len(cumul)
#   array = ndim * [0]
#   # 26 May 2011: below uses cumul in backwards fashion so breaks Analysis usage
#   # go back to previous (slower) code for now
#   """
#   for i,c in enumerate(cumul):
#     array[i], index = divmod(index, c)
# """
#   for i in range(ndim-1, -1, -1):
#     c = cumul[i]
#     array[i], index = divmod(index, c)
#     # futureproofed ('/' behaviour to chagne
#     #array[i] = index / c
#     #index = index % c
#
#   #array.reverse()
#
#   #return tuple(reversed(array))
#   return tuple(array)
#
# def indexOfArray(array, cumul):
#   """ Get from point address tuple to 1D index
#   """
#
#   return sum(x[0]*x[1] for x in zip(array, cumul))
#
#   #index = 0
#   #for i in range(len(array)):
#   #  index += array[i] * cumul[i]
#   #
#   #return index
#
# def determineShape(value):
#   """
#   Get shape from matrix of nested sequences. A sequence is defined as
#   anything that works with len(value) and value[0] and is not a string or dict.
#   From Python 2.6 we could use abstract base classes
#   # NB, uses 0th element to get lengths
#   """
#   result = []
#   while not isinstance(value, basestring) and not hasattr(value, 'keys'):
#     try:
#       length = len(value)
#       value = value[0]
#       result.append(length)
#     except TypeError:
#       break
#   #
#   return result
#
# def strides(shape):
#   """ convert shape array to stride array.
#   NB assumes slowest varying index *first*
#   NB equivalent to cumulativeArray function
#   """
#   ndim = len(shape)
#   result = ndim * [0]
#   n = 1
#   for i,size in enumerate(reversed(shape)):
#     result[i] = n
#     n = n * size
#
#   result.reverse()
#   #
#   return result
#
# def flatten(value, ndim=None):
#   """
#   Reduce nested sequence to a single list in correct traversal order
#   # NB the sequence must be nested to at least ndim depth everywhere,
#   but need not be regular
#   """
#
#   if ndim is None:
#     shape = determineShape(value)
#     ndim = len(shape)
#
#   if ndim <= 1:
#     result = list(value)
#
#   else:
#     for dummy in range(ndim-1):
#       result = list(value[0])
#       for seq in value[1:]:
#         result.extend(seq)
#       value = result
#   #
#   return result

  

def determineBlockSizes(npoints, totalBlockSize=4096):

  ndim = len(npoints)

  if (ndim < 1):
    return []
  elif (ndim == 1):
    return [ totalBlockSize ]

  n = 1 << ndim;

  if totalBlockSize < n: # unlikely
    blockSizes = ndim * [1]
    n = 1
  else:
    blockSizes = ndim * [2]
 
  while n < totalBlockSize:
    i_max = r_max = 0
    for i in range(ndim):
      r = float(npoints[i]) / blockSizes[i]
      if (r > r_max):
        i_max = i
        r_max = r
    blockSizes[i_max] *= 2
    n *= 2

  return blockSizes
#
# def writeBlockData(file, data, npoints, blockSizes = None):
#
#   ndim = len(npoints)
#
#   (npts, cumulPoints) = cumulativeArray(npoints)
#
#   if (npts != len(data)):
#     raise Exception('npoints = %s so should have len(data) = %d but it is %d' \
#                     % (npoints, npts, len(data)))
#
#   if (not blockSizes):
#     blockSizes = determineBlockSizes(npoints)
#
#   if (len(blockSizes) != ndim):
#     raise Exception('len(npoints) = %s but len(blockSizes) = %d' \
#                     % (ndim, len(blockSizes)))
#
#   (blkSize, cumulBlockSize) = cumulativeArray(blockSizes)
#
#   nblocks = [ 1 + (npoints[i] - 1)/blockSizes[i] for i in range(ndim) ]
#   (nblks, cumulBlocks) = cumulativeArray(nblocks)
#
#   fp = open(file, 'wb')
#
#   x = array.array('f')
#   npts = nblks * blkSize
#   for n in range(npts):
#     blk = n / blkSize
#     pnt = n % blkSize
#     y = arrayOfIndex(blk, cumulBlocks)
#     z = arrayOfIndex(pnt, cumulBlockSize)
#     point = [ blockSizes[i]*y[i] + z[i] for i in range(ndim) ]
#     for i in range(ndim):
#       if (point[i] >= npoints[i]):
#         d = 0
#         break
#     else:
#       ind = indexOfArray(point, cumulPoints)
#       d = data[ind]
#     x.append(d)
#
#   fp.write(x.tostring())
#   fp.close()
#
# if (__name__ == '__main__'):
#
#   file = 'test.bin'
#   npoints = [ 64, 32 ]
#   n = npoints[0] * npoints[1]
#   data = range(n)
#   writeBlockData(file, data, npoints)
