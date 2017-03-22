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
TEST_PROJECTS_PATH = os.path.join(Path.getTopDirectory(), 'internal', 'data', 'testProjects')



class UpgradeMolSystemTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = 'HaddockGUItest'

  def testMolsystemUpgrade(self):

    molSystemSummary = dict((
      ('1P91',['A', 'B', 'C', 'DNA-A', 'RNA-A', 'SAM-A', 'T33-A']),
      ('DNA',['A']),
      ('RNA',['A']),
      ('SAM',['A']),
      ('T33',['A']),
  ))

    project = self.project
    project.checkAllValid(complete=True)

    dd = {}
    for molSystem in project.sortedMolSystems():
      dd[molSystem.code] = [x.code for x in molSystem.sortedChains()]

    self.assertTrue(dd == molSystemSummary)

  def testHaddockUpgrade(self):
    haddockPartnerSummary = dict((
      ('A', ('1P91',['RNA-A'])),
      ('B', ('1P91',['T33-A']))
    ))

    project = self.project
    project.checkAllValid(complete=True)

    dd = {}

    for haddock in project.sortedHaddockProjects():
      for partner in haddock.sortedHaddockPartners():
        dd[partner.code] = (partner.molSystem.code,
                            [x.chain.code for x in partner.sortedChains()])

    self.assertTrue(dd == haddockPartnerSummary)


class UpgradeSamplesTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = '2x8n_str3_CCPN_mod'

  def testSamplesUpgrade(self):

    defaultLabeling = '_NATURAL_ABUNDANCE'

    testComponentNames = [('CV:sample'), ('DTT:sample'), ('NaCl:sample'),
                   ('NaN3:sample'), ('Roche inhibitor cocktail:sample'),
                   ('TRIS:sample'), ('ZnSO4:sample'), ('benzamidine:sample')]

    project = self.project
    project.checkAllValid(complete=True)

    sampleStores = project.sortedSampleStores()
    self.assertTrue(len(sampleStores) == 1)
    self.assertEqual(sampleStores[0].name, '2x8n_str3_CCPN')
    samples = sampleStores[0].sortedSamples()
    self.assertListEqual([x.name for x in samples], ['sample_1_1', 'sample_2_1',])


    for sample in samples:
      ss = sample.name[-4:]
      componentNames =  [x + ss for x in testComponentNames]
      ll = sample.sortedSampleComponents()
      self.assertListEqual([x.labeling for x in ll], 8*[defaultLabeling])
      self.assertListEqual([x.name for x in ll], componentNames)

