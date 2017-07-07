"""Module Documentation here

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
__dateModified__ = "$dateModified: 2017-04-07 11:41:47 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
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
