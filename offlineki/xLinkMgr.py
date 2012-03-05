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
import os, re, time
import xxConfig, xUserKI

_AvailableLinks = {}
# this list will always be empty, it must be present for the UAM KI plugin (AgeInfo module) not to crash
_RestorationLinks = []

# sort constants
kSortByName = 0
kSortByDate = 1

# Age datastructure and its operations
class _Age:
    def __init__(self, filename, displayName, detect = 'dataserver', linkrule = 'basic', defaultSpawnpoint = 'LinkInPointDefault',
            lastUpdate = None, publicLink = False, restorationLink = False):
        self.filename = filename
        self.displayName = displayName
        self.detect = detect
        self.linkrule = linkrule
        self.defaultSpawnpoint = defaultSpawnpoint
        self.spawnpoints = {}
        self.description = ''
        self.publicLink = publicLink
        self.restorationLink = restorationLink
        self.available = self._IsAvailable() # store this information, it is not supposed to change anyway
        self._setLastUpdate(lastUpdate)
        # print
        print "xLinkMgr: Adding age %s: display=%s, public=%s, restoration=%s, available=%s" % (filename,
            displayName, str(publicLink), str(restorationLink), str(self.available))
        # warn about adding the same age twice
        if filename in _AvailableLinks:
            print "xLinkMgr: WARNING: %s was already in the age list." % self.filename
        # add us to the global list
        _AvailableLinks[filename] = self

    
    def _setLastUpdate(self, lastUpdate):
        if lastUpdate is None:
            self.lastUpdate = None
            return
        # parse YYYY-MM-DD
        m = re.search('^([0-9]{4})-([0-9]{2})-([0-9]{2})$', lastUpdate)
        if m is None: raise Exception("Invalid date %s, must be in form YYYY-MM-DD" % lastUpdate)
        # create a struct_time-sized tuple
        self.lastUpdate = (int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]), 0, 0, 0, 0, 0, 0)
    

    def _IsAvailable(self):
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
        if not self.available:
            return 'xLinkMgr: The age with filename \"%s\" is not available on your PC or on this Shard.' % self.filename
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
def _LoadAvailableLinks():
    global _AvailableLinks
    if len(_AvailableLinks): # don't re-load
        return
    # reset lists
    _AvailableLinks = {}
    # load information
    _LoadAvailableLinksFile('AvailableLinks.inf')
    _LoadPerAgeDescriptors('img/AgeInfo') # load this after the global information, so it can be overwritten
    if xxConfig.isOffline():
        _FindUnknownAges()


def _LoadPerAgeDescriptors(folder):
    if not os.path.exists(folder): return
    for file in os.listdir(folder):
        if not file.endswith(".txt"): continue # skip unininteresting files
        age = file[:-len(".txt")]
        descriptor = xUserKI.LoadConfigFile(os.path.join(folder, file)) # load default section
        defSection = descriptor['']
        displayName = defSection.get('displayName', age)
        showIn = defSection.get('showIn', 'restoration').lower()
        defaultSpawnpoint = defSection.get('defaultSpawnpoint', 'LinkInPointDefault')
        description = defSection.get('description')
        detect = defSection.get('availableVia', 'dataserver')
        link = defSection.get('link', 'basic')
        lastUpdate = defSection.get('lastUpdate')
        # create the age
        age = _Age(age, displayName=displayName, detect=detect, linkrule=link, defaultSpawnpoint=defaultSpawnpoint, lastUpdate=lastUpdate,
                restorationLink=(showIn == 'restoration'), publicLink=(showIn == 'public'))
        if description is not None: age.description = description
        # add spawn points (name-to-title mapping)
        age.spawnpoints = descriptor.get('SpawnPoints', {}) # default to no specific spawn points


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
            type = line[:pos].lower()
            data = line[pos+1:].split(",")
            # process line
            # read include
            if type == 'include':
                if len(data) == 1:
                    _LoadAvailableLinksFile(data[0])
            # read link
            elif type in ('link', 'restorationlink', 'publiclink'):
                restorationLink = (type == 'restorationlink')
                publicLink = (type == 'publiclink')
                if len(data) == 5:
                    _Age(data[0], data[1], data[2], data[3], data[4], publicLink=publicLink, restorationLink=restorationLink)
                elif len(data) == 4:
                    _Age(data[0], data[1], data[2], data[3], publicLink=publicLink, restorationLink=restorationLink)
                elif len(data) == 3:
                   _Age(data[0], data[1], data[2], publicLink=publicLink, restorationLink=restorationLink)
                elif len(data) == 2:
                    _Age(data[0], data[1], publicLink=publicLink, restorationLink=restorationLink)
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
            # complain
            else:
                raise Exception("Unknown type "+type)
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
        _Age(ageName, displayName=ageName + " (unknown age)", restorationLink=True)


