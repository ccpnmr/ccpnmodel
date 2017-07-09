"""Module Documentation here

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:16 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================


from ccpnmodel.ccpncore.testing.CoreTesting import CoreTesting
import os
from ccpn.util import Path
TEST_PROJECTS_PATH = os.path.join(Path.getTopDirectory(), 'internal', 'data', 'testProjects')
from ccpnmodel.ccpncore.memops.ApiError import ApiError

class NaNtest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = None

  def testNaN(self):
    spectrum = self.nmrProject.createDummySpectrum(name='nanTest', axisCodes=('Hn', 'Nh', 'CO'))
    self.assertEqual(spectrum.scale, 1.0)
    self.assertEqual(spectrum.name, 'nanTest')

    # test NaN
    self.assertRaises(ApiError,setattr, spectrum, 'scale', float('NaN'))

class CrosslinkUndoTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = None

  def test_many_to_one(self):
    root = self.nmrProject.root
    nmrProjects = [root.newNmrProject(name=str(x)) for x in range(6)]
    ms0, ms1, ms2 = [root.newMolSystem(code=str(x)) for x in range(3)]
    ms0.nmrProjects = nmrProjects[:2]
    ms1.nmrProjects = nmrProjects[2:4]
    self.undo.newWaypoint()
    ms1.nmrProjects = nmrProjects[1:3]
    self.assertEquals(ms0.nmrProjects, frozenset((nmrProjects[0],)))
    self.assertEquals(ms1.nmrProjects, frozenset(nmrProjects[1:3]))
    self.assertEquals(set(x for x in nmrProjects if x.molSystem is None), set(nmrProjects[3:]))
    self.undo.undo()
    self.assertEquals(ms0.nmrProjects, frozenset(nmrProjects[:2]))
    self.assertEquals(ms1.nmrProjects, frozenset(nmrProjects[2:4]))
    self.assertEquals(set(x for x in nmrProjects if x.molSystem is None), set(nmrProjects[4:]))

  def test_many_to_one_deletion(self):
    root = self.nmrProject.root
    nmrProjects = [root.newNmrProject(name=str(x)) for x in range(6)]
    ms0 = root.newMolSystem(code='0')
    ms0.nmrProjects = nmrProjects[:4]
    self.undo.newWaypoint()
    ms1 = root.newMolSystem(code='1', nmrProjects=nmrProjects[2:])
    self.assertEquals(ms0.nmrProjects, frozenset(nmrProjects[:2]))
    self.assertEquals(ms1.nmrProjects, frozenset(nmrProjects[2:]))
    self.undo.undo()
    self.assertTrue(ms1.isDeleted)
    self.assertEquals(set(x for x in nmrProjects if x.molSystem is None), set(nmrProjects[4:]))
    self.assertEquals(ms0.nmrProjects, frozenset(nmrProjects[:4]))

  # NB you could have a similar problem with 0..1 <-> 0..1 links, but the only underived,
  # unfrozen example is ccp.molecule.MolStructure.StructureEnsemble.structureGeneration,
  # Which is not in use, so it is not worth teh hassle


  def test_many_to_one_add(self):
    root = self.nmrProject.root
    nmrProjects = [root.newNmrProject(name=str(x)) for x in range(4)]
    ms0, ms1 = [root.newMolSystem(code=str(x)) for x in range(2)]
    ms0.nmrProjects = nmrProjects[:2]
    ms1.nmrProjects = nmrProjects[2:4]
    self.undo.newWaypoint()
    ms1.addNmrProject(nmrProjects[1])
    self.assertEquals(ms0.nmrProjects, frozenset((nmrProjects[0],)))
    self.assertEquals(ms1.nmrProjects, frozenset(nmrProjects[1:4]))
    self.undo.undo()
    self.assertEquals(ms0.nmrProjects, frozenset(nmrProjects[:2]))
    self.assertEquals(ms1.nmrProjects, frozenset(nmrProjects[2:4]))
