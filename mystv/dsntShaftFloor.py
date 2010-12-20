# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import string
FloorRaisedSDL = ptAttribString(1, 'Age SDL Floor Raised')
BlueTimer = ptAttribActivator(2, 'act: Blue Timer')
YellowTimer = ptAttribActivator(3, 'act: Yellow Timer')
FloorCenter = ptAttribActivator(4, 'deprecated')
respRaiseFloor = ptAttribResponder(5, 'resp: Raise Floor')
respLowerFloor = ptAttribResponder(6, 'resp: Lower Floor')
TooHighToJump = ptAttribActivator(7, 'act: Floor Jumpable Height')
respEnableBlocker = ptAttribResponder(8, 'resp: Enable JumpBlocker')
respDisableBlocker = ptAttribResponder(9, 'resp: Disable JumpBlocker')
respEnableLadders = ptAttribResponder(10, 'resp: Enable Ladders')
respDisableLadders = ptAttribResponder(11, 'resp: Disable Ladders')
actSideDoorsSeal = ptAttribActivator(12, 'act: Side Doors Sealed')
respSideDoorsSeal = ptAttribResponder(13, 'resp: SideDoorsSeal')
respSideDoorsUnseal = ptAttribResponder(14, 'resp: SideDoorsUnseal')
actCrank = ptAttribActivator(15, 'act: the Man Crank')
respRedGlowStart = ptAttribResponder(16, 'resp: Red Glow Start')
respRedGlowStop = ptAttribResponder(17, 'resp: Red Glow Stop')
respBlueGlowStart = ptAttribResponder(18, 'resp: Blue Glow Start')
respBlueGlowStop = ptAttribResponder(19, 'resp: Blue Glow Stop')
respYellowGlowStart = ptAttribResponder(20, 'resp: Yellow Glow Start')
respYellowGlowStop = ptAttribResponder(21, 'resp: Yellow Glow Stop')
actOnFloor = ptAttribActivator(22, 'rgn sensor: on floor')
NodeRgnAbove = ptAttribSceneobject(23, 'Node Rgn Above')
NodeRgnBelow = ptAttribSceneobject(24, 'Node Rgn Below')
respCameraUp = ptAttribResponder(25, 'resp: FloorGoingUp Cam')
respCameraDown = ptAttribResponder(26, 'resp: FloorGoingDown Cam')
respPitBlock = ptAttribResponder(27, 'resp: PitBlocker Enable')
respPitUnblock = ptAttribResponder(28, 'resp: PitBlocker Disable')
RedTop = ptAttribActivator(29, 'act: Red Btn Top')
RedBottom = ptAttribActivator(30, 'act: Red Btn Bottom')
respButtonsSink = ptAttribResponder(31, 'resp: Buttons Sink')
respButtonsRise = ptAttribResponder(32, 'resp: Buttons Rise')
NodeUnderLoweredFloor = ptAttribSceneobject(33, 'Node Under Lowered Floor')
NodeUnderRaisedFloor = ptAttribSceneobject(34, 'Node Under Raised Floor')
objLadder01 = ptAttribSceneobject(35, 'so: Ladder #1')
objLadder02 = ptAttribSceneobject(36, 'so: Ladder #2')
objLadder03 = ptAttribSceneobject(37, 'so: Ladder #3')
respCatwalkBlock = ptAttribResponder(38, 'resp: PitBlocker Block')
respCatwalkUnblock = ptAttribResponder(39, 'resp: PitBlocker Unblock')

class dsntShaftFloor(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 6205
        version = 11
        self.version = version
        print '__init__dsntShaftFloor v.',
        print version,
        print '.0'



    def OnServerInitComplete(self):
        print 'dsntShaftFloor: OnServerInitComplete'
        respRaiseFloor.run(self.key, fastforward=1)
        respSideDoorsUnseal.run(self.key, fastforward=1)
        sealDoors = ['FloorWeight1', 'CounterWeightGlarePlane08', 'RTOmniLight21',
         'FloorWeight8', 'CounterWeightGlarePlane07', 'RTOmniLight22',
         'FloorWeight11', 'CounterWeightGlarePlane04', 'RTOmniLight25',
         'FloorWeight12', 'CounterWeightGlarePlane03', 'RTOmniLight01']
        for obj in sealDoors: PtFindSceneobject(obj, 'DescentMystV').draw.disable()
        #PtFindSceneobject('NodeRgnBelow', 'DescentMystV').physics.suppress(1)
        #PtFindSceneobject('NodeRgnAbove', 'DescentMystV').physics.suppress(1)
        PtFindSceneobject('CatwalkBlocker', 'DescentMystV').physics.suppress(1)


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



