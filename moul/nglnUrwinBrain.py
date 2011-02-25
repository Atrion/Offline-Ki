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
UrwinMasterAnim = ptAttribAnimation(1, 'Urwin Master Anim', netForce=1)
respUrwinVocalize = ptAttribResponder(2, 'resp: Urwin Vocalize')
respUrwinIdle = ptAttribResponder(3, 'resp: Urwin Idles')
respUrwinIdleToWalk = ptAttribResponder(4, 'resp: Urwin Idle To Walk')
respUrwinWalkLoop = ptAttribResponder(5, 'resp: Urwin Walk Loop')
respUrwinWalkToIdle = ptAttribResponder(6, 'resp: Urwin Walk To Idle')
respUrwinEat = ptAttribResponder(7, 'resp: Urwin Eats')
respUrwinSfx = ptAttribNamedResponder(8, 'resp: Urwin SFX', ['Eat', 'Idle', 'IdleToWalk', 'WalkLoop', 'WalkToIdle', 'Vocalize', 'Distance', 'Appear'], netForce=1)
actUrwinPathEnd = ptAttribActivator(9, 'act: Urwin Path End')
kDayLengthInSeconds = 56585
kMinimumTimeBetweenSpawns = 3600
kMaximumTimeBetweenSpawns = 25200
kFirstMorningSpawn = 445
minsteps = 3
maxsteps = 10
StepsToTake = 0
stackList = []
class nglnUrwinBrain(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5244
        version = 4
        self.version = version
        print '__init__nglnUrwinBrain v.',
        print version,
        print '.0'



    def OnFirstUpdate(self):
        whrandom.seed()



    def OnServerInitComplete(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            print 'nglnUrwinBrain:\tERROR---Cannot find the Negilahn Age SDL'
            self.InitNewSDLVars()
        ageSDL.sendToClients('UrwinLastUpdated')
        ageSDL.sendToClients('UrwinSpawnTimes')
        ageSDL.sendToClients('UrwinOnTheProwl')
        ageSDL.setFlags('UrwinLastUpdated', 1, 1)
        ageSDL.setFlags('UrwinSpawnTimes', 1, 1)
        ageSDL.setFlags('UrwinOnTheProwl', 1, 1)
        ageSDL.setFlags('nglnPodLights', 1, 1)
        ageSDL.setNotify(self.key, 'UrwinLastUpdated', 0.0)
        ageSDL.setNotify(self.key, 'UrwinSpawnTimes', 0.0)
        ageSDL.setNotify(self.key, 'UrwinOnTheProwl', 0.0)
        ageSDL.setNotify(self.key, 'nglnPodLights', 0.0)
        thisDay = int((PtGetDniTime() / kDayLengthInSeconds))
        lastDay = int((ageSDL['UrwinLastUpdated'][0] / kDayLengthInSeconds))
        if ((thisDay - lastDay) > 0):
            print "nglnUrwinBrain: It's been at least a day since the last update, running new numbers now."
            self.InitNewSDLVars()
        else:
            print "nglnUrwinBrain: It's been less than a day since the last update, doing nothing"
            self.SetUrwinTimers()
        if (not len(PtGetPlayerList())):
            UrwinMasterAnim.animation.skipToBegin()



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname == 'UrwinSpawnTimes'):
            self.SetUrwinTimers()
        elif (VARname == 'nglnPodLights'):
            ageSDL = PtGetAgeSDL()
            if ((not ageSDL[VARname][0]) and ageSDL['UrwinOnTheProwl'][0]):
                respUrwinSfx.run(self.key, state='Idle')



    def OnNotify(self, state, id, events):
        global StepsToTake
        ageSDL = PtGetAgeSDL()
        print ('nglnUrwinBrain.OnNotify:  state=%f id=%d owned=%s prowl=%s events=' % (state,
         id,
         str(self.sceneobject.isLocallyOwned()),
         str(ageSDL['UrwinOnTheProwl'][0]))),
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
        elif (state and (self.sceneobject.isLocallyOwned() and ageSDL['UrwinOnTheProwl'][0])):
            if (id == respUrwinSfx.id):
                print 'Callback was from Appearance SFX, and I own the age, so start walking'
                self.StartToWalk()
            else:
                print 'Callback was from responder, and I own the age, so Logic Time'
                old = stackList.pop(0)
                print ('Popping off: %s' % old)
                boolBatteryChargedAndOn = ageSDL['nglnPodLights'][0]
                if (id == respUrwinIdleToWalk.id):
                    self.StartToWalk()
                elif (id == respUrwinWalkLoop.id):
                    StepsToTake = (StepsToTake - 1)
                    if StepsToTake:
                        if whrandom.randint(0, 9):
                            print ('Urwin will take %d more steps...' % StepsToTake)
                            self.SendNote('respUrwinWalkLoop.run(self.key)')
                            if boolBatteryChargedAndOn:
                                respUrwinSfx.run(self.key, state='WalkLoop')
                        else:
                            print 'Urwin is hungry and decides to eat'
                            self.SendNote('respUrwinEat.run(self.key)')
                            if boolBatteryChargedAndOn:
                                respUrwinSfx.run(self.key, state='Eat')
                    else:
                        print 'Urwin is tired and stops walking'
                        PtAtTimeCallback(self.key, 0.66600000000000004, 3)
                        self.SendNote('respUrwinWalkToIdle.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='WalkToIdle')
                elif (id == respUrwinEat.id):
                    print 'Urwin is done eating and continues walking'
                    self.SendNote('respUrwinWalkLoop.run(self.key)')
                    if boolBatteryChargedAndOn:
                        respUrwinSfx.run(self.key, state='WalkLoop')
                elif (id == respUrwinWalkToIdle.id):
                    self.RandomBehavior()
                elif ((id == respUrwinIdle.id) or (id == respUrwinVocalize.id)):
                    if whrandom.randint(0, 2):
                        self.RandomBehavior()
                    else:
                        print 'Urwin is rested and goes back to walking'
                        self.SendNote('respUrwinIdleToWalk.run(self.key)')
                        UrwinMasterAnim.animation.resume()
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='IdleToWalk')
                elif (id == actUrwinPathEnd.id):
                    print 'End of the line, Urwin!'
                    UrwinMasterAnim.animation.stop()
                    UrwinMasterAnim.animation.skipToTime(0)
                    ageSDL['UrwinOnTheProwl'] = (0,)
                    if boolBatteryChargedAndOn:
                        respUrwinSfx.run(self.key, state='Distance')
        elif ((id in range(2, 8)) and (not self.sceneobject.isLocallyOwned())):
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
        boolBatteryChargedAndOn = ageSDL['nglnPodLights'][0]
        if whrandom.randint(0, 2):
            print 'Urwin is being lazy and just idling'
            self.SendNote('respUrwinIdle.run(self.key)')
            if boolBatteryChargedAndOn:
                respUrwinSfx.run(self.key, state='Idle')
        else:
            print 'Urwin is calling home.'
            self.SendNote('respUrwinVocalize.run(self.key)')
            if boolBatteryChargedAndOn:
                respUrwinSfx.run(self.key, state='Vocalize')



    def StartToWalk(self):
        global StepsToTake
        ageSDL = PtGetAgeSDL()
        boolBatteryChargedAndOn = ageSDL['nglnPodLights'][0]
        StepsToTake = whrandom.randint(minsteps, maxsteps)
        print ('Urwin has decided to take %d steps.' % StepsToTake)
        self.SendNote('respUrwinWalkLoop.run(self.key)')
        UrwinMasterAnim.animation.resume()
        if boolBatteryChargedAndOn:
            respUrwinSfx.run(self.key, state='WalkLoop')



    def OnTimer(self, TimerID):
        ageSDL = PtGetAgeSDL()
        boolBatteryChargedAndOn = ageSDL['nglnPodLights'][0]
        if self.sceneobject.isLocallyOwned():
            if (TimerID == 1):
                print 'UrwinBrain.OnTimer: Time for the Urwin to return.'
                ageSDL['UrwinOnTheProwl'] = (1,)
                if ageSDL['nglnPodLights'][0]:
                    respUrwinSfx.run(self.key, state='Appear')
                else:
                    self.StartToWalk()
            elif (TimerID == 2):
                print "UrwinBrain.OnTimer: New day, let's renew the timers."
                self.InitNewSDLVars()
            elif (TimerID == 3):
                UrwinMasterAnim.animation.stop()



    def SendNote(self, ExtraInfo):
        notify = ptNotify(self.key)
        notify.clearReceivers()
        notify.addReceiver(self.key)
        notify.netPropagate(1)
        notify.netForce(1)
        notify.setActivate(1.0)
        notify.addVarNumber(str(ExtraInfo), 1.0)
        notify.send()



    def InitNewSDLVars(self):
        ageSDL = PtGetAgeSDL()
        ageSDL['UrwinLastUpdated'] = (PtGetDniTime(),)
        beginningOfToday = (PtGetDniTime() - int((PtGetAgeTimeOfDayPercent() * kDayLengthInSeconds)))
        endOfToday = (int((kDayLengthInSeconds / 2)) + beginningOfToday)
        randnum = float(whrandom.randint(0, kFirstMorningSpawn))
        firstTime = (int(((randnum / 1000.0) * kDayLengthInSeconds)) + beginningOfToday)
        print ('nglnUrwinBrain: Generated a valid spawn time: %d' % firstTime)
        spawnTimes = [firstTime]
        while (type(spawnTimes[-1]) == type(long(1))):
            randnum = whrandom.randint(kMinimumTimeBetweenSpawns, kMaximumTimeBetweenSpawns)
            newTime = (spawnTimes[-1] + randnum)
            if (newTime < endOfToday):
                print ('nglnUrwinBrain: Generated a valid spawn time: %d' % newTime)
                spawnTimes.append(newTime)
            else:
                print ('nglnUrwinBrain: Generated a spawn time after dusk, exiting loop: %d' % newTime)
                break
        else:
            print "nglnUrwinBrain:ERROR---Tried to add a spawn time that's not a number: ",
            print spawnTimes
            spawnTimes = [0]

        while (len(spawnTimes) < 20):
            spawnTimes.append(0)

        ageSDL['UrwinSpawnTimes'] = tuple(spawnTimes)



    def SetUrwinTimers(self):
        PtClearTimerCallbacks(self.key)
        ageSDL = PtGetAgeSDL()
        if ageSDL['UrwinSpawnTimes'][0]:
            for timer in ageSDL['UrwinSpawnTimes']:
                if timer:
                    timeTillSpawn = (timer - PtGetDniTime())
                    print ('timer: %d    time: %d    timeTillSpawn: %d' % (timer,
                     PtGetDniTime(),
                     timeTillSpawn))
                    if (timeTillSpawn > 0):
                        print ('nglnUrwinBrain: Setting timer for %d seconds' % timeTillSpawn)
                        PtAtTimeCallback(self.key, timeTillSpawn, 1)

            timeLeftToday = (kDayLengthInSeconds - int((PtGetAgeTimeOfDayPercent() * kDayLengthInSeconds)))
            timeLeftToday += 1
            print ('nglnUrwinBrain: Setting EndOfDay timer for %d seconds' % timeLeftToday)
            PtAtTimeCallback(self.key, timeLeftToday, 2)
        else:
            print 'nglnUrwinBrain: Timer array was empty!'



    def OnBackdoorMsg(self, target, param):
        global kMaximumTimeBetweenSpawns
        global kMinimumTimeBetweenSpawns
        global kFirstMorningSpawn
        ageSDL = PtGetAgeSDL()
        if (target == 'urwin'):
            if self.sceneobject.isLocallyOwned():
                print 'nglnUrwinBrain.OnBackdoorMsg: Backdoor!'
                if (param == 'walk'):
                    ageSDL['UrwinOnTheProwl'] = (1,)
                    if ageSDL['nglnPodLights'][0]:
                        PtAtTimeCallback(self.key, 1, 1)
                    else:
                        self.StartToWalk()
                elif (param == 'restore'):
                    kMinimumTimeBetweenSpawns = 3600
                    kMaximumTimeBetweenSpawns = 25200
                    kFirstMorningSpawn = 445
                    self.InitNewSDLVars()
                elif (type(param) == type('')):
                    newTimes = param.split(';')
                    kMinimumTimeBetweenSpawns = int(newTimes[0])
                    kMaximumTimeBetweenSpawns = int(newTimes[1])
                    kFirstMorningSpawn = 1
                    self.InitNewSDLVars()


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



