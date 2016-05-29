"""Module Documentation here

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (www.ccpn.ac.uk) 2014 - $Date$"
__credits__ = "Wayne Boucher, Rasmus H Fogh, Simon P Skinner, Geerten W Vuister"
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
"""Test code"""


import os
import unittest
import contextlib

from ccpn.util import Path
from ccpnmodel.ccpncore.lib.Io import Api as apiIo
from ccpn.util import Undo

TEST_PROJECTS_PATH = os.path.join(Path.getTopDirectory(), 'internal', 'data', 'testProjects')

class CoreTesting(unittest.TestCase):
  """Base class for all testing code that requires projects."""

  # Path for project to load - can be overridden in subclasses
  projectPath = None

  @contextlib.contextmanager
  def initialSetup(self):
    if self.projectPath is None:
      project = self.project = apiIo.newProject('default', overwriteExisting=True)
      self.nmrProject = project.newNmrProject(name='default')
    else:
      project = self.project = apiIo.loadProject(os.path.join(TEST_PROJECTS_PATH, self.projectPath))
      nmrProject = project.currentNmrProject
      if not nmrProject:
        nmrProject = project.currentNmrProject = project.findFirstNmrProject()
      self.nmrProject = nmrProject
    Undo.resetUndo(self.project, debug=True)
    self.undo = self.project._undo
    try:
      yield
    except:
      self.tearDown()
      raise

  def setUp(self):
    with self.initialSetup():
      pass


  def tearDown(self):

    self.project = None
    self.nmrProject = None
    self.undo = None