# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
stringSDLVarClosed = ptAttribString(13, 'SDL Bool Closed')
xrgnDoorBlocker = ptAttribExcludeRegion(14, 'Exclude Region')
actInterior = ptAttribActivator(15, 'Clickable: interior')
respOpenInt = ptAttribResponder(16, 'Rspndr: open from inside')
actExterior = ptAttribActivator(17, 'Clickable: exterior')
respOpenExt = ptAttribResponder(18, 'Rspndr: open from outside')
boolCanManualClose = ptAttribBoolean(19, 'Player can close me', default=1)
respCloseInt = ptAttribResponder(20, 'Rspndr: close from inside')
respCloseExt = ptAttribResponder(21, 'Rspndr: close from outside')
boolCanAutoClose = ptAttribBoolean(22, 'Door can autoclose')
respAutoClose = ptAttribResponder(23, 'Rspndr: Auto Close')
boolForceOpen = ptAttribBoolean(24, 'Force Open if Age Empty')
boolForceClose = ptAttribBoolean(25, 'Force Close if Age Empty')
boolOwnedDoor = ptAttribBoolean(26, 'Only Owners Can Use', default=false)
stringSDLVarEnabled = ptAttribString(27, 'SDL Bool Enabled (Optional)')
boolEnableOK = true
AgeStartedIn = None

