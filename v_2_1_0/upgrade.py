"""
======================COPYRIGHT/LICENSE START==========================

upgrade.py: Data compatibility handling

Copyright (C) 2007-2014 Rasmus Fogh (CCPN project)

=======================================================================
# Licence, Reference and Credits

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

A copy of this license can be found in ../../../../license/LGPL.license.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

======================COPYRIGHT/LICENSE END============================

To obtain more information about this code:

- CCPN website (http://www.ccpn.ac.uk)

- contact Rasmus Fogh (ccpn@bioc.cam.ac.uk)

=======================================================================
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
__dateModified__ = "$dateModified: 2017-07-07 16:33:32 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: rhf22 $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

If you are using this software for academic purposes, we suggest
quoting the following reference:

===========================REFERENCE START=============================
Rasmus H. Fogh, Wayne Boucher, Wim F. Vranken, Anne
Pajon, Tim J. Stevens, T.N. Bhat, John Westbrook, John M.C. Ionides and
Ernest D. Laue (2005). A framework for scientific data modeling and
automated software development. Bioinformatics 21, 1678-1684.
===========================REFERENCE END===============================

"""

from ccpnmodel.ccpncore.lib import Conversion

versionSequence = ['2.0.a0', '2.0.a1', '2.0.a2', '2.0.a3', '2.0.b1', '2.0.b2', '2.0.b3',
                   '2.0.4',  '2.0.5',  '2.1.0',  '2.1.1']
# NBNB version 2.0.6 is a side branch, not on the main version sequence

emptyDict = {}
emptyList = []

# guids of elements that should be treated as old
# Must be kept out of map fixing till the last, as they break it.
elemsTreatedAsOld = set(('www.ccpn.ac.uk_Fogh_2009-04-16-16:24:04_00031',
                         'www.ccpn.ac.uk_Fogh_2009-04-16-16:24:03_00012'))

# pairs of element guids that should be treated as matching, e.g. when
# a single element must match with several elements in subclasses
elementPairings = []

def extraMapChanges(globalMapping):
  """ Extra map changes specific for a given step
  """

  for guid in (
               # set links to ExpPrototype package to delay, to allow resetting
               "www.ccpn.ac.uk_Fogh_2006-08-16-18:20:06_00008",
               "www.ccpn.ac.uk_Fogh_2006-08-16-18:23:00_00002",
               "www.ccpn.ac.uk_Fogh_2006-08-16-18:20:05_00025",
               ):
    globalMapping['mapsByGuid'][guid]['proc'] = 'delay'

  guid = 'www.ccpn.ac.uk_Fogh_2006-08-17-15:11:12_00001'
  dd = globalMapping['mapsByGuid'].get(guid)
  if dd and 'proc' in dd:
    del dd['proc']  # should not be 'proc':'delay' after all.



def correctData(topObj, delayDataDict, toNewObjDict, mapping=None):
  """ update topObj object tree using information in delayDataDict
  May be used either to postprocess a file load (minor upgrade)
  or as part of an in-memory data transfer (major upgrade)

  topObj is the package TopObject in the new tree
  toNewObjDict is _ID:newObj for minor
    and oldObj/oldObjId:newObj for major upgrades
  """

  pName = topObj.packageName

  if pName == 'ccp.molecule.MolStructure':
    # Fix MolStructure
    fixMolStructure(topObj, delayDataDict, toNewObjDict)

  #
  elif pName == 'ccp.nmr.Nmr':

    # Fix Nmr
    fixNmr(topObj, delayDataDict)


