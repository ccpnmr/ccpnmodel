"""Pdb IO functions

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
__dateModified__ = "$dateModified: 2017-04-07 11:41:32 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

NaN = float('NaN')
from typing import List, Tuple
from ccpn.util import Common as commonUtil
from ccpnmodel.ccpncore.lib.Io import PyMMLibPDB as PdbLib

class PdbRecordProcessor(PdbLib.RecordProcessor):
  """Class for custom record processing"""

  def process_ATOM(self, rec):
    """fix atom record - make only globally acceptable changes, special-case stuff is for later"""

    name = rec.get('name')
    # If no name it cannot be fixed.
    if name[0].isdigit():
      # move leading digit to end of atom name
      rec['name'] = name[1:] + name[0]

    if not rec.get('chainID', '').strip():
      # replace empty chainID with seqID if length is suitable
      seqId = rec.get('seqID', '').strip()
      if len(seqId) == 1:
        rec['chainID'] = seqId
      else:
        # May not be necessary, but just in case
        rec['chainID'] = ' '


def readPdbRecorsds(fil):
  """Read file or input stream, and return of PDBRecords, one per model
  Header records are given in the first list"""

  pdbFile = PdbLib.PDBFile()
  pdbFile.load_file(fil)
  recordProcessor = PdbLib.RecordProcessor()
  recordProcessor.process_pdb_records(pdbFile)
  #
  return pdbFile


def readModelRecords(fil) -> Tuple[List[PdbLib.PDBRecord], List[List[PdbLib.PDBRecord]]]:
  """Read file or input stream, and return list-of-lists-of PDBRecords, one per model
  All records are given in the first list, subsequent lists contain only ATOM records"""

  pdbFile = readPdbRecorsds(fil)

  model = []
  header = []
  data = []
  for rec in pdbFile:
    if rec._name == 'ENDMDL':
      # put model into result and make a new one
      data.append(model)
      model = []
    elif rec._name in('ATOM  ', 'HETATM'):
      # Always append ATOM and HETATM records
      model.append(rec)
    elif not data:
      # For the first model only append all records, in case we want them later
      header.append(rec)
  #
  if model:
    # Special case: ENDMDL record missing
    # Only arrive here if we have had ATOM records since the last ENDMDL record (or beginning)
    data.append(model)
  #
  return header, data

def loadStructureEnsemble(molSystem:"MolSystem", fil) -> "StructureEnsemble":
  """Load PDB file into new structure ensemble matching MolSystem
  NB MolSystem is a required parameter for the data model,
  but there is no requirement that the data match"""

  # TBD further data extraction, use of header, match chains to existing one, make new chains?? ...

  header, data = readModelRecords(fil)

  if data:
    atomCount = len(data[0])
    modelCount = len(data)
    if any(x for x in data[1:] if len(x) != atomCount):
      raise ValueError("Multiple models have different atom counts in PDB file %s - loading aborted")


    # NBNB TBD check that names match in different models

    memopsRoot = molSystem.root
    ll = [x.ensembleId for x in molSystem.structureEnsembles]
    nextId = max(ll) + 1 if ll else 1
    apiEnsemble = memopsRoot.newStructureEnsemble(molSystem=molSystem, ensembleId=nextId)

    for rec in data[0]:
      chain = (apiEnsemble.findFirstCoordChain(code=rec.get('chainID')) or
               apiEnsemble.newChain(code=rec.get('chainID')))
      residue = (chain.findFirstResidue(seqCode=rec.get('resSeq'),
                                        seqInsertCode=rec.get('iCode', ' ')) or
                 chain.newResidue(seqCode=rec.get('resSeq'), seqInsertCode=rec.get('iCode', ' '),
                                  code3Letter=rec.get('resName')))

      # NBNB Heuristic. We need an elementName
      elementName = (rec.get('element') or commonUtil.name2ElementSymbol(rec.get('name'))
                     or 'Unknown')
      # NBNB wil likely break with altLocated atoms. Meanwhile do it right
      residue.newAtom(name=rec.get('name'), altLocationCode=rec.get('altLoc', ' '),
                      elementName=elementName.title())


    # Gather data
    # NBNB TBD atomNameData need doing
    for modelData in data:
      apiModel = apiEnsemble.newModel()
      coordinates = []
      addCoordinate = coordinates.append
      occupancies = []
      addOccupancy = occupancies.append
      bFactors = []
      addBFactor = bFactors.append
      # NBNB TBD Add atomNames array
      for rec in modelData:
        addCoordinate(rec.get('x', NaN))
        addCoordinate(rec.get('y', NaN))
        addCoordinate(rec.get('z', NaN))
        addCoordinate(rec.get('occupancy', NaN))
        addCoordinate(rec.get('tempFactor', NaN))
      apiModel.setSubmatrixData('coordinates', coordinates)
      apiModel.setSubmatrixData('occupancies', occupancies)
      apiModel.setSubmatrixData('bFactors', bFactors)

    # Set data
    # apiEnsemble.findFirstDataMatrix(name='coordinates', shape=(modelCount, atomCount,3), data=coordinates)
    # apiEnsemble.newDataMatrix(name='occupancies', shape=(modelCount, atomCount), data=occupancies)
    # apiEnsemble.newDataMatrix(name='bFactors', shape=(modelCount, atomCount), data=bFactors)

    #
    return apiEnsemble

  else:
    print("WARNING, no ATOM data in PDB file %s - loading aborted" % fil)





