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
respBSDoor = ptAttribResponder(9, 'resp: BS Door', ['0', '1', '2', '3', '4', '5', '6'], netForce=1)
respBSCloth01 = ptAttribResponder(10, 'resp: BS Cloth 01')
respBSCloth02 = ptAttribResponder(11, 'resp: BS Cloth 02')
respBSCloth03 = ptAttribResponder(12, 'resp: BS Cloth 03')
respBSCloth04 = ptAttribResponder(13, 'resp: BS Cloth 04')
respBSCloth05 = ptAttribResponder(14, 'resp: BS Cloth 05')
respBSCloth06 = ptAttribResponder(15, 'resp: BS Cloth 06')
respBSCloth07 = ptAttribResponder(16, 'resp: BS Cloth 07')
respBSClothDoor = ptAttribResponder(17, 'resp: BS Cloth Door', netForce=1)
respBSFastDoor = ptAttribResponder(18, 'resp: BS Fast Door', ['0', '1', '2', '3', '4', '5', '6'])
respBSTicMarks = ptAttribResponder(19, 'resp: BS Tic Marks', ['1', '2', '3', '4', '5', '6', '7'])
respBSDoorOps = ptAttribResponder(20, 'resp: BS Door Ops', ['open', 'close'])
respBSSymbolSpin = ptAttribResponder(21, 'resp: BS Symbol Spin', ['fwdstart', 'fwdstop', 'bkdstart', 'bkdstop'])
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
gPlayCounter = 0
gIsForward = -1
gClkArray = [clkBSCloth01.id, clkBSCloth02.id, clkBSCloth03.id, clkBSCloth04.id, clkBSCloth05.id, clkBSCloth06.id, clkBSCloth07.id]
gRespBSClothArray = [respBSCloth01, respBSCloth02, respBSCloth03, respBSCloth04, respBSCloth05, respBSCloth06, respBSCloth07]
gRespTicClearArray = [respTicClear01, respTicClear02, respTicClear03, respTicClear04, respTicClear05, respTicClear06, respTicClear07]
slowdown = None
clothwait = None
runningvar = 'dlnBlueSpiralRunning'
olutionvar = 'dlnBlueSpiralSolution'
st = None # store the cloth which was clicked so the timer later knows what to do
isPlaying = 0
solutionList = None
keyList = None
consecutive = 0

kTimerShowSolution = 1
kTimerSpiralForward = 3
kTimerSpiralBackward = 4
kTimerCloseDoor = 5
kTimerGameOver = 43
kTimerShowSymbol = 44

