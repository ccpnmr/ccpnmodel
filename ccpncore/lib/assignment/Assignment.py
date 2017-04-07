"""Assignment-related library functions at API (data storage) level

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2017"
__credits__ = ("Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan"
               "Simon P Skinner & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license"
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for licence text")
__reference__ = ("For publications, please use reference from http://www.ccpn.ac.uk/v3-software/downloads/license"
               "or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:37 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================


def _doNamesMatchBound(lightName:str, heavyName:str) -> bool:
  """checks if lightName matches a hydrogen atom or fluorine bound to atom named heavyName
  NB, a name like H11 would match both C1 or C11 - cannot be helped"""

  # possible names for 'light' atoms or pseudoatoms
  lightFirstChars = 'HDTFMQ'
  lightAppendixChars = '123XY#'

  if ((lightName == "H" and heavyName == "N") or
      (lightName == "H#" and heavyName == "N") or
      (lightName == "H2''" and heavyName == "C2'") or
      (lightName == "H5''" and heavyName == "C5'")):
    # special cases for protein and DNA/RNA
    return True

  elif not lightName or len(heavyName) < 2:
    # lightName empty or heavyName too short
    # Single-char heavyName is only allowed in special cases above
    return False

  elif lightName[0] not in lightFirstChars or heavyName[0] in lightFirstChars:
    # incorrect nucleus code
    return False

  elif lightName[1:] == heavyName[1:]:
    # names match except for first character.
    return True

  elif lightName[1:-1] == heavyName[1:] and lightName[-1] in lightAppendixChars:
    # names match except for first character, with single suffix character
    return True

  else:
    return False


def getConnectedAtoms(spectrum):

  # chain = self.chain
  connections = []

  nDim = spectrum.numDim

  maxConnectionDist = 1
  minConnectionDist = 0
  # drawConnection = self.drawConnection

  boundDims = []
  for dataDim1, dataDim2 in spectrum.getOnebondDataDims():
    boundDims.append(set([dataDim1.dim-1, dataDim2.dim-1]))

  # includePredicted = self.includePredictedCheck.get()
  for peakList in spectrum.peakLists:
    # if (not includePredicted) and peakList.isSimulated:
    #   continue

    for peak in peakList.peaks:
      dimAtoms = {}
      for i in range(nDim):
        dimAtoms[i] = set()


      # Find all assigned-to atoms per dimension of the peak:
      if peak.peakContribs:
        for peakContrib in peak.peakContribs:

          for contrib in peakContrib.peakDimContribs:
            dim = contrib.peakDim

            resonanceSet = contrib.resonance.resonanceSet
            if resonanceSet:
              for atomSet in resonanceSet.atomSets:
                atom = atomSet.findFirstAtom()
                residue = atom.residue
                # if residue.chain is chain:
                dimAtoms[dim.dim-1].add((atom,residue))

      else:
        for dim in peak.peakDims:
          for contrib in dim.peakDimContribs:
            resonanceSet = contrib.resonance.resonanceSet
            if resonanceSet:
              for atomSet in resonanceSet.atomSets:
                atom = atomSet.findFirstAtom()
                residue = atom.residue
                # if residue.chain is chain:
                dimAtoms[dim.dim-1].add((atom,residue))

      for i in range(nDim-1):
        for j in range(i+1, nDim):
          atomPairs = []

          # if dimensions are bound, add pairs ofbound atoms
          if set([i,j]) in boundDims:
            for atomA, residueA in dimAtoms[i]:
              for atomB in atomA.boundAtoms:
                atomPairs.append((atomA, residueA, atomB, atomB.residue))
              #
              # for atomB, residueB in dimAtoms[j]:
              #
              #    if _areAtomsBound(atomA, atomB):
              #      atomPairs.append((atomA, residueA, atomB, residueB))

          # If dimensions were not bound, or nothing was found, add all possible atom pairs
          if not atomPairs:
            for atomA, residueA in dimAtoms[i]:
              for atomB, residueB in dimAtoms[j]:
                atomPairs.append((atomA, residueA, atomB, residueB))

          # Filter out connection distances between given limits
          for atomA, residueA, atomB, residueB in atomPairs:

            if atomA is atomB:
              continue

            diff = abs(residueA.seqId - residueB.seqId)
            if ((maxConnectionDist is None) or (diff <= maxConnectionDist)) and \
              (diff >= minConnectionDist):
              connections.append([atomA, atomB])
  return connections