def _GetAgeList(filterFunction, cmpFunction, reverse = False):
    _LoadAvailableLinks()
    ages = filter(filterFunction, _AvailableLinks.itervalues())
    ages.sort(cmpFunction)
    if reverse: ages.reverse()
    return map(lambda age: age.filename, ages) # return only filenames


def _AgeNameCmp(age1, age2):
    return cmp(age1.displayName.lower(), age2.displayName.lower())


def _AgeDateCmp(age1, age2):
    if age1.lastUpdate is None and age2.lastUpdate is None: return _AgeNameCmp(age1, age2)
    if age1.lastUpdate is None: # and age2 is not, so age2 is newer
        return 1
    if age2.lastUpdate is None: # age1 is newer
        return -1
    # both have a date, compare it
    return -cmp(age1.lastUpdate, age2.lastUpdate) # a bigger date goes further up, so reverse the order here

# Map sort-keys to compare functions
_SortBy = {
    kSortByName: _AgeNameCmp,
    kSortByDate: _AgeDateCmp,
}


# Public API
def ResetAvailableLinks():
    global _AvailableLinks
    _AvailableLinks = {} # empty the age list, it will then be re-loaded
    _LoadAvailableLinks()


def IsAgeAvailable(ageName):
    _LoadAvailableLinks()
    if not ageName in _AvailableLinks:
        print "xLinkMgr: Age %s is not available as it's not listed at all" % ageName
        return False
    return _AvailableLinks[ageName].available


def GetInstanceName(ageName):
    _LoadAvailableLinks()
    if not ageName in _AvailableLinks: # for example when the KI passes an already instanciated name to us
        return ageName
    return _AvailableLinks[ageName].displayName


def GetDescription(ageName):
    _LoadAvailableLinks()
    return _AvailableLinks[ageName].description


def GetAgeLastUpdate(ageName):
    _LoadAvailableLinks()
    return _AvailableLinks[ageName].lastUpdate


def LinkToAge(ageName, spawnpoint = None):
    als = GetAgeLinkStruct(ageName, spawnpoint)
    if isinstance(als, str): # an error occured
        print als
        PtSendKIMessage(kKIOKDialogNoQuit, als)
        return
    # done, go!
    linkMgr = ptNetLinkingMgr()
    linkMgr.linkToAge(als)
    print 'xLinkMgr: Linking to %s...' % ageName


def GetAgeLinkStruct(ageName, spawnpoint = None, needFullInfo = False):
    _LoadAvailableLinks()
    if not ageName in _AvailableLinks:
        return 'The age with filename \"%s\" does not exist at all.' % ageName
    return _AvailableLinks[ageName].GetAgeLinkStruct(spawnpoint, needFullInfo)


def IsBasicLinkAge(ageName):
    _LoadAvailableLinks()
    if not ageName in _AvailableLinks:
        return False
    return _AvailableLinks[ageName].IsBasicLinkAge()


def IsOriginalBookAge(ageName):
    _LoadAvailableLinks()
    if not ageName in _AvailableLinks:
        return False
    return _AvailableLinks[ageName].IsOriginalBookAge()


def IsSubAge(ageName): # returns the name of the parent age, or an empty string
    _LoadAvailableLinks()
    linkrule = _AvailableLinks[ageName].linkrule
    if linkrule.startswith("subageof(") and linkrule.endswith(")"):
        return linkrule[len("subageof("):-1]
    return ''


def GetRestorationAges(sortBy = kSortByName, reverse = False):
    return _GetAgeList(lambda age: age.available and age.restorationLink, _SortBy[sortBy], reverse)
# Deprecated
def GetRestorationLinks():
    return map(lambda name: (name, GetInstanceName(name)), GetRestorationAges())


def GetPublicAges(sortBy = kSortByName, reverse = False):
    return _GetAgeList(lambda age: age.available and age.publicLink, _SortBy[sortBy], reverse)
# Deprecated
def GetPublicLinks():
    return map(lambda name: (name, GetInstanceName(name)), GetPublicAges())


def GetCorrectFilenameCase(age1): # takes a non-case-sensitive filename and returns the correct case, if existing
    _LoadAvailableLinks()
    for age2 in _AvailableLinks:
        if age1.lower() == age2.lower(): return age2
    return age1 # not found


def GetLinkingImage(ageName, spawnpoint = None, width = 512, height = 512):
    if spawnpoint == None:
        # get default spawn point of that age (fail if the age dos not exist, that's okay)
        _LoadAvailableLinks()
        spawnpoint = _AvailableLinks[ageName].defaultSpawnpoint
    files = ['img/LinkingImage_%s_%s.jpg' % (ageName, spawnpoint), 'img/LinkingImage_%s.jpg' % ageName, 'img/LinkingImage_Void.jpg']
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

