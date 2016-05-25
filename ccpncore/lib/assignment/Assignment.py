"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon Skinner, Geerten Vuister"
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

# def _boundNamesfromType(chemCompVar, atomName):
#   """get names of atoms bound to atom names atomName within chemComp"""
# NBNB TBD What is this for?


def _areAtomsBound(atom1, atom2):
  """Dertemine whether two atoms are bonded together
  .. describe:: Input

  MolSystem.Atom, MolSystem.Atom

  .. describe:: Output

  Boolean
  """

  if not hasattr(atom1, 'isAtomBound'):
    atom1.isAtomBound = {}
  elif atom2 in atom1.isAtomBound.keys():
    return atom1.isAtomBound[atom2]

  if not hasattr(atom2, 'isAtomBound'):
    atom2.isAtomBound = {}
  elif atom1 in atom2.isAtomBound.keys():
    return atom2.isAtomBound[atom1]

  isBound = False

  if atom1 is not atom2:
    residue1 = atom1.residue
    residue2 = atom2.residue

    if residue2.chain is residue1.chain:
      if residue2 is not residue1:

        linkEnd1 = residue1.chemCompVar.findFirstLinkEnd(boundChemAtom=atom1.chemAtom)
        if not linkEnd1:
          isBound = False

        else:
          linkEnd2 = residue2.chemCompVar.findFirstLinkEnd(boundChemAtom=atom2.chemAtom)
          if not linkEnd2:
            isBound = False

          else:
            molResLinkEnd1 = residue1.molResidue.findFirstMolResLinkEnd(linkEnd=linkEnd1)
            if not molResLinkEnd1:
              isBound = False

            else:
              molResLinkEnd2 = residue2.molResidue.findFirstMolResLinkEnd(linkEnd=linkEnd2)
              if not molResLinkEnd2:
                isBound = False

              elif molResLinkEnd2 in molResLinkEnd1.molResLink.molResLinkEnds:
                isBound = True

              else:
                isBound = False

      else:
        for chemBond in atom1.chemAtom.chemBonds:
          if atom2.chemAtom in chemBond.chemAtoms:
            isBound = True
            break

  atom1.isAtomBound[atom2] = isBound
  atom2.isAtomBound[atom1] = isBound

  return isBound

def getOnebondDataDims(spectrum):
  """
  Get pairs of spectrum data dimensions that are connected by onebond transfers

  .. describe:: Input

  Nmr.DataSource

  .. describe:: Output

  List of 2-List of Nmr.DataDims
  """

  dataDims = []
  expDimRefs = getOnebondExpDimRefs(spectrum.experiment)

  for expDimRef0, expDimRef1 in expDimRefs:
    dataDim0 = spectrum.findFirstDataDim(expDim=expDimRef0.expDim)
    dataDim1 = spectrum.findFirstDataDim(expDim=expDimRef1.expDim)

    if dataDim0 and dataDim1:
      dataDims.append( [dataDim0,dataDim1] )

  return dataDims

def getOnebondExpDimRefs(experiment):
  """
  Get pairs of experiment dimensions that are connected by onebond transfers

  .. describe:: Input

  Nmr.Experiment

  .. describe:: Output

  List of 2-List of Nmr.ExpDimRefs
  """

  expDimRefs   = []
  expTransfers = []

  for expTransfer in experiment.sortedExpTransfers():
    if expTransfer.transferType in ('onebond',):
      expTransfers.append(expTransfer)

  for expTransfer in expTransfers:
    expDimRefs.append(expTransfer.sortedExpDimRefs())

  return expDimRefs


def getConnectedAtoms(spectrum):

  # chain = self.chain
  connections = []

  nDim = spectrum.numDim

  maxConnectionDist = 1
  minConnectionDist = 0
  # drawConnection = self.drawConnection

  boundDims = []
  for dataDim1, dataDim2 in getOnebondDataDims(spectrum):
    boundDims.append(set([dataDim1.dim-1, dataDim2.dim-1]))

  # includePredicted = self.includePredictedCheck.get()
  for peakList in spectrum.peakLists:
    # if (not includePredicted) and peakList.isSimulated:
    #   continue

    for peak in peakList.peaks:
      dimAtoms = {}
      for i in range(nDim):
        dimAtoms[i] = set()

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

          if set([i,j]) in boundDims:
            for atomA, residueA in dimAtoms[i]:
              for atomB, residueB in dimAtoms[j]:

                 if _areAtomsBound(atomA, atomB):
                   atomPairs.append((atomA, residueA, atomB, residueB))

          if not atomPairs:
            for atomA, residueA in dimAtoms[i]:
              for atomB, residueB in dimAtoms[j]:
                atomPairs.append((atomA, residueA, atomB, residueB))

          for atomA, residueA, atomB, residueB in atomPairs:

            if atomA is atomB:
              continue

            diff = abs(residueA.seqId - residueB.seqId)
            if ((maxConnectionDist is None) or (diff <= maxConnectionDist)) and \
              (diff >= minConnectionDist):
              connections.append([atomA, atomB])
  return connections