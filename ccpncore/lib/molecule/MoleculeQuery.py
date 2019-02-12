"""API (data storage) level functionality for querying molecules

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
"""Code for querying Molecules and MolSystems"""

from ccpnmodel.ccpncore.lib.chemComp import ChemCompOverview
from ccpnmodel.ccpncore.lib.chemComp import ObsoleteChemComps
from ccpnmodel.ccpncore.lib.chemComp import Io as chemCompIo
import urllib

molTypeOrder = ('protein', 'DNA', 'RNA', 'carbohydrate', 'other')

LINEAR_POLYMER_TYPES = ('protein', 'DNA', 'RNA')


# CifCode map - preset to ensure it is not overridden by obsolete ChemComps in list
cifCodeRemap = {}
# # Std DNA - keep one-letter ccpCode
cifCodeRemap['DA'] = cifCodeRemap['Da'] = ('DNA', 'Da')
cifCodeRemap['DC'] = cifCodeRemap['Dc'] = ('DNA', 'Dc')
cifCodeRemap['DG'] = cifCodeRemap['Dg'] = ('DNA', 'Dg')
cifCodeRemap['DI'] = cifCodeRemap['Di'] = ('DNA', 'Di')
cifCodeRemap['DU'] = cifCodeRemap['Du'] = ('DNA', 'Du')
cifCodeRemap['DT'] = cifCodeRemap['Dt'] = ('DNA', 'Dt')

# # Std RNA - keep one-letter ccpCode
cifCodeRemap['5MU'] = cifCodeRemap['5mu'] = cifCodeRemap['RT'] =  cifCodeRemap['Rt'] = ('RNA','5mu')
#
# Set as RNA or other, to override DNA with similar name
for tag in ('2at', '2bt', '2gt', '2nt', '2ot', '3me', 'Ap7', 'Atl', 'Boe', 'Car',
            'Eit', 'Fnu', 'Gmu', 'Lcc', 'Lcg', 'P2t', 'S2m', 'T2t', 'Tfe', 'Tln'):
  cifCodeRemap[tag] = cifCodeRemap[tag.upper()] = ['RNA', tag]

cifCodeRemap['Hob'] = cifCodeRemap['HOB'] = ('other', 'Hob')
cifCodeRemap['Xxx'] = cifCodeRemap['XXX'] = ('other', 'Xxx')

# ccpCode remaps - for upgrade convresion of 'inventive' ChemComps
ccpCodeRemap = {
  'DNA':{
    'Xxx':('DNA','Dn'),
    'A00':('DNA','Da'),
    'A11':('DNA','Da'),
    'C00':('DNA','Dc'),
    'C11':('DNA','Dc'),
    'G00':('DNA','Dg'),
    'G11':('DNA','Dg'),
    'I00':('DNA','Di'),
    'I11':('DNA','Di'),
    'U00':('DNA','Du'),
    'U11':('DNA','Du'),
  },
  'protein':{
    'Xxx':('protein','Unk'),
  },
  'RNA':{
    'Xxx':('RNA','N'),
    'A00':('RNA','A'),
    'A11':('RNA','A'),
    'C00':('RNA','C'),
    'C11':('RNA','C'),
    'G00':('RNA','G'),
    'G11':('RNA','G'),
    'I00':('RNA','I'),
    'I11':('RNA','I'),
    'U00':('RNA','U'),
    'U11':('RNA','U'),
  },
  'other':{
    'Acy':('other','Ace'),
    'Nh3':('other','Nh2'),
    'A01_dna':('DNA','Da'),
    'C01_dna':('DNA','Dc'),
    'G01_dna':('DNA','Dg'),
    'I01_dna':('DNA','Di'),
    'T01_dna':('DNA','Dt'),
    'U01_dna':('DNA','Du'),
    'A01_rna':('RNA','A'),
    'C01_rna':('RNA','C'),
    'G01_rna':('RNA','G'),
    'I01_rna':('RNA','I'),
    'T01_rna':('RNA','T'),
    'U01_rna':('RNA','U'),
  },
}


def fetchStdResNameMap(project:'MemopsRoot', reset:bool=False, debug:bool=False):
  """ fetch dict of {residueName:(molType,ccpCode)},
  using cached value if present and not reset.

  NBNB TBD Add naming variants from ChemComp naming systems
  """

  chemCompOverview = ChemCompOverview.chemCompOverview
  obsoleteChemComps = ObsoleteChemComps.obsoleteChemCompData

  logger = project._logger

  if hasattr(project, '_residueName2chemCompId') and not reset:
    return project._residueName2chemCompId
  else:
    result = project._residueName2chemCompId = {}
    rejected = {}
    result.update(cifCodeRemap)

  remapped = {}
  nFound = 0
  for molType in molTypeOrder:

    # Add data for all chemComps from overview
    for ccpCode,tt in reversed(sorted(chemCompOverview[molType].items())):
      nFound += 1
      # NB done in reversed order to ensure Xyz takes precedence over XYZ
      cifCode = tt[1]
      dd = obsoleteChemComps.get(cifCode)

      if dd:
        altCode = dd['cifCode']
        if altCode is None:
         rejected[molType, ccpCode] = None

        else:
          # Remaps are handled in another loop
          remapped[(molType, ccpCode)] = (cifCode, altCode)
      else:

        # Dummy value to allow shared diagnostics printout
        val = ('-', '-')

        if not cifCode:
          # no cifCode - skip. debug message
          rejected[molType, ccpCode] = cifCode
          ccId = ccpCodeRemap.get(molType, {}).get(ccpCode)
          if ccId:
            val = ccId
            message = 'CIF-CCP-REMAP'
          else:
            message = 'CIF-NO'

        elif cifCode != cifCode.upper():
          # cifCode is not upperCase - skip. debug message
          message = 'CIF-LOW'
          rejected[molType, ccpCode] = cifCode
        else:
          locif = cifCode[0] + cifCode[1:].lower()
          val = result.get(cifCode) or result.get(locif)
          if val is None:
            # New value. Set the map
            val = result[cifCode] = result[locif] =(molType, ccpCode)
            message = 'CIF-OK'

          else:
            # Value was already set

            if val[0] == molType and val[1] == ccpCode:
              # This one was set up front
              message = 'CIF-PRESET'

            elif val[1] == cifCode and val[1] != locif:
              # ccpCode was UPPER-CASE
              # replace UPPERCASE ccpCode with mixed-case
              if molType == val[0]:
                result[cifCode] = result[locif] = (molType, ccpCode)
                rejected[val[0], val[1]] = cifCode

                # Debug messages:
                if ccpCode.upper() == val[1].upper():
                  message = 'CIF-REPL-INTRA'
                else:
                  message = 'CIF-REPL-CLASH1'

              elif molType == 'other' and val[0] != 'other':
                message = 'CIF-CLASH-OTHER'
                rejected[molType, ccpCode] = cifCode

              else:
                message = 'CIF-REPL-CLASH2'
                rejected[molType, ccpCode] = cifCode

            else:
              # Simple cifCode clash. Ignore and set debug messages
              if molType == val[0]:
                if ccpCode.upper() == val[1].upper():
                  message = 'CIF-INTRA'
                else:
                  message = 'CIF-CLASH1'
              elif molType == 'other' and val[0] != 'other':
                message = 'CIF-OTHER'
              else:
                message = 'CIF-CLASH2'
              rejected[molType, ccpCode] = cifCode

        #   # Print out debug messages
        # print("\t".join((message, molType, ccpCode, val[0], val[1],
        #                  tt[0] or '-', tt[1] or '-', tt[2] or '-')))
        #
        # if len(ccpCode) == 5 and ccpCode.startswith('D-'):
        #   # D- amino acid - special case.
        #   # for now add ccpCode as extra alias
        #   print("\t".join(('CCP-D-Xyz', molType, ccpCode,val[0], val[1],
        #                    tt[0] or '-', tt[1] or '-', tt[2] or '-')))
          # result[ccpCode] = val


  # print("CIF-nFound %s" % nFound)

  for ccId, codes in sorted(remapped.items()):
    cifCode, altCode = codes
    val = result.get(altCode)
    if val is None:
      pass
      # print('\t'.join(("CIF-REMAP-ERROR1", ccId[0], ccId[1], cifCode, altCode)))
    else:
      locif = cifCode[0] + cifCode[1:].lower()
      result[cifCode] = result[locif] = val
      # print('\t'.join(("CIF-REMAP-OK", ccId[0], ccId[1], cifCode, altCode, val[0], val[1])))
    rejected[ccId] = cifCode


  if debug:
    # for tt, cifCode in sorted(rejected.items()):
    #   print("  %s:%s,  # REJECTED" % (repr(tt), repr(cifCode)))

    # Check for upper-case ccpCodes remaining
    # for tag,val in sorted(result.items()):
      # if val[1][1:] !=  val[1][1:].lower():
      #   print("CCP-UPPER\t%s\t%s\t%s" % (val[0], val[1], tag))

    # check for unused ChemComps
    for chemComp in project.sortedChemComps():
      cifCode = chemComp.code3Letter
      ccpCode = chemComp.ccpCode
      molType = chemComp.molType
      val = result.get(ccpCode)
      ccId = (chemComp.molType, ccpCode)

      # Debug output checking ccpCode
      message = None
      if not val:
        val = (chemComp.code1Letter, cifCode)
        message = "CHEM-MISS"
      elif molType != val[0]:
        message = "CHEM-TYPE-CLASH"
      elif ccpCode != val[1]:
        message = "CHEM-CODE-CLASH"
      else:
        message = "CHEM-OK"

      # if message is not None:
      #   print ("\t".join(str(x) for x in (message, molType, ccpCode, val[0], val[1], cifCode)))

      # Debug output checking ccpCode
      val = result.get(cifCode)
      message = None
      if not val:
        val = (chemComp.code1Letter, cifCode)
        message = "CCIF-MISS"
      elif molType != val[0]:
        message = "CCIF-TYPE-CLASH"
      elif ccpCode != val[1]:
        message = "CCIF-CODE-CLASH"
      else:
        message = "CCIF-OK"

      # if message is not None:
      #   print ("\t".join(str(x) for x in (message, molType, ccpCode, val[0], val[1], cifCode)))


    tags = set()
    # get sysNames
    for namingSystem in chemComp.namingSystems:
      for sysName in namingSystem.chemCompSysNames:
        tags.add(sysName.sysName)

    # set additional synonyms
    for tag in tags:
      prevId = result.get(tag)

      if prevId is None:

        if len(tag) == 1:
          pass
         # print ("CINFO8\tRejecting one-letter synonym\t%s from ChemComp %s:%s"
         #         % (tag, cifCode, val))

        elif ccId == val:
          # print ("CINFO9\tAdding new ccpCode synonym\t%s from ChemComp %s:%s"
          #        % (tag, cifCode, ccId))

          result[tag] = val
        #
        # else:
        #   print ("CWARNING\tclash1\tfor %s chemComp %s v. cifCode %s:%s"
        #         % (tag, ccId, cifCode,  val))

      # elif prevId != val:
      #   print ("CWARNING\tclash2\tfor %s chemComp %s, %s v. cifCode %s:%s"
      #         % (tag, ccId, prevId, cifCode,  val))


  #
  return result


if __name__ == '__main__':
  from ccpnmodel.ccpncore.lib.Io import Api as apiIo
  project = apiIo.newProject('ChemCompNameTest')
  # printCcpCodeStats(project)
  dd = fetchStdResNameMap(project, reset=True, debug=True)
  for key,val in sorted(dd.items()):
    print ("  '%s':('%s','%s')," % (key, val[0], val[1]))
  # import json
  # data = _parseObsoleteChemCompTable(open('/home/rhf22/rhf22/Dropbox/RHFnotes/ChemComp/ResidueNameMap3.txt'))
  # print(json.dumps(data, sort_keys=True, indent=4))


    #from NEF molecule creation

