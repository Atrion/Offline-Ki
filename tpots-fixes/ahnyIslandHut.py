# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from xPsnlVaultSDL import *
import time
ActRotateSwitch = ptAttribActivator(1, 'clk: rotate spheres')
RespRotateSwitch = ptAttribResponder(2, 'resp: rotate spheres switch')
SDLWaterCurrent = ptAttribString(3, 'SDL: water current')
ActWaterCurrent = ptAttribActivator(4, 'clk: water current')
RespCurrentValve = ptAttribResponder(5, 'resp: water current valve', ['on', 'off'])
WaterCurrent1 = ptAttribSwimCurrent(6, 'water current 1')
WaterCurrent2 = ptAttribSwimCurrent(7, 'water current 2')
WaterCurrent3 = ptAttribSwimCurrent(8, 'water current 3')
WaterCurrent4 = ptAttribSwimCurrent(9, 'water current 4')
RespCurrentChange = ptAttribResponder(10, 'resp: change the water current', ['on', 'off'])
RespRotateSpheres = ptAttribResponder(11, 'resp: rotate the spheres')
SDLHutDoor = ptAttribString(12, 'SDL: hut door')
ActHutDoor = ptAttribActivator(13, 'clk: hut door switch')
RespHutDoorBeh = ptAttribResponder(14, 'resp: hut door switch')
RespHutDoor = ptAttribResponder(15, 'resp: hut door', ['open', 'close'])
boolCurrent = 0
boolHutDoor = 0

class ahnyIslandHut(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5580
        self.version = 1


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        PtAtTimeCallback(self.key, 0, 1)


    def OnTimer(self, id):
        global boolCurrent
        global boolHutDoor
        if (id == 1):
            try:
                ageSDL = PtGetAgeSDL()
            except:
                print 'ahnySphere1MaintBtn.OnServerInitComplete():\tERROR---Cannot find the Ahnonay Age SDL'
                ageSDL[SDLWaterCurrent.value] = (0,)
                ageSDL[SDLHutDoor.value] = (0,)
            ageSDL.setFlags(SDLWaterCurrent.value, 1, 1)
            ageSDL.sendToClients(SDLWaterCurrent.value)
            ageSDL.setNotify(self.key, SDLWaterCurrent.value, 0.0)
            ageSDL.setFlags(SDLHutDoor.value, 1, 1)
            ageSDL.sendToClients(SDLHutDoor.value)
            ageSDL.setNotify(self.key, SDLHutDoor.value, 0.0)
            boolCurrent = ageSDL[SDLWaterCurrent.value][0]
            boolHutDoor = ageSDL[SDLHutDoor.value][0]
            if boolCurrent:
                RespCurrentChange.run(self.key, state='on', fastforward=1)
                print 'OnInit, will now enable current'
                WaterCurrent1.current.enable()
                WaterCurrent2.current.enable()
                WaterCurrent3.current.enable()
                WaterCurrent4.current.enable()
            else:
                RespCurrentChange.run(self.key, state='off', fastforward=1)
                print 'OnInit, will now disable current'
                WaterCurrent1.current.disable()
                WaterCurrent2.current.disable()
                WaterCurrent3.current.disable()
                WaterCurrent4.current.disable()
            if boolHutDoor:
                RespHutDoor.run(self.key, state='open', fastforward=1)
            else:
                RespHutDoor.run(self.key, state='close', fastforward=1)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global boolCurrent
        global boolHutDoor
        ageSDL = PtGetAgeSDL()
        if (VARname == SDLWaterCurrent.value):
            boolCurrent = ageSDL[SDLWaterCurrent.value][0]
            if boolCurrent:
                RespCurrentChange.run(self.key, state='on')
            else:
                RespCurrentChange.run(self.key, state='off')
        if (VARname == SDLHutDoor.value):
            boolHutDoor = ageSDL[SDLHutDoor.value][0]
            if boolHutDoor:
                RespHutDoor.run(self.key, state='open')
            else:
                RespHutDoor.run(self.key, state='close')


    def OnNotify(self, state, id, events):
        global boolCurrent
        global boolHutDoor
        ageSDL = PtGetAgeSDL()
        if ((id == ActRotateSwitch.id) and state):
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
#            RespRotateSwitch.run(self.key, avatar=PtGetLocalAvatar())
            RespRotateSwitch.run(self.key, avatar=PtFindAvatar(events))
        if ((id == ActWaterCurrent.id) and state):
            if boolCurrent:
#                RespCurrentValve.run(self.key, state='off', avatar=PtGetLocalAvatar())
                RespCurrentValve.run(self.key, state='off', avatar=PtFindAvatar(events))
            else:
#                RespCurrentValve.run(self.key, state='on', avatar=PtGetLocalAvatar())
                RespCurrentValve.run(self.key, state='on', avatar=PtFindAvatar(events))
        if ((id == ActHutDoor.id) and state):
#            RespHutDoorBeh.run(self.key, avatar=PtGetLocalAvatar())
            RespHutDoorBeh.run(self.key, avatar=PtFindAvatar(events))
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################
        if (id == RespRotateSwitch.id):
            RespRotateSpheres.run(self.key)
        if (id == RespRotateSpheres.id):
            if boolHutDoor:
                ageSDL[SDLHutDoor.value] = (0,)
            vault = ptVault()
            myAges = vault.getAgesIOwnFolder()
            myAges = myAges.getChildNodeRefList()
            for ageInfo in myAges:
                link = ageInfo.getChild()
                link = link.upcastToAgeLinkNode()
                info = link.getAgeInfo()
                if (not (info)):
                    continue
                ageName = info.getAgeFilename()
                spawnPoints = link.getSpawnPoints()
                if (ageName == 'Ahnonay'):
                    ahnySDL = info.getAgeSDL()
                    ahnyRecord = ahnySDL.getStateDataRecord()
                    sphereVar = ahnyRecord.findVar('ahnyCurrentSphere')
                    sphere = sphereVar.getInt(0)
                    newsphere = ((sphere + 1) % 3)
                    if (newsphere == 0):
                        newsphere = 3
                    sphereVar.setInt(newsphere, 0)
                    ahnySDL.setStateDataRecord(ahnyRecord)
                    ahnySDL.save()
                    print 'advanced from sphere ',
                    print sphere,
                    print ' with maintainence button'
                    return
        if (id == RespCurrentValve.id):
            if boolCurrent:
                ageSDL[SDLWaterCurrent.value] = (0,)
            else:
                ageSDL[SDLWaterCurrent.value] = (1,)
        if (id == RespCurrentChange.id):
            if boolCurrent:
                print 'will now enable current'
                WaterCurrent1.current.enable()
                WaterCurrent2.current.enable()
                WaterCurrent3.current.enable()
                WaterCurrent4.current.enable()
            else:
                print 'will now disable current'
                WaterCurrent1.current.disable()
                WaterCurrent2.current.disable()
                WaterCurrent3.current.disable()
                WaterCurrent4.current.disable()
        if (id == RespHutDoorBeh.id):
            if boolHutDoor:
                ageSDL[SDLHutDoor.value] = (0,)
            else:
                ageSDL[SDLHutDoor.value] = (1,)


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



