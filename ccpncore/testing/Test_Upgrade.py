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
__dateModified__ = "$dateModified: 2017-07-07 16:33:25 +0100 (Fri, July 07, 2017) $"
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

