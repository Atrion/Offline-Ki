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
import xRandom

sdlS1FinaleBahro = ['islmS1FinaleBahro', 'islmS1FinaleBahroCity1', 'islmS1FinaleBahroCity2', 'islmS1FinaleBahroCity3', 'islmS1FinaleBahroCity4', 'islmS1FinaleBahroCity5', 'islmS1FinaleBahroCity6']
pagesS1FinaleBahro = ['bahroFlyers_arch', 'bahroFlyers_city1', 'bahroFlyers_city2', 'bahroFlyers_city3', 'bahroFlyers_city4', 'bahroFlyers_city5', 'bahroFlyers_city6']

kRandomBahro = 1 # timer ID
kRandomBahroTimeMin = 5
kRandomBahroTimeMax = 200
randomSDL = ['islmS1FinaleBahroCity1', 'islmS1FinaleBahroCity2', 'islmS1FinaleBahroCity3', 'islmS1FinaleBahroCity4', 'islmS1FinaleBahroCity5', 'islmS1FinaleBahroCity6', 'islmBahroShoutFerryRun', 'islmBahroShoutLibraryRun', 'islmBahroShoutPalaceRun']
randomEmptyEvents = 2 # chances are equally distributed to get one event out of the SDL changes and the n empty ones defined here


BahroShouterNames = {'islmBahroShoutLibraryRun': 10, 'islmBahroShoutPalaceRun': 11, 'islmBahroShoutFerryRun': 12} # the numbers are the timer IDs
BahorShouterTime = 10

SDLPages = {
    'islmLibraryBannersVis': ['islmLibBanners00Vis', 'islmLibBanners02Vis', 'islmLibBanners03Vis'],
    'islmLibraryBooksVis': ['LibraryAhnonayVis', 'LibraryGarrisonVis', 'LibraryKadishVis', 'LibraryTeledahnVis', 'LibraryErcanaVis']
}

kKadishDoorInit = 2 # timer ID


class city(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5026
        self.version = 1


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        try:
            n = 0
            for sdl in sdlS1FinaleBahro:
                ageSDL.setFlags(sdl, 1, 1)
                ageSDL.sendToClients(sdl)
                ageSDL.setNotify(self.key, sdl, 0.0)
                val = ageSDL[sdl][0]
                if val:
                    self.ILoadS1FinaleBahro(n, 1)
                n += 1
            PtAtTimeCallback(self.key, xRandom.randint(kRandomBahroTimeMin, kRandomBahroTimeMax), kRandomBahro)
        except:
            print "ERROR!  Couldn't find all Bahro sdl, leaving default = 0"
        for sdl in BahroShouterNames:
            ageSDL.setFlags(sdl, 1, 1)
            ageSDL.sendToClients(sdl)
            ageSDL.setNotify(self.key, sdl, 0.0)
            if ageSDL[sdl][0]: PtAtTimeCallback(self.key, BahorShouterTime, BahroShouterNames[sdl])
        for sdl in SDLPages:
            ageSDL.setFlags(sdl, 1, 1)
            ageSDL.sendToClients(sdl)
            ageSDL.setNotify(self.key, sdl, 0.0)
            if ageSDL[sdl][0]: PtPageInNode(SDLPages[sdl])
        # init Kadish doors
        import os
        if os.path.exists('dat/city_District_KadishGalleryDustAdditions.prp'):
            PtAtTimeCallback(self.key, 0.8, kKadishDoorInit)


    def OnTimer(self, id):
        ageSDL = PtGetAgeSDL()
        if id == kRandomBahro:
            if ageSDL['islmS1FinaleBahro'][0] and PtFindSceneobject('ArchOfKerath', PtGetAgeName()).isLocallyOwned():
                global randomSDL
                global randomEmptyEvents
                # only one player should really do something
                theBahro = xRandom.randint(1, len(randomSDL)+randomEmptyEvents)-1 # the array starts counting at 0
                if theBahro < len(randomSDL): # start a bahro!
                    bahroName = randomSDL[theBahro]
                    if not ageSDL[bahroName][0]:
                        ageSDL[bahroName] = (1,)
                        PtDebugPrint('city.OnTimer():\tStarted Bahro %s' % bahroName)
                    else:
                        PtDebugPrint('city.OnTimer():\tBahro %s is already running, doing nothing' % bahroName)
                else:
                    PtDebugPrint('city.OnTimer():\tNot starting any Bahro')
            else:
                PtDebugPrint('city.OnTimer():\tThe Bahro are disabled or someone else is responsible')
            PtAtTimeCallback(self.key, xRandom.randint(kRandomBahroTimeMin, kRandomBahroTimeMax), kRandomBahro)
        elif id == kKadishDoorInit:
            objectsToHide = ['Collider-GalleryDoor-TEMP',
                            'KdshGalleryDoor01',
                            'KdshGalleryDoor02',
                            'KdshGalleryDoorBtnInt01',
                            'KdshGalleryDoorBtnInt02',
                            'KdshGalleryDoorBtnExt01',
                            'KdshGalleryDoorBtnExt02',
                            'KdshGalleryDoorFrame01',
                            'KdshGalleryDoorFrame02']
            for object in objectsToHide:
                object = PtFindSceneobject(object, 'city')
                object.draw.disable()
                object.physics.suppress(True)
        else:
            for sdl in BahroShouterNames:
                if BahroShouterNames[sdl] == id:
                    ageSDL[sdl] = (0,)
                    break


    def Load(self):
        pass


    def OnNotify(self, state, id, events):
        pass


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        print (('city.OnSDLNotify():\t VARname: %s, SDLname: %s, tag: %s, value: %d' % (VARname, SDLname, tag, ageSDL[VARname][0])))
        if (VARname in sdlS1FinaleBahro):
            id = sdlS1FinaleBahro.index(VARname)
            val = ageSDL[sdlS1FinaleBahro[id]][0]
            self.ILoadS1FinaleBahro(id, val)
        elif VARname in BahroShouterNames and ageSDL[VARname][0]: PtAtTimeCallback(self.key, BahorShouterTime, BahroShouterNames[VARname])
        elif VARname in SDLPages:
            if ageSDL[VARname][0]: PtPageInNode(SDLPages[VARname])
            else:
                for page in SDLPages[VARname]: PtPageOutNode(page) # PtPageOutNode doesn't support lists


    def ILoadS1FinaleBahro(self, bahro, state):
        print ('city.ILoadS1FinaleBahro(): bahro = %d, load = %d' % (bahro, state))
        if state:
            PtPageInNode(pagesS1FinaleBahro[bahro])
        else:
            PtPageOutNode(pagesS1FinaleBahro[bahro])


    def OnBackdoorMsg(self, target, param):
        if (target == 's1finale'):
            if ((param == 'on') or (param == '1')):
                n = 0
                for p in pagesS1FinaleBahro:
                    self.ILoadS1FinaleBahro(n, 1)
                    n += 1
            elif ((param == 'off') or (param == '0')):
                n = 0
                for p in pagesS1FinaleBahro:
                    self.ILoadS1FinaleBahro(n, 0)
                    n += 1


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



