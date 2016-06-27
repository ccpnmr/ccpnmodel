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
from ccpnmodel.ccpncore.memops.ApiError import ApiError



class UpgradeMolSystemTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = 'HaddockGUItest'

  def testMolsystemUpgrade(self):
    project = self.project

    dd = {}
    for molSystem in project.sortedMolSystems():
      dd[molSystem.code] = [x.code for x in molSystem.sortedChains()]

    for key, val in sorted(dd.items()):
      print ("('%s',%s)," % (key, val))

  def testHaddockUpgrade(self):
    project = self.project

    dd = {}

    for haddock in project.sortedHaddockProjects():
      for partner in haddock.sortedHaddockPartners():
        dd[partner.name] = (partner.molSystem.code,
                            [x.chain.code for x in partner.sortedChains()])

    for key, val in sorted(dd.items()):
      print ("('%s',%s)," % (key, val))


class UpgradeSamplesTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = '2x8n_str3_CCPN'

  def testSamplesUpgrade(self):
    project = self.project

    dd = {}
    for sample in project.sortedSamples():
      dd[sample.name] = [(x.name, x.labeling) for x in sample.sortedSamplecomponents()]

    for key, val in sorted(dd.items):
      print ("('%s',%s)," % (key, val))


