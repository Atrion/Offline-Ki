# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import whrandom
UrwinFlipSide_A = ptAttribAnimation(1, 'Urwin Flip Anim A', netForce=1)
UrwinFlipSide_B = ptAttribAnimation(2, 'Urwin Flip Anim B', netForce=1)
UrwinMasterAnim = ptAttribAnimation(3, 'Urwin Master Anim', netForce=1)
respUrwin_Eat_ToIdle = ptAttribResponder(4, 'resp: Eat To Idle')
respUrwin_Eat_ToWalkSniff = ptAttribResponder(5, 'resp: Eat To WalkSniff')
respUrwin_Eat_Scoop = ptAttribResponder(6, 'resp: Eat Scoop')
respUrwin_Eat_Shake = ptAttribResponder(7, 'resp: Eat Shake')
respUrwin_Eat_Swallow = ptAttribResponder(8, 'resp: Eat Swallow')
respUrwin_Idle_01 = ptAttribResponder(9, 'resp: Idle01')
respUrwin_Idle_02 = ptAttribResponder(10, 'resp: Idle02')
respUrwin_Idle_ToEat = ptAttribResponder(11, 'resp: Idle To Eat')
respUrwin_Idle_ToWalk = ptAttribResponder(12, 'resp: Idle To Walk')
respUrwin_Idle_Vocalize = ptAttribResponder(13, 'resp: Idle Vocalize')
respUrwin_Walk_ToIdle = ptAttribResponder(14, 'resp: Walk To Idle')
respUrwin_Walk_ToWalkSniff = ptAttribResponder(15, 'resp: Walk To WalkSniff')
respUrwin_Walk_Loop01 = ptAttribResponder(16, 'resp: Walk01')
respUrwin_Walk_Loop02 = ptAttribResponder(17, 'resp: Walk02')
respUrwin_WalkSniff_ToEat = ptAttribResponder(18, 'resp: WalkSniff To Eat')
respUrwin_WalkSniff_ToWalk = ptAttribResponder(19, 'resp: WalkSniff To Walk')
respUrwin_WalkSniff = ptAttribResponder(20, 'resp: WalkSniff')
respUrwinSfx = ptAttribResponder(21, 'resp: Urwin SFX', ['Eat2Idle',
 'Eat2Sniff',
 'Scoop',
 'Shake',
 'Swallow',
 'Idle01',
 'Idle02',
 'Idle2Eat',
 'Idle2Walk',
 'Vocalize',
 'Walk2Idle',
 'Walk2Sniff',
 'Walk01',
 'Walk02',
 'Sniff2Eat',
 'Sniff2Walk',
 'Sniff',
 'appear',
 'disappear'], netForce=1)
