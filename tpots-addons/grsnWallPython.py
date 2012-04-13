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
from PlasmaKITypes import *
import cPickle
## blockers activators on the panels
northPanelClick = ptAttribActivator(1, 'North Panel Clickables')
southPanelClick = ptAttribActivator(2, 'South Panel Clickables')
## blockers physics on both panels
northPanel = ptAttribSceneobjectList(3, 'North Panel Objects', byObject=1)
southPanel = ptAttribSceneobjectList(4, 'South Panel Objects', byObject=1)
## blockers physicals on the Wall (remember to check because the SOUTH blockers are of course on the NORTH wall !!!)
northWall = ptAttribSceneobjectList(5, 'North Wall', byObject=1)
southWall = ptAttribSceneobjectList(6, 'South Wall', byObject=1)
## chair clickable (to init game)
northChair = ptAttribActivator(7, 'North Chair')
southChair = ptAttribActivator(8, 'South Chair')
## blockers drawed on the panel
northLights = ptAttribSceneobjectList(9, 'North Panel Lights', byObject=1)
southLights = ptAttribSceneobjectList(10, 'South Panel Lights', byObject=1)
## blocker counters decals on the panels
northCountLights = ptAttribSceneobjectList(11, 'North Count Lights', byObject=1)
southCountLights = ptAttribSceneobjectList(12, 'South Count Lights', byObject=1)
## south panel blocker count buttons
upButtonS = ptAttribActivator(13, 'S up count button')
dnButtonS = ptAttribActivator(14, 'S down count button')
readyButtonS = ptAttribActivator(15, 'S ready button')
## north panel blocker count buttons
upButtonN = ptAttribActivator(18, 'N up count button')
dnButtonN = ptAttribActivator(19, 'N down count button')
readyButtonN = ptAttribActivator(20, 'N ready button')
## open tube/reset/turn on Wall
goButtonN = ptAttribActivator(21, 'N Go Button activator')
goButtonS = ptAttribActivator(22, 'S Go Button activator')
## layer anim for big buttons responders
goBtnNResp = ptAttribResponder(23, 'N Go Button anim responder', ["unknown", "bright", "dim", "pulse"], netForce=0) # "unknown" is the default layer anim. I don't know what it is, I didn't test it.
goBtnSResp = ptAttribResponder(24, 'S Go Button anim responder', ["unknown", "bright", "dim", "pulse"], netForce=0)
## SittingModifier (notify when we exit the chair. Check again to make sure)
nChairSit = ptAttribActivator(25, 'N sit component')
sChairSit = ptAttribActivator(26, 'S sit component')
## north panel blocker preset buttons
fiveBtnN = ptAttribActivator(27, '5 btn N')
tenBtnN = ptAttribActivator(28, '10 btn N')
fifteenBtnN = ptAttribActivator(29, '15 btn N')
## south panel blocker preset buttons
fiveBtnS = ptAttribActivator(30, '5 btn S')
tenBtnS = ptAttribActivator(31, '10 btn S')
fifteenBtnS = ptAttribActivator(32, '15 btn S')
## open tubes responders
sTubeOpen = ptAttribNamedResponder(33, 'S tube open', netForce=0)
nTubeOpen = ptAttribNamedResponder(34, 'N tube open', netForce=0)
## close tubes responders
sTubeClose = ptAttribNamedResponder(35, 'S tube close', ['down', 'closed'], netForce=0) # new states: will make sure we won't open traps if there is no triggerer
nTubeClose = ptAttribNamedResponder(36, 'N tube close', ['down', 'closed'], netForce=0)
## logic modifier for avatar dectect in the tube
sTubeEntry = ptAttribNamedActivator(37, 'S tube entry trigger')
nTubeEntry = ptAttribNamedActivator(38, 'N tube entry trigger')
## MultistageBehavior to animate avatar in tube
sTubeMulti = ptAttribBehavior(43, 's tube entry multi', netForce=0)
nTubeMulti = ptAttribBehavior(44, 'n tube entry multi', netForce=0)
## tube exclude regions
sTubeExclude = ptAttribExcludeRegion(45, 's tube exclude')
nTubeExclude = ptAttribExcludeRegion(46, 'n tube exclude')
## warp points to Wall area (these are wrong - var "north" is used for "south" wp)
nTeamWarpPt = ptAttribSceneobject(47, 'n team warp point')
sTeamWarpPt = ptAttribSceneobject(48, 's team warp point')
## top wall win region
sTeamWin = ptAttribActivator(49, 's team win')
nTeamWin = ptAttribActivator(50, 'n team win')
## quit activators
sTeamQuit = ptAttribActivator(51, 's team quit')
nTeamQuit = ptAttribActivator(52, 'n team quit')
## quit wps
sTeamWinTeleport = ptAttribSceneobject(53, 's team win point')
nTeamWinTeleport = ptAttribSceneobject(54, 'n team win point')
## ss and anim before link
nQuitBehavior = ptAttribBehavior(55, 's quit behavior', netForce=0)
sQuitBehavior = ptAttribBehavior(56, 'n quit behavior', netForce=0)
## sfx responders
# I know it would be better if netForce was 0, but it would be too complicated in OnNotify (these don't send a lot of messages anyway)
nPanelSound = ptAttribResponder(57, 'n panel sound', ['main', 'up', 'down', 'select', 'blockerOn', 'blockerOff', 'gameStart', 'denied'], netForce=1)
sPanelSound = ptAttribResponder(58, 's panel sound', ['main', 'up', 'down', 'select', 'blockerOn', 'blockerOff', 'gameStart', 'denied'], netForce=1)


## for team light responders (count)
# also used for blockers
kTeamLightsOn = 0
kTeamLightsOff = 1
# not for blockers
kRedOn = 3
kRedOff = 4
kRedFlash = 2
##

