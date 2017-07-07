"""Utility functions for ChemComp handling

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
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:37 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================



def chemAtomSetFromAtoms(atoms):
  """ Get a ChemAtomSet that matches all atoms

  .. describe:: Input

  List of Nmr.AtomSet or NmrConstraint.FixedAtomSet

  .. describe:: Output

  ChemComp.ChemAtomSet (or None)

  """

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

