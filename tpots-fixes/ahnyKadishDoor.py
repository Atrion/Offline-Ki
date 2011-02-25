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
import string
import copy
import time
import PlasmaControlKeys
SDLDoor = ptAttribString(1, 'SDL: door')
ActConsole = ptAttribActivator(2, 'clk: console')
RespConsole = ptAttribResponder(3, 'resp: console', ['enter', 'exit'])
MltStgSeek = ptAttribBehavior(4, 'Smart seek before puzzle')
ActButtons = ptAttribActivatorList(5, 'clk: list of 8 buttons')
RespButtons = ptAttribResponderList(6, 'resp: list of 8 buttons', byObject=1)
RespDoor = ptAttribResponder(7, 'resp: door ops', ['close', 'open'])
ObjButtons = ptAttribSceneobjectList(8, 'objects: list of 8 buttons')
boolDoor = 0
btnNum = 0
btnList = []
respList = []
objList = []
solutionNum = 8
solutionList = [3, 2, 1, 4, 8, 5, 6, 7]
currentList = [0, 0, 0, 0, 0, 0, 0, 0]

class ahnyKadishDoor(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5600
        self.version = 3


    def OnFirstUpdate(self):
        global btnList
        global respList
        global objList
        for button in ActButtons.value:
            tempName = button.getName()
            btnList.append(tempName)
        print 'btnList = ',
        print btnList
        for resp in RespButtons.value:
            tempResp = resp.getName()
            respList.append(tempResp)
        print 'respList = ',
        print respList
        for obj in ObjButtons.value:
            tempObj = obj.getName()
            objList.append(tempObj)
        print 'objList = ',
        print objList


    def OnServerInitComplete(self):
        PtAtTimeCallback(self.key, 0, 1)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global boolDoor
        ageSDL = PtGetAgeSDL()
        if (VARname == SDLDoor.value):
            boolDoor = ageSDL[SDLDoor.value][0]
            if boolDoor:
                RespDoor.run(self.key, state='open')
            else:
                RespDoor.run(self.key, state='close')


    def OnNotify(self, state, id, events):
        global objList
        global btnNum
        global respList
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
        if ((id == ActConsole.id) and state):
#            print 'switch to console close up'
#            ActConsole.disableActivator()
#            PtEnableControlKeyEvents(self.key)
#            avatar = PtFindAvatar(events)
#            MltStgSeek.run(avatar)
            ActConsole.disableActivator()
            if (not PtWasLocallyNotified(self.key)):
                return
            print 'switch to console close up'
            PtEnableControlKeyEvents(self.key)
            avatar = PtFindAvatar(events)
            MltStgSeek.run(avatar)
#        if (id == MltStgSeek.id):
        if ((id == MltStgSeek.id) and PtWasLocallyNotified(self.key)):
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################
            for event in events:
                if ((event[0] == kMultiStageEvent) and (event[2] == kEnterStage)):
                    avatar = PtFindAvatar(events)
                    MltStgSeek.gotoStage(avatar, -1)
                    PtDebugPrint('ahnyKadishDoor.onNotify: enter puzzle view mode now that seek is done')
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
                    #skipping invisibility, make avatar unclickable instead
#                    avatar.draw.disable()
                    PtToggleAvatarClickability(false)
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################
                    cam = ptCamera()
                    cam.disableFirstPersonOverride()
                    cam.undoFirstPerson()
                    RespConsole.run(self.key, state='enter')
                    PtAtTimeCallback(self.key, 0.5, 2)
        if ((id == ActButtons.id) and state):
            i = 0
            for btn in ActButtons.value:
                print 'ahnyKadishDoor.OnNotify: disabling 8 button clickables'
                ActButtons.value[i].disable()
                i += 1
            for event in events:
                if (event[0] == kPickedEvent):
                    xEvent = event[3]
                    btnName = xEvent.getName()
                    i = 0
                    for obj in objList:
                        if (obj == btnName):
                            btnNum = i
                            break
                        else:
                            i += 1
                    print 'btnNum =',
                    print (btnNum + 1)
                    RespButtons.run(self.key, objectName=respList[btnNum])
        if (id == RespButtons.id):
            self.ICheckButtons()
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
        #capturing notification from panel operator to all players (including him/herself)
        for event in events:
            if ((event[0] == kVariableEvent) and (event[3] == 84758)):
                print 'operator leaving console'
                self.IExitConsole()
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################


    def ICheckButtons(self):
        global btnNum
        global currentList
        global boolDoor
        print 'ahnyKadishDoor.ICheckButtons'
        ageSDL = PtGetAgeSDL()
        checkNum = (btnNum + 1)
        currentList.append(checkNum)
        while (len(currentList) > len(solutionList)):
            del currentList[0]
        print ('solution list: ' + str(solutionList))
        print ('current list: ' + str(currentList))
        if self.AreListsEquiv(solutionList, currentList):
            self.IExitConsole()
            ageSDL[SDLDoor.value] = (1,)
        elif boolDoor:
            self.IExitConsole()
            ageSDL[SDLDoor.value] = (0,)
        else:
            i = 0
            for btn in ActButtons.value:
                print 'ahnyKadishDoor.ICheckButtons: reenabling 8 button clickables'
                ActButtons.value[i].enable()
                i += 1


    def AreListsEquiv(self, list1, list2):
        if (list1[0] in list2):
            list2Copy = copy.copy(list2)
            while (list2Copy[0] != list1[0]):
                list2Copy.append(list2Copy.pop(0))
            for i in range(solutionNum):
                if (list2Copy[i] != list1[i]):
                    return false
            return true
        return false


    def OnControlKeyEvent(self, controlKey, activeFlag):
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
#        if (controlKey == PlasmaControlKeys.kKeyExitMode):
#            self.IExitConsole()
#        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
#            self.IExitConsole()
        print 'ahnyKadishDoor: controlkey event received'
        #others cannot receive control key events from the panel operator
        #so we must use another way to tell them that the panel is available again
        note = ptNotify(self.key)
        note.clearReceivers()
        note.addReceiver(self.key)
        note.setActivate(1)
        note.addVarNumber('foo', 84758)
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            try:
                note.netPropagate(1)
                note.netForce(1)
                note.send()
            except Exception, detail:
                print ('ahnyKadishDoor: could not send notify - %s' % detail)
                self.IExitConsole()
        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
            try:
                note.netPropagate(1)
                note.netForce(1)
                note.send()
            except Exception, detail:
                print ('ahnyKadishDoor: could not send notify - %s' % detail)
                self.IExitConsole()
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################


    def IExitConsole(self):
        print 'disengage and exit the console'
        i = 0
        for btn in ActButtons.value:
            print 'ahnyKadishDoor.IExitConsole: disabling 8 button clickables'
            ActButtons.value[i].disable()
            i += 1
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        PtDisableControlKeyEvents(self.key)
        RespConsole.run(self.key, state='exit')
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
        #skipping visibility, make avatar clickable instead
#        avatar = PtGetLocalAvatar()
#        avatar.draw.enable()
        PtToggleAvatarClickability(true)
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################
        PtAtTimeCallback(self.key, 0.5, 3)


    def OnTimer(self, id):
        global boolDoor
        if (id == 1):
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(SDLDoor.value, 1, 1)
            ageSDL.sendToClients(SDLDoor.value)
            ageSDL.setNotify(self.key, SDLDoor.value, 0.0)
            try:
                ageSDL = PtGetAgeSDL()
            except:
                print 'ahnyKadishDoor.OnServerInitComplete():\tERROR---Cannot find AhnySphere04 age SDL'
                ageSDL[SDLDoor.value] = (0,)
            boolDoor = ageSDL[SDLDoor.value][0]
            if boolDoor:
                RespDoor.run(self.key, state='open', fastforward=1)
            else:
                RespDoor.run(self.key, state='close', fastforward=1)
        elif (id == 2):
            i = 0
            for btn in ActButtons.value:
                print 'ahnyKadishDoor.onTimer: reenabling 8 button clickables'
                ActButtons.value[i].enable()
                i += 1
        elif (id == 3):
            print 'ahnyKadishDoor.onTimer: reenabling the console\'s clickable'
            ActConsole.enableActivator()


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



