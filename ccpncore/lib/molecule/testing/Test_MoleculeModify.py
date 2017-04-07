"""Tests for  package

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
__author__ = "$Author: CCPN $"
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:38 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"

#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: rhf22 $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

#
# Import the Implementation package - this is the root package
#

# from ccpnmodel.ccpncore.lib.Io import Api as apiIo
from ccpnmodel.ccpncore.testing.CoreTesting import CoreTesting
# from ccpn.testing.WrapperTesting import WrapperTesting
from ccpnmodel.ccpncore.lib.molecule import MoleculeModify

class CreateMoleculeTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = None

  def test_create_protein_from_one_letter_string(self):
    seq1 = "QWERTYIPASDFGHKLCVNM"
    startNumber = 10
    molecule1 = MoleculeModify.createMolecule(self.project, seq1, startNumber=startNumber)
    assert molecule1.seqString == seq1, ("seqString %s does not match input %s"
                                         % (molecule1.seqString, seq1))
    residues = molecule1.sortedMolResidues()
    assert residues[0].seqCode == startNumber
    assert residues[-1].seqCode == startNumber + len(seq1) - 1
    assert molecule1.molType == 'protein', ("Molecule %s has non-protein molType: %s"
                                            % (seq1, molecule1.molType))

  def test_create_DNA_from_one_letter_string(self):
    seq1 = "acgitu"
    molecule1 = MoleculeModify.createMolecule(self.project,  seq1, molType='DNA')
    assert molecule1.seqString == seq1.upper(), ("seqString %s does not match input %s"
                                         % (molecule1.seqString, seq1.upper()))
    assert molecule1.molType == 'DNA', ("Molecule %s has non-DNA molType: %s"
                                            % (seq1, molecule1.molType))
    assert molecule1.stdSeqString == seq1.upper(), ("stdSeqString %s does not match input %s"
                                         % (molecule1.seqString, seq1.upper()))

  def test_create_RNA_from_one_letter_string(self):
    seq1 = "acgiu"
    molecule1 = MoleculeModify.createMolecule(self.project,  seq1, molType='RNA')
    assert molecule1.seqString == seq1.upper(), ("seqString %s does not match input %s"
                                         % (molecule1.seqString, seq1.upper()))
    assert molecule1.molType == 'RNA', ("Molecule %s has non-RNA molType: %s"
                                            % (seq1, molecule1.molType))
    assert molecule1.stdSeqString == seq1.upper(), ("stdSeqString %s does not match input %s"
                                         % (molecule1.seqString, seq1.upper()))

  def test_create_cyclic_dna_rna(self):
    seq1 =  ['DA', 'DT', 'DC', 'DG',
            'A', 'C', 'G', 'U', 'DU', 'N', 'DN']
    molecule1 = MoleculeModify.createMolecule(self.project, seq1, isCyclic=True)
    assert molecule1.isStdCyclic, "Molecule is not cyclic as input."

  def test_create_mixed_molecule(self):
    seq1 = ['Ala', 'CYS', 'DAL', 'DVA', 'THR', 'HIS', 'TRP', 'DA', 'DT', 'DC', 'DG',
            'A', 'C', 'G', 'ATP', 'U', 'Ser', 'GDP', 'N', 'DN', 'UNK']
    startNumber = -1
    molecule1 = MoleculeModify.createMolecule(self.project, seq1, startNumber=startNumber)
