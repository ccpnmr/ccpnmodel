"""Functions for insertion into ccp.molecule.Molecule.MolSystem.Residue

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
__version__ = "$Revision: 3.0.b4 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from typing import Tuple, List
from ccpn.util.Constants import DEFAULT_ISOTOPE_DICT
from ccpnmodel.ccpncore.lib.molecule import Labeling


def findLinkedResidue(self: "Residue", linkCode: str = 'prev'):
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

    if molType == 'other':
        result = chemComp.findFirstChemCompVar(linking='none', isDefaultVar=True)

    elif molType == 'dummy':
        result = chemComp.findFirstChemCompVar(linking='dummy', isDefaultVar=True)

    elif residueType == 'HIS':
        codes = {
            'start' : "prot:H3,HD1;deprot:HE2",
            'middle': "prot:HD1;deprot:HE2",
            'end'   : "prot:HD1;deprot:H'',HE2",
            'none'  : "H3,HD1;deprot:H'',HE2",
            }
        # This should never be None
        result = chemComp.findFirstChemCompVar(linking=self.linking,
                                               descriptor=codes.get(self.linking))


    elif self.linking == 'start' and residueType in ('DA', 'DC', 'DG', 'DT', 'A', 'C', 'G', 'U',):
        # NBNB This is NOT the correct result, but it is the closest we can get.
        # Must be fixed downstream
        result = chemComp.findFirstChemCompVar(linking='start', isDefaultVar=True)

    elif (chemComp.className == 'StdChemComp' and (molType == 'protein' or
                                                   residueType in ('DA', 'DC', 'DG', 'DT', 'A', 'C', 'G', 'U',))):
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
    for chemAtom in refChemCompVar.findAllChemAtoms(className='ChemAtom'):
        atomSysName = namingSystem.findFirstAtomSysName(atomName=chemAtom.name)
        if atomSysName:
            refAtomNames.add(atomSysName.sysName)
        else:
            refAtomNames.add(chemAtom.name)

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
