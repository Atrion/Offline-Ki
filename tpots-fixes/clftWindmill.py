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
clickLever = ptAttribActivator(4, 'lever clickable')
clickLockCW = ptAttribActivator(5, 'clickable CW locked')
clickLockStart = ptAttribActivator(6, 'clickable CCW locked / Start')
respLockedCCW = ptAttribResponder(7, 'responder CCW Locked')
behLockedCCW = ptAttribBehavior(10, 'locked CCW behavior')
behStartWindmill = ptAttribBehavior(11, 'start windmill behavior')
respStart = ptAttribResponder(13, 'responder Start Windmill', ['Start'])
stringSDLVarLocked = ptAttribString(14, 'SDL Bool locked windmill')
stringSDLVarRunning = ptAttribString(15, 'SDL Bool windmill running')
respStartAtLoad = ptAttribResponder(16, 'start windmill at load')
respLightsOnOff = ptAttribResponder(17, 'lights on off', ['On', 'Off'])
stringSDLVarUnstuck = ptAttribString(18, 'SDL Bool unstuck windmill')
respImagerButtonLight = ptAttribResponder(19, 'Imager button light on off', ['On', 'Off'])
respBrakeOff = ptAttribResponder(20, 'resp: Gear lever up')
respBrakeOn = ptAttribResponder(21, 'resp: Gear lever back')
respBrakeOffAtStart = ptAttribResponder(22, 'resp: Gear lever up at start')
respBrakeOnAtStart = ptAttribResponder(23, 'resp: Gear lever back at start')
respStop = ptAttribResponder(24, 'stop windmill', ['Stop'])
respGrinderOn = ptAttribResponder(25, 'resp:  Grinder wheel on')
respGrinderOff = ptAttribResponder(26, 'resp:  Grinder wheel off')
windmillLocked = 1
windmillRunning = 0
windmillUnstuck = 0
boolTomahnaActive = 0
stopGrinder = 0
avatar = None

