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
import string
import time
import xRandom
variable = None
BooleanVARs = ['nb01LinkBookGarrisonVis', 'nb01RatCreatureVis']
byteEderToggle = 0
sdlEderToggle = 'nb01LinkBookEderToggle'
sdlEderGlass = 'nb01StainedGlassEders'
byteEderGlass = 0
AgeStartedIn = None
sdlGZGlass = 'nb01StainedGlassGZ'
byteGZGlass = 0
numGZGlasses = 3
nb01Ayhoheek5Man1StateMaxINT = 2
nb01PuzzleWallStateMaxINT = 3

def OutOfRange(VARname, NewSDLValue, myMaxINT):
    PtDebugPrint(('ERROR: nb01EmgrPhase0.OutOfRange:\tERROR: Variable %s expected range from  0 - %d. Received value of %d' % (VARname, NewSDLValue, myMaxINT)))


def Ayhoheek5Man1State(VARname, NewSDLValue):
    if (NewSDLValue > nb01Ayhoheek5Man1StateMaxINT):
        OutOfRange(VARname, NewSDLValue, nb01Ayhoheek5Man1StateMaxINT)
    elif (NewSDLValue == 0):
        PtDebugPrint('DEBUG: nb01EmgrPhase0.Ayhoheek5Man1State:\t Paging out 5 Man Heek table completely.')
        PtPageOutNode('nb01MOULAyhoheek5Man1State')
        PtPageOutNode('nb01MOULAyhoheek5Man1Dead')
    elif (NewSDLValue == 1):
        PtDebugPrint('DEBUG: nb01EmgrPhase0.Ayhoheek5Man1State:\t Paging in broken 5 Man Heek table.')
        PtPageInNode('nb01MOULAyhoheek5Man1Dead')
        PtPageOutNode('nb01MOULAyhoheek5Man1State')
    elif (NewSDLValue == 2):
        PtDebugPrint('DEBUG: nb01EmgrPhase0.Ayhoheek5Man1State:\t Paging in functional 5 Man Heek table.')
        PtPageInNode('nb01MOULAyhoheek5Man1State')
        PtPageOutNode('nb01MOULAyhoheek5Man1Dead')
    else:
        PtDebugPrint(('ERROR: nb01EmgrPhase0.Ayhoheek5Man1State: \tERROR: Unexpected value. VARname: %s NewSDLValue: %s' % (VARname, NewSDLValue)))


def CityLightsArchState(VARname, NewSDLValue):
    print 'CityLightsArchiState Notified.'
    print 'VARname = ',
    print VARname
    print 'Received value is ',
    print NewSDLValue


def PuzzleWallState(VARname, NewSDLValue):
    print 'PuzzleWallState Notified.'
    print 'VARname = ',
    print VARname
    print 'Received value is ',
    print NewSDLValue


StateVARs = {
    'nb01Ayhoheek5Man1State': Ayhoheek5Man1State,
    'nb01PuzzleWallState': PuzzleWallState
}

