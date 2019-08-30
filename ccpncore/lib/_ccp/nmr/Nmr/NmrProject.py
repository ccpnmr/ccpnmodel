"""Functions for insertion into ccp.nmr.Nmr.NmrProject

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
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: wb104 $"
__date__ = "$Date: 2017-03-23 14:02:49 +0000 (Thu, March 23, 2017) $"

#=========================================================================================
# Start of code
#=========================================================================================
import os

from ccpn.util import Common as commonUtil
from ccpn.util.Constants import DEFAULT_SPECTRUM_PARAMETERS
from typing import Sequence
from ccpnmodel.ccpncore.lib import Constants
from ccpnmodel.ccpncore.lib.spectrum import Spectrum as spectrumLib
from ccpnmodel.ccpncore.lib.spectrum.formats import Azara, Bruker, Felix, Hdf5, NmrPipe, NmrView, Ucsf, Varian, Xeasy
from ccpnmodel.ccpncore.lib.Io.Formats import AZARA, BRUKER, FELIX, HDF5, NMRPIPE, NMRVIEW, UCSF, VARIAN, XEASY
from ccpn.util.Path import checkFilePath
from ccpnmodel.ccpncore.lib import V2Upgrade
from ccpn.util.Logging import getLogger


def loadDataSource(self:'NmrProject', filePath, dataFileFormat, name=None):

  isOk, msg = checkFilePath(filePath)

  if not isOk:
    # print(msg)
    getLogger().warning(msg)
    raise ValueError(msg)
    # # showError('Error', msg)
    # return None

  numPoints = None

  paramModules = {AZARA:Azara, BRUKER:Bruker, FELIX:Felix,
                  HDF5:Hdf5, NMRPIPE:NmrPipe, NMRVIEW:NmrView,
                  UCSF:Ucsf, VARIAN:Varian, XEASY:Xeasy}

  # dataFileFormat = getSpectrumFileFormat(filePath)
  if dataFileFormat is None:
    msg = 'Spectrum data format could not be determined for %s' % filePath
    getLogger().warning(msg)
    raise ValueError(msg)
    # # print(msg)
    # return None

  #
  # if dataFileFormat == CCPN:
  #   return project.getSpectrum(filePath)

  formatData = paramModules[dataFileFormat].readParams(filePath)

  if formatData is None:
    msg = 'Spectrum load failed for "%s": could not read params' % filePath
    getLogger().warning(msg)
    raise ValueError(msg)
    # # print(msg)
    # return None

  else:
    fileType, specFile, numPoints, blockSizes, wordSize, isBigEndian, \
    isFloatData, headerSize, blockHeaderSize, isotopes, specFreqs, specWidths, \
    refPoints, refPpms, sampledValues, sampledErrors, pulseProgram, dataScale = formatData

  if not os.path.exists(specFile):
    msg = 'Spectrum data file %s not found' % specFile
    getLogger().warning(msg)
    raise ValueError(msg)
    # # print(msg)
    # return None

  # NBNB TBD REDO!
  # This way of setting DataLocationStores and DataUrls is HOPELESS, STUPID KLUDGE!!
  # If we want each file to have an individual name with no support for grouping
  # them, let us for Gods sake remove the fancy stuff from the model.
  # Or at least refrain from creating individual DataLocationStores
  # when you only ever need one!
  # Rasmus Fogh
  dirName, fileName = os.path.split(specFile)

  if not name:
    name, fex = os.path.splitext(fileName)

    if (dataFileFormat == BRUKER) and name in ('1r','2rr','3rrr','4rrrr'):
      rest, lower = os.path.split(dirName)
      rest, mid = os.path.split(rest)

      if mid == 'pdata':
        rest, upper = os.path.split(rest)
        name = '%s-%s' % (upper, lower)

    if (dataFileFormat == NMRPIPE) and len(numPoints) > 2:
      name = os.path.basename(dirName)

    while any(x.findFirstDataSource(name=name) for x in self.experiments):
      name = commonUtil.incrementName(name)

  numberType = 'float' if isFloatData else 'int'
  experiment = self.createExperiment(name=name, numDim=len(numPoints),
                                sf=specFreqs, isotopeCodes=isotopes)

  # dataLocationStore = self.root.newDataLocationStore(name=name)
  # dataUrl = dataLocationStore.newDataUrl(url=Url(path=os.path.dirname(filePath)))
  # # NBNB TBD - this is WRONG
  # # the dataUrl should be made from dirName, NOT to the filePath directory.
  dataUrl = self.root.fetchDataUrl(dirName)

  blockMatrix = spectrumLib.createBlockedMatrix(dataUrl, specFile, numPoints=numPoints,
                                                blockSizes=blockSizes, isBigEndian=isBigEndian,
                                                numberType=numberType, headerSize=headerSize,
                                                nByte=wordSize, fileType=fileType)
  dataSource = experiment.createDataSource(name=name, numPoints=numPoints, sw=specWidths,
                                refppm=refPpms, refpt=refPoints, dataStore=blockMatrix,
                                sampledValues=sampledValues, sampledErrors=sampledErrors)

  experiment.resetAxisCodes()

  return dataSource


def createDummySpectrum(self:'NmrProject', axisCodes:Sequence[str],
                      name=None, shiftList=None) -> 'DataSource':
  """Make Experiment and DataSource with no data from list of standard atom axisCodes"""

  # Set up parameters and make Experiment
  numDim = len(axisCodes)
  isotopeCodes = tuple(commonUtil.name2IsotopeCode(x) or x for x in axisCodes)

  # This is used as the user-readable experiment type
  expName = ''.join(x for x in ''.join(axisCodes) if not x.isdigit())
  specName = name or expName

  experiment = self.createExperiment(name=expName, numDim=numDim,
                                     sf=[DEFAULT_SPECTRUM_PARAMETERS[x]['sf']
                                         for x in isotopeCodes],
                                     axisCodes=axisCodes, isotopeCodes=isotopeCodes,
                                     shiftList=shiftList)
  # Make dataSource with default parameters
  params = dict((tag,[DEFAULT_SPECTRUM_PARAMETERS[x][tag] for x in isotopeCodes])
                for tag in ('sw', 'refppm', 'refpt', 'numPoints'))
  #
  while True:
    #print ('@~@~ specName', specName)
    for exp in self.experiments:
      if exp.findFirstDataSource(name=specName) is not None:
        # We should only get here once, but if there is a name clash
        # this keeps adding '@n' till the name is unique
        #
        #print ('@~@~', specName, exp.findFirstDataSource(name=specName))
        specName = '%s@%s' %(specName, experiment.serial)
        break
    else:
      # No name clash - we are done
      break

  return experiment.createDataSource(name=specName, **params)


def createExperiment(self:'NmrProject', name:str, numDim:int, sf:Sequence[float],
                     isotopeCodes:Sequence[str], isAcquisition:Sequence[bool]=None,
                     axisCodes:Sequence[str]=None,
                     **additionalParameters) -> 'Experiment':
  """Create Experiment object ExpDim, and one ExpDimRef per ExpDim.
  Additional parameters to Experiment object are passed in additionalParameters"""

  experiment = self.newExperiment(name=name, numDim=numDim, **additionalParameters)

  if isAcquisition is None:
    isAcquisition = (False,) * numDim

  if experiment.shiftList is None:
    # Set shiftList, creating it if necessary
    shiftLists = [x for x in self.sortedMeasurementLists() if x.className == 'ShiftList']
    if len(shiftLists) == 1:
      shiftList = shiftLists[0]
    else:
      shiftList = (self.findFirstMeasurementList(className='ShiftList', name='default') or
                   self.newShiftList(name='default'))
    experiment.shiftList = shiftList

  for n, expDim in enumerate(experiment.sortedExpDims()):
    expDim.isAcquisition = isAcquisition[n]
    ic = isotopeCodes[n]
    if ic:
      params = {'sf':sf[n], 'unit':'ppm'}
      params['isotopeCodes'] = (ic,) if isinstance(ic, str) else ic
      if axisCodes:
        ac = axisCodes[n]
        if ac is not None:
          params['axisCode'] = ac
      expDim.newExpDimRef(**params)

  return experiment


def initialiseData(self:'NmrProject'):
  """Add objects that must be present from V3 onwards"""
  # add V3 mandatory objects (code in Project.__init__ and _fixLoadedProject)

  project = self.root

  # PeakLists and Spectrum
  for experiment in self.experiments:
    for dataSource in experiment.dataSources:

      if not dataSource.findFirstPeakList(dataType='Peak'):
        # Set a peakList for every spectrum
        dataSource.newPeakList()

        # 20190520:ED new code to set colours and update contour levels now in core project_initialiseProject
      # if not dataSource.positiveContourColour or not dataSource.negativeContourColour:
      #   # set contour colours for every spectrum
      #   (dataSource.positiveContourColour,
      #    dataSource.negativeContourColour) = dataSource.getDefaultColours()
      # if not dataSource.sliceColour:
      #   dataSource.sliceColour = dataSource.positiveContourColour

  # MolSystem
  if self.molSystem is None:
    project.newMolSystem(name=self.name, code=self.name,
                            nmrProjects = (self,))

  # SampleStore
  apiSampleStore = self.sampleStore
  if apiSampleStore is None:
    apiSampleStore = (project.findFirstSampleStore(name='default') or
                      project.newSampleStore(name='default'))
    self.sampleStore = apiSampleStore

  # RefSampleComponentStore
  apiComponentStore = apiSampleStore.refSampleComponentStore
  if apiComponentStore is None:
    apiComponentStore = (project.findFirstRefSampleComponentStore(name='default') or
                         project.newRefSampleComponentStore(name='default'))
    apiSampleStore.refSampleComponentStore = apiComponentStore

  # Make Substances that match finalised Molecules
  for apiMolecule in project.sortedMolecules():
    if apiMolecule.isFinalised:
      # Create matchingMolComponent if none exists
      apiComponentStore.fetchMolComponent(apiMolecule)

  # Fix alpha or semi-broken projects. None of this should be necessary, but hey!
  # NB written to modify nothing for valid projects

  # # Get or (re)make default NmrChain
  # defaultChain = self.findFirstNmrChain(code=Constants.defaultNmrChainCode)
  # if defaultChain is None:
  #   # NO default chain - probably an alpha project or upgraded from V2
  #   defaultChain = self.findFirstNmrChain(code='@-')
  #   if defaultChain is None:
  #     defaultChain = self.newNmrChain(code=Constants.defaultNmrChainCode)
  #   else:
  #     defaultChain.code = '@-'
  # Get or (re)make default NmrChain
  defaultChain = self.findFirstNmrChain(code=Constants.defaultNmrChainCode)
  if defaultChain is None:
    defaultChain = self.newNmrChain(code=Constants.defaultNmrChainCode)

  # Make sure all non-offset ResonanceGroups have directNmrChain set.
  for rg in self.sortedResonanceGroups():
    if rg.mainGroupSerial == rg.serial:
      rg.mainGroupSerial = None
    if rg.mainGroupSerial is None and rg.directNmrChain is None:
      if hasattr(rg, 'chainSerial') and rg.chainSerial is not None:
        rg.directNmrChain = self.findFirstNmrChain(serial=rg.chainSerial)
      if rg.directNmrChain is None:
        rg.directNmrChain = defaultChain

  # Make ResonanceGroup for Resonances without them
  # Should not be necessary, for a well-set-up project, but for dodgy ones ...?
  resonances = [x for x in self.sortedResonances() if x.resonanceGroup is None]
  if resonances:
    defaultNmrChain = self.findFirstNmrChain(code=Constants.defaultNmrChainCode)
    if defaultNmrChain is None:
      defaultNmrChain = self.newNmrChain(code=Constants.defaultNmrChainCode)
    # Also set defaultResonanceGroup
    defaultResonanceGroup = (
      defaultNmrChain.findFirstResonanceGroup(seqCode=None,seqInsertCode='@')
      or self.newResonanceGroup(directNmrChain=defaultNmrChain, seqInsertCode='@',
                                details="Default ResonanceGroup")
    )
    for resonance in resonances:
      implName = resonance.implName
      if resonance.implName:
        resonance.implName = '%s@%s' % (implName, resonance.serial)
    defaultResonanceGroup.resonances = resonances

  # Upgrade old-style constraint lists
  for nmrConstraintStore in project.sortedNmrConstraintStores():
    for constraintList in nmrConstraintStore.sortedConstraintLists():
      if constraintList.className != 'GenericConstraintList':
        newConstraintList = V2Upgrade.upgradeConstraintList(constraintList)

  # End of API object fixing

def initialiseGraphicsData(self:'NmrProject'):
  """Add API objects that must exist for V3 GUI operation"""

  project = self.root

  # Make sure we have a WindowStore attached to the NmrProject - that guarantees a mainWindow
  # apiNmrProject = self.fetchNmrProject()
  if self.windowStore is None:
    self.windowStore = project.newWindowStore(nmrProject=self)

  # Ensure there is a (single) task
  # NB The underlying task must be made, even if it is not visible in the wrapper
  if not project.findAllGuiTasks(nmrProject=self):
    guiTask = project.newGuiTask(name='View', nmrProject=self,
                                 windows=(self.windowStore.mainWindow,))

  # add V3 mandatory objects like MainWindow and Task (code in initProject)
