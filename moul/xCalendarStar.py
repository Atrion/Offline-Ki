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
from PlasmaKITypes import *
import string
from xPsnlVaultSDL import *
import xxConfig
rgnCalStar = ptAttribActivator(1, 'rgn sns: calendar star')
sdlCalStar = ptAttribString(3, 'SDL: cal stone in Relto')
respCalStar = ptAttribResponder(4, 'resp: get star')
boolFirstUpdate = ptAttribBoolean(5, 'Eval On First Update?', 0)
boolCalStar = false
AgeStartedIn = None
LocalAvatar = None
sdlVars = {
 1: 'grsnCalendarSpark01',
 2: 'kdshCalendarSpark02',
 3: 'giraCalendarSpark03',
 4: 'grsnCalendarSpark04',
 5: 'dsntCalendarSpark05',
 6: 'minkCalendarSpark06',
 7: 'ercaCalendarSpark07',
 8: 'jlakCalendarSpark08',
 9: 'tldnCalendarSpark09',
 10: 'philCalendarSpark10',
 11: 'grtzCalendarSpark11',
 12: 'mystCalendarSpark12', }
class xCalendarStar(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 225
        self.version = 1



    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        if AgeStartedIn in ['Minkata', 'Ercana', 'Garrison', 'Gira', 'Kadish', 'Personal02', 'Teledahn', 'Myst', 'GreatZero', 'Descent']:
            boolFirstUpdate.value = true
        if (not ((type(sdlCalStar.value) == type('')) and (sdlCalStar.value != ''))):
            PtDebugPrint('ERROR: xCalendarStar.OnFirstUpdate():\tERROR: missing SDL var name')
        if boolFirstUpdate.value:
            self.Initialize()



    def OnServerInitComplete(self):
        if (not boolFirstUpdate.value):
            self.Initialize()



    def Initialize(self):
        global LocalAvatar
        global boolCalStar
        if (AgeStartedIn == PtGetAgeName()):
            # Diafero
            if not len(PtGetPlayerList()):
                import time
                dnitime = PtGetDniTime()
                monthNum = int(time.strftime('%m', time.gmtime(dnitime)))
                sparkNum = int(sdlCalStar.value[-2:])
                sdlName = sdlVars[sparkNum]
                sdl = PtGetAgeSDL()
                sdl.setFlags(sdlName,1,1)
                sdl.sendToClients(sdlName)
                if monthNum == sparkNum:
                    sdl.setIndex(sdlName,0,1) # enable
                    PtDebugPrint('xCalendarStar: Current month is %d, sparkly is %d - enabling' % (monthNum, sparkNum))
                else:
                    sdl.setIndex(sdlName,0,0) # disable
                    PtDebugPrint('xCalendarStar: Current month is %d, sparkly is %d - disabling' % (monthNum, sparkNum))
            # /Diafero
            LocalAvatar = PtGetLocalAvatar()
            psnlSDL = xPsnlVaultSDL()
            try:
                boolCalStar = psnlSDL[sdlCalStar.value][0]
            except:
                PtDebugPrint('ERROR: xCalendarStar.Initialize():\tERROR reading age SDL')
            PtDebugPrint(('DEBUG: xCalendarStar.Initialize():\t%s = %d' % (sdlCalStar.value,
             boolCalStar)))



    def OnNotify(self, state, id, events):
        global boolCalStar
        PtDebugPrint(('xCalendarStar.OnNotify(): state = %d, id = %d' % (state,
         id)))
        if ((not state) or (id != rgnCalStar.id)):
            return 
        if (PtFindAvatar(events) != LocalAvatar):
            PtDebugPrint('DEBUG: xCalendarStar.OnNotify():\t received notify from non-local player, ignoring...')
            return 
        else:
            PtDebugPrint(('DEBUG: xCalendarStar.OnNotify():\t local player requesting %s change via %s' % (sdlCalStar.value,
             rgnCalStar.value[0].getName())))
        if (not self.GotPage()):
            print 'xCalendarStar.OnNotify(): do NOT have YeeshaPage26 (the Calendar Pinnacle) yet'
            return 
        else:
            print 'xCalendarStar.OnNotify():  have YeeshaPage26 (the Calendar Pinnacle)'
            if (AgeStartedIn == PtGetAgeName()):
                psnlSDL = xPsnlVaultSDL()
                if (not boolCalStar):
                    print "xCalendarStar.OnNotify(): getting star's stone: ",
                    print sdlCalStar.value
                    psnlSDL[sdlCalStar.value] = (1,)
                    respCalStar.run(self.key)
                    boolCalStar = 1
                    PtSendKIMessageInt(kStartBookAlert, 0)
            else:
                print 'xCalendarStar.OnNotify(): already have the stone: ',
                print sdlCalStar.value



    def GotPage(self):
        vault = ptVault()
        if (type(vault) != type(None)):
            psnlSDL = vault.getPsnlAgeSDL()
            if psnlSDL:
                ypageSDL = psnlSDL.findVar('YeeshaPage26')
                if ypageSDL:
                    (size, state,) = divmod(ypageSDL.getInt(), 10)
                    print 'YeeshaPage26 = ',
                    print state
                    if state:
                        return 1
            return 0


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



