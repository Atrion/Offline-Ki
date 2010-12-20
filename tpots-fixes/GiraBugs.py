# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaConstants import *
water01 = ptAttribActivator(1, 'water 01')
water02 = ptAttribActivator(2, 'water 02')
water03 = ptAttribActivator(3, 'water 03')
fumerol01 = ptAttribActivator(4, 'fumerol 01')
fumerol02 = ptAttribActivator(5, 'fumerol 02')
fumerol03 = ptAttribActivator(6, 'fumerol 03')
fumerol04 = ptAttribActivator(7, 'fumerol 04')
fumerol05 = ptAttribActivator(8, 'fumerol 05')
fumerol06 = ptAttribActivator(9, 'fumerol 06')
fumerol07 = ptAttribActivator(10, 'fumerol 07')
fumerol08 = ptAttribActivator(11, 'fumerol 08')
fumerol09 = ptAttribActivator(12, 'fumerol 09')
fumerol10 = ptAttribActivator(13, 'fumerol 10')
fumerol11 = ptAttribActivator(14, 'fumerol 11')
fumerol12 = ptAttribActivator(15, 'fumerol 12')
fumerol13 = ptAttribActivator(16, 'fumerol 13')
fumerol14 = ptAttribActivator(17, 'fumerol 14')
fumerol15 = ptAttribActivator(18, 'fumerol 15')
currentBehavior = PtBehaviorTypes.kBehaviorTypeIdle
numJumps = 0
running = false

class GiraBugs(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 53627
        self.version = 1


    def OnServerInitComplete(self):
        self.OnFirstUpdate()


    def OnFirstUpdate(self):
        avatar = 0
        try:
            avatar = PtGetLocalAvatar()
        except:
            print 'failed to get local avatar'
            return
        avatar.avatar.registerForBehaviorNotify(self.key)
        bugs = PtGetNumParticles(avatar.getKey())
        if (bugs > 0):
            PtSetLightAnimStart(avatar.getKey(), true)
            print 'lights on at start'
        else:
            PtSetLightAnimStart(avatar.getKey(), false)
            print 'lights off at start'


    def BeginAgeUnLoad(self, avObj):
        try:
            local = PtGetLocalAvatar()
        except: return # player quitting the game, avatar already removed
        if (local == avObj):
            print 'avatar page out'
            local.avatar.unRegisterForBehaviorNotify(self.key)
            bugs = PtGetNumParticles(local.getKey()) # fix error at runtime
            print 'particles at age unload ',
            print bugs


    def OnTimer(self, id):
        global running
        avatar = PtGetLocalAvatar()
        bugs = PtGetNumParticles(avatar.getKey())
        if (bugs > 0):
            if (running and (id == PtBehaviorTypes.kBehaviorTypeRun)):
                PtKillParticles(3.0, 0.10000000000000001, avatar.getKey())
                PtAtTimeCallback(self.key, 0.40000000000000002, PtBehaviorTypes.kBehaviorTypeRun)
        elif (bugs == 0):
            PtSetLightAnimStart(avatar.getKey(), false)


    def OnNotify(self, state, id, events):
        local = PtGetLocalAvatar()
        avatar = PtFindAvatar(events)
        if (avatar != local):
            return
        bugs = PtGetNumParticles(avatar.getKey())
        if ((id == water01.id) or ((id == water02.id) or ((id == water03.id) or ((id == fumerol01.id) or ((id == fumerol02.id) or ((id == fumerol03.id) or ((id == fumerol04.id) or ((id == fumerol05.id) or ((id == fumerol06.id) or ((id == fumerol07.id) or ((id == fumerol08.id) or ((id == fumerol09.id) or ((id == fumerol10.id) or ((id == fumerol11.id) or ((id == fumerol12.id) or ((id == fumerol13.id) or ((id == fumerol14.id) or (id == fumerol15.id)))))))))))))))))):
            print 'splashdown! ',
            print id
            if bugs:
                print 'kill all bugs'
                PtSetParticleDissentPoint(0, 0, 10000, avatar.getKey())
                PtKillParticles(3.0, 1, avatar.getKey())
                PtSetLightAnimStart(avatar.getKey(), false)
                return


    def OnBehaviorNotify(self, behavior, id, state):
        global currentBehavior
        global running
        global numJumps
        if (state == false):
            currentBehavior = PtBehaviorTypes.kBehaviorTypeIdle
            if (behavior == PtBehaviorTypes.kBehaviorTypeRun):
                running = false
            return
        else:
            currentBehavior = behavior
            if (behavior == PtBehaviorTypes.kBehaviorTypeRun):
                running = true
        avatar = PtGetLocalAvatar()
        bugs = PtGetNumParticles(avatar.getKey())
        if (bugs > 0):
            if ((behavior == PtBehaviorTypes.kBehaviorTypeStandingJump) or (behavior == PtBehaviorTypes.kBehaviorTypeWalkingJump)):
                if (numJumps == 0):
                    numJumps = 1
                    if (bugs == 1):
                        PtKillParticles(3.0, 1, avatar.getKey())
                        PtSetLightAnimStart(avatar.getKey(), false)
                    else:
                        PtKillParticles(3.0, 0.5, avatar.getKey())
                else:
                    PtKillParticles(3.0, 1, avatar.getKey())
                    PtSetLightAnimStart(avatar.getKey(), false)
                    return
            if (behavior == PtBehaviorTypes.kBehaviorTypeRunningJump):
                print 'kill all bugs'
                PtSetParticleDissentPoint(0, 0, 10000, avatar.getKey())
                PtKillParticles(3.0, 1, avatar.getKey())
                PtSetLightAnimStart(avatar.getKey(), false)
                return
            if (behavior == PtBehaviorTypes.kBehaviorTypeRun):
                print 'started running, kill some bugs'
                PtSetParticleDissentPoint(0, 0, 10000, avatar.getKey())
                PtKillParticles(3.0, 0.10000000000000001, avatar.getKey())
                PtAtTimeCallback(self.key, 0.25, PtBehaviorTypes.kBehaviorTypeRun)
                return


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



