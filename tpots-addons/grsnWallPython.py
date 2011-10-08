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
northPanelClick = ptAttribActivator(1, 'North Panel Clickables')
southPanelClick = ptAttribActivator(2, 'South Panel Clickables')
northPanel = ptAttribSceneobjectList(3, 'North Panel Objects', byObject=1)
southPanel = ptAttribSceneobjectList(4, 'South Panel Objects', byObject=1)
northWall = ptAttribSceneobjectList(5, 'North Wall', byObject=1)
southWall = ptAttribSceneobjectList(6, 'South Wall', byObject=1)
northChair = ptAttribActivator(7, 'North Chair')
southChair = ptAttribActivator(8, 'South Chair')
northLights = ptAttribSceneobjectList(9, 'North Panel Lights', byObject=1)
southLights = ptAttribSceneobjectList(10, 'South Panel Lights', byObject=1)
northCountLights = ptAttribSceneobjectList(11, 'North Count Lights', byObject=1)
southCountLights = ptAttribSceneobjectList(12, 'South Count Lights', byObject=1)
upButtonS = ptAttribActivator(13, 'S up count button')
dnButtonS = ptAttribActivator(14, 'S down count button')
readyButtonS = ptAttribActivator(15, 'S ready button')
upButtonN = ptAttribActivator(18, 'N up count button')
dnButtonN = ptAttribActivator(19, 'N down count button')
readyButtonN = ptAttribActivator(20, 'N ready button')
goButtonN = ptAttribActivator(21, 'N Go Button activator')
goButtonS = ptAttribActivator(22, 'S Go Button activator')
goBtnNObject = ptAttribSceneobject(23, 'N Go Button object')
goBtnSObject = ptAttribSceneobject(24, 'S Go Button object')
nChairSit = ptAttribActivator(25, 'N sit component')
sChairSit = ptAttribActivator(26, 'S sit component')
fiveBtnN = ptAttribActivator(27, '5 btn N')
tenBtnN = ptAttribActivator(28, '10 btn N')
fifteenBtnN = ptAttribActivator(29, '15 btn N')
fiveBtnS = ptAttribActivator(30, '5 btn S')
tenBtnS = ptAttribActivator(31, '10 btn S')
fifteenBtnS = ptAttribActivator(32, '15 btn S')
sTubeOpen = ptAttribNamedResponder(33, 'S tube open', netForce=1)
nTubeOpen = ptAttribNamedResponder(34, 'N tube open', netForce=1)
sTubeClose = ptAttribNamedResponder(35, 'S tube close', netForce=1)
nTubeClose = ptAttribNamedResponder(36, 'N tube close', netForce=1)
sTubeEntry = ptAttribNamedActivator(37, 'S tube entry trigger')
nTubeEntry = ptAttribNamedActivator(38, 'N tube entry trigger')
sTubeMulti = ptAttribBehavior(43, 's tube entry multi', netForce=0)
nTubeMulti = ptAttribBehavior(44, 'n tube entry multi', netForce=0)
sTubeExclude = ptAttribExcludeRegion(45, 's tube exclude')
nTubeExclude = ptAttribExcludeRegion(46, 'n tube exclude')
sTeamWarpPt = ptAttribSceneobject(47, 's team warp point')
nTeamWarpPt = ptAttribSceneobject(48, 'n team warp point')
sTeamWin = ptAttribActivator(49, 's team win')
nTeamWin = ptAttribActivator(50, 'n team win')
sTeamQuit = ptAttribActivator(51, 's team quit')
nTeamQuit = ptAttribActivator(52, 'n team quit')
sTeamWinTeleport = ptAttribSceneobject(53, 's team win point')
nTeamWinTeleport = ptAttribSceneobject(54, 'n team win point')
nQuitBehavior = ptAttribBehavior(55, 's quit behavior')
sQuitBehavior = ptAttribBehavior(56, 'n quit behavior')
nPanelSound = ptAttribResponder(57, 'n panel sound', ['main', 'up', 'down', 'select', 'blockerOn', 'blockerOff', 'gameStart', 'denied'], netForce=1)
sPanelSound = ptAttribResponder(58, 's panel sound', ['main', 'up', 'down', 'select', 'blockerOn', 'blockerOff', 'gameStart', 'denied'], netForce=1)
kTeamLightsOn = 0
kTeamLightsOff = 1
kRedOn = 3
kRedOff = 4
kRedFlash = 2
kDim = 0
kBright = 1
kPulse = 2
kWaiting = 0
kNorthSit = 1
kSouthSit = 2
kNorthSelect = 3
kSouthSelect = 4
kNorthReady = 5
kSouthReady = 6
kNorthPlayerEntry = 7
kSouthPlayerEntry = 8
kGameInProgress = 9
kNorthWin = 10
kSouthWin = 11
kSouthQuit = 12
kNorthQuit = 13
SouthState = ptClimbingWallMsgState.kWaiting
NorthState = ptClimbingWallMsgState.kWaiting
NorthCount = 0
BlockerCountLimit = 0
SouthCount = 0
NorthWall = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
SouthWall = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
ReceiveInit = false

