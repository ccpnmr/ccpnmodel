"""Definition of program-level constants

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:09 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b4 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from collections import OrderedDict

# Default NmrChain code
defaultNmrChainCode = '@-'
defaultNmrResidueCode = '@'

# Constraint list constraintType to itemLength map
# NB these data determine which constraintListTypes are legal.
# To add new ones, just add them here.
#
# NBNB TBD we should constrain origin and measurementType depending on the constraintListType
constraintListType2ItemLength = OrderedDict([
        ('Distance', 2),
        ('Dihedral', 4),
        ('Rdc', 2),
        ('JCoupling', 2),
        ('ChemicalShift',1),
        ('Csa', 1),
        ('T1', 1),
        ('T2',1),
        ('T1rho', 1),
        ('pKa', 1),
])


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

