from Plasma import *
from PlasmaTypes import *
import string
actLever01 = ptAttribActivator(1, 'Actvr: Lever 01')
actLever02 = ptAttribActivator(2, 'Actvr: Lever 02')
actLever03 = ptAttribActivator(3, 'Actvr: Lever 03')
actLever04 = ptAttribActivator(4, 'Actvr: Lever 04')
actLever05 = ptAttribActivator(5, 'Actvr: Reset Ring')
respLever01 = ptAttribResponder(6, 'Rspndr: Lever 01')
respLever02 = ptAttribResponder(7, 'Rspndr: Lever 02')
respLever03 = ptAttribResponder(8, 'Rspndr: Lever 03')
respLever04 = ptAttribResponder(9, 'Rspndr: Lever 04')
respLever05 = ptAttribResponder(10, 'Rspndr: Reset Ring')
PillarAnim = ptAttribAnimation(15, 'Pillar Animation', byObject=1)
CounterAnim = ptAttribAnimation(16, 'Counterweight Animation')
SolutionResp = ptAttribResponder(17, 'resp: Lower Solution Ladder')
Ladderbox1 = ptAttribActivator(18, 'Act: Ladderbox1')
Ladderbox2 = ptAttribActivator(19, 'Act: Ladderbox2')
Ladderbox3 = ptAttribActivator(20, 'Act: Ladderbox3')
Ladderbox4 = ptAttribActivator(21, 'Act: Ladderbox4')
Ladderbox5 = ptAttribActivator(22, 'Act: Ladderbox5')
Ladderbox6 = ptAttribActivator(23, 'Act: Ladderbox6')
Ladderbox7 = ptAttribActivator(24, 'Act: Ladderbox7')
Ladderbox8 = ptAttribActivator(25, 'Act: Ladderbox8')
Ladderbox9 = ptAttribActivator(26, 'Act: Ladderbox9')
Ladderbox10 = ptAttribActivator(27, 'Act: Ladderbox10')
Ladderbox11 = ptAttribActivator(28, 'Act: Ladderbox11')
MultiStage1 = ptAttribBehavior(29, 'Mbeh01: Ladder1 Bottom', netForce=1)
MultiStage2 = ptAttribBehavior(30, 'Mbeh02: Ladder1 Top', netForce=1)
MultiStage3 = ptAttribBehavior(31, 'Mbeh03: Ladder2 Bottom', netForce=1)
MultiStage4 = ptAttribBehavior(32, 'Mbeh04: Ladder2 Top', netForce=1)
MultiStage5 = ptAttribBehavior(33, 'Mbeh05: Ladder3 Bottom', netForce=1)
MultiStage6 = ptAttribBehavior(34, 'Mbeh06: Ladder3 Top', netForce=1)
MultiStage7 = ptAttribBehavior(35, 'Mbeh07: Ladder4 Bottom', netForce=1)
MultiStage8 = ptAttribBehavior(36, 'Mbeh08: Ladder4 Top', netForce=1)
MultiStage9 = ptAttribBehavior(37, 'Mbeh09: Ladder2 Top Hang', netForce=1)
MultiStage10 = ptAttribBehavior(38, 'Mbeh10: Ladder3 Top Hang', netForce=1)
MultiStage11 = ptAttribBehavior(39, 'Mbeh11: Ladder4 Top Hang', netForce=1)
SolutionLadderBtm = ptAttribActivator(40, 'Act:Solution Ladder Btm')
MultiSolutionBtm = ptAttribBehavior(41, 'Mbeh:Solution Ladder Btm', netForce=1)
SolutionLadderTop = ptAttribActivator(42, 'Act:Solution Ladder Top')
MultiSolutionTop = ptAttribBehavior(43, 'Mbeh:Solution Ladder Top', netForce=1)
RedLight = ptAttribResponder(44, 'resp:Red Indicator Light', netForce=1)
actResetBtn = ptAttribActivator(45, 'act:Reset Button')
respResetBtn = ptAttribResponder(46, 'resp:Reset Button')
RaiseSolutionLadder = ptAttribResponder(47, 'resp: Raise Solution Ladder')
PillarCamBlocker = ptAttribAnimation(48, 'Unused')
respSfxRaisePillar01 = ptAttribResponder(49, 'resp:SFX Raise Pillar01')
respSfxRaisePillar02 = ptAttribResponder(50, 'resp:SFX Raise Pillar02')
respSfxRaisePillar03 = ptAttribResponder(51, 'resp:SFX Raise Pillar03')
respSfxRaisePillar04 = ptAttribResponder(52, 'resp:SFX Raise Pillar04')
respSfxLowerSolution = ptAttribResponder(53, 'resp:SFX Lower Solution Rings')
respSfxSolutionReset = ptAttribResponder(54, 'resp:SFX Reset Solution Rings')
respSfxResetFromHeight1 = ptAttribResponder(55, 'SFX Reset Pillar height 1', netForce=1)
respSfxResetFromHeight2 = ptAttribResponder(56, 'SFX Reset Pillar height 2', netForce=1)
respSfxResetFromHeight3 = ptAttribResponder(57, 'SFX Reset Pillar height 3', netForce=1)
respSfxResetFromHeight4 = ptAttribResponder(58, 'SFX Reset Pillar height 4', netForce=1)
respSolutionCam = ptAttribResponder(59, 'resp:Solution Cam')
OnlyOneOwner = ptAttribSceneobject(60, 'OnlyOneOwner')
Resetting = false
PullsInProgress = 0
AvatarWhoPulledLever = 0

