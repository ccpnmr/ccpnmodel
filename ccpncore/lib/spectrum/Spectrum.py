"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================

__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
              "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                " or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================
import os
from typing import Sequence

from ccpn.util import Path
from ccpnmodel.ccpncore.lib.spectrum.BlockData import determineBlockSizes
from ccpnmodel.ccpncore.memops.ApiError import ApiError


# _isotopeRefExperimentMap = None

# All known axisCodes: ['Br', 'C', 'CA', 'CA1', 'CO', 'CO1', 'C1', 'C2', 'Ch', 'Ch1',
# 'F', 'H', 'H1', 'H2', 'H3', 'H4', 'Hc', 'Hc1', 'Hcn', 'Hcn1', 'Hn', 'Hn1',
# 'Jch', 'Jhh', 'Jhn', 'Jhp', 'MQcc', 'MQhh', 'MQhhhh', 'N', 'N1', 'Nh', 'Nh1',
# 'P', 'delay']
#
# 'J' matches 'Jx...'


def createBlockedMatrix(dataUrl:'Url', path:str, numPoints:Sequence[int],
                        blockSizes:Sequence[int]=None,
                        isBigEndian:bool=True, numberType:str='float', isComplex:bool=None,
                        headerSize:int=0, blockHeaderSize:int=0, nByte=4, fileType=None,
                       **additionalParameters) -> 'BlockedBinaryMatrix':
  """Create BlockedBinaryMatrix object. Explicit parameters are the most important,
  additional parameters to BlockedBinaryMatrix are passed in additionalParameters"""
  path = Path.normalisePath(path)

  if os.path.isabs(path):
    urlpath = Path.normalisePath(dataUrl.url.path, makeAbsolute=True)
    if not path.startswith(urlpath):
      raise ApiError('path = %s, does not start with dataUrl path = %s' % (path, urlpath))
    if path == urlpath:
      raise ApiError('path = %s, same as dataUrl path but should be longer' % path)

    # TBD: below is a bit dangerous but should work (+1 is to remove '/')
    path = path[len(urlpath)+1:]

  if not blockSizes:
    blockSizes = determineBlockSizes(numPoints)

  if not isComplex:
    isComplex = len(numPoints) * [False]

  dataLocationStore = dataUrl.dataLocationStore


  matrix = dataLocationStore.newBlockedBinaryMatrix(dataUrl=dataUrl, path=path,
                 numPoints=numPoints, blockSizes=blockSizes, isBigEndian=isBigEndian,
                 numberType=numberType, isComplex=isComplex, headerSize=headerSize,
                 blockHeaderSize=blockHeaderSize, nByte=nByte, fileType=fileType,
                 **additionalParameters)

  return matrix


#

def dimensionTransferType(dataDims:Sequence['DataDim'])->str:
  """Get ExpTransferType connecting two dataDims - uses heuristics"""

  expDimRefs = [x.expDim.sortedExpDimRefs()[0] for x in dataDims]
  return _expDimRefTransferType(*expDimRefs)

def _expDimRefTransferType(expDimRef1:'ExpDimRef', expDimRef2:'ExpDimRef')->str:
  """Get ExpTransferType and isDirect boolean connecting two expDimRefs - uses heuristics"""

  # First try looking for one-bond axisCodes
  axisCode1 = expDimRef1.axisCode
  axisCode2 = expDimRef2.axisCode
  if len(axisCode1) > 1 and len(axisCode2) > 1:
    ss2 = axisCode2.upper()
    if axisCode1.upper() == ss2[1] + ss2[0] + ss2[2:]:
      if (axisCode1[0].isupper() and axisCode2[0].isupper() and
          axisCode1[1].islower() and axisCode2[1].islower()):
        # Hooray, we have a situation like 'Hn'/'Nh' or 'Hp1'/'Ph1'
        return ('onebond', True)

  # Still here - try with ExpPrototypes
  refExpDimRef1 = expDimRef1.refExpDimRef
  refExpDimRef2 = expDimRef2.refExpDimRef
  if None not in (refExpDimRef1, refExpDimRef2):
    for atomSite1 in refExpDimRef1.expMeasurement.atomSites:
      for atomSite2 in refExpDimRef2.expMeasurement.atomSites:
        ll = list(atomSite1.expTransfers.intersection(atomSite2.expTransfers))
        if len(ll) == 1:
          # We have an expTransfer that connects our expDimRefs
          return (ll[0].transferType, True)

  # Still here - try using expTransfer
  ll = list(expDimRef1.expTransfers.intersection(expDimRef2.expTransfers))
  if len(ll) == 1:
    return (ll[0].transferType, ll[0].isDirect)
  #
  return None