class clftWindmill(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 50248353
        self.version = 10


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        global boolTomahnaActive
        global windmillLocked
        global windmillRunning
        global windmillUnstuck
        if ((type(stringSDLVarLocked.value) == type('')) and (stringSDLVarLocked.value != '')):
            self.ageSDL = PtGetAgeSDL()
            self.ageSDL.setFlags(stringSDLVarLocked.value, 1, 1)
            self.ageSDL.sendToClients(stringSDLVarLocked.value)
        else:
            PtDebugPrint('clftWindmill.OnFirstUpdate():\tERROR: missing SDL var locked in max file')
        if ((type(stringSDLVarRunning.value) == type('')) and (stringSDLVarRunning.value != '')):
            self.ageSDL = PtGetAgeSDL()
            self.ageSDL.setFlags(stringSDLVarRunning.value, 1, 1)
            self.ageSDL.sendToClients(stringSDLVarRunning.value)
        else:
            PtDebugPrint('clftWindmill.OnFirstUpdate():\tERROR: missing SDL var running in max file')
        respLightsOnOff.run(self.key, state='Off')
        respImagerButtonLight.run(self.key, state='Off')
        if ((type(stringSDLVarUnstuck.value) == type('')) and (stringSDLVarUnstuck.value != '')):
            self.ageSDL = PtGetAgeSDL()
            self.ageSDL.setFlags(stringSDLVarUnstuck.value, 1, 1)
            self.ageSDL.sendToClients(stringSDLVarUnstuck.value)
        else:
            PtDebugPrint('clftWindmill.OnFirstUpdate():\tERROR: missing SDL var unstuck in max file')
        self.ageSDL = PtGetAgeSDL()
        self.ageSDL.setNotify(self.key, stringSDLVarLocked.value, 0.0)
        SDLVarTomahnaActive = 'clftTomahnaActive'
        boolTomahnaActive = self.ageSDL[SDLVarTomahnaActive][0]
        windmillLocked = 1
        try:
            windmillLocked = self.ageSDL[stringSDLVarLocked.value][0]
        except:
            windmillLocked = 1
            PtDebugPrint('ERROR: clftWindmill.OnServerInitComplete():\tERROR: age sdl read failed, defaulting windmill locked')
        if (windmillLocked == 0):
            respBrakeOffAtStart.run(self.key)
        elif (windmillLocked == 1):
            respBrakeOnAtStart.run(self.key)
        self.ageSDL.setNotify(self.key, stringSDLVarRunning.value, 0.0)
        windmillRunning = 0
        try:
            windmillRunning = self.ageSDL[stringSDLVarRunning.value][0]
        except:
            windmillRunning = 0
            PtDebugPrint('ERROR: clftWindmill.OnServerInitComplete():\tERROR: age sdl read failed, defaulting windmill stopped')
        if (windmillRunning == 1):
            respStartAtLoad.run(self.key)
            respLightsOnOff.run(self.key, state='On')
            respGrinderOn.run(self.key)
            if (boolTomahnaActive == 0):
                PtDebugPrint('clftWindmill.OnServerInitComplete: SDL says Tomahna is active, will set Imager light on...')
                respImagerButtonLight.run(self.key, state='On')
        self.ageSDL.setNotify(self.key, stringSDLVarUnstuck.value, 0.0)
        windmillUnstuck = 0
        try:
            windmillUnstuck = self.ageSDL[stringSDLVarUnstuck.value][0]
        except:
            windmillUnstuck = 0
            PtDebugPrint('ERROR: clftWindmill.OnServerInitComplete():\tERROR: age sdl read failed, defaulting windmill stuck')


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global windmillLocked
        global windmillRunning
        global stopGrinder
        global windmillUnstuck
        global avatar
        self.ageSDL = PtGetAgeSDL()
        if (type(avatar) == type(None)):
            PtDebugPrint('OnSDLNotify: Setting local avatar if none was set by OnNotify')
            avatar = PtGetLocalAvatar()
        if (VARname == stringSDLVarLocked.value):
            windmillLocked = self.ageSDL[stringSDLVarLocked.value][0]
            PtDebugPrint('clftWindmill.OnSDLNotify():\t windmill locked ', windmillLocked)
            if ((windmillLocked == 1) and (windmillRunning == 0)):
                respBrakeOn.run(self.key, avatar=avatar)
            if ((windmillLocked == 1) and (windmillRunning == 1)):
                PtDebugPrint('clftWindmill.OnSDLNotify: Both running and locked are 1, so stop windmill.')
                stopGrinder = 1
                respBrakeOn.run(self.key, avatar=avatar)
            elif ((windmillLocked == 0) and (windmillUnstuck == 1)):
                respBrakeOff.run(self.key, avatar=avatar)
                PtDebugPrint('clftWindmill.OnSDLNotify: Locked is 0 and windmillUnstuck is 1, run StartAtLoad.')
                windmillRunning = 1
            elif ((windmillLocked == 0) and (windmillUnstuck == 0)):
                respBrakeOff.run(self.key, avatar=avatar)


    def OnNotify(self, state, id, events):
        global windmillLocked
        global boolTomahnaActive
        global windmillRunning
        global windmillUnstuck
        global stopGrinder
        global avatar
        self.ageSDL = PtGetAgeSDL()
        if (PtWasLocallyNotified(self.key)):
            PtDebugPrint('OnNotify: You touched the windmill')
            avatar = PtGetLocalAvatar()
        else:
            PtDebugPrint('OnNotify: Somebody else touched the windmill')
            avatar = PtFindAvatar(events)
        if ((id == clickLockStart.id) and state):
            if (windmillLocked == 0):
                respStart.run(self.key, state='Start', avatar=avatar)
                respLightsOnOff.run(self.key, state='On', avatar=PtGetLocalAvatar())
                respGrinderOn.run(self.key)
                if (boolTomahnaActive == 0):
                    respImagerButtonLight.run(self.key, state='On', avatar=PtGetLocalAvatar())
                windmillRunning = 1
                self.ageSDL[stringSDLVarRunning.value] = (windmillRunning,)
                windmillUnstuck = 1
                self.ageSDL[stringSDLVarUnstuck.value] = (windmillUnstuck,)
            elif (windmillLocked == 1):
                respLockedCCW.run(self.key, avatar=avatar)
        if (id == respBrakeOn.id):
            if stopGrinder:
                respGrinderOff.run(self.key)
                stopGrinder = 0
                respStop.run(self.key, state='Stop', avatar=PtGetLocalAvatar())
                respLightsOnOff.run(self.key, state='Off', avatar=PtGetLocalAvatar())
                respImagerButtonLight.run(self.key, state='Off', avatar=PtGetLocalAvatar())
                windmillRunning = 0
                self.ageSDL[stringSDLVarRunning.value] = (windmillRunning,)
        if (id == respBrakeOff.id):
            if (windmillRunning == 1):
                respGrinderOn.run(self.key)
                respStartAtLoad.run(self.key, avatar=PtGetLocalAvatar())
                respLightsOnOff.run(self.key, state='On', avatar=PtGetLocalAvatar())
                self.ageSDL[stringSDLVarRunning.value] = (windmillRunning,)
                if (boolTomahnaActive == 0):
                    respImagerButtonLight.run(self.key, state='On', avatar=PtGetLocalAvatar())


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



