"""Code for recognising and analysing external data formats

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
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
import os
import tarfile

from ccpn.util import Path
from ccpn.util import Common as commonUtil

# Spectrum formats
AZARA = 'Azara'
BRUKER = 'Bruker'
FELIX = 'Felix'
HDF5 = 'Hdf5'
NMRPIPE = 'NmrPipe'
NMRVIEW = 'NmrView'
UCSF = 'UCSF'
VARIAN = 'Varian'
XEASY = 'XEASY'

ANSIG = 'ANSIG'
AUTOASSIGN = 'AutoAssign'
CCPN = 'CCPN'
CCPNTARFILE = 'CCPNTARFILE'
NEF = 'nef'
SPARKY = 'Sparky'
NMRDRAW = 'NMRDraw'
NMRSTAR = 'NMR-STAR'

# Sequence formats
FASTA = 'Fasta'

# Structure formats
PDB = 'PDB'

# Macro formats
PYTHON = 'Python'

#  Look-up formats
CSV = 'csv'
EXCEL = 'Excel'


DataTypes = ['Project', 'Spectrum', 'Text', 'Sequence', 'LookupFile', 'Structure', 'Macro']

def analyseUrl(filePath):
  """ Analyse filePath, and return (dataType, subType, usePath) tuple

  Note:
  For Bruker and Varian Spectrum data, the usePath returned is the directory containing the spectrum
  """

  isOk, msg = Path.checkFilePath(filePath)
  if not isOk:
    print (msg)
    return (None, None, filePath)

  # Deal with directories as input
  if os.path.isdir(filePath):

    # remove trailing '/',  lest subsequent code fail
    baseName, junk = os.path.split(filePath)
    if not junk:
      filePath = baseName

    # url is a directory
    fileNames = os.listdir(filePath)

    if filePath.endswith(Path.CCPN_DIRECTORY_SUFFIX) and Path.CCPN_API_DIRECTORY in fileNames:
      # V3 CCPN Project
      return ('Project', CCPN, filePath)

    elif 'memops' in fileNames:
      # V2 CCPN project, or 'ccpnv3' subdirectory of a V3 project (handled downstream)

      # CCPN Project
      return ('Project', CCPN, filePath)

    elif 'procs' in fileNames:

      # 'Bruker processed spectrum'
      return ('Spectrum', BRUKER, filePath)

    elif 'procpar' in fileNames:

      # Varian processed spectrum
      return ('Spectrum', VARIAN, filePath)


    else:
      # fileNames = os.listdir(filePath)

      for dirp, dirn, file in  os.walk(filePath):
        for name in file:
          path = os.path.join(dirp, name)

          if path.endswith('procs'):
            filePath = path
            return ('Spectrum', BRUKER, filePath)

    # No match
    return (None, None, filePath)

  if filePath.endswith('.hdf5'): # TBD: is this what we want?
    return ('Spectrum', HDF5, filePath)

  elif filePath.endswith('.nef'):
    # NBNB TODO is this OK? enough?
    return ('Project', NEF, filePath)

  elif filePath.endswith('.str'):
    # NBNB TODO:ED is this OK? enough?
    return ('Project', NMRSTAR, filePath)

  # Set up for further analysis
  dirName, fileName = os.path.split(filePath)

  # Check for binary files
  fileObj = open(filePath, 'rb')
  firstData = fileObj.read(1024)
  testData = set([c for c in firstData]) - commonUtil.WHITESPACE_AND_NULL
  isBinary = (min([ord(chr(c)) for c in testData]) < 32)

  # Deal with binary files
  if isBinary:
    # probably binary

    # UCSF spectrum
    if b'UCSF NMR' in firstData:
      return ('Spectrum', UCSF, filePath)

    refBytes = [ 0x40, 0x16, 0x14, 0x7b ]
    qBytes = [ ord(chr(c)) for c in firstData[8:12] ]

    # NMRPIPE spectrum
    if qBytes == refBytes:
      return ('Spectrum', NMRPIPE, filePath)

    qBytes.reverse()
    if qBytes == refBytes:
      return ('Spectrum', NMRPIPE, filePath)

    # NMRVIEW spectrum
    refBytes = ['34','18','AB','CD']
    qBytes = ["%02X" % ord(chr(c)) for c in firstData[:4]]

    if qBytes == refBytes:
      return ('Spectrum', NMRVIEW, filePath)


    qBytes.reverse()
    if qBytes == refBytes:
      return ('Spectrum', NMRVIEW, filePath)

    # BRUKER file
    if fileName in ('1r','2rr','3rrr','4rrrr'):
      return ('Spectrum', BRUKER, dirName)

    if fileName == 'phasefile':
      return ('Spectrum', VARIAN, dirName)

    if fileName.endswith('.spc'):
      return ('Spectrum', AZARA, filePath+'.par')

    from array import array

    vals = array('i')
    vals.fromstring(firstData[:4])
    if (0 < vals[0] < 6) and (vals[1] == 1):
      return ('Spectrum', FELIX, filePath)

    vals.byteswap()
    if (0 < vals[0] < 6) and (vals[1] == 1):
      return ('Spectrum', FELIX, filePath)

    if fileName.endswith('.tar.gz') or fileName.endswith('.tgz'):
      tp = tarfile.open(filePath, 'r')
      ok = False
      for tarPath in tp.getnames():
        allButTopDirectory = Path.converseSplitPath(tarPath)[1]
        oneLevelDownDirectory = Path.converseSplitPath(allButTopDirectory)[0]
        if oneLevelDownDirectory in ('ccpnv3', 'memops'): # v3 and v2 projects, respectively
          ok = True
          break
      if ok:
        return ('Project', CCPNTARFILE, filePath)


  if filePath.endswith('.csv'):
    return ('LookupFile', CSV, filePath)

  if filePath.endswith(('.xls', '.xlsx')):
    return ('LookupFile', EXCEL, filePath)

  else:

    fileObj.close()
    text = open(filePath, 'rU').read()
    textblock = '\n'.join([line.strip() for line in text.splitlines()
                           if not (line and line[0] == '!')])

    # NBNB FIXME TBD This assumes that comments are given by '!' in the first char.
    # IS THAT ALWAYS THE CASE?

    if filePath.endswith('.fasta') or text.startswith('>'):
      # FASTA file
      return ('Sequence', FASTA, filePath)
    elif filePath.endswith('.py'):
      return ('Macro', PYTHON, filePath)

    if textblock.startswith('##TITLE'):
      return ('Spectrum', BRUKER, dirName)

    if textblock.startswith('Version .....'):
      # NBNB TBD FIXME what data is this?
      return (None, XEASY, filePath)

    if fileName == 'procpar':
      return ('Spectrum', VARIAN, dirName)

    if (('.par' in fileName) and ('ndim ' in textblock) and ('file ' in textblock) and
        ('npts ' in textblock) and ('block ' in textblock)):
      return ('Spectrum', AZARA, filePath)

    if any(line for line in textblock.splitlines() if line.startswith('ATOM  ')):
      # Assume it is a PDB-type file
      return ('Structure', PDB, filePath)

    if textblock.startswith('<sparky project file>'):
      # ejb - new sparky project reader, must be the .proj/.proj.BAK file
      return ('Project', SPARKY, filePath)

    if textblock.startswith('<sparky save file>'):
      # ejb - new sparky project reader, must be the .save/.save.BAK file
      return ('Project', SPARKY, filePath)

    # Default - return as plain text
    return ('Text', None, filePath)

  # No match
  return (None, None, filePath)
