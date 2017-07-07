"""Functions to be copied automatically into ccpnmodel.ccpncore..api.ccp.molecule.Molecule.molecule

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:10 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from typing import Sequence, List, Tuple
from ccpnmodel.ccpncore.lib.chemComp import Io as chemCompIo
from ccpnmodel.ccpncore.lib.molecule import MoleculeQuery
from ccpnmodel.ccpncore.lib.molecule.MoleculeModify import _getLinearChemCompData
from ccpnmodel.ccpncore.memops.ApiError import ApiError
from ccpnmodel.ccpncore.lib import CopyData
from ccpn.util import Undo


def clone(self:'Molecule', newName:str=None) -> "Molecule":
  """Make a new molecule based upon the sequence of an existing one
  .. describe:: Input

  Molecule.Molecule

  .. describe:: Output

  Molecule.Molecule
  """
  defaultString =  'Molecule %d'

  project = self.root
  ii = len(project.molecules) + 1
  newName = newName or defaultString % ii
  while project.findFirstMolecule(name=newName) is not None:
    ii += 1
    newName = defaultString % ii
  newMolecule = CopyData.copySubTree(self, project, topObjectParameters={'name':newName,},
                                     maySkipCrosslinks=True )

  return newMolecule


def extendOneLetterMolResidues(self:'Molecule', sequence:str, molType:str='protein', startNumber:int=1,
                            isCyclic:bool=False) -> List["MolResidue"]:
  """Descrn: Adds MolResidues for a sequence of code1Letter to Molecule, using molType.
             Consecutive protein or DNA/RNA residues are connected, other residues remain unlinked

     Inputs: Ccp.Molecule.Molecule,
             Word (Sequence string, of one-letter codes),
             Word (molType: 'protein', 'DNA', or 'RNA'
             Int (first MolResidue.seqCode)
             bool (is molecule cyclic?)

     Output: List of new Ccp.Molecule.MolResidues
  """
  if not sequence:
    raise ValueError("Attempt to append empty residue sequence")

  root = self.root

  oldMolResidues = self.molResidues
  if oldMolResidues:
    nn = max([x.seqCode for x in oldMolResidues]) + 1
    startNumber = max(startNumber, nn)

  # Sequence string. Use molType and assume one-letter codes
  if not molType in MoleculeQuery.LINEAR_POLYMER_TYPES:
    raise ValueError("molType %s must be one of:  %s"
                     % (molType, MoleculeQuery.LINEAR_POLYMER_TYPES))

  # upcase, as all one-letter codes are upper case
  sequence = sequence.upper()

  ll = [root.findFirstChemComp(molType=molType, code1Letter=x, className="StdChemComp")
        for x in sequence]
  if None in ll:
    ii = ll.index(None)
    raise ValueError("Illegal %s code %s at position %s in sequence: %s"
                     % (molType, sequence[ii], ii, sequence))

  if len(ll) == 1:
    chemComp = ll[0]
    chemCompVar  = (chemComp.findFirstChemCompVar(linking='none') or
                    chemComp.findFirstChemCompVar()) # just a default
    molResidues = [self.newMolResidue(seqCode=startNumber, chemCompVar=chemCompVar)]

  else:
    seqInput= [(molType,x.ccpCode) for x in ll]
    molResidues = extendLinearSequence(self, seqInput, seqCodeStart=startNumber,
                                    isCyclic=isCyclic)

  #
  return molResidues


def extendMolResidues(self:'Molecule', sequence:Sequence[str], startNumber:int=1, isCyclic:bool=False
                      ) -> List["MolResidue"]:
  """Descrn: Adds MolResidues for a sequence of residueNames to Molecule.
             Consecutive protein or DNA/RNA residues are connected, other residues remain unlinked

     Inputs: Ccp.Molecule.Molecule,
             List of Words (residueName),
             Int (first MolResidue.seqCode)
             bool (is molecule cyclic?)

     Output: List of new Ccp.Molecule.MolResidues
  """

  root = self.root

  if not sequence:
    return []

  # Reset startNumber to match pre-existing MolResidues
  oldMolResidues = self.molResidues
  if oldMolResidues:
    nn = max([x.seqCode for x in oldMolResidues]) + 1
    startNumber = max(startNumber, nn)

  # Convert to sequence of (molType, ccpCode) and check for known residueNames
  residueName2chemCompId = MoleculeQuery.fetchStdResNameMap(root)
  # seqInput = [residueName2chemCompId.get(x) for x in sequence]
  seqInput = []
  for x in sequence:
    if x.startswith('dummy.'):
      # Dummy residue, special handling
      seqInput.append(('dummy',x[6:]))
    else:
      seqInput.append(residueName2chemCompId.get(x))

  if None in seqInput:
    ii = seqInput.index(None)
    raise ValueError("Unknown residueName %s at position %s in sequence"
                     % (sequence[ii], ii))

  # Divide molecule in stretches by type, and add the residues one stretch at a time
  result = []

  offset1 = 0
  while offset1 < len(seqInput):
    molType1, ccpCode = seqInput[offset1]

    if molType1 in MoleculeQuery.LINEAR_POLYMER_TYPES:
      # Linear polymer stretch - add to stretch
      offset2 = offset1 + 1
      while offset2 < len(seqInput):
        molType2 = seqInput[offset2][0]
        if (molType2 in MoleculeQuery.LINEAR_POLYMER_TYPES
            and (molType1 == 'protein') == (molType2 == 'protein')):
          # Either both protein or both RNA/DNA
          offset2 += 1
        else:
          break

      if offset2 - offset1 > 1:
        result.extend(extendLinearSequence(self, seqInput[offset1:offset2],
                                        seqCodeStart=startNumber+offset1, isCyclic=isCyclic))
        offset1 = offset2
        # End of stretch. Skip ret of loop and go on to next residue
        continue

    # No linear polymer stretch was found. Deal with residue by itself
    # assert  molType1 not in LINEAR_POLYMER_TYPES or offset2 - offset1 == 1
    chemComp = chemCompIo.fetchChemComp(root, molType1, ccpCode)
    if chemComp:
      chemCompVar  = (chemComp.findFirstChemCompVar(linking='none') or
                      chemComp.findFirstChemCompVar()) # just a default

      result.append(self.newMolResidue(seqCode=startNumber+offset1, chemCompVar=chemCompVar))
      offset1 += 1

    else:
      raise ValueError('ChemComp %s,%s cannot be found.' % (molType1, ccpCode))

  #
  return result


def extendLinearSequence(self:'Molecule', sequence:Sequence[Tuple[str, str]], seqCodeStart:int=1,
                       isCyclic:bool=False) -> List["MolResidue"]:
  """Descrn: Add residues to molecule. Fast method, which uses 'override' mode.
             sequence is a list of (molType,ccpCode) tuples - so can make mixed-type
             linear polymers; All ChemComps must have next and prev links to fit a
             linear polymer seqCodes start from seqCodeStart, serial from next
             free serial (or 1). First residue is 'start' and last is 'end', unlesss isCyclic
    Inputs: Molecule.molecule, List of Tuples of Strings (molType, ccpCode), Int, Boolean
     Output: List of Molecule.MolResidues
  """
  logger = self.root._logger

  if len(sequence) < 2:
    raise ApiError("Sequence %s too short for function" % sequence)


  # set up
  project = self.root
  chemCompData = {}

  molResidues = []
  molResLinkEnds = []
  molResLinks = []

  # get starting serial
  serialDict = self.__dict__.setdefault('_serialDict', {})
  serial = serialDict.get('molResidues', 0)

  root = self.root
  root.__dict__['override'] = True

  # Set up for undo
  undo = self.root._undo
  if undo is not None:
    undo.increaseBlocking()

  ###if 1:
  try:
    # first residue
    if isCyclic:
      seqCode = seqCodeStart - 1
      doSequence = sequence
    else:
      seqCode = seqCodeStart
      serial += 1
      doSequence = sequence[1:-1]

      molType, ccpCode = sequence[0]
      molResData, otherLinkCodes = _getLinearChemCompData(project, molType,
                                                        ccpCode, 'start')

      molResidue = self.newMolResidue(seqCode=seqCode, serial=serial,
                                          **molResData)
      molResidues.append(molResidue)

      if otherLinkCodes:
        for linkCode in otherLinkCodes:
          # TBC these mostly seem to exist already...
          if not molResidue.findFirstMolResLinkEnd(linkCode=linkCode):
            linkEnd = molResidue.newMolResLinkEnd(linkCode=linkCode)
            molResLinkEnds.append(linkEnd)

    # middle residues
    for seqTuple in doSequence:
      molType,ccpCode = seqTuple
      seqCode += 1
      serial += 1
      if seqTuple in chemCompData:
        molResData,otherLinkCodes = chemCompData[seqTuple]
      else:
        molResData,otherLinkCodes = _getLinearChemCompData(project, molType,
                                                          ccpCode, 'middle')
        chemCompData[seqTuple] = (molResData,otherLinkCodes)

      molResidue = self.newMolResidue(seqCode=seqCode, serial=serial,
                                          **molResData)
      molResidues.append(molResidue)

      if otherLinkCodes:
        for linkCode in otherLinkCodes:
          # TBC these mostly seem to exist already...
          if not molResidue.findFirstMolResLinkEnd(linkCode=linkCode):
            linkEnd = molResidue.newMolResLinkEnd(linkCode=linkCode)
            molResLinkEnds.append(linkEnd)

    # last residue
    if not isCyclic:
      seqCode += 1
      serial += 1
      (molType,ccpCode) = sequence[-1]
      molResData,otherLinkCodes = _getLinearChemCompData(project, molType,
                                                        ccpCode, 'end')

      molResidue = self.newMolResidue(seqCode=seqCode, serial=serial,
                                          **molResData)
      molResidues.append(molResidue)

      if otherLinkCodes:
        for linkCode in otherLinkCodes:
          # TBC these mostly seem to exist already...
          if molResidue.findFirstMolResLinkEnd(linkCode=linkCode):
            continue

          linkEnd = molResidue.newMolResLinkEnd(linkCode=linkCode)
          molResLinkEnds.append(linkEnd)

    # make links
    for second in range(1,len(sequence)):
      first = second -1
      nextLinkEnd = molResidues[first].findFirstMolResLinkEnd(linkCode='next')
      molResLinkEnds.append(nextLinkEnd)
      prevLinkEnd = molResidues[second].findFirstMolResLinkEnd(linkCode='prev')
      molResLinkEnds.append(prevLinkEnd)
      molResLinks.append(
       self.newMolResLink(molResLinkEnds=[nextLinkEnd,prevLinkEnd])
      )

    if isCyclic:
      # cyclising link
      nextLinkEnd = molResidues[-1].findFirstMolResLinkEnd(linkCode='next')
      molResLinkEnds.append(nextLinkEnd)
      prevLinkEnd = molResidues[0].findFirstMolResLinkEnd(linkCode='prev')
      molResLinkEnds.append(prevLinkEnd)
      molResLinks.append(
       self.newMolResLink(molResLinkEnds=[nextLinkEnd,prevLinkEnd])
      )

    # final validity check
    self.checkAllValid()

  except:
    # clean up
    try:
      while molResLinks:
        molResLink = molResLinks.pop()
        molResLink.delete()
      while molResidues:
        molResidue = molResidues.pop()
        molResidue.delete()
    except:
      logger.error("Error in clean-up after precious error")

  finally:
    # reset override and set isModified
    root.__dict__['override'] = False
    self.__dict__['isModified'] = True
    if undo is not None:
      undo.decreaseBlocking()

  if undo is not None and (molResidues or molResLinks):
    objectsCreated = molResidues+molResLinks
    for molResidue in molResidues:
      objectsCreated.extend(molResidue.molResLinkEnds)
    undo.newItem(Undo._deleteAllApiObjects, self.root._unDelete,
                 undoArgs=(objectsCreated,), redoArgs=(objectsCreated,
                                                       set(x.topObject for x in objectsCreated)))

  # call notifiers:
  # NBNB the im port MUST be inside a function as we can get circular import problems otherwise
  from ccpnmodel.ccpncore.api.ccp.molecule import Molecule
  for clazz, objs in (
   (Molecule.MolResidue, molResidues),
   (Molecule.MolResLinkEnd, molResLinkEnds),
   (Molecule.MolResLink, molResLinks),
  ):
    notifiers = clazz._notifies.get('__init__')
    if notifiers:
      for notify in notifiers:
        for obj in objs:
          notify(obj)

  return molResidues
