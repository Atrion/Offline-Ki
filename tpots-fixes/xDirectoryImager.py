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
ImagerMap = ptAttribDynamicMap(1, 'The Dynamic Texture Map')
ImagerTime = ptAttribInt(2, 'Number of seconds on each image', default=30)
ImagerDir = ptAttribString(3, 'Name of images directory')
EnabledVar = ptAttribString(4, 'Enabled SDL variable')
EnabledStates = ptAttribString(5, 'Enabled states', default='1')
CurrentImageName = ''
NumFiles = 0
kFlipImagesTimerStates = 5
kFlipImagesTimerCurrent = 0
IgnoreTimer = 0
CurrentState = 0
Instance = None
Disable = False

class xDirectoryImager(ptModifier):


    def __init__(self):
        global Instance
        ptModifier.__init__(self)
        Instance = self
        self.id = 5326
        self.version = 2
        self.enabledStateList = []
        self.initComplete = 0
        PtDebugPrint(('xDirectoryImager: init  version = %d' % self.version))
        if PtGetAgeName() == 'Personal' and os.path.exists('dat/Personal_District_psnlDustAdditions.prp'):
            global Disable
            Disable = True
            PtDebugPrint('xDirectoryImager is disabled because there is a MOUL imager')


    def AvatarPage(self, avObj, pageIn, lastOut):
        if (not pageIn):
            print 'clearing timer callbacks to me'
            PtClearTimerCallbacks(self.key)


    def OnFirstUpdate(self):
        if Disable: return
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        if ((type(EnabledStates.value) == type('')) and (EnabledStates.value != '')):
            try:
                self.enabledStateList = EnabledStates.value.split(',')
                for i in range(len(self.enabledStateList)):
                    self.enabledStateList[i] = int(self.enabledStateList[i].strip())
            except:
                PtDebugPrint("ERROR: xDirectoryImager.OnFirstUpdate():\tERROR: couldn't process start state list")


    def OnServerInitComplete(self):
        if Disable: return
        global CurrentState
        if (type(ImagerMap.textmap) == type(None)):
            PtDebugPrint('xDirectoryImager:ERROR! simpleImager: Dynamic textmap is broken!', level=kErrorLevel)
            return
        elif (type(ImagerDir.value) == type(None)):
            PtDebugPrint('xDirectoryImager:ERROR! simpleImager: no directory specified', level=kErrorLevel)
            return
        elif (not (os.access(ImagerDir.value, os.F_OK))):
            PtDebugPrint('xDirectoryImager:ERROR! simpleImager: Couldn\'t find the directory...creating', level=kErrorLevel)
            os.mkdir(ImagerDir.value)
        if ((type(EnabledVar.value) == type('')) and (EnabledVar.value != '')):
            print 'DirectoryImager has a good enabled var'
            ageSDL = PtGetAgeSDL()
            ageSDL.setNotify(self.key, EnabledVar.value, 0.0)
            CurrentState = ageSDL[EnabledVar.value][0]
            if (CurrentState in self.enabledStateList):
                enabled = 1
            else:
                enabled = 0
        else:
            enabled = 1
        if enabled:
            self.NextImage()
            PtAtTimeCallback(self.key, ImagerTime.value, kFlipImagesTimerCurrent)
        self.initComplete = 1


    def OnSDLNotify(self, VARname, SDLname, PlayerID, tag):
        if Disable: return
        global IgnoreTimer
        global CurrentState
        if (not (self.initComplete)):
            return
        if (VARname == EnabledVar.value):
            ageSDL = PtGetAgeSDL()
            if (ageSDL[EnabledVar.value][0] in self.enabledStateList):
                if (not (CurrentState in self.enabledStateList)):
                    IgnoreTimer = 0
                    self.NextImage()
                    PtAtTimeCallback(self.key, ImagerTime.value, kFlipImagesTimerCurrent)
            else:
                IgnoreTimer = 1
                ImagerMap.textmap.purgeImage()
            CurrentState = ageSDL[EnabledVar.value][0]


    def OnTimer(self, id):
        if IgnoreTimer:
            return
        if (id == kFlipImagesTimerCurrent):
            if self.NextImage():
                PtAtTimeCallback(self.key, ImagerTime.value, kFlipImagesTimerCurrent)
            else:
                PtAtTimeCallback(self.key, 0.10000000000000001, kFlipImagesTimerCurrent)


    def FileCmp(self, x, y):
        return cmp(os.stat(((ImagerDir.value + '\\') + y)).st_ctime, os.stat(((ImagerDir.value + '\\') + x)).st_ctime)


    def NextImage(self):
        global CurrentImageName
        global NumFiles
        dirlist = os.listdir(ImagerDir.value)
        filelist = []
        for f in dirlist:
            if ((f[-4:].lower() == '.jpg') or (f[-5:].lower() == '.jpeg')):
                filelist.append(f)
        filelist.sort(self.FileCmp)
        cur_numfiles = len(filelist)
        if (cur_numfiles <= 0):
            PtDebugPrint("xDirectoryImager.NextImage: Sorry but there are no images in the directory so I'm not updating.")
            return 1
        if (cur_numfiles != NumFiles):
            curIndex = 0
            NumFiles = cur_numfiles
        else:
            try:
                curIndex = (filelist.index(CurrentImageName) + 1)
            except ValueError:
                curIndex = 0
        if (curIndex >= len(filelist)):
            curIndex = 0
        CurrentImageName = filelist[curIndex]
        PtDebugPrint(('Trying to display: %s' % CurrentImageName), level=kDebugDumpLevel)
        theImage = PtLoadJPEGFromDisk(((ImagerDir.value + '\\') + CurrentImageName), 800, 600)
        if theImage:
            ImagerMap.textmap.drawImage(0, 0, theImage, 0)
            ImagerMap.textmap.flush()
        else:
            return 0
        return 1


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



