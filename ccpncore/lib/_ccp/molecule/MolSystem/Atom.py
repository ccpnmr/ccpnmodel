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


def expandNewAtom(self: 'Atom'):
  """Add compound Atoms and Bonds when template atoms are (re)added"""

  # NBNB This could be done differently.
  # It might be better to merge this wih expandMolSystemAtoms
  # but in order not to mess with the complexities of the expandMolSystemAtoms
  # function (which does the same job, but in batch) this is simpler

  apiResidue = self.residue
  apiChemAtom = self.chemAtom
  if apiChemAtom is not None:
    apiChemAtomSet = apiChemAtom.chemAtomSet
    if apiChemAtomSet is not None:
      # NB, we do not want to add atoms for '*', but rather for '%'
      newName = apiChemAtomSet.name.replace('*', '%')
      apiAtomGroup = apiResidue.findFirstAtom(name=newName)
      if apiAtomGroup is None:
        # NB - this is not tested and is likely to be used VERY rarely, if at all.
        # Basically this is the case where we have a ChemAtomSet in the template,
        # had only ONE of the relevant atoms previously, and are now adding the second
        # atom, so we have to create the Atom matching the ChemAtomSet.

        # check if we now have atoms to create one
        apiAtoms = []
        for aca in apiChemAtomSet.chemAtoms:
          aa = apiResidue.findFirstAtom(name=aca.name)
          if aa is not None:
            apiAtoms.append(aa)
        if len(apiAtoms) > 1:

          # NB this is slightly heuristic,
          # but I'd say it is as good as can reasonably be expected
          if apiChemAtomSet.isEquivalent:
            atomType = 'equivalent'
          elif len(apiChemAtomSet.chemAtoms) == 2:
            atomType = 'pseudo'
          else:
            atomType = 'nonstereo'

          apiResidue.newAtom(name=newName, components=apiAtoms,
                             atomType=atomType, elementSymbol=apiChemAtomSet.elementSymbol)
      else:
        # ChemAtomSet already exists in wrapper in partial form.
        # In Practice we must be adding the third H to an NH3 group
        apiAtomGroup.addComponent(self)

      # Add bonds from template
      for apiChemBond in apiChemAtom.chemBonds:
        apiAtoms = set(apiResidue.findFirstAtom(name=x.name)
                       for x in apiChemBond.chemAtoms)
        for aa in apiAtoms:
          if aa is not None and aa is not self and aa not in self.boundAtoms:
            self.addBoundAtom(aa)
