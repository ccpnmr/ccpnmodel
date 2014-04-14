"""
======================COPYRIGHT/LICENSE START==========================

upgrade.py: Data compatibility handling

Copyright (C) 2007-2014 Rasmus Fogh (CCPN project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

A copy of this license can be found in ../../../../license/LGPL.license.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

======================COPYRIGHT/LICENSE END============================

To obtain more information about this code:

- CCPN website (http://www.ccpn.ac.uk)

- contact Rasmus Fogh (ccpn@bioc.cam.ac.uk)

=======================================================================

If you are using this software for academic purposes, we suggest
quoting the following reference:

===========================REFERENCE START=============================
Rasmus H. Fogh, Wayne Boucher, Wim F. Vranken, Anne
Pajon, Tim J. Stevens, T.N. Bhat, John Westbrook, John M.C. Ionides and
Ernest D. Laue (2005). A framework for scientific data modeling and
automated software development. Bioinformatics 21, 1678-1684.
===========================REFERENCE END===============================

"""
from ccpnmodel.util import Conversion

__author__ = 'rhf22'

versionSequence = ['2.0.a0', '2.0.a1', '2.0.a2', '2.0.a3', '2.0.b1', '2.0.b2', '2.0.b3']
# NBNB version 2.0.6 is a side branch, not on the main version sequence

emptyDict = {}
emptyList = []

# guids of elements that should be treated as old
# Must be kept out of map fixing till the last, as they break it.
elemsTreatedAsOld = set((
 'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:52_00002', # spectrumWindowPanes
 'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:52_00008',
 'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:52_00006',
 'www.ccpn.ac.uk_Fogh_2008-09-24-15:20:52_00004'
))

# pairs of element guids that should be treated as matching, e.g. when
# a single element must match with several elements in subclasses
elementPairings = []

def extraMapChanges(globalMapping):
  """ Extra map changes specific for a given step
  """

  dd = globalMapping.get('ANAL')
  if dd is not None:
    ANALmapChanges(globalMapping)

  # Set links Nmr -> nmrExpPrototype to delayed
  for guid in ('www.ccpn.ac.uk_Fogh_2006-08-16-18:20:06_00008',
   'www.ccpn.ac.uk_Fogh_2006-08-16-18:23:00_00002',
   'www.ccpn.ac.uk_Fogh_2006-08-16-18:20:05_00025'
  ):
    globalMapping['mapsByGuid'][guid]['proc'] = 'delay'


def ANALmapChanges(globalMapping):
  """ changes for ANAL (ccpnmr.Analysis) package
  """

  # make changes for SpectrumWindow -> SpectrumWindowPane split
  # attributes that belong to SpectrumWindow are copied to
  # SpectrumWindowPane and set to 'delay'
  # they are attached to the actual SpectrumWindowPane, and
  # copied up to the proper location in SpectrumWindow by postprocessing
  loadMaps = globalMapping['loadMaps']
  SpWinMap = loadMaps['ANAL.SpectrumWindow']
  SpWinContent = SpWinMap['content']
  SpPaneMap = loadMaps['ANAL.SpectrumWindowPane']
  SpPaneContent = SpPaneMap['content']

  # copy maps from Window to WindowPane and set proc to delay
  ll = SpWinMap['headerAttrs'] + SpWinMap['simpleAttrs'] + SpWinMap['cplxAttrs']
  ll.remove('name')
  ll.remove('access')
  ll.remove('applicationData')

  for tag in ll:
    dd = SpWinContent[tag]
    dd['proc'] = 'delay'
    SpPaneContent[tag] = dd

  # set proc to skip for link into SpectrumWindow
  dd = loadMaps['ANAL.SpectrumWindowGroup']
  dd['content']['spectrumWindows']['proc'] = 'skip'

  # set custom constructor
  SpWinMap['constructor'] = constructWindowAndPane

  # copy WinPane attributes to Win
  aDict = {
   'headerAttrs':['aspectRatio'],
   'simpleAttrs':['sliceRange'],
   'cplxAttrs':['spectrumWindowViews', 'slicePanels', 'axisPanels']
  }
  for ss in ('headerAttrs', 'simpleAttrs', 'cplxAttrs'):
    ll = aDict[ss]
    SpWinMap[ss].extend(ll)
    for tag in ll:
      SpWinContent[tag] = SpPaneContent[tag]
      loadMaps['ANAL.SpectrumWindow.%s' % tag] = (
        loadMaps['ANAL.SpectrumWindowPane.%s' % tag])
  SpWinMap['children'].extend(aDict['cplxAttrs'])


  # disable child link setting to SpectrumWindow
  dd = globalMapping['loadMaps']['ANAL.AnalysisProject']
  dd['children'].remove('spectrumWindows')
  #
  return


