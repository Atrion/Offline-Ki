# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
sdlWind = ptAttribString(1, 'SDL: wind')
sdlGear = ptAttribString(2, 'SDL: gear')
sdlDoor1 = ptAttribString(3, 'SDL: door1')
sdlDoor2 = ptAttribString(4, 'SDL: door2')
respWindmill = ptAttribResponder(5, 'resp: windmill', ['on', 'off'])
actGear = ptAttribActivator(6, 'drag: gear lever')
actHeight = ptAttribActivator(7, 'drag: cage height lever')
actRotate = ptAttribActivator(8, 'drag: cage rotation lever')
actDoor1 = ptAttribActivator(9, 'clk: door1 button')
actDoor2 = ptAttribActivator(10, 'clk: door2 button')
respGearLev = ptAttribResponder(11, 'resp: gear lever at start', ['on', 'off'])
respHeight = ptAttribResponder(12, 'resp: cage height', ['LowToMid', 'MidToHigh', 'HighToMid', 'MidToLow'])
respRotate = ptAttribResponder(13, 'resp: cage rotation', ['use', 'kill', 'rotsetup'])
respDoor1 = ptAttribResponder(14, 'resp: door1', ['open', 'close'])
respDoor2 = ptAttribResponder(15, 'resp: door2', ['stuck'])
anmEvtHgtLev = ptAttribActivator(16, 'anm evt: cage height lever')
anmEvtRotate = ptAttribActivator(17, 'anm evt: cage rotate')
sdlHeight = ptAttribString(18, 'SDL: cage height')
respHgtLevReset = ptAttribResponder(19, 'resp: reset height lever')
anmEvtRotLev = ptAttribActivator(20, 'anm evt: cage rotate lever')
respRotLevReset = ptAttribResponder(21, 'resp: reset rotate lever')
anmEvtGearLevOn = ptAttribActivator(22, 'anm evt: gear lever on')
anmEvtGearLevOff = ptAttribActivator(23, 'anm evt: gear lever off')
respDoorBtn1 = ptAttribResponder(24, 'resp: door btn 1', ['press', 'reenable'])
respDoorBtn2 = ptAttribResponder(25, 'resp: door btn 2', ['press', 'reenable'])
NodeRgnLow = ptAttribSceneobject(26, 'obj: node region - low')
NodeRgnMid = ptAttribSceneobject(27, 'obj: node region - mid')
NodeRgnHigh = ptAttribSceneobject(28, 'obj: node region - high')
respWindFX = ptAttribResponder(30, 'resp: wind FX', ['on', 'off'])
sdlRotSetup = ptAttribString(31, 'SDL: rotation setup')
actMazeNoFog1 = ptAttribActivator(32, 'rgn sns: maze no-fog 1')
actMazeNoFog2 = ptAttribActivator(33, 'rgn sns: maze no-fog 2')
actMazeNoFog3 = ptAttribActivator(34, 'rgn sns: maze no-fog 3')
actCanalDrop = ptAttribActivator(35, 'rgn sns: canal drop')
respCanalDrop = ptAttribResponder(36, 'resp: canal drop', ['on', 'off'])
objTree = ptAttribSceneobject(37, 'obj: any tree dummy')

class lakiWindmill(ptResponder):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 6362
        version = 11
        self.version = version
        print '__init__lakiWindmill v. ',
        print version,
        print '.0'


    def OnServerInitComplete(self):
        print 'lakiwindmill:onserverinitcomplete'
        respHeight.run(self.key, state='HighToMid', fastforward=1)
        NodeRgnLow.value.physics.disable()
        NodeRgnMid.value.physics.enable()
        NodeRgnHigh.value.physics.disable()
        respDoor1.run(self.key, state='open', fastforward=1)


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



