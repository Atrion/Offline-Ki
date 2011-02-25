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
from xEnum import Enum
strDoorClosedVar = ptAttribString(1, 'Door Closed SDL Var')
xrgnDoorBlocker = ptAttribExcludeRegion(2, 'Exclude Region')
rgnSensor = ptAttribActivator(3, 'Region Sensor', netForce=1)
respDoor = ptAttribResponder(4, 'Open door Responder', ['open', 'close'])
strDoorEnabledVar = ptAttribString(6, 'Door Enabled SDL Var (optional)')
doorClosed = 1
doorEnabled = 1
AgeStartedIn = None

class xNewHighLevelStarTrekDoor(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5310
        self.version = 1
        PtDebugPrint(('DEBUG: xHighLevelStarTrekDoor.__init__: v. %d' % self.version))


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        if (not ((type(strDoorClosedVar.value) == type('')) and (strDoorClosedVar.value != ''))):
            PtDebugPrint('ERROR: xHighLevelStarTrekDoor.OnFirstUpdate():\tERROR: missing door closed SDL var name in max file')


    def OnServerInitComplete(self):
        global doorEnabled
        global doorClosed
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(strDoorClosedVar.value, 1, 1)
            ageSDL.sendToClients(strDoorClosedVar.value)
            ageSDL.setNotify(self.key, strDoorClosedVar.value, 0.0)
            ageSDL.setNotify(self.key, strDoorEnabledVar.value, 0.0)
            try:
                doorClosed = ageSDL[strDoorClosedVar.value][0]
            except:
                doorClosed = true
                PtDebugPrint('ERROR: xHighLevelStarTrekDoor.OnServerInitComplete():\tERROR: age sdl read failed, defaulting door closed value')
            if ((type(strDoorEnabledVar.value) == type('')) and (strDoorEnabledVar.value != '')):
                try:
                    doorEnabled = ageSDL[strDoorEnabledVar.value][0]
                except:
                    doorEnabled = true
                    PtDebugPrint('ERROR: xHighLevelStarTrekDoor.OnServerInitComplete():\tERROR: age sdl read failed, defaulting door enabled value')
            PtDebugPrint(('xHighLevelStarTrekDoor.OnServerInitComplete():\tdoorClosed = %d' % doorClosed))
            if ((len(PtGetPlayerList()) == 0) and (not doorClosed)):
                ageSDL.setTagString(strDoorClosedVar.value, 'ignore')
                ageSDL[strDoorClosedVar.value] = (1,)
                doorClosed = 1
                PtDebugPrint("DEBUG:  xHighLevelStarTrekDoor.OnServerInitComplete: door is open and I'm the only one here, so closing")
            if doorClosed:
                xrgnDoorBlocker.clearNow(self.key)
                respDoor.run(self.key, state='close', fastforward=1)
            else:
                xrgnDoorBlocker.releaseNow(self.key)
                respDoor.run(self.key, state='open', fastforward=1)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global doorEnabled
        global doorClosed
        global doorActive
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            if (VARname == strDoorEnabledVar.value):
                doorEnabled = ageSDL[strDoorEnabledVar.value][0]
                PtDebugPrint(('DEBUG: xHighLevelStarTrekDoor.OnSDLNotify: updated doorEnabled to %d' % doorEnabled))
            elif (VARname == strDoorClosedVar.value):
                doorClosed = ageSDL[strDoorClosedVar.value][0]
                PtDebugPrint(('DEBUG: xHighLevelStarTrekDoor.OnSDLNotify: updated doorClosed to %d' % doorClosed))
                if doorClosed:
                    if (tag != 'ignore'):
                        if respDoor.getState() != 'close':
                            print 'HighLevelStarTrekDoor.OnSDLNotify: closing door'
                            respDoor.run(self.key, state='close')
                        else:
                            print 'HighLevelStarTrekDoor.OnSDLNotify: door already closed!'
                    else:
                        ageSDL.setTagString(strDoorClosedVar.value, '')
                elif (tag != 'ignore'):
                    if respDoor.getState() != 'open':
                        print 'HighLevelStarTrekDoor.OnSDLNotify: opening door'
                        respDoor.run(self.key, state='open')
                    else:
                        print 'HighLevelStarTrekDoor.OnSDLNotify: door already open!'
                else:
                    ageSDL.setTagString(strDoorClosedVar.value, '')
            else:
                PtDebugPrint(("ERROR: xHighLevelStarTrekDoor.OnSDLNotify: received SDL var that I wasn't expecting - %s" % VARname))


    def OnNotify(self, state, id, events):
        global doorClosed
        ageSDL = PtGetAgeSDL()
        if ((id == rgnSensor.id) and PtWasLocallyNotified(self.key)):
            if (not state):
                return 
            if doorEnabled:
                for event in events:
                    if (event[0] == kCollisionEvent):
                        if PtFindAvatar(events) == PtGetLocalAvatar():
                            if event[1]:
                                try:
                                    ageSDL[strDoorClosedVar.value] = (0,)
                                except Exception, detail:
                                    PtDebugPrint("ERROR: xHighLevelStarTrekDoor.DoorActivate: attempted to set door open but I couldn't update SDL")
                            else:
                                try:
                                    ageSDL[strDoorClosedVar.value] = (1,)
                                except:
                                    PtDebugPrint("ERROR: xHighLevelStarTrekDoor.DoorActivate: attempted to set door closed but I couldn't update SDL")
                        break
        elif (id == respDoor.id):
            print ('HighLevelStarTrekDoor.OnNotify: door finished opening or closing, state now = ' + respDoor.getState())
            if doorEnabled:
                #doorClosed = ageSDL[strDoorClosedVar.value][0]
                if (doorClosed and respDoor.getState() != 'close'):
                    print 'HighLevelStarTrekDoor.OnNotify: door should be closed; closing'
                    respDoor.run(self.key, state='close')
                elif ((not doorClosed) and respDoor.getState() != 'open'):
                    print 'HighLevelStarTrekDoor.OnNotify: door should be open; opening'
                    respDoor.run(self.key, state='open')


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



