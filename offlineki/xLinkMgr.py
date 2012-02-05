# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2004-2011  The Offline KI contributors                      #
#    See the file AUTHORS for more info about the contributors (including      #
#    contact information)                                                      #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    Please see the file COPYING for the full GPLv3 license, or see            #
#    <http://www.gnu.org/licenses/>                                            #
#                                                                              #
#    Uru exception: In addition, this file may be used in combination with     #
#    (non-GPL) code within the context of Uru.                                 #
#                                                                              #
#==============================================================================#
import string
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
import os
import re
import xxConfig

_AvailableLinks = {}
_PublicLinks = []
_RestorationLinks = []

# Age datastructure and its operations
class _Age:
    def __init__(self, filename, displayName, detect = 'dataserver', linkrule = 'basic', defaultSpawnpoint = 'LinkInPointDefault'):
        self.filename = filename
        self.displayName = displayName
        self.detect = detect
        self.linkrule = linkrule
        self.defaultSpawnpoint = defaultSpawnpoint
        self.spawnpoints = {}
        self.description = ''

    def IsAvailable(self):
        if self.detect == 'disabled':
            return xxConfig.isOffline() and os.path.exists('dat\\%s.age' % self.filename)
        if self.detect == 'file' or (self.detect.startswith('dataserver') and xxConfig.isOffline()):
            return os.path.exists('dat\\%s.age' % self.filename)
        if self.detect.startswith('dataserver'): # online, obviously
            return (self.detect == 'dataserver') or (self.detect == ('dataserver('+xxConfig.shardIdentifier+')'))
        return False

    def IsBasicLinkAge(self):
        return (self.linkrule == 'basic')

    def IsOriginalBookAge(self):
        return (self.linkrule == 'original')

    # If the spawnpoint is None, use the default one. If needFullInfo is True, we need the full UUID for the age.
    def GetAgeLinkStruct(self, spawnpoint = None, needFullInfo = False):
        # check general age availability
        if not self.IsAvailable():
            return 'The age with filename \"%s\" is not available on your PC or on this Shard.' % self.filename
        # get correct spawn point
        if spawnpoint == None: spawnpoint = self.defaultSpawnpoint
        # check subage
        partnerAge = IsSubAge(PtGetAgeName()) # the name of the parent age of the current age
        if partnerAge == self.filename:
            print "xLinkMgr: Auto-detected %s (current age) to be a sub-age of %s" % (PtGetAgeName(), self.filename)
        else: # the current age is not a sub age of another age, so ignore that
            partnerAge = ''
        if not len(partnerAge): # ok, we are not linking to our parent age, but maybe we link to a sub age of ourselves?
            # check whether the destination age has a partner age
            partnerAge = IsSubAge(self.filename)
            if len(partnerAge) and partnerAge != PtGetAgeName(): # indeed we are linking to a sub age, but it's someone else's sub age!
                return 'You can not link to %s from here.' % self.displayName
        # intialize basic age link struct
        als = ptAgeLinkStruct()
        ainfo = ptAgeInfoStruct()
        ainfo.setAgeFilename(self.filename)
        ainfo.setAgeInstanceName(self.displayName)
        als.setAgeInfo(ainfo)
        # check spawnpoint and linking rule
        if (len(partnerAge) or self.IsOriginalBookAge()): # we need to verify the spawn point
            # we might need some information from the vault
            vault = ptVault()
            vinfo = ptAgeInfoStruct()
            vinfo.setAgeFilename(self.filename)
            vinfo = vault.getOwnedAgeLink(vinfo)
            if len(partnerAge):
                # either we are linking to a sub age and checked that this is indeed a sub age of the current age
                # or fromSubAge is true, and we checked that the current age is indeed a subage of the destination age
                if needFullInfo: return "Can't link to a sub-age with full info"
                als.setLinkingRules(PtLinkingRules.kSubAgeBook)
            else: # must be an original age
                if needFullInfo:
                    if vinfo == None: return "Can't link to a not-yet registered owned age with full info"
                    als = vinfo.asAgeLinkStruct()
                als.setLinkingRules(PtLinkingRules.kOriginalBook)
            # now, do the spawn point thingy
            if spawnpoint in self.spawnpoints: # we got a spawn point :)
                als.setSpawnPoint(ptSpawnPointInfo(self.spawnpoints[spawnpoint], spawnpoint))
                return als # done!
            # no spawn point specified in the linking definitions
            # let's check if that age was already linked to, and the spawn point is registered in the vault
            if vinfo != None:
                spoints = vinfo.getSpawnPoints()
                for spoint in spoints:
                    if spoint.getName().lower() == spawnpoint.lower():
                        als.setSpawnPoint(spoint) # yes, we can use it!
                        return als # done :)
            return 'Linking to spawn point %s in %s is not possible' % (spawnpoint, self.displayName) # no luck :(
        elif self.IsBasicLinkAge(): # any spawn point can be used
            als.setLinkingRules(PtLinkingRules.kBasicLink)
            als.setSpawnPoint(ptSpawnPointInfo('LinkMgrBasicLink', spawnpoint))
            return als
        else:
            return "ERROR: unable to get linkrule: %s (%s)"  % (self.filename, self.linkrule)