def constructWindowAndPane(analysisProject):
  """ Special constructor.
  Creates both SpectrumWindow and SpectrumWindowPane
  Called for the slot fo the former but returns the latter
  """
  spectrumWindow = analysisProject.newSpectrumWindow()
  spectrumWindowPane = spectrumWindow.newSpectrumWindowPane(serial=1)
  return spectrumWindowPane


def correctData(topObj, delayDataDict, toNewObjDict, mapping=None):
  """ update topObj object tree using information in delayDataDict
  May be used either to postprocess a file load (minor upgrade)
  or as part of an in-memory data transfer (major upgrade)

  topObj is the MemopsRoot in the new tree
  toNewObjDict is _ID:newObj for minor
    and oldObj/oldObjId:newObj for major upgrades
  """

  pName = topObj.packageName

  if pName == 'ccpnmr.Analysis':
    fixAnalysis(topObj, delayDataDict, toNewObjDict, mapping)
  #
  elif pName == 'ccp.nmr.Nmr':
    # Fix Nmr
    fixNmr(topObj, delayDataDict)
  #


def fixNmr(topObj, delayDataDict):
  """ remap defunct RefExperiment
  """
  doGet = delayDataDict.get

  memopsRoot = topObj.parent
  topObjByGuid = memopsRoot.__dict__.get('topObjects')

  for xpr in doGet(topObj, emptyDict).get('experiments', emptyList):
    expDict = doGet(xpr, emptyDict)

    # fix NmrExpPrototype mapping for defunct types
    Conversion.setNmrExpPrototypeLink(xpr, 'refExperiment', topObjByGuid, delayDataDict,
                           remapPrototypeLink)
    for xd in expDict.get('expDims', emptyList):
      Conversion.setNmrExpPrototypeLink(xd, 'refExpDim', topObjByGuid, delayDataDict,
                             remapPrototypeLink)
      for xdr in doGet(xd, emptyDict).get('expDimRefs', emptyList):
        Conversion.setNmrExpPrototypeLink(xdr, 'refExpDimRef', topObjByGuid, delayDataDict,
                               remapPrototypeLink)


def remapPrototypeLink(keyList):

  guid = keyList[0]

  # map to different keys
  if guid == 'cam_wb104_2008-01-15-16-06-39_00031':
    # 'H[N[CA[HA]]] removed RefExperiment - change to correct version
    if keyList[1] == 4:
      keyList[1] = 8


def fixAnalysis(topObj, delayDataDict, toNewObjDict, mapping):
  """ The spectrumWindows slot actually contains spectrumWindowPanes
  With the attributes of the SpectrunmWindow put in as 'delay'
  The fixing function puts the delayed attributes in the right place
  rearranges the delayDataDict to be read correctly when setting child
  links later, and sets child links from SpectrumWIndow down
  """

  simpleAttrs = ['isCanvasLabelShown', 'isCanvasMidpointShown', 'isIconified',
                 'isXSliceDrawn', 'isXTickShown', 'isYSliceDrawn',
                 'isYTickShown', 'serial', 'stripAxis', 'useMultiplePeakLists',
                 'useOverrideRegion']

  doGet = delayDataDict.get

  dd = doGet(topObj, emptyDict)

  spectrumWindows = dd.get('spectrumWindows', emptyList)
  for swp in spectrumWindows:   # really SpectrumWindowPanes

    # get next dictionary
    swpdd = doGet(swp, emptyDict)

    # get SpectrumWindow
    sw = swp.spectrumWindow
    swdict = sw.__dict__

    # fill in delayDataDict
    delayDataDict[sw] = {'spectrumWindowPanes':[swp]}

    # fix SpectrumWindow.name
    swdict['name'] = swp.name

    # set simple hicard==1 attrs:
    for tag in simpleAttrs:
      vals = swpdd.get(tag)
      if vals:
        setattr(sw, tag, vals[0])

    # set location
    tag = 'location'
    vals = swpdd.get(tag)
    if vals:
      setattr(sw, tag, vals)

    # set spectrumWindowGroups crosslink
    tag = 'spectrumWindowGroups'
    vals = swpdd.get(tag)
    if vals:
      setattr(sw, tag, [toNewObjDict.get(x) for x in vals])

    # set children, recursively
    from ccpncore.xml.memops.Implementation import linkChildData
    linkChildData(delayDataDict, sw, mapping, linkTopToParent=2)