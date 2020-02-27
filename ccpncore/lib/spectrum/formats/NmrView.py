"""Module Documentation here
  based on original code from g.s.thompson@kent.ac.uk
  Copyright (C) 2006 Gary Thompson (University of Leeds & Kent)

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
  
  dataFileName = os.path.splitext(paramFileName)[0] + '.nv'
  parFileName = os.path.splitext(paramFileName)[0] + '.par'

  
  fileObj = open(dataFileName, 'rb')
  parFileText = []
  with open(parFileName) as parFile:
    for line in parFile:
      parFileText.append(line.strip())

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
    refPoints[i] = floatVals[dimBase + (i*dimRecordSize) + dimRefPointOffset]+1
    refPpms[i] = floatVals[dimBase + (i*dimRecordSize) + dimRefValueOffset]
  
  for i in duffDims[::-1]:
    del numPoints[i]
    del blockSizes[i]
    del specFreqs[i]
    del specWidths[i]
    del refPpms[i]
    del refPpms[i]
  
  isotopes = _guessConsistentNuclei(specFreqs)

  if len(parFileText) != 0:
    parFileData = parseParFile( parFileName, ndim, parFileText)

    if parFileData['good']:
      for dim in range(ndim):
        if parFileData['sf'][dim] != None:
          specFreqs[dim] = parFileData['sf'][dim]
        if parFileData['sw'][dim] != None:
          specWidths[dim] = parFileData['sw'][dim]
        if parFileData['refpt'][dim] != None:
          refPoints[dim] = parFileData['refpt'][dim]
        if parFileData['refppm'][dim] != None:
          refPpms[dim] = parFileData['refppm'][dim]

  data = (FILE_TYPE, dataFileName, numPoints, blockSizes,
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

def parseParFile(parFileName, ndims, lines):
  result = {'sw' : [None] * ndims, 'sf' : [None] * ndims, 'refpt' : [None] * ndims,
            'refppm' : [None] * ndims, 'good' : True}
  try:
      for i, line in enumerate(lines):
        fields = line.strip().split()
        attribute = fields[0]
        # doesn't work for nmrpipe currently
        # if i ==0:
        #   if attribute != 'header':
        #     msg = 'file %s doesn\'t appear to be an nmrview .par file the first line doesn\'t start with \'header\' %s'
        #     return
        if attribute == 'sw':
          axisIndex = int(fields[1])-1
          checkParFileNumberOfFields(parFileName, i, fields, 3)
          checkParFileAxisIndex(parFileName, ndims, i, fields)
          result[attribute][axisIndex] = float(fields[2])

        elif attribute == 'sf':
          axisIndex = int(fields[1])-1
          checkParFileNumberOfFields(parFileName, i, fields, 3)
          checkParFileAxisIndex(parFileName,  ndims, i, fields)
          result[attribute][axisIndex] = float(fields[2])

        elif attribute == 'ref':
          axisIndex = int(fields[1])-1
          checkParFileNumberOfFields(parFileName, i, fields, 4)
          checkParFileAxisIndex(parFileName, ndims, i, fields)
          result['refpt'][axisIndex] = float(fields[3])
          result['refppm'][axisIndex] = float(fields[2])

  except Exception as  e:
    print ('nmrview parameter file error',e)
    traceback.print_exc(file=sys.stdout)
    result['good'] = False

  return result

def checkParFileNumberOfFields(parFile, lineIndex, fields, expected):
  if len(fields) != expected:
    tooManyFieldsError = 'line %d in nmrview .par file %s has a bad format: incorrect number of fields for %s expected %d\n (line: %s)\n'
    raise Exception(tooManyFieldsError % (lineIndex +1 ,parFile,fields[0],expected,' '.join(fields)))

def checkParFileAxisIndex(parFile, ndim, lineIndex, fields):
  axis = int(fields[1])
  if axis > ndim or  axis < 1:
    badAxisError = 'line %d in nmrview .par %s, has a bad axis index: %d. Permissible axis indices are 1 to %d  (line: %s)\n'
    raise Exception(badAxisError % (lineIndex + 1, parFile, axis, ndim, ' '.join(fields)))