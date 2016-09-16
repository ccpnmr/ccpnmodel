import os
import csv
from collections import OrderedDict
import pathlib
import pandas as pd
# from PyQt4 import QtCore, QtGui


# if project._appBase.applicationName == 'Screen':
# if project._appBase.applicationName == 'Metabolomics':


# def readXls(project, path=None):
#
#   ex = pd.ExcelFile(path)
#   for p,f in screenExcelSheetProcessors.items():
#     if p in ex.sheet_names:
#       e = ex.parse(p)
#       e.fillna('Empty',inplace=True)
#       f(project, e)

def readXls(project, path):
  ex = pd.ExcelFile(path)
  if ex.sheet_names == ['Metabolomics']:
    print('loading metabolomics...')
    readXlsMetabolomics(ex, project, path)
  else:
    readXlsScreen(ex, project, path)

screeningSheetNames = ['Reference', 'STD_Samples']

def readXlsScreen(ex, project, path=None):

  ex = pd.ExcelFile(path)
  for sheetName in screeningSheetNames:
    if sheetName in ex.sheet_names:
      dataFrame = ex.parse(sheetName)
      dataFrame.fillna('Empty',inplace=True)
      workingDirectoryPath = getWorkingDirectoryPath(path)
      brukerDirs = getBrukerTopDirs(workingDirectoryPath)

      if sheetName == 'Reference':
        dataDicts =  createSpectrumDataDicts(project, workingDirectoryPath, brukerDirs, dataFrame)
        loadReferenceSheet(project, dataDicts)
      if sheetName == 'STD_Samples':
        loadSTDSheet(project, workingDirectoryPath, brukerDirs, dataFrame)


def getWorkingDirectoryPath(xlsPath):
  xlsLookupPath = pathlib.Path(xlsPath)
  return str(xlsLookupPath.parent)

def getBrukerTopDirs(workingDirectoryPath):
  dirs = os.listdir(str(workingDirectoryPath))
  excludedFiles = ('.DS_Store', '.xls')
  brukerDirs = [dir for dir in dirs if not dir.endswith(excludedFiles)]
  return brukerDirs


def createSpectrumDataDicts(project, workingDirectoryPath, brukerDirs, dataFrame):
  dataDicts = []
  for spectrumName, spectrumPath in zip(brukerDirs, getFullFilePaths(brukerDirs, workingDirectoryPath)) :
    for name in dataFrame['name']:
      if str(spectrumName) == str(name):
        for data in dataFrame.to_dict(orient="index").values():
          for key, value in data.items():
            if key == 'name':
              if str(value) == str(spectrumName):
                spectrum = project.loadData(spectrumPath)
                dataDict = {spectrum[0]:data}
                dataDicts.append(dataDict)
  return dataDicts

def getFullFilePaths(brukerDirs, workingDirectoryPath):
  fullPaths = []
  for spectrumName in brukerDirs:
    path = workingDirectoryPath + '/' + spectrumName
    for dirname, dirnames, filenames in os.walk(path):
      for filename in filenames:
        if filename == '1r':
          fullPath = os.path.join(dirname, filename)
          fullPaths.append(fullPath)
  return fullPaths



def readXlsMetabolomics(ex, project, path):
  metsSheet = getMetabolomicsSheet(ex)
  dataLocations = getRelativeBrukerDataLocations(metsSheet)
  spectra = loadBrukerSpectra(project, path, dataLocations)
  try:
    spectrumNames = getSpectrumNamesFromDf(metsSheet)
    for spectrum, name in list(zip(spectra, spectrumNames)):
      spectrum.rename(name)
  except KeyError:
    pass
  groups = getAllSpectrumGroupAssignments(spectra, metsSheet)
  for k, v in sorted(groups.items()):
    project.newSpectrumGroup(name=k, spectra=v)

def getMetabolomicsSheet(excelFile):
  sheet = excelFile.parse('Metabolomics')
  sheet = sheet.replace(regex='^# .*', value=pd.np.nan)
  sheet = sheet.dropna((0, 1), how='all')
  sheet['expno'] = sheet['expno'].astype(int)
  sheet['procno'] = sheet['procno'].astype(int)
  for column in sheet.columns:
    sheet[column] = sheet[column].astype(str)
  return sheet

