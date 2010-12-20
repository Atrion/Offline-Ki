# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
stringSDLVarName = ptAttribString(1, 'Age SDL Variable')
stringSDLVarToSet = ptAttribString(2, 'SDL Variable To Set')
stringStartStates = ptAttribString(3, 'State value tuples')
stringTag = ptAttribString(4, 'Extra info to pass along')
boolFirstUpdate = ptAttribBoolean(6, 'Init SDL On First Update?', 0)
AgeStartedIn = None

class xAgeSDLVarSet(ptResponder):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5303
        version = 2
        self.version = version
        self.enabledStateDict = {}
        print '__init__xAgeSDLVarSet v.',
        print version


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        if ((type(stringSDLVarName.value) == type('')) and (stringSDLVarName.value != '')):
            PtDebugPrint(('DEBUG: xAgeSDLVarSet.OnFirstUpdate:\tOn %s' % stringSDLVarName.value))
            try:
                str = stringStartStates.value.replace(' ', '')
                tuples = str.split(')(')
                tuples[0] = tuples[0][1:]
                tuples[-1] = tuples[-1][:-1]
                for tup in tuples:
                    vals = tup.split(',')
                    self.enabledStateDict[int(vals[0])] = int(vals[1])
            except:
                PtDebugPrint('ERROR: xAgeSDLVarSet.OnFirstUpdate():\tERROR: couldn\'t process start state list')
        else:
            PtDebugPrint('ERROR: xAgeSDLVarSet.OnFirstUpdate():\tERROR: missing SDL var name in max file')
        # fix for pages that are loaded deferred
        import xUserKI
        if (boolFirstUpdate.value or (xUserKI.AgeInitialized())): # if it is already initialized now, we are loaded dynamically
            self.OnServerInitComplete()


    def OnServerInitComplete(self):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(stringSDLVarToSet.value, 1, 1)
            ageSDL.sendToClients(stringSDLVarToSet.value)
            PtDebugPrint(('DEBUG: xAgeSDLVarSet.OnServerInitComplete:\tSetting notify on %s' % stringSDLVarName.value))
            ageSDL.setNotify(self.key, stringSDLVarName.value, 0.0)
            SDLvalue = ageSDL[stringSDLVarName.value][0]
            PtDebugPrint(('DEBUG: xAgeSDLVarSet.OnServerInitComplete:\tCurrent SDL value = %d' % SDLvalue))
            if self.enabledStateDict.has_key(int(SDLvalue)):
                ageSDL[stringSDLVarToSet.value] = (self.enabledStateDict[int(SDLvalue)],)
                if ((type(stringSDLVarToSet) != type(None)) and (stringSDLVarToSet.value != '')):
                    ageSDL.setTagString(stringSDLVarToSet.value, stringTag.value)
                PtDebugPrint(('DEBUG: xAgeSDLVarSet.OnServerInitComplete:\t%s setting %s to %d' % (stringSDLVarName.value, stringSDLVarToSet.value, self.enabledStateDict[int(SDLvalue)])))


    def OnSDLNotify(self, VARname, SDLname, PlayerID, tag):
        if (VARname != stringSDLVarName.value):
            return
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            PtDebugPrint(('DEBUG: xAgeSDLVarSet.OnSDLNotify received: %s' % VARname))
            SDLvalue = ageSDL[stringSDLVarName.value][0]
            if self.enabledStateDict.has_key(int(SDLvalue)):
                ageSDL[stringSDLVarToSet.value] = (self.enabledStateDict[int(SDLvalue)],)
                if ((type(stringSDLVarToSet) != type(None)) and (stringSDLVarToSet.value != '')):
                    ageSDL.setTagString(stringSDLVarToSet.value, stringTag.value)
                PtDebugPrint(('DEBUG: xAgeSDLVarSet.OnServerInitComplete:\t%s setting %s to %d, tag string: %s' % (stringSDLVarName.value, stringSDLVarToSet.value, self.enabledStateDict[int(SDLvalue)], stringTag.value)))


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



