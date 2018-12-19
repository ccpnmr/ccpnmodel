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
__version__ = "$Revision: 3.0.b4 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

from ccpnmodel.ccpncore.testing.CoreTesting import CoreTesting


class DataSourcePlaneDataTest(CoreTesting):
    # Path of project to load (None for new project)
    projectPath = 'CcpnCourse1a'

    def Test_GetPlaneData(self, *args, **kw):
        spectrum = self.nmrProject.findFirstExperiment(name='HSQC').findFirstDataSource()
        planeData = spectrum.getPlaneData()
        print('planeData.shape =', planeData.shape)
        print('planeData =', planeData[508:, 2045:])


class DataSourceSliceDataTest(CoreTesting):
    # Path of project to load (None for new project)
    projectPath = 'CcpnCourse1a'

    def Test_GetSliceData(self, *args, **kw):
        spectrum = self.nmrProject.findFirstExperiment(name='HSQC').findFirstDataSource()
        # just check an arbitrary slice
        sliceData = spectrum.getSliceData(position=(1001, 231), sliceDim=2)
        print('sliceData.shape =', sliceData.shape)
        # check a small part of the returned data
        actualInd = 379
        actualData = [-75826.875, -135818.1563, -132515.0938, -76160.47656, 14403.3877, 119186.0625]
        sliceData = sliceData[actualInd:actualInd + len(actualData)]
        print('sliceData =', sliceData)
        diff = sum(abs(actualData - sliceData))
        assert diff < 0.001
