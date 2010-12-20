# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import xSndLogTracks
actSwitch01 = ptAttribActivator(1, 'Act: Roof Button')
respButtonOneshot = ptAttribResponder(21, 'Resp: Main Light Oneshot')
respFloorDark = ptAttribResponder(2, 'Resp: Floor Dark')
respFloorGlow = ptAttribResponder(3, 'Resp: Floor Glow')
respFloorLitFromDark = ptAttribResponder(4, 'Resp: LitFromDark')
respFloorLitFromGlow = ptAttribResponder(5, 'Resp: LitFromGlow')
respZone01 = ptAttribActivator(6, 'Glow Zone 01')
respZone02 = ptAttribActivator(7, 'Glow Zone 02')
respZone03 = ptAttribActivator(8, 'Glow Zone 03')
respZone04 = ptAttribActivator(9, 'Glow Zone 04')
respZone05 = ptAttribActivator(10, 'Glow Zone 05')
respZone06 = ptAttribActivator(11, 'Glow Zone 06')
respZone07 = ptAttribActivator(12, 'Glow Zone 07')
respZone08 = ptAttribActivator(13, 'Glow Zone 08')
respZone09 = ptAttribActivator(14, 'Glow Zone 09')
respZone10 = ptAttribActivator(15, 'Glow Zone 10')
respFloorZone = ptAttribActivator(16, 'Floor Zone')
rgnEnterSubTop = ptAttribActivator(17, 'Elev Rgn at top')
respElevDown = ptAttribResponder(18, 'resp: Elev Down', netForce=1)
rgnEnterSubBtm = ptAttribActivator(19, 'Elev Rgn at bottom')
respElevUp = ptAttribResponder(20, 'resp: Elev Up', netForce=1)
elevatorsubworld = ptAttribSceneobject(22, 'elevator subworld')
actResetBtn = ptAttribActivator(23, 'act:Reset Button')
respResetBtn = ptAttribResponder(24, 'resp:Reset Button')
xRgnTop = ptAttribExcludeRegion(25, 'xRgn Top of Shaft')
xRgnBottom = ptAttribExcludeRegion(26, 'xRgn Bottom of Shaft')
rgnExitSubTop = ptAttribActivator(27, 'rgn:Exit Subworld Top')
rgnExitSubBtm = ptAttribActivator(28, 'rgn:Exit Subworld Btm')
objExitTop = ptAttribSceneobjectList(29, 'ExitTopRegions')
OnlyOneOwner = ptAttribSceneobject(30, 'OnlyOneOwner')
ElapsedTime = 0
SecondsToCharge = 60
baton = 0
ElevatorDelay = 5
Resetting = 0

