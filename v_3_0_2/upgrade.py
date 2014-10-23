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

from ccpncore.util import CopyData
from ccpncore.lib import V2Upgrade
from ccpncore.util import Common as commonUtil


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

  # Copy across molSystem chains so all NmrProjects have only one MolSystem
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

    # Add new atoms to MolSystem
    expandMolSystemAtoms(mainMolSystem)

    for nmrConstraintStore in nmrProject.sortedNmrConstraintStores():
      fixNmrConstraintStore(nmrConstraintStore, chainMap)

    # Transfer assignments in NmrProject
    transferAssignments(nmrProject, mainMolSystem, chainMap)

    # Fix pek intensities and assignments storage
    fixPeaks(nmrProject)

def fixPeaks(nmrProject):
  """Copy Peak intensity records to peak attributes,
   and assignment related attributes to new locations """

  for peakList in nmrProject.sortedPeakLists():
    for peak in peakList.sortedPeaks():

      # Copy intensity values across
      if not peak.height:
        # No good way of determining which object to take if there are multiple height objects
        # Fortunately there rarely is (Analysis used findFirst too)
        intensityObject = peak.findFirstPeakIntensity(intensityType='height')
        peak.height = intensityObject.value
        peak.heightError = intensityObject.error
      if not peak.volume:
        # No good way of determining which object to take if there are multiple height objects
        # Fortunately there rarely is (Analysis used findFirst too)
        intensityObject = peak.findFirstPeakIntensity(intensityType='volume')
        peak.volume = intensityObject.value
        peak.volumeError = intensityObject.error

      for obj in peak.peakIntensities:
        # clean up
        obj.delete()

      # Copy across PeakDimComponent data
      for peakDimComponent in peak.sortedPeakDimComponents():
        scalingFactor = peakDimComponent.scalingFactor
        annotation = peakDimComponent.annotation
        refSerial = peakDimComponent.getByNavigation('dataDimRef', 'expDimRef', 'serial')
        for peakDimContrib in peakDimComponent.peakDimContribs:
          if scalingFactor != 1.0:
            peakDimContrib.scalingFactor = scalingFactor
          if annotation:
            peakDimContrib.annotation = annotation
          if refSerial:
            peakDimContrib.expDimRefSerial = refSerial
        #
            peakDimComponent.delete()


def fixNmrConstraintStore(nmrConstraintStore, chainMap):
    """Fix NmrConstraintStore"""

    # First fix FixedResonances (so we can remap them below)
    assignmentMap = V2Upgrade.mapAllAssignments(nmrConstraintStore, chainMap=chainMap)
    assignment2Resonance = {}
    resonanceMap = {}
    for resonance, assignment in assignmentMap.items():
      resonance.chainCode = assignment[0]
      resonance.sequencCode = assignment[1]
      resonance.residueType = assignment[2]
      resonance.name = assignment[3]

      oldResonance = assignment2Resonance.get(assignment)
      if oldResonance is None:
        assignment2Resonance[assignment] = resonance
      elif oldResonance.serial > resonance.serial:
        # We want only one
        assignment2Resonance[assignment] = resonance
        resonanceMap[oldResonance] = resonance
      else:
        resonanceMap[resonance] = oldResonance


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
            assignments = [assignmentMap[resonanceMap.get(x,x)] for x in constraintItem.resonances]
            getattr(contribution, newItem)(resonances=tuple(assignment2Resonance[x]
                                                            for x in sorted(assignments)))
            constraintItem.delete()

      elif restraintType in ('Csa', 'ChemShift'):
        #ix one-resonance restraints
        for constraint in constraintList.sortedConstraints():

          # Make new Contribution
          dd = dict((x,getattr(constraint,x))
                    for x in ('targetValue', 'error', 'upperLimit', 'lowerLimit'))
          contribution = getattr(constraint, newContribution)(**dd )

          # Transfer resonances to new Items objects and delete old ones.
          rs = constraint.resonance
          getattr(contribution, newItem)(resonance=resonanceMap.get(rs,rs))

      elif restraintType == 'Dihedral':
        #ix dihedral restraints - NB these should NOT be sorted
        for constraint in constraintList.sortedConstraints():
          resonances = tuple(resonanceMap.get(x,x) for x in constraint.resonances)
          for constraintItem in constraint.sortedItems():
            # Make new Contribution
            dd = dict((x,getattr(constraintItem,x))
                      for x in ('targetValue', 'error', 'upperLimit', 'lowerLimit'))
            contribution = getattr(constraint, newContribution)(**dd )
            getattr(contribution, newItem)(resonances=resonances)
            constraintItem.delete()

      else:
        raise ValueError("Restraint list named %s not recognized by code (BUG?)" % className)

    # Remove obsolete FixedResonances, ResonanceSets and AtomSets
    for oldResonance in resonanceMap:
      oldResonance.delete()
    for fixedAtomSet in nmrConstraintStore.sortedFixedAtomSets():
      # NB this deletes FixedResonanceSets too by cascading delete.
      fixedAtomSet.delete()