class xStandardDoor(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5031
        version = 6
        self.version = version
        print '__init__xStandardDoor v.',
        print version


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        if (not ((type(stringSDLVarClosed.value) == type('')) and (stringSDLVarClosed.value != ''))):
            PtDebugPrint('xStandardDoor.OnFirstUpdate():\tERROR: missing SDL var name in max file')
        # Fix some SDL vars to be updated here
        import xUserKI
        if xUserKI.AgeInitialized(): # if it is already initialized now, we are loaded dynamically
            self.OnServerInitComplete()
        # END Fix some SDL vars to be updated here


    def OnServerInitComplete(self):
        if (AgeStartedIn != PtGetAgeName()):
            raise Exception("Very serious problem: AgeStartedIn (%s) != current age (%s)" % (AgeStartedIn, PtGetAgeName()))
        global boolEnableOK
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(stringSDLVarClosed.value, 1, 1)
        ageSDL.sendToClients(stringSDLVarClosed.value)
        ageSDL.setNotify(self.key, stringSDLVarClosed.value, 0.0)
        ageSDL.setNotify(self.key, stringSDLVarEnabled.value, 0.0)
        try:
            doorClosed = ageSDL[stringSDLVarClosed.value][0]
        except:
            doorClosed = true
            PtDebugPrint('xStandardDoor.OnServerInitComplete():\tERROR: age sdl read failed, defaulting door closed value')
        PtDebugPrint(('xStandardDoor.OnServerInitComplete():\tageSDL[%s] = %d' % (stringSDLVarClosed.value, doorClosed)))
        try:
            if (stringSDLVarEnabled.value != ''):
                doorEnabled = ageSDL[stringSDLVarEnabled.value][0]
            else:
                doorEnabled = true
        except:
            doorEnabled = true
            PtDebugPrint('xStandardDoor.OnServerInitComplete():\tERROR: age sdl read failed, defaulting door enabled')
        if (len(PtGetPlayerList()) == 0):
            if (boolForceOpen.value and doorClosed):
                doorClosed = 0
                ageSDL.setTagString(stringSDLVarClosed.value, 'ignore')
                ageSDL[stringSDLVarClosed.value] = (0,)
                PtDebugPrint("xStandardDoor.OnServerInitComplete():\tdoor closed, but I'm the only one here...opening")
            elif (boolForceClose.value and (not doorClosed)):
                doorClosed = 1
                ageSDL.setTagString(stringSDLVarClosed.value, 'ignore')
                ageSDL[stringSDLVarClosed.value] = (1,)
                PtDebugPrint("xStandardDoor.OnServerInitComplete():\tdoor open, but I'm the only one here...closing")
        if (not boolOwnedDoor.value):
            boolEnableOK = true
        else:
            vault = ptVault()
            if vault.amOwnerOfCurrentAge():
                PtDebugPrint('xStandardDoor.OnServerInitComplete():\tWelcome Home!')
                boolEnableOK = true
            else:
                PtDebugPrint('xStandardDoor.OnServerInitComplete():\tWelcome Visitor.')
                boolEnableOK = false
        if (not doorEnabled):
            boolEnableOK = false
        if (not doorClosed):
            xrgnDoorBlocker.releaseNow(self.key)
            if len(respOpenExt.value):
                respOpenExt.run(self.key, fastforward=1)
            elif len(respOpenInt.value):
                respOpenInt.run(self.key, fastforward=1)
            else:
                PtDebugPrint("xStandardDoor.OnServerInitComplete():\tERROR - no open responder defined, can't init door open")
            if (boolCanManualClose.value and boolEnableOK):
                actExterior.enable()
                actInterior.enable()
                PtAtTimeCallback(self.key, 0, 1) # the ID (last parameter) indicates "disable" or "enable"
            else:
                actExterior.disable()
                actInterior.disable()
                PtAtTimeCallback(self.key, 0, 0) # the ID (last parameter) indicates "disable" or "enable"
        else:
            xrgnDoorBlocker.clearNow(self.key)
            if boolCanAutoClose.value:
                respAutoClose.run(self.key, fastforward=1)
            elif boolCanManualClose.value:
                if len(respCloseExt.value):
                    respCloseExt.run(self.key, fastforward=1)
                elif len(respCloseInt.value):
                    respCloseInt.run(self.key, fastforward=1)
                else:
                    PtDebugPrint("xStandardDoor.OnServerInitComplete():\tERROR - no close responder defined, can't init door closed")
            else:
                PtDebugPrint("xStandardDoor.OnServerInitComplete():\tWARNING: door set to neither manual close nor auto close, can't init closed")
            if boolEnableOK:
                actExterior.enable()
                actInterior.enable()
                PtAtTimeCallback(self.key, 0, 1) # the ID (last parameter) indicates "disable" or "enable"
            else:
                actExterior.disable()
                actInterior.disable()
                PtAtTimeCallback(self.key, 0, 0) # the ID (last parameter) indicates "disable" or "enable"


    def OnTimer(self, id):
        # work around the doors in the city not disabling properly
        if id:
            actExterior.enable()
            actInterior.enable()
        else:
            actExterior.disable()
            actInterior.disable()


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global boolEnableOK
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            if (VARname == stringSDLVarEnabled.value):
                PtDebugPrint(('xStandardDoor.OnSDLNotify():\t VARname:%s, SDLname:%s, tag:%s, value:%d, playerID:%d' % (VARname, SDLname, tag, ageSDL[stringSDLVarEnabled.value][0], playerID)))
                doorEnabled = ageSDL[stringSDLVarEnabled.value][0]
                if (not (doorEnabled)):
                    PtDebugPrint('xStandardDoor.OnSDLNotify():\tDoor Disabled')
                    boolEnableOK = false
                    actExterior.disable()
                    actInterior.disable()
                    return
                if (not (boolOwnedDoor.value)):
                    PtDebugPrint('xStandardDoor.OnSDLNotify():\tDoor Enabled')
                    boolEnableOK = true
                    actExterior.enable()
                    actInterior.enable()
                    return
                else:
                    vault = ptVault()
                    if vault.amOwnerOfCurrentAge():
                        PtDebugPrint('xStandardDoor.OnSDLNotify():\tOwners-Only Door Enabled')
                        boolEnableOK = true
                        actExterior.enable()
                        actInterior.enable()
                        return
                    PtDebugPrint("xStandardDoor.OnSDLNotify():\tOwners-Only Door Enabled...but I'm not an owner")
                    return
            if (VARname == stringSDLVarClosed.value):
                PtDebugPrint(('xStandardDoor.OnSDLNotify():\t VARname:%s, SDLname:%s, tag:%s, value:%d, playerID:%d' % (VARname, SDLname, tag, ageSDL[stringSDLVarClosed.value][0], playerID)))
                if (tag == 'ignore'):
                    return
                if playerID:
                    objAvatar = ptSceneobject(PtGetAvatarKeyFromClientID(playerID), self.key)
                    fastforward = 0
                else:
                    objAvatar = None
                    fastforward = 1
                PtDebugPrint(('xStandardDoor.OnSDLNotify():\tnotification from playerID: %d' % playerID))
                actExterior.disable()
                actInterior.disable()
                if ageSDL[stringSDLVarClosed.value][0]:
                    try:
                        if (tag == 'fromOutside'):
                            respCloseExt.run(self.key, avatar=objAvatar, fastforward=fastforward)
                        elif (tag == 'fromInside'):
                            respCloseInt.run(self.key, avatar=objAvatar, fastforward=fastforward)
                        elif (tag == 'fromAuto'):
                            respAutoClose.run(self.key, fastforward=fastforward)
                        elif (tag == 'fastforward'):
                            respCloseExt.run(self.key, avatar=objAvatar, fastforward=1)
                        else:
                            PtDebugPrint(('xStandardDoor.OnSDLNotify():\tWARNING missing or invalid hint string:%s' % tag))
                            fastforward = 1
                            if boolCanManualClose.value:
                                respCloseExt.run(self.key, fastforward=fastforward)
                            elif boolCanAutoClose.value:
                                respAutoClose.run(self.key, fastforward=fastforward)
                            else:
                                PtDebugPrint("xStandardDoor.OnSDLNotify():\tWARNING: door set to neither manual close nor auto close, can't close")
                    except:
                        PtDebugPrint(('xStandardDoor.OnSDLNotify():\tERROR processing sdl var %s hint string: $s' % (VARname, tag)))
                    if fastforward:
                        if boolEnableOK:
                            actExterior.enable()
                            actInterior.enable()
                        xrgnDoorBlocker.clearNow(self.key)
                else:
                    try:
                        if (tag == 'fromOutside'):
                            respOpenExt.run(self.key, avatar=objAvatar, fastforward=fastforward)
                        elif ((tag == 'fromInside') or (playerID == 0)):
                            respOpenInt.run(self.key, avatar=objAvatar, fastforward=fastforward)
                        else:
                            PtDebugPrint(('xStandardDoor.OnSDLNotify():\tWARNING missing or invalid hint string:%s' % tag))
                            fastforward = 1
                            respOpenExt.run(self.key, fastforward=fastforward)
                    except:
                        PtDebugPrint(('xStandardDoor.OnSDLNotify():\tERROR processing sdl var %s hint string: $s' % (VARname, tag)))
                        fastforward = 1
                        respOpenExt.run(self.key, fastforward=fastforward)
                    if fastforward:
                        if (boolCanManualClose.value and boolEnableOK):
                            actExterior.enable()
                            actInterior.enable()
                        xrgnDoorBlocker.releaseNow(self.key)


    def OnNotify(self, state, id, events):
        if ((id == respOpenExt.id) or (id == respOpenInt.id)):
            if (boolCanManualClose.value and boolEnableOK):
                actExterior.enable()
                actInterior.enable()
        elif ((id == respCloseExt.id) or ((id == respCloseInt.id) or (id == respAutoClose.id))):
            if boolEnableOK:
                actExterior.enable()
                actInterior.enable()


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



