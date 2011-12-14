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
import string, time, math
variable = None
BooleanVARs = []
AgeStartedIn = None
islmDRCStageStateMaxINT = 2

def OutOfRange(VARname, NewSDLValue, myMaxINT):
    PtDebugPrint(('islmEmgrPhase0.OutOfRange:\tERROR: Variable %s expected range from  0 - %d. Received value of %d' % (VARname, NewSDLValue, myMaxINT)))


def DRCStageState(VARname, NewSDLValue):
    if (NewSDLValue > islmDRCStageStateMaxINT):
        OutOfRange(VARname, NewSDLValue, islmDRCStageStateMaxINT)
    elif (NewSDLValue == 0):
        PtDebugPrint('islmEmgrPhase0.DRCStageState: paging out DRC stage')
        PtPageOutNode('islmDRCStageState01')
        PtPageOutNode('islmDRCStageState02')
    elif (NewSDLValue == 1):
        PtDebugPrint('islmEmgrPhase0.DRCStageState: paging in DRC stage')
        PtPageOutNode('islmDRCStageState02')
        PtPageInNode('islmDRCStageState01')
    elif (NewSDLValue == 2):
        PtDebugPrint('islmEmgrPhase0.DRCStageState: paging in deco DRC stage')
        PtPageInNode('islmDRCStageState01')
        PtPageInNode('islmDRCStageState02')
    else:
        PtDebugPrint(('islmEmgrPhase0.DRCStageState: \tERROR: Unexpected value. VARname: %s NewSDLValue: %s' % (VARname, NewSDLValue)))

StateVARs = {
    'islmDRCStageState': DRCStageState
}

def ISetSeasonalStates():
    HourLength = 60*60
    DayLength = HourLength*24
    EpochDict = {2011: 1324422000,
        2012: 1355007600,
        2013: 1385593200,
        2014: 1418770800,
        2015: 1449442800,
        2016: 1482620400,
        2017: 1513119600,
        2018: 1543791600,
        2019: 1577055600,
        2020: 1607641200,
        2021: 1638140400,
        2022: 1671404400,
        2023: 1701990000,
        2024: 1735167600,
        2025: 1765753200}
    DniTime = PtGetDniTime()
#### Debug start
    ##check dates (see http://www.cuecalendar.com/holidays/JewishHolidays.htm): hmm, 1 hour off?
    #for yr in EpochDict:
    #    yrTime = time.strftime('%m/%d/%Y  %H:%M:%S', time.gmtime(EpochDict[yr]))
    #    print yrTime
    ##fake the time for testing purposes
    #DniTime = EpochDict[2011] - (5 * HourLength) + (8 * DayLength)
#### Debug end
    CurrentTime = time.strftime('Year %Y, Month %m, Day %d, Time %H:%M:%S', time.gmtime(DniTime))
    PtDebugPrint('islmEmgrPhase0.ISetSeasonalStates(): It is now: %s' % CurrentTime)
    # Hanukkah sometimes extends into January so we have to grab the "current" year from last month!
    PrevMonth = (DniTime - (31 * DayLength))
    Year = int(time.strftime('%Y', time.gmtime(PrevMonth)))
    if Year in EpochDict:
        ageSDL = PtGetAgeSDL()
        Epoch = EpochDict[Year]
        # Candles are lit shortly after sunset the PREVIOUS day, so we must subtract a few hours.
        Epoch = (Epoch - (5 * HourLength))
        # Delta in days, make sure it's a float!
        Delta = (float(DniTime - Epoch) / DayLength)
        # Let's see what we got
        HanukTime = time.strftime('Month %m, Day %d, Time %H:%M:%S', time.gmtime(Epoch))
        PtDebugPrint('islmEmgrPhase0.ISetSeasonalStates(): This year (%s) Hanukkah starts: %s. Delta = %f' % (Year, HanukTime, Delta))
        # Round upwards because anything between 0 and 1 counts as day 1, etc.
        Delta = math.ceil(Delta)
        if ((Delta < 0) or (Delta > 10)):
            # We could hide the menorah here but we won't
            #ageSDL['islmMinorahVis'] = (0,)
            # Just make sure the candles are out
            for i in range(1, 9):
                SDLname = ('islmMinorahNight0' + str(i) + 'Vis')
                ageSDL[SDLname] = (0,)
        else:
            ageSDL['islmMinorahVis'] = (1,)
            PtDebugPrint('islmEmgrPhase0.ISetSeasonalStates(): Menorah on. Sorting candles...')
            for i in range(1, 9):
                SDLname = ('islmMinorahNight0' + str(i) + 'Vis')
                if (Delta >= i):
                    print ('islmEmgrPhase0.ISetSeasonalStates(): Candle %d is on' % i)
                    ageSDL[SDLname] = (1,)
                else:
                    ageSDL[SDLname] = (0,)


class islmEmgrPhase0(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5223
        version = 2
        self.version = version
        print '__init__islmEmgrPhase0 v.',
        print version


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()


    def OnServerInitComplete(self):
        import xxConfig
        global AgeStartedIn
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            for variable in BooleanVARs:
                print 'tying together',
                print variable
                ageSDL.setNotify(self.key, variable, 0.0)
                self.IManageBOOLs(variable, '')
            for variable in StateVARs.keys():
                PtDebugPrint(('setting notify on %s' % variable))
                ageSDL.setNotify(self.key, variable, 0.0)
                StateVARs[variable](variable, ageSDL[variable][0])
        if xxConfig.isOnline() and not len(PtGetPlayerList()):
            ISetSeasonalStates()


    def OnSDLNotify(self, VARname, SDLname, PlayerID, tag):
        global AgeStartedIn
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            PtDebugPrint(('islmEmgrPhase0.SDLNotify - name = %s, SDLname = %s' % (VARname, SDLname)))
            if (VARname in BooleanVARs):
                print ('islmEmgrPhase0.OnSDLNotify : %s is a BOOLEAN Variable' % VARname)
                self.IManageBOOLs(VARname, SDLname)
            elif (VARname in StateVARs.keys()):
                PtDebugPrint(('islmEmgrPhas0.OnSDLNotify : %s is a STATE variable' % VARname))
                NewSDLValue = ageSDL[VARname][0]
                StateVARs[VARname](VARname, NewSDLValue)
            else:
                PtDebugPrint(('islmEmgrPhase0.OnSDLNotify:\tERROR: Variable %s was not recognized as a Boolean, Performance, or State Variable. ' % VARname))


    def IManageBOOLs(self, VARname, SDLname):
        global AgeStartedIn
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            if (ageSDL[VARname][0] == 1):
                PtDebugPrint('islmEmgrPhase0.OnSDLNotify:\tPaging in room ', VARname)
                PtPageInNode(VARname)
            elif (ageSDL[VARname][0] == 0):
                print 'variable = ',
                print VARname
                PtDebugPrint('islmEmgrPhase0.OnSDLNotify:\tPaging out room ', VARname)
                PtPageOutNode(VARname)
            else:
                sdlvalue = ageSDL[VARname][0]
                PtDebugPrint(('islmEmgrPhase0.OnSDLNotify:\tERROR: Variable %s had unexpected SDL value of %s' % (VARname, sdlvalue)))


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



