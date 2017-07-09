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
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
import os, sys

from ccpn.util import Common as commonUtil

# from memops.qtgui.MessageDialog import showError

FILE_TYPE = 'Azara'

def readParams(filePath):
  
  # Check whether we have a binary file

  with open(filePath, 'rb') as fileObj:
    firstData = fileObj.read(1024)

    testData = set([c for c in firstData]) - set([ord(w) for w in commonUtil.WHITESPACE_AND_NULL])
    if min([ord(chr(c)) for c in testData]) < 32:
      dataFile = filePath
      filePath = dataFile + '.par'
      if not os.path.exists(filePath):
        dirName, fileName = os.path.split(filePath)

        for otherFile in os.listdir(dirName):
          if otherFile == fileName:
            continue

          if ('.par' in otherFile) and otherFile.startswith(fileName):
            filePath = os.path.join(dirName, otherFile)
            break

        else:
          msg = "Cannot find AZARA parameter file to go with binary file %s"
          # showError('Error', msg % filePath)
          return
    else:
      dataFile = None
      

  # Format invariant

  wordSize = 4
  headerSize = 0
  blockHeaderSize = 0
  pulseProgram = None
  dataScale = 1.0

  # Params

  numPoints = []
  blockSizes = []
  refPpms = []
  refPoints = []
  specWidths = []
  specFreqs = []
  isotopes = []
  sampledValues = []
  sampledSigmas = []

  isFloatData = True
  isBigEndian = sys.byteorder == 'big'

  with open(filePath, 'rU', encoding='utf-8') as fileObj:

    dim = 0
    for line in fileObj:
      line = line.strip()

      if not line:
        continue

      if line.startswith('!'):
        continue

      if '!' in line:
        line = line.split('!')[0]

      data = line.split()
      keyword = data[0]

      if keyword == 'file':
        if not dataFile:
          dataFile = data[1]

      elif keyword == 'int':
        isFloatData = False

      elif keyword == 'swap':
        isBigEndian = not isBigEndian

      elif keyword == 'big_endian':
        isBigEndian = True

      elif keyword == 'little_endian':
        isBigEndian = False

      elif keyword == 'ndim':
        nDim = int(data[1])
        numPoints = [None] * nDim
        blockSizes = [1] * nDim
        refPpms = [1.0] * nDim
        refPoints = [1.0] * nDim
        specWidths = [1000.0] * nDim
        specFreqs = [500.0] * nDim
        isotopes = ['1H'] * nDim
        sampledSigmas = [[]] * nDim
        sampledValues = [[]] * nDim

      elif keyword == 'dim':
        dim = int(data[1]) - 1

      elif keyword == 'npts':
        numPoints[dim] = int(data[1])

      elif keyword == 'block':
        blockSizes[dim] = int(data[1])

      elif keyword == 'sw':
        specWidths[dim] = float(data[1])

      elif keyword == 'sf':
        specFreqs[dim] = float(data[1])

      elif keyword == 'refppm':
        refPpms[dim] = float(data[1])

      elif keyword == 'refpt':
        refPoints[dim] = float(data[1])

      elif keyword == 'nuc':
        isotopes[dim] = commonUtil.checkIsotope(data[1])

      elif keyword == 'params':
        sampledValues[dim] = [float(x) for x in data[1:]]
        isotopes[dim] = None

      elif keyword == 'sigmas':
        sampledSigmas[dim] = [float(x) for x in data[1:]]

  if dataFile is None:
    msg = "AZARA spectrum file not set in parameters"
    # showError('Error', msg)
    return

  if not os.path.exists(dataFile):
    dirPath, parFile = os.path.split(filePath)
    null, specFile = os.path.split(dataFile)
    dataFile = os.path.join(dirPath, specFile)
    
  if not os.path.exists(dataFile):
    msg = "AZARA spectrum data file %s does not exist"
    # showError('Error', msg % dataFile)
    return

  data = (FILE_TYPE, dataFile, numPoints, blockSizes,
          wordSize, isBigEndian, isFloatData,
          headerSize, blockHeaderSize,
          isotopes, specFreqs,
          specWidths, refPoints, refPpms,
          sampledValues, sampledSigmas,
          pulseProgram, dataScale)

  return data