actUrwinPathEnd = ptAttribActivator(22, 'act: Urwin Path End')
kDayLengthInSeconds = 56585
kMinimumTimeBetweenSpawns = 3600
kMaximumTimeBetweenSpawns = 25200
kFirstMorningSpawn = 445
minsteps = 3
maxsteps = 10
StepsToTake = 0
stackList = []
class payiUrwinBrain(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5253
        version = 1
        self.version = version
        print '__init__payiUrwinBrain v.',
        print version,
        print '.0'



    def OnFirstUpdate(self):
        whrandom.seed()



    def OnServerInitComplete(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            print 'payiUrwinBrain:\tERROR---Cannot find the Payiferen Age SDL'
            self.InitNewSDLVars()
        ageSDL.sendToClients('UrwinLastUpdated')
        ageSDL.sendToClients('UrwinSpawnTimes')
        ageSDL.sendToClients('UrwinOnTheProwl')
        ageSDL.setFlags('UrwinLastUpdated', 1, 1)
        ageSDL.setFlags('UrwinSpawnTimes', 1, 1)
        ageSDL.setFlags('UrwinOnTheProwl', 1, 1)
        ageSDL.setFlags('payiPodLights', 1, 1)
        ageSDL.setNotify(self.key, 'UrwinLastUpdated', 0.0)
        ageSDL.setNotify(self.key, 'UrwinSpawnTimes', 0.0)
        ageSDL.setNotify(self.key, 'UrwinOnTheProwl', 0.0)
        ageSDL.setNotify(self.key, 'payiPodLights', 0.0)
        thisDay = int((PtGetDniTime() / kDayLengthInSeconds))
        lastDay = int((ageSDL['UrwinLastUpdated'][0] / kDayLengthInSeconds))
        if ((thisDay - lastDay) > 0):
            print "payiUrwinBrain: It's been at least a day since the last update, running new numbers now."
            self.InitNewSDLVars()
        else:
            print "payiUrwinBrain: It's been less than a day since the last update, doing nothing"
            self.SetUrwinTimers()
        if (not len(PtGetPlayerList())):
            UrwinMasterAnim.animation.skipToBegin()



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname == 'UrwinSpawnTimes'):
            self.SetUrwinTimers()
        elif (VARname == 'payiPodLights'):
            ageSDL = PtGetAgeSDL()
            if ((not ageSDL[VARname][0]) and ageSDL['UrwinOnTheProwl'][0]):
                respUrwinSfx.run(self.key, state='Idle01')



    def OnNotify(self, state, id, events):
        global StepsToTake
        ageSDL = PtGetAgeSDL()
        print ('payiUrwinBrain.OnNotify:  state=%f id=%d owned=%s prowl=%s events=' % (state,
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
                boolBatteryChargedAndOn = ageSDL['payiPodLights'][0]
                if ((id == respUrwin_Walk_Loop01.id) or ((id == respUrwin_Walk_Loop02.id) or ((id == respUrwin_WalkSniff_ToWalk.id) or (id == respUrwin_Idle_ToWalk.id)))):
                    UrwinMasterAnim.animation.resume()
                    if (StepsToTake == 0):
                        StepsToTake = whrandom.randint(minsteps, maxsteps)
                        print ('We should have steps, so Urwin has decided to take %d steps.' % StepsToTake)
                    StepsToTake = (StepsToTake - 1)
                    if StepsToTake:
                        if whrandom.randint(0, 9):
                            print ('Urwin will take %d more steps...' % StepsToTake)
                            if whrandom.randint(0, 2):
                                print 'Urwin walks one way.'
                                self.SendNote('respUrwin_Walk_Loop01.run(self.key)')
                                if boolBatteryChargedAndOn:
                                    respUrwinSfx.run(self.key, state='Walk01')
                            else:
                                print 'Urwin walks the other way.'
                                self.SendNote('respUrwin_Walk_Loop02.run(self.key)')
                                if boolBatteryChargedAndOn:
                                    respUrwinSfx.run(self.key, state='Walk02')
                        else:
                            print 'Urwin smells something...'
                            self.SendNote('respUrwin_Walk_ToWalkSniff.run(self.key)')
                            if boolBatteryChargedAndOn:
                                respUrwinSfx.run(self.key, state='Walk2Sniff')
                    else:
                        print 'Urwin is tired and stops walking'
                        self.SendNote('respUrwin_Walk_ToIdle.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Walk2Idle')
                elif ((id == respUrwin_Walk_ToWalkSniff.id) or ((id == respUrwin_WalkSniff.id) or (id == respUrwin_Eat_ToWalkSniff.id))):
                    UrwinMasterAnim.animation.resume()
                    pct = whrandom.randint(0, 2)
                    if (pct == 2):
                        print 'Urwin smells something good!'
                        self.SendNote('respUrwin_WalkSniff.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Sniff')
                    elif (pct == 1):
                        print 'Urwin found food!'
                        self.SendNote('respUrwin_WalkSniff_ToEat.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Sniff2Eat')
                    else:
                        print 'Urwin says nevermind, back to walking.'
                        self.SendNote('respUrwin_WalkSniff_ToWalk.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Sniff2Walk')
                elif ((id == respUrwin_WalkSniff_ToEat.id) or (id == respUrwin_Idle_ToEat.id)):
                    UrwinMasterAnim.animation.stop()
                    pct = whrandom.randint(0, 2)
                    if (pct == 2):
                        print 'Urwin lost interest in the food.'
                        self.SendNote('respUrwin_Eat_ToIdle.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Eat2Idle')
                    elif (pct == 1):
                        print 'Urwin is still searching for the food.'
                        self.SendNote('respUrwin_Eat_ToWalkSniff.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Eat2Sniff')
                    else:
                        print 'Urwin scoops up the food!'
                        self.SendNote('respUrwin_Eat_Scoop.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Scoop')
                elif ((id == respUrwin_Eat_Scoop.id) or ((id == respUrwin_Eat_Shake.id) or (id == respUrwin_Eat_Swallow.id))):
                    pct = whrandom.randint(0, 4)
                    if (pct == 4):
                        print 'Urwin scoops up the food!'
                        self.SendNote('respUrwin_Eat_Scoop.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Scoop')
                    elif (pct == 3):
                        print 'Urwin shakes the food!'
                        self.SendNote('respUrwin_Eat_Shake.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Shake')
                    elif (pct == 2):
                        print 'Urwin swallows the food!'
                        self.SendNote('respUrwin_Eat_Swallow.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Swallow')
                    elif (pct == 1):
                        print 'Urwin lost interest in the food.'
                        self.SendNote('respUrwin_Eat_ToIdle.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Eat2Idle')
                    else:
                        print 'Urwin is still searching for the food.'
                        self.SendNote('respUrwin_Eat_ToWalkSniff.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Eat2Sniff')
                elif ((id == respUrwin_Idle_01.id) or ((id == respUrwin_Idle_02.id) or ((id == respUrwin_Eat_ToIdle.id) or ((id == respUrwin_Walk_ToIdle.id) or (id == respUrwin_Idle_Vocalize.id))))):
                    UrwinMasterAnim.animation.stop()
                    pct = whrandom.randint(0, 4)
                    if (pct == 4):
                        print 'Urwin idles one way.'
                        self.SendNote('respUrwin_Idle_01.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Idle01')
                    elif (pct == 3):
                        print 'Urwin idles the other way.'
                        self.SendNote('respUrwin_Idle_02.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Idle02')
                    elif (pct == 2):
                        print 'Urwin calls home!'
                        self.SendNote('respUrwin_Idle_Vocalize.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Vocalize')
                    elif (pct == 1):
                        print 'Urwin gets hungry.'
                        self.SendNote('respUrwin_Idle_ToEat.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Idle2Eat')
                    else:
                        print 'Urwin is done resting, back to walking.'
                        self.SendNote('respUrwin_Idle_ToWalk.run(self.key)')
                        if boolBatteryChargedAndOn:
                            respUrwinSfx.run(self.key, state='Idle2Walk')
                elif (id == actUrwinPathEnd.id):
                    print 'End of the line, Urwin!'
                    UrwinMasterAnim.animation.stop()
                    UrwinMasterAnim.animation.skipToTime(0)
                    ageSDL['UrwinOnTheProwl'] = (0,)
                    if boolBatteryChargedAndOn:
                        respUrwinSfx.run(self.key, state='disappear')
        elif ((id in range(3, 20)) and (not self.sceneobject.isLocallyOwned())):
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



    def StartToWalk(self):
        global StepsToTake
        ageSDL = PtGetAgeSDL()
        boolBatteryChargedAndOn = ageSDL['payiPodLights'][0]
        StepsToTake = whrandom.randint(minsteps, maxsteps)
        print ('Urwin has decided to take %d steps.' % StepsToTake)
        if whrandom.randint(0, 1):
            self.SendNote('respUrwin_Walk_Loop01.run(self.key)')
            if boolBatteryChargedAndOn:
                respUrwinSfx.run(self.key, state='Walk01')
        else:
            self.SendNote('respUrwin_Walk_Loop02.run(self.key)')
            if boolBatteryChargedAndOn:
                respUrwinSfx.run(self.key, state='Walk02')
        UrwinMasterAnim.animation.resume()



    def OnTimer(self, TimerID):
        ageSDL = PtGetAgeSDL()
        boolBatteryChargedAndOn = ageSDL['payiPodLights'][0]
        if self.sceneobject.isLocallyOwned():
            if (TimerID == 1):
                print 'UrwinBrain.OnTimer: Time for the Urwin to return.'
                ageSDL['UrwinOnTheProwl'] = (1,)
                if whrandom.randint(0, 1):
                    UrwinFlipSide_A.animation.play()
                else:
                    UrwinFlipSide_B.animation.play()
                if ageSDL['payiPodLights'][0]:
                    respUrwinSfx.run(self.key, state='appear')
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
        print ('payiUrwinBrain: Generated a valid spawn time: %d' % firstTime)
        spawnTimes = [firstTime]
        while (type(spawnTimes[-1]) == type(long(1))):
            randnum = whrandom.randint(kMinimumTimeBetweenSpawns, kMaximumTimeBetweenSpawns)
            newTime = (spawnTimes[-1] + randnum)
            if (newTime < endOfToday):
                print ('payiUrwinBrain: Generated a valid spawn time: %d' % newTime)
                spawnTimes.append(newTime)
            else:
                print ('payiUrwinBrain: Generated a spawn time after dusk, exiting loop: %d' % newTime)
                break
        else:
            print "payiUrwinBrain:ERROR---Tried to add a spawn time that's not a number: ",
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
                        print ('payiUrwinBrain: Setting timer for %d seconds' % timeTillSpawn)
                        PtAtTimeCallback(self.key, timeTillSpawn, 1)

            timeLeftToday = (kDayLengthInSeconds - int((PtGetAgeTimeOfDayPercent() * kDayLengthInSeconds)))
            timeLeftToday += 1
            print ('payiUrwinBrain: Setting EndOfDay timer for %d seconds' % timeLeftToday)
            PtAtTimeCallback(self.key, timeLeftToday, 2)
        else:
            print 'payiUrwinBrain: Timer array was empty!'



    def OnBackdoorMsg(self, target, param):
        global kMaximumTimeBetweenSpawns
        global kMinimumTimeBetweenSpawns
        global kFirstMorningSpawn
        ageSDL = PtGetAgeSDL()
        if (target == 'urwin'):
            if self.sceneobject.isLocallyOwned():
                print 'payiUrwinBrain.OnBackdoorMsg: Backdoor!'
                if (param == 'walk'):
                    ageSDL['UrwinOnTheProwl'] = (1,)
                    if ageSDL['payiPodLights'][0]:
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



