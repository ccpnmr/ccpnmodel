"""Upgrade code for upgrades to version 3.0.2 (intermeciate 2/3 conversion version

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2002 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon Skinner, Timothy J. Stevens, Geerten Vuister"
__license__ = ("CCPN license. See www.ccpn.ac.uk/license"
               "or ccpncore.memops.Credits.CcpnLicense for license text")
__reference__ = ("For publications, please use reference from www.ccpn.ac.uk/license"
                 " or ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification:
#=========================================================================================
__author__ = "$Author$"
__date__ = "$Date$"
__version__ = "$Revision$"

#=========================================================================================
# Start of code
#=========================================================================================

import operator
from ccpncore.util import CopyData
from ccpncore.lib import MoleculeQuery

versionSequence = ['2.0.a0', '2.0.a1', '2.0.a2', '2.0.a3', '2.0.b1', '2.0.b2', '2.0.b3',
                   '2.0.4',  '2.0.5',  '2.1.0',  '2.1.1', '2.1.2', '3.0.a1', '3.0.2']
# NBNB version 2.0.6 is a side branch, not on the main version sequence

emptyDict = {}
emptyList = []

# guids of elements that should be treated as old
# Must be kept out of map fixing till the last, as they break it.
elemsTreatedAsOld = set(())

# pairs of element guids that should be treated as matching, e.g. when
# a single element must match with several elements in subclasses
elementPairings = []


def extraMapChanges(globalMapping):
  """ Extra map changes specific for a given step
  """
  pass

  # # Text type disappears and is replaced by String
  # globalMapping['loadMaps']['IMPL.Text'] = globalMapping['loadMaps']['IMPL.String']
  # globalMapping['IMPL']['abstractTypes']['Text'] = globalMapping['IMPL']['abstractTypes']['String']
  # textTypeGuid = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00036'
  # stringTypeGuid = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00035'
  # globalMapping['mapsByGuid'][textTypeGuid] = globalMapping['mapsByGuid'][stringTypeGuid]
  #
  # # Double type disappears and is replaced by Float
  # globalMapping['loadMaps']['IMPL.Double'] = globalMapping['loadMaps']['IMPL.Float']
  # globalMapping['IMPL']['abstractTypes']['Double'] = globalMapping['IMPL']['abstractTypes']['Float']
  # doubleTypeGuid = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00030'
  # floatTypeGuid = 'www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031'
  # globalMapping['mapsByGuid'][doubleTypeGuid] = globalMapping['mapsByGuid'][floatTypeGuid]
  #
  # #ShiftReference.indirectShiftRatio
  # guid = 'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:12_00012'
  # dd = globalMapping['mapsByGuid'].get(guid)
  # if dd:
  #   dd['data'] = globalMapping['mapsByGuid']['www.ccpn.ac.uk_Fogh_2006-08-16-14:22:53_00031']
  #   if 'proc' in dd:
  #     del dd['proc']  # should not be 'proc':'delay' after all.




def correctData(topObj, delayDataDict, toNewObjDict, mapping=None):
  """ update topObj object tree using information in delayDataDict
  May be used either to postprocess a file load (minor upgrade)
  or as part of an in-memory data transfer (major upgrade)

  topObj is the MemopsRoot in the new tree
  toNewObjDict is _ID:newObj for minor
    and oldObj/oldObjId:newObj for major upgrades
  """

  doGet = delayDataDict.get
  pName = topObj.packageName

def correctFinalResult(memopsRoot):
  """Correct final result in situ, after loading has finished
  NOT part of standard compatibility process, but a special case for upgrade from v2 to v3 """

  # Copy across molSystem chains so all NmrAProjects have only one MolSystem
  molSystemMap = {}
  chainMap = {}
  for nmrProject in memopsRoot.sortedNmrProjects():
    molSystemCounts =  getNmrMolSystems(nmrProject)
    if not molSystemCounts:
      continue

    for ms in molSystemCounts:
      mainMolSystem = molSystemMap.get(ms)
      if mainMolSystem:
        break
    else:
      # select main system as the most common
      sentinel = -1
      for molSystem, count in sorted(molSystemCounts.items()):
        if count > sentinel:
          mainMolSystem = molSystem
          sentinel = count
      molSystemMap[mainMolSystem] = mainMolSystem

    # Overlap with previous molSystem set - merge into previous system.
    for molSystem in molSystemCounts:
      if molSystem not in molSystemMap:
        molSystemMap[molSystem] = mainMolSystem
      copyMolSystemContents(molSystem, mainMolSystem, chainMap=chainMap)

    # Fix constraint lists
    for nmrConstraintStore in nmrProject.sortedNmrConstraintStores():
      for constraintList in nmrConstraintStore.sortedConstraintLists():
        className = constraintList.className
        restraintType = className[:-14]
        newContribution = 'new%sContribution' % restraintType
        newItem = 'new%sItem' % restraintType

        if restraintType in ('Distance', 'HBond', 'JCoupling', 'Rdc',):
          #ix pairwise restraints
          for constraint in constraintList.sortedConstraints():

            # Make new Contribution
            dd = dict((x,getattr(constraint,x))
                      for x in ('targetValue', 'error', 'upperLimit', 'lowerLimit'))
            contribution = getattr(constraint, newContribution)(**dd )

            # Transfer resonances to new Items objects and delete old ones.
            for constraintItem in constraint.sortedItems():
              getattr(contribution, newItem)(resonances=constraintItem.resonances)
              constraintItem.delete()

        elif restraintType in ('Csa', 'ChemShift'):
          #ix pairwise restraints
          for constraint in constraintList.sortedConstraints():

            # Make new Contribution
            dd = dict((x,getattr(constraint,x))
                      for x in ('targetValue', 'error', 'upperLimit', 'lowerLimit'))
            contribution = getattr(constraint, newContribution)(**dd )

            # Transfer resonances to new Items objects and delete old ones.
            getattr(contribution, newItem)(resonance=constraint.resonance)

        elif restraintType == 'Dihedral':
          #ix dihedral restraints
          for constraint in constraintList.sortedConstraints():
            resonances = constraint.resonances
            for constraintItem in constraint.sortedItems():
              # Make new Contribution
              dd = dict((x,getattr(constraintItem,x))
                        for x in ('targetValue', 'error', 'upperLimit', 'lowerLimit'))
              contribution = getattr(constraint, newContribution)(**dd )
              getattr(contribution, newItem)(resonances=resonances)
              constraintItem.delete()

        else:
          raise ValueError("Restraint list named %s not recognized by code (BUG?)" % className)

    # Transfer assignments
    transferAssignments(chainMap, nmrProject)

def getResonanceGroupStretch(startingGroup):
  """get stretch of connected resonanceGroups, only counting +/- 1 links"""
  sequentialLinks = startingGroup.findAllResonanceroupProbs(linkType='sequential', isSelected=True)



def transferAssignments(chainMap, nmrProject):
  """transfer assignments to new form"""

  # Make default chain and residue
  defaultNmrChain = nmrProject.newNmrChain(code='@')
  defaultResonanceGroup = nmrProject.newResonanceGroup(nmrChain=defaultNmrChain,
                                                       seqInsertCode = '@',
                                                       details="default ResonanceGroup")

  # first deal with NmrChains and ResonanceGroups
  assignedResonanceGroups  = []
  for resonanceGroup in nmrProject.sortedResonanceGroups():

    # Find residue
    residue = resonanceGroup.residue
    if residue is None:
      ll = []
      for residueProb in resonanceGroup.residueProbs:
        if residueProb.weight:
          ll.append(residueProb)
      if len(ll) == 1:
        residue = ll[0].possibility

    if residue:
      assignedResonanceGroups.add(resonanceGroup)

      # use residue to set values
      chain = chainMap[residue.chain]
      # get residue in new chain
      residue = chain.findFirstResidue(seqCode=residue.seqCode,
                                       seqInsertCode=residue.seqInsertCode)
      chainCode = chain.code
      nmrChain =(nmrProject.findFirstNmrChain(code=chainCode) or
                 nmrProject.newNmrChain(code=chainCode))
      resonanceGroup.nmrChain = nmrChain
      seqCode = residue.seqCode
      seqInsertCode = residue.seqInsertCode.strip() or None
      oldResonanceGroup = nmrChain.findFirstResonanceGroup(seqCode=seqCode,
                                                           seqInsertCode=seqInsertCode)
      if oldResonanceGroup:
        # We had that residue already - move resonances to the old one
        for resonance in resonanceGroup.resonances:
          resonance.resonanceGroup = oldResonanceGroup
      else:
        # Set values from residue
        for tag in ('seqCode', 'seqInsertCode', 'molType', 'ccpCode', 'linking', 'descriptor'):
          setattr(resonanceGroup, tag, getattr(residue, tag))
        resonanceGroup.residueType = residue.code3Letter

  # for resonanceGroup in assignedResonanceGroups:
  #
  #   probs = resonanceGroup.findAllResonancGroupProbs(isSelected=True)
  #
  #   for prob in probs:
  #     resonanceGroup2 = prob.possibility
  #     if resonanceGroup2 not in assignedResonanceGroups:
  #       if prob.linkType == 'sequential':
  #         offset = prob.sequenceOffset



    # else:
    #   # unassigned residue
    #   # NBNB TBD
    #   # NBNB need to allow for +1/-1 offsets HOW IS THAT STORED?
    #
    #   # where there is NOT any offset you get this:
    #   resonanceGroup.seqInsertCode = '@' + str(resonanceGroup.serial)
    #   resonanceGroup.nmrChain = defaultNmrChain
    #   chemComp = resonanceGroup.chemComp
    #   if chemComp:
    #     resonanceGroup.residueType = chemComp.code3Letter


  # Now for assigned resonances

  for resonanceSet in nmrProject.sortedResonanceSets():
    # Assigned resonances take priority over unassigned ones
    _assignResonanceSet(nmrProject, resonanceSet, chainMap, defaultResonanceGroup)

  # Now unassigned resonances
  for resonance in nmrProject.resonances:
    if resonance.resonanceSet is None:
      # Resonance is unassigned

      resonanceGroup = resonance.resonanceGroup

      if resonanceGroup is None:
        # Ungrouped resonance. Put in default group, and give name ending in '@<serial>'
        resonance.resonanceGroup = defaultResonanceGroup
        resonanceName = str(resonance.serial)
        ss = resonance.name
        if ss and resonanceName not in ss:
          # guard against having resonance.serial in the name twice
          resonance.name = '%s@%s' % (ss, resonanceName)
        else:
          resonance.name = '@' + resonanceName

      else:
        # grouped, unassigned resonance
        resonanceName = resonance.name
        if resonanceName:
          # Resonance has a name. Use it.

          # Check if name would give a full assignment, and if so modify it
          chain = resonanceGroup.nmrChain.chain
          if chain is not None and resonanceGroup.relativeOffset is None:
            residue = chain.findFirstResidue(seqCode=resonanceGroup.seqCode,
                                             seqInsertCode=(resonanceGroup.seqInsertCode or ' '))
            if residue is not None:
              if residue.findFirstAtom(resonanceName) is not None:
                resonanceName += '?'

          if [x for x in resonanceGroup.resonances if x.name==resonanceName and x is not resonance]:
            # There is another resonance with the same name - add resonance serial
            resonanceName = '%s@%s' % (resonanceName, resonance.serial)

        else:
          resonanceName = '@' + str(resonance.serial)

        # Set the name
        resonance.name = resonanceName


  # Then for FixedResonances
  for nmrConstraintStore in nmrProject.sortedNmrConstraintStores():
    for resonanceSet in nmrConstraintStore.sortedFixedResonanceSets():
      _assignResonanceSet(nmrProject, resonanceSet, chainMap, defaultResonanceGroup)

def _assignResonanceSet(nmrProject, resonanceSet, chainMap, defaultResonanceGroup):
  """Assign resonances in resonance Set or fixedResonanceSet"""

  # set up some parameters
  resonances = resonanceSet.sortedResonances()
  atomSets = resonanceSet.sortedAtomSets()
  chemAtomSet = getChemAtomSetFromAtomSets(atomSets)
  allAtoms = [x for y in atomSets for x in y.atoms]
  if len(set(x.residue for x in allAtoms)) == 1:
    oldResidue = allAtoms[0].residue
  else:
    oldResidue = None

  if oldResidue:

    # Find or make nmrChain
    chain = chainMap[oldResidue.chain]
    # get residue in new chain
    residue = chain.findFirstResidue(seqCode=oldResidue.seqCode,
                                     seqInsertCode=oldResidue.seqInsertCode)
    chainCode = chain.code
    nmrChain =(nmrProject.findFirstNmrChain(code=chainCode) or
               nmrProject.newNmrChain(code=chainCode))

    # make or find resonanceGroup
    seqCode = residue.seqCode
    seqInsertCode = residue.seqInsertCode.strip() or None
    resonanceGroup = nmrChain.findFirstResonanceGroup(seqCode=seqCode,
                                                      seqInsertCode=seqInsertCode)
    if resonanceGroup is None:
      resonanceGroup = nmrChain.newResonanceGroup()
      for tag in ('seqCode', 'seqInsertCode', 'molType', 'ccpCode', 'linking', 'descriptor'):
        setattr(resonanceGroup, tag, getattr(residue, tag))
      resonanceGroup.residueType = residue.code3Letter

    if chemAtomSet and len(atomSets) == 2 and len(resonances) <= 2:
      # prochiral pair. Use getAmbigProchiralLabel for priority, and set 'X' for 'a', 'Y' for 'b'
      # NB atoms are sorted by name
      useNewAtoms = [x for x in residue.sortedAtoms()
                     if x.atomType == 'nonstereo' and x.atomSetName == chemAtomSet.name]
      for resonance in resonances:
        if getAmbigProchiralLabel(resonance) == 'a': # NBNB TBD not for fixedResonance
          resonanceName = useNewAtoms[0].name
        else:
          resonanceName = useNewAtoms[1].name

        oldResonance = resonanceGroup.findFirstResonance(name=resonanceName)
        if oldResonance is None:
          resonance.resonanceGroup = resonanceGroup
          resonance.name = resonanceName
        else:
          # NBNB TBD merge resonances
          # NBNB TBD different for fixed
          pass

    elif len(resonances) == 1:

      resonance = resonances[0]
      if len(atomSets) == 1:
        # simple one-to-one stereospecific assignment
        if chemAtomSet:
          # assignment to atomSet
          resonanceName = residue.findFirstAtom(atomType='equivalent',
                                                atomSetName=chemAtomSet.name).name
        else:
          #asssignment to single atom
          resonanceName = atomSets.sortedAtoms()[0].name

      else:
        # multiple atomSets

        if len(allAtoms) == len(residue.findAllAtoms(atomType='single')):
          # All single atoms in residue
          resonanceName = '*'

        else:
          nuc = allAtoms[0].elementSymbol
          if (all((x.elementSymbol == nuc) for x in allAtoms) and
              len(residue.findAllAtoms(elementSymbol=nuc, atomType='single')) == len(allAtoms)):
            # All atoms of a given nucleus
            resonanceName = 'nuc' + '*'

          else:
            # random multiple atom selection
            resonanceName = '/'.join(sorted((str(x.name) for x in atomSets)))

      # Set resonance group and name
      oldResonance = resonanceGroup.findFirstResonance(name=resonanceName)
      if oldResonance is None:
        resonance.resonanceGroup = resonanceGroup
        resonance.name = resonanceName
      else:
        # NBNB TBD merge resonances
        pass

    else:
      # multiple resonances not matching chemAtomSet
      atomsName = '/'.join(sorted((str(x.name) for x in atomSets)))
      for resonance in resonances:
        # NB this name can not be in use already, so we do not need to check
        resonance.resonanceGroup = resonanceGroup
        resonance.name = '%s@%s' % (atomsName, resonance.serial)

  else:
    # assigned to multiple residues - cannot be helped
    # Same naming style for single and multiple resonances
    ll = [(str(x.findFirstAtom().residue.seqCode), str(x.name)) for x in atomSets]
    resonanceName = '/'.join('%s-%s' % tt for tt in sorted(ll))
    for resonance in resonances:
      resonance.name = '%s@%s' % (resonanceName, resonance.serial)
      resonance.resonanceGroup = defaultResonanceGroup
      print('WARNING - resonance %s reassigned to @.@.%s' % (resonance.serial, resonance.name))


def getOnebondResonance(resonance, isotopeCode=None):
  """
  Find any resonance that may have a single bond connetion to the input resonance
  Option to specify the isotope type

  .. describe:: Input

  Nmr.Resonance, Nmr.Resonance.isotopeCode

  .. describe:: Output

  Nmr.Resonance
  """

  resonances = getBoundResonances(resonance)
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



def getBoundResonances(resonance, recalculate=False, contribs=None, recursiveCall=False):
  """
  Find all resonances that have a single bond connection to the input resonance
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

      for atom2 in MoleculeQuery.getBoundAtoms(atom):
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
                  print( 'WARNING: in getBoundResonances(): resonance %d tried to be linked to itself' % resonance.serial)
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
      if expTransfer.transferType in ('onebond','CP'):
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
    # Resonnce is bound to both prochiral altrnatives but always as a pair.

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
          boundResons = getBoundResonances(reson, recalculate=True, contribs=contribs, recursiveCall=True)
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



