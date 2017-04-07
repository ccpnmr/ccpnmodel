"""Functions for insertion into ccp.nmr.Nmr.Shift

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
__modifiedBy__ = "$modifiedBy: Ed Brooksbank $"
__dateModified__ = "$dateModified: 2017-04-07 11:41:36 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import math
# from ccpnmodel.ccpncore.api.ccp.nmr.import Nmr



def recalculateValue(self:'Shift', simulatedPeakScale:float=0.0001) -> float:
  """
  Calculates the value and error for a given shift based upon the
  peaks to which its resonance is assigned. Also sets links to
  appropriate peaks and peak dims. Optional float to scale simulated
  peak contributions (normally so that they have much less influence)

  .. describe:: Input
  
  Nmr.Shift, Float
  
  .. describe:: Output
  
  Float (shift.value)
  """

  # NBNB TBD spectrum dimensions weighting must be added
  # hasApp = hasattr(shift.root, 'application')


  if self.isDeleted:
    return

  shiftList = self.parentList

  if not shiftList.autoUpdate:
    return

  experiments = shiftList.experiments
  resonance = self.resonance
  sum1  = 0.0
  sum2  = 0.0
  N     = 0.0
  peakDims = []
  peaks = set([])

  for contrib in resonance.peakDimContribs:

    if contrib.isDeleted:
      # Function may be called during PeakDimContrib deletion
      continue

    peakDim = contrib.peakDim
    peak = peakDim.peak
    
    if peak.isDeleted or peakDim.isDeleted or peak.figOfMerit == 0.0:
      continue
      
    peakList = peak.peakList
    experiment = peakList.dataSource.experiment
    if experiment not in experiments:
      continue
    
    # NBNB TBD peak splittings are not yet handled in V3. TBD add them
    # component = contrib.peakDimComponent
    # if component:
    #   #if isinstance(contrib, Nmr.PeakDimContribN):
    #   if contrib.className ==  'PeakDimContribN':
    #     continue
    #
    #   expDimRef = component.dataDimRef.expDimRef
    #   if expDimRef.unit == shiftList.unit:
    #     # Works for MQ etc
    #     value = getPeakDimComponentSplitting(component)
    #   else:
    #     continue
    #
    # else:
    value = peakDim.realValue

    # NBNB TBD spectrum dimensions weighting must be added
    # if hasApp:
    #   weight = getAnalysisDataDim(peakDim.dataDim).chemShiftWeight
    # else:
    weight = 1.0
 
    if peakList.isSimulated:
      weight *= simulatedPeakScale
 
    peakDims.append(peakDim)
    peaks.add(peak)
 
    vw    = value * weight
    sum1 += vw
    sum2 += value * vw
    N    += weight

  if N > 0.0:
    mean  = sum1/N
    mean2 = sum2/N
    sigma2= abs(mean2 - (mean * mean))
    sigma = math.sqrt(sigma2)
    
  else:
    # resonance has run out of contribs
    # - leave it be, even if orphaned
    # or all dataDimWeighting are zero
    self.error = 0.0
    return

  self.value = mean
  self.error = sigma
  self.peaks = peaks
  self.peakDims = peakDims

  return mean
