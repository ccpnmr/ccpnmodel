"""Functions for insertion into ccp.nmr.Nmr.Peak

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:11 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from typing import Sequence

def assignByDimensions(self:'Peak', value:Sequence[Sequence['Resonance']]):
  """Set per-dimension assignments on peak.
  value is a list of lists (one per dimension) of resonances.
  NB only works for single-PeakContrib, one-ref-per-dimension assignments
  NB resets PeakContribs
  """
  numDim =  self.peakList.dataSource.numDim
  if len(value) != numDim:
    raise ValueError("Assignment length does not match number of peak dimensions %s: %s"
                      % (numDim, value))

  for ii, val in enumerate(value):
    if len(set(val)) != len(val):
      raise ValueError("Assignments contain duplicates in dimension %s: %s" % (ii+1, val))

  peakContribs = self.sortedPeakContribs()
  if peakContribs:
    # Clear existing assignments, keeping first peakContrib
    peakContrib = peakContribs[0]
    for xx in peakContribs[1:]:
      xx.delete()
    for peakDim in self.peakDims:
      for peakDimContrib in peakDim.peakDimContribs:
        peakDimContrib.delete()

  else:
    # No assignments. Make peakContrib
    peakContrib = self.newPeakContrib()

  peakDims = self.sortedPeakDims()
  for ii,val in enumerate(value):
    peakDim = peakDims[ii]
    for resonance in val:
      peakDim.newPeakDimContrib(resonance=resonance, peakContribs=(peakContrib,))


def assignByContributions(self:'Peak', value:Sequence[Sequence['Resonance']]):
  """Set assignments on peak.
  value is a list of lists (one per combination) of resonances.
  NB only works for single-resonance, one-ref-per-dimension assignments
  NB sets one PeakContrib per combination
  """

  peakDims = self.sortedPeakDims()
  dimensionCount = len(peakDims)
  dimResonances = []
  for ii in range(dimensionCount):
    dimResonances.append([])

  # get per-dimension resonances
  for tt in value:
    for ii,resonance in enumerate(tt):
      if resonance is not None and resonance not in dimResonances[ii]:
        dimResonances[ii].append(resonance)

  # reassign dimension resonances
  assignByDimensions(self, dimResonances)

  # Get first PeakContrib before we add new ones
  firstPeakContrib = self.findFirstPeakContrib()

  if value:
    # set PeakContribs, one per assignment tuple, skipping the first one
    for tt in value[1:]:
      ll = [peakDim.findFirstPeakDimContrib(resonance=tt[ii])
            for ii,peakDim in enumerate(peakDims)]
      self.newPeakContrib(peakDimContribs=[x for x in ll if x is not None])

    # reset PeakDimContribs for first PeakContrib
    ll = [peakDim.findFirstPeakDimContrib(resonance=value[0][ii])
          for ii,peakDim in enumerate(peakDims)]
    firstPeakContrib.peakDimContribs = [x for x in ll if x is not None]


# NBNB unit operations needed:
#
# clearAssignments
# _setToPerDimension
# _setToPerAssignment
# addAssignment
# assignDimension