def transferAssignments(nmrProject, mainMolSystem, chainMap):
  """Transfer NmrProject assignments"""

  # Get ResonanceGroup mapping
  if len(mainMolSystem.chains) == 1:
    defaultChainCode = mainMolSystem.findFirstChain().code
  else:
    defaultChainCode = '@'

  resonanceGroupMap =  V2Upgrade.mapResonanceGroups(nmrProject, chainMap=chainMap,
                                               defaultChainCode=defaultChainCode)

  # Set ResonanceGroup attributes and NmrChains, and merge duplicate ResonanceGroups
  reverseGroupMap = {}
  for resonanceGroup in nmrProject.sortedResonanceGroups():
    groupAssignment = resonanceGroupMap[resonanceGroup]

    firstResonanceGroup = reverseGroupMap.get(groupAssignment)
    if firstResonanceGroup is None:
      # new group - handle it
      reverseGroupMap[groupAssignment] = resonanceGroup

      resonanceGroup.nmrChain = (nmrProject.findFirstNmrChain(code=groupAssignment[0]) or
                                 nmrProject.newNmrChain(code=groupAssignment[0]))
      # NBNB TBD data model change required, derived, settable sequenceCode attr
      resonanceGroup.sequenceCode = groupAssignment[1]
      resonanceGroup.residueType = groupAssignment[2]

    else:
      # Merge duplicates
      for resonance in resonanceGroup.resonances:
        resonance.resonanceGroup = firstResonanceGroup
      resonanceGroup.delete()


  # Add default chain and ResonanceGroup for non-grouped resonances
  defaultNmrChain = (nmrProject.findFirstNmrChain(code=defaultChainCode) or
                         nmrProject.newNmrChain(code=defaultChainCode))
  defaultResonanceGroup = (defaultNmrChain.findFirstResonanceGroup(seqCode=None,
                                                                   seqInsertCode='@') or
                           nmrProject.newResonanceGroup(nmrChain=defaultNmrChain,
                                                       seqInsertCode = '@',
                                                       details="default ResonanceGroup"))
  resonanceGroupMap[None] = (defaultChainCode, '@', defaultResonanceGroup)

  # Now fix resonance assignments
  assignmentMap = {}
  V2Upgrade. mapAssignedResonances(nmrProject, assignmentMap, chainMap=chainMap)
  reverseMap = {}
  for resonance in nmrProject.sortedResonances():
    assignment = assignmentMap.get(resonance)
    resonanceGroup = resonance.resonanceGroup
    groupAssignment = resonanceGroupMap.get(resonanceGroup)

    if assignment:
      # resonance is assigned - at this point it must be to a molecule atom

      # Use the name of the assignment
      name = assignment[3]
      resonance.name = name

      oldResonance = reverseMap.get(assignment)
      if oldResonance is None:
        # No resonance assignment clashes - just put in reverse map
        reverseMap[assignment] = resonance

        if groupAssignment != assignment[:3]:
          # Residue assignment mismatch. This should not happen
          # Use assignmentMap assignment and remove link to ResonanceGroup

          print ('WARNING, %s: %s does not match %s: %s' %
                 (resonance, assignment, resonanceGroup, groupAssignment))

          newResonanceGroup = reverseGroupMap.get(assignment[:3])
          if newResonanceGroup is None:
            # Assigned resonance with no matching ResonanceGroup. Make a new group
            rg = nmrProject.newResonanceGroup(sequenceCode=assignment[1], residuetype=assignment[2],
                                              resonances=(resonance,))
            # NBNB TBD residueType/ccpCode still to be sorted out
            rg.nmrChain = (nmrProject.findFirstNmrChain(code=groupAssignment[0]) or
                           nmrProject.newNmrChain(code=groupAssignment[0]))

          else:
            # resonance belongs in a different group. Move it there
            # NB. Name clashes (if any) wil be resolved when second clashing resonance comes up
            resonance.resonanceGroup = newResonanceGroup

      else:
        # Assignment clash - merge into old resonance that at this point must be
        # assigned and have a lower serial
        oldResonance.absorbResonance(resonance)

    else:
      # resonance was not assigned from a resonanceSet (in mapAssignedResonances)
      name = V2Upgrade.regularisedResonanceName(resonance)
      assignment = groupAssignment + {name,}

      oldResonance = reverseMap.get(assignment)
      if oldResonance is None:
        # no clashes
        resonance.name = name
        if resonanceGroup is None:
          resonance.resonanceGroup = defaultResonanceGroup
        reverseMap[assignment] = resonance

      else:
        # Assignment clash

        # Check if assignment is to molecule
        atom =None
        chain = mainMolSystem.findFirstChain(code=assignment[0])
        if chain is not None:
          seqCode, seqInsertCode, offset = commonUtil.parseSequenceCode(assignment[1])
          seqInsertCode = seqInsertCode or ' '
          residue = chain.findFirstResidue(seqCode=seqCode, seqInsertCode=seqInsertCode)
          if residue is not None:
            atom = residue.findFirstAtom(name=assignment[3])

        if atom is None:
          # Assignment not to molecule. Add resonance serial to atom name
          # To preserve difference between
          serial = resonance.serial
          ss = '@%s' % serial
          if ss not in name:
            name = '%s@%s' % (name, serial)
          resonance.name = name
          assignment = groupAssignment + {name,}
          reverseMap[assignment] = resonance

        else:
          # Assignment ot molecule. Absorb  in previous resonance
          oldResonance.absorbResonance(resonance)



