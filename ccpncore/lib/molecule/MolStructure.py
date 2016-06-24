"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Luca Mureddu, Simon Skinner, Geerten Vuister"
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


def makeEmptyStructureEnsemble(molSystem):
  """Make an empty StructureEnsemble matching MolSystem"""
  project = molSystem.root
  nextId = 0
  for ee in project.structureEnsembles:
    nextId = max(nextId, ee.ensembleId)
  nextId += 1
  ensemble = project.newStructureEnsemble(molSystem=molSystem, ensembleId=nextId)
  for cc in molSystem.sortedChains():
    chain = ensemble.newChain(code=cc.code)
    for rr in cc.sortedResidues():
      residue = chain.newResidue(seqCode=rr.seqCode, seqInsertCode=rr.seqInsertCode,
                                 code3Letter=rr.code3Letter, seqId = rr.seqId)
      for aa in rr.sortedAtoms():
        atom = residue.newAtom(name=aa.name, elementName=aa.elementSymbol)
  #
  return ensemble

