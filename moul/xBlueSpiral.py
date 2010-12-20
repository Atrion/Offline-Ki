# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import random
import xxConfig
clkBSDoor = ptAttribActivator(1, 'clk: BS Door')
clkBSCloth01 = ptAttribActivator(2, 'clk: BS Cloth 01')
clkBSCloth02 = ptAttribActivator(3, 'clk: BS Cloth 02')
clkBSCloth03 = ptAttribActivator(4, 'clk: BS Cloth 03')
clkBSCloth04 = ptAttribActivator(5, 'clk: BS Cloth 04')
clkBSCloth05 = ptAttribActivator(6, 'clk: BS Cloth 05')
clkBSCloth06 = ptAttribActivator(7, 'clk: BS Cloth 06')
clkBSCloth07 = ptAttribActivator(8, 'clk: BS Cloth 07')
respBSDoor = ptAttribResponder(9, 'resp: BS Door', ['0',
 '1',
 '2',
 '3',
 '4',
 '5',
 '6'], netForce=1)
respBSCloth01 = ptAttribResponder(10, 'resp: BS Cloth 01')
respBSCloth02 = ptAttribResponder(11, 'resp: BS Cloth 02')
respBSCloth03 = ptAttribResponder(12, 'resp: BS Cloth 03')
respBSCloth04 = ptAttribResponder(13, 'resp: BS Cloth 04')
respBSCloth05 = ptAttribResponder(14, 'resp: BS Cloth 05')
respBSCloth06 = ptAttribResponder(15, 'resp: BS Cloth 06')
respBSCloth07 = ptAttribResponder(16, 'resp: BS Cloth 07')
respBSClothDoor = ptAttribResponder(17, 'resp: BS Cloth Door', netForce=1)
respBSFastDoor = ptAttribResponder(18, 'resp: BS Fast Door', ['0',
 '1',
 '2',
 '3',
 '4',
 '5',
 '6'])
respBSTicMarks = ptAttribResponder(19, 'resp: BS Tic Marks', ['1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7'])
respBSDoorOps = ptAttribResponder(20, 'resp: BS Door Ops', ['open',
 'close'])
respBSSymbolSpin = ptAttribResponder(21, 'resp: BS Symbol Spin', ['fwdstart',
 'fwdstop',
 'bkdstart',
 'bkdstop'])
animBlueSpiral = ptAttribAnimation(22, 'anim: Blue Spiral', netForce=1)
evntBSBeginning = ptAttribActivator(23, 'evnt: Blue Spiral Beginning')
SDLBSKey = ptAttribString(24, 'SDL: BS Key')
SDLBSConsecutive = ptAttribString(27, 'SDL: BS Consecutive')
respTicClear01 = ptAttribResponder(28, 'resp: Tic Clear 01')
respTicClear02 = ptAttribResponder(29, 'resp: Tic Clear 02')
respTicClear03 = ptAttribResponder(30, 'resp: Tic Clear 03')
respTicClear04 = ptAttribResponder(31, 'resp: Tic Clear 04')
respTicClear05 = ptAttribResponder(32, 'resp: Tic Clear 05')
respTicClear06 = ptAttribResponder(33, 'resp: Tic Clear 06')
respTicClear07 = ptAttribResponder(34, 'resp: Tic Clear 07')
gAgeStartedIn = None
gPlayCounter = 0
gIsForward = -1
gDoorIsOpen = 0
gClkArray = [clkBSCloth01.id,
 clkBSCloth02.id,
 clkBSCloth03.id,
 clkBSCloth04.id,
 clkBSCloth05.id,
 clkBSCloth06.id,
 clkBSCloth07.id]