def copyMolSystemContents(molSystem, toMolSystem, chainMap):
  """Copy MolSystem contents into a pre-existing MolSystem
   NB chainMap is an in/out parameter DESIGNED to be modified."""

  molSystemCode = molSystem.code

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

def expandMolSystemAtoms(molSystem):
  """Add extra atoms corresponding to AtomSets"""

  # Set elementSymbol and add missing atoms (lest something breaks lower down)
  for chain in molSystem.sortedChains():
    for residue in chain.soredResidues():
      chemCompVar = residue.chemCompVar
      for chemAtom in chemCompVar.findAllChemAtoms(className='ChemAtom'):
        atom = residue.findFirstAtom(name=chemAtom.name)
        if atom is None:
          residue.newAtom(name=chemAtom.name, atomType='single',
                          elementSymbol=chemAtom.elementSymbol)
        else:
          atom.elementSymbol = chemAtom.elementSymbol


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
      # AQUA is good on pseudoatom names
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
            # NB the fact that chemAtoms and chemAtomSets are sorted (by name) is used lower down
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
        for eqvAtom2 in eqvTypeAtoms[ii+1:]:
          components2 = eqvAtom2.sortedComponents()
          if len(components) == len(components2):
            if all((x in components2[jj].boundAtoms) for jj,x in enumerate(components)):
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
                # NB We rely on names being sorted (X then Y in both cases)
                for kk,name in enumerate(nsNames1):
                  atom2 = residue.findFirstAtom(name=nsNames2[kk])
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