## for go button light states (not used anymore)
kDim = 0 # desactivated
kBright = 1 # can be pushed
kPulse = 2 # has to be pushed

## current game state (assuming Wall off, if there is a game running it will be updated)
SouthState = ptClimbingWallMsgState.kWaiting
NorthState = ptClimbingWallMsgState.kWaiting
## current blockers set and max number
NorthCount = 0
SouthCount = 0
BlockerCountLimit = 0
## sets which blocker (from 0 to 171) is set for each of the panels
NorthWall = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
SouthWall = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
## tells which messages we have to receive (when we link-in or when we're playing)
ReceiveInit = false
## accessories avatar can be wearing
MaleSuit = ['03_MHAcc_SuitHelmet', '03_MLHand_Suit', '03_MRHand_Suit', '03_MTorso_Suit', '03_MLegs_Suit', '03_MLFoot_Suit', '03_MRFoot_Suit']
FemaleSuit = ['03_FHair_SuitHelmet', '03_FLHand_Suit', '03_FRHand_Suit', '03_FTorso_Suit', '03_FLegs_Suit', '03_FLFoot_Suit', '03_FRFoot_Suit']

class grsnWallPython(ptResponder):
# VERSION: modified
# This is for all the bugs with netForce and not fastforwarded responders.
# This is not sure it will work.

## INFO:
# changed UpdateBlockerCountDisplay. It won't set the counter lights to off as it was send only by ZeroBlockerCount, which is called by SetN/SPanelMode
# layer anim for blockers not run on server init complete: this isn't needed.

