
"""Functions for calculating axisCodes for NmrExpPrototypes, adn necessary utilities.
For normal cases, use only refExpFimRefCodeMap function, and get axisCodes from
refExpDimRefs and the map.

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
import ccpn.util.Constants

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:14 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import operator
import collections
from typing import Dict
from ccpn.util import Constants

# Dictionary of experiment names that should come first in the list
#  - with optional remapping of names
priorityNameRemapping = {
# C,H experiments
'13C HSQC/HMQC':'13C HSQC/HMQC',

# C,H,H experiments
'13C NOESY-HSQC':'13C NOESY-HSQC',
'13C HSQC-NOESY':'13C HSQC-NOESY',
'HcCH-TOCSY':'HcCH-TOCSY',
'HCcH-TOCSY':'HCcH-TOCSY',
'HcCH-COSY':'HcCH-COSY',
'HCcH-COSY':'HCcH-COSY',

# H,N experiments
'15N HSQC/HMQC':'15N HSQC/HMQC',

# H,H,N experiments
'15N HSQC-TOCSY':'15N HSQC-TOCSY',
'15N TOCSY-HSQC':'15N TOCSY-HSQC',
'15N NOESY-HSQC':'15N NOESY-HSQC',
'15N HSQC-NOESY':'15N HSQC-NOESY',
'HBcb/HAcacoNH':'HB/HAcoNH',

# C,H,N experiments
'HNCA/CB':'HNCA/CB',
'hCca-TOCSY-coNH':'hCcacoNH-TOCSY',
'Hcca-TOCSY-coNH':'HccacoNH-TOCSY',
'hCc-TOCSY-NH':'hCcaNH-TOCSY',
'Hcc-TOCSY-NH':'HccaNH-TOCSY',
'HNcoCA/CB':'HNcoCA/CB',
'HNCA':'HNCA',
'HNcaCO':'HNcaCO',
'HNcoCA':'HNcoCA',
'HNCO':'HNCO',
'hbCB/haCAcoNH':'CB/CAcoNH',
}


def resetAllAxisCodes(nmrProject):
  """Reset all axisCodes (ExpDimRef.name) in project to be unique, match the isotope,
  and match the standard Prototype where a prototype is known"""

  stdCodeMap = refExpDimRefCodeMap(nmrProject.root)

  for experiment in nmrProject.sortedExperiments():

    if experiment.refExperiment is None:
      # No prototype - just use nucleus as axis code

      foundCodes = {}
      for expDim in experiment.expDims:
        for expDimRef in expDim.expDimRefs:
          isotopeCodes = expDimRef.isotopeCodes

          # Get axis code
          if expDimRef.measurementType.lower() == 'shift' and len(isotopeCodes) == 1:
            # Normal shift axis, use nucleus to set
            code = isotope2Nucleus(isotopeCodes[0])
          else:
            # Different type of axis.
            # For simplicity set to axis_1, axis_2, ... for now
            print ("WARNING, non-std axis - axisCode set to 'axis'")
            code = 'axis'
            foundCodes[code] = 0

          # add index for duplicates
          indx = foundCodes.get(code)
          if indx is None:
            foundCodes[code] = 0
          else:
            indx += 1
            foundCodes[code] = indx
            code = '%s%s' % (code, str(indx))

          # Set the attribute
          expDimRef.name = code


    else:
      # We have a prototype - use standard axisCode map
      for expDim in experiment.expDims:
        for expDimRef in expDim.expDimRefs:
          expDimRef.name = stdCodeMap[expDimRef.refExpDimRef]



def refExpDimRefCodeMap(project):
  """get RefExpDimRef: axisCode map for all NmrExpPrototypes in project"""
  result = {}

  for nxp in project.sortedNmrExpPrototypes():
    for isReversed in False, True:
      refExperiments = nxp.findAllRefExperiments(isReversed=isReversed)
      if refExperiments:
        measurementMap = _measurementCodeMap(nxp, forReversed=isReversed)
        for re in refExperiments:
          for red in re.refExpDims:
            for redr in red.refExpDimRefs:
              result[redr] = measurementMap[redr.expMeasurement]
  #
  return result


def _measurementCodeMap(nmrExpPrototype, forReversed=False):
  """get expMeasurement:axisCode map"""
  result = {}
  measurements = _orderedMeasurements(nmrExpPrototype, forReversed=forReversed)

  foundCodes = {}
  # get axisCodes per expMeasurement
  for measurement in measurements:
    code = rawAxisCode(measurement)
    indx = foundCodes.get(code)
    if indx is None:
      foundCodes[code] = 0
    else:
      indx += 1
      foundCodes[code] = indx
      code = '%s%s' % (code, indx)
    result[measurement] = code
  #
  return result


def _connectedShiftMeasurements(expMeasurement):
  """find expMeasurements that are of type Shift, match a HX bond, and onebonded to the input measurement"""
  result = []

  nmrExpPrototype = expMeasurement.nmrExpPrototype

  if expMeasurement.measurementType.lower() != 'shift':
    return result

  atomSites = expMeasurement.atomSites
  if len(atomSites) != 1:
    print ("WARNING%s Shift must have single AtomSite, has: %s"
           % (expMeasurement.nmrExpPrototype.name, [x.name for x in atomSites]))
    if not atomSites:
      return result

  expSite = atomSites[0]
  expIsotope = expSite.isotopeCode
  sites = []
  if expIsotope in ('1H', '19F'):
    for et in expSite.findAllExpTransfers(transferType='onebond'):
      for site in et.atomSites:
        if site is not expSite:
          if site.isotopeCode in ('13C', '15N') and site.maxNumber != 0:
            sites.append(site)
          break

  elif expIsotope in ('13C', '15N'):
    for et in expSite.findAllExpTransfers(transferType='onebond'):
      for site in et.atomSites:
        if site is not expSite:
          if site.isotopeCode in ('1H', '19F') and site.maxNumber != 0:
            sites.append(site)
          break

  result = [x for x in nmrExpPrototype.expMeasurements if x.measurementType.lower() == 'shift'
            and x.findFirstAtomSite() in sites]
  #
  return result

def _orderedMeasurements(nmrExpPrototype, forReversed=False):
  """get ExpMeasurements in order: acquisition first, furthest from acquisition last,
  connected measurements grouped together. If forReversed, get with acquisition last
  (for reversed experiments"""

  ll = [tt[1].expMeasurement
        for tt in sorted((x.stepNumber,x)
                         for x in nmrExpPrototype.findFirstExpGraph().expSteps)]
  if not forReversed:
    ll.reverse()

  measurements = []
  for measurement in ll:
    if measurement not in measurements:
      measurements.append(measurement)
      for me in _connectedShiftMeasurements(measurement):
        if me not in measurements:
          measurements.append(me)

  # we do not search all expGraphs, so just add missing measurements to the end
  # this is a heuristic, not a rigid ordering
  for measurement in nmrExpPrototype.expMeasurements:
    if measurement not in measurements:
      measurements.append(measurement)
      for me in _connectedShiftMeasurements(measurement):
        if me not in measurements:
          measurements.append(me)
  #
  return measurements


def rawAxisCode(expMeasurement):
  """Get raw expMeasurement axisCode (without number suffixes) from NmrExpPrototype.ExpMeasurement"""

  em = expMeasurement
  emType = em.measurementType.lower()

  tag = Constants.measurementType2ElementCode.get(emType, emType)
  if tag == 'delay':
    result = tag
  elif tag == 'shift':
    result = ''.join(sorted(atomSiteAxisCode(x) for x in em.atomSites))
  else:
    result = tag + ''.join(sorted(isotope2Nucleus(x.isotopeCode).lower() for x in em.atomSites))
  #
  return result

# def nucleusCode(expMeasurement):
#   """Get nucleusCode from NmrExpPrototype.ExpMeasurement"""
#   from ccpn.util import Constants
#
#   em = expMeasurement
#   emType = em.measurementType.lower()
#
#   tag = Constants.measurementType2ElementCode.get(emType, emType)
#   if tag == 'delay':
#     result = tag
#   else:
#     records = [Constants.isotopeRecords.get(x.isotopeCode.upper() for x in em.atomSites)]
#     if None in records:
#       raise ValueError("Invalid NmrExpPrototype, unknown isotopeCode for atomSite at %s "
#                        % expMeasurement)
#     else:
#       result = ''.join(sorted(x.symbol for x in records))
#       if tag != 'shift':
#         result = tag + result.lower()
#   #
#   return result


def isotope2Nucleus(isotopeCode):
  """remove integer prefix from integer+string string"""
  record = Constants.isotopeRecords.get(isotopeCode)
  if record is None:
    raise ValueError("Isotope %s not recognised")
  else:
    return record.symbol.upper()


def atomSiteAxisCode(atomSite):
  """Get axisCode (without number suffixes) from NmrExPrototype.AtomSite"""

  name = atomSite.name
  result = nucleus = isotope2Nucleus(atomSite.isotopeCode)

  if name == 'CA':
    result = 'CA'

  elif name == 'CO':
    result = 'CO'

  elif nucleus in 'HF':
    # H or F, check if bound to C or N
    ll = []
    for et in atomSite.findAllExpTransfers(transferType='onebond'):
      for site in et.atomSites:
        if site is not atomSite:
          if site.isotopeCode == '13C':
            ss = 'c'
          elif site.isotopeCode == '15N':
            ss = 'n'
          else:
            break
          if site.maxNumber == 0:
              ll.append('-'+ss)
          elif site.minNumber > 0:
              ll.append(ss)

          break

    # In rare cases we get both - this is nonsense, so remove them
    for tags in ('n', '-n'),('c','-c'):
      if tags[0] in ll and tags[1] in ll:
        for tag in tags:
          while tag in ll:
            ll.remove(tag)

    # Now remove the '-x' tags - they were there to catch the above problem
    for tag in ('-n', '-c'):
      while tag in ll:
        ll.remove(tag)

    result += ''.join(sorted(set(ll)))

  elif nucleus in 'CN':

    ll = []
    for et in atomSite.findAllExpTransfers(transferType='onebond'):
      for site in et.atomSites:
        if site is not atomSite:
          if site.isotopeCode == '1H':
            ss = 'h'
          elif site.isotopeCode == '19F':
            ss = 'f'
          else:
            break
          if site.maxNumber == 0:
              ll.append('-'+ss)
          elif site.minNumber > 0:
              ll.append(ss)
          break

    # In rare cases we get both - this is nonsense, so remove them
    for tags in ('h', '-h'),('f','-f'):
      if tags[0] in ll and tags[1] in ll:
        for tag in tags:
          while tag in ll:
            ll.remove(tag)

    # Now remove the '-x' tags - they were there to catch the above problem
    for tag in ('-h', '-f'):
      while tag in ll:
        ll.remove(tag)

    result += ''.join(sorted(set(ll)))
  #
  return result


def testExpPrototypes(resetCodes=False):
  """Test functions and make diagnostic output"""
  from ccpnmodel.ccpncore.lib.Io import Api as apiIo
  project = apiIo.newProject("ExpPrototypeTest", overwriteExisting=True)

  codeMap = refExpDimRefCodeMap(project)

  axisCodeSet = set()
  useNames = {}
  synonyms= []
  for nmrExpPrototype in project.sortedNmrExpPrototypes():
  # for nmrExpPrototype in project.findAllNmrExpPrototypes(serial=292):
    # print("nmrExpPrototype: %s %s " % (nmrExpPrototype, nmrExpPrototype._ID))
    for refExperiment in nmrExpPrototype.sortedRefExperiments():
      # print("refExperiment: %s %s " % (refExperiment, refExperiment._ID))

      # check axis codes
      codes = []
      for red in refExperiment.sortedRefExpDims():
        # print("red: %s %s" % (red, red._ID))
        for redr in red.sortedRefExpDimRefs():
          # print("redr: %s %s " % ( redr, redr._ID))
          code = codeMap[redr]
          codes.append(code)
          axisCodeSet.add(code)
      if len(codes) == len(set(codes)):
        if resetCodes:
          # Codes are unique - set them
          for red in refExperiment.sortedRefExpDims():
            for redr in red.sortedRefExpDimRefs():
              redr.axisCode = codeMap[redr]
      else:
        print ("Duplicate code in %s: %s. SKIPPING" % (refExperiment.name, codes))

      # print ("TEST %s %s" % (refExperiment.name, codes))

      # check for duplicate synonyms and collect all synonyms
      key = refExperiment.name
      usename = refExperiment.synonym or key
      ll = useNames.get(usename, [])
      ll.append(key)
      useNames[usename] = ll
      if usename != key:
        synonyms.append((usename, key))

  print ("All axisCodes: %s" % list(sorted(axisCodeSet)))

  for key, val in sorted(useNames.items()):
    if len(val) > 1:
      print ("Duplicate name: %s %s" % (key, val))

  # for tt in sorted(synonyms):
  #   print ("SYNONYM: %s %s" % tt)

  if resetCodes:
    project.saveModified()

def experimentSynonymSummary():
  """1) set of atomSiteNames appearing
  2) List of dimensionCount, synonym, name, atomNames for refExperiments sorted by name """

  from ccpnmodel.ccpncore.lib.Io import Api as apiIo
  project = apiIo.newProject("ExpPrototypeTest", overwriteExisting=True)

  # NBNB
  # 1) Some refExperiments have no synonym - use the name instead for these

  result= []
  # atomSiteNames = set()
  allAxisCodes = set()
  # Sort refExperiments by name
  refExperiments = list(sorted([x for y in project.nmrExpPrototypes for x in y.refExperiments],
                               key=operator.attrgetter('name')))
  for refExperiment in refExperiments:
      # print("refExperiment: %s %s " % (refExperiment, refExperiment._ID))
      typ = 'NORM'
      # siteNames = []
      axisCodes = []
      synonym = refExperiment.synonym
      for red in refExperiment.sortedRefExpDims():
        ll = [x.axisCode for x in red.sortedRefExpDimRefs()]
        if len(ll) == 1:
          axisCodes.extend(ll)
          allAxisCodes.add(ll[0])
        else:
          axisCodes.append(str(ll))
          typ = 'CPLX'

      data = [typ, len(refExperiment.refExpDims), synonym or refExperiment.name,
              refExperiment.name, axisCodes]
      result.append(data)

          # ss = ','.join(tuple(x.name for x in redr.expMeasurement.atomSites))
          # siteNames.append(ss)
          # atomSiteNames.add(ss)
  #
  return allAxisCodes, result



def fetchIsotopeRefExperimentMap(project:'MemopsRoot') -> Dict:
  """fetch {tuple(sortedNucleusCodes):RefExperiment} dictionary for project
  The key is a tuple of element names ('C, Br, H, D, T, ...) or either of J, MQ, ALT, or delay

  NB, each list value is sorted ad-hoc to bring the most common experiments to the top.
  Do NOT sort or reorder the result"""
  result = {}
  if hasattr(project, '_isotopeRefExperimentMap'):
    result = project._isotopeRefExperimentMap

  if not result:

    tuples = []
    for expPrototype in project.sortedNmrExpPrototypes():
      expGraph = expPrototype.sortedExpGraphs()[0]
      expSteps = sorted(expGraph.expSteps, key=operator.attrgetter('stepNumber'))
      atomSiteCount = len(expPrototype.atomSites)
      for refExperiment in expPrototype.sortedRefExperiments():

        # ExpSteps in order of traversal
        expMeasurements = list(x.expMeasurement for x in expSteps)
        if refExperiment.isReversed:
          expMeasurements.reverse()
        # We now have expMeasurements in traversal order, from start to acquisition

        # Sort key for simple (e.g. shift)
        # versus compound (e.g. coupling, MQ, or reduced-dimensionality) axes
        axisCodes = refExperiment.axisCodes
        multiAxisCodeSort = 100 if None in axisCodes else max(x.count(',') for x in axisCodes)

        # Sort key for start and acquisition dimensions
        ss = expMeasurements[-1].atomSites[0].isotopeCode
        for acqNucleusCode in ss:
          if not acqNucleusCode.isdigit():
            break
        if acqNucleusCode == 'H':
          ll = list(expMeasurements[0].atomSites)
          startsOnProton = (ll[0].isotopeCode == '1H' if len(ll) == 1 else False)
          if startsOnProton:
            # Proton start and end -= sort first
            nucleusAcquisitionSort = -30
          else:
            # Proton end only - sort third
            nucleusAcquisitionSort = -10
        elif acqNucleusCode == 'C':
          # Carbon detection - sort second
          nucleusAcquisitionSort = -20
        else:
          # Other. Sort last, grouping by acquisition nucleus
          nucleusAcquisitionSort = ord(acqNucleusCode)

        refExperimentName = refExperiment.name
        # Ad-hoc - give absolute priority for preferred experiments
        if (refExperiment.synonym or refExperimentName) in priorityNameRemapping:
          multiAxisCodeSort = -100

        # Ad hoc modifications - to get more common experiments first:
        downgrade = ('(', 'base','coupling', '[n')
        adhoc = any(x in refExperimentName for x in downgrade)
        if '{C' in refExperimentName:
          # Give higher priority to CA|Cca experiments
          atomSiteCountMod = atomSiteCount -1
          if 'co' in refExperimentName.lower():
            # Move CB/CA CO experiments yet one more level up
            atomSiteCountMod -= 0.5
        else:
          atomSiteCountMod = atomSiteCount

        # Put result on tuples list, with sorting keys in position
        key = tuple(sorted(refExperiment.nucleusCodes))
        tt = (key, multiAxisCodeSort, nucleusAcquisitionSort, adhoc, atomSiteCountMod,
              len(refExperimentName),refExperiment)
        tuples.append(tt)

    # Sort tuples by arranged sort codes
    tuples.sort()
    for tt in tuples:
      # Get actual result out and in dict

      refExperiment = tt[-1]
      key = tt[0]
      ll = result.get(key, [])
      ll.append(refExperiment)
      result[key] = ll

      # print(key, refExperiment.name, refExperiment.synonym)

    project._isotopeRefExperimentMap = result

  #
  return result


# ExperimentClassification namedtuple, showing which groups a given RefExperiment falls into
ExperimentClassification = collections.namedtuple('ExperimentCharacteristic',
                                                  ('dimensionCount', 'acquisitionNucleus',
                                                   'isThroughSpace','isRelayed',
                                                   'isRelaxation', 'isQuantification', 'isJResolved',
                                                   'isMultipleQuantum', 'isProjection',
                                                   'name', 'synonym'))


def getExpClassificationDict(nmrProject) -> dict:
  """
  Get a dictionary of dictionaries of dimensionCount:sortedNuclei:ExperimentClassification named tuples.
  """
  classificationDict = {}
  for nmrExpProtoType in nmrProject.root.sortedNmrExpPrototypes():
    for refExperiment in nmrExpProtoType.sortedRefExperiments():
      dimensionCount = len(refExperiment.refExpDims)
      if dimensionCount not in classificationDict.keys():
        classificationDict[dimensionCount] = {}
      nucleusCodes = tuple(sorted(refExperiment.nucleusCodes))
      if nucleusCodes not in classificationDict[dimensionCount].keys():
        classificationDict[dimensionCount][nucleusCodes] = []
      classification = getExperimentClassification(refExperiment)
      classificationDict[dimensionCount][nucleusCodes].append(classification)
  return classificationDict


def getExperimentClassification(refExperiment:'RefExperiment') -> ExperimentClassification:
  """Get ExperimentClassification namedtuple, showing which groups a given RefExperiment falls into

  The field names should be self-explanatory, except for 'isQuantification' - this covers
  experiments that are classified as 'quantification' in the NmrExpPrototype description, and are
  *not* relaxation measurements. In practice these are J-measurement experiments (for now)."""

  nmrExpPrototype = refExperiment.nmrExpPrototype
  transferTypes = set(y.transferType for x in nmrExpPrototype.expGraphs for y in x.expTransfers)
  measurementTypes = set(x.measurementType for x in nmrExpPrototype.expMeasurements)

  dimensionCount = len(refExperiment.refExpDims)

  expMeasurement = _orderedMeasurements(nmrExpPrototype, forReversed=refExperiment.isReversed)[0]
  acquisitionNucleus = expMeasurement.atomSites[0].isotopeCode

  isThroughSpace = 'through-space' in transferTypes

  isRelayed = ('relayed' in transferTypes or 'relayed-alternate' in transferTypes)

  isRelaxation = (nmrExpPrototype.category == 'quantification' and any(x for x in measurementTypes
                                                                        if x.startswith('T')))

  isQuantification = (nmrExpPrototype.category == 'quantification' and not isRelaxation)

  isJResolved = 'JCoupling' in measurementTypes

  isMultipleQuantum = 'MQShift' in measurementTypes

  isProjection = ('.2D.' in refExperiment.name or '.3D.' in refExperiment.name)

  name = refExperiment.name

  synonym = refExperiment.synonym or name

  # NEW - bug fix:
  synonym = priorityNameRemapping.get(synonym, synonym)

  result = ExperimentClassification(dimensionCount, acquisitionNucleus, isThroughSpace, isRelayed,
                                    isRelaxation, isQuantification, isJResolved, isMultipleQuantum,
                                    isProjection, name, synonym)
  #
  return result


def testExperimentFilter(project):
  allData = {}
  counters = {}
  for nxp in project.sortedNmrExpPrototypes():
    for rx in nxp.sortedRefExperiments():
      filterData = getExperimentClassification(rx)
      allData[rx.name] = filterData

  fields = list(allData.values())[0]._fields
  byColumns = list(zip(*allData.values()))

  for ii,field in enumerate(fields):
    counters[field] = collections.Counter(byColumns[ii])

  #
  return counters


if __name__ == '__main__':
  pass

  counter = collections.Counter()

  from ccpnmodel.ccpncore.lib.Io.Api import newProject
  project = newProject("ExpPrototypeTest", overwriteExisting=True)
  for cc in project.sortedChemComps():
    counter['ChemComp'] += 1

    for ns in cc.namingSystems:
      counter[ns.name] += 1

    if False: #cc.className == 'StdChemComp':
      for ccv in cc.sortedChemCompVars():
        if ccv.isDefaultVar:
        #   print ('@~@~', cc.molType, cc.code3Letter, cc.code1Letter, ccv.linking, ccv.descriptor)
          ll = sorted(x.name for x in ccv.chemAtoms if x.className == 'ChemAtom' and x.name.startswith('H'))
          print ('\t'.join((cc.molType, cc.code3Letter, str(cc.code1Letter), str(ccv.isDefaultVar),
                            ccv.linking, ccv.descriptor, str(ll))))

  # for item in sorted(testExperimentFilter(project).items()):
  #   pass
  #   # print ('\n%s:\n%s' % item)

  # counter = collections.Counter()
  # for nxp in project.nmrExpPrototypes:
  #   for xx in nxp.atomSites:
  #     counter[(xx.name, xx.isotopeCode)] += 1

  # for item in sorted(counter.items()):
  #   print ('@~@~', item)

  dd = {}
  ala = project.findFirstChemComp(code3Letter='ALA')
  for ns in ala.namingSystems:
    dd[ns.name] = ll = []
    for asn in ns.atomSysNames:
      name = asn.atomName
      sysName = asn.sysName
      if name != sysName:
        ll.append((name, sysName))

  for key, ll in sorted(dd.items()):
    print ('-->', key, ll)

