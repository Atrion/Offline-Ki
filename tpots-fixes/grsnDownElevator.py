# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import cPickle
downElevTrigger = ptAttribActivator(1, 'down elevator button')
downElevStartPoint = ptAttribSceneobject(2, 'the point you start down from')
downBehavior = ptAttribBehavior(3, 'down elevator behavior')
downElevWarpPoint = ptAttribSceneobject(4, 'the point you warp to on going down')
upElevTrigger = ptAttribActivator(5, 'up elevator button')
upElevStartPoint = ptAttribSceneobject(6, 'the point you start up from')
upBehavior = ptAttribBehavior(7, 'up elevator behavior')
upElevWarpPoint = ptAttribSceneobject(8, 'the point you warp to on going up')
upElevWarpHack = ptAttribSceneobject(9, 'hack to get you where you should go')
subworld = ptAttribSceneobject(10, 'subworld')
startUpCamera = ptAttribSceneobject(11, 'up elev bottom cam')
finishUpCamera = ptAttribSceneobject(12, 'up elev top cam')
startDownCamera = ptAttribSceneobject(13, 'down elev bottom cam')
finishDownCamera = ptAttribSceneobject(14, 'down elev top cam')
exitTopCamera = ptAttribSceneobject(22, 'exit top camera')
downElevatorTopOpenAnim = ptAttribAnimation(15, 'down elevDoorOpen', 1, netForce=0)
downElevatorTopCloseAnim = ptAttribAnimation(16, 'down elevDoorClose', 1, netForce=0)
upElevatorTopOpenAnim = ptAttribAnimation(17, 'up elevDoorOpen', 1, netForce=0)
upElevatorTopCloseAnim = ptAttribAnimation(18, 'up elevDoorClose', 1, netForce=0)
downElevatorBottomTrigger = ptAttribNamedResponder(19, 'bottom down door opener', ['on', 'off'])
upElevatorBottomTrigger = ptAttribNamedActivator(20, 'bottom up elevator trigger')
upElevatorDoorTrigger = ptAttribNamedResponder(21, 'bottom up door trigger', ['on', 'off'])
upElevBotSoundDummyAnim = ptAttribAnimation(23, 'sound dummy up bottom')
upElevTopSoundDummyAnim = ptAttribAnimation(24, 'sound dummy up top')
dnElevBotSoundDummyAnim = ptAttribAnimation(25, 'sound dummy dn bottom')
dnElevTopSoundDummyAnim = ptAttribAnimation(26, 'sound dummy dn top')
upElevSDL = ptAttribString(27, 'up elevator SDL var')
dnElevSDL = ptAttribString(28, 'down elevator SDL var')
upElevatorLights = ptAttribNamedResponder(29, 'up elevator button lights', ['TurnOn', 'TurnOff'])
dnElevatorLights = ptAttribResponder(30, 'down elevator lights', ['TurnOn', 'TurnOff'])
WellTopDefaultCam = ptAttribSceneobject(31, 'well top camera')
kOpenUpElevatorTop = 1
kCloseUpElevatorTop = 2
kOpenUpElevatorBottom = 3
kCloseUpElevatorBottom = 4
kOpenDownElevatorTop = 5
kCloseDownElevatorTop = 6
kOpenDownElevatorBottom = 7
kCloseDownElevatorBottom = 8

