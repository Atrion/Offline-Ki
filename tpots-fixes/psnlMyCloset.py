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
from PlasmaKITypes import *
from PlasmaNetConstants import *
import PlasmaControlKeys
import string
actClosetOpen = ptAttribActivator(1, 'Open Activator')
respClosetOpen = ptAttribResponder(2, 'Open Responder', netForce=1)
actClosetClose = ptAttribActivator(3, 'Close Activator')
respClosetClose = ptAttribResponder(4, 'Close Responder', netForce=1)
objOpenClosetBlockers = ptAttribSceneobjectList(9, 'Door Blockers')
kSDLClosetClosed = 'psnlClosetClosed'
boolAmOwner = false
AgeStartedIn = None
kCloseClosetTimer = 99
kVisitorDisableTimer = 100

class psnlMyCloset(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5016
        self.version = 6


    def __del__(self):
        pass


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()


    def OnServerInitComplete(self):
        global boolAmOwner
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(kSDLClosetClosed, 1, 1)
            ageSDL.sendToClients(kSDLClosetClosed)
            ageSDL.setNotify(self.key, kSDLClosetClosed, 0.0)
            vault = ptVault()
            if vault.amOwnerOfCurrentAge():
                boolAmOwner = true
                PtDebugPrint('psnlCloset.OnServerInitComplete():\tWelcome Home!')
                try:
                    closetClosed = ageSDL[kSDLClosetClosed][0]
                except:
                    PtDebugPrint('psnlCloset.OnServerInitComplete():\tERROR reading SDL from vault, defaulting to closed (fastforward)')
                    self.ICloseCloset(1)
                if (not closetClosed):
                    PtDebugPrint('psnlCloset.OnServerInitComplete():\tCloset is open, so setting a timer to close it')
                    self.IOpenCloset(1)
                    PtAtTimeCallback(self.key, 2, kCloseClosetTimer)
                else:
                    PtDebugPrint('psnlCloset.OnServerInitComplete():\tCloset is closed, making sure the geometry matches')
                    self.ICloseCloset(1)
            else:
                PtDebugPrint('psnlCloset.OnServerInitComplete():\tWelcome Visitor')
                PtAtTimeCallback(self.key, 1, kVisitorDisableTimer)
                try:
                    closetClosed = ageSDL[kSDLClosetClosed][0]
                except:
                    PtDebugPrint('psnlCloset.OnServerInitComplete():\tERROR reading SDL from vault, defaulting closed')
                    closetClosed = true
                if (not closetClosed):
                    self.IOpenCloset(1)
                else:
                    self.ICloseCloset(1)
        return


    def IOpenCloset(self, ff = 0, events = None):
        vault = ptVault()
        respClosetOpen.run(self.key, fastforward=ff, events=events)
        if vault.amOwnerOfCurrentAge():
            ageSDL = PtGetAgeSDL()
            ageSDL.setTagString(kSDLClosetClosed, 'ignore')
            ageSDL[kSDLClosetClosed] = (0,)
        actClosetOpen.disable()
        for obj in objOpenClosetBlockers.value:
            obj.physics.suppress(false)


    def ICloseCloset(self, ff = 0, events = None):
        vault = ptVault()
        respClosetClose.run(self.key, fastforward=ff, events=events)
        if vault.amOwnerOfCurrentAge():
            ageSDL = PtGetAgeSDL()
            ageSDL.setTagString(kSDLClosetClosed, 'ignore')
            ageSDL[kSDLClosetClosed] = (1,)
        actClosetOpen.enable()
        for obj in objOpenClosetBlockers.value:
            obj.physics.suppress(true)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname == kSDLClosetClosed):
            if (AgeStartedIn == PtGetAgeName()):
                ageSDL = PtGetAgeSDL()
                PtDebugPrint(('psnlClosetDoor.OnSDLNotify():\t VARname:%s, SDLname:%s, tag:%s, value:%d, playerID:%d' % (VARname, SDLname, tag, ageSDL[VARname][0], playerID)))
            if (tag == 'ignore'):
                return
            else:
                PtDebugPrint('psnlClosetDoor.OnSDLNotify():\ttag not ignore, ignoring anyway :P')
                return


    def OnNotify(self, state, id, events):
        if ((id == actClosetOpen.id) and state):
            if (AgeStartedIn == PtGetAgeName()):
                self.IOpenCloset(events=events)
        elif ((id == respClosetOpen.id) and state):
            if PtWasLocallyNotified(self.key):
                self.ILinkToACA()

    def OnTimer(self, id):
        if (id == kCloseClosetTimer):
            self.ICloseCloset()
        elif (id == kVisitorDisableTimer):
            actClosetOpen.disable()
            actClosetClose.disable()


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            self.IExitCloset(false)
            return


    def ILinkToACA(self):
        # BEGIN DarkFalkon's 1st/3rd person patch
        cam = ptCamera()
        cam.undoFirstPerson()
        cam.disableFirstPersonOverride()
        # END DarkFalkon's 1st/3rd person patch
        PtDisableControlKeyEvents(self.key)
        PtSendKIMessage(kDisableKIandBB, 0)
        PtDisableMovementKeys()
        ageLink = ptAgeLinkStruct()
        ageInfo = ageLink.getAgeInfo()
        temp = ptAgeInfoStruct()
        temp.copyFrom(ageInfo)
        ageInfo = temp
        ageInfo.setAgeFilename('AvatarCustomization')
        ageLink.setAgeInfo(ageInfo)
        ageLink.setLinkingRules(PtLinkingRules.kOriginalBook)
        linkmgr = ptNetLinkingMgr()
        linkmgr.linkToAge(ageLink)


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



