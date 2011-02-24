# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    This is a patched file that was originally written by Cyan Worlds Inc.    #
#    See the file AUTHORS for more info about the contributors of the changes  #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                      #
#                                                                              #
#    You may re-use the code in this file within the context of Uru.           #
#                                                                              #
#==============================================================================#
from Plasma import *
from PlasmaTypes import *
import os
import glob
actTrigger = ptAttribActivator(1, 'Triggerer')
respOneShot = ptAttribResponder(2, 'Oneshot resp')
respStart = ptAttribResponder(3, 'Start responder')
respStop = ptAttribResponder(4, 'Stop responder')
soSoundObj = ptAttribSceneobject(5, 'Sound sceneobject')
strPath = ptAttribString(6, 'File path')
strSoundObj = ptAttribString(7, 'Sound component name')
CurrentFile = None
SoundObjIndex = 0
IsPlaying = 0
InitialSongName = 'sfx/psnlMusicPlayer.ogg'
sdlCurrentSongVar = 'psnlMusicBoxCurrentSong'

class xMusicBox(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5329
        self.version = 1
        PtDebugPrint(('xMusicBox: init  version = %d' % self.version))


    def OnServerInitComplete(self):
        global SoundObjIndex
        if (not (os.access(strPath.value, os.F_OK))):
            PtDebugPrint('xMusicBox:ERROR! simpleImager: Couldn\'t find the directory...creating', level=kErrorLevel)
            os.mkdir(strPath.value)
        SoundObjIndex = soSoundObj.value.getSoundIndex(strSoundObj.value)
        PtDebugPrint(('xMusicBox.OnServerInitComplete: using sound object index:' + str(SoundObjIndex)))
        self.InitMusicBoxSongList()
        # check for current song
        ageSDL = PtGetAgeSDL()
        filename = ageSDL[sdlCurrentSongVar][0]
        if (len(filename) > 4):
            self.PlaySong(filename)


    def OnNotify(self, state, id, events):
        global IsPlaying
        if (not (state)):
            return
        if (id == actTrigger.id):
            respOneShot.run(self.key, events=events)
        elif (id == respOneShot.id):
            if IsPlaying:
                respStop.run(self.key)
                # this will trigger the respStart event and switch to the next song
            else:
                # no song currently running, start the next one
                self.NextSong()
        elif (id == respStart.id):
            # respStart is triggered when a song ends, or respStop is called
            IsPlaying = 0 # the song is over
            self.NextSong() # go to the next one


    def FileCmp(self, x, y):
        return cmp(os.stat(y).st_ctime, os.stat(x).st_ctime)
    
    
    def PlaySong(self, filename):
        # This assuems that currently, no song is playing and IsPlaying is 0
        global CurrentFile
        global IsPlaying
        if not os.path.exists(filename): filename = InitialSongName # make sure we play an existing song
        CurrentFile = filename
        # save song info
        if (filename[-4:].lower() == '.ogg'):
            iscompressed = 1
        else:
            iscompressed = 0
        PtDebugPrint('xMusicBox.PlaySong: Going to play: %s' % filename)
        # play song
        soSoundObj.value.setSoundFilename(SoundObjIndex, filename, iscompressed)
        IsPlaying = 1
        respStart.run(self.key)
        # save in SDL
        ageSDL = PtGetAgeSDL()
        ageSDL[sdlCurrentSongVar] = (filename,)

    def NextSong(self):
        # This assuems that currently, no song is playing and IsPlaying is 0
        global CurrentFile
        # get list of songs
        wavlist = glob.glob((strPath.value + '/*.wav'))
        ogglist = glob.glob((strPath.value + '/*.ogg'))
        filelist = (wavlist + ogglist)
        filelist.sort(self.FileCmp)
        if not len(filelist): # the folder is empty, use list saved in the vault
            filelist = self.GetMusicBoxSongList()
        if not len(filelist): # make sure we have at least one song
            filelist = [InitialSongName,]
        # get next song index
        curIndex = 0 # per default, start from scratch
        try:
            if CurrentFile: curIndex = (filelist.index(CurrentFile) + 1)
        except ValueError: pass # song not found
        if (curIndex >= len(filelist)): # after last song, make pause
            curIndex = -1
        # apply song
        if curIndex >= 0: # there is a next song, play it
            self.PlaySong(filelist[curIndex])
        else: # playlist finished
            PtDebugPrint('xMusicBox.NextSong: Stopping')
            CurrentFile = None
            # save that we do not play anything next time
            ageSDL = PtGetAgeSDL()
            ageSDL[sdlCurrentSongVar] = ("",)


    def InitMusicBoxSongList(self):
        musicBoxChronFound = 0
        ageDataFolder = None
        ageVault = ptAgeVault()
        ageInfoNode = ageVault.getAgeInfo()
        ageInfoChildren = ageInfoNode.getChildNodeRefList()
        for ageInfoChildRef in ageInfoChildren:
            ageInfoChild = ageInfoChildRef.getChild()
            folder = ageInfoChild.upcastToFolderNode()
            if (folder and (folder.folderGetName() == 'AgeData')):
                ageDataFolder = folder
                ageDataChildren = folder.getChildNodeRefList()
                for ageDataChildRef in ageDataChildren:
                    ageDataChild = ageDataChildRef.getChild()
                    chron = ageDataChild.upcastToChronicleNode()
                    if (chron and (chron.getName() == 'MusicBoxSongs')):
                        musicBoxChronFound = 1
        # create what's missing
        if (not ageDataFolder):
            newFolder = ptVaultFolderNode(0)
            newFolder.folderSetName('AgeData')
            ageInfoNode.addNode(newFolder)
            # add the chronicle with a timer - we have to wait till we got the new folder ID from the vault
            PtAtTimeCallback(self.key, 0.5, 0)
        elif (not musicBoxChronFound):
            newNode = ptVaultChronicleNode(0)
            newNode.chronicleSetName('MusicBoxSongs')
            newNode.chronicleSetValue(InitialSongName)
            ageDataFolder.addNode(newNode)


    def OnTimer(self, id):
        self.InitMusicBoxSongList()


    def GetMusicBoxSongList(self):
        ageVault = ptAgeVault()
        ageInfoNode = ageVault.getAgeInfo()
        ageInfoChildren = ageInfoNode.getChildNodeRefList()
        for ageInfoChildRef in ageInfoChildren:
            ageInfoChild = ageInfoChildRef.getChild()
            folder = ageInfoChild.upcastToFolderNode()
            if (folder and (folder.folderGetName() == 'AgeData')):
                ageDataChildren = folder.getChildNodeRefList()
                for ageDataChildRef in ageDataChildren:
                    ageDataChild = ageDataChildRef.getChild()
                    chron = ageDataChild.upcastToChronicleNode()
                    if (chron and (chron.getName() == 'MusicBoxSongs')):
                        return chron.getValue().split(';')
        PtDebugPrint("Error: No music box list found")
        return []


glue_cl = None
glue_inst = None
glue_params = None
glue_paramKeys = None
try:
    x = glue_verbose
except NameError:
    glue_verbose = 0

def glue_getClass():
    global glue_cl
    if (glue_cl == None):
        try:
            cl = eval(glue_name)
            if issubclass(cl, ptModifier):
                glue_cl = cl
            elif glue_verbose:
                print ('Class %s is not derived from modifier' % cl.__name__)
        except NameError:
            if glue_verbose:
                try:
                    print ('Could not find class %s' % glue_name)
                except NameError:
                    print 'Filename/classname not set!'
    return glue_cl


def glue_getInst():
    global glue_inst
    if (type(glue_inst) == type(None)):
        cl = glue_getClass()
        if (cl != None):
            glue_inst = cl()
    return glue_inst


def glue_delInst():
    global glue_inst
    global glue_cl
    global glue_params
    global glue_paramKeys
    if (type(glue_inst) != type(None)):
        del glue_inst
    glue_cl = None
    glue_params = None
    glue_paramKeys = None


def glue_getVersion():
    inst = glue_getInst()
    ver = inst.version
    glue_delInst()
    return ver


def glue_findAndAddAttribs(obj, glue_params):
    if isinstance(obj, ptAttribute):
        if glue_params.has_key(obj.id):
            if glue_verbose:
                print 'WARNING: Duplicate attribute ids!'
                print ('%s has id %d which is already defined in %s' % (obj.name, obj.id, glue_params[obj.id].name))
        else:
            glue_params[obj.id] = obj
    elif (type(obj) == type([])):
        for o in obj:
            glue_findAndAddAttribs(o, glue_params)
    elif (type(obj) == type({})):
        for o in obj.values():
            glue_findAndAddAttribs(o, glue_params)
    elif (type(obj) == type(())):
        for o in obj:
            glue_findAndAddAttribs(o, glue_params)


def glue_getParamDict():
    global glue_params
    global glue_paramKeys
    if (type(glue_params) == type(None)):
        glue_params = {}
        gd = globals()
        for obj in gd.values():
            glue_findAndAddAttribs(obj, glue_params)
        glue_paramKeys = glue_params.keys()
        glue_paramKeys.sort()
        glue_paramKeys.reverse()
    return glue_params


def glue_getClassName():
    cl = glue_getClass()
    if (cl != None):
        return cl.__name__
    if glue_verbose:
        print ('Class not found in %s.py' % glue_name)
    return None


def glue_getBlockID():
    inst = glue_getInst()
    if (inst != None):
        return inst.id
    if glue_verbose:
        print ('Instance could not be created in %s.py' % glue_name)
    return None


def glue_getNumParams():
    pd = glue_getParamDict()
    if (pd != None):
        return len(pd)
    if glue_verbose:
        print ('No attributes found in %s.py' % glue_name)
    return 0


def glue_getParam(number):
    global glue_paramKeys
    pd = glue_getParamDict()
    if (pd != None):
        if (type(glue_paramKeys) == type([])):
            if ((number >= 0) and (number < len(glue_paramKeys))):
                return pd[glue_paramKeys[number]].getdef()
            else:
                print ('glue_getParam: Error! %d out of range of attribute list' % number)
        else:
            pl = pd.values()
            if ((number >= 0) and (number < len(pl))):
                return pl[number].getdef()
            elif glue_verbose:
                print ('glue_getParam: Error! %d out of range of attribute list' % number)
    if glue_verbose:
        print 'GLUE: Attribute list error'
    return None


def glue_setParam(id, value):
    pd = glue_getParamDict()
    if (pd != None):
        if pd.has_key(id):
            try:
                pd[id].__setvalue__(value)
            except AttributeError:
                if isinstance(pd[id], ptAttributeList):
                    try:
                        if (type(pd[id].value) != type([])):
                            pd[id].value = []
                    except AttributeError:
                        pd[id].value = []
                    pd[id].value.append(value)
                else:
                    pd[id].value = value
        elif glue_verbose:
            print 'setParam: can\'t find id=',
            print id
    else:
        print 'setParma: Something terribly has gone wrong. Head for the cover.'


def glue_isNamedAttribute(id):
    pd = glue_getParamDict()
    if (pd != None):
        try:
            if isinstance(pd[id], ptAttribNamedActivator):
                return 1
            if isinstance(pd[id], ptAttribNamedResponder):
                return 2
        except KeyError:
            if glue_verbose:
                print ('Could not find id=%d attribute' % id)
    return 0


def glue_isMultiModifier():
    inst = glue_getInst()
    if isinstance(inst, ptMultiModifier):
        return 1
    return 0


def glue_getVisInfo(number):
    global glue_paramKeys
    pd = glue_getParamDict()
    if (pd != None):
        if (type(glue_paramKeys) == type([])):
            if ((number >= 0) and (number < len(glue_paramKeys))):
                return pd[glue_paramKeys[number]].getVisInfo()
            else:
                print ('glue_getVisInfo: Error! %d out of range of attribute list' % number)
        else:
            pl = pd.values()
            if ((number >= 0) and (number < len(pl))):
                return pl[number].getVisInfo()
            elif glue_verbose:
                print ('glue_getVisInfo: Error! %d out of range of attribute list' % number)
    if glue_verbose:
        print 'GLUE: Attribute list error'
    return None