## TODO:
# -test

    def __init__(self):
        PtDebugPrint('grsnWallPython::__init__')
        ptResponder.__init__(self)
        self.id = 52392
        self.version = 3


    def OnServerInitComplete(self):
        '''Tells what to do on link-in'''
        global ReceiveInit
        PtDebugPrint('grsnWallPython::OnServerInitComplete')
        """These SDLs should not be used -> chair acivator should be disabled.
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags('nChairOccupant', 0, 1)
        ageSDL.setFlags('sChairOccupant', 0, 1)
        ageSDL.setNotify(self.key, 'nChairOccupant', 0.0)
        ageSDL.setNotify(self.key, 'sChairOccupant', 0.0)
        ageSDL.sendToClients('nChairOccupant')
        ageSDL.sendToClients('sChairOccupant')"""
        solo = true
        if len(PtGetPlayerList()):
            # a game is already running, ask its state
            solo = false
            ReceiveInit = true # accept OnClimbingWallInit  and not OnClimbingWallEvent
            print 'requesting game state message from master client'
            msg = ptClimbingWallMsg(self.key)
            msg.init(ptClimbingWallMsgType.kRequestGameState, 0, 0)
            msg.send()
            return
        else:
            # we don't need to ask game state
            print 'solo in climbing wall -> no need to ask game state.'

        # self.InitPanels() will now fastforward the responders.
        self.InitPanels()
        sTubeClose.run(self.key, state='closed', fastforward=1)
        nTubeClose.run(self.key, state='closed', fastforward=1)
        sTubeExclude.clear(self.key)
        nTubeExclude.clear(self.key)
        """ Theses SDLs should not be used, and both sides state is already set.
        if solo:
            ageSDL.setIndex('nChairOccupant', 0, -1)
            ageSDL.setIndex('sChairOccupant', 0, -1)
            ageSDL.setIndex('nWallPlayer', 0, -1)
            ageSDL.setIndex('sWallPlayer', 0, -1)
            SouthState = ptClimbingWallMsgState.kWaiting
            NorthState = ptClimbingWallMsgState.kWaiting"""


    def OnClimbingWallInit(self, type, state, value):
        '''Receives infos from current playing game (only on link-in)'''
        global ReceiveInit
        global BlockerCountLimit
        global SouthWall
        global NorthWall
        global SouthState
        global NorthState
        print 'grsnClimbingWall::OnClimbingWallInit type ',
        print type,
        print ' state ',
        print state,
        print ' value ',
        print value
        if (ReceiveInit == false): # don't receive a running game message
            print 'failed to receive init'
            return
        if (type == ptClimbingWallMsgType.kEndGameState):
            ReceiveInit = false # stop receiving init messages
            print 'finished receiving total game state'
            # set all the panel count lights
            i = 0
            while ((i < BlockerCountLimit)):
                northCountLights.value[i].runAttachedResponder(kTeamLightsOff)
                southCountLights.value[i].runAttachedResponder(kTeamLightsOff)
                i = (i + 1)
            i = BlockerCountLimit
            while ((i < 20)):
                northCountLights.value[i].runAttachedResponder(kRedOn)
                southCountLights.value[i].runAttachedResponder(kRedOn)
                i = (i + 1)
            i = 0
            j = 0
            while ((i < BlockerCountLimit)):
                if (SouthWall[i] > 0):
                    southCountLights.value[j].runAttachedResponder(kTeamLightsOn)
                    j = (j + 1)
                i = (i + 1)
            i = 0
            j = 0
            while ((i < BlockerCountLimit)):
                if (NorthWall[i] > 0):
                    northCountLights.value[j].runAttachedResponder(kTeamLightsOn)
                    j = (j + 1)
                i = (i + 1)
            return
        if (type == ptClimbingWallMsgType.kTotalGameState):
            SouthState = state
            NorthState = value
            print 'begin receiving total game state'
        elif ((type == ptClimbingWallMsgType.kAddBlocker) and (state >= 0)):
            self.SetWallIndex(state, true, value)
            if value:
                self.ChangeNorthBlocker(state)
            else:
                self.ChangeSouthBlocker(state)
        elif (type == ptClimbingWallMsgType.kSetBlockerNum):
            BlockerCountLimit = value
            self.UpdateBlockerCountDisplay(state)


    def OnClimbingWallEvent(self, type, state, value):
        '''Receives infos from current playing game'''
        global ReceiveInit
        global NorthState
        global SouthState
        global BlockerCountLimit
        global NorthWall
        global SouthWall
        if ReceiveInit: # don't accept messages if we didn't received game state (link in)
            return
        print 'grsnClimbingWall::OnClimbingWallMsg type ',
        print type,
        print ' state ',
        print state,
        print ' value ',
        print value
        if (type == ptClimbingWallMsgType.kNewState):
            # update state of the team
            if (value == 1):
                NorthState = state
                self.SetNPanelMode(state)
            else:
                SouthState = state
                self.SetSPanelMode(state)
        elif (type == ptClimbingWallMsgType.kAddBlocker):
            # add new blocker
            self.SetWallIndex(state, true, value)
            if value:
                self.ChangeNorthBlocker(state)
            else:
                self.ChangeSouthBlocker(state)
        elif (type == ptClimbingWallMsgType.kRemoveBlocker):
            # remove blocker we set
            self.SetWallIndex(state, false, value)
            if value:
                self.ChangeNorthBlocker(state)
            else:
                self.ChangeSouthBlocker(state)
        elif (type == ptClimbingWallMsgType.kSetBlockerNum):
            # set max number of available blockers
            BlockerCountLimit = value
            self.UpdateBlockerCountDisplay(state)
        elif (type == ptClimbingWallMsgType.kRequestGameState):
            # visitor wants to know if we're playing, so why don't we tell him ?
            if (self.IAmMaster() == false):
                return
            msg = ptClimbingWallMsg(self.key)
            msg.createGameState(BlockerCountLimit, SouthState, NorthState)
            i = 0
            while ((i < BlockerCountLimit)):
                msg.addBlocker(NorthWall[i], i, true)
                msg.addBlocker(SouthWall[i], i, false)
                i = (i + 1)
            msg.send()


    def SetSPanelMode(self, state):
        '''Update panel with specified state'''
        global BlockerCountLimit
        global NorthState
        print 'set S Panel Mode called with state ',
        print state
        if (state == ptClimbingWallMsgState.kWaiting): # this should never be called: we'll always use state "Sit" to restart game
            self.ResetSouthPanel()
            sTubeExclude.clear(self.key)
            sTubeClose.run(self.key, avatar=PtGetLocalAvatar(), state='closed')
            goBtnSResp.run(self.key, avatar=PtGetLocalAvatar(), state="dim")
        elif (state == ptClimbingWallMsgState.kSouthSit):
            goBtnSResp.run(self.key, avatar=PtGetLocalAvatar(), state="bright")
        elif (state == ptClimbingWallMsgState.kSouthSelect):
            self.ResetSouthPanel()
            i = 0
            while ((i < 20)):
                southCountLights.value[i].runAttachedResponder(kRedFlash)
                i = (i + 1)
            print 'enabled all s switches'
        elif (state == ptClimbingWallMsgState.kSouthReady):
            i = 0
            while ((i < BlockerCountLimit)):
                southCountLights.value[i].runAttachedResponder(kTeamLightsOff)
                i = (i + 1)
            i = BlockerCountLimit
            while ((i < 20)):
                southCountLights.value[i].runAttachedResponder(kRedOn)
                i = (i + 1)
            upButtonS.disable()
            dnButtonS.disable()
            readyButtonS.disable()
            fiveBtnS.disable()
            tenBtnS.disable()
            fifteenBtnS.disable()
            goBtnSResp.run(self.key, avatar=PtGetLocalAvatar(), state="pulse")
        elif (state == ptClimbingWallMsgState.kSouthPlayerEntry):
            self.EnableSouthButtons(false)
            goBtnSResp.run(self.key, avatar=PtGetLocalAvatar(), state="dim")
            if (NorthState == ptClimbingWallMsgState.kNorthPlayerEntry):
                # other side was waiting for us, so WE have to update the tubes
                sTubeOpen.run(self.key, avatar=PtGetLocalAvatar())
                nTubeOpen.run(self.key, avatar=PtGetLocalAvatar())
                print 'tubes open'
        elif ((state == ptClimbingWallMsgState.kNorthQuit) or ((state == ptClimbingWallMsgState.kNorthWin) or ((state == ptClimbingWallMsgState.kSouthQuit) or (state == ptClimbingWallMsgState.kSouthWin)))):
            sTubeExclude.clear(self.key)
            sTubeClose.run(self.key, avatar=PtGetLocalAvatar(), state='closed')
            goBtnSResp.run(self.key, avatar=PtGetLocalAvatar(), state="bright")


    def SetNPanelMode(self, state):
        '''Update panel with specified state'''
        global BlockerCountLimit
        global SouthState
        print 'set N Panel Mode called with state ',
        print state
        if (state == ptClimbingWallMsgState.kWaiting): # this should never be called: we'll always use state "Sit" to restart game
            self.ResetNorthPanel()
            nTubeExclude.clear(self.key)
            nTubeClose.run(self.key, avatar=PtGetLocalAvatar(), state='closed')
            goBtnNResp.run(self.key, avatar=PtGetLocalAvatar(), state="dim")
        elif (state == ptClimbingWallMsgState.kNorthSit):
            goBtnNResp.run(self.key, avatar=PtGetLocalAvatar(), state="bright")
        elif (state == ptClimbingWallMsgState.kNorthSelect):
            self.ResetNorthPanel()
            i = 0
            while ((i < 20)):
                northCountLights.value[i].runAttachedResponder(kRedFlash)
                i = (i + 1)
            print 'enabled all n switches'
        elif (state == ptClimbingWallMsgState.kNorthReady):
            i = 0
            while ((i < BlockerCountLimit)):
                northCountLights.value[i].runAttachedResponder(kTeamLightsOff)
                i = (i + 1)
            i = BlockerCountLimit
            while ((i < 20)):
                northCountLights.value[i].runAttachedResponder(kRedOn)
                i = (i + 1)
            upButtonN.disable()
            dnButtonN.disable()
            readyButtonN.disable()
            fiveBtnN.disable()
            tenBtnN.disable()
            fifteenBtnN.disable()
            goBtnNResp.run(self.key, avatar=PtGetLocalAvatar(), state="pulse")
        elif (state == ptClimbingWallMsgState.kNorthPlayerEntry):
            self.EnableNorthButtons(false)
            goBtnNResp.run(self.key, avatar=PtGetLocalAvatar(), state="dim")
            if (SouthState == ptClimbingWallMsgState.kSouthPlayerEntry):
                sTubeOpen.run(self.key, avatar=PtGetLocalAvatar())
                nTubeOpen.run(self.key, avatar=PtGetLocalAvatar())
                print 'tubes open'
        elif ((state == ptClimbingWallMsgState.kNorthQuit) or ((state == ptClimbingWallMsgState.kNorthWin) or ((state == ptClimbingWallMsgState.kSouthQuit) or (state == ptClimbingWallMsgState.kSouthWin)))):
            nTubeExclude.clear(self.key)
            nTubeClose.run(self.key, avatar=PtGetLocalAvatar(), state='closed')
            goBtnNResp.run(self.key, avatar=PtGetLocalAvatar(), state="bright")


    def ResetNorthPanel(self):
        '''Reset responders and values when restarting game'''
        # modified: this is now used to reset Wall between two games. OnServerInitComplete will now call self.InitPanels()
        global NorthCount
        global BlockerCountLimit
        self.EnableNorthButtons(true)
        """ No longer needed: this is already in ClearIndices
        i = 0
        while ((i < 171)):
            # reset drawed blocker
            northLights.value[i].runAttachedResponder(kTeamLightsOff)
            if (i < 20):
                # reset counter
                northCountLights.value[i].runAttachedResponder(kTeamLightsOff)
            # disable wall blocker physics
            northWall.value[i].physics.suppress(true)
            i = (i + 1)"""
        self.ClearIndices(true)
        if (BlockerCountLimit > 0):
            self.ZeroBlockerCount()
        goBtnNResp.run(self.key, avatar=PtGetLocalAvatar(), state="dim")


    def ResetSouthPanel(self):
        '''Reset responders and values when restarting game'''
        # modified: this is now used to reset Wall between two games. OnServerInitComplete will now call self.InitPanels()
        global SouthCount
        global BlockerCountLimit
        self.EnableSouthButtons(true)
        """ No longer needed: this is already in ClearIndices
        i = 0
        while ((i < 171)):
            # reset drawed blocker
            #southLights.value[i].runAttachedResponder(kTeamLightsOff)
            if (i < 20):
                # reset counter
                southCountLights.value[i].runAttachedResponder(kTeamLightsOff)
            # disable wall blocker physics
            southWall.value[i].physics.suppress(true)
            i = (i + 1)"""
        self.ClearIndices(false)
        if (BlockerCountLimit > 0):
            self.ZeroBlockerCount()
        goBtnSResp.run(self.key, avatar=PtGetLocalAvatar(), state="dim")


    def ClearIndices(self, north):
        '''Clear set blockers, and run "off" layer anim'''
        global NorthWall
        global SouthWall
        global NorthCount
        global SouthCount
        i = 0
        while ((i < 171)):
            if (i < 20):
                # clear set blocker
                if north:
                    NorthWall[i] = -1
                else:
                    SouthWall[i] = -1
            # run all the layer anims on the panel
            if north:
                northLights.value[i].runAttachedResponder(kTeamLightsOff)
                northWall.value[i].physics.suppress(true) # fix bug reported by D'Lanor
            else:
                southLights.value[i].runAttachedResponder(kTeamLightsOff)
                southWall.value[i].physics.suppress(true) # fix bug reported by D'Lanor
            i = (i + 1)
        if north:
            NorthCount = 0
        else:
            SouthCount = 0


    def EnableSouthButtons(self, enable):
        '''Enable or not the south buttons physics'''
        i = 0
        while ((i < 171)):
            if enable:
                southPanel.value[i].physics.suppress(false)
            else:
                southPanel.value[i].physics.suppress(true)
            i = (i + 1)
        if enable:
            upButtonS.enable()
            dnButtonS.enable()
            readyButtonS.enable()
            fiveBtnS.enable()
            tenBtnS.enable()
            fifteenBtnS.enable()
        else:
            upButtonS.disable()
            dnButtonS.disable()
            readyButtonS.disable()
            fiveBtnS.disable()
            tenBtnS.disable()
            fifteenBtnS.disable()


    def EnableNorthButtons(self, enable):
        '''Enable or not the north buttons physics'''
        i = 0
        while ((i < 171)):
            if enable:
                northPanel.value[i].physics.suppress(false)
            else:
                northPanel.value[i].physics.suppress(true)
            i = (i + 1)
        if enable:
            upButtonN.enable()
            dnButtonN.enable()
            readyButtonN.enable()
            fiveBtnN.enable()
            tenBtnN.enable()
            fifteenBtnN.enable()
        else:
            upButtonN.disable()
            dnButtonN.disable()
            readyButtonN.disable()
            fiveBtnN.disable()
            tenBtnN.disable()
            fifteenBtnN.disable()


    def InitPanels(self):
        '''Set panels on server init complete'''
        self.EnableNorthButtons(false)
        self.EnableSouthButtons(false)
        # doesn't make any diference
