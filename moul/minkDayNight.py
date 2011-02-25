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
import minkDustglobal
respLinkIn = ptAttribResponder(1, 'resp: Link In Sound')
respExcludeRegion = ptAttribResponder(2, 'resp: Exclude Regions', ['Clear', 'Release'])
HackIt = 1
class minkDayNight(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5258
        version = 1
        self.version = version
        print '__init__minkDayNight v.',
        print version,
        print '.0'



    def OnServerInitComplete(self):
        try:
            ageSDL = PtGetAgeSDL()
            ageSDL['minkIsDayTime'][0]
        except:
            print 'minkDayNight.OnServerInitComplete(): ERROR --- Cannot find Minkata age SDL'
            ageSDL['minkIsDayTime'] = (1,)
        ageSDL.setFlags('minkIsDayTime', 1, 1)
        ageSDL.sendToClients('minkIsDayTime')
        ageSDL.setNotify(self.key, 'minkIsDayTime', 0.0)
        if (not len(PtGetPlayerList())):
            ageSDL['minkIsDayTime'] = (1,)
        if ageSDL['minkIsDayTime'][0]:
            print "minkDayNight.OnServerInitComplete(): It's Day Time, Loading Day Page"
            PtPageInNode('minkExteriorDay')
            minkDustglobal.minkShowDayClusters(1)
            minkDustglobal.minkShowNightClusters(0)
        else:
            print "minkDayNight.OnServerInitComplete(): It's Night Time, Loading Night Page"
            PtPageInNode('minkExteriorNight')
            minkDustglobal.minkShowNightClusters(1)
            minkDustglobal.minkShowDayClusters(0)



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        print ('minkDayNight.OnSDLNotify(): VARname:%s, SDLname:%s, tag:%s, value:%s, playerID:%d' % (VARname,
         SDLname,
         tag,
         ageSDL[VARname][0],
         playerID))
        if ((VARname == 'minkIsDayTime') and (not HackIt)):
            print 'minkDayNight.OnSDLNotify(): SDL Updated, Fading Screen'
            PtDisableMovementKeys()
            PtSendKIMessage(kDisableKIandBB, 0)
            PtFadeOut(1.5, 1)
            PtAtTimeCallback(self.key, 1.75, 3)
            PtAtTimeCallback(self.key, 2.0, 1)



    def OnTimer(self, id):
        if (id == 1):
            ageSDL = PtGetAgeSDL()
            if ageSDL['minkIsDayTime'][0]:
                print 'minkDayNight.OnTimer(): Paging in Day Page'
                PtPageInNode('minkExteriorDay')
                minkDustglobal.minkShowDayClusters(1)
            else:
                print 'minkDayNight.OnTimer(): Paging in Night Page'
                PtPageInNode('minkExteriorNight')
                minkDustglobal.minkShowNightClusters(1)
        elif (id == 2):
            print 'minkDayNight.OnTimer(): Finished faux link, Re-enable controls'
            PtEnableMovementKeys()
            PtSendKIMessage(kEnableKIandBB, 0)
        elif (id == 3):
            PtFadeOut(0.0, 1)
            respExcludeRegion.run(self.key, state='Clear')



    def OnPageLoad(self, what, who):
        global HackIt
        print ('minkDayNight.OnPageLoad(): what=%s who=%s' % (what,
         who))
        if (what == kLoaded):
            if ((who == 'Minkata_District_minkExteriorDay') or (who == 'Minkata_minkExteriorDay')):
                if HackIt:
                    HackIt = 0
                    return 
                print 'minkDayNight.OnPageLoad(): Day Page loaded, unloading Night'
                PtPageOutNode('minkExteriorNight')
                minkDustglobal.minkShowNightClusters(0)
            elif ((who == 'Minkata_District_minkExteriorNight') or (who == 'Minkata_minkExteriorNight')):
                if HackIt:
                    HackIt = 0
                    return 
                print 'minkDayNight.OnPageLoad(): Night Page loaded, unloading Day'
                PtPageOutNode('minkExteriorDay')
                minkDustglobal.minkShowDayClusters(0)
        elif (what == kUnloaded):
            if ((who == 'Minkata_District_minkExteriorDay') or ((who == 'Minkata_District_minkExteriorNight') or ((who == 'Minkata_minkExteriorDay') or (who == 'Minkata_minkExteriorNight')))):
                print 'minkDayNight.OnPageLoad(): Page unloaded, Fading screen back in'
                PtFadeIn(1.5, 1)
                respExcludeRegion.run(self.key, state='Release')
                PtAtTimeCallback(self.key, 2, 2)
                respLinkIn.run(self.key)



    def OnBackdoorMsg(self, target, param):
        if ((target == 'switch') and self.sceneobject.isLocallyOwned()):
            ageSDL = PtGetAgeSDL()
            ageSDL['minkIsDayTime'] = ((not ageSDL['minkIsDayTime'][0]),)


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