class grsnDownElevator(ptResponder):


    def __init__(self):
        PtDebugPrint('grsnDownElevator::init begin')
        ptResponder.__init__(self)
        self.id = 51001
        self.version = 9
        PtDebugPrint('grsnDownElevator::init end')


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        ageSDL.setNotify(self.key, upElevSDL.value, 0.0)
        ageSDL.setNotify(self.key, dnElevSDL.value, 0.0)
        downOn = ageSDL[dnElevSDL.value][0]
        if downOn:
            dnElevatorLights.run(self.key, state='TurnOn', avatar=PtGetLocalAvatar())
            downElevTrigger.enable()
            print 'down elevator on at load'
        else:
            dnElevatorLights.run(self.key, state='TurnOff', avatar=PtGetLocalAvatar())
            downElevTrigger.disable()
            print 'down elevator off at load'
        upOn = ageSDL[upElevSDL.value][0]
        if upOn:
            upElevatorLights.run(self.key, state='TurnOn', avatar=PtGetLocalAvatar())
            upElevatorBottomTrigger.enable()
            print 'up elevator on at load'
        else:
            upElevatorLights.run(self.key, state='TurnOff', avatar=PtGetLocalAvatar())
            upElevatorBottomTrigger.disable()
            print 'up elevator off at load'


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        if (VARname == dnElevSDL.value):
            downOn = ageSDL[dnElevSDL.value][0]
            if downOn:
                dnElevatorLights.run(self.key, state='TurnOn', avatar=PtGetLocalAvatar())
                downElevTrigger.enable()
                print 'turn on down elevator'
            else:
                dnElevatorLights.run(self.key, state='TurnOff', avatar=PtGetLocalAvatar())
                downElevTrigger.disable()
                print 'turn off down elevator'
        elif (VARname == upElevSDL.value):
            upOn = ageSDL[upElevSDL.value][0]
            if upOn:
                upElevatorLights.run(self.key, state='TurnOn', avatar=PtGetLocalAvatar())
                upElevatorBottomTrigger.enable()
                print 'turn on up elevator'
            else:
                upElevatorLights.run(self.key, state='TurnOff', avatar=PtGetLocalAvatar())
                upElevatorBottomTrigger.disable()
                print 'turn off up elevator'


    def OnTimer(self, id):
        if (id == kOpenDownElevatorTop):
            downElevatorTopOpenAnim.animation.play()
            PtAtTimeCallback(self.key, 2.6000000000000001, kCloseDownElevatorTop)
        elif (id == kCloseDownElevatorTop):
            downElevatorTopCloseAnim.animation.play()
        elif (id == kOpenUpElevatorBottom):
            upElevatorDoorTrigger.run(self.key, state='on')
        elif (id == kOpenUpElevatorTop):
            upElevatorTopOpenAnim.animation.play()
        elif (id == kOpenDownElevatorBottom):
            downElevatorBottomTrigger.run(self.key, state='on')


    def OnNotify(self, state, id, events):
        global avatarInDnElevator
        global avatarInUpElevator
        if ((id == downBehavior.id) and PtWasLocallyNotified(self.key)):
            PtDebugPrint(('grsnDownElevator: Avatar going down is %s' % PtGetClientName(avatarInDnElevator.getKey())))
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    PtDebugPrint('grsnDownElevator: entering elevator')
                    PtAtTimeCallback(self.key, 1, kOpenDownElevatorTop)
                    dnElevTopSoundDummyAnim.animation.play()
                    return
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                    PtDebugPrint('grsnDownElevator: warping to down point')
                    dnElevBotSoundDummyAnim.animation.play()
                    startDownCamera.value.pushCutsceneCamera(1, avatarInDnElevator.getKey())
                    avatarInDnElevator.avatar.exitSubWorld()
                    avatarInDnElevator.physics.warpObj(downElevWarpPoint.value.getKey())
                    PtAtTimeCallback(self.key, 1.66, kOpenDownElevatorBottom)
                    return
                if ((event[0] == kMultiStageEvent) and ((event[1] == 1) and (event[2] == kAdvanceNextStage))):
                    PtDebugPrint('grsnDownElevator: finished coming out of elevator')
                    startDownCamera.value.popCutsceneCamera(avatarInDnElevator.getKey())
                    cam = ptCamera()
                    cam.enableFirstPersonOverride()
                    downElevTrigger.enable()
                    if (avatarInDnElevator == PtGetLocalAvatar()):
                        PtSendKIMessage(kEnableEntireYeeshaBook, 0)
                    return
        if ((id == upBehavior.id) and PtWasLocallyNotified(self.key)):
            PtDebugPrint(('grsnDownElevator: Avatar going up is %s' % PtGetClientName(avatarInUpElevator.getKey())))
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    PtDebugPrint('grsnDownElevator: entering elevator')
                    PtAtTimeCallback(self.key, 1, kOpenUpElevatorBottom)
                    upElevBotSoundDummyAnim.animation.play()
                    return
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                    PtDebugPrint('grsnDownElevator: warping to up point')
                    upElevTopSoundDummyAnim.animation.play()
                    avatarInUpElevator.avatar.enterSubWorld(subworld.value)
                    avatarInUpElevator.physics.warpObj(upElevWarpPoint.value.getKey())
                    exitTopCamera.value.pushCamera(avatarInUpElevator.getKey())
                    startUpCamera.value.popCutsceneCamera(avatarInUpElevator.getKey())
                    PtAtTimeCallback(self.key, 1.66, kOpenUpElevatorTop)
                    return
                if ((event[0] == kMultiStageEvent) and ((event[1] == 1) and (event[2] == kAdvanceNextStage))):
                    PtDebugPrint('grsnDownElevator: finished coming out of elevator')
                    cam = ptCamera()
                    cam.enableFirstPersonOverride()
                    WellTopDefaultCam.value.pushCamera(avatarInUpElevator.getKey())
                    upElevatorTopCloseAnim.animation.play()
                    upElevatorBottomTrigger.enable()
                    if (avatarInUpElevator == PtGetLocalAvatar()):
                        PtSendKIMessage(kEnableEntireYeeshaBook, 0)
                    return
        if state:
            if (id == downElevTrigger.id):
                downElevTrigger.disable()
                avatarInDnElevator = PtFindAvatar(events)
                PtDebugPrint('triggered down elevator')
                cam = ptCamera()
                if (avatarInDnElevator == PtGetLocalAvatar()):
                    cam.disableFirstPersonOverride()
                    cam.undoFirstPerson()
                    PtSendKIMessage(kDisableEntireYeeshaBook, 0)
                finishDownCamera.value.pushCutsceneCamera(0, avatarInDnElevator.getKey())
                downBehavior.run(avatarInDnElevator)
            elif (id == upElevatorBottomTrigger.id):
                upElevatorBottomTrigger.disable()
                avatarInUpElevator = PtFindAvatar(events)
                PtDebugPrint('triggered up elevator')
                cam = ptCamera()
                if (avatarInUpElevator == PtGetLocalAvatar()):
                    cam.disableFirstPersonOverride()
                    cam.undoFirstPerson()
                    PtSendKIMessage(kDisableEntireYeeshaBook, 0)
                startUpCamera.value.pushCutsceneCamera(0, avatarInUpElevator.getKey())
                upBehavior.run(avatarInUpElevator)


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