# Code for collecting available ages
def _AddAge(linktype, age):
    global _AvailableLinks, _RestorationLinks, _PublicLinks
    #print ('xLinkMgr: Found %s to %s' % (linktype, age.filename))
    # update Nexus link lists (iff the age is actually available)
    if linktype == 'restorationlink':
        if age.IsAvailable(): _RestorationLinks.append([age.filename, age.displayName])
    elif linktype == 'publiclink':
        if age.IsAvailable(): _PublicLinks.append([age.filename, age.displayName])
    elif linktype != 'link': # unknown link type...
        raise Exception("Unknown link type "+linktype)
    # and add the age (do this afterwards, so if the link type is invalid, you can not link here, which I will probably notice)
    _AvailableLinks[age.filename] = age


def _LoadAvailableLinks():
    global _AvailableLinks, _RestorationLinks, _PublicLinks
    if len(_AvailableLinks): # don't re-load
        return
    _AvailableLinks = {}
    _PublicLinks = []
    _RestorationLinks = []
    _LoadAvailableLinksFile('AvailableLinks.inf')
    if xxConfig.isOffline():
        _FindUnknownAges()


def _LoadAvailableLinksFile(filename):
    if not os.path.exists(filename):
        return
    f = open(filename)
    try:
        for line in f:
            # get header (type) of line and the data segments
            line = line.replace('\n', '').replace('\r', '')
            if not len(line) or line.startswith('#'): continue # skip
            pos = line.find(':')
            if pos <= 0: continue # a comment
            type = line[:pos]
            data = line[pos+1:].split(",")
            # process line
            # read include
            if type == 'include':
                if len(data) == 1:
                    _LoadAvailableLinksFile(data[0])
            # read link
            elif type.endswith('link'):
                if len(data) == 5:
                    _AddAge(type, _Age(data[0], data[1], data[2], data[3], data[4]))
                elif len(data) == 4:
                    _AddAge(type, _Age(data[0], data[1], data[2], data[3]))
                elif len(data) == 3:
                    _AddAge(type, _Age(data[0], data[1], data[2]))
                elif len(data) == 2:
                    _AddAge(type, _Age(data[0], data[1]))
            # read spawnpoint
            elif type == 'spawnpoint':
                if len(data) == 3:
                    (age, name, title) = data
                    if not age in _AvailableLinks:
                        print "ERROR: Found spawn point for unknown age "+age
                    else:
                        _AvailableLinks[age].spawnpoints[name] = title
            # read description
            elif type == 'description':
                if len(data) == 2:
                    (age, description) = data
                    if not age in _AvailableLinks:
                        print "ERROR: Found description for unknown age "+age
                    else:
                        description = description.replace(';', ',')
                        description = description.replace('\\n', '\n')
                        _AvailableLinks[age].description = description
    finally:
        f.close()


def _FindUnknownAges():
    import os
    dirList = os.listdir('dat\\')
    for fname in dirList:
        if fname[len(fname)-4:] != ".age": continue
        ageName = fname[:len(fname)-4]
        if ageName in _AvailableLinks: continue
        # found an unknown age, add it to global list and to resoration links in Nexus
        print 'Adding unknown age %s' % ageName
        _AddAge('restorationlink', ageName, _Age(ageName + " (unknown age)"))