class kdshPillarRoom(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5210
        version = 19
        self.version = version
        print '__init__kdshPillarRoom v.',
        print version,
        print '.5'


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        if (ageSDL == None):
            print 'kdshPillarRoom.OnFirstUpdate():\tERROR---missing SDL (%s)'
            return
        ageSDL.sendToClients('pheight01')
        ageSDL.sendToClients('pheight02')
        ageSDL.sendToClients('pheight03')
        ageSDL.sendToClients('pheight04')
        ageSDL.sendToClients('PillarsOccupied')
        ageSDL.sendToClients('budget')
        ageSDL.sendToClients('PillarsResetting')
        ageSDL.setFlags('pheight01', 1, 1)
        ageSDL.setFlags('pheight02', 1, 1)
        ageSDL.setFlags('pheight02', 1, 1)
        ageSDL.setFlags('pheight04', 1, 1)
        ageSDL.setFlags('PillarsOccupied', 1, 1)
        ageSDL.setFlags('budget', 1, 1)
        ageSDL.setFlags('PillarsResetting', 1, 1)
        self.CleanUpLaddersIfImAlone()
        ageSDL.setNotify(self.key, 'pheight01', 0.0)
        ageSDL.setNotify(self.key, 'pheight02', 0.0)
        ageSDL.setNotify(self.key, 'pheight03', 0.0)
        ageSDL.setNotify(self.key, 'pheight04', 0.0)
        ageSDL.setNotify(self.key, 'PillarsOccupied', 0.0)
        ageSDL.setNotify(self.key, 'budget', 0.0)
        ageSDL.setNotify(self.key, 'PillarRoomSolved', 0.0)
        ageSDL.setNotify(self.key, 'PillarsResetting', 0.0)
        print 'kdshPillarRoom: When I got here:'
        pillar = 1
        for pillar in [1, 2, 3, 4]:
            currentheight = ageSDL[('pheight0' + str(pillar))][0]
            print ('\t pheight0%s = %s ' % (pillar, currentheight))
            if (currentheight > 0):
                PillarAnim.byObject[('pillar0' + str(pillar))].skipToTime((currentheight * 10))
                self.EnableAppropriateLadders(pillar)
        print '\t budget = ',
        print ageSDL['budget'][0]
        CounterAnim.animation.skipToTime(((8 - ageSDL['budget'][0]) * 10))
        print '\t PillarRoomSolved = ',
        print ageSDL['PillarRoomSolved'][0]
        if (ageSDL['PillarRoomSolved'][0] == 1):
            SolutionResp.run(self.key, fastforward=1)
            SolutionLadderBtm.enable()
            SolutionLadderTop.enable()


    def OnNotify(self, state, id, events):
        global AvatarWhoPulledLever
        global Resetting
        global PullsInProgress
        ageSDL = PtGetAgeSDL()
        if (id in [1, 2, 3, 4, 5]):
            code = (('respLever0' + str(id)) + '.run(self.key, events=events)')
            exec code
            AvatarWhoPulledLever = PtFindAvatar(events)
            AvatarWhoPulledLever = PtGetClientIDFromAvatarKey(AvatarWhoPulledLever.getKey())
            return
        elif ((id in [6, 7, 8, 9]) and OnlyOneOwner.sceneobject.isLocallyOwned()):
            if Resetting:
                print 'Lever pull ignored because the puzzle is still resetting.'
                return
            if self.PillarIsSafeToMove(id):
                if (ageSDL['budget'][0] == 0):
                    print 'Counterweight expired.\n'
                elif (ageSDL[('pheight0' + str((id - 5)))][0] == 4):
                    print ('Pillar0%d is already at maximum height.' % (id - 5))
                else:
                    newheight = (ageSDL[('pheight0' + str((id - 5)))][0] + 1)
                    ageSDL[('pheight0' + str((id - 5)))] = (newheight,)
                    newbudget = (ageSDL['budget'][0] - 1)
                    ageSDL['budget'] = (newbudget,)
                    print ('%d pulls left' % newbudget)
            else:
                RedLight.run(self.key)
            return
        elif ((id == respResetBtn.id) or (id == respLever05.id)):
            if (not (OnlyOneOwner.sceneobject.isLocallyOwned())):
                return
            if (PullsInProgress > 0):
                print 'Can\'t reset now. PullsInProgress = ',
                print PullsInProgress
                return
            safetoreset = true
            for pillarcheck in [6, 7, 8, 9]:
                if self.PillarIsSafeToMove(pillarcheck):
                    pass
                else:
                    print 'kdshPillar.OnNotify: A reset button was pushed, but Pillar',
                    print (pillarcheck - 4),
                    print 'can\'t reset now.'
                    safetoreset = false
            if safetoreset:
                print 'kdshShadowPath Reset Button Pushed.'
                self.ResetPuzzle()
            return
        if (not (state)):
            return
        elif ((id >= 18) and ((id <= 28) and PtWasLocallyNotified(self.key))):
            print ('Ladderbox %s entered.' % (id - 17))
            LocalAvatar = PtFindAvatar(events)
            code = (('MultiStage' + str((id - 17))) + '.run(LocalAvatar)')
            exec code
            return
        elif ((id == SolutionLadderBtm.id) and PtWasLocallyNotified(self.key)):
            print 'Solution Ladder mounted from bottom.'
            LocalAvatar = PtFindAvatar(events)
            MultiSolutionBtm.run(LocalAvatar)
            return
        elif ((id == SolutionLadderTop.id) and PtWasLocallyNotified(self.key)):
            print 'Solution Ladder mounted from top.'
            LocalAvatar = PtFindAvatar(events)
            MultiSolutionTop.run(LocalAvatar)
            return
        elif (id == actResetBtn.id):
            print 'kdshPillarRoom Reset Button clicked.'
            LocalAvatar = PtFindAvatar(events)
            respResetBtn.run(self.key, events=events)
            return
        elif ((id == respSolutionCam.id) and PtWasLocallyNotified(self.key)):
            cam = ptCamera()
            cam.enableFirstPersonOverride()
            return


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global Resetting
        ageSDL = PtGetAgeSDL()
        if ((VARname == 'budget') or (VARname == 'PillarsOccupied')):
            return
        elif (VARname == 'PillarRoomSolved'):
            PtAtTimeCallback(self.key, 10, 5)
            return
        elif (VARname == 'PillarsResetting'):
            Resetting = ageSDL['PillarsResetting'][0]
            print 'kdshPillarRoom.OnSDLNotify: Resetting =',
            print Resetting
            if Resetting:
                for count in range(1, 12):
                    code = (('Ladderbox' + str(count)) + '.disable()')
                    exec code
                highest = 0
                sumofpulls = 0
                for pillar in [1, 2, 3, 4]:
                    thisheight = ageSDL[('pheight0' + str(pillar))][0]
                    sumofpulls = (sumofpulls + thisheight)
                    if (thisheight > highest):
                        highest = thisheight
                print 'The highest pillar when you reset was ',
                print highest,
                print ' notches high.'
                if (highest != 0):
                    PtAtTimeCallback(self.key, (5 * highest), 6)
                    code = (('respSfxResetFromHeight' + str(highest)) + '.run(self.key)')
                    exec code
                if (ageSDL['budget'][0] != 8):
                    CounterAnim.value.speed((2 * (float(sumofpulls) / float(highest))))
                    rangestart = ((8 - ageSDL['budget'][0]) * 10)
                    CounterAnim.value.playRange(rangestart, 0)
                    ageSDL['budget'] = (8,)
                for count in [1, 2, 3, 4]:
                    if (ageSDL[('pheight0' + str(count))][0] != 0):
                        PillarAnim.byObject[('pillar0' + str(count))].speed(2)
                        rangestart = (ageSDL[('pheight0' + str(count))][0] * 10)
                        PillarAnim.byObject[('pillar0' + str(count))].playRange(rangestart, 0)
                    ageSDL[('pheight0' + str(count))] = (0,)
                    print ('Pillar0%d height is now: %d' % (count, ageSDL[('pheight0' + str(count))][0]))
            return
        elif (not (Resetting)):
            id = string.atoi(VARname[-1:])
            newpheight = ageSDL[('pheight0' + str(id))][0]
            if (newpheight == 0):
                return
            self.RaiseAPillar(id)
            self.LowerCounterweight()
            self.CheckSolution()
            self.DisableAppropriateLadders(id)
            PtAtTimeCallback(self.key, 10, id)


    def CleanUpLaddersIfImAlone(self):
        ageSDL = PtGetAgeSDL()
        if (len(PtGetPlayerList()) == 0):
            ageSDL['PillarsOccupied'] = (0,)
            ageSDL['PillarsResetting'] = (0,)
        else:
            print 'kdshPillar.Load: I\'m not alone in Kadish. Leaving Ladder SDLs as they previously were.'


    def PillarIsSafeToMove(self, id):
        ageSDL = PtGetAgeSDL()
        if ageSDL['PillarsOccupied'][0]:
            print 'PillarIsSafeToMove: Can\'t do that now. Someone is on a pillar.'
            return false
        else:
            return true


    def RaiseAPillar(self, id):
        ageSDL = PtGetAgeSDL()
        PillarAnim.byObject[('pillar0' + str(id))].backwards(0)
        PillarAnim.byObject[('pillar0' + str(id))].speed(1)
        rangestart = ((ageSDL[('pheight0' + str(id))][0] - 1) * 10)
        rangeend = (ageSDL[('pheight0' + str(id))][0] * 10)
        PillarAnim.byObject[('pillar0' + str(id))].playRange(rangestart, rangeend)
        code = (('respSfxRaisePillar0' + str(id)) + '.run(self.key)')
        exec code
        print '\n##'
        print ('Pillar0%d height is now: %d' % (id, ageSDL[('pheight0' + str(id))][0]))


    def LowerCounterweight(self):
        global PullsInProgress
        ageSDL = PtGetAgeSDL()
        CounterAnim.value.backwards(0)
        PullsInProgress = (PullsInProgress + 1)
        CounterAnim.value.speed(PullsInProgress)
        rangeend = ((8 - ageSDL['budget'][0]) * 10)
        CounterAnim.animation.playToTime(rangeend)


    def CheckSolution(self):
        global AvatarWhoPulledLever
        ageSDL = PtGetAgeSDL()
        if ((ageSDL['pheight01'][0] == 1) and ((ageSDL['pheight02'][0] == 4) and ((ageSDL['pheight03'][0] == 1) and (ageSDL['pheight04'][0] == 2)))):
            print 'kdshPillarRoom: Puzzle solved. \n'
            ageSDL['PillarRoomSolved'] = (1,)
            avatar = PtGetLocalAvatar()
            myID = PtGetClientIDFromAvatarKey(avatar.getKey())
            print 'kdshPillarRoom.CheckSolution: AvatarWhoPulledLever=',
            print AvatarWhoPulledLever,
            print 'myID=',
            print myID
            if (myID == AvatarWhoPulledLever):
                print '\tI pulled the final lever. Playing solution cam.'
                cam = ptCamera()
                cam.undoFirstPerson()
                cam.disableFirstPersonOverride()
                respSolutionCam.run(self.key)
            else:
                print '\tI did not pull the final lever.'


    def ResetPuzzle(self):
        ageSDL = PtGetAgeSDL()
        budget = ageSDL['budget'][0]
        print 'kdshPillarRoom.ResetPuzzle: budget = ',
        print budget
        if (budget != 8):
            ageSDL['PillarsResetting'] = (1,)
            ageSDL['PillarRoomSolved'] = (0,)
            print '\tAt least one pillar has been raised. Resetting Pillar puzzle'
        else:
            print 'Each of the four pillars was already down. Won\'t reset.'
            return


    def OnTimer(self, id):
        global PullsInProgress
        global Resetting
        ageSDL = PtGetAgeSDL()
        if (id in [1, 2, 3, 4]):
            self.EnableAppropriateLadders(id)
            PullsInProgress = (PullsInProgress - 1)
        elif (id == 5):
            PillarRoomSolved = ageSDL['PillarRoomSolved'][0]
            if PillarRoomSolved:
                SolutionResp.run(self.key)
                respSfxLowerSolution.run(self.key)
                SolutionLadderBtm.enable()
                SolutionLadderTop.enable()
            else:
                RaiseSolutionLadder.run(self.key)
                respSfxSolutionReset.run(self.key)
                SolutionLadderBtm.disable()
                SolutionLadderTop.disable()
            return
        elif (id == 6):
            if Resetting:
                ageSDL['PillarsResetting'] = (0,)
                Resetting = 0


    def DisableAppropriateLadders(self, pillar):
        if (pillar == 1):
            ladderstodisable = [1, 2, 3, 4, 9]
        elif (pillar == 2):
            ladderstodisable = [3, 4, 5, 6, 9, 10]
        elif (pillar == 3):
            ladderstodisable = [5, 6, 7, 8, 10, 11]
        elif (pillar == 4):
            ladderstodisable = [7, 8, 11]
        for each in ladderstodisable:
            code = (('Ladderbox' + str(each)) + '.disable()')
            exec code


    def EnableAppropriateLadders(self, id):
        ageSDL = PtGetAgeSDL()
        if (id != 1):
            difference01 = (ageSDL[('pheight0' + str(id))][0] - ageSDL[('pheight0' + str((id - 1)))][0])
            tolerance01 = (5 - id)
            if (difference01 >= 1):
                if (difference01 > tolerance01):
                    code = (('Ladderbox' + str(((id * 2) - 1))) + '.disable()')
                    exec code
                    code = (('Ladderbox' + str((id * 2))) + '.disable()')
                    exec code
                    code = (('Ladderbox' + str((id + 7))) + '.enable()')
                    exec code
                else:
                    code = (('Ladderbox' + str(((id * 2) - 1))) + '.enable()')
                    exec code
                    code = (((('MultiStage' + str(((id * 2) - 1))) + '.setLoopCount(1,') + str(((6 * difference01) - 4))) + ')')
                    exec code
                    code = (('Ladderbox' + str((id * 2))) + '.enable()')
                    exec code
                    code = (((('MultiStage' + str((id * 2))) + '.setLoopCount(1,') + str(((6 * difference01) - 4))) + ')')
                    exec code
                    code = (('Ladderbox' + str((id + 7))) + '.disable()')
                    exec code
            else:
                code = (('Ladderbox' + str(((id * 2) - 1))) + '.disable()')
                exec code
                code = (('Ladderbox' + str((id * 2))) + '.disable()')
                exec code
        else:
            rungs = ((6 * ageSDL['pheight01'][0]) - 4)
            MultiStage1.setLoopCount(1, rungs)
            Ladderbox1.enable()
            rungs = ((6 * ageSDL['pheight01'][0]) - 4)
            MultiStage2.setLoopCount(1, rungs)
            Ladderbox2.enable()
        if (id != 4):
            difference02 = (ageSDL[('pheight0' + str((id + 1)))][0] - ageSDL[('pheight0' + str(id))][0])
            tolerance02 = (5 - (id + 1))
            if (difference02 >= 1):
                if (difference02 > tolerance02):
                    code = (('Ladderbox' + str(((id * 2) + 1))) + '.disable()')
                    exec code
                    code = (('Ladderbox' + str(((id * 2) + 2))) + '.disable()')
                    exec code
                    code = (('Ladderbox' + str((id + 8))) + '.enable()')
                    exec code
                else:
                    code = (('Ladderbox' + str(((id * 2) + 1))) + '.enable()')
                    exec code
                    code = (((('MultiStage' + str(((id * 2) + 1))) + '.setLoopCount(1,') + str(((6 * difference02) - 4))) + ')')
                    exec code
                    code = (('Ladderbox' + str(((id * 2) + 2))) + '.enable()')
                    exec code
                    code = (((('MultiStage' + str(((id * 2) + 2))) + '.setLoopCount(1,') + str(((6 * difference02) - 4))) + ')')
                    exec code
                    code = (('Ladderbox' + str((id + 8))) + '.disable()')
                    exec code
        elif (ageSDL['pheight04'][0] == 4):
            print 'Pillar04 has reached the red herring door'


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



