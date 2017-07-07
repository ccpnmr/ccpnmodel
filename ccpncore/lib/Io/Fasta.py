"""Code for reading Fasta format files

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:13 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================


def parseFastaFile(inputFile):
  """Parse  Fasta file and return sequences"""

  sequences = []
  with open(inputFile, 'r') as f:
    chains = []
    lines = [line.strip() for line in f.readlines() if line.strip()]
    for line in lines:
      if line and line[0] == '>':
        chains.append(lines.index(line))
  for chain in chains :
    name = lines[chain][1:].lstrip().split()[0] # the [1:] to eliminate the '>'
    index = chains.index(chain)
    if not index == len(chains)-1:
      endIndex = chains[index+1]
      sequences.append([name, ''.join(lines[chain+1:endIndex])])
    else:
      sequences.append([name, ''.join(lines[chain+1:])])

  return sequences
