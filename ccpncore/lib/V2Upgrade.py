"""Mapping of Resonances and ResonancGroups in version 2 to new 4-string assignment style

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:09 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import os
import operator

from ccpnmodel.ccpncore.lib.chemComp.Util import chemAtomSetFromAtoms


def mapResonanceGroupResidues(apiNmrProject, molSystem=None, chainMap=None) -> dict:
  """Map resonanceGroup:assignmentTuple for fully assigned ResonanceGroups """

  result = {}

  # We need either chainMap or molSystem, and chainMap takes precedence
  if chainMap:
    molSystem = None

  # Handle properly assigned ResonanceGroups
  for resonanceGroup in apiNmrProject.sortedResonanceGroups():

    # Find residue
    residue = resonanceGroup.residue
    if residue is None:
      ll = []
      for residueProb in resonanceGroup.residueProbs:
        if residueProb.weight:
          ll.append(residueProb)
      if len(ll) == 1:
        # In principle this should never happen, but it does not hurt to be careful
        residue = ll[0].possibility

    if residue:

      # Remap chain and residue if necessary,

      chain = residue.chain
      if chainMap:
        # If there is a chainMap the chain MUST be in it.
        chain = chainMap[chain]
        # get residue in new chain
        residue = chain.findFirstResidue(seqCode=residue.seqCode,
                                         seqInsertCode=residue.seqInsertCode)

      elif residue.topObject is not molSystem:
          raise ValueError("Cannot generate consistent assignment names from mixed MolSystems - 1")
      #
      # # set residue assignment strings
      # chainCode = chain.code
      # sequenceCode = str(residue.seqCode)+ (residue.seqInsertCode or '').strip()
      # residueType = residue.code3Letter

      if residue:
        # Should nevere happen, bunless there is an error in teh cahinMapping
        result[resonanceGroup] = residue
  #
  return result


def mapUnAssignedFixedResonances(nmrConstraintStore):
  """Map unassigned resonances for NmrConstraintStore"""

  result = {}

  separator1 = '@'
  separator2 = '@@'   # To distinguish fixedResonance serial from resonance serial

  for resonance in nmrConstraintStore.sortedFixedResonances():
    if not resonance.resonanceSet:
      # unassigned - treat it

      name =  regularisedResonanceName(resonance)

      # Add resonance serial to name, if it is not in the name already.
      separator = separator1
      # use resonanceSerial if available
      serial = resonance.resonanceSerial
      if not serial:
        # use FixedResonance.serial instead, and use '@@' to distinguish
        serial = resonance.serial
        separator = separator2

      ss = '%s%s' % (separator1, serial)
      if ss not in name:
        name = '%s%s%s' % (name, separator, serial)

      #
      result[resonance] = (None, None, None, name)
  #
  return result


def addOffsetResonanceGroup(addToGroup:'ResonanceGroup', addGroup:'ResonanceGroup',
                             offset:int) -> bool:
  """Add addGroup as satellite to addToGroup with offset offset. Return True if successful"""
  previous = addToGroup.nmrProject.findFirstResonanceGroup(mainGroupSerial=addToGroup.serial,
                                                           relativeOffset=offset)
  if previous is None:
    # New. Set as offset. Multisteps to avoid name clashes and ensure undo.
    # We do not need to guard against connected stretches etc. in V2 conversion
    addGroup.sequenceCode = None
    addGroup.directNmrChain = addToGroup.nmrChain
    addGroup.sequenceCode = '%s%+d' % (addToGroup.sequenceCode, offset)

    # set offset residueType
    residueType = addGroup.residueType
    if residueType is None:
      chemComp = addToGroup.root.findFirstChemComp(molType=addGroup.molType,
                                                         ccpCode=addGroup.ccpCode)
      if chemComp:
        addGroup.residueType = chemComp.code3Letter

    return True

  else:
    # Duplicate. Merge.
    # NBNB check that resonance names are dealt with properly later
    for resonance in addGroup.resonances:
      resonance.resonanceGroup = previous
    addGroup.delete()

    return False



def mapAssignedResonances(topObject, molSystem=None, chainMap=None):
  """Make/extend {resonance:assignmentTuple} map in V2 for either Resonances or fixedResonances
  chainMap remaps chains to new ones with different chainCodes (for V2-V3 upgrade).

  NB, does NOT use ResonanceGroup information"""

  result = {}

  if topObject.className == 'NmrProject':
    resonanceSets = topObject.sortedResonanceSets()
  else:
    resonanceSets = topObject.sortedFixedResonanceSets()

  for resonanceSet in resonanceSets:

    # set up loop-level parameters
    resonances = list(resonanceSet.resonances)
    if resonanceSet.findFirstResonance(name=None):
      resonances.sort(key=operator.attrgetter('serial'))
    else:
      resonances.sort(key=operator.attrgetter('name'))
    atomSets = list(resonanceSet.atomSets)
    if resonanceSet.findFirstAtomSet(name=None):
      atomSets.sort(key=operator.attrgetter('serial'))
    else:
      atomSets.sort(key=operator.attrgetter('name'))
    allAtoms = [x for y in atomSets for x in y.atoms]
    chemAtomSet = chemAtomSetFromAtoms(allAtoms)
    if len(set(x.residue for x in allAtoms)) == 1:
      residue = allAtoms[0].residue
    else:
      residue = None

    if residue:

      # Remap chain and residue if necessary
      chain = residue.chain
      if chainMap:
        # If there is a chainMap the chain MUST be in it.
        chain = chainMap[chain]
        # get residue in new chain
        residue = chain.findFirstResidue(seqCode=residue.seqCode,
                                         seqInsertCode=residue.seqInsertCode)

      elif chain.molSystem is not molSystem:
        raise ValueError("Cannot generate consistent assignment names from mixed MolSystems - 2")

    if residue:
      # Should always be true - but in case something went wrong with the chain mapping

      # We have the residue - and we need the ChemCompVar below
      chemComp = residue.molResidue.chemComp
      chemCompVar = residue.chemCompVar or chemComp.findFirstChemCompVar(isDefaultVar=True)

      # Now for the atom name
      if chemAtomSet and len(atomSets) == 2 and len(resonances) <= 2:
        # prochiral pair. Use _getAmbigProchiralLabel for priority, and set 'x' for 'a', 'y' for 'b'

        # get non-stereo names
        atomSetNames = [x.name for x in atomSets]
        starpos = chemAtomSet.name.find('*')
        newNames = []
        if [x[starpos:] for x in sorted(atomSetNames)] == ["", "'"]:
          # special case - names are "abc'", "abc''"
          ss = atomSetNames[0][:starpos-1]
          newNames = [ss + 'x', ss + 'y']
        else:
          for ii, newChar in enumerate('xy'):
            chars = list(atomSetNames[ii])
            chars[starpos] = newChar
            newNames.append(''.join(chars))

        # select new name to use
        if topObject.className == 'NmrProject':
          # Real resonance - use normal procedure

          # First one resonance. NB we test prochiral label on one resonance only
          # - if data are inconsistent both might give 'a' and we must avoid a name clash.
          if _getAmbigProchiralLabel(resonances[0]) != 'a':
            # First resonance does not match first name - reverse name order
            # NB we test on one resonance only. If data are inconsistent and both give 'a'
            # we still want the names to be different
            newNames.reverse()

          for ii,resonance in enumerate(resonances):
            result[resonance] = (residue, newNames[ii].replace('*','%'))


        else:
          # NmrConstraintStore - these are fixed resonances

          if len(resonances) == 2:
            # resonances are sorted by name, as are newNames. Match in order.
            # NB this being in an NmrConstraintStore, we have to assume that names  are
            # consistent, so e.g. HG1* is bound to CG1 and not CG2
            for ii in range(2):
              result[resonances[ii]] = (residue, newNames[ii].replace('*','%'))

          else:
            # Only one resonance. Must choose which.
            # Use various heuristics, as we can not assume assignments in NmrProject still match.

            # assert len(resonances) == 1
            resonance = resonances[0]

            if resonance.name is None:
              # Aribtratily pck the first one. Wnat else?
              indx = 0

            else:
              for ii in range(2):
                if (resonance.name in(atomSetNames[ii], newNames[ii]) or
                    resonance.name.upper() in(atomSetNames[ii], newNames[ii])):
                  # name matches one of the atomSets - use matching name
                  indx = ii
                  break

              else:
                # Name did not match either possibility, so these are non-standard. Try anyway
                if 'b' in resonance.name or '3' in resonance.name:
                  # Heuristic - these names are likely to be second in sorting
                  # e.g. 'HBb' or 'HB3'
                  indx = 1
                elif 'a' in resonance.name or '1' in resonance.name:
                  # Heuristic = this name is likely to be first in sorting (e.g. 'HBa'
                  # NB both XY1, XY1*, XY11, XY21 (Asn, Gln,Arg) XY12 (Ile) should sort first
                  # Arg HH12 should sort second, but this cannot be helped
                  indx = 0
                elif '2' in resonance.name:
                  # This will not sort second for e,g, HB2/HB3, but that cannot be helped.
                  # The only one that matters is
                  # where e.g. HD1 must bind to CD1 and HD2 to CD2, and it gets those right
                  # Anyway the real atom names are caught before this
                  indx = 1
                else:
                  realResonance = resonance.resonance
                  if realResonance:
                    # We can not be sure that assignments have not changed, but
                    # better have it match the resonance than not
                    if _getAmbigProchiralLabel(realResonance) == 'a':
                      indx = 0
                    else:
                      indx = 1
                  else:
                    # Stuff it. We just do not know and pick the first one.
                    # Anyway the cases where is makes a difference are cared for above.
                    indx = 0

            resonanceName = newNames[indx]
            result[resonance] = (residue, resonanceName.replace('*','%'))

      elif len(resonances) == 1:
        # Single resonance, not assigned to prochiral

        resonance = resonances[0]
        if len(atomSets) == 1:
          # simple one-to-one stereospecific assignment
          if chemAtomSet:
            # assignment to atomSet
            resonanceName = chemAtomSet.name.replace('*', '%')
          else:
            #asssignment to single atom
            resonanceName = allAtoms[0].name

        else:
          # multiple atomSets
          # NB we do it this way because it must work in pure V2 as well as the intermediate model
          nuc = allAtoms[0].elementSymbol
          residueChemAtoms = [chemCompVar.findFirstChemAtom(name=x.name) for x in residue.atoms]
          residueChemAtoms = [x for x in residueChemAtoms if x is not None]
          if len(allAtoms) == len(residueChemAtoms):
            # All single atoms in residue
            resonanceName = '*'

          elif (all((x.elementSymbol == nuc) for x in allAtoms) and
              len([x for x in residueChemAtoms if x.elementSymbol == nuc]) == len(allAtoms)):
            # All atoms of a given nucleus
            resonanceName = nuc + '*'

          else:
            # random multiple atom selection
            resonanceName = '/'.join(sorted((str(x.name) for x in atomSets)))

        result[resonance] = (residue, resonanceName)

      else:
        # multiple resonances not matching chemAtomSet
        atomsName = '/'.join(sorted((str(x.name) for x in atomSets)))
        for resonance in resonances:
          # NB this name can not be in use already, so we do not need to check
          resonanceName = '%s@%s' % (atomsName, resonance.serial)

          result[resonance] = (residue, resonanceName.replace('*','%'))

    else:
      # assigned to multiple residues - cannot be helped
      # Same naming style for single and multiple resonances
      partNames = []
      for atomSet in atomSets:
        rr = atomSet.findFirstAtom().residue
        partNames.append('%s%s-%s' % (rr.seqCode, (rr.seqInsertCode or '').strip(), atomSet.name))

      ss = '/'.join(sorted(partNames))
      for resonance in resonances:
        resonanceName = '%s@%s' % (ss, resonance.serial)

        result[resonance] = (None, resonanceName.replace('*','%'))
  #
  return result

###################################################################################
#
#  Functions for V2/upgrade only:
#
###################################################################################

def regularisedResonanceName(resonance):
  """V2: Get resonance name, starting with element type and adding @serial to impossible names"""

  # NB names like '*', 'C*' etc. will not make it through regularisation
  # but it is too dangerous to arrive at those from name strings only
  # For that you need to have them properly assigned.

  resonanceName = resonance.name or ''

  # get elementCode
  isotope = resonance.isotope
  if isotope is None:
    elementCode = '?'
  else:
    elementCode = isotope.chemElement.symbol.upper()

  result = None

  if resonance.className == 'Resonance':

    # Exclude fixedResonances
    assignNames = list(set(resonance.assignNames))
    if len(assignNames) == 1:
      # One assignName - use for assignment
      name = assignNames[0]
      result =  name.replace('*', '%')


    elif len(assignNames) == 2:
      # 2 assignNames - if they match prochiral return nonstereo variant
      assignNames.sort()
      prefix = os.path.commonprefix(assignNames)
      lenPrefix = len(prefix)
      if assignNames[0][lenPrefix].isdigit() and assignNames[1][lenPrefix].isdigit():
        if assignNames[0][lenPrefix+1:] == assignNames[1][lenPrefix+1:]:

          # Heuristics, try to get x or y right
          # NB 'x' will not always match the lowest sorting - it fails for
          # ordinary HB2/HB3 methylenes and must be caught later
          # But the crucial isopropyl and aromatic cases should work
          newChar = None
          for char in reversed(resonanceName):
            if char.isdigit():
              break
          else:
            char = None
          if assignNames[0][lenPrefix] == char:
            newChar = 'x'
          elif assignNames[1][lenPrefix] == char:
            newChar = 'y'
          elif 'a' in resonanceName and not 'b' in resonanceName:
            newChar = 'x'
          elif 'b' in resonanceName and not 'a' in resonanceName:
            newChar = 'y'

          if newChar is not None:
            ll = list(assignNames[0])
            ll[lenPrefix] = newChar
            result = ''.join(ll).replace('*', '%')

  if result is None:
    # If we are still here, assignNames did not help. Use resonanceName only

    if resonanceName:
      if elementCode and resonanceName.upper().startswith(elementCode):
        # name is OK except possibly for casing - fix the casing
        ss = resonanceName[len(elementCode):]

        if 'x' in ss or 'y' in ss:
          # Necessary to avoid potential clashes with XY names set above
          # No actual assigned names contain 'x' or 'y' anyway
          result = '%s@%s-%s' % (elementCode, resonance.serial, resonanceName)
        else:
          # Name might be proper assignment name. Change to new wildcard convention
         result = (elementCode + ss).replace('*', '%')

      else:
        # Set unique default name
        result = '%s@%s-%s' % (elementCode, resonance.serial, resonanceName)

    else:
      result = '%s@%s' % (elementCode, resonance.serial)
  #
  return result


def upgradeConstraintList(constraintList):
  """Upgrade ConstraintList from early V3 to newer V3 - this avoids redoing earlier function
  and anyway data must be copied to a new set of objects

  Will also work if called on old-type V3 ConstraintLists (use only internally)"""

  constraintStore = constraintList.nmrConstraintStore

  # Get defining parameters
  className = constraintList.className
  restraintType = className[:-14]

  if restraintType in ('Distance', 'HBond', 'JCoupling', 'Rdc',):
    itemLength = 2
  elif restraintType in ('Csa', 'ChemicalShift'):
    itemLength = 1
  elif restraintType == 'Dihedral':
    itemLength = 4
  else:
    raise ValueError("Restraint list named %s not recognized by code (BUG2?)" % className)

  # Make new ConstraintList
  params = {'constraintType':restraintType, 'itemLength':itemLength}
  for tag in ('name', 'details', 'potentialType', 'unit', 'usedForCalculation', 'experimentSerial',
              'measureListSerial', 'origin', 'tensorIsotropicValue', 'tensorMagnitude',
              'tensorRhombicity', 'tensorChainCode', 'tensorSequenceCode', 'tensorResidueType'):
    if hasattr(constraintList, tag):
      val = getattr(constraintList, tag)
      if val is not None:
        params[tag] = getattr(constraintList, tag)
  # RESETS:
  # reset name to unique string, to free the name to give to new ConstraintList:
  constraintList.name = '@@@%s' % constraintList.serial
  if restraintType == 'HBond':
    # RESET: HBond lists are type 'Distance' origin 'hbond'
    restraintType = params['constraintType'] = 'Distance'
    params['origin'] = 'hbond'

  newList = constraintStore.newGenericConstraintList(**params)

  constraintStore.root.override = True
  constraintTags = ('serial', 'origData', 'details')
  contributionTags = ('serial', 'weight', 'targetValue', 'error',
                      'upperLimit', 'lowerLimit', 'additionalUpperLimit', 'additionalLowerLimit',
                      'combinationId', )
  contributionTags2 = ('scale', 'isDistanceDependent')
  try:

    for constraint in constraintList.sortedConstraints():
      # Make new Constraint
      params = {}
      for tag in constraintTags:
        if hasattr(constraint, tag):
          val = getattr(constraint, tag)
          if val is not None:
            params[tag] = val
      # params = {tag:getattr(constraint,tag) for tag in constraintTags}
      if hasattr(constraint, 'vectorLength'):
        params['vectorLength'] = constraint.vectorLength
      newConstraint = newList.newGenericConstraint(**params)

      for peakContrib in constraint.sortedPeakContribs():
        dd = {}
        for tag in ('experimentSerial', 'dataSourceSerial', 'peakListSerial', 'peakSerial'):
          dd[tag] = getattr(peakContrib, tag)
        newConstraint.newConstraintPeakContrib(**dd)

      for contribution in constraint.sortedContributions():
        # Make new Contribution
        params = {}
        for tag in contributionTags + contributionTags2:
          if hasattr(contribution, tag):
            val = getattr(contribution, tag)
            if val is not None:
              params[tag] = val
        # params = {tag:getattr(contribution,tag) for tag in contributionTags}
        # for tag in contributionTags2:
        #   if hasattr(contribution, tag):
        #     params[tag] = getattr(contribution, tag)
        newContribution = newConstraint.newGenericContribution(**params)

        for item in contribution.items:
        # Make new Item
          if itemLength == 1:
            newContribution.newSingleAtomItem(resonance=item.resonance)
          elif itemLength == 4:
            newContribution.newFourAtomItem(resonances=item.resonances)
          else:
            # assert itemLength == 2
            newContribution.newAtomPairItem(resonances=item.resonances)

    # delete old list and copy across serial
    serial = constraintList.serial
    tempSerial = newList.serial
    constraintList.delete()
    newList.__dict__['serial'] = serial
    constraintStore.__dict__['constraintLists'][serial] = newList
    del constraintStore.__dict__['constraintLists'][tempSerial]
    constraintStore.__dict__['_serialDict']['constraintLists'] -= 1
  finally:
    constraintStore.root.override = False



def findSpinSystemStretch(resonanceGroup, excludedSpinSystems=set()):
  """Find (one of the) longest sequential spin system stretch(es) containing resonanceGroup
  """

  # To avoid modifying external data
  excludedSpinSystems = excludedSpinSystems.copy()
  excludedSpinSystems.add(resonanceGroup)

  stretches = []

  for delta in (-1,1):
    queue = [resonanceGroup]
    dd = {resonanceGroup:[]}
    for rg in queue:
      ll = dd[rg]
      for rg2 in findConnectedSpinSystems(rg, delta):
        if rg2 not in excludedSpinSystems:
          excludedSpinSystems.add(rg2)
          queue.append(rg2)
          ll2 = dd[rg2] = ll.copy()
          ll2.append(rg2)

    stretch = []
    for ll3 in sorted(dd.values()):
      if len(ll3) > len(stretch):
        stretch = ll3
    #
    stretches.append(stretch)
  #
  result = list(reversed(stretches[0])) + [resonanceGroup] + stretches[1]
  return result


def getSeqSpinSystemLinks(spinSystem, delta=None):
  """
  Get any sequential spin system links (resonanceGroupProbs).
  An optional sequence offset may be specified.

  .. describe:: Input

  Nmr.ResonanceGroup, Int

  .. describe:: Output

  List of Nmr.ResonanceGroupProbs
  """

  seqLinks = {}
  for link in spinSystem.findAllResonanceGroupProbs(linkType='sequential', isSelected=True):
    if delta is None:
      seqLinks[link] = None

    elif link.sequenceOffset == delta:
      seqLinks[link] = None

  for link in spinSystem.findAllFromResonanceGroups(linkType='sequential', isSelected=True):
    if delta is None:
      seqLinks[link] = None

    elif link.sequenceOffset == -delta:
      seqLinks[link] = None

  return seqLinks.keys()


def findConnectedSpinSystems(spinSystem, delta=None):
  """
  Find spin systems sequentially connected to the input one with given sequence offset.

  .. describe:: Input

  Nmr.ResonanceGroup, Int
  .. describe:: Output

  Nmr.ResonanceGroup
  """

  result = []

  for link in getSeqSpinSystemLinks(spinSystem, delta=delta):
    if spinSystem is link.parent:
      result.append(link.possibility)
    else:
      result.append(link.parent)
  #
  return result


def  findIdentityResonanceGroup(resonanceGroup):
  """V2: find unique resonanceGroup linked as identical to teh input"""
  ll = resonanceGroup.findAllResonanceGroupProbs(linkType='identity',
                                                  isSelected=True)
  identicals = list(x.possibility for x in ll)
  ll2 = resonanceGroup.findAllFromResonanceGroups(linkType='identity',
                                                  isSelected=True)
  identicals.extend(x.parent for x in ll2)
  if len(identicals) == 1:
    return identicals[0]
  else:
    return None

def _getAmbigProchiralLabel(resonance):
  """
  V2: Deterimine if an ambigous prochiral resonance (non-stereospecifically assigned)
  Has an "a" label or a "b" label. "a" is reserved for the upfield proton and any
  other nulceus bound to it.

  .. describe:: Input

  Nmr.Resonance

  .. describe:: Output

  Character
  """

  letter = ''
  if hasattr(resonance, 'onebond'):
    del resonance.onebond

  resonanceSet = resonance.resonanceSet

  if resonanceSet:
    if resonance.isotopeCode == '1H':
      data = []
      for resonance2 in resonanceSet.sortedResonances():
        if resonance2.shifts:
          data.append( (resonance2.findFirstShift().value, resonance2.serial, resonance2) )
        else:
          data.append( (999999.999, resonance2.serial, resonance2) )

      data.sort()
      resonances = [x[2] for x in data]
      i = resonances.index(resonance)
      letter = chr(ord('a')+i)

    else:
      resonance2 = _getOnebondResonance(resonance, isotopeCode='1H')

      if resonance2 and resonance2.resonanceSet and (len(resonance2.resonanceSet.atomSets) > 1):
        letter = _getAmbigProchiralLabel(resonance2)
        resonance2.onebond = resonance

      elif (len(resonanceSet.resonances) > 1) and (len(resonanceSet.atomSets) > 1):
        for resonance2 in resonanceSet.resonances:
          if resonance2 is not resonance:
            resonance3 = _getOnebondResonance(resonance2)
            if (resonance3 and resonance3.resonanceSet
                and (len(resonance3.resonanceSet.atomSets) > 1)):
              letter = 'b'
            break

      if not letter:
        data = []
        for resonance2 in resonanceSet.resonances:
          if resonance2.shifts:
            data.append( (resonance2.findFirstShift().value,resonance2) )
          else:
            data.append( (resonance2.serial,resonance2) )

        data.sort()
        resonances = [x[1] for x in data]
        i = resonances.index(resonance)
        letter = chr(ord('a')+i)

  #keyword = 'ambigProchiralLabel'
  #appData = resonance.findFirstApplicationData(application=app, keyword=keyword)
  #
  #if appData and (appData.value != letter):
  #  appData.delete()
  #  appData = None
  #
  #if not appData:
  #  AppDataString(resonance,application=app,keyword=keyword, value=letter)

  return letter


def _getOnebondResonance(resonance, isotopeCode=None):
  """
  V2: Find any resonance that may have a single bond connection to the input resonance
  Option to specify the isotope type

  .. describe:: Input

  Nmr.Resonance, Nmr.Resonance.isotopeCode

  .. describe:: Output

  Nmr.Resonance
  """

  resonances = _getBoundResonances(resonance)
  if resonances:
    if isotopeCode:
      for resonance1 in resonances:
        if resonance1.isotopeCode == isotopeCode:
          return resonance1

    else:
      return resonances[0]

  resonance2 = None

  for contrib in resonance.peakDimContribs:
    peakDim      = contrib.peakDim
    expDimRef1   = peakDim.dataDimRef.expDimRef
    expTransfers = expDimRef1.expTransfers

    for expTransfer in expTransfers:
      if expTransfer.transferType in ('onebond','CP'):
        expDimRef2 = None

        for expDimRef in expTransfer.expDimRefs:
          if expDimRef is not expDimRef1:
            expDimRef2 = expDimRef
            break

        if expDimRef2:
          if (not isotopeCode) or (isotopeCode in expDimRef2.isotopeCodes):
            for peakDim2 in peakDim.peak.peakDims:
              if peakDim2.dataDimRef and (peakDim2.dataDimRef.expDimRef is expDimRef2):
                for contrib2 in peakDim2.peakDimContribs:
                  if (not isotopeCode) or (contrib2.resonance.isotopeCode == isotopeCode):
                    resonance2 = contrib2.resonance

                break

    if resonance2:
      break

  return resonance2



def _getBoundResonances(resonance, recalculate=False, contribs=None, recursiveCall=False):
  """
  V2: Find all resonances that have a single bond connection to the input resonance
  Option to recalculate given assignment status (e.g. if something changes)
  Option to specify peakDimContribs to search

  .. describe:: Input

  Nmr.Resonance, Boolean, List of Nmr.PeakDimContribs

  .. describe:: Output

  List of Nmr.Resonances
  """

  if (not recalculate) and resonance.covalentlyBound:
    return list(resonance.covalentlyBound)

  resonances = set() # Linked by bound atoms irrespective of spectra
  pairResonances = set() # prochiral or other pairs that can not be determined imemdiately
  resonanceSet   = resonance.resonanceSet

  funnyResonances = set()

  if resonanceSet:
    #residue  = resonanceSet.findFirstAtomSet().findFirstAtom().residue
    atomSets = resonanceSet.atomSets

    for atomSet in atomSets:
      #for atom in atomSet.atoms:
      atom = atomSet.findFirstAtom()

      for atom2 in _getBoundAtoms(atom):
        atomSet2 = atom2.atomSet

        if atomSet2 and atomSet2.resonanceSets:

          usePaired = False
          if len(atomSets) > 1:
            chemAtomSet = atom2.chemAtom.chemAtomSet
            if chemAtomSet:
              usePaired = (chemAtomSet.isProchiral or
                           (chemAtomSet.chemAtomSet and chemAtomSet.chemAtomSet.isProchiral))

          for resonanceSet2 in atomSet2.resonanceSets:
            for resonance2 in resonanceSet2.resonances:
              if resonance2 is resonance: # should not happen
                if resonance not in funnyResonances:
                  resonance.root._logger.warning( 'in _getBoundResonances():'
                                                  'resonance %d tried to be linked to itself'
                                                  % resonance.serial)
                  funnyResonances.add(resonance)
              elif usePaired:
                pairResonances.add(resonance2)
              else:
                resonances.add(resonance2)

  if not contribs:
    contribs = resonance.peakDimContribs

  expResonances = set()
  foundBothPaired = False
  for contrib in contribs:
    peakDim      = contrib.peakDim
    expDimRef1   = peakDim.dataDimRef.expDimRef
    expTransfers = expDimRef1.expTransfers

    for expTransfer in expTransfers:
      if expTransfer.transferType == 'onebond':
        expDimRef2 = None

        for expDimRef in expTransfer.expDimRefs:
          if expDimRef is not expDimRef1:
            expDimRef2 = expDimRef
            break

        if expDimRef2:
          for peakDim2 in peakDim.peak.peakDims:
            if peakDim2.dataDimRef and (peakDim2.dataDimRef.expDimRef is expDimRef2):
              expBound = set()

              for contrib2 in peakDim2.peakDimContribs:
                if (not contrib.peakContribs) and (not contrib2.peakContribs):
                  resonance2 = contrib2.resonance

                  if resonance is not resonance2:
                    expBound.add(resonance2)

                else:
                  for peakContrib in contrib.peakContribs:
                    if peakContrib in contrib2.peakContribs:
                      resonance2 = contrib2.resonance

                      if resonance is not resonance2:
                        expBound.add(resonance2)

                      break

              if len(expBound) > 1:
                # Ambiguity
                for bound in expBound:
                  # Leave the covalently bound one
                  if bound in resonances:
                    break

                else:
                  aSet = set(x for x in expBound if x in resonance.covalentlyBound)
                  if aSet and aSet != pairResonances:
                    # Resonances found. Previously linked.
                    # Not the pairResonances. Use them
                    expResonances.update(aSet)

                  else:
                    # check presence of prochiral pairs
                    ll = [x for x in pairResonances if x in expBound]
                    if len(pairResonances) == 2 and len(ll) == 2:
                      foundBothPaired= True
                    elif ll:
                      # found some prochiral pair resonances - use them
                      expResonances.update(ll)
              else:
                expResonances.update(expBound)

  if foundBothPaired and not [x for x in expResonances if x in pairResonances]:
    # particular special case.
    # Resonance is bound to both prochiral alternatives but always as a pair.

    if recursiveCall:
      # This was called from elsewhere. We could resolve nothing, so send back to caller
      pass

    else:
      # call for sister resonances and see
      resons = resonanceSet.sortedResonances()
      newResonances = set()
      if len(resons)> 1:
        # there are sister resonances
        resons.remove(resonance)
        for reson in resons:
          boundResons = _getBoundResonances(reson, recalculate=True, contribs=contribs,
                                            recursiveCall=True)
          ll = [x for x in pairResonances if x not in boundResons]
          if not ll:
            # One sister was bound to both. Incorrect data. Bind to both here too
            newResonances.update(pairResonances)
            break
          elif len(ll) < len(pairResonances):
            # Some resonances were taken. Use the free ones.
            newResonances.update(ll)

      if newResonances:
        expResonances.update(newResonances)
      else:
        # No data anywhere to resolve which is which. Match on serials
        pairResonList = list(sorted(pairResonances, key=operator.attrgetter('serial')))
        rr = pairResonList[resonanceSet.sortedResonances().index(resonance)]
        expResonances.add(rr)


  resonances.update(expResonances)

  #if doWarning and (resonance.isotopeCode == '1H') and (len(resonances) > 1):
  #  pass

  if resonances:
    resonance.setCovalentlyBound(resonances)
  else:
    resonance.setCovalentlyBound([])

  return list(resonances)




def _getBoundAtoms(atom):
  """Get a list of atoms bound to a given atom. NB ONLY for use in upgrade
  .. describe:: Input

  MolSystem.Atom

  .. describe:: Output

  List of MolSystem.Atoms
  """

  if hasattr(atom, 'boundAtoms'):
    return atom.boundAtoms

  atoms    = []
  chemAtom = atom.chemAtom
  residue  = atom.residue

  chemAtomDict = {}
  for atom2 in residue.atoms:
    # Only atoms specific to ChemCompVar :-)
    chemAtomDict[atom2.chemAtom] = atom2

  for chemBond in chemAtom.chemBonds:
    for chemAtom2 in chemBond.chemAtoms:
      if chemAtom2 is not chemAtom:
        atom2 = chemAtomDict.get(chemAtom2)
        if atom2:
          atoms.append(atom2)

  linkEnd = residue.chemCompVar.findFirstLinkEnd(boundChemAtom=chemAtom)
  if linkEnd:
    molResLinkEnd = residue.molResidue.findFirstMolResLinkEnd(linkEnd=linkEnd)

    if molResLinkEnd:
      molResLink = molResLinkEnd.molResLink

      if molResLink:
        for molResLinkEnd2 in molResLink.molResLinkEnds:
          if molResLinkEnd2 is not molResLinkEnd:
            residue2 = residue.chain.findFirstResidue(molResidue=molResLinkEnd2.molResidue)

            if residue2:
              chemAtom2 = molResLinkEnd2.linkEnd.boundChemAtom
              atom2 = residue2.findFirstAtom(chemAtom=chemAtom2)

              if atom2:
                atoms.append(atom2)

            break

  atom.boundAtoms = atoms
  return atoms
