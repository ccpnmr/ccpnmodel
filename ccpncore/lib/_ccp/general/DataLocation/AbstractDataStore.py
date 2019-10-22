"""Functions for insertion into ccp.general.DataLocation.AbstractDataStore

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:10 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.0 $"
#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: rhf22 $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import os
from ccpn.util import Path
from ccpnmodel.ccpncore.api.memops import Implementation


def forceChangeDataStoreUrl(self: 'AbstractDataStore', newPath: str):
    """ Change the url for this dataStore, so that the end we have
    dataStore.dataUrl.url.path = newPath.  This changes all dataUrls
    with the same old path if the old path does not exist and the
    new one does.
    """

    newPath = Path.normalisePath(newPath, makeAbsolute=True)
    oldDataUrl = self.dataUrl
    oldUrl = oldDataUrl.url
    oldPath = oldUrl.dataLocation
    if newPath != oldPath:
        dataLocationStore = self.dataLocationStore

        # newUrl = Implementation.Url(path=newPath)  # TBD: should use oldUrl.clone(path=newPath)
        newUrl = oldUrl.clone(path=newPath)

        # first check if have a dataUrl with this path
        newDataUrl = dataLocationStore.findFirstDataUrl(url=newUrl)
        if not newDataUrl:
            newDataUrl = dataLocationStore.newDataUrl(name=oldDataUrl.name, url=newUrl)
            self.dataUrl = newDataUrl
            repointToDataUrl(self, newDataUrl)
            # oldDataUrl.delete()

            return newDataUrl

def changeDataStoreUrl(self: 'AbstractDataStore', newPath: str):
    """ Change the url for this dataStore, so that the end we have
    dataStore.dataUrl.url.path = newPath.  This changes all dataUrls
    with the same old path if the old path does not exist and the
    new one does.
    """

    newPath = Path.normalisePath(newPath, makeAbsolute=True)
    oldDataUrl = self.dataUrl
    oldUrl = oldDataUrl.url
    oldPath = oldUrl.dataLocation
    oldExists = os.path.exists(oldPath)
    if newPath != oldPath:
        dataLocationStore = self.dataLocationStore
        newUrl = Implementation.Url(path=newPath)  # TBD: should use oldUrl.clone(path=newPath)

        # first check if have a dataUrl with this path
        newDataUrl = dataLocationStore.findFirstDataUrl(url=newUrl)
        if not newDataUrl:
            # if old path exists and there is more than one dataStore with
            # this dataUrl then create new one
            dataUrlStores = dataLocationStore.findAllDataStores(dataUrl=oldDataUrl)
            if oldExists and len(dataUrlStores) > 1:
                newDataUrl = dataLocationStore.newDataUrl(name=oldDataUrl.name, url=newUrl)

        # if have found or have created newDataUrl then set dataStore to point to it
        # else just change url of oldDataUrl (which could affect other dataStores)
        if newDataUrl:
            self.dataUrl = newDataUrl
        else:
            oldDataUrl.url = newUrl

        # if old path does not exist and new path exists then change urls of
        # all data urls which have old path to new path (there might be none)
        if not oldExists:
            newExists = os.path.exists(newPath)
            if newExists:
                for dataUrl in dataLocationStore.dataUrls:
                    if dataUrl.url == oldUrl:
                        dataUrl.url = newUrl


def repointToDataUrl(self: 'AbstractDataStore', dataUrl: 'DataUrl'):
    """Set self.datUrl=dataUrl, AND move self to newDataLocationStore first if necessary"""
    dataLocationStore = dataUrl.dataLocationStore
    oldDataUrl = self.dataUrl
    oldDataLocationStore = oldDataUrl.dataLocationStore
    undo = self.root._undo
    if undo is not None:
        undo.increaseBlocking()
    try:
        if oldDataUrl is dataUrl:
            return
        elif oldDataLocationStore is dataLocationStore:
            self.dataUrl = dataUrl
        else:
            # We need to move self to a new DataLocationStore. This bypasses the API

            # First load NmrProjects and set to modified
            # - necessary to avoid broken exoLinks in non-loaded files
            for topObject in set(x.topObject for x in self.nmrDataSources):
                if not topObject.isLoaded:
                    topObject.load()
                topObject.touch()

            # get data set up
            oldSerial = newSerial = self.serial
            serialDict = dataLocationStore.__dict__['_serialDict']
            previousDataStore = dataLocationStore.findFirstDataStore(serial=oldSerial)
            if previousDataStore is not None:
                newSerial = serialDict['dataStores'] + 1

            del oldDataLocationStore.__dict__['dataStores'][oldSerial]
            self.__dict__['dataLocationStore'] = self.__dict__['topObject'] = dataLocationStore
            if newSerial != oldSerial:
                self.__dict__['serial'] = newSerial
            if newSerial > serialDict['dataStores']:
                serialDict['dataStores'] = newSerial
            dataLocationStore.__dict__['dataStores'][newSerial] = self
            self.dataUrl = dataUrl

            self.root.override = True
            try:
                self.set_ID(-1)
            finally:
                self.root.override = False

    finally:
        # reset override and set isModified
        # root.__dict__['override'] = False
        # self.__dict__['isModified'] = True
        if undo is not None:
            undo.decreaseBlocking()

    if undo is not None:
        undo.newItem(self.repointToDataUrl, self.repointToDataUrl,
                     undoArgs=(oldDataUrl,), redoArgs=(dataUrl,))