# Public API
def ResetAvailableLinks():
    global _AvailableLinks
    _AvailableLinks = {} # the rest will be reset by _LoadAvailableLinks - but this is necessary to make sure it re-loads the file
    _LoadAvailableLinks()


def IsAgeAvailable(ageName):
    _LoadAvailableLinks()
    if not ageName in _AvailableLinks:
        print "xLinkMgr: Age %s is not available as it's not listed at all" % ageName
        return False
    return _AvailableLinks[ageName].IsAvailable()


def GetInstanceName(ageName):
    _LoadAvailableLinks()
    if not ageName in _AvailableLinks:
        return ageName
    return _AvailableLinks[ageName].displayName


def GetDescription(ageName):
    _LoadAvailableLinks()
    if not ageName in _AvailableLinks:
        return ''
    return _AvailableLinks[ageName].description


def LinkToAge(agename, spawnpoint = None):
    als = GetAgeLinkStruct(agename, spawnpoint)
    if isinstance(als, str): # an error occured
        print als
        PtSendKIMessage(kKIOKDialogNoQuit, als)
        return
    # done, go!
    linkMgr = ptNetLinkingMgr()
    linkMgr.linkToAge(als)
    print 'xLinkMgr: Linking to %s...' % agename


# If the spawnpoint is None, use the default one. If needFullInfo is True, we need the full UUID for the age.
def GetAgeLinkStruct(agename, spawnpoint = None, needFullInfo = False):
    _LoadAvailableLinks()
    if not agename in _AvailableLinks:
        return 'The age with filename \"%s\" does not exist at all.' % agename
    return _AvailableLinks[agename].GetAgeLinkStruct(spawnpoint, needFullInfo)


def IsBasicLinkAge(agename):
    _LoadAvailableLinks()
    if not agename in _AvailableLinks:
        return False
    return _AvailableLinks[agename].IsBasicLinkAge()


def IsOriginalBookAge(agename):
    _LoadAvailableLinks()
    if not agename in _AvailableLinks:
        return False
    return _AvailableLinks[agename].IsOriginalBookAge()


def IsSubAge(agename): # returns the name of the parent age, or an empty string
    _LoadAvailableLinks()
    if not agename in _AvailableLinks:
        return ''
    linkrule = _AvailableLinks[agename].linkrule
    if linkrule.startswith("subageof(") and linkrule.endswith(")"):
        return linkrule[len("subageof("):-1]
    return ''


def GetRestorationLinks():
    _LoadAvailableLinks()
    return _RestorationLinks[:] # return a copy of the list, not a reference


def GetPublicLinks():
    _LoadAvailableLinks()
    return _PublicLinks[:] # return a copy of the list, not a reference


def GetCorrectFilenameCase(age1): # takes a non-case-sensitive filename and returns the correct case, if existing
    _LoadAvailableLinks()
    for age2 in _AvailableLinks:
        if age1.lower() == age2.lower(): return age2
    return age1 # not found

def GetLinkingImage(agename, spawnpoint = None, width = 512, height = 512):
    if spawnpoint == None:
        # get default spawn point of that age (fail if the age dos not exist, that's okay)
        _LoadAvailableLinks()
        spawnpoint = _AvailableLinks[agename].defaultSpawnpoint
    files = ['img/LinkingImage_%s_%s.jpg' % (agename, spawnpoint), 'img/LinkingImage_%s.jpg' % agename, 'img/LinkingImage_Void.jpg']
    for file in files:
        if os.path.exists(file):
            return PtLoadJPEGFromDisk(file, width, height)
    raise Exception("Not even the void image exists, nothing I can do")


def DisableLinking():
    linkMgr = ptNetLinkingMgr()
    linkMgr.setEnabled(0)
    print 'xLinkMgr: Linking disabled...'


def EnableLinking():
    linkMgr = ptNetLinkingMgr()
    linkMgr.setEnabled(1)
    print 'xLinkMgr: Linking enabled...'