def getRelativeBrukerDataLocations(df):
  expnos = df['expno'].values
  procnos = df['procno'].values
  return list(zip(expnos, procnos))

def loadBrukerSpectra(project, path, locations):
  specs = []
  # path = os.path.join(os.path.split(path)[:-1])[0]
  path = os.path.split(path)[0]
  for location in locations:
    specLocation = os.path.join(path, location[0], 'pdata', location[1])
    specs.append(project.loadData(specLocation)[0])
  return specs

def getSpectrumNamesFromDf(df):
  return list(df['name'].values)

def getAllGroupsFromDf(df):
  groupsDf = df[[c for c in df.columns if c.startswith('group ')]]
  groupsDf.columns = [c.split(' ')[1] for c in groupsDf.columns]
  groupsLists = groupsDf.to_dict(orient='list')
  groups = []
  for k, v in groupsLists.items():
    for g in set(v):
      groups.append('_'.join((str(k), str(g))))
  return groups

def getSpecrumGroupsByName(df, name):
  row = df[df['name'] == name]
  return getAllGroupsFromDf(row)

def getAllSpectrumGroupAssignments(spectra, df):
  assembledGroups = {k: [] for k in getAllGroupsFromDf(df)}
  # print(df)
  # print(spectrum)
  for spectrum in spectra:
    groups = getSpecrumGroupsByName(df, spectrum.name)
    for group in groups:
      assembledGroups[group].append(spectrum)
  return assembledGroups

# def readXls(project, path=None):
#   ex = pd.ExcelFile(path)
#   excelSheet = ex.parse(ex.sheet_names[0])
#   excelSheet.fillna('Empty',inplace=True)
#   createDataDict(project, excelSheet)
#
#   if len(ex.sheet_names) > 1:
#     secondSheetExcel = ex.parse(ex.sheet_names[1])
#     secondSheetExcel.fillna('Empty',inplace=True)
#     createSampleDicts(project, secondSheetExcel)

def readCsv(project, path=None):

  csv_in = open(path, 'r')
  reader = csv.reader(csv_in)
  for row in reader:
    if row[0].split('/')[-1] == 'procs':
      filename = row[0].split('/')
      filename.pop()
      filenamePath = '/'.join(filename)
      spectrum = project.loadData(filenamePath)


def loadReferenceSheet(project, dataDicts):
  ''' dispatch data to the project'''
  createGroupNameDicts(project, dataDicts)
  if project._appBase.applicationName == 'AnalysisScreen':
      createNewSubstance(project, dataDicts)


def createGroupNameDicts(project,dataDicts):
  ''' creates dicts group name with its spectrum '''
  groupNameDicts = []
  for dataDict in dataDicts:
    for spectrum, data in dataDict.items():
      groupNameDict= {str(groupName):spectrum for header, groupName in data.items() if header == 'groupName'}
      groupNameDicts.append(groupNameDict)
  newSpectrumGroup(project, groupNameDicts)

def newSpectrumGroup(project, groupNameDicts):
  '''creates new spectrum group for the project. If more groups have the same name they are merged'''
  newGroupsDict = {}
  for groupName in set(k for d in groupNameDicts for k in d):
    newGroupsDict[groupName] = [d[groupName] for d in groupNameDicts if groupName in d]
  for groupName, spectra in newGroupsDict.items():
    print(groupName, spectra)
    newSpectrumGroup = project.newSpectrumGroup(name=groupName, spectra=spectra)




def _loadSTDtoProject(project, dataFrame, workingDirectoryPath):
  '''creates new sample for the project and associate all value in a dict'''
  STDs_Off_Res_SP = []
  STDs_ON_Res_SP = []
  for data in dataFrame.to_dict(orient="index").values():
    for key, value in data.items():
        if key == 'SampleName':
          sample = project.newSample(str(value))
          loadSTDspectra(project, sample,data, workingDirectoryPath)
          STDs_Off_Res_SP.append(getSTDoffResonance(sample))
          STDs_ON_Res_SP.append(getSTDonResonance(sample))
          for sampleProperty in sampleProperties:
            sampleProperty(sample, data)

  project.newSpectrumGroup('STD_OFF_RES', spectra=STDs_Off_Res_SP)
  project.newSpectrumGroup('STD_ON_RES', spectra=STDs_ON_Res_SP)
  project.newSpectrumGroup('STD_DIFF')

