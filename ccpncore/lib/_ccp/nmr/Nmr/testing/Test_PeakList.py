"""Module Documentation here

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:12 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b3 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
# import numpy

from ccpnmodel.ccpncore.testing.CoreTesting import CoreTesting

class PeakListPickPeaksTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = 'CcpnCourse1a'

  def Test_PickPeaks(self, *args, **kw):
    
    dataSource = self.nmrProject.findFirstExperiment(name='HSQC').findFirstDataSource()
    peakList = dataSource.findFirstPeakList()
    numPoints = [dataDim.numPoints for dataDim in dataSource.sortedDataDims()]
    startPoint = [0, 0]
    endPoint = numPoints
    posLevel = 1.0e8

    peaks = peakList.pickNewPeaks(startPoint, endPoint, posLevel, fitMethod='gaussian')
    print('number of peaks', len(peaks))
    assert len(peaks) == 4, 'len(peaks) = %d' % len(peaks)
    
    for peak in peaks:
      print([peakDim.position for peakDim in peak.sortedPeakDims()])
    
  def Test_PickPeaks2(self, *args, **kw):
    
    dataSource = self.nmrProject.findFirstExperiment(name='HSQC').findFirstDataSource()
    peakList = dataSource.findFirstPeakList()
    numPoints = [dataDim.numPoints for dataDim in dataSource.sortedDataDims()]
    startPoint = [600, 100]
    endPoint = [700, 150]
    posLevel = 1.0e8

    peaks = peakList.pickNewPeaks(startPoint, endPoint, posLevel, fitMethod='gaussian')
    print('number of peaks', len(peaks))
    assert len(peaks) == 3, 'len(peaks) = %d' % len(peaks)
    
    for peak in peaks:
      print([peakDim.position for peakDim in peak.sortedPeakDims()])
  
