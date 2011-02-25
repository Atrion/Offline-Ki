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
from xPsnlVaultSDL import *
clkBSTsogal = ptAttribActivator(1, 'clk: Tsogal Blue Spiral')
clkBSDelin = ptAttribActivator(2, 'clk: Delin Blue Spiral')
respWedges = ptAttribResponder(3, 'resp: Ground Wedges', ['Delin', 'Tsogal'])
respRings = ptAttribResponder(4, 'resp: Floating Rings', ['Delin', 'Tsogal'])
class bhroBahroBlueSpiral(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 8813
        self.version = 1
        print ('bhroBahroBlueSpiral: init  version = %d' % self.version)



    def __del__(self):
        pass


    def OnFirstUpdate(self):
        global gAgeStartedIn
        gAgeStartedIn = PtGetAgeName()
        PtSendKIMessage(kDisableYeeshaBook, 0)



    def OnServerInitComplete(self):
        ageFrom = PtGetPrevAgeName()
        print ('bhroBahroBlueSpiral.OnServerInitComplete: Came from %s, running opposite responder state' % ageFrom)
        if (ageFrom == 'EderTsogal'):
            respWedges.run(self.key, state='Delin', fastforward=1)
        elif (ageFrom == 'EderDelin'):
            respWedges.run(self.key, state='Tsogal', fastforward=1)
        psnlSDL = xPsnlVaultSDL()
        if psnlSDL['psnlBahroWedge05'][0]:
            respRings.run(self.key, state='Delin', fastforward=1)
        if psnlSDL['psnlBahroWedge06'][0]:
            respRings.run(self.key, state='Tsogal', fastforward=1)
        # platform collision fix
        platforms = {
            'EderDelin': 'Wedge-GarrisonExclude',
            'EderTsogal': 'Wedge-TeledahnExclude'
        }
        for age in platforms.keys():
            if age != ageFrom:
                PtFindSceneobject(platforms[age], 'LiveBahroCaves').physics.suppress(1)



    def OnNotify(self, state, id, events):
        if ((id == clkBSTsogal.id) and (not state)):
            print 'bhroBahroBlueSpiral.OnNotify: clicked Tsogal Spiral'
            respRings.run(self.key, state='Tsogal', avatar=PtFindAvatar(events))
            psnlSDL = xPsnlVaultSDL()
            sdlVal = psnlSDL['psnlBahroWedge06'][0]
            if (not sdlVal):
                print 'bhroBahroBlueSpiral.OnNotify:  Tturning wedge SDL of psnlBahroWedge06 to On'
                psnlSDL['psnlBahroWedge06'] = (1,)
        elif ((id == clkBSDelin.id) and (not state)):
            print 'bhroBahroBlueSpiral.OnNotify: clicked Delin Spiral'
            respRings.run(self.key, state='Delin', avatar=PtFindAvatar(events))
            psnlSDL = xPsnlVaultSDL()
            sdlVal = psnlSDL['psnlBahroWedge05'][0]
            if (not sdlVal):
                print 'bhroBahroBlueSpiral.OnNotify:  Tturning wedge SDL of psnlBahroWedge05 to On'
                psnlSDL['psnlBahroWedge05'] = (1,)


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



