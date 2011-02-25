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
from xPsnlVaultSDL import *
import time
SphereNum = ptAttribInt(1, 'sphere #')
ActAdvanceSwitch = ptAttribActivator(2, 'clk: advance spheres switch')
RespAdvanceBeh = ptAttribResponder(3, 'resp: advance spheres beh')
RespAdvanceUse = ptAttribResponder(4, 'resp: advance spheres use', ['down0', 'up', 'down1', 'down2', 'down3'])
RespHubDoor = ptAttribResponder(5, 'resp: hub door (sphere 4 only!)', ['close', 'open'])
boolHubDoor = 0

class ahnyMaintRoom(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5581
        self.version = 2


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        PtAtTimeCallback(self.key, 0, 1)


    def OnTimer(self, id):
        global boolHubDoor
        if (id == 1):
            if (SphereNum.value == 4):
                try:
                    ageSDL = PtGetAgeSDL()
                except:
                    print 'ahnyMaintRoom.OnTimer():\tERROR---Cannot find the Ahnonay Age SDL'
                    ageSDL['ahnyHubDoor'] = (0,)
                    ageSDL['ahnyImagerSphere'] = (1,)
                ageSDL.setFlags('ahnyHubDoor', 1, 1)
                ageSDL.sendToClients('ahnyHubDoor')
                ageSDL.setNotify(self.key, 'ahnyHubDoor', 0.0)
                ageSDL.setFlags('ahnyImagerSphere', 1, 1)
                ageSDL.sendToClients('ahnyImagerSphere')
                ageSDL.setNotify(self.key, 'ahnyImagerSphere', 0.0)
                boolHubDoor = ageSDL['ahnyHubDoor'][0]
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
                print 'sphere =',
                print sphere
                ageSDL['ahnyImagerSphere'] = (sphere,)
                if (sphere == 4):
                    if (not (boolHubDoor)):
                        boolHubDoor = 1
                        ageSDL['ahnyHubDoor'] = (1,)
                    RespHubDoor.run(self.key, state='open', fastforward=1)
                else:
                    if boolHubDoor:
                        boolHubDoor = 0
                        ageSDL['ahnyHubDoor'] = (0,)
                    RespHubDoor.run(self.key, state='close', fastforward=1)
                RespAdvanceUse.run(self.key, state='down0', fastforward=1)
            elif ((SphereNum.value != 1) and ((SphereNum.value != 2) and (SphereNum.value != 3))):
                print 'ahnyMaintRoom.OnServerInitComplete():\tERROR---Invalid sphere# set in component.  Disabling clickable.'
                ActAdvanceSwitch.disableActivator()
        elif (id == 2):
            if (SphereNum.value == 4):
                ageSDL = PtGetAgeSDL()
                ageSDL['ahnyHubDoor'] = (1,)
            else:
                ActAdvanceSwitch.enableActivator()


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global boolHubDoor
        if (SphereNum.value == 4):
            ageSDL = PtGetAgeSDL()
            if (VARname == 'ahnyHubDoor'):
                boolHubDoor = ageSDL['ahnyHubDoor'][0]
                if boolHubDoor:
                    RespHubDoor.run(self.key, state='open')
                else:
                    RespHubDoor.run(self.key, state='close')


    def OnNotify(self, state, id, events):
        ageSDL = PtGetAgeSDL()
        if ((id == ActAdvanceSwitch.id) and state):
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
#            RespAdvanceBeh.run(self.key, avatar=PtGetLocalAvatar())
            RespAdvanceBeh.run(self.key, avatar=PtFindAvatar(events))
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################
        if (id == RespAdvanceBeh.id):
            RespAdvanceUse.run(self.key, state='up')
        if (id == RespAdvanceUse.id):
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
                    newsphere = SphereNum.value
                    diffsphere = ((newsphere - sphere) % 4)
                    if (diffsphere == 0):
                        RespAdvanceUse.run(self.key, state='down0')
                        return
                    else:
                        sphereVar.setInt(newsphere, 0)
                        ahnySDL.setStateDataRecord(ahnyRecord)
                        ahnySDL.save()
                        print 'advanced from sphere ',
                        print sphere,
                        print ' with maintainence button'
                        print 'sphere ',
                        print newsphere,
                        print ' will now be the active sphere'
                        if (diffsphere == 1):
                            RespAdvanceUse.run(self.key, state='down1')
                            PtAtTimeCallback(self.key, 7, 2)
                        elif (diffsphere == 2):
                            RespAdvanceUse.run(self.key, state='down2')
                            PtAtTimeCallback(self.key, 14, 2)
                        elif (diffsphere == 3):
                            RespAdvanceUse.run(self.key, state='down3')
                            PtAtTimeCallback(self.key, 21, 2)
                        else:
                            print 'ahnyMaintRoom.py: ERROR.  Sphere advancement# not possible??'
                        if (SphereNum.value == 4):
                            ageSDL['ahnyImagerSphere'] = (newsphere,)


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



