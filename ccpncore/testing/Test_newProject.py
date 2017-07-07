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
__author__ = "$Author: CCPN $"
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:47 +0100 (Fri, April 07, 2017) $"
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

from ccpnmodel.ccpncore.lib.Io import Api as apiIo

# Put project inside this directory
projectPath = './local.'
projectName = 'test'

#
# Import the Molecule and MolSystem packages

#
# Python standard stuff
#

def doTest():

  project = newProject()
  project.saveModified()
  del project

  project2 = apiIo.loadProject(path=projectPath, projectName=projectName)
  successful = apiIo.saveProject(project2, newPath=projectPath+'_out')
  if not successful:
    raise ValueError("Project save was not successful")



def newProject():

  project = apiIo.newProject(projectName, overwriteExisting=True)

  # Make molecule using API

  molecule1 =  project.newMolecule(name='molecule1')
  #

  exampleSequence = ['Ala','Gly','Tyr','Glu','Leu','Gly','Ser','His','Ile']

  for seqPosition, ccpCode in enumerate(exampleSequence):

    chemComp = project.findFirstChemComp(molType='protein', ccpCode=ccpCode)

    if seqPosition == 0:
      linking = 'start'
    elif seqPosition == len(exampleSequence) - 1:
      linking = 'end'
    else:
      linking = 'middle'

    chemCompVar = chemComp.findFirstChemCompVar(linking=linking, isDefaultVar=True)

    molRes = molecule1.newMolResidue(chemComp=chemComp,seqCode=seqPosition+5,
                                    chemCompVar=chemCompVar)

    if linking != 'start':
      prevLink = molRes.findFirstMolResLinkEnd(linkCode = 'prev')
      prevMolRes = molecule1.sortedMolResidues()[-1]
      if prevLink and prevMolRes:
        nextLink = prevMolRes.findFirstMolResLinkEnd(linkCode = 'next')
        if nextLink:
          molecule1.newMolResLink(molResLinkEnds=(nextLink,prevLink))


  molSystem = project.newMolSystem(code='MS1', name = 'MolSystem1')

  #
  # Now create a homodimer - two chains referring to the same Molecule
  #

  molSystem.newChain(molSystem,code='A', molecule=molecule1)
  molSystem.newChain(molSystem,code='B', molecule=molecule1)


  project.checkAllValid(complete=True)

  #
  # Write out the project.
  #

  project.saveModified()

  #
  return project

if __name__ == '__main__':
    doTest()
