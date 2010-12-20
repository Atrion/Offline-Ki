# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import string
import xxConfig
iconStates = ['first',
 'second',
 'third',
 'fourth',
 'fifth',
 'sixth',
 'seventh']
sdlSaveCloth1 = ptAttribString(1, 'sdl: SaveCloth 1')
sdlSaveCloth2 = ptAttribString(2, 'sdl: SaveCloth 2')
sdlSaveCloth3 = ptAttribString(3, 'sdl: SaveCloth 3')
sdlSaveCloth4 = ptAttribString(4, 'sdl: SaveCloth 4')
sdlSaveCloth5 = ptAttribString(5, 'sdl: SaveCloth 5')
sdlSaveCloth6 = ptAttribString(6, 'sdl: SaveCloth 6')
sdlSaveCloth7 = ptAttribString(7, 'sdl: SaveCloth 7')
respIconStages = ptAttribResponder(8, 'resp: icon stages', statelist=iconStates)
rgnIconLinker = ptAttribActivator(9, 'rgn sns: icon linker')
boolFirstUpdate = ptAttribBoolean(10, 'Eval On First Update?', 0)
AgeStartedIn = None
listSDL = []
class xPotsSymbol(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 230
        self.version = 1
        print 'xPotsSymbol.__init__: v.',
        print self.version



    def OnFirstUpdate(self):
        global AgeStartedIn
        global listSDL
        AgeStartedIn = PtGetAgeName()
        if ((not ((type(sdlSaveCloth1.value) == type('')) and (sdlSaveCloth1.value != ''))) or ((not ((type(sdlSaveCloth2.value) == type('')) and (sdlSaveCloth2.value != ''))) or ((not ((type(sdlSaveCloth3.value) == type('')) and (sdlSaveCloth3.value != ''))) or ((not ((type(sdlSaveCloth4.value) == type('')) and (sdlSaveCloth4.value != ''))) or ((not ((type(sdlSaveCloth5.value) == type('')) and (sdlSaveCloth5.value != ''))) or ((not ((type(sdlSaveCloth6.value) == type('')) and (sdlSaveCloth6.value != ''))) or (not ((type(sdlSaveCloth7.value) == type('')) and (sdlSaveCloth7.value != ''))))))))):
            PtDebugPrint('ERROR: xPotsSymbol.OnFirstUpdate():\tERROR: missing a SDL var name')
        # Ercana is loaded dynamically
        if AgeStartedIn == 'Ercana': boolFirstUpdate.value = 1
        # END Ercana is loaded dynamically
        listSDL = [sdlSaveCloth1.value,
         sdlSaveCloth2.value,
         sdlSaveCloth3.value,
         sdlSaveCloth4.value,
         sdlSaveCloth5.value,
         sdlSaveCloth6.value,
         sdlSaveCloth7.value]
        print 'xPotsSymbol.OnFirstUpdate(): listSDL = ',
        print listSDL
        if boolFirstUpdate.value:
            self.Initialize()



    def OnServerInitComplete(self):
        if (not boolFirstUpdate.value):
            self.Initialize()



    def Initialize(self):
        if (AgeStartedIn == PtGetAgeName()):
            try:
                ageSDL = PtGetAgeSDL()
                for sc in listSDL:
                    print ('xPotsSymbol.OnServerInitComplete():\t sdl: %s = %d' % (sc,
                     ageSDL[sc][0]))
                    ageSDL.setFlags(sc, 1, 1)
                    ageSDL.sendToClients(sc)
                    ageSDL.setNotify(self.key, sc, 0.0)

            except:
                #dustin
                #PtDebugPrint('ERROR: xPotsSymbol.OnServerInitComplete():\tERROR reading age SDL, ignoring script')
                print "xPotsSymbol: Dustin: skipping return to draw symbol anyway; alternatively we could just add the sdl vars."
                #return 
                #/dustin
            self.IUpdateIcon()



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            if (VARname in listSDL):
                PtDebugPrint(('DEBUG: xPotsSymbol.OnSDLNotify():\t VARname:%s, SDLname:%s, value:%d' % (VARname,
                 SDLname,
                 ageSDL[VARname][0])))
                if (ageSDL[VARname][0] == 1):
                    self.IUpdateIcon()



    def IUpdateIcon(self, ff = 0):
        ageSDL = PtGetAgeSDL()
        tallySC = 7
        print 'xPotsSymbol.IUpdateIcon(): total # of SaveCloths hit = ',
        print tallySC
        if (tallySC > 0):
            respIconStages.run(self.key, state=iconStates[(tallySC - 1)], fastforward=ff)
            print 'turning on POTS icon stage: ',
            print iconStates[(tallySC - 1)]
            if (tallySC == len(listSDL)):
                print 'POTS icon is completed, will enable link to POTS cave'
                rgnIconLinker.enable()



    def OnNotify(self, state, id, events):
        pass


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