def getAmbigProchiralLabel(resonance):
  """
  Deterimine if an ambigous prochiral resonance (non-stereospecifically assigned)
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
          data.append( ('%f%d' % (resonance2.findFirstShift().value,resonance2.serial),resonance2) )
        else:
          data.append( (resonance2.serial,resonance2) )

      data.sort()
      resonances = [x[1] for x in data]
      i = resonances.index(resonance)
      letter = chr(ord('a')+i)

    else:
      resonance2 = getOnebondResonance(resonance, isotopeCode='1H')

      if resonance2 and resonance2.resonanceSet and (len(resonance2.resonanceSet.atomSets) > 1):
        letter = getAmbigProchiralLabel(resonance2)
        resonance2.onebond = resonance

      elif (len(resonanceSet.resonances) > 1) and (len(resonanceSet.atomSets) > 1):
        for resonance2 in resonanceSet.resonances:
          if resonance2 is not resonance:
            resonance3 = getOnebondResonance(resonance2)
            if resonance3 and resonance3.resonanceSet and (len(resonance3.resonanceSet.atomSets) > 1):
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
  #app     = 'Analysis'
  #appData = resonance.findFirstApplicationData(application=app, keyword=keyword)
  #
  #if appData and (appData.value != letter):
  #  appData.delete()
  #  appData = None
  #
  #if not appData:
  #  AppDataString(resonance,application=app,keyword=keyword, value=letter)

  return letter

def copyMolSystemContents(molSystem, toMolSystem, chainMap=None):
  """Copy MolSystem contents into a pre-existing MolSystem
   NB chainMap is an in/out parameter DESIGNED to be modified."""

  molSystemCode = molSystem.code

  if chainMap is None:
    chainMap = {}

  # copy chains across
  newChains = []
  for chain in molSystem.sortedChains():
    newCode = '-'.join((molSystemCode, chain.code))
    newChain = CopyData.copySubTree(chain, molSystem, topObjectParameters={'code':newCode,},
                                    maySkipCrosslinks=True)
    chainMap[chain] = newChain
    newChains.append(newChain)

  # copy ChainInteractions
  for chainInteraction in molSystem.sortedChainInteractions():
    chains = [chainMap[x] for x in chainInteraction.chains]
    toMolSystem.newChainInteraction(chains=chains,
                                    interactionType=chainInteraction.interactionType)

  # copy StructureGroups
  for structureGroup in molSystem.sortedStructureGroups():
    CopyData.copySubTree(structureGroup, toMolSystem, maySkipCrosslinks=True)

  # relink StructureEnsembles
  for structureEnsemble in molSystem.structureEnsembles:

    # reset chainCode
    for coordChain in structureEnsemble.coordChains:
      parentDict = structureEnsemble.__dict__['coordChains']
      del parentDict[coordChain.code]
      newCode = chainMap[coordChain.chain].code
      coordChain.__dict__['code'] = newCode
      parentDict[newCode] = coordChain

  # reset molSystem link
    molSystem.root.override=True
    try:
      structureEnsemble.molSystem = toMolSystem
    finally:
      molSystem.root.override = False

  # Fix NmrCalc instances
  for nmrCalcStore in molSystem.root.sortedNmrCalcStores():
    for run in nmrCalcStore.sortedRuns():
      for obj in run.findAllData(molSystemCode=molSystemCode):
        className = obj.className
        if className == 'MolSystemData':
          obj.chains = newChains
        elif className == 'MolResidueData':
          newResidues = []
          for residue in obj.residues:
            newResidue = chainMap[residue.chain].findFirstResidue(seqId=residue.seqId)
            newResidues.append(newResidue)
          obj.residues = newResidues
        elif className == 'StructureEnsembleData':
          obj.molSystemCode = toMolSystem.code

  # NBNB TBD Nmr assignments and FixedResonances

def expandMolSystemAtoms(molSystem):
  """Add extra atoms corresponding to \AtomSets"""

  # Set elementSymbol and add missing atoms (lest something breaks lower down)
  for chain in molSystem.sortedChains():
    for residue in chain.soredResidues():
      chemCompVar = residue.chemCompVar
      for chemAtom in chemCompVar.findAllChemAtoms(className='ChemAtom'):
        atom = residue.findFirstAtom(name=chemAtom.name)
        if atom is None:
          residue.newAtom(name=chemAtom.name, atomType='single',
                          elementSymbol=chemAtom.elmentSymbol)
        else:
          atom.elementSymbol = chemAtom.elmentSymbol


  # Set boundAtoms for existing atoms within residue
  for chain in molSystem.sortedChains():
    for residue in chain.soredResidues():
      chemCompVar = residue.chemCompVar
      for atom in residue.atoms:
        chemAtom = chemCompVar.findFirstChemAtom(name=atom.name, className='ChemAtom')
        if chemAtom is not None:
          boundChemAtoms = set(x for y in chemAtom.chemBonds for x in y.chemAtoms)
          for boundChemAtom in boundChemAtoms:
            if boundChemAtom is not chemAtom and boundChemAtom.className == 'ChemAtom':
              boundAtom = residue.findFirstAtom(name=boundChemAtom.name)
              if boundAtom is not None and boundAtom not in atom.boundAtoms:
                atom.addBoundAtom(boundAtom)

    # Add boundAtoms for MolResLinks
      for molResLink in chain.molecule.molResLinks:
        ff = chain.findFirstResidue
        atoms = [ff(seqId=x.molResidue.seqId).findFirstAtom(name=x.linkEnd.boundChemAtom.name)
                 for x in molResLink.molResLinkEnds]
        atoms[0].addBoundAtom(atoms[1])

  # Add boundAtoms for MolSystemLinks
  for molSystemLink in molSystem.molSystemLinks:
    atoms = [x.residue.findFirstAtom(name=x.linkEnd.boundChemAtom.name)
             for x in molSystemLink.molSystemLinkEnds]
    atoms[0].addBoundAtom(atoms[1])

  # NB we do NOT add boundAtoms for NonCovalentBonds

  # Add extra atoms corresponding to ChemAtomSets
  for chain in molSystem.sortedChains():
    for residue in chain.soredResidues():
      chemCompVar = residue.chemCompVar
      pseudoNamingSystem = chemCompVar.chemComp.findFirstNamingSystem(name='AQUA')

      # Map from chemAtomSet to equivalent Atom
      casMap = {}

      # map from chemAtomSet.name to nonStereo names
      nonStereoNames = {}

      for chemAtomSet in chemCompVar.chemAtomSets:

        # get nests of connected chemAtomSets
        if not chemAtomSet.chemAtomSet:
          # get nested chemAtomSets, starting at topmost set
          localSets = [chemAtomSet]
          for cas in localSets:
            localSets.extend(cas.chemAtomSets)

          # Process in reverse order, guaranteeing that contained sets are always ready
          for cas in reversed(localSets):
            chemContents = cas.sortedChemAtoms()
            if chemContents:
              # contents are real atoms
              components = [residue.findFirstAtom(name=x.name) for x in chemContents]
            else:
              chemContents = cas.sortedChemAtomSets()
              components = [casMap[x] for x in chemContents]
            elementSymbol = chemContents[0].elementSymbol

            commonBound = set.intersection(*(x.boundAtoms for x in components))

            # Add 'equivalent' atom
            newName = cas.name.replace('*', '#')
            newAtom = residue.newAtom(name=newName, atomType='equivalent',
                                      elementSymbol=elementSymbol,atomSetName=cas.name,
                                      components=components, boundAtoms=commonBound)
            casMap[cas] = newAtom

            # Add 'pseudo' atom for proton
            if elementSymbol == 'H':
              newName = None
              if pseudoNamingSystem:
                atomSysName = pseudoNamingSystem.findFirstAtomSysName(atomName=cas.name,
                                                                      atomSubType=cas.subType)
                if atomSysName:
                  newName = atomSysName.sysName

              if newName is None:
                # No systematic pseudoatom name found - make one.
                # NBNB this will give names like MD1, QG1, MD2 for cases like Ile delta,
                # where the standard says MD, QG, MG.
                # But all the standard cases are covered by the pseudoNamingSystem ('AQUA')
                # Can we get away with this, or do we have to rename on a per-residue basis
                # for the special cases?
                startChar = 'Q'
                if (len(cas.chemAtoms) == 3 and cas.isEquivalent
                    and components[0].findFirstBoundAtom().elementSymbol == 'C'):
                  if len(set(x.findFirstBoundAtom() for x in components)) == 1:
                    # This is a methyl group
                    # The second 'if' is likely unnecessary in practice, but let us be correct here
                    startChar = 'M'

                newName = startChar + cas.name.strip('*')[1:]

              if len(newName) > 1:
                # Make pseudoatom, except for 'H*'
                residue.newAtom(name=newName, atomType='pseudo', elementSymbol=elementSymbol,
                                atomSetName=cas.name, components=components, boundAtoms=commonBound)

            # Add 'nonstereo atoms
            if not cas.isEquivalent and len(components) == 2:
              # NB excludes cases with more than two non-equivalent components
              # But then I do not think there are any in practice.
              # and anyway we do not have a convention for them.
              nonStereoNames[cas.name] = newNames = []
              starpos = cas.name.find('*')
              for ii,component in enumerate(components):
                # NB components are sorted by key, which means by name
                newChar = 'XY'[ii]
                ll = list(component.name)
                ll[starpos] = newChar
                newName = ''.join(ll)
                newNames.append(newName)
                residue.newAtom(name=newName, atomType='nonstereo', elementSymbol=elementSymbol,
                                atomSetName=cas.name, components=components, boundAtoms=commonBound)
      # NBNB Now we need to set boundAtoms for non-single Atoms.
      # We need to set:
      # HG*-CG* etc.
      # HGX*-CGX etc. - can be done from previous by char substitution
      eqvTypeAtoms = [x for x in residue.sortedAtoms() if x.atomType == 'equivalent']
      for ii,eqvAtom in enumerate(eqvTypeAtoms):
        components = eqvAtom.sortedComponents()
        for eqvAtom2 in eqvTypeAtoms[11+1:]:
          components2 = eqvAtom2.sortedComponents()
          if len(components) == len(components2):
            if all((x in components2[ii].boundAtoms) for ii,x in enumerate(components)):
              # All components of one are bound to a component of the other
              # NB this relies on the sorted components being ordered to match the bonds
              # but you should expect that both cases are sorted by branch index
              # CG1,CG2 matching HG1*,HG2* etc.

              # Add bond between equivalent atoms
              eqvAtom.addBoundAtom(eqvAtom2)

              nsNames1 = nonStereoNames.get(eqvAtom.atomSetName)
              nsNames2 = nonStereoNames.get(eqvAtom2.atomSetName)
              if nsNames1 and nsNames2:
                # Non-stereoAtoms are defined for both - add X,Y bonds
                # NB We rely on names being sorted (X tehn Y in both cases)
                for jj,name in enumerate(nsNames1):
                  atom2 = residue.findFirstAtom(name=nsNames2[jj])
                  residue.findFirstAtom(name=name).addBoundAtom(atom2)

              break





def getNmrMolSystems(nmrProject):
  """Find MolSystems referred to in Nmr and dependent packages (NmrConstraint, NmrCalc, ...)
  and return them in rough order of maximum usage (most used first)."""

  # mainMolSystem = None
  molSystemCounts = {}

  # count assigned Resonances
  for resonance in nmrProject.resonances:
    resonanceSet = resonance.resonanceSet
    if resonanceSet:
      for molSystem in (x.topObject for y in resonanceSet.atomSets for x in y.atoms):
        count = molSystemCounts.get(molSystem, 0)
        molSystemCounts[molSystem] = count + 1

  #count assigned ResonanceGroups
  for resonanceGroup in nmrProject.resonanceGroups:
    residue = resonanceGroup.residue
    if residue:
      molSystem = residue.topObject
      count = molSystemCounts.get(molSystem, 0)
      molSystemCounts[molSystem] = count + 1

    # count chains
    for chain in resonanceGroup.chains:
      molSystem = chain.topObject
      count = molSystemCounts.get(molSystem, 0)
      molSystemCounts[molSystem] = count + 1

    # ResidueProbs
    for residueProb in resonanceGroup.residueProbs:
      molSystem = residueProb.residue.topObject
      count = molSystemCounts.get(molSystem, 0)
      molSystemCounts[molSystem] = count + 1

  # count Experiment.molSystems
  for experiment in nmrProject.experiments:
    for molSystem in experiment.molSystems:
      count = molSystemCounts.get(molSystem, 0)
      molSystemCounts[molSystem] = count + 1

  # # count ChainStateSets
  # for chainStateSet in nmrProject.chainStateSets:
  #   molSystem = chainStateSet.chain.molSystem
  #   count = molSystemCounts.get(molSystem, 0)
  #   molSystemCounts[molSystem] = count + 1
  #
  #   for residue in chainStateSet.residues:
  #     molSystem = residue.topObject
  #     count = molSystemCounts.get(molSystem, 0)
  #     molSystemCounts[molSystem] = count + 1
  #
  #   for atom in chainStateSet.atoms:
  #     molSystem = atom.topObject
  #     count = molSystemCounts.get(molSystem, 0)
  #     molSystemCounts[molSystem] = count + 1

  # count over NmrConstraintSets:
  for constraintSet in nmrProject.nmrConstraintStores:
    for resonance in constraintSet.fixedResonances:
      resonanceSet = resonance.resonanceSet
      if resonanceSet:
        for molSystem in (x.topObject for y in resonanceSet.atomSets for x in y.atoms):
          count = molSystemCounts.get(molSystem, 0)
          molSystemCounts[molSystem] = count + 1

  # count over NmrCalc
  for nmrCalcStore in nmrProject.nmrCalcStores:
    for run in nmrCalcStore.runs:

      for molSystemData in run.findAllData(className='MolSystemData'):
        molSystem = molSystemData.molSystem
        if molSystem:
          count = molSystemCounts.get(molSystem, 0)
          molSystemCounts[molSystem] = count + 1

      for molResidueData in run.findAllData(className='MolResidueData'):
        molSystem = molResidueData.molSystem
        if molSystem:
          count = molSystemCounts.get(molSystem, 0)
          molSystemCounts[molSystem] = count + 1

  return molSystemCounts

  # # select main system as the most common
  # sentinel = -1
  # for molSystem, count in sorted(molSystemCounts.items()):
  #   if count > sentinel:
  #     mainMolSystem = molSystem
  #
  # if mainMolSystem is None:
  #   return []
  # else:
  #   return [mainMolSystem] + list(x for x in molSystemCounts if x is not mainMolSystem)


def getChemAtomSetFromAtomSets(atomSets):
  """ Get a ChemAtomSet that matches all atoms in V2 atomSets

  .. describe:: Input

  List of Nmr.AtomSet or NmrConstraint.FixedAtomSet

  .. describe:: Output

  ChemComp.ChemAtomSet (or None)

  """

  atoms = []
  for atomSet in atomSets:
    atoms.extend(atomSet.atoms)

  chemAtoms = [x.chemAtom for x in atoms]
  if None in chemAtoms:
    return None

  chemAtomSets = set(x.chemAtomSet for x in chemAtoms)
  if None in chemAtomSets:
    return None

  nChemAtoms = 0
  for chemAtomSet in chemAtomSets:
    nChemAtoms += len(chemAtomSet.chemAtoms)
  if nChemAtoms != len(atoms):
    return None


  while len(chemAtomSets) > 1:
    chemAtomSets = set(x.chemAtomSet for x in chemAtomSets)
    if None in chemAtomSets:
      return None
  else:
    return chemAtomSets.pop()
