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
import string
ActElevBtn = ptAttribActivator(1, 'clk: elevator button')
SDLPlatform1 = ptAttribString(2, 'SDL: platform 1')
SDLPlatform2 = ptAttribString(3, 'SDL: platform 2')
SDLPlatform3 = ptAttribString(4, 'SDL: platform 3')
SDLPlatform4 = ptAttribString(5, 'SDL: platform 4')
SDLElevPos = ptAttribString(6, 'SDL: elevator pos')
SDLPower = ptAttribString(7, 'SDL: bakery power')
RespElevClk = ptAttribResponder(8, 'resp: elevator clicker')
RespElevPwr = ptAttribResponder(9, 'resp: elevator power', ['off', 'on'])
RespElevOps = ptAttribResponder(10, 'resp: elevator ops', ['up', 'jam', 'down'])
SDLElevBusy = ptAttribString(11, 'SDL: elevator busy')
ActBkryPwr = ptAttribActivator(12, 'clk: bakery power switch')
RespBkryPwrOff = ptAttribResponder(13, 'resp: bakery power off')
RespBkryPwrOn = ptAttribResponder(14, 'resp: bakery power on')
boolPlat1 = 0
boolPlat2 = 0
boolPlat3 = 0
boolPlat4 = 0
boolElevPos = 0
boolPwr = 0
boolElevBusy = 0
AutoDown = 0
LocalAvatar = None

