"""Module Documentation here

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
__dateModified__ = "$dateModified: 2017-04-07 11:41:40 +0100 (Fri, April 07, 2017) $"
__version__ = "$Revision: 3.0.b1 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"

__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from ccpnmodel.ccpncore.testing.CoreTesting import CoreTesting

from ccpnmodel.ccpncore.lib.spectrum import Peak

class PeakTest(CoreTesting):

  # Path of project to load (None for new project)
  projectPath = 'CcpnCourse1b'

  def Test_PeakFit(self, *args, **kw):
    print('project.name = %s' % self.project.name)
    nmrProject = self.project.findFirstNmrProject()
    experiment = nmrProject.findFirstExperiment(name='HSQC')
    dataSource = experiment.findFirstDataSource()
    peakList = dataSource.findFirstPeakList()
    print('peakList = %s' % peakList)
    peak = peakList.findFirstPeak(serial=42)
    print('peak = %s, peak.height = %f' % (peak, peak.height))
    peaks = [peak]
    Peak.fitExistingPeaks(peaks, fitMethod='gaussian')
    print('peak.height = %f' % peak.height)
    