class xBlueSpiral(ptResponder,):


    def __init__(self):
        global clothwait,  slowdown, runningvar, solutionvar
        ptResponder.__init__(self)
        self.id = 8812
        self.version = 2
        if xxConfig.isOffline():
            slowdown = 0.25
            clothwait = 15.0
        else:
            slowdown = 1.0
            clothwait = 0.2
        if (PtGetAgeName() == 'EderDelin'):
            runningvar = 'dlnBlueSpiralRunning'
            solutionvar = 'dlnBlueSpiralSolution'
        elif (PtGetAgeName() == 'EderTsogal'):
            runningvar = 'tsoBlueSpiralRunning'
            solutionvar = 'tsoBlueSpiralSolution'
        else:
            raise Exception('Error: Unsupported Age for xBlueSpiral.')
        print ('xBlueSpiral: init  version = %d' % self.version)



    def dustShowSymbols(self):
        global gPlayCounter, consecutive
        print 'dustshowsymbols'
        consecutive = 0
        gPlayCounter = 0
        ageSDL = PtGetAgeSDL()
        ageSDL[SDLBSConsecutive.value] = (consecutive,)
        PtAtTimeCallback(self.key, 0.1, kTimerShowSolution)



    def dustHitCloth(self, clothid):
        global consecutive
        wanted = int(solutionList[consecutive])
        print ((((('dusthitcloth consecutive=' + str(consecutive)) + ' clothid=') + str(clothid)) + ' wanted=') + str(wanted))
        if (wanted == clothid):
            print 'got it!'
            consecutive += 1
            ageSDL = PtGetAgeSDL()
            ageSDL[SDLBSConsecutive.value] = (consecutive,)
            print ('dusthitcloth: Consecutive Hits: %d' % consecutive)
        else:
            print 'wrong one; game over'
            self.dustGameOver()



    def dustNewConsecutive(self):
        global consecutive
        ageSDL = PtGetAgeSDL()
        consecutive = ageSDL[SDLBSConsecutive.value][0]
        print ('dustnewconsecutive=' + str(consecutive))
        if consecutive == 0: return
        respBSTicMarks.run(self.key, state=str(consecutive))
        if (consecutive == 7):
            print 'won!'
            respBSDoorOps.run(self.key, state='open')
            self.dustGameOver()



    def dustNewRunning(self):
        global gPlayCounter, isPlaying, solutionList, consecutive
        ageSDL = PtGetAgeSDL()
        isPlaying = ageSDL[runningvar][0]
        print ('dustnewrunning=' + str(isPlaying))
        PtClearTimerCallbacks(self.key)
        if isPlaying:
            sol = ageSDL[solutionvar][0]
            solutionList = sol.split(' ')
            self.dustShowSymbols()
        else:
            PtAtTimeCallback(self.key, 1, kTimerSpiralBackward)
            gPlayCounter = 0
            isPlaying = 0
            if consecutive:
                for i in range(consecutive):
                    print ('xBlueSpiral.OnGameCliMsg(): Playing Tic Clear state %d' % (i + 1))
                    gRespTicClearArray[i].run(self.key)
            consecutive = 0
            ageSDL = PtGetAgeSDL()
            ageSDL[SDLBSConsecutive.value] = (0,)



    def dustGameOver(self):
        print 'dustgameover'
        ageSDL = PtGetAgeSDL()
        ageSDL[runningvar] = (0,)



    def dustNewGame(self):
        global isPlaying
        print 'dustNewGame: door clicked on'
        if isPlaying:
            print 'already have a game, stop it'
            self.dustGameOver()
            return 
        ageSDL = PtGetAgeSDL()
        sol = ['0', '1', '2', '3', '4', '5', '6']
        random.shuffle(sol)
        sol2 = ''
        for i in sol:
            sol2 += (i + ' ')

        sol2 = sol2.strip(' ')
        ageSDL[solutionvar] = (sol2,)
        print 'solution',sol2,' current runningvar',ageSDL[runningvar][0]
        if ageSDL[runningvar][0]:
            self.dustNewRunning()
        else:
            ageSDL[runningvar] = (1,)
        return 



    def OnServerInitComplete(self):
        global isPlaying, solutionList, consecutive
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(SDLBSKey.value, 1, 1)
        ageSDL.setFlags(SDLBSConsecutive.value, 1, 1)
        ageSDL.setFlags(runningvar, 1, 1)
        ageSDL.setFlags(solutionvar, 1, 1)
        ageSDL.sendToClients(SDLBSKey.value)
        ageSDL.sendToClients(SDLBSConsecutive.value)
        ageSDL.sendToClients(runningvar)
        ageSDL.sendToClients(solutionvar)
        ageSDL.setNotify(self.key, SDLBSKey.value, 0.0)
        ageSDL.setNotify(self.key, SDLBSConsecutive.value, 0.0)
        ageSDL.setNotify(self.key, runningvar, 0.0)
        ageSDL.setNotify(self.key, solutionvar, 0.0)
        self.GetSDLKey()
        respBSDoorOps.run(self.key, state='close', fastforward=1) # always closed for new players
        if len(PtGetPlayerList()): # there is already someone in here
            consecutive = ageSDL[SDLBSConsecutive.value][0]
            newrunning = ageSDL[runningvar][0]
            isPlaying = newrunning
            if isPlaying:
                sol = ageSDL[solutionvar][0]
                solutionList = sol.split(' ')
            print ('xBlueSpiral.OnServerInitComplete(): People in Age - consecutive = %d' % consecutive)
            if consecutive:
                for i in range(consecutive):
                    respBSTicMarks.run(self.key, state=str((i + 1)), fastforward=1)
        else:
            print 'No one online, reset everything'
            consecutive = 0
            ageSDL[SDLBSConsecutive.value] = (consecutive,)
            isPlaying = False
            ageSDL[runningvar] = (isPlaying,)
            animBlueSpiral.animation.stop()
            animBlueSpiral.animation.skipToBegin()
            print ('xBlueSpiral.OnServerInitComplete(): Empty Age - consecutive = %d' % consecutive)
        print str(runningvar)



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        print 'dustin onsdlnotify'
        ageSDL = PtGetAgeSDL()
        print ('xBlueSpiral.OnSDLNotify(): VARname:%s, SDLname:%s, tag:%s, value:%s, playerID:%d' % (VARname, SDLname, tag, ageSDL[VARname][0], playerID))
        if (VARname == SDLBSConsecutive.value):
            self.dustNewConsecutive()
        elif (VARname == runningvar):
            self.dustNewRunning()



    def GetSDLKey(self):
        global keyList
        try:
            ageSDL = PtGetAgeSDL()
            key = ageSDL[SDLBSKey.value][0]
            if (key == 'empty'):
                raise ValueError, 'xBlueSpiral.OnServerInitComplete(): First time here, generating new key'
            if ((key == '') or ((key == ' ') or (key == None))):
                raise error, 'xBlueSpiral.OnServerInitComplete(): Empty key'
            keyList = key.split(' ')
            print ('xBlueSpiral.OnServerInitComplete(): ageSDL[xBlueSpiralKey] = %s' % key)
        except ValueError:
            key = ''
            keyList = ['0', '1', '2', '3', '4', '5', '6']
            random.shuffle(keyList)
            for i in keyList:
                key += (i + ' ')
            key = key.strip(' ')
            ageSDL[SDLBSKey.value] = (key,)
            keyList = key.split(' ')
            print ('xBlueSpiral.OnServerInitComplete(): First time here, new key = %s.' % key)
        except:
            raise Exception('ERROR: Something wrong, can not grab SDL key')
        return 1



    def OnNotify(self, state, id, events):
        global gIsForward
        global st, isPlaying
        print ('xBlueSpiral.OnNotify: state=%s id=%d events=' % (state, id)),
        print events
        ageSDL = PtGetAgeSDL()
        isFromUs = PtWasLocallyNotified(self.key)
        if ((id == evntBSBeginning.id) and (gIsForward == 0)): # backwards rotation finished
            print 'xBlueSpiral.OnNotify: Spiral hit beginning'
            respBSSymbolSpin.run(self.key, state='bkdstop')
            gIsForward = -1
            return 
        elif ((id in gClkArray) and state):
            range0 = gClkArray.index(id)
            gRespBSClothArray[range0].run(self.key, avatar=PtFindAvatar(events))
            if isFromUs:
                if isPlaying:
                    print ('xBlueSpiral.OnNotify: Cloth0%d clicked during game with a value of %d' % (range0+1,
                     int(keyList[range0])))
                    self.dustHitCloth(int(keyList[range0]))
                else:
                    print ('xBlueSpiral.OnNotify: Cloth0%d clicked, playing glow for Door part %s' % (range0+1,
                     keyList[range0]))
                    st = keyList[range0]
                    PtAtTimeCallback(self.key, clothwait, kTimerShowSymbol)
            else:
                print ('xBlueSpiral.OnNotify: Someone else clicked Cloth0%d with a value of %d' % (range0+1,
                 int(keyList[range0])))
        elif (id == clkBSDoor.id) and (not state) and isFromUs:
            print 'xBlueSpiral.OnNotify: Door clicked on'
            respBSClothDoor.run(self.key, avatar=PtFindAvatar(events))
        elif (id == respBSDoorOps.id):
            print 'xBlueSpiral.OnNotify: Door is fully open'
            PtAtTimeCallback(self.key, 10, kTimerCloseDoor)
        elif ((id == respBSClothDoor.id) and isFromUs):
            print 'xBlueSpiral.OnNotify: Door actually touched'
            self.dustNewGame()



    def OnTimer(self, id):
        global gPlayCounter
        global gIsForward, isPlaying, solutionList
        print 'ontimer'
        if (id == kTimerShowSolution):
            print ('draw symbol ' + str(gPlayCounter))
            ageSDL = PtGetAgeSDL()
            if isPlaying:
                respBSFastDoor.run(self.key, state=str(solutionList[gPlayCounter]), netPropagate=0)
                if (gPlayCounter >= 0):
                    gPlayCounter += 1
                if (gPlayCounter >= 7):
                    gPlayCounter = 0
                    PtAtTimeCallback(self.key, 3, kTimerShowSolution) # wait a bit longer before showing the solution again
                    if gIsForward != 1:
                        print 'start rotating'
                        PtAtTimeCallback(self.key, 0.1, kTimerSpiralForward)
                        totaltime = (60 / slowdown)
                        PtAtTimeCallback(self.key, totaltime, kTimerGameOver)
                    return 
                PtAtTimeCallback(self.key, 2, kTimerShowSolution)
        elif (id == kTimerSpiralForward):
            print ('xBlueSpiral.OnTimer: id = %d - Playing Spiral Forward' % id)
            print 'fwdstart'
            respBSSymbolSpin.run(self.key, state='fwdstart')
            animBlueSpiral.animation.backwards(0)
            print ('speed=' + str(slowdown))
            animBlueSpiral.animation.speed((1 * slowdown))
            animBlueSpiral.animation.play()
            gIsForward = 1
        elif ((id == kTimerSpiralBackward)):
            print ('xBlueSpiral.OnTimer: id = %d - Playing Spiral backwards' % id)
            print 'bkdstart'
            respBSSymbolSpin.run(self.key, state='bkdstart')
            animBlueSpiral.animation.backwards(1)
            animBlueSpiral.animation.speed(10.0)
            animBlueSpiral.animation.resume()
            gIsForward = 0
        elif (id == kTimerCloseDoor):
            print ('xBlueSpiral.OnTimer: id = %d - Closing door' % id)
            respBSDoorOps.run(self.key, state='close')
        elif (id == kTimerGameOver):
            print 'time up'
            self.dustGameOver()
        elif (id == kTimerShowSymbol):
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



