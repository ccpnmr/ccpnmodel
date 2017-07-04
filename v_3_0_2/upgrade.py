"""Upgrade code for upgrades to version 3.0.2 (intermeciate 2/3 conversion version

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
__dateModified__ = "$dateModified: 2017-04-07 11:41:49 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import time
import math
import operator
import collections

from ccpnmodel.ccpncore.lib import CopyData
from ccpnmodel.ccpncore.lib import V2Upgrade
from ccpnmodel.ccpncore.lib import Constants
from ccpnmodel.ccpncore.memops.ApiError import ApiError
from ccpn.util import Common as commonUtil
from ccpn.util import Sorting

versionSequence = ['2.0.a0', '2.0.a1', '2.0.a2', '2.0.a3', '2.0.b1', '2.0.b2', '2.0.b3',
                   '2.0.4',  '2.0.5',  '2.1.0',  '2.1.1', '2.1.2', '3.0.a1', '3.0.2']
# NBNB version 2.0.6 is a side branch, not on the main version sequence

emptyDict = {}
emptyList = []

# guids of elements that should be treated as old
# Must be kept out of map fixing till the last, as they break it.
#
# These are atributes with new IeeeFloat type from FloatMatrix,
# which being inherited down from an abstract class
# do not fit in the normal treatment.
elemsTreatedAsOld = {'www.ccpn.ac.uk_Fogh_2011-03-30-18:03:29_00002',
                     'www.ccpn.ac.uk_Fogh_2011-03-30-18:03:29_00001',}

# pairs of element guids that should be treated as matching, e.g. when
# a single element must match with several elements in subclasses
elementPairings = []


def extraMapChanges(globalMapping):
  """ Extra map changes specific for a given step
  """
  pass

  # set proc to skip for unsettable now-derived ExpDim.refExpDim
  # skip seems not to work properly for exolinks. Try delay
  # dd = {'proc':'delay'}
  # globalMapping['loadMaps']['NMR.ExpDim']['content']['refExpDim'] = dd
  # globalMapping['loadMaps']['NMR.ExpDim.refExpDim'] = dd
  # globalMapping['mapsByGuid']['www.ccpn.ac.uk_Fogh_2006-08-16-18:23:00_00002'] = dd

  # Suspend processing of SampleComponent.refComponent, now derived with changed key
  # and requires special handling
  globalMapping['mapsByGuid']['www.ccpn.ac.uk_Fogh_2006-08-16-18:22:42_00002']['proc'] = 'delay'

  # Set exolinks to Sample to 'delay' to handle key change
  globalMapping['mapsByGuid']['www.ccpn.ac.uk_Fogh_2006-08-16-18:22:35_00001']['proc'] = 'delay'


def correctData(topObj, delayDataDict, toNewObjDict, mapping=None):
  """ update topObj object tree using information in delayDataDict
  May be used either to postprocess a file load (minor upgrade)
  or as part of an in-memory data transfer (major upgrade)

  topObj is the package TopObject in the new tree
  toNewObjDict is _ID:newObj for minor
    and oldObj/oldObjId:newObj for major upgrades
  """

  doGet = delayDataDict.get
  pName = topObj.packageName

  if pName == 'ccp.lims.Sample':
    nextSerial = 1
    for sample in sorted(doGet(topObj, emptyDict).get('samples', emptyList),
                         key=operator.attrgetter('name')):

      # Add serial where missing (because of model change)
      if sample.serial is None:
        sample.__dict__['serial'] = nextSerial
        nextSerial += 1

      # Correct SampleComponent key, based on the old refComponent link (previous key)
      for sampleComponent in doGet(sample, emptyDict).get('sampleComponents', emptyList):
        dd = doGet(sampleComponent, emptyDict)
        inDataList = dd.get('refComponent')
        if inDataList:
          keyList = inDataList[0]
          name = keyList[1]
          sampleComponent.__dict__['name'] = name


  elif pName == 'ccp.nmr.Nmr':
    nextSerial = 1
    for spectrumGroup in sorted(doGet(topObj, emptyDict).get('spectrumGroups', emptyList),
                                key=operator.attrgetter('name')):
      # Add serial where missing (because of model change)
      if spectrumGroup.serial is None:
        spectrumGroup.__dict__['serial'] = nextSerial
        nextSerial += 1

    # Correct link to Sample (key has changed)
    # This really is tricky, but byu th3 time this code is reached, the relevant SAmples
    # should be loaded and ready
    for experiment in doGet(topObj, emptyDict).get('experiments', emptyList):
      dd = doGet(experiment, emptyDict)
      inDataList = dd.get('sample')
      if __name__ == '__main__':
        if inDataList:
          # set link to Sample - whose key has changed
          keyList = inDataList[0]
          sampleStore = experiment.root.findFirstSampleStore(guid=keyList[0])
          sample = sampleStore.findFirstSample(name=keyList[-2])
          experiment.sample = sample

    # NBNB TODO ?? SampledDataDim.samples is NOT dealt with
    # In theory it should, but there are no V2 data that require it.

  elif pName == 'ccp.molecule.MolSystem':
    nextSerial = 1
    for chainGroup in sorted(doGet(topObj, emptyDict).get('chainGroups', emptyList),
                             key=operator.attrgetter('name')):
      # Add serial where missing (because of model change)
      if chainGroup.serial is None:
        chainGroup.__dict__['serial'] = nextSerial
        nextSerial += 1


def correctFinalResult(memopsRoot):
  """Correct final result in situ, after loading has finished
  NOT part of standard compatibility process, but a special case for upgrade from v2 to v3 """


  print ("Correcting Final Result for V2-V3 transition")

  # Copy across molSystem chains so all NmrProjects have only one MolSystem
  molSystemMap = {}
  chainMap = {}
  for nmrProject in memopsRoot.sortedNmrProjects():

    # time0 = time.time()
    # print ('@~@~ top time0', time0)

    nmrProject.isModifiable = True

    # Link to SampleStore - if unique
    sampleStores = memopsRoot.sortedSampleStores()
    if len(sampleStores) == 1:
      nmrProject.sampleStore = sampleStores[0]

    molSystemCounts =  getNmrMolSystems(nmrProject)
    if molSystemCounts:
      # select main system as the most common
      sentinel = -1
      for molSystem, count in sorted(molSystemCounts.items()):
        if count > sentinel:
          mainMolSystem = molSystem
          sentinel = count
    else:
      mainMolSystem = memopsRoot.newMolSystem(name='MolSystem0', code='MS0')
      molSystemCounts[mainMolSystem] = 1
    molSystemMap[mainMolSystem] = mainMolSystem

    # print ('@~@~ in molSystems 1', time.time() - time0)

    # Set link to NmrProject
    mainMolSystem.isModifiable = True
    nmrProject.molSystem = mainMolSystem

    # Replace chainCode ' ' with something else
    for replaceSpaceCode in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopgrstuvwxyz':
      if mainMolSystem.findFirstChain(code=replaceSpaceCode) is None:
        break
    else:
      replaceSpaceCode = '_'
    spaceChain = mainMolSystem.findFirstChain(code=' ')
    if spaceChain is not None:
      spaceChain.renameChain(replaceSpaceCode)

    # print ('@~@~ in molSystems 2', time.time() - time0)

    # Keep a list for use in chainMap
    mainMolSystemChains = mainMolSystem.sortedChains()

    # Overlap with previous molSystem set - merge into previous system.
    # resetting chainCode ' ' as you go
    for molSystem in molSystemCounts:
      if molSystem not in molSystemMap:
        molSystemMap[molSystem] = mainMolSystem
        spaceChain = molSystem.findFirstChain(code=' ')
        if spaceChain is not None:
          ss = replaceSpaceCode
          for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopgrstuvwxyz':
            if molSystem.findFirstChain(code=ss) is None:
              break
            else:
              ss = char
          spaceChain._renameChain(ss)
        copyMolSystemContents(molSystem, mainMolSystem, chainMap=chainMap)

    # print ('@~@~ in molSystems 3', time.time() - time0)

    if chainMap:
      # Add mainMolSystem chains to chainMap if it is not empty
      for ch in mainMolSystemChains:
        chainMap[ch] = ch


    # Add new atoms to MolSystem
    for chain in mainMolSystem.sortedChains():
      chain.expandMolSystemAtoms()

    # print ('@~@~ done molSystems', time.time() - time0)

    # Transfer residue Types to structure residues

    # relink StructureEnsembles
    for structureEnsemble in mainMolSystem.structureEnsembles:
      for coordChain in structureEnsemble.coordChains:
        # Make sure code3Letter is set
        for coordResidue in coordChain.sortedResidues():
          code3Letter = coordResidue.code3Letter
          if not code3Letter:
            chain = coordResidue.chain.chain
            if chain is not None:
              residue = (chain.findFirstResidue(seqId=coordResidue.seqId) or
                        chain.findFirstResidue(seqCode=coordResidue.seqCode,
                                               seqInsertCode=coordResidue.seqInsertCode))
              if residue:
                coordResidue.code3Letter = residue.code3Letter or residue.ccpCode

      # Move structure data into new Pandas structure
      upgradeToPandasData(structureEnsemble)


    # print ('@~@~ done structures', time.time() - time0)

    for nmrConstraintStore in nmrProject.sortedNmrConstraintStores():
      nmrConstraintStore.isModifiable = True
      fixNmrConstraintStore(nmrConstraintStore ,mainMolSystem, chainMap)

    # print ('@~@~ done constraints', time.time() - time0)

    # Fix measurementList names
    for obj in nmrProject.measurementLists:
      name = obj.name
      if name:
        name = '_'.join(name.split()).replace('.','_')
      else:
        name = '%ss%s' % (obj.className[:-4], obj.serial)

      while nmrProject.findAllMeasurementLists(name=name) not in (set(), {obj}):
        name = commonUtil.incrementName(name)

      obj.name = name

    # print ('@~@~ done measurements', time.time() - time0)

    # Fix experiments
    fixExperiments(nmrProject)

    # Make default NmrChain
    nmrChain = (nmrProject.findFirstNmrChain(code=Constants.defaultNmrChainCode) or
                nmrProject.newNmrChain(code=Constants.defaultNmrChainCode))


    # Transfer assignments in NmrProject
    transferAssignments(nmrProject, mainMolSystem, chainMap)

    # Fix peak intensities and assignments storage
    fixPeaks(nmrProject)

    # Remove ResonanceGroup.residue - no longer needed, and superseded in new model
    for resonanceGroup in nmrProject.resonanceGroups:
      resonanceGroup.residue = None

    # print ('@~@~ done experiments and assignments', time.time() - time0)

def upgradeToPandasData(structureEnsemble):
  """Move all data to new pandas data structures and delete old objects"""

  from ccpn.util.StructureData import EnsembleData

  memopsRoot = structureEnsemble.root

  # Get data for atoms
  atomData = []
  sequenceCodes = []
  for atom in structureEnsemble.orderedAtoms:
    coordResidue = atom.residue
    # NB, this gives teh 'official' sequence codes as consecutive integers
    # and uses the user-set values only for the nmrSequenceCode
    atomData.append([
      coordResidue.chain.code, coordResidue.seqId, coordResidue.code3Letter, atom.name,
      atom.altLocationCode.strip() or None, atom.elementSymbol
    ])
    sequenceCodes.append(str(coordResidue.seqCode) + coordResidue.seqInsertCode.strip())
  atomCount = len(atomData)
  atomData = list(zip(*atomData))
  modelCount = len(structureEnsemble.models)

  #Pack atom data into ordered dictionary
  allData = collections.OrderedDict()
  allData['modelNumber'] = []
  allData['chainCode'] = atomData[0] * modelCount
  allData['sequenceId'] = atomData[1] * modelCount
  allData['insertionCode'] = [None] * (modelCount * atomCount)
  allData['residueName'] = atomData[2] * modelCount
  allData['atomName'] = atomData[3] * modelCount
  allData['altLocationCode'] = atomData[4] * modelCount
  allData['element'] = atomData[5] * modelCount
  allData['x'] = []
  allData['y'] = []
  allData['z'] = []
  allData['occupancy'] = []
  allData['bFactor'] = []
  allData['nmrChainCode'] = list(allData['chainCode'])
  allData['nmrSequenceCode'] = sequenceCodes * modelCount
  allData['nmrResidueName'] = list(allData['residueName'])
  allData['nmrAtomName'] = list(allData['atomName'])

  isnan = math.isnan

  for model in structureEnsemble.sortedModels():
    # Add model-dependent data

    allData['modelNumber'].extend([model.serial] * atomCount)

    try:
      occupancies = model.occupancies
      occupancies = [None if isnan(x) else x for x in occupancies]
    except:
      occupancies = [None] * atomCount
    allData['occupancy'].extend(occupancies)

    try:
      bFactors = model.bFactors
      bFactors = [None if isnan(x) else x for x in bFactors]
    except:
      bFactors = [None] * atomCount
    allData['bFactor'].extend(bFactors)

    try:
      coordinates = model.coordinates
      coordinates = [None if isnan(x) else x for x in coordinates]
    except:
      coordinates = [None] * (atomCount * 3)
    # The inner zip divides the packed coordinates into triples,
    # and the outer zip gives separate x, y, z lists
    x,y,z = zip(*zip(*[iter(coordinates)] * 3))
    allData['x'].extend(x)
    allData['y'].extend(y)
    allData['z'].extend(z)

  # Delete unneeded old data:
  for obj in structureEnsemble.dataMatrices:
    obj.resetData()
  memopsRoot.override = True
  try:
    for obj in structureEnsemble.coordChains:
      obj.delete()
  finally:
    memopsRoot.override = False

  ensembleData = EnsembleData()
  structureEnsemble.newParameter(name='data', value=ensembleData)
  for key, val in allData.items():
    # print('@~@~', key, len(val), val[0], '..', val[-1])
    ensembleData[key] = val
  # NBNB this still is missing setting ensembleData._structureEnsemble


def fixExperiments(nmrProject):
  """ensure DataSource.name is unique"""
  usedNames = set()
  for experiment in nmrProject.sortedExperiments():
    refExperiment = experiment.refExperiment
    nameExp = experiment.name
    for dataSource in experiment.sortedDataSources():
      # nameDat = dataSource.name
      #
      # SUPERSEDED - we want the dataSource name to travel unchanged, where possible
      # to allow NEF roundtripping
      # if nameExp and nameDat and nameExp != nameDat:
      #   # We had both experiment and dataSource name. Combine them
      #   # Use name from serials
      #   name = '%s-%s' % (nameExp, nameDat)
      #
      # else:
      #   # Use experiment or dataSource name as default
      #   name = nameExp or nameDat

      # Give preference to datasource name
      name = dataSource.name or experiment.name

      # Try peakList name as an alternative
      peakLists = dataSource.sortedPeakLists()
      if len(peakLists) == 1:
        name = name or peakLists[0].name

      if refExperiment:
        refName = refExperiment.synonym or refExperiment.name
        if name:
          if dataSource.name and experiment.name and experiment.name != refName:
            # Special case. For native (i.e. not beackread from V3) V2 data
            # we want this behaviour
            name = '%s-%s' % (experiment.name, dataSource.name)
        else:
          # Use name from experiment type
          name = refName

      if not name:
        # no name set anywhere, use serials
        name = '%s-%s' % (experiment.serial, dataSource.serial)

      #regularise name
      name = '_'.join(name.split()).replace('.','_')
      while name in usedNames:
        name = commonUtil.incrementName(name)
      usedNames.add(name)
      dataSource.name = name

    # set experiment.name - now used for refExperiment common name
    if refExperiment:
      experiment.name = refExperiment.synonym or refExperiment.name
    else:
      experiment.name = '?'

    # set expDimRef.axisCodes if not set already
    for expDim in experiment.expDims:
      if expDim.findFirstExpDimRef(axisCode=None) is not None:
        experiment.resetAxisCodes()
        # in future can do:
        # experiment.resetAxisCodes()
        break


def fixPeaks(nmrProject):
  """Copy Peak intensity records to peak attributes,
   and assignment related attributes to new locations """

  for experiment in nmrProject.sortedExperiments():
    for dataSource in experiment.sortedDataSources():
      for peakList in dataSource.sortedPeakLists():
        for peak in peakList.sortedPeaks():

          # Copy intensity values across
          if not peak.height:
            # No good way of determining which object to take if there are multiple height objects
            # Fortunately there rarely is (Analysis used findFirst too)
            intensityObject = peak.findFirstPeakIntensity(intensityType='height')
            if intensityObject is not None:
              peak.height = intensityObject.value
              peak.heightError = intensityObject.error
          if not peak.volume:
            # No good way of determining which object to take if there are multiple height objects
            # Fortunately there rarely is (Analysis used findFirst too)
            intensityObject = peak.findFirstPeakIntensity(intensityType='volume')
            if intensityObject is not None:
              peak.volume = intensityObject.value
              peak.volumeError = intensityObject.error

          for obj in peak.peakIntensities:
            # clean up
            obj.delete()

          # Copy across PeakDimComponent data
          for peakDim in peak.sortedPeakDims():
            for peakDimComponent in peakDim.sortedPeakDimComponents():
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


def fixNmrConstraintStore(nmrConstraintStore, molSystem, chainMap):
    """Fix NmrConstraintStore"""

    # First fix FixedResonances (so we can remap them below)
    # Map unassigned, then assigned resonances


    sortKey = Sorting.universalNaturalSortKey

    assignmentMap = V2Upgrade.mapUnAssignedFixedResonances(nmrConstraintStore)
    for resonance, tt in V2Upgrade.mapAssignedResonances(nmrConstraintStore, chainMap=chainMap,
                                                         molSystem=molSystem).items():
      residue, name = tt
      if residue is None:
        assignmentMap[resonance] = (None, None, None, name)
      else:
        chainCode = residue.chain.code
        sequenceCode = str(residue.seqCode) + (residue.seqInsertCode or '').strip()
        residueType = residue.molResidue.chemComp.code3Letter
        assignmentMap[resonance] = (chainCode, sequenceCode, residueType, name)

    assignment2Resonance = {}
    resonanceMap = {}
    for resonance, assignment in assignmentMap.items():
      resonance.chainCode = assignment[0]
      resonance.sequenceCode = assignment[1]
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

      name = constraintList.name
      if name:
        name = '_'.join(name.split()).replace('.','_')
      else:
        name = '%ss%s' % (restraintType, constraintList.serial)

      while (nmrConstraintStore.findAllConstraintLists(name=name) not in (set(),
             {constraintList})):
        name = commonUtil.incrementName(name)

      constraintList.name = name

      newContribution = 'new%sContribution' % restraintType
      newItem = 'new%sItem' % restraintType

      if restraintType in ('Distance', 'HBond', 'JCoupling', 'Rdc',):
        #ix pairwise restraints
        for constraint in constraintList.sortedConstraints():

          # Make new Contribution
          dd = dict((x,getattr(constraint,x))
                    for x in ('targetValue', 'error', 'upperLimit', 'lowerLimit', 'weight'))
          contribution = getattr(constraint, newContribution)(**dd )

          # Transfer resonances to new Items objects and delete old ones.
          for constraintItem in constraint.sortedItems():
            assignments = (assignmentMap[resonanceMap.get(x,x)] for x in constraintItem.resonances)
            resonances = tuple(assignment2Resonance[x] for x in sorted(assignments, key=sortKey))
            if not contribution.findFirstItem(resonances=resonances):
              # The 'if' statements protects against the case where a contribution has two items
              # from different FixedResonances that map out to the same pair of assignments
              # Rare and messy, but better skip one than crash
              getattr(contribution, newItem)(resonances=resonances)

            constraintItem.delete()

      elif restraintType in ('Csa', 'ChemicalShift'):
        #ix one-resonance restraints
        for constraint in constraintList.sortedConstraints():

          # Make new Contribution
          dd = dict((x,getattr(constraint,x))
                    for x in ('targetValue', 'error', 'upperLimit', 'lowerLimit', 'weight'))
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
            contribution.weight = constraint.weight
            getattr(contribution, newItem)(resonances=resonances)
            constraintItem.delete()

      else:
        raise ValueError("Restraint list named %s not recognized by code (BUG?)" % className)

      # Upgrade from earlyV3 to finalV3
      V2Upgrade.upgradeConstraintList(constraintList)

    # Remove obsolete FixedResonances, ResonanceSets and AtomSets
    for oldResonance in resonanceMap:
      oldResonance.delete()
    for fixedAtomSet in nmrConstraintStore.sortedFixedAtomSets():
      # NB this deletes FixedResonanceSets too by cascading delete.
      fixedAtomSet.delete()


def transferAssignments(nmrProject, mainMolSystem, chainMap):
  """Transfer NmrProject assignments"""

  # @~@~ debug:
  # import time
  # time0 = time.time()
  # print ('@~@~ time0', time0)


  # Map Resonances that are fully assigned
  resonance2Assignment = V2Upgrade.mapAssignedResonances(nmrProject, molSystem=mainMolSystem,
                                                         chainMap=chainMap)
  # Map ResonanceGroups that are fully assigned
  resonanceGroup2Residue = V2Upgrade.mapResonanceGroupResidues(nmrProject,
                                                               molSystem=mainMolSystem,
                                                               chainMap=chainMap)

  # print ('@~@~ time1', time.time() - time0)

  # Map unmapped ResonanceGroups that follow from assigned resonances.
  # If resonance assignment conflicts with resonanceGroup assignment tha latter takes precedence.
  # But in that case data are inconsistent  and any solution is arbitrary.
  # Note that resonances will always keep their assignment
  for resonance, tt in sorted(resonance2Assignment.items()):
    resonanceGroup = resonance.resonanceGroup
    if resonanceGroup is not None:
      previousResidue = resonanceGroup2Residue.get(resonanceGroup)
      residue, resonanceName = tt
      if previousResidue is None:
        if residue is not None:
          resonanceGroup2Residue[resonanceGroup] = residue
      elif residue is not previousResidue:
        print ('WARNING, ResonanceGroup %s, %s, does not match resonance %s, %s'
               % (resonanceGroup.serial, previousResidue, resonance.serial, residue)
               )

  handledResonanceGroups = set(resonanceGroup2Residue.keys())

  # print ('@~@~ time2', time.time() - time0)

  # Set mandatory default NmrChain - must have serial == 1.
  # NB Looks like this is (sometimes?) set in wrapper init, hence the if statement
  defaultNmrChain = nmrProject.findFirstNmrChain(code=Constants.defaultNmrChainCode)
  if defaultNmrChain is None:
    defaultNmrChain = nmrProject.newNmrChain(code=Constants.defaultNmrChainCode)
  # Also set defaultResonanceGroup
  defaultResonanceGroup = (defaultNmrChain.findFirstResonanceGroup(seqCode=None,
                                                                   seqInsertCode='@') or
                           nmrProject.newResonanceGroup(directNmrChain=defaultNmrChain,
                                                       seqInsertCode = '@',
                                                       details="Default ResonanceGroup"))

  # print ('@~@~ time3', time.time() - time0)

  # Now set up assigned ResonanceGroups and add their offset groups
  reverseGroupMap = {}
  groupsToMerge = {}
  for resonanceGroup, residue in sorted(resonanceGroup2Residue.items()):
    useResonanceGroup = reverseGroupMap.get(residue)
    if useResonanceGroup is None:
      useResonanceGroup = resonanceGroup
      # new group - handle it
      reverseGroupMap[residue] = resonanceGroup
      resonanceGroup.assignedResidue = residue

    # Add offset ResonanceGroups
    for direction in (+1,-1):
      stretch = V2Upgrade.findSpinSystemStretch(resonanceGroup, direction=direction)
      offset = 0
      for rg in stretch:
        offset += direction

        if rg in handledResonanceGroups:
          # We have reached a residue already handled. Stop here.
          break

        else:
          hasAddedGroup = V2Upgrade.addOffsetResonanceGroup(useResonanceGroup, rg, offset)
          if hasAddedGroup:
            handledResonanceGroups.add(rg)

    # Add unique, identity-linked ResonanceGroup, if any
    rg0 = V2Upgrade.findIdentityResonanceGroup(resonanceGroup)
    if rg0 is not None and rg0 not in handledResonanceGroups:
      hasAddedGroup = V2Upgrade.addOffsetResonanceGroup(useResonanceGroup, rg0, 0)
      if hasAddedGroup:
        handledResonanceGroups.add(rg0)

    if useResonanceGroup is not resonanceGroup:
      # Set up to merge duplicates
      groupsToMerge[resonanceGroup] = useResonanceGroup
      handledResonanceGroups.add(resonanceGroup)
      # print ('@~@~ +++ WARNING clashing assigned ResonanceGroups %s %s %s'
      #        % (useResonanceGroup.sequenceCode, useResonanceGroup.serial, resonanceGroup.serial))
      # Set to default naming to avoid potential clashes
      resonanceGroup.sequenceCode = None
      resonanceGroup.directNmrChain = defaultNmrChain
      # NBNB check that resonance names are dealt with properly later
      # print ('@~@~ from', resonanceGroup, resonanceGroup.sequenceCode, resonanceGroup.nmrChain)
      # print ('@~@~', [(x.serial, x.name) for x in resonanceGroup.sortedResonances()])
      # print ('@~@~ to', useResonanceGroup, useResonanceGroup.sequenceCode, useResonanceGroup.nmrChain)
      # print ('@~@~', [(x.serial, x.name) for x in useResonanceGroup.sortedResonances()])
      # for resonance in resonanceGroup.resonances:
      #   resonance.resonanceGroup = useResonanceGroup
      # resonanceGroup.delete()

  # print ('@~@~ time4', time.time() - time0)

  # Now deal with stretches of connected resonanceGroups
  for resonanceGroup in nmrProject.sortedResonanceGroups():
    if (resonanceGroup not in handledResonanceGroups
        and not V2Upgrade.findSpinSystemStretch(resonanceGroup, direction=-1)):
      # start at first resonanceGroup in stretch
      stretch = V2Upgrade.findSpinSystemStretch(resonanceGroup, direction=1)
      if len(stretch) > 1:
        # Multi-residue stretch. Make connected stretch
        newNmrChain = nmrProject.newNmrChain(isConnected=True)
        for rg in stretch:
          if rg in handledResonanceGroups:
            break
          else:
            newNmrChain.addMainResonanceGroup(rg)
            handledResonanceGroups.add(rg)

  # print ('@~@~ time5', time.time() - time0)

  # Deal with isolated resonanceGroups

  for resonanceGroup in nmrProject.sortedResonanceGroups():
    if resonanceGroup not in handledResonanceGroups:

      plusStretch = V2Upgrade.findSpinSystemStretch(resonanceGroup, direction=1)
      minusStretch = V2Upgrade.findSpinSystemStretch(resonanceGroup, direction=-1)
      if plusStretch and plusStretch[0] in handledResonanceGroups:
        rgmain = plusStretch[0]
        rgminus = resonanceGroup
      elif minusStretch and minusStretch[0] in handledResonanceGroups:
        rgmain = resonanceGroup
        rgminus = minusStretch[0]
      else:
        rgmain = resonanceGroup
        rgminus = None

      if rgminus is None:
        # No two-group stretch found. Try assigning as zero-offset to already assigned resonanceGroup
        rg0 = V2Upgrade.findIdentityResonanceGroup(resonanceGroup)
        addedGroup = False
        if rg0 is not None and rg0.relativeOffset is None:
          addedGroup = V2Upgrade.addOffsetResonanceGroup(rg0, resonanceGroup, 0)

        if not addedGroup:
        # Not a zero-offset residue3. Set it is its own right.
          try:
            resonanceGroup.directNmrChain = defaultNmrChain
          except ApiError:
            resonanceGroup.sequenceCode = None
            resonanceGroup.directNmrChain = defaultNmrChain
        handledResonanceGroups.add(resonanceGroup)

      else:
        # Set i group.
        try:
          rgmain.directNmrChain = defaultNmrChain
        except ApiError:
          rgmain.sequenceCode = None
          rgmain.directNmrChain = defaultNmrChain
        handledResonanceGroups.add(rgmain)

        # Try setting i-1 group as offset
        addedGroup = V2Upgrade.addOffsetResonanceGroup(rgmain, rgminus, -1)
        if not addedGroup:
          try:
            resonanceGroup.directNmrChain = defaultNmrChain
          except ApiError:
            resonanceGroup.sequenceCode = None
            resonanceGroup.directNmrChain = defaultNmrChain
        handledResonanceGroups.add(resonanceGroup)

  # print ('@~@~ time6', time.time() - time0)

  # Almost done with resonanceGroups. Now for resonances.

  # First assigned resonances
  handledResonances = set()
  for resonance in nmrProject.sortedResonances():
    tt = resonance2Assignment.get(resonance)
    if tt is not None:

      residue, name = tt
      if residue is not None and not resonance.isDeleted:

        # Get target ResonanceGroup
        chainCode = residue.chain.code
        nmrChain = (nmrProject.findFirstNmrChain(code=chainCode) or
                    nmrProject.newNmrChain(code=chainCode))
        seqCode = residue.seqCode
        insertCode = residue.seqInsertCode.strip()
        sequenceCode = '%s%s' % (seqCode, insertCode)
        resonanceGroup = (nmrChain.findFirstResonanceGroup(seqCode=seqCode,
                                                           seqInsertCode=insertCode or None)
                          or nmrProject.newResonanceGroup(sequenceCode=sequenceCode,
                                                          directNmrChain=nmrChain))
        if resonance.resonanceGroup not in (None, resonanceGroup):
          print (
            'WARNING, %s ResonanceGroup %s does not match assignment to %s.%s (resonanceGroup %s' %
            (resonance, resonance.resonanceGroup, chainCode, sequenceCode, resonanceGroup)
          )

        # Move or merge resonance in position
        convertResonance = None
        ll = sorted(x for x in resonanceGroup.findAllResonances(name=name) if x is not resonance)
        if ll:
          # Clashing resonances. In theory should be merged, but better keep them separate
          # as they are likely caused by error and might be at different freqs
          if ll[0].serial < resonance.serial:
            # Keep the resonance with the lowest serial and rename this one.
            # It is always handled already
            ll[0] = resonance
          else:
            # Keep this one, but wait till we have renamed the others
            convertResonance = resonance

          for rs in ll:
            # Rename to avoid clashes,
            ss = '%s@%s' % (name, rs.serial)
            if any(x for x in resonanceGroup.findAllResonances(name=ss) if x is not rs):
              # Name clash. Should never happen here, but to avoid trouble, ...
                ss = None
            rs.name = ss
            rs.resonanceGroup = resonanceGroup
            handledResonances.add(rs)

        else:
          # No clashes, just assign resonance
          convertResonance = resonance

        if convertResonance is not None:
          convertResonance.name = None  # TO avoid clashes
          convertResonance.resonanceGroup = resonanceGroup
          convertResonance.name = name
          if convertResonance.isotopeCode in ('?', 'unknown', None):
            convertResonance.isotopeCode = commonUtil.name2IsotopeCode(name) or '?'
          handledResonances.add(resonance)

  # print ('@~@~ time7', time.time() - time0)

  # Now do unassigned resonances:
  for resonance in nmrProject.sortedResonances():
    if resonance not in handledResonances:

      # get target resonanceGroup
      resonanceGroup = resonance.resonanceGroup
      if resonanceGroup is None:
        resonanceGroup = defaultResonanceGroup
      else:
        resonanceGroup = groupsToMerge.get(resonanceGroup, resonanceGroup)

      name = V2Upgrade.regularisedResonanceName(resonance)
      oldResonance = resonanceGroup.findFirstResonance(name=name)
      if oldResonance is not None:
        if oldResonance is not resonance or len(resonanceGroup.findAllResonances(name=name)) > 1:
          # Name clash. Should never happen here, but to avoid trouble, ...
          name = None

      resonance.name = None
      resonance.resonanceGroup = resonanceGroup
      resonance.name = name
      handledResonances.add(resonance)
      if name and resonance.isotopeCode in ('?', 'unknown', None):
        resonance.isotopeCode = commonUtil.name2IsotopeCode(name) or '?'

  # print ('@~@~ time8', time.time() - time0)

  # Clean up merged ResonanceGroups
  for resonanceGroup in groupsToMerge:
    if resonanceGroup.resonances:
      raise ApiError("Resonances left in what should be empty ResonanceGroup before deletion: %s: %s"
      % (resonanceGroup, resonanceGroup.sortedResonances()))
    resonanceGroup.delete()

  # print ('@~@~ time9', time.time() - time0)


def copyMolSystemContents(molSystem, toMolSystem, chainMap):
  """Copy MolSystem contents into a pre-existing MolSystem
   NB chainMap is an in/out parameter DESIGNED to be modified."""

  molSystemCode = molSystem.code

  # copy chains across
  newChains = []
  for chain in molSystem.sortedChains():
    newCode = '-'.join((molSystemCode, chain.code))
    newChain = CopyData.copySubTree(chain, toMolSystem, topObjectParameters={'code':newCode,},
                                    maySkipCrosslinks=True)
    chainMap[chain] = newChain
    newChains.append(newChain)

  # chainCodeMap = dict(((key.code, val.code) for key,val in chainMap.items()))

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
      parentDict = molSystem.root.__dict__['structureEnsembles']
      del parentDict[(molSystem, structureEnsemble.ensembleId)]
      newCode = (toMolSystem, structureEnsemble.ensembleId)
      structureEnsemble.molSystem = toMolSystem
      parentDict[newCode] = structureEnsemble
    finally:
      molSystem.root.override = False

  # Fix Haddock Partners
  for haddock in molSystem.root.sortedHaddockProjects():
    for partner in haddock.sortedHaddockPartners():
      if partner.molSystem is molSystem:
        for hchain in partner.sortedChains():
          oldChain = hchain.chain
          newChain = chainMap.get(oldChain, oldChain)
          if newChain is not oldChain:
            newChainCode = newChain.code
            if newChainCode != oldChain.code:
              if newChainCode:
                # Should always be true, but it should fail more gracefully this way
                parentDict = partner.__dict__['chains']
                del parentDict[oldChain.code]
                hchain.__dict__['chainCode'] = newChainCode
                parentDict[newChainCode] = hchain
        #
        partner.molSystem = toMolSystem

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
      molSystem = residueProb.possibility.topObject
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

      # Reset unknown code to '?'
      if resonance.isotopeCode in (None,'unknown'):
        resonance.isotopeCode = '?'

      # Continue with the rest
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

  if not molSystemCounts:
    molSystems = nmrProject.root.sortedMolSystems()
    if molSystems:
      molSystemCounts[molSystems[0]] = 200
      for molSystem in molSystems[1:]:
        molSystemCounts[molSystem] = 50

  return molSystemCounts
