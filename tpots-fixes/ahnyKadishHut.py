# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import string
import time
SDLWindows = ptAttribString(1, 'SDL: windows')
ActWindows = ptAttribActivator(2, 'clk: windows')
RespWindowsBeh = ptAttribResponder(3, 'resp: windows oneshot')
RespWindows = ptAttribResponder(4, 'resp: windows use', ['close', 'open'])
SDLDniTimer = ptAttribString(5, 'SDL: D\'ni timer')
ActDniTimer = ptAttribActivator(6, 'clk: D\'ni timer')
RespDniTimer = ptAttribResponder(7, 'resp: D\'ni timer', ['off', 'on'])
MatAnimDniTimer = ptAttribMaterialAnimation(8, 'mat anim: D\'ni timer')
boolWindows = 0
StartTime = 0
EndTime = 0
kTimeWarp = 870

class ahnyKadishHut(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5610
        self.version = 4


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        PtAtTimeCallback(self.key, 0, 1)


    def OnTimer(self, id):
        global boolWindows
        global EndTime
        if (id == 1):
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(SDLWindows.value, 1, 1)
            ageSDL.sendToClients(SDLWindows.value)
            ageSDL.setNotify(self.key, SDLWindows.value, 0.0)
            ageSDL.setFlags(SDLDniTimer.value, 1, 1)
            ageSDL.sendToClients(SDLDniTimer.value)
            ageSDL.setNotify(self.key, SDLDniTimer.value, 0.0)
            try:
                ageSDL = PtGetAgeSDL()
            except:
                print 'ahnyKadishHut.OnServerInitComplete():\tERROR---Cannot find AhnySphere04 age SDL'
                ageSDL[SDLWindows.value] = (0,)
                ageSDL[SDLDniTimer.value] = (0,)
            boolWindows = ageSDL[SDLWindows.value][0]
            EndTime = ageSDL[SDLDniTimer.value][0]
            if boolWindows:
                print 'ahnyKadishHut.OnServerInitComplete(): Windows are open'
                RespWindows.run(self.key, state='open', fastforward=1)
            else:
                print 'ahnyKadishHut.OnServerInitComplete(): Windows are closed'
                RespWindows.run(self.key, state='close', fastforward=1)
            InitTime = PtGetDniTime()
            if (InitTime < EndTime):
                print 'ahnyKadishHut.OnServerInitComplete(): Timer is on'
                RespDniTimer.run(self.key, state='on')
                dniSecsLeft = (EndTime - InitTime)
                dniSecsElapsed = (kTimeWarp - dniSecsLeft)
                print 'dniSecsElapsed = ',
                print dniSecsElapsed
                MatAnimDniTimer.animation.skipToTime(dniSecsElapsed)
                MatAnimDniTimer.animation.resume()
                PtAtTimeCallback(self.key, 1, 2)
            else:
                print 'ahnyKadishHut.OnServerInitComplete(): Timer is off'
                RespDniTimer.run(self.key, state='off')
        if (id == 2):
            CurTime = PtGetDniTime()
            if (CurTime >= EndTime):
                RespDniTimer.run(self.key, state='off')
            else:
                PtAtTimeCallback(self.key, 1, 2)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global boolWindows
        global EndTime
        ageSDL = PtGetAgeSDL()
        if (VARname == SDLWindows.value):
            boolWindows = ageSDL[SDLWindows.value][0]
            if boolWindows:
                print 'ahnyKadishHut.OnSDLNotify(): Windows will now open'
                RespWindows.run(self.key, state='open')
            else:
                print 'ahnyKadishHut.OnSDLNotify(): Windows will now close'
                RespWindows.run(self.key, state='close')
        if (VARname == SDLDniTimer.value):
            EndTime = ageSDL[SDLDniTimer.value][0]
            if EndTime:
                print 'ahnyKadishHut.OnSDLNotify(): Timer is now on'
                RespDniTimer.run(self.key, state='on')
                MatAnimDniTimer.animation.skipToTime(0)
                MatAnimDniTimer.animation.play()
                PtAtTimeCallback(self.key, 1, 2)
            else:
                print 'ahnyKadishHut.OnSDLNotify(): Timer is now off'
                RespDniTimer.run(self.key, state='off')
                MatAnimDniTimer.animation.stop()


    def OnNotify(self, state, id, events):
        global StartTime
        global boolWindows
        ageSDL = PtGetAgeSDL()
        if ((id == ActWindows.id) and state):
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
#            RespWindowsBeh.run(self.key, avatar=PtGetLocalAvatar())
            RespWindowsBeh.run(self.key, avatar=PtFindAvatar(events))
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################
        if ((id == ActDniTimer.id) and state):
            StartTime = PtGetDniTime()
            newtime = (StartTime + kTimeWarp)
            ageSDL[SDLDniTimer.value] = (newtime,)
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
#        if (id == RespWindowsBeh.id):
        if ((id == RespWindowsBeh.id) and PtWasLocallyNotified(self.key)):
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################
            if boolWindows:
                ageSDL[SDLWindows.value] = (0,)
            else:
                ageSDL[SDLWindows.value] = (1,)


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



