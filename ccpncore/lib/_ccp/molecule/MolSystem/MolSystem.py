"""Functions to be copied automatically into ccpnmodel.ccpncore..api.ccp.molecule.MolSystem.MolSystem

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:11 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b5 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

def nextChainCode(self: "MolSystem"):
    """Descrn: Gives the first unused chain code for a molSystem, starting as close to 'A' as possible
       Inputs: Ccp.MolSystem.MolSystem
       Output: Word (Ccp.MolSystem.Chain.code)
    """

    chains = self.sortedChains()

    if not chains:
        return 'A'

    codes = []
    for chain in chains:
        codes.append(chain.code)

    code = 'A'
    while code in codes:
        i = ord(code)
        i += 1
        j = i - ord('A')
        if j >= 26:
            code = chr(ord('A') + int(j / 26)) + chr(ord('A') + int(j % 26))
        else:
            code = chr(i)

    return code


def createSimpleChain(self: "MolSystem", molecule: "Molecule", code: str = None):
    """Descrn: Make a molSystem chain based upon an input molecule template
       Inputs: Ccp.MolSystem.MolSystem, Ccp.Molecule.Molecule, Word
       Output: Ccp.MolSystem.Chain
    """

    if code is None:
        code = nextChainCode(self)

    chain = self.newChain(code=code, molecule=molecule)

    if len(molecule.molResidues) == 1:
        details = molecule.findFirstMolResidue().chemComp.name
    else:
        details = molecule.seqString

    if details:
        if len(details) > 10:
            details = details[:10] + '...'

        chain.setDetails(details)

    return chain