def getSTDoffResonance(sample):
  return sample.spectra[0]

def getSTDonResonance(sample):
  return sample.spectra[1]


def loadSTDSheet(project, workingDirectoryPath, brukerDirs, dataFrame):
  _loadSTDtoProject(project, dataFrame, workingDirectoryPath)


def createNewSubstance(project, dataDicts):
  for dataDict in dataDicts:
    for spectrum, data in dataDict.items():
      expType = ([[key, value] for key, value in data.items() if key == 'expType'])
      newSubstance = project.newSubstance(name=spectrum.id, labeling=str(expType[0][1]))
      # newChain = project.createChain(sequence=str('A'),compoundName=str(spectrum.name), molType='protein')
      newSubstance.referenceSpectra = [spectrum]
      dispatchSubstanceProperties(newSubstance, data)

def dispatchSubstanceProperties(substance, data):
  for substanceProperty in substanceProperties:
    substanceProperty(substance, data)

def dispatchSampleProperties(sample, data):
  for sampleProperty in sampleProperties:
    sampleProperty(sample, data)

def addSampleComponents(sample, data):
  sampleComponents = [[header, sampleComponentName] for header, sampleComponentName in data.items() if header == 'sampleComponents']
  for name in sampleComponents[0][1].split(','):
    sampleComponent = sample.newSampleComponent(name=(str(name)+'-1'), labeling='H')


def createStdSpectrumGroup(project,):
  spectra = []
  for sample in project.samples:
    for spectrum in sample.spectra:
      spectra.append(spectrum)
  for spectrumGroup in project.spectrumGroups:
    if spectrumGroup.name == 'STD':
      spectrumGroup.spectra = spectra

def loadSTDspectra(project, sample, data, workingDirectoryPath):
  stdOffSpectrumName = [[excelHeader, value] for excelHeader, value in data.items()
                   if excelHeader == 'spectrumOFF_Resonance' and value != 'Empty']
  stdOnSpectrumName = [[excelHeader, value] for excelHeader, value in data.items()
                        if excelHeader == 'spectrumON_Resonance' and value != 'Empty']
  brukerDirNames = [str(stdOffSpectrumName[0][1]), str(stdOnSpectrumName[0][1])]
  fullPaths = getFullFilePaths(brukerDirNames, workingDirectoryPath)
  spectra = [project.loadData(path)[0] for  path in fullPaths]
  sample.spectra = spectra


def setSamplepH(sample, data):
  samplePH = [[excelHeader, value] for excelHeader, value in data.items()
              if excelHeader == 'pH' and value != 'Empty']
  if len(samplePH)>0:
    sample.ph = samplePH[0][1]

def setSampleIonicStrength(sample, data):
  ionicStrength = [[excelHeader, value] for excelHeader, value in data.items()
                   if excelHeader == 'ionicStrength'and value != 'Empty']
  if len(ionicStrength)>0:
    sample.ph = ionicStrength[0][1]

def setSampleAmount(sample, data):
  amount = [[excelHeader, value] for excelHeader, value in data.items()
            if excelHeader == 'amount' and value != 'Empty']
  if len(amount)>0:
    sample.amount = amount[0][1]

def setSampleAmountUnit(sample, data):
  amountUnit = [[excelHeader, value] for excelHeader, value in data.items()
                if excelHeader == 'amountUnit' and value != 'Empty']
  if len(amountUnit)>0:
    sample.amountUnit = amountUnit[0][1]

def setSampleCreationDate(sample, data):
  creationDate = [[excelHeader, value] for excelHeader, value in data.items()
                  if excelHeader == 'creationDate' and value != 'Empty']
  if len(creationDate)>0:
    sample.creationDate = creationDate[0][1]

def setSampleBatchIdentifier(sample, data):
  batchIdentifier = [[excelHeader, value] for excelHeader, value in data.items()
                     if excelHeader == 'batchIdentifier' and value != 'Empty']
  if len(batchIdentifier)>0:
    sample.batchIdentifier = batchIdentifier[0][1]

