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
import whrandom
respSpawnPt = ptAttribResponder(1, 'resp: Spawn Point', ['0', '1', '2'], netForce=1)
respMonkeyAct = ptAttribResponder(2, 'resp: Monkey Actions', ['Alarmed', 'Up', 'Eat', 'Idle', 'Vocalize'])
respMonkeySfx = ptAttribNamedResponder(3, 'resp: Monkey SFX', ['Alarmed', 'Up', 'Eat', 'Idle', 'Off', 'Vocalize'], netForce=1)
respMonkeyOff = ptAttribResponder(4, 'resp: Monkey Off')
kDayLengthInSeconds = 56585
kMinimumTimeBetweenSpawns = 300
kMaximumTimeBetweenSpawns = 18000
IdlePct = 30
EatPct = 20
VocalizePct = 20
AlarmedPct = 10
OffPct = 20
stackList = []
class nglnTreeMonkey(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5241
        version = 3
        self.version = version
        print '__init__nglnTreeMonkey v.',
        print version,
        print '.0'



    def OnFirstUpdate(self):
        whrandom.seed()



    def OnServerInitComplete(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            print 'nglnTreeMonkey:\tERROR---Cannot find the Negilahn Age SDL'
            self.InitNewSDLVars()
        ageSDL.sendToClients('MonkeyLastUpdated')
        ageSDL.sendToClients('MonkeySpawnTimes')
        ageSDL.setFlags('MonkeyLastUpdated', 1, 1)
        ageSDL.setFlags('MonkeySpawnTimes', 1, 1)
        ageSDL.setNotify(self.key, 'MonkeyLastUpdated', 0.0)
        ageSDL.setNotify(self.key, 'MonkeySpawnTimes', 0.0)
        thisDay = int((PtGetDniTime() / kDayLengthInSeconds))
        lastDay = int((ageSDL['MonkeyLastUpdated'][0] / kDayLengthInSeconds))
        if ((thisDay - lastDay) > 0):
            print "nglnTreeMonkey: It's been at least a day since the last update, running new numbers now."
            self.InitNewSDLVars()
        else:
            print "nglnTreeMonkey: It's been less than a day since the last update, doing nothing"
            self.SetMonkeyTimers()
        if (not len(PtGetPlayerList())):
            respMonkeyOff.run(self.key, fastforward=1)



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname == 'MonkeySpawnTimes'):
            self.SetMonkeyTimers()



    def OnNotify(self, state, id, events):
        print ('nglnTreeMonkey.OnNotify:  state=%f id=%d events=' % (state,
         id)),
        print events
        if (id == -1):
            print ('Need to store event: %s' % events[0][1])
            stackList.append(events[0][1])
            print ('New list is: %s' % str(stackList))
            if (len(stackList) == 1):
                print "List is only one command long, so I'm playing it"
                code = stackList[0]
                print ('Playing command: %s' % code)
                exec code
        elif ((id == respMonkeyAct.id) and self.sceneobject.isLocallyOwned()):
            print 'Callback was from responder, and I own the age, so Logic Time'
            old = stackList.pop(0)
            print ('Popping off: %s' % old)
            self.RandomBehavior()
        elif ((id == respMonkeyOff.id) and self.sceneobject.isLocallyOwned()):
            print "Callback was from 'Off' responder"
            old = stackList.pop(0)
            print ('Popping off: %s' % old)
        elif (((id == respMonkeyAct.id) or (id == respMonkeyOff.id)) and (not self.sceneobject.isLocallyOwned())):
            print "Callback was from responder, and I DON'T own the age, so I'll try playing the next item in list"
            old = stackList.pop(0)
            print ('Popping off: %s' % old)
            if len(stackList):
                print 'List has at least one item ready to play'
                code = stackList[0]
                print ('Playing command: %s' % code)
                exec code
        else:
            print 'Callback from something else?'



    def RandomBehavior(self):
        ageSDL = PtGetAgeSDL()
        PickABehavior = whrandom.randint(1, 100)
        LightsOn = ageSDL['nglnPodLights'][0]
        posMonkeyStates = ['Idle',
         'Eat',
         'Alarmed',
         'Vocalize',
         'Off']
        Cumulative = 0
        for MonkeyState in posMonkeyStates:
            NewCumulative = eval((('Cumulative + ' + MonkeyState) + 'Pct'))
            if ((PickABehavior > Cumulative) and (PickABehavior <= NewCumulative)):
                if (MonkeyState == 'Off'):
                    self.SendNote('respMonkeyOff.run(self.key)')
                else:
                    respString = (("respMonkeyAct.run(self.key, state='" + str(MonkeyState)) + "')")
                    self.SendNote(respString)
                print ('nglnTreeMonkey: Attempting Tree Monkey Anim: %s' % MonkeyState)
                if LightsOn:
                    respMonkeySfx.run(self.key, state=str(MonkeyState))
                    print ('nglnTreeMonkey: Attempting Tree Monkey SFX: %s' % MonkeyState)
                return 
            Cumulative = eval((('Cumulative + ' + MonkeyState) + 'Pct'))




    def SendNote(self, ExtraInfo):
        notify = ptNotify(self.key)
        notify.clearReceivers()
        notify.addReceiver(self.key)
        notify.netPropagate(1)
        notify.netForce(1)
        notify.setActivate(1.0)
        notify.addVarNumber(str(ExtraInfo), 1.0)
        notify.send()



    def MonkeyAppears(self):
        whichtree = whrandom.randint(0, 2)
        respSpawnPt.run(self.key, state=str(whichtree))
        self.SendNote("respMonkeyAct.run(self.key, state='Up')")
        print ('nglnTreeMonkey: Tree Monkey is climbing Tree: %d' % whichtree)



    def OnTimer(self, TimerID):
        print ('nglnTreeMonkey.OnTimer: callback id=%d' % TimerID)
        if self.sceneobject.isLocallyOwned():
            if (TimerID == 1):
                self.MonkeyAppears()
            elif (TimerID == 2):
                self.InitNewSDLVars()



    def InitNewSDLVars(self):
        ageSDL = PtGetAgeSDL()
        ageSDL['MonkeyLastUpdated'] = (PtGetDniTime(),)
        beginningOfToday = (PtGetDniTime() - int((PtGetAgeTimeOfDayPercent() * kDayLengthInSeconds)))
        endOfToday = (int((kDayLengthInSeconds / 2)) + beginningOfToday)
        randnum = float(whrandom.randint(0, 318))
        firstTime = (int(((randnum / 1000.0) * kDayLengthInSeconds)) + beginningOfToday)
        print ('nglnTreeMonkey: Generated a valid spawn time: %d' % firstTime)
        spawnTimes = [firstTime]
        while (type(spawnTimes[-1]) == type(long(1))):
            randnum = whrandom.randint(kMinimumTimeBetweenSpawns, kMaximumTimeBetweenSpawns)
            newTime = (spawnTimes[-1] + randnum)
            if (newTime < endOfToday):
                print ('nglnTreeMonkey: Generated a valid spawn time: %d' % newTime)
                spawnTimes.append(newTime)
            else:
                print ('nglnTreeMonkey: Generated a spawn time after dusk, exiting loop: %d' % newTime)
                break
        else:
            print "nglnTreeMonkey:ERROR---Tried to add a spawn time that's not a number: ",
            print spawnTimes
            spawnTimes = [0]

        while (len(spawnTimes) < 20):
            spawnTimes.append(0)

        ageSDL['MonkeySpawnTimes'] = tuple(spawnTimes)



    def SetMonkeyTimers(self):
        PtClearTimerCallbacks(self.key)
        ageSDL = PtGetAgeSDL()
        if ageSDL['MonkeySpawnTimes'][0]:
            for timer in ageSDL['MonkeySpawnTimes']:
                if timer:
                    timeTillSpawn = (timer - PtGetDniTime())
                    print ('timer: %d    time: %d    timeTillSpawn: %d' % (timer,
                     PtGetDniTime(),
                     timeTillSpawn))
                    if (timeTillSpawn > 0):
                        print ('nglnTreeMonkey: Setting timer for %d seconds' % timeTillSpawn)
                        PtAtTimeCallback(self.key, timeTillSpawn, 1)

            timeLeftToday = (kDayLengthInSeconds - int((PtGetAgeTimeOfDayPercent() * kDayLengthInSeconds)))
            timeLeftToday += 1
            print ('nglnTreeMonkey: Setting EndOfDay timer for %d seconds' % timeLeftToday)
            PtAtTimeCallback(self.key, timeLeftToday, 2)
        else:
            print 'nglnTreeMonkey: Timer array was empty!'



    def OnBackdoorMsg(self, target, param):
        if (target == 'monkey'):
            if self.sceneobject.isLocallyOwned():
                print 'nglnTreeMonkey.OnBackdoorMsg: Work!'
                if (param == 'up'):
                    self.SendNote("respMonkeyAct.run(self.key, state='Up')")
                elif (param == 'tree'):
                    self.MonkeyAppears()


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



