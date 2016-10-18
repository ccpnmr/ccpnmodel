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


from ccpnmodel.ccpncore.testing.CoreTesting import CoreTesting
import os
from ccpn.util import Path
from ccpnmodel.ccpncore.lib.molecule import MoleculeModify
from ccpnmodel.ccpncore.lib.molecule.MolStructure import  makeEmptyStructureEnsemble
TEST_PROJECTS_PATH = os.path.join(Path.getTopDirectory(), 'internal', 'data', 'testProjects')
from ccpnmodel.ccpncore.memops.ApiError import ApiError



class StructureEnsembleTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = None

  def testSpecificNames(self):
    chainAtomNames = [
      'C', 'CA', 'H%', 'H1', 'H2', 'H3', 'HA%', 'HA2', 'HA3', 'HAx', 'HAy',  'N', 'O', 'QA',
      'C', 'CA', 'CB', 'H', 'HA', 'HB%', 'HB1', 'HB2', 'HB3', 'MB', 'N', 'O',
      'C', 'CA', 'H', 'HA%', 'HA2', 'HA3', 'HAx', 'HAy', 'N', "O'", "O''", 'QA']

    project = self.project
    molSystem = project.newMolSystem(code='A')
    molecule = MoleculeModify.createMolecule(project, 'GAG', name='gag')
    chain = molSystem.newChain(code='X', molecule=molecule)
    ensemble = makeEmptyStructureEnsemble(molSystem)
    atoms = ensemble.orderedAtoms
    self.assertEquals([x.name for x in atoms], chainAtomNames)

    model0 = ensemble.newModel()
    self.assertEquals(list(model0.specificAtomNames), chainAtomNames)

    model1 = ensemble.newModel()
    model2 = ensemble.newModel()
    atom0 = atoms[0]
    atom1 = atoms[1]
    atom2 = atoms[2]
    self.assertEqual(atom0.modelSpecificNames, ('C','C','C'))
    self.assertEqual(atom0.implSpecificNames, ())

    newNames = ('X', 'Y', 'Z')
    atom1.modelSpecificNames = newNames
    self.assertEqual(atom1.modelSpecificNames, newNames)
    self.assertEqual(atom1.implSpecificNames, newNames)

    atom0.changeModelSpecificName(model1, 'II')
    atom1.changeModelSpecificName(model2, 'JJ')
    self.assertEqual(model0.specificAtomNames[:3], ('C', 'X', 'H%'))
    self.assertEqual(model1.specificAtomNames[:3], ('II', 'Y', 'H%'))
    self.assertEqual(model2.specificAtomNames[:3], ('C', 'JJ', 'H%'))
    self.assertEqual(atom0.modelSpecificNames, ('C','II','C'))
    self.assertEqual(atom1.modelSpecificNames, ('X','Y','JJ'))
    self.assertEqual(atom2.modelSpecificNames, ('H%','H%','H%'))
    self.assertEqual(atom0.implSpecificNames, ('C','II','C'))
    self.assertEqual(atom1.implSpecificNames, ('X','Y','JJ'))
    self.assertEqual(atom2.implSpecificNames, ())
    self.assertEqual(atom1.fetchModelSpecificName(model0), 'X')
    self.assertEqual(atom1.fetchModelSpecificName(model1), 'Y')
    self.assertEqual(atom1.fetchModelSpecificName(model2), 'JJ')
    self.assertEqual(atom2.fetchModelSpecificName(model0), 'H%')

    model1.delete()
    self.assertEqual(atom0.modelSpecificNames, ('C', 'C'))
    self.assertEqual(atom1.modelSpecificNames, ('X','JJ'))
    self.assertEqual(atom2.modelSpecificNames, ('H%','H%'))
    self.assertEqual(atom0.implSpecificNames, ('C','C'))
    self.assertEqual(atom1.implSpecificNames, ('X','JJ'))
    self.assertEqual(atom2.implSpecificNames, ())

    ensemble.newModel()
    self.assertEqual(atom0.modelSpecificNames, ('C', 'C', 'C'))
    self.assertEqual(atom1.modelSpecificNames, ('X','JJ', 'CA'))
    self.assertEqual(atom2.modelSpecificNames, ('H%','H%', 'H%'))
    self.assertEqual(atom0.implSpecificNames, ('C','C', 'C'))
    self.assertEqual(atom1.implSpecificNames, ('X','JJ', 'CA'))
    self.assertEqual(atom2.implSpecificNames, ())