def setSamplePlateIdentifier(sample, data):
  plateIdentifier = [[excelHeader, value] for excelHeader, value in data.items()
                     if excelHeader == 'plateIdentifier' and value != 'Empty']
  if len(plateIdentifier)>0:
   sample.plateIdentifier = plateIdentifier[0][1]

def setSampleRowNumber(sample, data):
  rowNumber = [[excelHeader, value] for excelHeader, value in data.items()
               if excelHeader == 'rowNumber' and value != 'Empty']
  if len(rowNumber)>0:
    sample.rowNumber = rowNumber[0][1]

def setSampleColumnNumberr(sample, data):
  columnNumber = [[excelHeader, value] for excelHeader, value in data.items()
                  if excelHeader == 'columnNumber' and value != 'Empty']
  if len(columnNumber)>0:
    sample.columnNumber = columnNumber[0][1]

def setSampleComment(sample, data):
  comments = [[excelHeader, value] for excelHeader, value in data.items()
              if excelHeader == 'sampleComments' and value != 'Empty']
  if len(comments)>0:
    sample.comments = comments[0][1]

sampleProperties = [addSampleComponents, setSamplepH,
  setSampleIonicStrength, setSampleAmount, setSampleAmountUnit, setSampleCreationDate,
  setSampleBatchIdentifier, setSampleRowNumber, setSampleColumnNumberr, setSampleComment]

### Setting Substance properties

def setSubstanceType(substance, data):
  substanceType = [[excelHeader, value] for excelHeader, value in data.items()
                   if excelHeader == 'substanceType' and value != 'Empty']
  if len(substanceType)>0:
   substance.substanceType = str(substanceType[0][1])

def setSubstanceSynonyms(substance, data):
  substanceSynonyms = [[excelHeader, value] for excelHeader, value in data.items()
                       if excelHeader == 'substanceSynonyms']
  if len(substanceSynonyms)>0:
    substance.synonyms = substanceSynonyms[0][1]

def setSubstanceComment(substance, data):
  comments = [[excelHeader, value] for excelHeader, value in data.items()
              if excelHeader == 'substanceComments' and value != 'Empty']
  if len(comments)>0:
    substance.comments = comments[0][1]

def setSubstanceUserCode(substance, data):
  userCode = [[excelHeader, value] for excelHeader, value in data.items()
              if excelHeader == 'substanceUserCode' and value != 'Empty']
  if len(userCode)>0:
    substance.userCode = userCode[0][1]

def setSubstanceSmiles(substance, data):
  smiles = [[excelHeader, value] for excelHeader, value in data.items()
            if excelHeader == 'substanceSmiles' and value != 'Empty']
  if len(smiles)>0:
    substance.smiles = smiles[0][1]

def setSubstanceInChi(substance, data):
  inChi = [[excelHeader, value] for excelHeader, value in data.items()
           if excelHeader == 'substanceInChi' and value != 'Empty']
  if len(inChi)>0:
    substance.inChi = inChi[0][1]

def setSubstanceCasNumber(substance, data):
  substanceCasNumber = [[excelHeader, value] for excelHeader, value in data.items()
                        if excelHeader == 'substanceCasNumber' and value != 'Empty']
  if len(substanceCasNumber)>0:
    substance.casNumber = substanceCasNumber[0][1]

def setSubstanceEmpiricalFormula(substance, data):
  substanceEmpiricalFormula = [[excelHeader, value] for excelHeader, value in data.items()
                               if excelHeader == 'substanceEmpiricalFormula' and value != 'Empty']
  if len(substanceEmpiricalFormula)>0:
    substance.empiricalFormula = substanceEmpiricalFormula[0][1]

def setSubstanceMolecularMass(substance, data):
  substanceMolecularMass = [[excelHeader, value] for excelHeader, value in data.items()
                            if excelHeader == 'molecularMass' and value != 'Empty']
  if len(substanceMolecularMass)>0:
    substance.molecularMass = substanceMolecularMass[0][1]

