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
from xPsnlVaultSDL import *
import string
import xRandom
respCalStoneFire = ptAttribResponder(1, 'resp: cal stones active', ['on', 'off'])
respFireworksLaunch1 = ptAttribResponder(2, 'resp: fireworks launch 1', netForce=1)
respFireworksExplode1 = ptAttribResponder(3, 'resp: fireworks explode 1', netForce=1)
respFireworksLaunch2 = ptAttribResponder(4, 'resp: fireworks launch 2', netForce=1)
respFireworksExplode2 = ptAttribResponder(5, 'resp: fireworks explode 2', netForce=1)
respFireworksLaunch3 = ptAttribResponder(6, 'resp: fireworks launch 3', netForce=1)
respFireworksExplode3 = ptAttribResponder(7, 'resp: fireworks explode 3', netForce=1)
sdlCalStone01 = 'psnlCalendarStone01'
sdlCalStone02 = 'psnlCalendarStone02'
sdlCalStone03 = 'psnlCalendarStone03'
sdlCalStone04 = 'psnlCalendarStone04'
sdlCalStone05 = 'psnlCalendarStone05'
sdlCalStone06 = 'psnlCalendarStone06'
sdlCalStone07 = 'psnlCalendarStone07'
sdlCalStone08 = 'psnlCalendarStone08'
sdlCalStone09 = 'psnlCalendarStone09'
sdlCalStone10 = 'psnlCalendarStone10'
sdlCalStone11 = 'psnlCalendarStone11'
sdlCalStone12 = 'psnlCalendarStone12'
sdlCalStones = ['psnlCalendarStone01', 'psnlCalendarStone02', 'psnlCalendarStone03', 'psnlCalendarStone04', 'psnlCalendarStone05', 'psnlCalendarStone06', 'psnlCalendarStone07', 'psnlCalendarStone08', 'psnlCalendarStone09', 'psnlCalendarStone10', 'psnlCalendarStone11', 'psnlCalendarStone12']
kMinLaunchTime = 15
kMaxLaunchTime = 25
kMinExplodeTime = 10
kMaxExplodeTime = 20
fireworksTestMode = 0
fireworks = 0

class psnlCalendarStones(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5082
        self.version = 1
        PtDebugPrint(('__init__psnlCalendarStones v. %d' % self.version))


    def OnFirstUpdate(self):
        self.OnServerInitComplete()


    def OnServerInitComplete(self):
        global fireworks
        ageSDL = xPsnlVaultSDL(1)
        fire = 1
        for sdl in sdlCalStones:
            val = ageSDL[sdl][0]
            if (not val):
                fire = 0
                break
        if fire:
            try:
                CurrentValue = ageSDL['YeeshaPage26'][0]
            except:
                PtDebugPrint('psnlCalendarStones.OnServerInitComplete():\tERROR reading age SDLVar for YeeshaPage20. Assuming value = 0')
                CurrentValue = 0
            if (CurrentValue in [0, 2, 4]):
                print 'psnlCalendarStones.OnServerInitComplete():  don\'t have YeeshaPage20 on, no FIRE for you!'
                respCalStoneFire.run(self.key, state='off', fastforward=1)
            else:
                print 'psnlCalendarStones.OnServerInitComplete():  have all 12 calendar stones AND YeeshaPage20 is on, will give you FIRE!'
                fireworks = 1
                respCalStoneFire.run(self.key, state='on', fastforward=1)
                if (not self.sceneobject.isLocallyOwned()): # this will not work correctly when the owner links out later...
                    return 
                if (not fireworksTestMode):
                    self.DoFireworks(1, 1)
                    self.DoFireworks(3, 1)
                    self.DoFireworks(5, 1)
        else:
            print "psnlCalendarStones.OnServerInitComplete():  don't have all 12 calendar stones, no FIRE for you!"
            respCalStoneFire.run(self.key, state='off', fastforward=1)



    def OnNotify(self, state, id, events):
        pass


    def OnTimer(self, id):
        if ((not fireworks) and (not fireworksTestMode)):
            return 
        if (not self.sceneobject.isLocallyOwned()):
            return 
        if (id == 1):
            respFireworksLaunch1.run(self.key)
            self.DoFireworks(1, 2)
        elif (id == 2):
            respFireworksExplode1.run(self.key)
            if (not fireworksTestMode):
                self.DoFireworks(1, 1)
        elif (id == 3):
            respFireworksLaunch2.run(self.key)
            self.DoFireworks(3, 2)
        elif (id == 4):
            respFireworksExplode2.run(self.key)
            if (not fireworksTestMode):
                self.DoFireworks(3, 1)
        elif (id == 5):
            respFireworksLaunch3.run(self.key)
            self.DoFireworks(5, 2)
        elif (id == 6):
            respFireworksExplode3.run(self.key)
            if (not fireworksTestMode):
                self.DoFireworks(5, 1)


    def DoFireworks(self, rocket, stage):
        if (stage == 1):
            timer = self.GetLaunchTime()
        elif (stage == 2):
            timer = self.GetExplodeTime()
            rocket += 1
        PtAtTimeCallback(self.key, timer, rocket)


    def GetLaunchTime(self):
        timeLaunch = xRandom.randint(kMinLaunchTime, kMaxLaunchTime)
        return timeLaunch


    def GetExplodeTime(self):
        timeExplode = xRandom.randint(kMinExplodeTime, kMaxExplodeTime)
        timeExplode = (float(timeExplode) / 10)
        return timeExplode


    def OnBackdoorMsg(self, target, param):
        timer = float(param)
        if (target == 'fireworks1'):
            respFireworksLaunch1.run(self.key)
            print 'launch rocket 1'
            PtAtTimeCallback(self.key, timer, 2)
        elif (target == 'fireworks2'):
            respFireworksLaunch2.run(self.key)
            print 'launch rocket 2'
            PtAtTimeCallback(self.key, timer, 4)
        elif (target == 'fireworks3'):
            respFireworksLaunch3.run(self.key)
            print 'launch rocket 3'
            PtAtTimeCallback(self.key, timer, 6)
        elif (target == 'fireworksall'):
            respFireworksLaunch1.run(self.key)
            print 'launch rocket 1'
            PtAtTimeCallback(self.key, timer, 2)
            respFireworksLaunch2.run(self.key)
            print 'launch rocket 2'
            PtAtTimeCallback(self.key, timer, 4)
            respFireworksLaunch3.run(self.key)
            print 'launch rocket 3'
            PtAtTimeCallback(self.key, timer, 6)


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



