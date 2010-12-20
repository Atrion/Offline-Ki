# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import string
stringVarName = ptAttribString(1, 'Battery Updated SDL')
SunriseRGB = ptAttribString(2, 'Sunrise: (Red,Green,Blue)')
SunriseDensity = ptAttribString(3, 'Sunrise: (Start,End,Density)')
NoonRGB = ptAttribString(4, 'Noon: (Red,Green,Blue)')
NoonDensity = ptAttribString(5, 'Noon: (Start,End,Density)')
SunsetRGB = ptAttribString(6, 'Sunset: (Red,Green,Blue)')
SunsetDensity = ptAttribString(7, 'Sunset: (Start,End,Density)')
MidnightRGB = ptAttribString(8, 'Midnight: (Red,Green,Blue)')
MidnightDensity = ptAttribString(9, 'Midnight: (Start,End,Density)')
kSunrisePct = 0
kNoonPct = 0.25
kSunsetPct = 0.5
kMidnightPct = 0.75
SunriseR = 0
SunriseG = 0
SunriseB = 0
SunriseS = 0
SunriseE = 0
SunriseD = 0
NoonR = 0
NoonG = 0
NoonB = 0
NoonS = 0
NoonE = 0
NoonD = 0
SunsetR = 0
SunsetG = 0
SunsetB = 0
SunsetS = 0
SunsetE = 0
SunsetD = 0
MidnightR = 0
MidnightG = 0
MidnightB = 0
MidnightS = 0
MidnightE = 0
MidnightD = 0
StartR = 0
StartG = 0
StartB = 0
EndR = 0
EndG = 0
EndB = 0
StartS = 0
EndS = 0
StartE = 0
EndE = 0
StartD = 0
EndD = 0
class nglnFogTweener(ptMultiModifier,):


    def __init__(self):
        ptMultiModifier.__init__(self)
        self.id = 5243
        version = 3
        self.version = version
        print '__init__nglnFogTweener v.',
        print version
        self.SunriseRGBList = []
        self.SunriseDensityList = []
        self.NoonRGBList = []
        self.NoonDensityList = []
        self.SunsetRGBList = []
        self.SunsetDensityList = []
        self.MidnightRGBList = []
        self.MidnightDensityList = []



    def OnFirstUpdate(self):
        global SunsetS
        global SunsetR
        global MidnightB
        global SunsetB
        global SunsetE
        global SunsetD
        global SunsetG
        global MidnightD
        global MidnightE
        global SunriseB
        global MidnightG
        global SunriseG
        global SunriseE
        global SunriseD
        global NoonG
        global NoonE
        global NoonD
        global NoonB
        global SunriseS
        global SunriseR
        global MidnightS
        global MidnightR
        global NoonS
        global NoonR
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(stringVarName.value, 1, 1)
        ageSDL.sendToClients(stringVarName.value)
        self.SunriseRGBList = SunriseRGB.value.split(',')
        SunriseR = string.atof(self.SunriseRGBList[0])
        SunriseG = string.atof(self.SunriseRGBList[1])
        SunriseB = string.atof(self.SunriseRGBList[2])
        self.SunriseDensityList = SunriseDensity.value.split(',')
        SunriseS = string.atof(self.SunriseDensityList[0])
        SunriseE = string.atof(self.SunriseDensityList[1])
        SunriseD = string.atof(self.SunriseDensityList[2])
        self.NoonRGBList = NoonRGB.value.split(',')
        NoonR = string.atof(self.NoonRGBList[0])
        NoonG = string.atof(self.NoonRGBList[1])
        NoonB = string.atof(self.NoonRGBList[2])
        self.NoonDensityList = NoonDensity.value.split(',')
        NoonS = string.atof(self.NoonDensityList[0])
        NoonE = string.atof(self.NoonDensityList[1])
        NoonD = string.atof(self.NoonDensityList[2])
        self.SunsetRGBList = SunsetRGB.value.split(',')
        SunsetR = string.atof(self.SunsetRGBList[0])
        SunsetG = string.atof(self.SunsetRGBList[1])
        SunsetB = string.atof(self.SunsetRGBList[2])
        self.SunsetDensityList = SunsetDensity.value.split(',')
        SunsetS = string.atof(self.SunsetDensityList[0])
        SunsetE = string.atof(self.SunsetDensityList[1])
        SunsetD = string.atof(self.SunsetDensityList[2])
        self.MidnightRGBList = MidnightRGB.value.split(',')
        MidnightR = string.atof(self.MidnightRGBList[0])
        MidnightG = string.atof(self.MidnightRGBList[1])
        MidnightB = string.atof(self.MidnightRGBList[2])
        self.MidnightDensityList = MidnightDensity.value.split(',')
        MidnightS = string.atof(self.MidnightDensityList[0])
        MidnightE = string.atof(self.MidnightDensityList[1])
        MidnightD = string.atof(self.MidnightDensityList[2])
        print ('nglnFogTweener.OnFirstUpdate: SunriseRGB=(%s,%s,%s), NoonRGB=(%s,%s,%s), SunsetRGB=(%s,%s,%s), MidnightRGB=(%s,%s,%s) ' % (SunriseR,
         SunriseG,
         SunriseB,
         NoonR,
         NoonG,
         NoonB,
         SunsetR,
         SunsetG,
         SunsetB,
         MidnightR,
         MidnightG,
         MidnightB))
        print ('nglnFogTweener.OnFirstUpdate: SunriseDensity=(%s,%s,%s), NoonDensity=(%s,%s,%s), SunsetDensity=(%s,%s,%s), MidnightDensity=(%s,%s,%s) ' % (SunriseS,
         SunriseE,
         SunriseD,
         NoonS,
         NoonE,
         NoonD,
         SunsetS,
         SunsetE,
         SunsetD,
         MidnightS,
         MidnightE,
         MidnightD))



    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        ageSDL.setNotify(self.key, stringVarName.value, 0.0)
        self.CalculateNewFogValues()



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname != stringVarName.value):
            return 
        else:
            self.CalculateNewFogValues()



    def CalculateNewFogValues(self):
        global EndS
        global EndR
        global StartR
        global StartS
        global EndB
        global EndE
        global EndD
        global EndG
        global StartB
        global StartG
        global StartD
        global StartE
        AgeTimeOfDayPercent = PtGetAgeTimeOfDayPercent()
        print ('nglnFogTweener: The day is %.2f%% through its complete cycle.' % (AgeTimeOfDayPercent * 100))
        if ((AgeTimeOfDayPercent > kSunrisePct) and (AgeTimeOfDayPercent < kNoonPct)):
            StartR = SunriseR
            EndR = NoonR
            StartG = SunriseG
            EndG = NoonG
            StartB = SunriseB
            EndB = NoonB
            StartS = SunriseS
            EndS = NoonS
            StartE = SunriseE
            EndE = NoonE
            StartD = SunriseD
            EndD = NoonD
            TweenPct = ((AgeTimeOfDayPercent - kSunrisePct) / (kNoonPct - kSunrisePct))
            print ("\tIt's after Sunrise and before Noon. (%.2f%% through this quadrant)" % (TweenPct * 100))
        elif ((AgeTimeOfDayPercent > kNoonPct) and (AgeTimeOfDayPercent < kSunsetPct)):
            StartR = NoonR
            EndR = SunsetR
            StartG = NoonG
            EndG = SunsetG
            StartB = NoonB
            EndB = SunsetB
            StartS = NoonS
            EndS = SunsetS
            StartE = NoonE
            EndE = SunsetE
            StartD = NoonD
            EndD = SunsetD
            TweenPct = ((AgeTimeOfDayPercent - kNoonPct) / (kSunsetPct - kNoonPct))
            print ("\tIt's after Noon and before Sunset. (%.2f%% this quadrant)" % (TweenPct * 100))
        elif ((AgeTimeOfDayPercent > kSunsetPct) and (AgeTimeOfDayPercent < kMidnightPct)):
            StartR = SunsetR
            EndR = MidnightR
            StartG = SunsetG
            EndG = MidnightG
            StartB = SunsetB
            EndB = MidnightB
            StartS = SunsetS
            EndS = MidnightS
            StartE = SunsetE
            EndE = MidnightE
            StartD = SunsetD
            EndD = MidnightD
            TweenPct = ((AgeTimeOfDayPercent - kSunsetPct) / (kMidnightPct - kSunsetPct))
            print ("\tIt's after Sunset and before Midnight. (%.2f%% this quadrant)" % (TweenPct * 100))
        elif ((AgeTimeOfDayPercent > kMidnightPct) and (AgeTimeOfDayPercent < 1)):
            StartR = MidnightR
            EndR = SunriseR
            StartG = MidnightG
            EndG = SunriseG
            StartB = MidnightB
            EndB = SunriseB
            StartS = MidnightS
            EndS = SunriseS
            StartE = MidnightE
            EndE = SunriseE
            StartD = MidnightD
            EndD = SunriseD
            TweenPct = ((AgeTimeOfDayPercent - kMidnightPct) / (1 - kMidnightPct))
            print ("\tIt's after Midnight and before Sunrise. (%.2f%% this quadrant)" % (TweenPct * 100))
        else:
            print "ERROR: I can't tell what time it is."
        self.UpdateFog(StartR, EndR, StartG, EndG, StartB, EndB, StartS, EndS, StartE, EndE, StartD, EndD, TweenPct)



    def UpdateFog(self, StartR, EndR, StartG, EndG, StartB, EndB, StartS, EndS, StartE, EndE, StartD, EndD, TweenPct):
        print ('UpdateFog: StartR=%s, EndR=%s, StartG=%s, EndG=%s, StartB=%s, EndB=%s' % (StartR,
         EndR,
         StartG,
         EndG,
         StartB,
         EndB))
        print ('UpdateFog: StartS=%s, EndS=%s, StartE=%s, EndE=%s, StartD=%s, EndD=%s' % (StartS,
         EndS,
         StartE,
         EndE,
         StartD,
         EndD))
        NewR = (StartR + ((EndR - StartR) * TweenPct))
        NewG = (StartG + ((EndG - StartG) * TweenPct))
        NewB = (StartB + ((EndB - StartB) * TweenPct))
        NewS = (StartS + ((EndS - StartS) * TweenPct))
        NewE = (StartE + ((EndE - StartE) * TweenPct))
        NewD = (StartD + ((EndD - StartD) * TweenPct))
        print ('UpdateFog: The new fog RGB is (%.3f, %.3f, %.3f)' % (NewR,
         NewG,
         NewB))
        print ('UpdateFog: The new fog Density is (%.3f, %.3f, %.3f)' % (NewS,
         NewE,
         NewD))
        newfogcolor = ptColor(red=NewR, green=NewG, blue=NewB)
        PtFogSetDefColor(newfogcolor)
        PtFogSetDefLinear(NewS, NewE, NewD)


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



