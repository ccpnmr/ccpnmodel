"""Functions for insertion into ccp.molecule.Molecule.MolSystem.Residue

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

from typing import Tuple, List
from ccpn.util.Constants import DEFAULT_ISOTOPE_DICT
from ccpnmodel.ccpncore.lib.molecule import Labeling

def findLinkedResidue(self:"Residue", linkCode:str='prev'):
  """find residue linked to current with link of type 'linkCode' (defaults to 'prev')
  Use 'prev' to find previous residue, 'next' to find next residue"
  .. describe:: Input

  MolSystem.Residue

  .. describe:: Output

  MolSystem.Residue
  """
  newMolResidue = None
  linkEnd = self.molResidue.findFirstMolResLinkEnd(linkCode=linkCode)
  if linkEnd is not None:
    for otherEnd in linkEnd.molResLink.molResLinkEnds:
      if otherEnd is not linkEnd:
        newMolResidue = otherEnd.molResidue
        break

  if newMolResidue is None:
    return None
  else:
    return self.chain.findFirstResidue(seqId=newMolResidue.serial)

def getReferenceChemCompVar(self) -> 'ChemCompVar':
  """Get Reference ChemCompVar, as used in the NEF standard.

  Could be a derived, immutable link in the API model, but implemented as
  function for flexibility.

  NBNB - This does *NOT* always give the correct variant according to the NEF standard:
  In some cases there is no ChemCompVar that matches - see comments in code.
  These cases must be tested and compensated for in the calling code.
  """
  chemComp = self.chemCompVar.chemComp
  molType = chemComp.molType
  residueType = chemComp.code3Letter

  if molType =='other':
    result = chemComp.findFirstChemCompVar(linking='none', isDefaultVar=True)

  elif molType =='dummy':
    result = chemComp.findFirstChemCompVar(linking='dummy', isDefaultVar=True)

  elif residueType == 'HIS':
    codes = {
      'start':"prot:H3,HD1;deprot:HE2",
      'middle':"prot:HD1;deprot:HE2",
      'end':"prot:HD1;deprot:H'',HE2",
      'none':"H3,HD1;deprot:H'',HE2",
    }
    # This should never be None
    result = chemComp.findFirstChemCompVar(linking=self.linking,
                                           descriptor=codes.get(self.linking))

    # for ccv in chemComp.findAllChemCompVars(linking=self.linking):
    #   variantParts = ccv.descriptor.split(';')
    #   if (len(variantParts) > 1 and 'HD1' in variantParts[0] and 'HE2' in variantParts[1]):
    #     result = ccv
    #     break
    # else:
    #   raise ValueError("No ChemCompVar with prot:HD1, deprot:HE2 found for HIS, linking %s"
    #                    % self.linking)

  elif self.linking == 'start' and residueType in ('DA', 'DC', 'DG', 'DT', 'A', 'C', 'G', 'U', ):
    # NBNB This is NOT the correct result, but it is the closest we can get.
    # Must be fixed downstream
    result = chemComp.findFirstChemCompVar(linking='start', isDefaultVar=True)

  elif (chemComp.className == 'StdChemComp' and (molType == 'protein' or
            residueType in ('DA', 'DC', 'DG', 'DT', 'A', 'C', 'G', 'U', ))):
    # NEF Standard Residue - OK
    result = chemComp.findFirstChemCompVar(linking=self.linking, isDefaultVar=True)

  else:
    # protein, DNA, or RNA, but not a standard residue.
    # NBNB This is NOT the correct result, but it is the closest we can get.
    # Must be fixed downstream
    result = chemComp.findFirstChemCompVar(linking='none', isDefaultVar=True)
  #
  return result

def getAtomNameDifferences(self) -> Tuple[List[str], List[str]]:
  """return list of atomNamesRemoved, atomNamesAdded, relative to reference standard"""
  refChemCompVar = self.getReferenceChemCompVar()
  chemComp = refChemCompVar.chemComp
  molType = chemComp.molType
  namingSystem = chemComp.findFirstNamingSystem(name='PDB_REMED')
  linking = self.linking

  refAtomNames = set()
  for chemAtom in refChemCompVar.chemAtoms:
    atomSysName = namingSystem.findFirstAtomSysName(atomName=chemAtom.name)
    if atomSysName:
      refAtomNames.add(atomSysName.sysName)
    else:
      refAtomNames.add(chemAtom.name)

  # refAtomNames = set(x.name for x in refChemCompVar.chemAtoms
  #                    if x.className == 'ChemAtom')


  # NBNB for non-std protein/RNA/DNA we are NOT going back to
  # neutral form for backbone, but only for the side chain.
  # For backbone we are using linking-appropriate atoms
  # (but keeping neutral protonation states)
  # # This should be cleared with teh NEF standard..

  if molType == 'protein':
    if chemComp.className != 'StdChemComp':
      # NBNB we use PDB_REMED (O, OXT, HXT) for (O', O'', H'')
      if 'H3' in refAtomNames:
        refAtomNames.remove('H3')
      if (linking in ('end', 'none') and "HXT" not in refAtomNames
          and chemComp.findFirstChemAtom(name="H''")):  # NB "H''" is deliberate!!
        refAtomNames.add("HXT")

  elif molType in ('DNA', 'RNA'):
    if chemComp.code3Letter in ('DA', 'DC', 'DG', 'DT', 'A', 'C', 'G', 'U'):
      # Standard DNA or RNA
      for name in ('HOP2', 'HOP3'):
        if name in refAtomNames:
          refAtomNames.remove(name)
      if linking == 'start':
        # Remove phosphate for start variant
        for name in ('P', 'OP1', 'OP2', 'OP3'):
          if name in refAtomNames:
            refAtomNames.remove(name)
        if "HO5'" not in refAtomNames:
          refAtomNames.add("HO5'")
  #
  atomNames = [x.name for x in self.atoms if x.atomType == 'single']

  atomNamesRemoved = list(set(refAtomNames).difference(atomNames))
  atomNamesAdded = list(set(atomNames).difference(refAtomNames))
  #
  return atomNamesRemoved, atomNamesAdded


# # NBNB TODO FIXME update this to work.
#
# def findResidueObservableAtoms(residue, refExperiment=None, labeling=None,
#                               minFraction:float=0.1, jCouplingBonds=(1,2,3),
#                               usePermissiveShifts:bool=False,
#                               chemElements=('H','C','N','F','P')):
#   """
#   Determine which atoms of a chem comp variant would give rise to
#   observable resonances considering a given reference experiment
#   and/or an isotope labeling scheme. Can specify minimum fraction of
#   an isotope to consider something observable and the chemical elements which
#   you are observing. Boolean option to match database min and max
#   chemical shift bounds to atom sites, rather than randon coil shift
#   values (default).
#
#   .. describe:: Input
#
#   MolSystem.Residue, NmrExpPrototype.RefExperiment,
#   ChemCompLabel.LabelingScheme or LabeledMolecule.LabeledMixture,
#   Float, Boolean, List of Words
#
#   .. describe:: Output
#
#   List of ChemComp.ChemAtoms
#   """
#
#   if not jCouplingBonds:
#     jCouplingBonds = (0,)
#
#   atomSiteDict   = {}
#   isotopomerDict = {}
#   atomSitesAll   = {}
#
#   if refExperiment:
#     for atomSite in refExperiment.nmrExpPrototype.atomSites:
#       isotope = atomSite.isotopeCode
#       if not isotope in atomSitesAll:
#         atomSitesAll[isotope] = []
#
#       atomSitesAll[isotope].append(atomSite)
#
#   isotopeDict = {}
#
#   if atomSitesAll:
#     isotopes = atomSitesAll.keys()
#
#   else:
#     isotopes = []
#     for element in chemElements:
#       # NBNB FIXME update to use new isotope dictionaries
#       isotope = DEFAULT_ISOTOPE_DICT.get(element)
#
#       if isotope:
#         isotopes.append(isotope)
#
#   for isotope in isotopes:
#     element = isotope
#
#     while element[0] in '0123456789':
#       element = element[1:]
#
#     isotopeDict[element] = isotope
#
#
#   filteredAtoms = []
#   nextMolResiduen= residue.molResidue.nextMolResidue
#
#   prevResidue = residue.findLinkedResidue('prev')
#   nextResidue = residue.findLinkedResidue('next')
#
#   natAbundance = residue.root.findFirstLabelingScheme(name='NatAbun')
#
#   #print residue.seqCode, residue.ccpCode, refExperiment.name
#   for residue0 in (prevResidue,residue,nextResidue):
#     isotopomers = None
#
#     if residue0:
#       resId = residue0.molResidue.serial
#       atoms = residue0.atoms
#
#       # Compile isotopomers for this residue
#       if labeling and (labeling.className == 'LabelingScheme'):
#         chemComp   = residue0.chemCompVar.chemComp
#         ccpCode    = chemComp.ccpCode
#         molType    = chemComp.molType
#         chemCompLabel = labeling.findFirstChemCompLabel(ccpCode=ccpCode,
#                                                         molType=molType)
#
#         if not chemCompLabel:
#           chemCompLabel = natAbundance.findFirstChemCompLabel(ccpCode=ccpCode,
#                                                               molType=molType)
#
#
#         if chemCompLabel:
#           isotopomers  = chemCompLabel.isotopomers
#           isotopomerDict[residue0] = isotopomers
#
#
#     else:
#       atoms = []
#
#     #atoms0 = [] # Those which make it through the filter
#     for atom in atoms:
#       chemAtom = atom.chemAtom
#       isotope  = isotopeDict.get(chemAtom.elementSymbol)
#
#       if not isotope:
#         continue
#
#       if chemAtom.waterExchangeable:
#         continue
#
#       if isotopomers:
#         fractionDict = Labeling._getIsotopomerSingleAtomFractions(isotopomers,atom.name,
#                                                                   chemAtom.subType)
#         # Exclude if no isotope incorporation above threshold
#         fraction = fractionDict.get(isotope, minFraction)
#         if fraction < minFraction:
#           continue
#
#       elif labeling:
#         fractionDict = Labeling._singleAtomFractions(labeling, resId, atom.name)
#         if not fractionDict:
#           continue
#
#         fraction = fractionDict.get(isotope, minFraction)
#         if fraction < minFraction:
#           continue
#
#
#       atomSitesIsotope = atomSitesAll.get(isotope)
#       if atomSitesIsotope:
#         setSize = None
#
#         if usePermissiveShifts:
#           shifts = getChemicalShiftBounds(chemAtom)
#           if not shifts:
#             shifts = [getRandomCoilShift(chemAtom),]
#
#         else:
#           shifts = [getRandomCoilShift(chemAtom),]
#
#         for atomSite in atomSitesIsotope:
#
#           maxShift = atomSite.maxShift
#           if (maxShift is not None) and (shifts[0] > maxShift):
#             continue
#
#           minShift = atomSite.minShift
#           if (minShift is not None) and (shifts[-1] < minShift):
#             continue
#
#           if setSize is None:
#             setSize     = 1
#             chemAtomSet = chemAtom.chemAtomSet
#
#             if chemAtomSet:
#               setSize = len(chemAtomSet.chemAtoms)
#
#           minNumber =  atomSite.minNumber
#           if setSize < minNumber:
#             continue
#
#           maxNumber = atomSite.maxNumber
#           if maxNumber and (setSize>maxNumber):
#             continue
#
#           numberStep = atomSite.numberStep
#           if (setSize-minNumber) % numberStep != 0:
#             continue
#
#           if atomSiteDict.get(atomSite) is None:
#             atomSiteDict[atomSite] = []
#           atomSiteDict[atomSite].append(atom)
#
#           #print 'AS', atomSite.name, atom.name
#
#       filteredAtoms.append(atom)
#
#
#   if refExperiment:
#     #print refExperiment.name
#
#     # Atom sites which are possibly visible given dims
#     observableAtomSites = {}
#     for refExpDim in refExperiment.refExpDims:
#       for refExpDimRef in refExpDim.refExpDimRefs:
#         for atomSite in refExpDimRef.expMeasurement.atomSites:
#           observableAtomSites[atomSite] = True
#
#     # Get prototype graph atomSite routes
#
#     graphRoutes = []
#     for expGraph in refExperiment.nmrExpPrototype.expGraphs:
#       expSteps = [(es.stepNumber, es) for es in expGraph.expSteps]
#       expSteps.sort()
#       routes = []
#       stepNumber, expStep = expSteps[0]
#
#       for atomSite in expStep.expMeasurement.atomSites:
#         route = [(atomSite,None,stepNumber)]
#         routes.append(route)
#
#       while True:
#         routes2 = []
#
#         for route in routes:
#           atomSiteA, null, stepA = route[-1]
#           #print atomSiteA.name, step
#
#           for expTransfer in atomSiteA.expTransfers:
#             atomSites = list(expTransfer.atomSites)
#             atomSites.remove(atomSiteA)
#             atomSiteB = atomSites[0]
#
#             if not expTransfer.transferToSelf:
#               if atomSiteB is atomSiteA:
#                 continue
#
#             for stepB, expStepB in expSteps:
#               if stepA > stepB:
#                 continue
#
#               if atomSiteB in expStepB.expMeasurement.atomSites:
#                 routes2.append( route[:] + [(atomSiteB,expTransfer,stepB)] )
#                 #print ['%s %d' % (a[0].name, a[2]) for a in routes2[-1]]
#                 break
#
#         if routes2:
#           routes = routes2
#         else:
#           break
#
#       for route in routes:
#         atomRoutes = []
#         lastAtomSite = route[-1][0]
#
#         for i in range(len(route)-1):
#           atomSiteA, null, stepA = route[i]
#           atomSiteB, expTransfer, stepB = route[i+1]
#           transferType = expTransfer.transferType
#
#           #print stepA, atomSiteA.name, stepB, atomSiteB.name, transferType
#
#           if atomRoutes:
#             atomsA = [r[-1][0] for r in atomRoutes]
#           else:
#             atomsA = atomSiteDict[atomSiteA]
#
#           atomRoutes2 = []
#           for atomA in atomsA:
#             for atomB in atomSiteDict[atomSiteB]:
#               if isotopomerDict:
#                 chemAtomA = atomA.chemAtom
#                 chemAtomB = atomB.chemAtom
#                 subTypeA  = chemAtomA.subType
#                 subTypeB  = chemAtomB.subType
#                 isotopeA  = isotopeDict[chemAtomA.elementSymbol]
#                 isotopeB  = isotopeDict[chemAtomB.elementSymbol]
#                 residueA  = atomA.residue
#                 residueB  = atomB.residue
#
#                 if residueA is residueB:
#                   isotopomersA = isotopomerDict.get(residueA)
#                   atomNames    = (atomA.name, atomB.name)
#                   subTypes     = (subTypeA, subTypeB)
#                   pairDict     = Labeling._getIsotopomerAtomPairFractions(isotopomersA, atomNames,
#                                                                           subTypes)
#                   fraction     = pairDict.get((isotopeA, isotopeB), minFraction)
#
#                   if fraction  < minFraction:
#                     continue
#
#                 else:
#                   isotopomersA = isotopomerDict.get(residueA)
#                   isotopomersB = isotopomerDict.get(residueB)
#
#                   if isotopomersB and isotopomersA:
#                     fractionDictA = Labeling._getIsotopomerSingleAtomFractions(isotopomersA,
#                                                                                atomA.name, subTypeA)
#                     fractionDictB = Labeling._getIsotopomerSingleAtomFractions(isotopomersB,
#                                                                                atomB.name, subTypeB)
#                     fraction = fractionDictA.get(isotopeA, 1.0) * fractionDictB.get(isotopeB, 1.0)
#
#                     if fraction < minFraction:
#                       continue
#
#               elif labeling:
#                 chemAtomA = atomA.chemAtom
#                 chemAtomB = atomB.chemAtom
#                 isotopeA  = isotopeDict[chemAtomA.elementSymbol]
#                 isotopeB  = isotopeDict[chemAtomB.elementSymbol]
#                 residueA = atomA.residue
#                 residueB = atomB.residue
#                 molResidueA = residueA.molResidue
#                 molResidueB = residueB.molResidue
#                 resIds = (molResidueA.serial, molResidueB.serial)
#                 atomNames = (atomA.name, atomB.name)
#
#                 pairDict = Labeling._atomPairFractions(labeling, resIds, atomNames)
#                 fraction = pairDict.get((isotopeA, isotopeB), minFraction)
#
#                 if fraction  < minFraction:
#                   continue
#
#               addAtom = False
#               if transferType in longRangeTransfers:
#                 addAtom = True
#
#               elif transferType in ('onebond','CP') and areAtomsBound(atomA, atomB):
#                 addAtom = True
#
#               elif transferType == 'TOCSY'and areAtomsTocsyLinked(atomA, atomB):
#                 addAtom = True
#
#               elif transferType == 'Jcoupling':
#                 numBonds = getNumConnectingBonds(atomA, atomB, limit=max(jCouplingBonds))
#                 if numBonds in jCouplingBonds:
#                   addAtom = True
#
#               elif transferType == 'Jmultibond' and not areAtomsBound(atomA, atomB):
#                 numBonds = getNumConnectingBonds(atomA, atomB, limit=max(jCouplingBonds))
#                 if numBonds in jCouplingBonds:
#                   addAtom = True
#
#               if addAtom:
#                 grown = True
#                 #print 'AB', atomA.name, atomA.residue.seqCode,'+', atomB.name, atomB.residue.seqCode
#                 if not atomRoutes:
#                   atomRoutes2.append( [(atomA,atomSiteA),(atomB,atomSiteB),] )
#                   #print atomA.name, atomB.name
#
#                 else:
#                   for atomRoute in atomRoutes:
#                     atomRoutes2.append( atomRoute[:] + [(atomB,atomSiteB),] )
#                   #print '+', atomB.name
#
#
#           atomRoutes = []
#           for atomRoute in atomRoutes2:
#             if atomRoute[-1][1] is lastAtomSite:
#               atomRoutes.append(atomRoute)
#
#         graphRoutes.append(atomRoutes)
#
#
#     observableAtoms = set()
#     for routes in graphRoutes:
#       for route in routes:
#
#         for atomB, atomSiteB in route:
#           if atomB.residue is residue: # Must have one atom from this residue
#             for atomA, atomSiteA in route:
#               if observableAtomSites.get(atomSiteA):
#                 observableAtoms.add(atomA)
#             break
#
#   else:
#     observableAtoms = filteredAtoms
#
#   return list(observableAtoms)
#