class kdshGlowInTheDark(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5212
        version = 10
        self.version = version
        print '__init__kdshGlowInTheDark v.',
        print version,
        print '.5'


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        if (ageSDL == None):
            print 'kdshGlowInTheDark:\tERROR---Cannot find the Kadish Age SDL'
        ageSDL.setNotify(self.key, 'RoofClosed', 0.0)
        ageSDL.setNotify(self.key, 'GlowCharged', 0.0)
        ageSDL.setNotify(self.key, 'TimeOpened', 0.0)
        ageSDL.sendToClients('RoofClosed')
        ageSDL.sendToClients('GlowCharged')
        ageSDL.sendToClients('TimeOpened')
        ageSDL.sendToClients('GlowInTheDarkSolved')
        ageSDL.setFlags('RoofClosed', 1, 1)
        ageSDL.setFlags('GlowCharged', 1, 1)
        ageSDL.setFlags('TimeOpened', 1, 1)
        ageSDL.setFlags('GlowInTheDarkSolved', 1, 1)
        RoofClosed = ageSDL['RoofClosed'][0]
        GlowCharged = ageSDL['GlowCharged'][0]
        solved = ageSDL['GlowInTheDarkSolved'][0]
        print 'kdshGlowInTheDark: When I got here:'
        if (not RoofClosed):
            print '\tThe roof was open when I got here.'
            respFloorLitFromGlow.run(self.key, fastforward=1)
        else:
            print '\tThe roof is still closed.'
        if (RoofClosed and GlowCharged):
            print '\tThe floor was glowing when I got here.'
            PtAtTimeCallback(self.key, 1, 5)
        else:
            print '\tThe floor is not charged.'
        if solved:
            print '\tThe puzzle was solved.'
            print '\tThere are',
            print len(PtGetPlayerList()),
            print ' other players in this Kadish instance.'
            if (len(PtGetPlayerList()) == 0):
                print "\t I'm alone, so I'm starting the elevator."
                respElevDown.run(self.key)
                PtAtTimeCallback(self.key, 3, 2)
            else:
                print '\t Someone else was already in this Kadish instance. Depending on Overriding HighSDL component to synch elevator.'
        else:
            print '\t The puzzle has not been solved. Putting elevator at the top.'
            respElevUp.run(self.key, fastforward=true)


    def OnNotify(self, state, id, events):
        global Resetting
        global baton
        ageSDL = PtGetAgeSDL()
        if (not state):
            return
        if (id == actSwitch01.id):
            respButtonOneshot.run(self.key, events=events)
            return
        elif ((id == respButtonOneshot.id) and OnlyOneOwner.sceneobject.isLocallyOwned()):
            print '##'
            oldstate = ageSDL['RoofClosed'][0]
            if (oldstate == 1):
                print 'kdshGlowInTheDark: The roof is now open.'
                self.RecordOpenTime()
                GlowCharged = ageSDL['GlowCharged'][0]
                print 'kdshGlowInTheDark: GlowCharged = ',
                print GlowCharged
            elif (oldstate == 0):
                print 'kdshGlowInTheDark: The roof is now closed.'
                self.CalculateTimeOpen()
            else:
                print ('kdshGlowInTheDark: Unexpected roof state: (%s)' % newstate)
            newstate = abs((oldstate - 1))
            ageSDL['RoofClosed'] = (newstate,)
            return
        elif (id == respElevDown.id):
            print 'kdshGlowInTheDark: The elevator has reached the bottom.'
            PtAtTimeCallback(self.key, ElevatorDelay, 1)
            xRgnBottom.releaseNow(self.key)
            rgnEnterSubBtm.enable()
            return
        elif (id == respElevUp.id):
            print 'kdshGlowInTheDark: The elevator has reached the top.'
            PtAtTimeCallback(self.key, ElevatorDelay, 3)
            xRgnTop.releaseNow(self.key)
            rgnEnterSubTop.enable()
            for region in objExitTop.value:
                region.physics.suppress(0)
            return
        elif ((id >= 6) and (id <= 15)):
            if PtWasLocallyNotified(self.key):
                self.BatonPassCheck(id, events)
            return
        elif (id == 16):
            for event in events:
                if ((event[0] == 1) and (event[1] == 1)):
                    print 'kdshGlowInTheDark: A second player stepped on floor.'
                    baton = 0
                elif (event[0] == 1):
                    print 'kdshGlowInTheDark: Floor unoccupied.'
            return
        elif (id == actResetBtn.id):
            print 'kdshGlowInTheDark Reset Button clicked.'
            Resetting = 1
            respResetBtn.run(self.key, events=events)
            return
        elif ((id == respResetBtn.id) and OnlyOneOwner.sceneobject.isLocallyOwned()):
            print 'kdshGlowInTheDark Reset Button Pushed. Puzzle resetting.'
            ageSDL['RoofClosed'] = (1,)
            ageSDL['GlowCharged'] = (0,)
            ageSDL['TimeOpened'] = (0,)
            ageSDL['GlowInTheDarkSolved'] = (0,)
            xSndLogTracks.LogTrack('94', '143')
            return
        elif ((id == rgnExitSubTop.id) and PtWasLocallyNotified(self.key)):
            print 'kdshGlowInTheDark: You stepped off the elevator at the top. Removing from Subworld'
            avatarInElevator = PtFindAvatar(events)
            avatarInElevator.avatar.exitSubWorld()
            return
        elif ((id == rgnExitSubBtm.id) and PtWasLocallyNotified(self.key)):
            print 'kdshGlowInTheDark: You stepped off the elevator at the btm. Removing from Subworld'
            avatarInElevator = PtFindAvatar(events)
            avatarInElevator.avatar.exitSubWorld()
            return
        elif ((id == rgnEnterSubTop.id) and PtWasLocallyNotified(self.key)):
            print 'You stepped on the elevator at the top. Joining subworld.'
            for region in objExitTop.value:
                region.physics.suppress(1)
            avatarInElevator = PtFindAvatar(events)
            avatarInElevator.avatar.enterSubWorld(elevatorsubworld.value)
            return
        elif ((id == rgnEnterSubBtm.id) and PtWasLocallyNotified(self.key)):
            print 'You stepped on the elevator at the bottom. Joining subworld.'
            rgnExitSubBtm.disable()
            avatarInElevator = PtFindAvatar(events)
            avatarInElevator.avatar.enterSubWorld(elevatorsubworld.value)
            return
        else:
            for event in events:
                if (event[0] == kVariableEvent):
                    TimerID = int(event[3])
                    if (TimerID == 1):
                        print 'kdshGlowInTheDark: Timer 1 Callback. Raising elevator again.'
                        xRgnBottom.clearNow(self.key)
                        rgnExitSubBtm.disable()
                        if (not self.sceneobject.isLocallyOwned()):
                            print "\tI'm not the owner, so I'll let another client netforce raise the elevator."
                            return
                        else:
                            respElevUp.run(self.key)
                    if (TimerID == 2):
                        print 'kdshGlowInTheDark: Timer 2 Callback. Clearing top Xrgn'
                        xRgnTop.clearNow(self.key)
                        rgnEnterSubTop.disable()
                    if (TimerID == 3):
                        print 'kdshGlowInTheDark: Timer 3 Callback.'
                        ageSDL = PtGetAgeSDL()
                        solved = ageSDL['GlowInTheDarkSolved'][0]
                        if solved:
                            print '\t Puzzle is still solved. Lowering Elevator again.'
                            PtAtTimeCallback(self.key, 1, 2)
                            for region in objExitTop.value:
                                region.physics.suppress(1)
                            rgnExitSubBtm.enable()
                            if (not self.sceneobject.isLocallyOwned()):
                                print "\tI'm not the owner, so I'll let another client netforce lower the elevator."
                                return
                            else:
                                respElevDown.run(self.key)
                        else:
                            print '\t Puzzle has been reset. Leaving elevator alone at top.'
                            rgnEnterSubTop.disable()
                            for region in objExitTop.value:
                                region.physics.suppress(0)
                    if (TimerID == 4):
                        print 'kdshGlowInTheDark: Timer 4 Callback.'
                        print '\tkdshGlowInTheDark.OnTimer: Running from Lit to Dark.'
                        respFloorDark.run(self.key)
                        Resetting = 0


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        if (VARname == 'RoofClosed'):
            RoofClosed = ageSDL['RoofClosed'][0]
            GlowCharged = ageSDL['GlowCharged'][0]
            if (RoofClosed and (GlowCharged and Resetting)):
                return
            if (RoofClosed == 0):
                if (GlowCharged == 0):
                    respFloorLitFromDark.run(self.key)
                else:
                    respFloorLitFromGlow.run(self.key)
            elif (RoofClosed == 1):
                if (GlowCharged == 1):
                    respFloorGlow.run(self.key)
                else:
                    respFloorDark.run(self.key)
        elif (VARname == 'TimeOpened'):
            TimeOpened = ageSDL['TimeOpened'][0]
        elif (VARname == 'GlowCharged'):
            if (not Resetting):
                return
            GlowCharged = ageSDL['GlowCharged'][0]
            print '\tkdshGlowInTheDark.OnSDLNotify: GlowCharged now =',
            print GlowCharged
            PtAtTimeCallback(self.key, 6, 4)
            respFloorLitFromGlow.run(self.key)
            return


    def RecordOpenTime(self):
        ageSDL = PtGetAgeSDL()
        CurrentTime = PtGetDniTime()
        print 'kdshGlowInTheDark: The roof was opened at: ',
        print CurrentTime
        ageSDL['TimeOpened'] = (CurrentTime,)


    def CalculateTimeOpen(self):
        ageSDL = PtGetAgeSDL()
        TimeOpened = ageSDL['TimeOpened'][0]
        CurrentTime = PtGetDniTime()
        ElaspedTime = (CurrentTime - TimeOpened)
        if (ElaspedTime > SecondsToCharge):
            print 'kdshGlowInTheDark: The floor is now charged'
            ageSDL['GlowCharged'] = (1,)


    def BatonPassCheck(self, id, events):
        global baton
        ageSDL = PtGetAgeSDL()
        print '##'
        for event in events:
            if (event[0] == 7):
                break
            if (event[1] == 1):
                print 'kdshGlowInTheDark: Entered Zone:',
                print (id - 5)
                if (id == 6):
                    baton = 1
                elif (id == (baton + 6)):
                    baton = (baton + 1)
            elif (event[1] == 0):
                print ' kdshGlowInTheDark: Exited Zone:',
                print (id - 5)
                if ((baton != (id - 4)) and (baton != 0)):
                    print 'kdshGlowInTheDark: Dropped the baton.'
                    baton = 0
                if ((id == 14) and (baton == 10)):
                    solved = ageSDL['GlowInTheDarkSolved'][0]
                    if (not solved):
                        print 'GlowInTheDark: Puzzle solved.'
                        ageSDL['GlowInTheDarkSolved'] = (1,)
                        baton = 0
                    else:
                        print 'GlowInTheDark: Yes, you completed the path, but I thought the path was already solved.'
                        return
                    if PtWasLocallyNotified(self.key):
                        print 'kdshGlowInTheDark: Since you solved the puzzle, putting your avatar on elevator'
                        avatarInElevator = PtFindAvatar(events)
                        avatarInElevator.avatar.enterSubWorld(elevatorsubworld.value)
                    rgnEnterSubTop.enable()
                    respElevDown.run(self.key)
                    PtAtTimeCallback(self.key, 3, 2)
        if (baton > 0):
            print 'kdshGlowInTheDark: Baton value is now:',
            print baton


    def OnTimer(self, id):
        if (id == 1):
            note = ptNotify(self.key)
            note.clearReceivers()
            note.addReceiver(self.key)
            note.setActivate(1)
            note.addVarNumber('foo', id)
            note.send()
        if (id == 2):
            if (not self.sceneobject.isLocallyOwned()):
                print "\tI'm not the owner, so I'll let another client tell all clients to clear top Xrgn."
                return
            else:
                note = ptNotify(self.key)
                note.clearReceivers()
                note.addReceiver(self.key)
                note.setActivate(1)
                note.addVarNumber('foo', id)
                note.send()
        if (id == 3):
            note = ptNotify(self.key)
            note.clearReceivers()
            note.addReceiver(self.key)
            note.setActivate(1)
            note.addVarNumber('foo', id)
            note.send()
        if (id == 4):
            note = ptNotify(self.key)
            note.clearReceivers()
            note.addReceiver(self.key)
            note.setActivate(1)
            note.addVarNumber('foo', id)
            note.send()
        if (id == 5):
            print "kdshGlowInTheDark: It's been one second. FF'ing floor to glow state."
            respFloorGlow.run(self.key, fastforward=1)


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



