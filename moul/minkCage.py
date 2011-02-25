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
regCageSymbol = ptAttribActivator(1, 'reg: Cage Symbol')
respCageSymbol = ptAttribResponder(15, 'resp: Cage Symbol', ['1', '2', '3', '4', '5', 'Link', 'Hide'])
respSymbolSFX = ptAttribResponder(16, 'resp: Symbol SFX', ['0', '1', '2', '3', '4', '5'])
class minkCage(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5261
        version = 2
        self.version = version
        print '__init__minkCage v.',
        print version,
        print '.0'



    def OnFirstUpdate(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            print 'minkCage.OnFirstUpdate(): ERROR --- Cannot find Minkata age SDL'
        ageSDL.setFlags('minkSymbolPart01', 1, 1)
        ageSDL.setFlags('minkSymbolPart02', 1, 1)
        ageSDL.setFlags('minkSymbolPart03', 1, 1)
        ageSDL.setFlags('minkSymbolPart04', 1, 1)
        ageSDL.setFlags('minkSymbolPart05', 1, 1)
        ageSDL.sendToClients('minkSymbolPart01')
        ageSDL.sendToClients('minkSymbolPart02')
        ageSDL.sendToClients('minkSymbolPart03')
        ageSDL.sendToClients('minkSymbolPart04')
        ageSDL.sendToClients('minkSymbolPart05')
        ageSDL.setNotify(self.key, 'minkSymbolPart01', 0.0)
        ageSDL.setNotify(self.key, 'minkSymbolPart02', 0.0)
        ageSDL.setNotify(self.key, 'minkSymbolPart03', 0.0)
        ageSDL.setNotify(self.key, 'minkSymbolPart04', 0.0)
        ageSDL.setNotify(self.key, 'minkSymbolPart05', 0.0)
        print 'minkCage.OnFirstUpdate(): Hiding all Cage Symbol pieces'
        respCageSymbol.run(self.key, state='Hide')
        symbolCount = 0
        if ageSDL['minkSymbolPart01'][0]:
            print "minkCage.OnFirstUpdate(): You've found piece 1"
            respCageSymbol.run(self.key, state='1')
            symbolCount += 1
        if ageSDL['minkSymbolPart02'][0]:
            print "minkCage.OnFirstUpdate(): You've found piece 2"
            respCageSymbol.run(self.key, state='2')
            symbolCount += 1
        if ageSDL['minkSymbolPart03'][0]:
            print "minkCage.OnFirstUpdate(): You've found piece 3"
            respCageSymbol.run(self.key, state='3')
            symbolCount += 1
        if ageSDL['minkSymbolPart04'][0]:
            print "minkCage.OnFirstUpdate(): You've found piece 4"
            respCageSymbol.run(self.key, state='4')
            symbolCount += 1
        if ageSDL['minkSymbolPart05'][0]:
            print "minkCage.OnFirstUpdate(): You've found piece 5"
            respCageSymbol.run(self.key, state='5')
            symbolCount += 1
        PtDebugPrint(('DEBUG: minkCage.OnFirstUpdate():\tRunning SFX Level: %s' % symbolCount))
        respSymbolSFX.run(self.key, state=('%s' % symbolCount))
        if (ageSDL['minkSymbolPart01'][0] and (ageSDL['minkSymbolPart02'][0] and (ageSDL['minkSymbolPart03'][0] and (ageSDL['minkSymbolPart04'][0] and ageSDL['minkSymbolPart05'][0])))):
            print "minkCage.OnFirstUpdate(): You've found all the Pieces, enabling link"
            regCageSymbol.enable()



    def OnNotify(self, state, id, events):
        print ('minkCage.OnNotify(): state=%s id=%d events=' % (state,
         id)),
        print events
        if ((id == regCageSymbol.id) and (PtFindAvatar(events) == PtGetLocalAvatar())):
            print 'minkCage.OnNotify(): Linking to bahro cave.'
            respCageSymbol.run(self.key, state='Link', avatar=PtGetLocalAvatar())



    def OnBackdoorMsg(self, target, param):
        if ((target.lower() == 'bahrocave') and self.sceneobject.isLocallyOwned()):
            respCageSymbol.run(self.key, state='1')
            respCageSymbol.run(self.key, state='2')
            respCageSymbol.run(self.key, state='3')
            respCageSymbol.run(self.key, state='4')
            respCageSymbol.run(self.key, state='5')
            regCageSymbol.enable()
        elif (target.lower() == 'resetsymbol'):
            PtDebugPrint("DEBUG: minkCage.OnBackdoorMsg('ResetSymbols'):\tResetting Bahro Cave Symbols...")
            respCageSymbol.run(self.key, state='Hide')
            ageSDL = PtGetAgeSDL()
            ageSDL['minkSymbolPart01'] = (0,)
            ageSDL['minkSymbolPart02'] = (0,)
            ageSDL['minkSymbolPart03'] = (0,)
            ageSDL['minkSymbolPart04'] = (0,)
            ageSDL['minkSymbolPart05'] = (0,)
            regCageSymbol.disable()


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