class grsnWallPython(ptResponder):


    def __init__(self):
        PtDebugPrint('grsnWallPython::init begin')
        ptResponder.__init__(self)
        self.id = 52392
        self.version = 3


    def Load(self):
        PtDebugPrint('grsnWallPython::Load')


    def LookupIndex(self, index, north):
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


    def ClearIndices(self, north):
        global NorthWall
        global SouthWall
        global NorthCount
        global SouthCount
        i = 0
        while ((i < 171)):
            if (i < 20):
                if north:
                    NorthWall[i] = -1
                else:
                    SouthWall[i] = -1
            if north:
                northLights.value[i].runAttachedResponder(kTeamLightsOff)
            else:
                southLights.value[i].runAttachedResponder(kTeamLightsOff)
            i = (i + 1)
        if north:
            NorthCount = 0
        else:
            SouthCount = 0


    def SetSPanelMode(self, state):
        global BlockerCountLimit
        global NorthState
        if (state == ptClimbingWallMsgState.kWaiting):
            self.ResetSouthPanel(false)
            self.ClearIndices(false)
            sTubeExclude.clear(self.key)
            sTubeClose.run(self.key, avatar=PtGetLocalAvatar())
        elif (state == ptClimbingWallMsgState.kSouthSit):
            goBtnSObject.value.runAttachedResponder(kBright)
        elif (state == ptClimbingWallMsgState.kSouthSelect):
            self.ClearIndices(false)
            i = 0
            while ((i < 20)):
                southCountLights.value[i].runAttachedResponder(kRedFlash)
                i = (i + 1)
            upButtonS.enable()
            dnButtonS.enable()
            readyButtonS.enable()
            fiveBtnS.enable()
            tenBtnS.enable()
            fifteenBtnS.enable()
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
        elif (state == ptClimbingWallMsgState.kSouthPlayerEntry):
            self.EnableSouthButtons(false)
            if (NorthState == ptClimbingWallMsgState.kNorthPlayerEntry):
                sTubeOpen.run(self.key, avatar=PtGetLocalAvatar())
                goBtnSObject.value.runAttachedResponder(kBright)
                nTubeOpen.run(self.key, avatar=PtGetLocalAvatar())
                goBtnNObject.value.runAttachedResponder(kBright)
                print 'tubes open'


    def SetNPanelMode(self, state):
        global BlockerCountLimit
        global SouthState
        print 'set N Panel Mode called with state ',
        print state
        if (state == ptClimbingWallMsgState.kWaiting):
            self.ResetNorthPanel(false)
            self.ClearIndices(true)
            nTubeExclude.clear(self.key)
            nTubeClose.run(self.key, avatar=PtGetLocalAvatar())
            goBtnNObject.value.runAttachedResponder(kDim)
        elif (state == ptClimbingWallMsgState.kNorthSit):
            goBtnNObject.value.runAttachedResponder(kBright)
        elif (state == ptClimbingWallMsgState.kNorthSelect):
            self.ClearIndices(true)
            i = 0
            while ((i < 20)):
                northCountLights.value[i].runAttachedResponder(kRedFlash)
                print 'run red flash ',
                print i
                i = (i + 1)
            upButtonN.enable()
            dnButtonN.enable()
            readyButtonN.enable()
            fiveBtnN.enable()
            tenBtnN.enable()
            fifteenBtnN.enable()
            goBtnNObject.value.runAttachedResponder(kDim)
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
            goBtnNObject.value.runAttachedResponder(kRedFlash)
        elif (state == ptClimbingWallMsgState.kNorthPlayerEntry):
            self.EnableNorthButtons(false)
            if (SouthState == ptClimbingWallMsgState.kSouthPlayerEntry):
                sTubeOpen.run(self.key, avatar=PtGetLocalAvatar())
                goBtnSObject.value.runAttachedResponder(kBright)
                nTubeOpen.run(self.key, avatar=PtGetLocalAvatar())
                goBtnNObject.value.runAttachedResponder(kBright)
                print 'tubes open'


    def IAmMaster(self):
        return self.sceneobject.isLocallyOwned()


    def ChangeGameState(self, newState):
        print 'sending change game state message with state ',
        print newState
        msg = ptClimbingWallMsg(self.key)
        msg.init(ptClimbingWallMsgType.kNewState, newState, 0)
        msg.send()


    def ChangeBlockerCount(self, newCount):
        print 'sending change blocker count message with new count ',
        print newCount
        msg = ptClimbingWallMsg(self.key)
        msg.init(ptClimbingWallMsgType.kSetBlockerNum, 1, newCount)
        msg.send()


    def ZeroBlockerCount(self):
        msg = ptClimbingWallMsg(self.key)
        msg.init(ptClimbingWallMsgType.kSetBlockerNum, 0, 0)
        msg.send()


    def ChangeBlockerState(self, on, index, north):
        msg = ptClimbingWallMsg(self.key)
        if on:
            msg.init(ptClimbingWallMsgType.kAddBlocker, index, north)
        else:
            msg.init(ptClimbingWallMsgType.kRemoveBlocker, index, north)
        msg.send()


    def OnClimbingWallInit(self, type, state, value):
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
        if (ReceiveInit == false):
            print 'failed to receive init'
            return
        if (type == ptClimbingWallMsgType.kEndGameState):
            ReceiveInit = false
            print 'finished receiving total game state'
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
        elif ((type == ptClimbingWallMsgType.kAddBlocker) and (state > 0)):
            self.SetWallIndex(state, true, value)
            if value:
                self.ChangeNorthBlocker(state)
            else:
                self.ChangeSouthBlocker(state)
        elif (type == ptClimbingWallMsgType.kSetBlockerNum):
            BlockerCountLimit = value
            self.UpdateBlockerCountDisplay(state)


    def OnClimbingWallEvent(self, type, state, value):
        global ReceiveInit
        global NorthState
        global SouthState
        global BlockerCountLimit
        global NorthWall
        global SouthWall
        if ReceiveInit:
            return
        print 'grsnClimbingWall::OnClimbingWallMsg type ',
        print type,
        print ' state ',
        print state,
        print ' value ',
        print value
        if (type == ptClimbingWallMsgType.kNewState):
            if (value == 1):
                NorthState = state
                self.SetNPanelMode(state)
            else:
                SouthState = state
                self.SetSPanelMode(state)
        elif (type == ptClimbingWallMsgType.kAddBlocker):
            self.SetWallIndex(state, true, value)
            if value:
                self.ChangeNorthBlocker(state)
            else:
                self.ChangeSouthBlocker(state)
        elif (type == ptClimbingWallMsgType.kRemoveBlocker):
            self.SetWallIndex(state, false, value)
            if value:
                self.ChangeNorthBlocker(state)
            else:
                self.ChangeSouthBlocker(state)
        elif (type == ptClimbingWallMsgType.kSetBlockerNum):
            BlockerCountLimit = value
            self.UpdateBlockerCountDisplay(state)
        elif (type == ptClimbingWallMsgType.kRequestGameState):
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


    def OnServerInitComplete(self):
        global ReceiveInit
        PtDebugPrint('grsnWallPython::OnServerInitComplete')
        solo = true
        if len(PtGetPlayerList()):
            solo = false
            ReceiveInit = true
            i = 0
            while ((i < 171)):
                southWall.value[i].physics.suppress(true)
                northWall.value[i].physics.suppress(true)
                i = (i + 1)
            sTubeClose.run(self.key, fastforward=true, netForce=0)
            nTubeClose.run(self.key, fastforward=true, netForce=0)
            print 'requesting game state message from master client'
            msg = ptClimbingWallMsg(self.key)
            msg.init(ptClimbingWallMsgType.kRequestGameState, 0, 0)
            msg.send()
            return
        else:
            print 'solo in climbing wall'
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags('nChairOccupant', 0, 1)
        ageSDL.setFlags('sChairOccupant', 0, 1)
        ageSDL.setNotify(self.key, 'nChairOccupant', 0.0)
        ageSDL.setNotify(self.key, 'sChairOccupant', 0.0)
        ageSDL.sendToClients('nChairOccupant')
        ageSDL.sendToClients('sChairOccupant')
        self.ResetSouthPanel(false)
        self.ResetNorthPanel(false)
        sTubeClose.run(self.key)
        nTubeClose.run(self.key)
        if solo:
            ageSDL.setIndex('nChairOccupant', 0, -1)
            ageSDL.setIndex('sChairOccupant', 0, -1)
            ageSDL.setIndex('nWallPlayer', 0, -1)
            ageSDL.setIndex('sWallPlayer', 0, -1)
            SouthState = ptClimbingWallMsgState.kWaiting
            NorthState = ptClimbingWallMsgState.kWaiting


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        return


    def UpdateBlockerCountDisplay(self, flash):
        global BlockerCountLimit
        numSelected = BlockerCountLimit
        i = 0
        while ((i < numSelected)):
            northCountLights.value[i].runAttachedResponder(kTeamLightsOn)
            southCountLights.value[i].runAttachedResponder(kTeamLightsOn)
            i = (i + 1)
        i = numSelected
        while ((i < 20)):
            northCountLights.value[i].runAttachedResponder(kRedFlash)
            southCountLights.value[i].runAttachedResponder(kRedFlash)
            i = (i + 1)
        if (flash == 0):
            i = 0
            while ((i < 20)):
                northCountLights.value[i].runAttachedResponder(kTeamLightsOff)
                southCountLights.value[i].runAttachedResponder(kTeamLightsOff)
                i = (i + 1)


    def ChangeSouthBlocker(self, index):
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


    def EnableSouthButtons(self, enable):
        i = 0
        while ((i < 171)):
            if enable:
                southPanel.value[i].physics.enable()
            else:
                southPanel.value[i].physics.disable()
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
        i = 0
        while ((i < 171)):
            if enable:
                northPanel.value[i].physics.enable()
            else:
                northPanel.value[i].physics.disable()
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


    def ResetSouthPanel(self, enable):
        global SouthCount
        self.EnableSouthButtons(enable)
        ageSDL = PtGetAgeSDL()
        i = 0
        while ((i < 171)):
            southLights.value[i].runAttachedResponder(kTeamLightsOff)
            if (i < 20):
                southCountLights.value[i].runAttachedResponder(kTeamLightsOff)
            if (enable == 0):
                southWall.value[i].physics.suppress(true)
            i = (i + 1)
        self.ZeroBlockerCount()
        SouthCount = 0
        goBtnSObject.value.runAttachedResponder(kDim)


    def ResetNorthPanel(self, enable):
        global NorthCount
        self.EnableNorthButtons(enable)
        ageSDL = PtGetAgeSDL()
        i = 0
        while ((i < 171)):
            northLights.value[i].runAttachedResponder(kTeamLightsOff)
            if (i < 20):
                northCountLights.value[i].runAttachedResponder(kTeamLightsOff)
            if enable:
                print 'enabled north wall - this should not happen  '
            else:
                northWall.value[i].physics.suppress(true)
            i = (i + 1)
        self.ZeroBlockerCount()
        NorthCount = 0
        goBtnNObject.value.runAttachedResponder(kDim)


    def OnTimer(self, id):
        avatar = PtGetLocalAvatar()
        if (id == kNorthQuit):
            PtFakeLinkAvatarToObject(avatar.getKey(), sTeamWinTeleport.value.getKey())
            self.ChangeGameState(ptClimbingWallMsgState.kSouthQuit)
            self.ChangeGameState(ptClimbingWallMsgState.kNorthWin)
        else:
            PtFakeLinkAvatarToObject(avatar.getKey(), nTeamWinTeleport.value.getKey())
            self.ChangeGameState(ptClimbingWallMsgState.kSouthWin)
            self.ChangeGameState(ptClimbingWallMsgState.kNorthQuit)


    def OnNotify(self, state, id, events):
        global SouthState
        global NorthState
        global BlockerCountLimit
        global SouthCount
        global NorthCount
        ageSDL = PtGetAgeSDL()
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
                        PtAtTimeCallback(self.key, 0.80000000000000004, kSouthQuit)
                    return
        if (id == nQuitBehavior.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    print 'start touching quit jewel, warp out'
                    if (avatar == PtGetLocalAvatar()):
                        PtAtTimeCallback(self.key, 0.80000000000000004, kNorthQuit)
                    return
        if (id == nTubeOpen.id):
            print 'tube finished opening'
            nTubeExclude.release(self.key)
        if (id == nTubeMulti.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    print 'Smart seek completed. close tube'
                    nTubeClose.run(self.key, avatar=avatar)
                elif ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                    print 'multistage complete, warp to wall south room with suit'
                    if (avatar == PtGetLocalAvatar()):
                        PtWearMaintainerSuit(PtGetLocalAvatar().getKey(), true)
                        PtSendKIMessage(kDisableEntireYeeshaBook, 0)
                    avatar.physics.warpObj(sTeamWarpPt.value.getKey())
        if (id == sTubeOpen.id):
            print 'tube finished opening'
            sTubeExclude.release(self.key)
        if (id == sTubeMulti.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    print 'Smart seek completed. close tube'
                    sTubeClose.run(self.key, avatar=avatar)
                elif ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                    print 'multistage complete, warp to wall north room with suit'
                    if (avatar == PtGetLocalAvatar()):
                        PtWearMaintainerSuit(PtGetLocalAvatar().getKey(), true)
                        PtSendKIMessage(kDisableEntireYeeshaBook, 0)
                    avatar.physics.warpObj(nTeamWarpPt.value.getKey())
        if ((id == sTeamWin.id) and state):
            print 'you win'
            PtFakeLinkAvatarToObject(avatar.getKey(), sTeamWinTeleport.value.getKey())
            self.ChangeGameState(ptClimbingWallMsgState.kSouthWin)
            self.ChangeGameState(ptClimbingWallMsgState.kNorthQuit)
        if ((id == nTeamWin.id) and state):
            print 'you win'
            PtFakeLinkAvatarToObject(avatar.getKey(), nTeamWinTeleport.value.getKey())
            self.ChangeGameState(ptClimbingWallMsgState.kNorthWin)
            self.ChangeGameState(ptClimbingWallMsgState.kSouthQuit)
        if ((id == nTeamQuit.id) and state):
            avatar.avatar.runBehaviorSetNotify(nQuitBehavior.value, self.key, nQuitBehavior.netForce)
            self.ChangeGameState(ptClimbingWallMsgState.kNorthQuit)
            self.ChangeGameState(ptClimbingWallMsgState.kSouthWin)
            return
        if ((id == sTeamQuit.id) and state):
            avatar.avatar.runBehaviorSetNotify(sQuitBehavior.value, self.key, sQuitBehavior.netForce)
            self.ChangeGameState(ptClimbingWallMsgState.kNorthWin)
            self.ChangeGameState(ptClimbingWallMsgState.kSouthQuit)
            return
        if (id == southChair.id):
            print 'clicked south chair'
            avID = PtGetClientIDFromAvatarKey(avatar.getKey())
            if state:
                occupant = ageSDL['sChairOccupant'][0]
                print 'occupant ',
                print occupant
                if 1:
                    print 'sitting down in south chair'
                    southChair.disable()
                    ageSDL.setIndex('sChairOccupant', 0, avID)
                    if ((southState == ptClimbingWallMsgState.kWaiting) or ((southState == ptClimbingWallMsgState.kSouthWin) or (southState == ptClimbingWallMsgState.kSouthQuit))):
                        self.ChangeGameState(ptClimbingWallMsgState.kSouthSit)
                    return
        if (id == sChairSit.id):
            for event in events:
                if ((event[0] == 6) and ((event[1] == 1) and (state == 0))):
                    if 1:
                        print 'standing up from south chair'
                        southChair.enable()
                        ageSDL.setIndex('sChairOccupant', 0, -1)
                    return
        if (id == northChair.id):
            print 'clicked north chair'
            avID = PtGetClientIDFromAvatarKey(avatar.getKey())
            if state:
                occupant = ageSDL['nChairOccupant'][0]
                print 'occupant ',
                print occupant
                if 1:
                    print 'sitting down in south chair'
                    northChair.disable()
                    ageSDL.setIndex('nChairOccupant', 0, avID)
                    if ((northState == ptClimbingWallMsgState.kWaiting) or ((northState == ptClimbingWallMsgState.kNorthWin) or (northState == ptClimbingWallMsgState.kNorthQuit))):
                        self.ChangeGameState(ptClimbingWallMsgState.kNorthSit)
                    return
        if (id == nChairSit.id):
            for event in events:
                if ((event[0] == 6) and ((event[1] == 1) and (state == 0))):
                    if 1:
                        print 'standing up from north chair'
                        northChair.enable()
                        ageSDL.setIndex('nChairOccupant', 0, -1)
                    return
        elif (not (state)):
            return
        if (avatar != PtGetLocalAvatar()):
            print 'not activated by me'
            return
        if (id == nTubeEntry.id):
            trigger = PtFindAvatar(events)
            print 'entered team 1 tube, run behavior'
            ageSDL.setIndex('nWallPlayer', 0, PtGetClientIDFromAvatarKey(trigger.getKey()))
            trigger.avatar.runBehaviorSetNotify(nTubeMulti.value, self.key, 0)
        if (id == sTubeEntry.id):
            trigger = PtFindAvatar(events)
            print 'entered team 2 tube, run behavior'
            ageSDL.setIndex('sWallPlayer', 0, PtGetClientIDFromAvatarKey(trigger.getKey()))
            trigger.avatar.runBehaviorSetNotify(sTubeMulti.value, self.key, 0)
        if (id == upButtonS.id):
            print 'up button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                print 'correct state, blocker count limit ',
                print BlockerCountLimit
                if (BlockerCountLimit < 20):
                    self.ChangeBlockerCount((BlockerCountLimit + 1))
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
                else:
                    print 'somehow think blocker count limit greater than 20?'
            return
        elif (id == dnButtonS.id):
            print 'down button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                if (BlockerCountLimit > 0):
                    self.ChangeBlockerCount((BlockerCountLimit - 1))
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='down')
            return
        elif (id == fiveBtnS.id):
            print 'five button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                self.ChangeBlockerCount(5)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
            return
        elif (id == tenBtnS.id):
            print 'ten button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                self.ChangeBlockerCount(10)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
            return
        elif (id == fifteenBtnS.id):
            print 'fifteen button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                self.ChangeBlockerCount(15)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
            return
        elif (id == readyButtonS.id):
            print 'ready button south'
            if (southState == ptClimbingWallMsgState.kSouthSelect):
                self.ChangeGameState(ptClimbingWallMsgState.kSouthReady)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='select')
                if (northState == ptClimbingWallMsgState.kNorthSelect):
                    self.ChangeGameState(ptClimbingWallMsgState.kNorthReady)
            else:
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == goButtonS.id):
            print 'picked s go button'
            if (southState == ptClimbingWallMsgState.kSouthSit):
                print 'set index to kSouthSelect'
                self.ClearIndices(false)
                self.ChangeGameState(ptClimbingWallMsgState.kSouthSelect)
                sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='main')
                if ((northState == ptClimbingWallMsgState.kWaiting) or ((northState == ptClimbingWallMsgState.kNorthSit) or ((northState == ptClimbingWallMsgState.kNorthWin) or (northState == ptClimbingWallMsgState.kNorthQuit)))):
                    print 'force north chair to keep up'
                    self.ChangeGameState(ptClimbingWallMsgState.kNorthSelect)
            elif (southState == ptClimbingWallMsgState.kSouthReady):
                print 'check to see if you\'ve used all your wall blockers'
                numSelected = SouthCount
                maxSelections = BlockerCountLimit
                if (numSelected < maxSelections):
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
                else:
                    self.ChangeGameState(ptClimbingWallMsgState.kSouthPlayerEntry)
                    sPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='gameStart')
            return
        if (id == upButtonN.id):
            print 'up button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                numSelected = BlockerCountLimit
                if (numSelected < 20):
                    numSelected = (numSelected + 1)
                    self.ChangeBlockerCount(numSelected)
                    nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
            return
        elif (id == dnButtonN.id):
            print 'down button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                numSelected = BlockerCountLimit
                if (numSelected > 0):
                    numSelected = (numSelected - 1)
                    self.ChangeBlockerCount(numSelected)
                    nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='down')
            return
        elif (id == fiveBtnN.id):
            print 'five button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                self.ChangeBlockerCount(5)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
            return
        elif (id == tenBtnN.id):
            print 'ten button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                self.ChangeBlockerCount(10)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
            return
        elif (id == fifteenBtnN.id):
            print 'fifteen button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                self.ChangeBlockerCount(15)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='up')
            return
        elif (id == readyButtonN.id):
            print 'ready button north'
            if (northState == ptClimbingWallMsgState.kNorthSelect):
                self.ChangeGameState(ptClimbingWallMsgState.kNorthReady)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='select')
                if (southState == ptClimbingWallMsgState.kSouthSelect):
                    self.ChangeGameState(ptClimbingWallMsgState.kSouthReady)
                    print 'force south chair to keep up'
            else:
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='denied')
            return
        elif (id == goButtonN.id):
            print 'picked n go button'
            if (northState == ptClimbingWallMsgState.kNorthSit):
                print 'set index to kNorthSelect'
                self.ChangeGameState(ptClimbingWallMsgState.kNorthSelect)
                self.ClearIndices(true)
                nPanelSound.run(self.key, avatar=PtGetLocalAvatar(), state='main')
                if ((southState == ptClimbingWallMsgState.kWaiting) or ((southState == ptClimbingWallMsgState.kSouthSit) or ((southState == ptClimbingWallMsgState.kSouthWin) or (southState == ptClimbingWallMsgState.kSouthWin)))):
                    self.ChangeGameState(ptClimbingWallMsgState.kSouthSelect)
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


