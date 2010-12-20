# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from xPsnlVaultSDL import *
clkNegilahn = ptAttribActivator(1, 'clk: Negilahn Spiral')
clkDereno = ptAttribActivator(2, 'clk: Dereno Spiral')
clkPayiferen = ptAttribActivator(3, 'clk: Payiferen Spiral')
clkTetsonot = ptAttribActivator(4, 'clk: Tetsonot Spiral')
respWedges = ptAttribResponder(5, 'resp: Ground Wedges', ['Negilahn',
 'Dereno',
 'Payiferen',
 'Tetsonot'])
respNegilahnRing = ptAttribResponder(6, 'resp: Negilahn Floating Ring')
respDerenoRing = ptAttribResponder(7, 'resp: Dereno Floating Ring')
respPayiferenRing = ptAttribResponder(8, 'resp: Payiferen Floating Ring')
respTetsonotRing = ptAttribResponder(9, 'resp: Tetsonot Floating Ring')
class bhroBahroPod(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 8814
        self.version = 1
        print ('bhroBahroPod: init  version = %d' % self.version)



    def __del__(self):
        pass


    def OnFirstUpdate(self):
        global gAgeStartedIn
        gAgeStartedIn = PtGetAgeName()
        PtSendKIMessage(kDisableYeeshaBook, 0)



    def OnServerInitComplete(self):
        ageFrom = PtGetPrevAgeName()
        print ('bhroBahroPod.OnServerInitComplete: Came from %s, running opposite responder state' % ageFrom)
        if (ageFrom == 'Negilahn'):
            respWedges.run(self.key, state='Dereno', fastforward=1)
            respWedges.run(self.key, state='Payiferen', fastforward=1)
            respWedges.run(self.key, state='Tetsonot', fastforward=1)
        elif (ageFrom == 'Dereno'):
            respWedges.run(self.key, state='Negilahn', fastforward=1)
            respWedges.run(self.key, state='Payiferen', fastforward=1)
            respWedges.run(self.key, state='Tetsonot', fastforward=1)
        elif (ageFrom == 'Payiferen'):
            respWedges.run(self.key, state='Negilahn', fastforward=1)
            respWedges.run(self.key, state='Dereno', fastforward=1)
            respWedges.run(self.key, state='Tetsonot', fastforward=1)
        elif (ageFrom == 'Tetsonot'):
            respWedges.run(self.key, state='Negilahn', fastforward=1)
            respWedges.run(self.key, state='Dereno', fastforward=1)
            respWedges.run(self.key, state='Payiferen', fastforward=1)
        psnlSDL = xPsnlVaultSDL()
        print psnlSDL['psnlBahroWedge07'][0]
        print psnlSDL['psnlBahroWedge08'][0]
        print psnlSDL['psnlBahroWedge09'][0]
        print psnlSDL['psnlBahroWedge10'][0]
        if psnlSDL['psnlBahroWedge07'][0]:
            print 'bhroBahroPod.OnServerInitComplete: You have the Negilahn wedge, no need to display it.'
            respNegilahnRing.run(self.key, fastforward=1)
        if psnlSDL['psnlBahroWedge08'][0]:
            print 'bhroBahroPod.OnServerInitComplete: You have the Dereno wedge, no need to display it.'
            respDerenoRing.run(self.key, fastforward=1)
        if psnlSDL['psnlBahroWedge09'][0]:
            print 'bhroBahroPod.OnServerInitComplete: You have the Payiferen wedge, no need to display it.'
            respPayiferenRing.run(self.key, fastforward=1)
        if psnlSDL['psnlBahroWedge10'][0]:
            print 'bhroBahroPod.OnServerInitComplete: You have the Tetsonot wedge, no need to display it.'
            respTetsonotRing.run(self.key, fastforward=1)
        # platform collision fix
        platforms = {
            'Negilahn': 'Wedge-NglnExclude',
            'Dereno': 'Wedge-GardenExclude',
            'Payiferen': 'Wedge-TeledahnExclude',
            'Tetsonot': 'Wedge-GarrisonExclude'
        }
        for age in platforms.keys():
            if age != ageFrom:
                PtFindSceneobject(platforms[age], 'LiveBahroCaves').physics.suppress(1)



    def OnNotify(self, state, id, events):
        if ((id == clkNegilahn.id) and (not state)):
            print 'bhroBahroPod.OnNotify: clicked Negilahn Spiral'
            respNegilahnRing.run(self.key, avatar=PtFindAvatar(events))
            psnlSDL = xPsnlVaultSDL()
            sdlVal = psnlSDL['psnlBahroWedge07'][0]
            if (not sdlVal):
                print 'bhroBahroPod.OnNotify:  Turning wedge SDL of psnlBahroWedge07 to On'
                psnlSDL['psnlBahroWedge07'] = (1,)
        elif ((id == clkDereno.id) and (not state)):
            print 'bhroBahroPod.OnNotify: clicked Dereno Spiral'
            respDerenoRing.run(self.key, avatar=PtFindAvatar(events))
            psnlSDL = xPsnlVaultSDL()
            sdlVal = psnlSDL['psnlBahroWedge08'][0]
            if (not sdlVal):
                print 'bhroBahroPod.OnNotify:  Turning wedge SDL of psnlBahroWedge08 to On'
                psnlSDL['psnlBahroWedge08'] = (1,)
        elif ((id == clkPayiferen.id) and (not state)):
            print 'bhroBahroPod.OnNotify: clicked Payiferen Spiral'
            respPayiferenRing.run(self.key, avatar=PtFindAvatar(events))
            psnlSDL = xPsnlVaultSDL()
            sdlVal = psnlSDL['psnlBahroWedge09'][0]
            if (not sdlVal):
                print 'bhroBahroPod.OnNotify:  Turning wedge SDL of psnlBahroWedge09 to On'
                psnlSDL['psnlBahroWedge09'] = (1,)
        elif ((id == clkTetsonot.id) and (not state)):
            print 'bhroBahroPod.OnNotify: clicked Tetsonot Spiral'
            respTetsonotRing.run(self.key, avatar=PtFindAvatar(events))
            psnlSDL = xPsnlVaultSDL()
            sdlVal = psnlSDL['psnlBahroWedge10'][0]
            if (not sdlVal):
                print 'bhroBahroPod.OnNotify:  Turning wedge SDL of psnlBahroWedge10 to On'
                psnlSDL['psnlBahroWedge10'] = (1,)


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



