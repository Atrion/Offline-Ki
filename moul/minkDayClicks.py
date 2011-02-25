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
clkCave01 = ptAttribActivator(1, 'clk: Cave 01', netForce=1)
clkCave02 = ptAttribActivator(2, 'clk: Cave 02', netForce=1)
clkCave03 = ptAttribActivator(3, 'clk: Cave 03', netForce=1)
clkCave04 = ptAttribActivator(4, 'clk: Cave 04', netForce=1)
clkCave05 = ptAttribActivator(5, 'clk: Cave 05', netForce=1)
clkCage = ptAttribActivator(6, 'clk: Cage', netForce=1)
behRespCave01 = ptAttribResponder(7, 'beh resp: Cave 01')
behRespCave02 = ptAttribResponder(8, 'beh resp: Cave 02')
behRespCave03 = ptAttribResponder(9, 'beh resp: Cave 03')
behRespCave04 = ptAttribResponder(10, 'beh resp: Cave 04')
behRespCave05 = ptAttribResponder(11, 'beh resp: Cave 05')
behRespCage = ptAttribResponder(12, 'beh resp: Cage')
ClickToResponder = {clkCave01.id: behRespCave01,
 clkCave02.id: behRespCave02,
 clkCave03.id: behRespCave03,
 clkCave04.id: behRespCave04,
 clkCave05.id: behRespCave05,
 clkCage.id: behRespCage}
ResponderId = [behRespCave01.id,
 behRespCave02.id,
 behRespCave03.id,
 behRespCave04.id,
 behRespCave05.id,
 behRespCage.id]
class minkDayClicks(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5259
        version = 1
        self.version = version
        print '__init__minkDayClicks v.',
        print version,
        print '.0'



    def OnFirstUpdate(self):
        ageSDL = PtGetAgeSDL()
        if ((not len(PtGetPlayerList())) and ageSDL['minkIsDayTime'][0]):
            print 'minkDayClicks.OnFirstUpdate(): Resetting Show and Touch vars.'
            ageSDL['minkSymbolShow01'] = (0,)
            ageSDL['minkSymbolShow02'] = (0,)
            ageSDL['minkSymbolShow03'] = (0,)
            ageSDL['minkSymbolShow04'] = (0,)
            ageSDL['minkSymbolShow05'] = (0,)
            ageSDL['minkSymbolTouch01'] = (0,)
            ageSDL['minkSymbolTouch02'] = (0,)
            ageSDL['minkSymbolTouch03'] = (0,)
            ageSDL['minkSymbolTouch04'] = (0,)
            ageSDL['minkSymbolTouch05'] = (0,)



    def OnNotify(self, state, id, events):
        print ('minkDayClicks.OnNotify(): state=%s id=%d events=' % (state,
         id)),
        print events
        if ((id in ClickToResponder.keys()) and (state and (PtFindAvatar(events) == PtGetLocalAvatar()))):
            print ('minkDayClicks.OnNotify(): Clicked on %d, running %d' % (id,
             ClickToResponder[id].id))
            LocalAvatar = PtFindAvatar(events)
            clkCave01.disable()
            clkCave02.disable()
            clkCave03.disable()
            clkCave04.disable()
            clkCave05.disable()
            clkCage.disable()
            ClickToResponder[id].run(self.key, avatar=LocalAvatar)
        elif (id in ResponderId):
            print 'minkDayClicks.OnNotify(): Responder Finished, Updating SDL'
            ageSDL = PtGetAgeSDL()
            ageSDL['minkIsDayTime'] = ((not ageSDL['minkIsDayTime'][0]),)
            if (id != behRespCage.id):
                num = (ResponderId.index(id) + 1)
                print ('minkDayClicks.OnNotify(): Should show %d' % num)
                code = ('ageSDL["minkSymbolShow0%d"] = (1,)' % num)
                exec code


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



