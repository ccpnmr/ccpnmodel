"""Functions for insertion into ccp.lims.RefSampleComponent..RefSampleComponentStore

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
from ccpnmodel.ccpncore.api.ccp.molecule.Molecule import Molecule
from ccpn.util.Constants import DEFAULT_LABELLING


def fetchMolComponent(self:"RefSampleComponentStore", molecule:Molecule,
                      labeling:str=None) -> "AbstractComponent":
  """fetch or create new MolComponent matching Molecule name and (if not None) labeling
  labeling for new MolComponents default to std
  NB pre-existing RefComponents returned may be of other types (Cell, Substance or Composite)
  if their names match the molecule
  """
  name = molecule.name
  if labeling is None:
    labeling = DEFAULT_LABELLING
  result = self.findFirstComponent(name=name, labeling=labeling)

  if result is None:
    # Finalise, so molecule does not change 'underneath' substance
    molecule.isFinalised = True
    seqString = molecule.seqString
    if not seqString or '*' in seqString:
      # Set seqString (one-letter or comma-separated) that allows recreating the molecule
      seqString = ','.join(x.chemComp.code3Letter for x in molecule.sortedMolResidues())

    # Make new MolComponent
    result = self.newMolComponent(name=name, labeling=labeling, synonyms=molecule.commonNames,
                                  details=molecule.details, smiles=molecule.smiles,
                                  empiricalFormula=molecule.empiricalFormula,
                                  molecularMass=molecule.molecularMass,
                                  molType=molecule.molType, seqString=seqString)
  elif result.className != 'MolComponent':
    self.root._logger.error("Molecule %s matches Substance of incorrect type: %s"
    % (molecule, result))
  #
  return result