#        i = 0
#        while ((i < 171)):
#            # reset blocker
#            northLights.value[i].fastForwardAttachedResponder(kTeamLightsOff)
#            southLights.value[i].fastForwardAttachedResponder(kTeamLightsOff)
#            if (i < 20):
#                # reset light
#                northCountLights.value[i].fastForwardAttachedResponder(kTeamLightsOff)
#                southCountLights.value[i].fastForwardAttachedResponder(kTeamLightsOff)
#            i = (i + 1)
        goBtnNResp.run(self.key, avatar=PtGetLocalAvatar(), state="dim", fastforward=1)
        goBtnSResp.run(self.key, avatar=PtGetLocalAvatar(), state="dim", fastforward=1)


    def LookupIndex(self, index, north):
        '''Returns whether blocker is on or not'''
        global BlockerCountLimit
        global NorthWall
        global SouthWall
        i = 0
        print 'looking north ',
        print north
        if north:
            while ((i < BlockerCountLimit)):
                if (NorthWall[i] == index):
                    print 'index found in north list in slot ',
                    print i
                    return true
                print 'north wall [',
                print i,
                print '] = ',
                print NorthWall[i]
                i = (i + 1)
        else:
            while ((i < BlockerCountLimit)):
                if (SouthWall[i] == index):
                    print 'index found in south list in slot ',
                    print i
                    return true
                print 'south wall [',
                print i,
                print '] = ',
                print SouthWall[i]
                i = (i + 1)
        print 'index not found'
        return false


    def SetWallIndex(self, index, value, north):
        '''Raise or not one of the blockers'''
        global NorthWall
        global NorthCount
        global SouthWall
        global SouthCount
        i = 0
        if value:
            if north:
                while ((NorthWall[i] >= 0)):
                    i = (i + 1)
                    if (i == 20):
                        print 'yikes - somehow overran the array!'
                        return
                NorthWall[i] = index
                NorthCount = (NorthCount + 1)
                print 'set north wall index ',
                print index,
                print ' in slot ',
                print i,
                print ' to true'
            else:
                while ((SouthWall[i] >= 0)):
                    i = (i + 1)
                    if (i == 20):
                        print 'yikes - somehow overran the array!'
                        return
                SouthWall[i] = index
                SouthCount = (SouthCount + 1)
                print 'set south wall index ',
                print index,
                print ' in slot ',
                print i,
                print ' to true'
        elif north:
            while ((NorthWall[i] != index)):
                i = (i + 1)
                if (i == 20):
                    print 'this should not get hit - looked for non-existent NorthWall entry!'
                    return
            NorthWall[i] = -1
            NorthCount = (NorthCount - 1)
            print 'removed index ',
            print index,
            print ' from list slot ',
            print i
        else:
            while ((SouthWall[i] != index)):
                i = (i + 1)
                if (i == 20):
                    print 'this should not get hit - looked for non-existent SouthWall entry!'
                    return
            SouthWall[i] = -1
            SouthCount = (SouthCount - 1)
            print 'removed index ',
            print index,
            print ' from list slot ',
            print i


    def ChangeSouthBlocker(self, index):
        '''Sets the south blocker index the inverse of its current state'''
        global SouthCount
        print 'found South index ',
        print index
        wallPicked = southWall.value[index]
        animPicked = southLights.value[index]
        if self.LookupIndex(index, false):
            wallPicked.physics.suppress(false)
            animPicked.runAttachedResponder(kTeamLightsOn)
            counterPicked = southCountLights.value[(SouthCount - 1)]
            counterPicked.runAttachedResponder(kTeamLightsOn)
            sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='blockerOn')
        else:
            wallPicked.physics.suppress(true)
            animPicked.runAttachedResponder(kTeamLightsOff)
            counterPicked = southCountLights.value[SouthCount]
            counterPicked.runAttachedResponder(kTeamLightsOff)
            sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='blockerOff')
        return


    def ChangeNorthBlocker(self, index):
        '''Sets the north blocker index the inverse of its current state'''
        global NorthCount
        print 'found North index ',
        print index
        wallPicked = northWall.value[index]
        animPicked = northLights.value[index]
        if self.LookupIndex(index, true):
            wallPicked.physics.suppress(false)
            animPicked.runAttachedResponder(kTeamLightsOn)
            counterPicked = northCountLights.value[(NorthCount - 1)]
            counterPicked.runAttachedResponder(kTeamLightsOn)
            nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='blockerOn')
        else:
            wallPicked.physics.suppress(true)
            animPicked.runAttachedResponder(kTeamLightsOff)
            counterPicked = northCountLights.value[NorthCount]
            counterPicked.runAttachedResponder(kTeamLightsOff)
            nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='blockerOff')
        return


    def ChangeGameState(self, newState):
        '''Send new state to the game (should always be done by one client)'''
        print 'sending change game state message with state ',
        print newState
        msg = ptClimbingWallMsg(self.key)
        msg.init(ptClimbingWallMsgType.kNewState, newState, 0)
        msg.send()


    def ChangeBlockerCount(self, newCount):
        '''Send number of blockers to game'''
        print 'sending change blocker count message with new count ',
        print newCount
        msg = ptClimbingWallMsg(self.key)
        msg.init(ptClimbingWallMsgType.kSetBlockerNum, 1, newCount)
        msg.send()


    def ChangeBlockerState(self, on, index, north):
        '''Tell the game to remove or add blocker'''
        msg = ptClimbingWallMsg(self.key)
        if on:
            msg.init(ptClimbingWallMsgType.kAddBlocker, index, north)
        else:
            msg.init(ptClimbingWallMsgType.kRemoveBlocker, index, north)
        msg.send()


    def UpdateBlockerCountDisplay(self, flash):
        '''Sets the panels lights'''
        # modified: don't run TeamLightsOn or RedFlash if we need to run TeamLightsOff. Should be fine.
        global BlockerCountLimit
        if (flash):
            numSelected = BlockerCountLimit
            i = 0
            while ((i < numSelected)):
                northCountLights.value[i].runAttachedResponder(kTeamLightsOn)
                southCountLights.value[i].runAttachedResponder(kTeamLightsOn)
                i = (i + 1)
            i = numSelected # should be its value already
            while ((i < 20)):
                northCountLights.value[i].runAttachedResponder(kRedFlash)
                southCountLights.value[i].runAttachedResponder(kRedFlash)
                i = (i + 1)
        # don't run layer anim, SetNPanelMode and SetSPanelMode does that already.
        #else:
            #i = 0
            #while ((i < 20)):
                #northCountLights.value[i].runAttachedResponder(kTeamLightsOff)
                #southCountLights.value[i].runAttachedResponder(kTeamLightsOff)
                #i = (i + 1)


    def IAmMaster(self):
        '''Tells if we're the game master'''
        return self.sceneobject.isLocallyOwned()


    def ZeroBlockerCount(self):
        '''Reset max number of blockers'''
        msg = ptClimbingWallMsg(self.key)
        msg.init(ptClimbingWallMsgType.kSetBlockerNum, 0, 0)
        msg.send()


    def OnTimer(self, id):
        '''Run callback actions'''
        avatar = PtGetLocalAvatar()
        if (id == ptClimbingWallMsgState.kNorthQuit):
            PtFakeLinkAvatarToObject(avatar.getKey(), sTeamWinTeleport.value.getKey())
            self.ChangeGameState(ptClimbingWallMsgState.kNorthQuit)
            self.ChangeGameState(ptClimbingWallMsgState.kSouthWin)
        else:
            PtFakeLinkAvatarToObject(avatar.getKey(), nTeamWinTeleport.value.getKey())
            self.ChangeGameState(ptClimbingWallMsgState.kNorthWin)
            self.ChangeGameState(ptClimbingWallMsgState.kSouthQuit)


    def SetWearingMaintainerSuit(self, avatar):
        '''Sets the avatar wearing a maintainer's suit, if that's not already the case'''
        currentgender = avatar.avatar.getAvatarClothingGroup()
        # get the gender of our avatar
        if (currentgender == kFemaleClothingGroup):
            clothing = FemaleSuit
        else:
            clothing = MaleSuit

        if (not (self.IItemInCloset(avatar, clothing[0]))):
            # we don't have the suit in our Relto, so let's add it.
            avatar.avatar.addWardrobeClothingItem(clothing[0], ptColor().white(), ptColor().white())
            print "grsnWallPython: added the suit to your wardrobe"

        # check the clothing our avatar is wearing
        worn = avatar.avatar.getAvatarClothingList()
        for item in worn:
            name = item[0]
            if (name in clothing):
                print "Avatar seems to be wearing the suit already."
                return

        # give the avatar his suit.
        PtWearMaintainerSuit(avatar.getKey(), true)
        print "grsnWallPython: avatar is now wearing suit."


    def IItemInCloset(self, avatar, clothingName):
        '''Returns whether the avatar already owns an item'''
        clothingList = avatar.avatar.getWardrobeClothingList()
        for item in clothingList:
            if (clothingName == item[0]):
                return 1
        return 0


    def OnNotify(self, state, id, events):
        '''Manages notifies from objects and responders'''
        global SouthState
        global NorthState
        global BlockerCountLimit
        global SouthCount
        global NorthCount
        #ageSDL = PtGetAgeSDL()
        avatar = PtFindAvatar(events)
        southState = SouthState
        northState = NorthState
        print 'southState = ',
        print southState
        print 'northState = ',
        print northState
        if (id == sQuitBehavior.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    print 'start touching quit jewel, warp out'
                    if (avatar == PtGetLocalAvatar()):
                        PtAtTimeCallback(self.key, 0.80000000000000004, ptClimbingWallMsgState.kSouthQuit)
                    return
        if (id == nQuitBehavior.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    print 'start touching quit jewel, warp out'
                    if (avatar == PtGetLocalAvatar()):
                        PtAtTimeCallback(self.key, 0.80000000000000004, ptClimbingWallMsgState.kNorthQuit)
                    return
        if (id == nTubeOpen.id):
            print 'tube finished opening'
            nTubeExclude.release(self.key)
            nTubeEntry.enable()
        if (id == nTubeMulti.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    print 'Smart seek completed. close tube'
                    nTubeExclude.clear(self.key)
                    nTubeClose.run(self.key, avatar=avatar, state='down')
                elif ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                    print 'multistage complete, warp to wall south room with suit'
                    if (avatar == PtGetLocalAvatar()):
                        self.SetWearingMaintainerSuit(avatar)
                        PtSendKIMessage(kDisableEntireYeeshaBook, 0)
                    avatar.physics.warpObj(nTeamWarpPt.value.getKey())
                    nTubeOpen.run(self.key, avatar=avatar)
        if (id == sTubeOpen.id):
            print 'tube finished opening'
            sTubeExclude.release(self.key)
            sTubeEntry.enable()
        if (id == sTubeMulti.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    print 'Smart seek completed. close tube'
                    sTubeExclude.clear(self.key)
                    sTubeClose.run(self.key, avatar=avatar, state='down')
                elif ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                    print 'multistage complete, warp to wall north room with suit'
                    if (avatar == PtGetLocalAvatar()):
                        self.SetWearingMaintainerSuit(avatar)
                        PtSendKIMessage(kDisableEntireYeeshaBook, 0)
                    avatar.physics.warpObj(sTeamWarpPt.value.getKey())
                    sTubeOpen.run(self.key, avatar=avatar)
        if ((id == sTeamWin.id) and state):
            if (avatar == PtGetLocalAvatar()):
                print 'you win'
                PtFakeLinkAvatarToObject(avatar.getKey(), sTeamWinTeleport.value.getKey())
                self.ChangeGameState(ptClimbingWallMsgState.kSouthWin)
                self.ChangeGameState(ptClimbingWallMsgState.kNorthQuit)
        if ((id == nTeamWin.id) and state):
            if (avatar == PtGetLocalAvatar()):
                print 'you win'
                PtFakeLinkAvatarToObject(avatar.getKey(), nTeamWinTeleport.value.getKey())
                self.ChangeGameState(ptClimbingWallMsgState.kNorthWin)
                self.ChangeGameState(ptClimbingWallMsgState.kSouthQuit)
        if ((id == nTeamQuit.id) and state):
            avatar.avatar.runBehaviorSetNotify(nQuitBehavior.value, self.key, nQuitBehavior.netForce)
            return
        if ((id == sTeamQuit.id) and state):
            avatar.avatar.runBehaviorSetNotify(sQuitBehavior.value, self.key, sQuitBehavior.netForce)
            return
        if (id == southChair.id):
            print 'clicked south chair'
            #avID = PtGetClientIDFromAvatarKey(avatar.getKey())
            if (avatar == PtGetLocalAvatar()):
                if state:
                    #occupant = ageSDL['sChairOccupant'][0]
                    #print 'occupant ',
                    #print occupant
                    #if (occupant == -1):# from CC: should make sure we don't try to sit on an occupied chair. (should not happen anyway as its physics are disabled, but OK)
                    print 'sitting down in south chair'
                    southChair.disable()
                    PtDisableForwardMovement()
                    #ageSDL.setIndex('sChairOccupant', 0, avID)
                    if ((southState == ptClimbingWallMsgState.kWaiting) or ((southState == ptClimbingWallMsgState.kSouthWin) or (southState == ptClimbingWallMsgState.kSouthQuit))):
                        self.ChangeGameState(ptClimbingWallMsgState.kSouthSit)
                    return
        if (id == sChairSit.id):
            for event in events:
                if ((event[0] == 6) and ((event[1] == 1) and (state == 0))):
                    #if (ageSDL['sChairOccupant'][0] != -1): # from CC -> OK
                    print 'standing up from south chair'
                    southChair.enable()
                    PtEnableForwardMovement()
                    #    ageSDL.setIndex('sChairOccupant', 0, -1)
                    return
        if (id == northChair.id):
            print 'clicked north chair'
            #avID = PtGetClientIDFromAvatarKey(avatar.getKey())
            if (avatar == PtGetLocalAvatar()):
                if state:
                #occupant = ageSDL['nChairOccupant'][0]
                #print 'occupant ',
                #print occupant
                #if (occupant == -1):# from CC
                    print 'sitting down in north chair'
                    northChair.disable()
                    PtDisableForwardMovement()
                    #ageSDL.setIndex('nChairOccupant', 0, avID)
                    if ((northState == ptClimbingWallMsgState.kWaiting) or ((northState == ptClimbingWallMsgState.kNorthWin) or (northState == ptClimbingWallMsgState.kNorthQuit))):
                        self.ChangeGameState(ptClimbingWallMsgState.kNorthSit)
                    return
        if (id == nChairSit.id):
            for event in events:
                if ((event[0] == 6) and ((event[1] == 1) and (state == 0))):
                #if (ageSDL['nChairOccupant'][0] != -1): # from CC
                    print 'standing up from north chair'
                    northChair.enable()
                    PtEnableForwardMovement()
                    #ageSDL.setIndex('nChairOccupant', 0, -1)
                return
        elif (not (state)):
            return
        if (id == nTubeEntry.id):
            #trigger = PtFindAvatar(events)
            print 'entered team 1 tube, run behavior'
            #ageSDL.setIndex('nWallPlayer', 0, PtGetClientIDFromAvatarKey(trigger.getKey()))
            nTubeEntry.disable()
            avatar.avatar.runBehaviorSetNotify(nTubeMulti.value, self.key, 0)
        if (id == sTubeEntry.id):
            #trigger = PtFindAvatar(events)
            print 'entered team 2 tube, run behavior'
            #ageSDL.setIndex('sWallPlayer', 0, PtGetClientIDFromAvatarKey(trigger.getKey()))
            sTubeEntry.disable()
            avatar.avatar.runBehaviorSetNotify(sTubeMulti.value, self.key, 0)
        if (avatar != PtGetLocalAvatar()):
            print 'not activated by me'
            return
        if (id == upButtonS.id):
            print 'up button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                print 'correct state, blocker count limit ',
                print BlockerCountLimit
                if (BlockerCountLimit < 20):
                    self.ChangeBlockerCount((BlockerCountLimit + 1))
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                    return
                else:
                    print 'somehow think blocker count limit greater than 20?'
            sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == dnButtonS.id):
            print 'down button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                if (BlockerCountLimit > 0):
                    self.ChangeBlockerCount((BlockerCountLimit - 1))
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='down')
                    return
            sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == fiveBtnS.id):
            print 'five button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                self.ChangeBlockerCount(5)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                return
            sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == tenBtnS.id):
            print 'ten button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                self.ChangeBlockerCount(10)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                return
            sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == fifteenBtnS.id):
            print 'fifteen button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                self.ChangeBlockerCount(15)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                return
            sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == readyButtonS.id):
            print 'ready button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                self.ChangeGameState(ptClimbingWallMsgState.kSouthReady)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='select')
                if (northState == ptClimbingWallMsgState.kNorthSelect):
                    self.ChangeGameState(ptClimbingWallMsgState.kNorthReady)
                    nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='select') # also disable looping sounds for other panel
            else:
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == goButtonS.id):
            print 'picked s go button'
            if (southState == ptClimbingWallMsgState.kSouthSit):
                print 'set index to kSouthSelect'
                self.ChangeGameState(ptClimbingWallMsgState.kSouthSelect)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='main')
                if ((northState == ptClimbingWallMsgState.kWaiting) or ((northState == ptClimbingWallMsgState.kNorthSit) or ((northState == ptClimbingWallMsgState.kNorthWin) or (northState == ptClimbingWallMsgState.kNorthQuit)))):
                    print 'force north chair to keep up'
                    self.ChangeGameState(ptClimbingWallMsgState.kNorthSelect)
                    nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='main')
            elif (southState == ptClimbingWallMsgState.kSouthReady):
                print 'check to see if you\'ve used all your wall blockers'
                numSelected = SouthCount
                maxSelections = BlockerCountLimit
                if (numSelected < maxSelections):
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
                else:
                    self.ChangeGameState(ptClimbingWallMsgState.kSouthPlayerEntry)
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='gameStart')
            else:
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        if (id == upButtonN.id):
            print 'up button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                if (BlockerCountLimit < 20):
                    self.ChangeBlockerCount(BlockerCountLimit + 1)
                    nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                    return
            nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == dnButtonN.id):
            print 'down button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                if (BlockerCountLimit > 0):
                    self.ChangeBlockerCount(BlockerCountLimit - 1)
                    nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='down')
                    return
            nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == fiveBtnN.id):
            print 'five button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                self.ChangeBlockerCount(5)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                return
            nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == tenBtnN.id):
            print 'ten button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                self.ChangeBlockerCount(10)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                return
            nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == fifteenBtnN.id):
            print 'fifteen button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                self.ChangeBlockerCount(15)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                return
            nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == readyButtonN.id):
            print 'ready button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                self.ChangeGameState(ptClimbingWallMsgState.kNorthReady)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='select')
                if (southState == ptClimbingWallMsgState.kSouthSelect):
                    self.ChangeGameState(ptClimbingWallMsgState.kSouthReady)
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='select') # also disable looping sounds for other panel
                    print 'force south chair to keep up'
            else:
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == goButtonN.id):
            print 'picked n go button'
            if (northState == ptClimbingWallMsgState.kNorthSit):
                print 'set index to kNorthSelect'
                self.ChangeGameState(ptClimbingWallMsgState.kNorthSelect)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='main')
                if ((southState == ptClimbingWallMsgState.kWaiting) or ((southState == ptClimbingWallMsgState.kSouthSit) or ((southState == ptClimbingWallMsgState.kSouthWin) or (southState == ptClimbingWallMsgState.kSouthQuit)))): # corrected: this test used two times kSouthWin, and never kSouthQuit.... mauvais perdant !
                    self.ChangeGameState(ptClimbingWallMsgState.kSouthSelect)
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='main')
                    print 'force south chair to keep up'
            elif (northState == ptClimbingWallMsgState.kNorthReady):
                print 'check to see if you\'ve used all your wall blockers'
                numSelected = NorthCount
                maxSelections = BlockerCountLimit
                if (numSelected < maxSelections):
                    nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
                else:
                    self.ChangeGameState(ptClimbingWallMsgState.kNorthPlayerEntry)
                    nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='gameStart')
            else:
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        for event in events:
            if ((event[0] == kPickedEvent) and (event[1] == 1)):
                panelPicked = event[3]
                objName = panelPicked.getName()
                print 'player picked blocker named ',
                print objName
                north = 0
                try:
                    index = northPanel.value.index(panelPicked)
                    north = 1
                except:
                    try:
                        index = southPanel.value.index(panelPicked)
                    except:
                        print 'no wall blocker found'
                        return
                if north:
                    if (northState != ptClimbingWallMsgState.kNorthReady):
                        print 'no blocker picking for you!'
                        nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
                        return
                    numSelected = NorthCount
                    print 'numSelected = ',
                    print numSelected
                    maxSelections = BlockerCountLimit
                    if (self.LookupIndex(index, true) == 0):
                        if (numSelected == maxSelections):
                            print 'you\'ve picked all you can'
                            nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
                            return
                        self.ChangeBlockerState(true, index, true)
                    else:
                        numSelected = (numSelected - 1)
                        if (numSelected == -1):
                            print 'what?!?'
                            return
                        self.ChangeBlockerState(false, index, true)
                else:
                    if (southState != ptClimbingWallMsgState.kSouthReady):
                        print 'no blocker picking for you!'
                        sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
                        return
                    numSelected = SouthCount
                    print 'numSelected = ',
                    print numSelected
                    maxSelections = BlockerCountLimit
                    if (self.LookupIndex(index, false) == 0):
                        if (numSelected == maxSelections):
                            print 'you\'ve picked all you can'
                            sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
                            return
                        self.ChangeBlockerState(true, index, false)
                    else:
                        numSelected = (numSelected - 1)
                        if (numSelected == -1):
                            print 'what?!?'
                            return
                        self.ChangeBlockerState(false, index, false)


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


def glue_getParamDict():
    global glue_params
    global glue_paramKeys
    if (type(glue_params) == type(None)):
        glue_params = {}
        gd = globals()
        for obj in gd.values():
            if isinstance(obj, ptAttribute):
                if glue_params.has_key(obj.id):
                    if glue_verbose:
                        print 'WARNING: Duplicate attribute ids!'
                        print ('%s has id %d which is already defined in %s' % (obj.name, obj.id, glue_params[obj.id].name))
                else:
                    glue_params[obj.id] = obj
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



