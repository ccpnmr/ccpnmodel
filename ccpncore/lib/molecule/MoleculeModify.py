"""API (data storage) level functionality for creating and modifying molecules

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:14 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b5 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
"""Code for generating and modifying Molecules and MolSystems"""

import typing
from ccpn.util.nef import StarIo
from ccpn.util import Common as commonUtil
from ccpnmodel.ccpncore.memops.ApiError import ApiError
from ccpnmodel.ccpncore.lib.chemComp import Io as chemCompIo
from ccpnmodel.ccpncore.lib.molecule import MoleculeQuery


###from ccp.general.Io import getChemComp

#################################################################
#
# Molecule creation
#
##################################################################

def createMolecule(project, sequence:(list,str), molType:str='protein', name:str="Molecule",
                 startNumber:int=1, isCyclic=False):

  """Descrn: Makes Molecule for a given sequence

     Inputs: Project,List of Words (ChemComp.CcpCode), Word (ChemComp.molType), 
     String ( Ccp.Molecule.Molecule.name) Int (first MolResidue.seqCode)

     Output: Molecule
  """

  # ensure name is unique
  i = 0
  ss = name
  while project.findFirstMolecule(name=ss):
    i += 1
    ss = '%s%d' % (name,i)
  if ss != name:
    project._logger.warning(
    "CCPN molecule named %s already exists. New molecule has been named %s" %
    (name,ss))
  name = ss
 
  molecule =  project.newMolecule(name=name)

  try:
    if isinstance(sequence, str):
      molecule.extendOneLetterMolResidues(sequence, molType, startNumber, isCyclic)
    else:
      molecule.extendMolResidues(sequence, startNumber, isCyclic)
  except Exception as e:
    try:
      molecule.delete()
    except:
      pass
    raise e

  return molecule

  
  
def _getLinearChemCompData(project, molType, ccpCode, linking):
  """Descrn: Implementation function, specific for addLinearSequence()
     Inputs: Project object, and desired molType, ccpCode, linking (all strings)
     Output: (dd,ll) tuple where dd is a dictionary for passing to the 
              MolResidue creation (as **dd), and ll is a list of the linkCodes
              that are different from 'next' and 'prev'
  """
  
  seqLinks = []
  otherLinkCodes = []
  
  chemComp = project.findFirstChemComp(molType=molType, ccpCode=ccpCode)
  
  isOther = False
  if chemComp is None:
    isOther = True
    chemComp = project.findFirstChemComp(molType='other', ccpCode=ccpCode)

  if chemComp is None:
    chemComp = chemCompIo.fetchChemComp(project, molType, ccpCode)

  if chemComp is None:
    raise ApiError("No chemComp for %s residue %s" % (molType, ccpCode))
    
  chemCompVar = chemComp.findFirstChemCompVar(linking=linking, isDefaultVar=True) or \
                chemComp.findFirstChemCompVar(linking=linking)
  # Note requiring a default var is too strict - not always set for
  # imports from mol2/PDB etc

  if isOther and (chemCompVar is None):
    if linking == 'start':
      linkEnd = chemComp.findFirstLinkEnd(linkCode='next')
     
    elif linking == 'end':
      linkEnd = chemComp.findFirstLinkEnd(linkCode='prev')
    
    else:
      linkEnd = None
      
    if linkEnd:
      otherLinkCodes.append(linkEnd.linkCode)
      chemCompVar = chemComp.findFirstChemCompVar(isDefaultVar=True) or \
                    chemComp.findFirstChemCompVar()            
                
  if chemCompVar is None:
    raise ApiError("No ChemCompVar found for %s:%s linking %s" % (molType, ccpCode, linking))
  
  molResData = {'chemComp':chemComp, 'linking':chemCompVar.linking,
                'descriptor':chemCompVar.descriptor}
  
  for linkEnd in chemCompVar.linkEnds:
    code = linkEnd.linkCode
    
    if code in ('next','prev'):
      seqLinks.append(code)
    else:
      otherLinkCodes.append(code)
  
  if linking == 'start':
    if seqLinks and seqLinks != ['next']:
      raise ApiError("Linking 'start' must have just 'next' linkEnd")
      
  elif linking == 'end':
    if seqLinks and seqLinks != ['prev']:
      raise ApiError("Linking 'end' must have just 'prev' linkEnd ")
      
  elif linking != 'middle' or seqLinks not in (['next','prev'],['prev','next']):
    raise ApiError("Illegal linking %s with seqLinks %s" % (linking,seqLinks))
  
  return molResData, otherLinkCodes

def createMoleculeFromNef(project, name:str, sequence:typing.Sequence[dict],
                          defaultType:str='UNK') -> 'Molecule':
  """Create a Molecule from a sequence of NEF row dictionaries (or equivalent)"""

  residueName2chemCompId = MoleculeQuery.fetchStdResNameMap(project)

  stretches = StarIo.splitNefSequence(sequence)
  molecule =  project.newMolecule(name=name)

  for stretch in stretches:

    # Try setting start number
    sequenceCode = stretch[0]['sequence_code']
    seqCode, seqInsertCode,offset = commonUtil.parseSequenceCode(sequenceCode)
    if seqCode is None:
      startNumber = 1
    else:
      startNumber = seqCode

    # Create new MolResidues
    residueTypes = [row.get('residue_name', defaultType) for row in stretch]
    firstLinking = stretch[0].get('linking')
    if len(residueTypes) > 1:
      lastLinking = stretch[-1].get('linking')
      if (firstLinking in ('start', 'single', 'nonlinear', 'dummy') or
          lastLinking == 'end'):
        isCyclic = False
      else:
        # We use isCyclic to set the ends to 'middle'. It gets sorted out below
        isCyclic = True

      molResidues = molecule.extendMolResidues(sequence=residueTypes, startNumber=startNumber,
                                               isCyclic=isCyclic)

      # Adjust linking and descriptor
      if isCyclic:
        if firstLinking != 'cyclic' or lastLinking != 'cyclic':
          # not cyclic after all - remove cyclising link
          cyclicLink = molResidues[-1].findFirstMolResLinkEnd(linkCode='next').molResLink
          cyclicLink.delete()
      else:
        if firstLinking != 'start':
          ff = molResidues[0].chemComp.findFirstChemCompVar
          chemCompVar = (ff(linking='middle', isDefaultVar=True) or ff(linking='middle'))
          molResidues[0].__dict__['linking'] = 'middle'
          molResidues[0].__dict__['descriptor'] = chemCompVar.descriptor
        if lastLinking != 'end':
          ff = molResidues[-1].chemComp.findFirstChemCompVar
          chemCompVar = (ff(linking='middle', isDefaultVar=True) or ff(linking='middle'))
          molResidues[-1].__dict__['linking'] = 'middle'
          molResidues[-1].__dict__['descriptor'] = chemCompVar.descriptor
    else:
      # Only one residue
      residueType = residueTypes[0]
      if residueType.startswith('dummy.'):
        tt = ('dummy',residueType[6:])
      else:
        tt = residueName2chemCompId.get(residueTypes[0])
      if not tt:
        project._logger.warning("""Could not access ChemComp for %s - replacing with %s
NB - could be a failure in fetching remote information.
Are you off line?""" % (residueTypes[0], defaultType))
        tt = residueName2chemCompId.get(defaultType)
      if tt:
        chemComp = chemCompIo.fetchChemComp(project, tt[0], tt[1])
        if chemComp:
          chemCompVar  = (chemComp.findFirstChemCompVar(linking='none') or
                          chemComp.findFirstChemCompVar()) # just a default
          molResidues = [molecule.newMolResidue(seqCode=startNumber, chemCompVar=chemCompVar)]

        else:
          raise ValueError("Residue type %s %s: Error in getting template information"
                           % (residueTypes[0], tt))

      else:
        raise ValueError("Residue type %s not recognised" % residueTypes[0])

    startNumber += len(residueTypes)
  #
  return molecule

