# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
class ptAttribStateResponder(ptAttribResponder,):


    def run(self, key, state = None, events = None, avatar = None, objectName = None, netForce = 0, netPropagate = 1, fastforward = 0):
        if (type(self.value) != type(None)):
            nt = ptNotify(key)
            nt.clearReceivers()
            if ((type(objectName) != type(None)) and (type(self.byObject) != type(None))):
                nt.addReceiver(self.byObject[objectName])
            elif (type(self.value) == type([])):
                for resp in self.value:
                    nt.addReceiver(resp)

            else:
                nt.addReceiver(self.value)
            if (not netPropagate):
                nt.netPropagate(0)
            if (netForce or self.netForce):
                nt.netForce(1)
            if ((type(state) == type(0)) and (state >= 0)):
                nt.addResponderState(state)
            else:
                raise ptResponderStateError, 'State must be a positive integer'
            if (type(events) != type(None)):
                PtAddEvents(nt, events)
            if (type(avatar) != type(None)):
                nt.addCollisionEvent(1, avatar.getKey(), avatar.getKey())
            if fastforward:
                nt.setType(PtNotificationType.kResponderFF)
                nt.netPropagate(0)
                nt.netForce(0)
            nt.setActivate(1.0)
            nt.send()



strSDLVarName = ptAttribString(1, 'SDL Variable')
respEnterState = ptAttribStateResponder(2, 'Enter State Responder')
strStates = ptAttribString(3, 'Value/State Pairs')
boolStartFF = ptAttribBoolean(4, 'F-Forward on start', 0)
boolVaultManagerFF = ptAttribBoolean(5, 'F-Forward on VM notifications', 0)
intDefault = ptAttribInt(6, 'Default setting', 0)
#boolFirstUpdate = ptAttribBoolean(7, 'Eval On First Update?', 0)
class xAgeSDLIntStateListResp(ptResponder,):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5350
        version = 1
        self.version = version
        self.enabledStateList = []
        print '__init__xAgeSDLIntStateListResp v',
        print version



    def OnFirstUpdate(self):
        if (not ((type(strSDLVarName.value) == type('')) and (strSDLVarName.value != ''))):
            PtDebugPrint('ERROR: xAgeSDLIntStateListResp.OnFirstUpdate():\tERROR: missing SDL var name in max file')
        # fix for pages that are loaded deferred
        import xUserKI
        if xUserKI.AgeInitialized(): # if it is already initialized now, we are loaded dynamically
            self.Initialize()



    def OnServerInitComplete(self):
        self.Initialize()



    def Initialize(self):
        ageSDL = PtGetAgeSDL()
        ageSDL.setNotify(self.key, strSDLVarName.value, 0.0)
        try:
            SDLvalue = ageSDL[strSDLVarName.value][0]
        except:
            PtDebugPrint(('ERROR: xAgeSDLIntShowHide.OnServerInitComplete():\tERROR: age sdl read failed, SDLvalue = %d by default. stringVarName = %s' % (intDefault.value,
             stringVarName.value)))
            SDLvalue = intDefault.value
        try:
            self.dictStates = {}
            stateList = strStates.value.replace(' ', '')[1:-1].split(')(')
            for i in stateList:
                decState = i.split(',')
                self.dictStates[int(decState[0])] = int(decState[1])

        except:
            PtDebugPrint("ERROR: xAgeSDLIntStateListResp.OnServerInitComplete():\tERROR: couldn't process state list")
            PtDebugPrint('ERROR: xAgeSDLIntStateListResp.OnServerInitComplete():\tPlease enter states in the format: (val,stateNum)(val,stateNum)')
            return 
        PtDebugPrint(('DEBUG: xAgeSDLIntStateListResp.OnServerInitComplete():\t Registered State List: %s ' % self.dictStates))
        self.UpdateState(SDLvalue, None, boolStartFF.value)



    def OnSDLNotify(self, VARname, SDLname, PlayerID, tag):
        if (VARname != strSDLVarName.value):
            return 
        ageSDL = PtGetAgeSDL()
        SDLvalue = ageSDL[strSDLVarName.value][0]
        PtDebugPrint(('DEBUG: xAgeSDLIntStateListResp.OnSDLNotify received: %s = %d' % (VARname,
         SDLvalue)))
        if PlayerID:
            objAvatar = ptSceneobject(PtGetAvatarKeyFromClientID(PlayerID), self.key)
            fastforward = 0
        else:
            objAvatar = None
            fastforward = boolVaultManagerFF.value
        if (tag == 'fastforward'):
            objAvatar = None
            fastforward = 1
        self.UpdateState(SDLvalue, objAvatar, fastforward)



    def UpdateState(self, SDLval, avatar, fastforward):
        if self.dictStates.has_key(SDLval):
            PtDebugPrint(('DEBUG: xAgeSDLIntStateListResp.OnSDLNotify: running state responder: %s' % self.dictStates[SDLval]))
            respEnterState.run(self.key, state=self.dictStates[SDLval], avatar=avatar, fastforward=fastforward)
        else:
            PtDebugPrint(("ERROR: xAgeSDLIntStateListResp.OnSDLNotify: Couldn't find state: %d " % SDLval))


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



