"""Definition of program-level constants

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

import re

# CCPNMR data-transfer json mimetype
ccpnmrJsonData = 'ccpnmr-json'

# Timestamp formats
stdTimeFormat = "%Y-%m-%d %%H:M:%S.%f"
isoTimeFormat = "%Y-%m-%dT%%H:M:%S.%f"

# Default NmrChain code
defaultNmrChainCode = '@-'

# Constraint list constraintType to itemLength map
# NB these data determine which constraintListTypes are legal.
# To add new ones, just add them here.
#
# NBNB TBD we should constrain origin and measurementType depending on the constraintListType
constraintListType2ItemLength = {
  'Csa':1,
  'T1':1,
  'T2':1,
  'T1rho':1,
  'pKa':1,
  'ChemicalShift':1,
  'Distance':2,
  'Rdc':2,
  'JCoupling':2,
  'Dihedral':4,
}

# sequenceCode parsing expression
# A sequenceCOde is combined (without whitespace) of:
#   an optional integer
#   an optional text field, as short as possible
#   an optional field of the form +ii of -ii, where ii is an integer
#
# The expression below has one error:
# a string of the form '+12' is parsed as (None, '', '+12'}
# whereas it should be interpreted as (None, '+12', None), but that cannot be helped
sequenceCodePattern = re.compile('(\-?\d+)?(.*?)(\+\d+|\-\d+)?$')


#
# Standard residue codes
#

standardResidueCcpCodes = {

    'protein':

      ('Ala','Arg','Asn','Asp','Cys',
       'Gln','Glu','Gly','His','Ile',
       'Leu','Lys','Met','Phe','Pro',
       'Ser','Thr','Trp','Tyr','Val'),

    'DNA':

      ('A','C','G','T'),

    'RNA':

      ('A','C','G','U')

                          }

code1LetterToCcpCodeDict = {

  'protein': {
     
     'A': 'Ala',
     'C': 'Cys',
     'D': 'Asp',
     'E': 'Glu',
     'F': 'Phe',
     'G': 'Gly',
     'H': 'His',
     'I': 'Ile',
     'K': 'Lys',
     'L': 'Leu',
     'M': 'Met',
     'N': 'Asn',
     'P': 'Pro',
     'Q': 'Gln',
     'R': 'Arg',
     'S': 'Ser',
     'T': 'Thr',
     'V': 'Val',
     'W': 'Trp',
     'Y': 'Tyr'
     
             },
             
  'DNA': {
     
     'A': 'A',
     'C': 'C',
     'G': 'G',
     'T': 'T',
     'I': 'I',
     'U': 'U',
     
          },
             
  'RNA': {
     
     'A': 'A',
     'C': 'C',
     'G': 'G',
     'T': 'T',
     'I': 'I',
     'U': 'U',
     
          }

    }

ccpCodeToCode1LetterDict = {

  'protein': {}, # set up below
  'DNA': code1LetterToCcpCodeDict['DNA'].copy(),
  'RNA': code1LetterToCcpCodeDict['RNA'].copy()
}

dict1 = code1LetterToCcpCodeDict['protein']
dict2 = ccpCodeToCode1LetterDict['protein']
for key in list(dict1.keys()):
  dict2[dict1[key]] = key