slowdown = None
clothwait = None
st = None
long = False
class xBlueSpiral(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 8812
        self.version = 2
        self.isPlaying = 0
        self.clientId = 0
        self.joinedToGame = 0
        self.solutionList = None
        self.keyList = None
        self.consecutive = 0
        self.isOwner = 0
        self.tableId = 0
        self.gameId = 0
        self.runningvar = None
        self.solutionvar = None
        self.rotating = False
        print ('xBlueSpiral: init  version = %d' % self.version)



    def dustShowSymbols(self):
        global gPlayCounter
        print 'dustshowsymbols'
        self.consecutive = 0
        gPlayCounter = 0
        ageSDL = PtGetAgeSDL()
        ageSDL[SDLBSConsecutive.value] = (self.consecutive,)
        self.rotating = False
        PtAtTimeCallback(self.key, 0.10000000000000001, 1)



    def dustHitCloth(self, clothid):
        wanted = int(self.solutionList[self.consecutive])
        print ((((('dusthitcloth consecutive=' + str(self.consecutive)) + ' clothid=') + str(clothid)) + ' wanted=') + str(wanted))
        if (wanted == clothid):
            print 'got it!'
            self.consecutive += 1
            ageSDL = PtGetAgeSDL()
            ageSDL[SDLBSConsecutive.value] = (self.consecutive,)
            print ('dusthitcloth: Consecutive Hits: %d' % self.consecutive)
        else:
            print 'wrong one; game over'
            self.dustGameOver()



    def dustNewConsecutive(self):
        ageSDL = PtGetAgeSDL()
        newconsecutive = ageSDL[SDLBSConsecutive.value][0]
        self.consecutive = newconsecutive
        print ('dustnewconsecutive=' + str(self.consecutive))
        respBSTicMarks.run(self.key, state=str(self.consecutive))
        if (self.consecutive == 7):
            print 'won!'
            respBSDoorOps.run(self.key, state='open')
            self.dustGameOver()



    def dustNewRunning(self):
        global gPlayCounter
        ageSDL = PtGetAgeSDL()
        newrunning = ageSDL[self.runningvar][0]
        self.isPlaying = newrunning
        print ('dustnewrunning=' + str(newrunning))
        PtClearTimerCallbacks(self.key)
        if self.isPlaying:
            sol = ageSDL[self.solutionvar][0]
            self.solutionList = sol.split(' ')
            self.dustShowSymbols()
        else:
            self.rotating = False
            PtAtTimeCallback(self.key, 1, 4)
            gPlayCounter = 0
            self.isPlaying = 0
            gIsForward = -1
            if self.consecutive:
                for i in range(self.consecutive):
                    print ('xBlueSpiral.OnGameCliMsg(): Playing Tic Clear state %d' % (i + 1))
                    code = (('respTicClear0' + str((i + 1))) + '.run(self.key)')
                    exec code

            if (self.consecutive == 7):
                print 'disabled door raise/lower call'
            else:
                print 'bkdstop'
                respBSSymbolSpin.run(self.key, state='fwdstop', fastforward=1)
            self.consecutive = 0
            ageSDL = PtGetAgeSDL()
            ageSDL[SDLBSConsecutive.value] = (self.consecutive,)



    def dustGameOver(self):
        print 'dustgameover'
        ageSDL = PtGetAgeSDL()
        ageSDL[self.runningvar] = (0,)



    def dustNewGame(self):
        print 'dustNewGame: door clicked on'
        if self.isPlaying:
            print 'already have a game, stop it'
            self.dustGameOver()
            return 
        ageSDL = PtGetAgeSDL()
        sol = ['0',
         '1',
         '2',
         '3',
         '4',
         '5',
         '6']
        random.shuffle(sol)
        sol2 = ''
        for i in sol:
            sol2 += (i + ' ')

        sol2 = sol2.strip(' ')
        ageSDL[self.solutionvar] = (sol2,)
        if ageSDL[self.runningvar][0]:
            self.dustNewRunning()
        else:
            ageSDL[self.runningvar] = (1,)
        return 



    def OnFirstUpdate(self):
        global gAgeStartedIn
        global clothwait
        global slowdown
        gAgeStartedIn = PtGetAgeName()
        self.clientId = PtGetLocalClientID()
        if xxConfig.isOffline():
            slowdown = 0.25
            clothwait = 15.0
        else:
            slowdown = 1.0
            clothwait = 0.0
        if (gAgeStartedIn == 'EderDelin'):
            self.runningvar = 'dlnBlueSpiralRunning'
            self.solutionvar = 'dlnBlueSpiralSolution'
        elif (gAgeStartedIn == 'EderTsogal'):
            self.runningvar = 'tsoBlueSpiralRunning'
            self.solutionvar = 'tsoBlueSpiralSolution'
        else:
            print 'Error: Unsupported Age for xBlueSpiral.'



    def OnServerInitComplete(self):
        if (gAgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            self.GetSDLKey()
            if len(PtGetPlayerList()):
                self.consecutive = ageSDL[SDLBSConsecutive.value][0]
                newrunning = ageSDL[self.runningvar][0]
                self.isPlaying = newrunning
                if self.isPlaying:
                    sol = ageSDL[self.solutionvar][0]
                    self.solutionList = sol.split(' ')
                print ('xBlueSpiral.OnServerInitComplete(): People in Age - self.consecutive = %d' % self.consecutive)
                if self.consecutive:
                    for i in range(self.consecutive):
                        respBSTicMarks.run(self.key, state=str((i + 1)), fastforward=1)

            else:
                print 'No one online, reset everything'
                self.consecutive = 0
                ageSDL[SDLBSConsecutive.value] = (self.consecutive,)
                self.isPlaying = False
                ageSDL[self.runningvar] = (self.isPlaying,)
                animBlueSpiral.animation.stop()
                animBlueSpiral.animation.skipToBegin()
                respBSDoorOps.run(self.key, state='close', fastforward=1)
                print ('xBlueSpiral.OnServerInitComplete(): Empty Age - self.consecutive = %d' % self.consecutive)
            ageSDL.setFlags(SDLBSKey.value, 1, 1)
            ageSDL.setFlags(SDLBSConsecutive.value, 1, 1)
            ageSDL.setFlags(self.runningvar, 1, 1)
            ageSDL.sendToClients(SDLBSKey.value)
            ageSDL.sendToClients(SDLBSConsecutive.value)
            ageSDL.sendToClients(self.runningvar)
            ageSDL.setNotify(self.key, SDLBSKey.value, 0.0)
            ageSDL.setNotify(self.key, SDLBSConsecutive.value, 0.0)
            ageSDL.setNotify(self.key, self.runningvar, 0.0)
            print str(self.runningvar)



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        print 'dustin onsdlnotify'
        if (gAgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            print ('xBlueSpiral.OnSDLNotify(): VARname:%s, SDLname:%s, tag:%s, value:%s, playerID:%d' % (VARname,
             SDLname,
             tag,
             ageSDL[VARname][0],
             playerID))
            if (VARname == SDLBSConsecutive.value):
                self.dustNewConsecutive()
            if (VARname == self.runningvar):
                self.dustNewRunning()



    def GetSDLKey(self):
        try:
            ageSDL = PtGetAgeSDL()
            key = ageSDL[SDLBSKey.value][0]
            if (key == 'empty'):
                raise ValueError, 'xBlueSpiral.OnServerInitComplete(): First time here, generating new key'
            if ((key == '') or ((key == ' ') or (key == None))):
                raise error, 'xBlueSpiral.OnServerInitComplete(): Empty key'
            self.keyList = key.split(' ')
            print ('xBlueSpiral.OnServerInitComplete(): ageSDL[xBlueSpiralKey] = %s' % key)
        except ValueError:
            key = ''
            self.keyList = ['0',
             '1',
             '2',
             '3',
             '4',
             '5',
             '6']
            random.shuffle(self.keyList)
            for i in self.keyList:
                key += (i + ' ')

            key = key.strip(' ')
            ageSDL[SDLBSKey.value] = (key,)
            self.keyList = key.split(' ')
            print ('xBlueSpiral.OnServerInitComplete(): First time here, new key = %s.' % key)
        except:
            print 'Something wrong, try grabbing SDL later'
            self.keyList = None
            return 0
        return 1



    def OnNotify(self, state, id, events):
        global gDoorIsOpen
        global gIsForward
        global st
        if (self.keyList == None):
            print 'xBlueSpiral.OnNotify: I had SDL issues earlier'
            if (not self.GetSDLKey()):
                print 'xBlueSpiral.OnNotify: And I still do'
                return 
            print 'xBlueSpiral.OnNotify: But I got them worked out'
        print ('xBlueSpiral.OnNotify: state=%s id=%d events=' % (state,
         id)),
        print events
        ageSDL = PtGetAgeSDL()
        if ((id == evntBSBeginning.id) and (gIsForward == 0)):
            print 'xBlueSpiral.OnNotify: Spiral hit beginning'
            print "bkdstop doesn't occur"
            respBSSymbolSpin.run(self.key, state='bkdstop')
            gIsForward = -1
            return 
        elif ((id in gClkArray) and state):
            range0 = gClkArray.index(id)
            range1 = (gClkArray.index(id) + 1)
            code = (('respBSCloth0' + str(range1)) + '.run(self.key, avatar=PtFindAvatar(events))')
            exec code
            if ((PtFindAvatar(events) == PtGetLocalAvatar()) and PtWasLocallyNotified(self.key)):
                if self.isPlaying:
                    print ('xBlueSpiral.OnNotify: Cloth0%d clicked during game with a value of %d' % (range1,
                     int(self.keyList[range0])))
                    self.dustHitCloth(int(self.keyList[range0]))
                else:
                    print ('xBlueSpiral.OnNotify: Cloth0%d clicked, playing glow for Door part %s' % (range1,
                     self.keyList[range0]))
                    st = self.keyList[range0]
                    PtAtTimeCallback(self.key, clothwait, 44)
            else:
                print ('xBlueSpiral.OnNotify: Someone else clicked Cloth0%d with a value of %d' % (range1,
                 int(self.keyList[range0])))
        elif ((id == clkBSDoor.id) and ((not state) and ((PtFindAvatar(events) == PtGetLocalAvatar()) and PtWasLocallyNotified(self.key)))):
            print 'xBlueSpiral.OnNotify: Door clicked on'
            respBSClothDoor.run(self.key, avatar=PtFindAvatar(events))
        elif (id == respBSDoorOps.id):
            print 'xBlueSpiral.OnNotify: Door is fully open'
            gDoorIsOpen = 1
        elif ((id == respBSClothDoor.id) and self.sceneobject.isLocallyOwned()):
            print 'xBlueSpiral.OnNotify: Door actually touched'
            self.dustNewGame()



    def OnTimer(self, id):
        global gDoorIsOpen
        global gPlayCounter
        global gIsForward
        print 'ontimer'
        if (id == 1):
            print ('draw symbol ' + str(gPlayCounter))
            ageSDL = PtGetAgeSDL()
            if self.isPlaying:
                respBSFastDoor.run(self.key, state=str(self.solutionList[gPlayCounter]), netPropagate=0)
                if (gPlayCounter >= 0):
                    gPlayCounter += 1
                if (gPlayCounter >= 7):
                    gPlayCounter = 0
                    PtAtTimeCallback(self.key, 3, 1)
                    if (not self.rotating):
                        print 'start rotating'
                        self.rotating = True
                        PtAtTimeCallback(self.key, 1, 3)
                        totaltime = (60 / slowdown)
                        PtAtTimeCallback(self.key, totaltime, 43)
                    return 
                PtAtTimeCallback(self.key, 2, 1)
        elif (id == 3):
            print ('xBlueSpiral.OnTimer: id = %d - Playing Spiral Forward' % id)
            print 'fwdstart'
            respBSSymbolSpin.run(self.key, state='fwdstart')
            animBlueSpiral.animation.backwards(0)
            print ('speed=' + str(slowdown))
            animBlueSpiral.animation.speed((1 * slowdown))
            animBlueSpiral.animation.play()
            gIsForward = 1
        elif ((id == 4) and (gIsForward == 1)):
            print ('xBlueSpiral.OnTimer: id = %d - Playing Spiral backwards' % id)
            print 'bkdstart'
            respBSSymbolSpin.run(self.key, state='bkdstart')
            animBlueSpiral.animation.backwards(1)
            animBlueSpiral.animation.speed(10.0)
            animBlueSpiral.animation.resume()
            gIsForward = 0
        elif (id == 5):
            if gDoorIsOpen:
                print ('xBlueSpiral.OnTimer: id = %d - Closing door' % id)
                gDoorIsOpen = 0
                respBSDoorOps.run(self.key, state='close')
            else:
                print ('xBlueSpiral.OnTimer: id = %d - Waiting for door to open before closing' % id)
                PtAtTimeCallback(self.key, 1, 5)
        elif (id == 43):
            print 'time up'
            self.dustGameOver()
        elif (id == 44):
            respBSDoor.run(self.key, state=st)


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