class nb01EmgrPhase0(ptResponder):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5222
        version = 7
        self.version = version
        print '__init__nb01EmgrPhase0 v.',
        print version


    def OnFirstUpdate(self):
        global AgeStartedIn
        print 'nb01EmgrPhase0.OnFirstUpdate()'
        AgeStartedIn = PtGetAgeName()


    def OnServerInitComplete(self):
        global byteEderGlass
        global byteEderToggle
        global byteGZGlass
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(sdlEderToggle, 1, 1)
            ageSDL.sendToClients(sdlEderToggle)
            ageSDL.setNotify(self.key, sdlEderToggle, 0.0)
            byteEderToggle = ageSDL[sdlEderToggle][0]
            print 'nb01EmgrPhase0.OnServerInitComplete(): byteEderToggle = ',
            print byteEderToggle
            ageSDL.setFlags(sdlEderGlass, 1, 1)
            ageSDL.sendToClients(sdlEderGlass)
            ageSDL.setNotify(self.key, sdlEderGlass, 0.0)
            byteEderGlass = ageSDL[sdlEderGlass][0]
            print 'nb01EmgrPhase0.OnServerInitComplete(): byteEderGlass = ',
            print byteEderGlass
            ageSDL.setFlags(sdlGZGlass, 1, 1)
            ageSDL.sendToClients(sdlGZGlass)
            ageSDL.setNotify(self.key, sdlGZGlass, 0.0)
            byteGZGlass = ageSDL[sdlGZGlass][0]
            print 'nb01EmgrPhase0.OnServerInitComplete(): byteGZGlass = ',
            print byteGZGlass
            if self.sceneobject.isLocallyOwned():
                print 'nb01EmgrPhase0.OnServerInitComplete(): will check the Eder Delin/Tsogal book and its stained glass...'
                self.IManageEders()
            if ((byteGZGlass > numGZGlasses) and self.sceneobject.isLocallyOwned()):
                newGlass = xRandom.randint(1, numGZGlasses)
                print 'nb01EmgrPhase0.OnServerInitComplete():  GZ stained glass randomly picked to be #: ',
                print newGlass
                ageSDL = PtGetAgeSDL()
                ageSDL[sdlGZGlass] = (newGlass,)
            for variable in BooleanVARs:
                ageSDL.setNotify(self.key, variable, 0.0)
                self.IManageBOOLs(variable, '')

            for variable in StateVARs:
                ageSDL.setNotify(self.key, variable, 0.0)
                StateVARs[variable](variable, ageSDL[variable][0])



    def OnSDLNotify(self, VARname, SDLname, PlayerID, tag):
        global byteEderGlass
        global byteEderToggle
        global byteGZGlass
        ageSDL = PtGetAgeSDL()
        PtDebugPrint(('nb01EmgrPhase0.OnSDLNotify():\t VARname:%s, SDLname:%s, tag:%s, value:%d' % (VARname, SDLname, tag, ageSDL[VARname][0])))
        if (VARname in BooleanVARs):
            self.IManageBOOLs(VARname, SDLname)
        elif (VARname in StateVARs.keys()):
            if (AgeStartedIn == PtGetAgeName()):
                ageSDL = PtGetAgeSDL()
                NewSDLValue = ageSDL[VARname][0]
                StateVARs[VARname](VARname, NewSDLValue)
                print 'Sending new value',
                print NewSDLValue
        elif (VARname == sdlEderToggle):
            byteEderToggle = ageSDL[sdlEderToggle][0]
            print 'nb01EmgrPhase0.OnSDLNotify(): byteEderToggle = ',
            print byteEderToggle
        elif (VARname == sdlEderGlass):
            byteEderGlass = ageSDL[sdlEderGlass][0]
            print 'nb01EmgrPhase0.OnSDLNotify(): byteEderGlass = ',
            print byteEderGlass
        elif (VARname == sdlGZGlass):
            byteGZGlass = ageSDL[sdlGZGlass][0]
            print 'nb01EmgrPhase0.OnSDLNotify(): byteGZGlass = ',
            print byteGZGlass
        else:
            PtDebugPrint(('ERROR: nb01EmgrPhase0.OnSDLNotify:\tERROR: Variable %s was not recognized as a Boolean, Performance, or State Variable. ' % VARname))


    def IManageBOOLs(self, VARname, SDLname):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            try:
                if (ageSDL[VARname][0] == 1):
                    PtDebugPrint('DEBUG: nb01EmgrPhase0.IManageBOOLs:\tPaging in room ', VARname)
                    PtPageInNode(VARname)
                elif (ageSDL[VARname][0] == 0):
                    print 'variable = ',
                    print VARname
                    PtDebugPrint('DEBUG: nb01EmgrPhase0.IManageBOOLs:\tPaging out room ', VARname)
                    PtPageOutNode(VARname)
                else:
                    sdlvalue = ageSDL[VARname][0]
                    PtDebugPrint(('ERROR: nb01EmgrPhase0.IManageBOOLs:\tVariable %s had unexpected SDL value of %s' % (VARname, sdlvalue)))
            except:
                PtDebugPrint(('ERROR: nb01EmgrPhase0.IManageBOOLs: problem with %s' % VARname))


    def IManageEders(self, onInit = 0):
        print 'nb01EmgrPhase0.IManageEders(): byteEderToggle = ',
        print byteEderToggle,
        print '; byteEderGlass = ',
        print byteEderGlass
        if byteEderToggle:
            if ((byteEderToggle == 2) and (byteEderGlass not in (0, 1, 2, 3))):
                self.IPickEderGlass(2)
            elif ((byteEderToggle == 3) and (byteEderGlass not in (0, 4, 5, 6))):
                self.IPickEderGlass(3)
            elif (byteEderToggle not in (2, 3)):
                self.IPickEderBooks()
        elif byteEderGlass:
            self.IPickEderGlass(0)


    def IPickEderBooks(self):
        print 'nb01EmgrPhase0.IPickEderBooks()'
        newBook = xRandom.randint(2, 3)
        ageSDL = PtGetAgeSDL()
        ageSDL[sdlEderToggle] = (newBook,)
        self.IPickEderGlass(newBook)


    def IPickEderGlass(self, eder):
        print 'nb01EmgrPhase0.IPickEderGlass()'
        newGlass = 0
        if (eder == 2):
            newGlass = xRandom.randint(1, 3)
        elif (eder == 3):
            newGlass = xRandom.randint(4, 6)
        ageSDL = PtGetAgeSDL()
        ageSDL[sdlEderGlass] = (newGlass,)


    def OnBackdoorMsg(self, target, param):
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