class ercaBakeryElev(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 7029
        self.version = 4


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        global boolPlat1
        global boolPlat2
        global boolPlat3
        global boolPlat4
        global boolElevPos
        global boolPwr
        global boolElevBusy
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(SDLPlatform1.value, 1, 1)
        ageSDL.sendToClients(SDLPlatform1.value)
        ageSDL.setFlags(SDLPlatform2.value, 1, 1)
        ageSDL.sendToClients(SDLPlatform2.value)
        ageSDL.setFlags(SDLPlatform3.value, 1, 1)
        ageSDL.sendToClients(SDLPlatform3.value)
        ageSDL.setFlags(SDLPlatform4.value, 1, 1)
        ageSDL.sendToClients(SDLPlatform4.value)
        ageSDL.setFlags(SDLElevPos.value, 1, 1)
        ageSDL.sendToClients(SDLElevPos.value)
        ageSDL.setFlags(SDLPower.value, 1, 1)
        ageSDL.sendToClients(SDLPower.value)
        ageSDL.setFlags(SDLElevBusy.value, 1, 1)
        ageSDL.sendToClients(SDLElevBusy.value)
        ageSDL.setNotify(self.key, SDLPlatform1.value, 0.0)
        ageSDL.setNotify(self.key, SDLPlatform2.value, 0.0)
        ageSDL.setNotify(self.key, SDLPlatform3.value, 0.0)
        ageSDL.setNotify(self.key, SDLPlatform4.value, 0.0)
        ageSDL.setNotify(self.key, SDLElevPos.value, 0.0)
        ageSDL.setNotify(self.key, SDLPower.value, 0.0)
        ageSDL.setNotify(self.key, SDLElevBusy.value, 0.0)
        try:
            boolPlat1 = ageSDL[SDLPlatform1.value][0]
        except:
            PtDebugPrint('ERROR: ercaBakeryElev.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolPlat1 = 0
        PtDebugPrint(('DEBUG: ercaBakeryElev.OnServerInitComplete():\t%s = %d' % (SDLPlatform1.value, ageSDL[SDLPlatform1.value][0])))
        try:
            boolPlat2 = ageSDL[SDLPlatform2.value][0]
        except:
            PtDebugPrint('ERROR: ercaBakeryElev.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolPlat2 = 0
        PtDebugPrint(('DEBUG: ercaBakeryElev.OnServerInitComplete():\t%s = %d' % (SDLPlatform2.value, ageSDL[SDLPlatform2.value][0])))
        try:
            boolPlat3 = ageSDL[SDLPlatform3.value][0]
        except:
            PtDebugPrint('ERROR: ercaBakeryElev.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolPlat3 = 0
        PtDebugPrint(('DEBUG: ercaBakeryElev.OnServerInitComplete():\t%s = %d' % (SDLPlatform3.value, ageSDL[SDLPlatform3.value][0])))
        try:
            boolPlat4 = ageSDL[SDLPlatform4.value][0]
        except:
            PtDebugPrint('ERROR: ercaBakeryElev.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolPlat4 = 0
        PtDebugPrint(('DEBUG: ercaBakeryElev.OnServerInitComplete():\t%s = %d' % (SDLPlatform4.value, ageSDL[SDLPlatform4.value][0])))
        try:
            boolElevPos = ageSDL[SDLElevPos.value][0]
        except:
            PtDebugPrint('ERROR: ercaBakeryElev.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolElevPos = 0
        PtDebugPrint(('DEBUG: ercaBakeryElev.OnServerInitComplete():\t%s = %d' % (SDLElevPos.value, ageSDL[SDLElevPos.value][0])))
        try:
            boolPwr = ageSDL[SDLPower.value][0]
        except:
            PtDebugPrint('ERROR: ercaBakeryElev.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolPwr = 0
        PtDebugPrint(('DEBUG: ercaBakeryElev.OnServerInitComplete():\t%s = %d' % (SDLPower.value, ageSDL[SDLPower.value][0])))
        try:
            boolElevBusy = ageSDL[SDLElevBusy.value][0]
        except:
            PtDebugPrint('ERROR: ercaBakeryElev.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolElevBusy = 0
        PtDebugPrint(('DEBUG: ercaBakeryElev.OnServerInitComplete():\t%s = %d' % (SDLElevBusy.value, ageSDL[SDLElevBusy.value][0])))
        if boolElevPos:
            RespElevOps.run(self.key, state='up', fastforward=1)
        else:
            RespElevOps.run(self.key, state='down', fastforward=1)
        if boolPwr:
            RespBkryPwrOn.run(self.key, fastforward=1)
            RespElevPwr.run(self.key, state='on', fastforward=1)
        else:
            RespBkryPwrOff.run(self.key, fastforward=1)
            RespElevPwr.run(self.key, state='off', fastforward=1)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global boolPlat1
        global boolPlat2
        global boolPlat3
        global boolPlat4
        global boolElevPos
        global boolPwr
        global boolElevBusy
        global AutoDown
        ageSDL = PtGetAgeSDL()
        if (VARname == SDLPlatform1.value):
            boolPlat1 = ageSDL[SDLPlatform1.value][0]
        if (VARname == SDLPlatform2.value):
            boolPlat2 = ageSDL[SDLPlatform2.value][0]
        if (VARname == SDLPlatform3.value):
            boolPlat3 = ageSDL[SDLPlatform3.value][0]
        if (VARname == SDLPlatform4.value):
            boolPlat4 = ageSDL[SDLPlatform4.value][0]
        if (VARname == SDLElevPos.value):
            boolElevPos = ageSDL[SDLElevPos.value][0]
            ageSDL[SDLElevBusy.value] = (1,)
            RespElevPwr.run(self.key, state='off')
            if boolElevPos:
                RespElevOps.run(self.key, state='up')
            else:
                RespElevOps.run(self.key, state='down')
        if (VARname == SDLPower.value):
            boolPwr = ageSDL[SDLPower.value][0]
            if (boolElevBusy == 0):
                if boolPwr:
                    RespElevPwr.run(self.key, state='on')
                else:
                    RespElevPwr.run(self.key, state='off')
                    if boolElevPos:
                        AutoDown = 1
                        ageSDL[SDLElevPos.value] = (0,)
        if (VARname == SDLElevBusy.value):
            boolElevBusy = ageSDL[SDLElevBusy.value][0]
##############################################################################
# Attempt to fix the button slurp.
##############################################################################
#            if boolElevBusy:
#                if (not (AutoDown)):
#                    objAvatar = ptSceneobject(PtGetAvatarKeyFromClientID(playerID), self.key)
#                    RespElevClk.run(self.key, avatar=objAvatar)
##############################################################################
# End attempt to fix the button slurp.
##############################################################################


    def OnNotify(self, state, id, events):
        global boolElevPos
        global boolPlat1
        global boolPlat2
        global boolPlat3
        global boolPlat4
        global boolPwr
        global AutoDown
        ageSDL = PtGetAgeSDL()
        if ((id == ActElevBtn.id) and state):
##############################################################################
# Attempt to fix the button slurp.
##############################################################################
            if (PtWasLocallyNotified(self.key)):
                PtDebugPrint('OnNotify: You touched the elevator button')
                ageSDL[SDLElevBusy.value] = (1,)
            else:
                PtDebugPrint('OnNotify: Someone else touched the elevator button')
            RespElevClk.run(self.key, avatar=PtFindAvatar(events))
##############################################################################
# End attempt to fix the button slurp.
##############################################################################
        if (id == RespElevClk.id):
            if boolElevPos:
                ageSDL[SDLElevPos.value] = (0,)
            elif (boolPlat1 or (boolPlat2 or (boolPlat3 or boolPlat4))):
                RespElevPwr.run(self.key, state='off')
                RespElevOps.run(self.key, state='jam')
            else:
                ageSDL[SDLElevPos.value] = (1,)
        if (id == RespElevOps.id):
            ageSDL[SDLElevBusy.value] = (0,)
            if boolPwr:
                RespElevPwr.run(self.key, state='on')
            if (boolElevPos == 0):
                if AutoDown:
                    AutoDown = 0
        if ((id == ActBkryPwr.id) and state):
            objAvatar = PtFindAvatar(events)
            if boolPwr:
                RespBkryPwrOff.run(self.key, avatar=objAvatar)
            else:
                RespBkryPwrOn.run(self.key, avatar=objAvatar)
        if (id == RespBkryPwrOff.id):
            ageSDL[SDLPower.value] = (0,)
        if (id == RespBkryPwrOn.id):
            ageSDL[SDLPower.value] = (1,)


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