def setSubstanceHAtomCount(substance, data):
  substanceHAtomCount = [[excelHeader, value] for excelHeader, value in data.items()
                         if excelHeader == 'substanceHAtomCount' and value != 'Empty']
  if len(substanceHAtomCount)>0:
    substance.atomCount = substanceHAtomCount[0][1]

def setSubstanceBondCount(substance, data):
  substanceBondCount = [[excelHeader, value] for excelHeader, value in data.items()
                        if excelHeader == 'substanceBondCount' and value != 'Empty']
  if len(substanceBondCount)>0:
    substance.bondCount = substanceBondCount[0][1]

def setSubstanceRingCount(substance, data):
  substanceRingCount = [[excelHeader, value] for excelHeader, value in data.items()
                        if excelHeader == 'substanceRingCount' and value != 'Empty']
  if len(substanceRingCount)>0:
    substance.ringCount = substanceRingCount[0][1]

def setSubstanceHBondDonorCount(substance, data):
  substanceHBondDonorCount = [[excelHeader, value] for excelHeader, value in data.items()
                              if excelHeader == 'Hdonor' and value != 'Empty']
  if len(substanceHBondDonorCount)>0:
    substance.hBondDonorCount = substanceHBondDonorCount[0][1]

def setSubstanceHBondAcceptorCount(substance, data):
  substanceHBondDonorCount = [[excelHeader, value] for excelHeader, value in data.items()
                              if excelHeader == 'Hacceptor' and value != 'Empty']
  if len(substanceHBondDonorCount)>0:
    substance.hBondAcceptorCount = substanceHBondDonorCount[0][1]

def setSubstancePolarSurfaceArea(substance, data):
  substancePolarSurfaceArea = [[excelHeader, value] for excelHeader, value in data.items()
                               if excelHeader == 'substancePolarSurfaceArea' and value != 'Empty']
  if len(substancePolarSurfaceArea)>0:
    substance.polarSurfaceArea = substancePolarSurfaceArea[0][1]

def setSubstanceLogPartitionCoefficient(substance, data):
  substanceLogPartitionCoefficient = [[excelHeader, value] for excelHeader, value in data.items()
                                      if excelHeader == 'cLogP' and value != 'Empty']
  if len(substanceLogPartitionCoefficient)>0:
    substance.logPartitionCoefficient = substanceLogPartitionCoefficient[0][1]

substanceProperties = [setSubstanceType, setSubstanceComment, setSubstanceSynonyms, setSubstanceUserCode,
  setSubstanceSmiles, setSubstanceInChi, setSubstanceCasNumber, setSubstanceEmpiricalFormula,
  setSubstanceMolecularMass, setSubstanceHAtomCount, setSubstanceBondCount, setSubstanceRingCount,
  setSubstanceLogPartitionCoefficient,setSubstancePolarSurfaceArea,
  setSubstanceHBondDonorCount, setSubstanceHBondAcceptorCount]


### Loading obj in SideBar

# Feb 2106 Rasmus Fogh. No longer needed

# def loadSpectrumInSideBar(project, spectrum):
#   ''' load the spectrum in the sidebar '''
#   peakList = spectrum.newPeakList()
#   sideBar = project._appBase.mainWindow.sideBar
#   spectra = sideBar.spectrumItem
#   newSpectrumItem = sideBar.addItem(spectra, spectrum)
#   peakListItem = QtGui.QTreeWidgetItem(newSpectrumItem)
#   peakListItem.setText(0, peakList.pid)

# def loadSampleInSideBar(project, sample):
#   sideBar = project._appBase.mainWindow.sideBar
#   sampleSideBar = sideBar.samplesItem
#   sampleItem =  sideBar.addItem(sampleSideBar, sample)
#   for sampleComponent in sample.sampleComponents[0:]:
#     sideBar.addItem(sampleItem, sampleComponent)
#
# def loadSpectrumGroupInSideBar(project, newSpectrumGroup):
#   sideBar = project._appBase.mainWindow.sideBar
#   spectrumGroupItem = sideBar.spectrumGroupItem
#   newGroupItem =  sideBar.addItem(spectrumGroupItem, newSpectrumGroup)
#   for spectrum in newSpectrumGroup.spectra:
#     sideBar.addItem(newGroupItem, spectrum)
#     peakList = spectrum.newPeakList()