def fixMolStructure(topObj, delayDataDict, toNewObjDict):

  doGet = delayDataDict.get

  # make new Atoms if necessary, and make list of Atoms
  allAtoms = []
  for chain in doGet(topObj, emptyDict).get('coordChains', emptyList):
    for res in doGet(chain, emptyDict).get('residues', emptyList):
      for atom in doGet(res, emptyDict).get('atoms', emptyList):

        allAtoms.append(atom)

        coords= doGet(atom, emptyDict).get('coords', emptyList)
        if coords:

          # group coords by their altLocCode
          altLocs = {}
          for coord in coords:
            altLocCode = doGet(coord, emptyDict).get('altLocationCode',
                                                     emptyList)
            if altLocCode:
              altLocCode = altLocCode[0]
              ll = altLocs.get(altLocCode)
              if ll:
                ll.append(coord)
              else:
                altLocs[altLocCode] = [coord]

          del coords[:] # We want them removed before objects get created

          #
          if altLocs:
            altLocCodes = list(sorted(altLocs.keys()))
            atom.altLocationCode = altLocCodes[0]

            for altLocCode in altLocCodes[1:]:
              newAtom = res.newAtom(name=atom.name, altLocationCode=altLocCode,
                                    access = atom.access,
                                    applicationData = atom.applicationData)
              allAtoms.append(newAtom)
              ll = altLocs[altLocCode]
              for coord in ll:
                coord.__dict__['atom'] = newAtom

  # set up system - atoms
  topObj.orderedAtoms = allAtoms
  for ii, atom in enumerate(allAtoms):
    atom.index = ii

  # set up system - models
  models = doGet(topObj, emptyDict).get('models', emptyList)
  nModels = len(models)
  if nModels:
    # NB this is called also on partial load,
    # where there are no models and nothing should be done

    ll = [(x.serial,x) for x in models]
    ll.sort()
    models = [x[1] for x in ll]
    for ii,model in enumerate(models):
      model.index = ii

    # set up system - data matrices
    # NB must set entry in parent __dict__ as this is done while reading
    nAtoms = len(allAtoms)
    xx = topObj.newDataMatrix(name='bFactors', shape=(nModels,nAtoms))
    topObj.__dict__['dataMatrices']['bFactors'] = xx
    xx = topObj.newDataMatrix(name='occupancies', shape=(nModels,nAtoms))
    topObj.__dict__['dataMatrices']['occupancies'] = xx
    xx = topObj.newDataMatrix(name='coordinates', shape=(nModels,nAtoms,3))
    topObj.__dict__['dataMatrices']['coordinates'] = xx

    # set data
    for model in models:

      occupancies = [1.0] * nAtoms
      bFactors = [0.0] * nAtoms
      coordinates = bFactors * 3

      setBFactors = False
      setOccupancies = False
      coordIds = delayDataDict[model].get('coords', emptyList)

      #coords = [toNewObjDict.get(x) for x in coordIds]

      nfound = 0
      for coordId in coordIds:
        coord = toNewObjDict.pop(coordId)    # Want them gone before final check
        coordDict = delayDataDict.pop(coord) # Want them gone before final check
        index = coord.atom.index

        ll = coordDict.get('occupancy')
        if ll:
          setOccupancies = True
          occupancies[index] = ll[0]

        ll = coordDict.get('bFactor')
        if ll:
          setBFactors = True
          bFactors[index] = ll[0]

        for ii,tag in enumerate(('x','y','z')):
          ll = coordDict.get(tag)
          if ll:
            nfound += 1
            coordinates[3*index + ii] = ll[0]

      model.setSubmatrixData('coordinates', coordinates)
      if setOccupancies:
        model.setSubmatrixData('occupancies', occupancies)
      if setBFactors:
        model.setSubmatrixData('bFactors', bFactors)
    #
    topObj.purge()



def fixNmr(topObj, delayDataDict):
  """
  """

  doGet = delayDataDict.get

  memopsRoot = topObj.parent
  topObjByGuid = memopsRoot.__dict__.get('topObjects')

  # remap defunct RefExperiment
  for xpr in doGet(topObj, emptyDict).get('experiments', emptyList):

    expDict = doGet(xpr, emptyDict)

    # fix NmrExpPrototype mapping for defunct types
    Conversion.setNmrExpPrototypeLink(xpr, 'refExperiment', topObjByGuid, delayDataDict,
                                      remapPrototypeLink)
    for xd in expDict.get('expDims', emptyList):

      Conversion.setNmrExpPrototypeLink(xd, 'refExpDim', topObjByGuid, delayDataDict,
                                        remapPrototypeLink)
      for xdr in doGet(xd, emptyDict).get('expDimRefs', emptyList):

        Conversion.setNmrExpPrototypeLink(xdr, 'refExpDimRef', topObjByGuid, delayDataDict,
                                          remapPrototypeLink)


def remapPrototypeLink(keyList):

  guid = keyList[0]

  # map to different keys
  if guid == "ccpn_rhf22_2009-04-02-16-03-22-040_00001":
    # Remap {CA|Cca}CONH 143 to H{CA|Cca}CONH 59
    keyList[0] = "cam_wb104_2008-01-15-16-06-40_00025"
    refExpMap = {1:38, 2:5, 3:39, 8:8, 24:24, }
    keyList[1] = refExpMap[keyList[1]]

  elif guid == "ccpn_rhf22_2009-04-02-15-29-19-145_00001":
    # Remap {CA|Cca}NH (142) to H{CA|Cca}NH (70)
    keyList[0] = "cam_wb104_2008-01-15-16-06-40_00036"
    # RefExpMap is identity, just keep them
    #keyList[1] = refExpMap[keyList[1]]

  elif guid == "ccpn_rhf22_2009-04-03-14-39-42-994_00001":
    # Remap 152 CA[N] to 243 HCA[N]
    keyList[0] = "ccpn_rhf22_2009-04-24-16-19-16-187_00001"
    refExpMap = {1:2}
    keyList[1] = refExpMap[keyList[1]]

  elif guid == "ccpn_rhf22_2009-04-02-16-10-54-048_00001":
    # Remap 144 C_cCONH.relayed to 281 HNCO_C.relayed
    # NB refExp 15 (projection) is not mapped. It is assumed it was never used.
    keyList[0] = "Expts_vicky_2010-12-15-16-02-18-326_00001"
    refExpMap = {1:7, 3:8, 6:9, 17:10}
    keyList[1] = refExpMap[keyList[1]]
