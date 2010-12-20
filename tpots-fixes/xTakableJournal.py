# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import string
stringVarName = ptAttribString(1, 'Show/hide age SDL var name')
boolShowOnTrue = ptAttribBoolean(2, 'Show on true', 1)
actClickable = ptAttribActivator(3, 'Journal clickable')
AgeStartedIn = None
kEnableJournalTimer = 99
kDisableJournalTimer = 98

class xTakableJournal(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 217
        self.version = 1


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        self.shown = false
        if (not ((type(stringVarName.value) == type('')) and (stringVarName.value != ''))):
            PtDebugPrint(('ERROR: xTakableJournal.OnFirstUpdate():\tERROR: missing SDL var name on %s' % self.sceneobject.getName()))


    def OnServerInitComplete(self):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            if ((type(stringVarName.value) == type('')) and (stringVarName.value != '')):
                try:
                    ageSDL.setNotify(self.key, stringVarName.value, 0.0)
                    #if (not (ageSDL[stringVarName.value][0] ^ boolShowOnTrue.value)):
######
# new code - fix for thiefs
                    vault = ptAgeVault()
                    playerid = PtGetLocalClientID()
                    if vault.getAgeInfo().getAgeOwnersFolder().hasPlayer(playerid) and (not (ageSDL[stringVarName.value][0] ^ boolShowOnTrue.value)):
######
                        PtAtTimeCallback(self.key, 1, kEnableJournalTimer)
                        self.shown = true
                    else:
                        PtAtTimeCallback(self.key, 1, kDisableJournalTimer)
                except:
                    PtDebugPrint(("ERROR: xTakableJournal.OnServerInitComplete():\tERROR accessing ageSDL on %s so we're disabling" % self.sceneobject.getName()))
                    PtAtTimeCallback(self.key, 1, kDisableJournalTimer)
            else:
                PtDebugPrint(("ERROR: xTakableJournal.OnServerInitComplete():\tERROR: missing SDL var name on %s so we're disabling" % self.sceneobject.getName()))
                PtAtTimeCallback(self.key, 1, kDisableJournalTimer)


    def OnTimer(self, id):
        if (id == kEnableJournalTimer):
            self.IEnableJournal()
        elif (id == kDisableJournalTimer):
            self.IDisableJournal()


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname != stringVarName.value):
            return
        if (AgeStartedIn != PtGetAgeName()):
            return
        ageSDL = PtGetAgeSDL()
        try:
            if (not (ageSDL[stringVarName.value][0] ^ boolShowOnTrue.value)):
                self.IEnableJournal()
            else:
                self.IDisableJournal()
        except:
            PtDebugPrint(("ERROR: xTakableJournal.OnSDLNotify():\tERROR reading age SDL on %s so we're disabling" % self.sceneobject.getName()))
            self.IDisableJournal()


    def OnNotify(self, state, id, events):
        if (not (state)):
            return
        if (not PtWasLocallyNotified(self.key)):
            PtDebugPrint("DEBUG: xTakableJournal.OnNotify(): Message didn't come from our player, ignoring")
            return
        if (id == actClickable.id):
            ageSDL = PtGetAgeSDL()
            ageSDL[stringVarName.value] = ((not boolShowOnTrue.value),)
            PtSendKIMessage(kAddJournalBook, 0)


    def IEnableJournal(self):
        PtDebugPrint(('DEBUG: xTakableJournal.IEnableJournal():  Enabling clickable on %s...' % self.sceneobject.getName()))
        actClickable.enable()


    def IDisableJournal(self):
        PtDebugPrint(('DEBUG: xTakableJournal.IDisableJournal():  Disabling clickable on %s...' % self.sceneobject.getName()))
        actClickable.disable()


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



