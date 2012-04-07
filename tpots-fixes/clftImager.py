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
import whrandom
import time
import copy
import PlasmaControlKeys
imagerBtn = ptAttribActivator(1, 'fake imager button')
imagerBrokenBtn = ptAttribActivator(2, 'broken imager go switch')
imagerLockN = ptAttribActivator(3, 'imager lock N')
imagerLockS = ptAttribActivator(4, 'imager lock S')
imagerLockE = ptAttribActivator(5, 'imager lock E')
imagerLockW = ptAttribActivator(6, 'imager lock W')
imagerCam = ptAttribSceneobject(7, 'imager camera')
imagerRespN = ptAttribResponder(8, 'N Responder', ['State 1', 'State 2', 'State 3', 'State 4', 'SOLVED', 'State 6', 'State 7'])
imagerRespS = ptAttribResponder(9, 'S Responder', ['State 1', 'State 2', 'State 3', 'State 4', 'State 5', 'State 6', 'SOLVED'])
imagerRespW = ptAttribResponder(10, 'W Responder', ['State 1', 'SOLVED', 'State 3', 'State 4', 'State 5', 'State 6', 'State 7'])
imagerRespE = ptAttribResponder(11, 'E Responder', ['State 1', 'State 2', 'State 3', 'SOLVED', 'State 5', 'State 6', 'State 7'])
ImagerOneshot = ptAttribResponder(12, 'Rspdnr: Player avatar oneshot')
ShortVisionSound = ptAttribResponder(13, 'Rspdnr: Short Vision audio', ['on', 'off'])
LongVisionSound = ptAttribResponder(14, 'Rspdnr: Long Vision audio', ['on', 'off'])
MultiStage01 = ptAttribBehavior(15, 'Yeesha Multistage Final 01', netForce=1)
NpcSpawner = ptAttribActivator(16, 'NPC Spawn point')
hiddennode = ptAttribSceneobject(17, 'Hidden Warp node')
visiblenode = ptAttribSceneobject(18, 'Visible Warp node')
stringSDLVarLocked = ptAttribString(19, 'sdl for windmill lock')
stringSDLVarPanelN = ptAttribString(20, 'sdl for PanelN')
stringSDLVarPanelS = ptAttribString(21, 'sdl for PanelS')
stringSDLVarPanelE = ptAttribString(22, 'sdl for PanelE')
stringSDLVarPanelW = ptAttribString(23, 'sdl for PanelW')
FinalSpeech01 = ptAttribResponder(24, 'Resp: Final Speech 01', ['on', 'off'])
respBookAnim = ptAttribResponder(25, 'Resp: Tomahna book disabler')
stringSDLVarRunning = ptAttribString(26, 'sdl for windmill running')
ImagerBtnVisible = ptAttribResponder(27, 'Resp: Imager dummy vis')
ImagerBtnInvisible = ptAttribResponder(28, 'Resp: Imager dummy invis')
SeekBehavior = ptAttribBehavior(29, 'Smart seek before GUI')
FinalWarpNode = ptAttribSceneobject(30, 'Final Holo warp node')
GetClothesEvent = ptAttribActivator(31, 'event to get Yeeshas Clothes')
StopIntroVisEvent = ptAttribActivator(32, 'event to stop intro vis')
StopFinalVisEvent = ptAttribActivator(33, 'event to stop final vis')
KillIntroVisMusic = ptAttribResponder(34, 'Resp: kill intro vis music')
KillFinalVisMusic = ptAttribResponder(35, 'Resp: kill final vis music')
MakeMeVisible = ptAttribActivator(36, 'force visible on local avatar')
PlayFull = 0
minstoptime = 3
maxstoptime = 5
NpcName = None
FoundJCs = None
visionplaying = 0
visits = 0
kVision = 99
kFinished = 55
kLostPowerID = 33
PlayFinal = 0
statesN = ('State 1', 'State 2', 'State 3', 'State 4', 'SOLVED', 'State 6', 'State 7')
statesS = ('State 1', 'State 2', 'State 3', 'State 4', 'State 5', 'State 6', 'SOLVED')
statesE = ('State 1', 'State 2', 'State 3', 'SOLVED', 'State 5', 'State 6', 'State 7')
statesW = ('State 1', 'SOLVED', 'State 3', 'State 4', 'State 5', 'State 6', 'State 7')
imagerBusted = 0
speechKilled = 0
PuzzleView = 0
VisionID = None

class clftImager(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 50248473
        self.version = 26


    def OnFirstUpdate(self):
        whrandom.seed()


    def OnServerInitComplete(self):
        global statesN
        global statesS
        global statesE
        global statesW
        global imagerBusted
        respBookAnim.run(self.key)
        self.ageSDL = PtGetAgeSDL()
        self.ageSDL.setNotify(self.key, stringSDLVarLocked.value, 0.0)
        self.ageSDL.setNotify(self.key, stringSDLVarPanelN.value, 0.0)
        self.ageSDL.setNotify(self.key, stringSDLVarPanelS.value, 0.0)
        self.ageSDL.setNotify(self.key, stringSDLVarPanelE.value, 0.0)
        self.ageSDL.setNotify(self.key, stringSDLVarPanelW.value, 0.0)
        try:
            intPanelN = self.ageSDL[stringSDLVarPanelN.value][0]
        except:
            intPanelN = 3
            PtDebugPrint('ERROR:  clftImager.OnServerInitComplete():\tERROR: age sdl read failed, defaulting intPanelN = 3')
        panelN = statesN[intPanelN]
        imagerRespN.run(self.key, state=('%s' % panelN))
        try:
            intPanelS = self.ageSDL[stringSDLVarPanelS.value][0]
        except:
            intPanelS = 5
            PtDebugPrint('ERROR:  clftImager.OnServerInitComplete():\tERROR: age sdl read failed, defaulting intPanelS = 5')
        panelS = statesS[intPanelS]
        imagerRespS.run(self.key, state=('%s' % panelS))
        try:
            intPanelE = self.ageSDL[stringSDLVarPanelE.value][0]
        except:
            intPanelE = 3
            PtDebugPrint('ERROR:  clftImager.OnServerInitComplete():\tERROR: age sdl read failed, defaulting intPanelE = 3')
        panelE = statesE[intPanelE]
        imagerRespE.run(self.key, state=('%s' % panelE))
        try:
            intPanelW = self.ageSDL[stringSDLVarPanelW.value][0]
        except:
            intPanelW = 0
            PtDebugPrint('ERROR:  clftImager.OnServerInitComplete():\tERROR: age sdl read failed, defaulting intPanelW = 0')
        panelW = statesW[intPanelW]
        imagerRespW.run(self.key, state=('%s' % panelW))
        SDLVarTomahnaActive = 'clftTomahnaActive'
        boolTomahnaActive = self.ageSDL[SDLVarTomahnaActive][0]
        if boolTomahnaActive:
            PtDebugPrint('Cleft.OnServerInitComplete: SDL says Tomahna is active, will set Imager to break...')
            imagerBusted = 1
        else:
            PtDebugPrint('Cleft.OnServerInitComplete: SDL says Tomahna is NOT active, will set Imager to work...')
            imagerBusted = 0


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global visionplaying
        global statesN
        global statesS
        global statesE
        global statesW
        self.ageSDL = PtGetAgeSDL()
        if (VARname == stringSDLVarLocked.value):
            windmillLocked = self.ageSDL[stringSDLVarLocked.value][0]
            if (windmillLocked and visionplaying):
                PtAtTimeCallback(self.key, 3, kLostPowerID)
        if (VARname == stringSDLVarPanelN.value):
            intPanelN = self.ageSDL[stringSDLVarPanelN.value][0]
            panelN = statesN[intPanelN]
            imagerRespN.run(self.key, state=('%s' % panelN))
        if (VARname == stringSDLVarPanelS.value):
            intPanelS = self.ageSDL[stringSDLVarPanelS.value][0]
            panelS = statesS[intPanelS]
            imagerRespS.run(self.key, state=('%s' % panelS))
        if (VARname == stringSDLVarPanelE.value):
            intPanelE = self.ageSDL[stringSDLVarPanelE.value][0]
            panelE = statesE[intPanelE]
            imagerRespE.run(self.key, state=('%s' % panelE))
        if (VARname == stringSDLVarPanelW.value):
            intPanelW = self.ageSDL[stringSDLVarPanelW.value][0]
            panelW = statesW[intPanelW]
            imagerRespW.run(self.key, state=('%s' % panelW))
        intPanelN = self.ageSDL[stringSDLVarPanelN.value][0]
        intPanelS = self.ageSDL[stringSDLVarPanelS.value][0]
        intPanelE = self.ageSDL[stringSDLVarPanelE.value][0]
        intPanelW = self.ageSDL[stringSDLVarPanelW.value][0]
        if ((intPanelN == 0) and ((intPanelS == 0) and ((intPanelW == 0) and (intPanelE == 0)))):
            import xSndLogTracks
            if xSndLogTracks.LogTrack('421', '15'):
                xSndLogTracks.SetLogMode()


    def OnControlKeyEvent(self, controlKey, activeFlag):
        global PuzzleView
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            if PuzzleView:
                self.IQuitImager()
        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
            if PuzzleView:
                self.IQuitImager()


    def IQuitImager(self):
        global PuzzleView
        print 'disengage and exit the imager puzzle'
        avatar = PtGetLocalAvatar()
        imagerCam.value.popCutsceneCamera(avatar.getKey())
        imagerBrokenBtn.disableActivator()
        imagerLockN.disableActivator()
        imagerLockS.disableActivator()
        imagerLockW.disableActivator()
        imagerLockE.disableActivator()
        avatar.draw.enable()
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        PtDisableControlKeyEvents(self.key)
        PtEnableForwardMovement()
        PtSendKIMessage(kEnableEntireYeeshaBook, 0)
        PuzzleView = 0
        PtAtTimeCallback(self.key, 1, imagerBtn.id)


    def OnNotify(self, state, id, events):
        global NpcName
        global PuzzleView
        global PlayFull
        global PlayFinal
        global imagerBusted
        global visionplaying
        global speechKilled
        global minstoptime
        global maxstoptime
        global kVision
        self.ageSDL = PtGetAgeSDL()
        if ((id == MakeMeVisible.id) and state):
            if PtFirstPerson():
                return
            avatar = PtFindAvatar(events)
            avatar.draw.enable()
            print 'force avatar visible'
            return
        if (id == NpcSpawner.id):
            NpcName = PtFindAvatar(events)
            MultiStage01.run(NpcName)
            NpcName.draw.disable()
            print ' yeesha spawned'
        if ((id == imagerBtn.id) and state):
            print 'switch to imager close up'
            imagerBtn.disableActivator()
            ImagerBtnInvisible.run(self.key)
            PtEnableControlKeyEvents(self.key)
            avatar = PtFindAvatar(events)
            SeekBehavior.run(avatar)
        if (id == SeekBehavior.id):
            if PtWasLocallyNotified(self.key):
                for event in events:
                    if ((event[0] == kMultiStageEvent) and (event[2] == kEnterStage)):
                        avatar = PtFindAvatar(events)
                        SeekBehavior.gotoStage(avatar, -1)
                        PtDebugPrint('clftImager.onNotify: enter puzzle view mode now that seek is done')
                        avatar.draw.disable()
                        imagerCam.value.pushCutsceneCamera(0, avatar.getKey())
                        cam = ptCamera()
                        cam.disableFirstPersonOverride()
                        cam.undoFirstPerson()
                        PtSendKIMessage(kDisableEntireYeeshaBook, 0)
                        PtDisableForwardMovement()
                        PuzzleView = 1
                        PtAtTimeCallback(self.key, 0.5, imagerBrokenBtn.id)
                        return
        if ((id == imagerBrokenBtn.id) and state):
            print 'trigger imager'
            imagerBrokenBtn.disableActivator()
            imagerLockN.disableActivator()
            imagerLockS.disableActivator()
            imagerLockW.disableActivator()
            imagerLockE.disableActivator()
            PtDisableControlKeyEvents(self.key)
            avatar = PtFindAvatar(events)
            imagerCam.value.popCutsceneCamera(avatar.getKey())
            avatar.draw.enable()
            cam = ptCamera()
            cam.enableFirstPersonOverride()
            if self.EndgameSolved():
                PlayFull = 0
                PlayFinal = 1
                print 'play final speech'
            elif self.OpeningSolved():
                PlayFull = 1
                PlayFinal = 0
                print 'play full opening speech'
            else:
                PlayFull = 0
                PlayFinal = 0
                print 'play partial opening speech'
            for event in events:
                if ((event[0] == 2) and (event[1] == 1)):
                    ImagerOneshot.run(self.key, events=events, avatar=PtGetLocalAvatar())
                    return
        if (id == ImagerOneshot.id):
            print 'avatar oneshot callback'
            PuzzleView = 0
            PtEnableForwardMovement()
            PtSendKIMessage(kEnableEntireYeeshaBook, 0)
            windmillRunning = self.ageSDL[stringSDLVarRunning.value][0]
            if ((windmillRunning == 1) and (imagerBusted == 0)):
                PtDebugPrint('clftImager.OnNotify: SDL says windmill is running, so button will do SOMETHING after oneshot...')
                for event in events:
                    if ((event[0] == 8) and (event[1] == 1)):
                        if visionplaying:
                            print 'Now, killing vision'
                            speechKilled = 1
                            self.StopVision()
                        elif (visionplaying == 0):
                            self.StartVision()
                            if (PlayFinal == 1):
                                print 'nothing'
                            elif ((PlayFinal == 0) and (PlayFull == 0)):
                                stopvision = whrandom.randint(minstoptime, maxstoptime)
                                print ('\tImager will autoshut off in %d seconds' % stopvision)
                                PtAtTimeCallback(self.key, stopvision, kVision)
                            elif (PlayFull == 1):
                                print 'nothing'
            else:
                PtDebugPrint('clftImager.OnNotify: SDL says windmill is NOT running, so button will stop after oneshot...')
                PtAtTimeCallback(self.key, 1, imagerBtn.id)
        if ((id == GetClothesEvent.id) and state):
            avatar = PtGetLocalAvatar()
            currentgender = avatar.avatar.getAvatarClothingGroup()
            if (currentgender == kFemaleClothingGroup):
                clothingName = '02_FTorso11_01'
            else:
                clothingName = '02_MTorso09_01'
            clothingList = avatar.avatar.getWardrobeClothingList()
            if (clothingName not in clothingList):
                print ('adding Yeesha reward clothing %s to wardrobe' % clothingName)
                avatar.avatar.addWardrobeClothingItem(clothingName, ptColor().white(), ptColor().black())
            else:
                print 'player already has Yeesha reward clothing, doing nothing'
        if ((id == StopIntroVisEvent.id) and state):
            speechKilled = 0
            self.StopVision()
        if ((id == StopFinalVisEvent.id) and state):
            speechKilled = 0
            self.StopVision()


    def OpeningSolved(self):
        solutionList = [4, 3, 6, 1]
        imagerList = []
        imagerList.append(imagerRespN.state_list.index(imagerRespN.getState()))
        imagerList.append(imagerRespE.state_list.index(imagerRespE.getState()))
        imagerList.append(imagerRespS.state_list.index(imagerRespS.getState()))
        imagerList.append(imagerRespW.state_list.index(imagerRespW.getState()))
        print 'solution list:',
        print solutionList
        print 'imager list  :',
        print imagerList
        if self.AreListsEquiv(solutionList, imagerList):
            return true
        else:
            return false


    def GetAgeNode(self, age):
        vault = ptVault()
        chron = vault.findChronicleEntry('BahroCave')
        if (type(chron) != type(None)):
            ageChronRefList = chron.getChildNodeRefList()
            if (type(ageChronRefList) != type(None)):
                for ageChron in ageChronRefList:
                    ageChild = ageChron.getChild()
                    ageChild = ageChild.upcastToChronicleNode()
                    if (ageChild.chronicleGetName() == age):
                        return ageChild
        return None


    def GetAgeSolutionSymbol(self, age):
        node = self.GetAgeNode(age)
        if (node != None):
            varlist = node.chronicleGetValue().split(',')
            return varlist[1]
        else:
            return None


    def AreListsEquiv(self, list1, list2):
        if (list1[0] in list2):
            list2Copy = copy.copy(list2)
            while ((list2Copy[0] != list1[0])):
                list2Copy.append(list2Copy.pop(0))
            for i in range(4):
                if (list2Copy[i] != list1[i]):
                    return false
            return true
        return false


    def EndgameSolved(self):
        solutionList = []
        currentStateList = []
        for age in ['Teledahn', 'Garden', 'Garrison', 'Kadish']:
            symbol = self.GetAgeSolutionSymbol(age)
            if (type(symbol) == type('')):
                symbol = int(symbol)
            solutionList.append(symbol)
        currentStateList.append(imagerRespN.state_list.index(imagerRespN.getState()))
        currentStateList.append(imagerRespE.state_list.index(imagerRespE.getState()))
        currentStateList.append(imagerRespS.state_list.index(imagerRespS.getState()))
        currentStateList.append(imagerRespW.state_list.index(imagerRespW.getState()))
        for x in range(4):
            currentStateList[x] = ((currentStateList[x] + 6) % 7)
        print ('solution list: ' + str(solutionList))
        print ('currentState list: ' + str(currentStateList))
        if self.AreListsEquiv(solutionList, currentStateList):
            return true
        else:
            return false


    def OnTimer(self, id):
        global visionplaying
        global kVision
        global speechKilled
        if ((visionplaying == 1) and (id == kVision)):
            print '\nclftImager.Ontimer:Got kVision timer callback. Automatically stopping vision.'
            self.StopVision()
            imagerBrokenBtn.disableActivator()
            imagerLockN.disableActivator()
            imagerLockS.disableActivator()
            imagerLockW.disableActivator()
            imagerLockE.disableActivator()
        elif (id == imagerBrokenBtn.id):
            print '\nclftImager.Ontimer:Got timer callback. Setting up Imager button....'
            imagerBtn.disableActivator()
            ImagerBtnInvisible.run(self.key)
            imagerBrokenBtn.enableActivator()
            imagerLockN.enableActivator()
            imagerLockS.enableActivator()
            imagerLockW.enableActivator()
            imagerLockE.enableActivator()
            PtSendKIMessage(kDisableEntireYeeshaBook, 0)
            PtDisableForwardMovement()
        elif (id == imagerBtn.id):
            print '\nclftImager.Ontimer:Got timer callback. Setting up Imager dummy....'
            imagerBrokenBtn.disableActivator()
            imagerLockN.disableActivator()
            imagerLockS.disableActivator()
            imagerLockW.disableActivator()
            imagerLockE.disableActivator()
            imagerBtn.enableActivator()
            ImagerBtnVisible.run(self.key)
            PtEnableForwardMovement()
            PtSendKIMessage(kEnableEntireYeeshaBook, 0)
        elif (id == kLostPowerID):
            speechKilled = 1
            self.StopVision()
            imagerBrokenBtn.disableActivator()
            imagerLockN.disableActivator()
            imagerLockS.disableActivator()
            imagerLockW.disableActivator()
            imagerLockE.disableActivator()


    def StartVision(self):
        global NpcName
        global PlayFinal
        global visionplaying
        global VisionID
        global PlayFull
        print 'clftImager.StartVision: Playing Yeesha vision.'
        NpcName.draw.enable()
        PtDebugPrint(('clftImager.StartVision: PlayFinal = %s' % PlayFinal))
        if (PlayFinal == 1):
            NpcName.physics.warpObj(FinalWarpNode.value.getKey())
            MultiStage01.gotoStage(NpcName, 2, dirFlag=1, isForward=1)
            visionplaying = 1
            VisionID = 'final'
            FinalSpeech01.run(self.key, state='on')
            PtDebugPrint('clftImager.StartVision: play final Yeesha speech 01, then enable Tomahna book...')
            PtAtTimeCallback(self.key, 1, imagerBtn.id)
        elif ((PlayFinal == 0) and (PlayFull == 1)):
            vault = ptVault()
            entry = vault.findChronicleEntry('YeeshaVisionViewed')
            if (type(entry) == type(None)):
                vault.addChronicleEntry('YeeshaVisionViewed', 0, '1')
            else:
                entry.chronicleSetValue('1')
                entry.save()
            NpcName.physics.warpObj(visiblenode.value.getKey())
            MultiStage01.gotoStage(NpcName, 1, dirFlag=1, isForward=1)
            visionplaying = 1
            VisionID = 'long'
            LongVisionSound.run(self.key, state='on')
            PtAtTimeCallback(self.key, 1, imagerBtn.id)
        else:
            NpcName.physics.warpObj(visiblenode.value.getKey())
            MultiStage01.gotoStage(NpcName, 1, dirFlag=1, isForward=1)
            visionplaying = 1
            VisionID = 'short'
            ShortVisionSound.run(self.key, state='on')
            PtAtTimeCallback(self.key, 1, imagerBtn.id)


    def StopVision(self):
        global NpcName
        global VisionID
        global visionplaying
        global speechKilled
        global PuzzleView
        print 'clftImager.StopVision: Stopping Yeesha vision.'
        NpcName.draw.disable()
        NpcName.physics.warpObj(hiddennode.value.getKey())
        if (VisionID == 'final'):
            MultiStage01.gotoStage(NpcName, 0, dirFlag=1, isForward=1)
            visionplaying = 0
            print 'TRYING TO KILL FINAL VISION'
            if (speechKilled == 1):
                FinalSpeech01.run(self.key, state='on', fastforward=1)
                KillFinalVisMusic.run(self.key)
                speechKilled = 0
            FinalSpeech01.run(self.key, state='off')
        elif (VisionID == 'long'):
            MultiStage01.gotoStage(NpcName, 0, dirFlag=1, isForward=1)
            visionplaying = 0
            if (speechKilled == 1):
                LongVisionSound.run(self.key, state='on', fastforward=1)
                KillIntroVisMusic.run(self.key)
                speechKilled = 0
            LongVisionSound.run(self.key, state='off')
        elif (VisionID == 'short'):
            MultiStage01.gotoStage(NpcName, 0, dirFlag=1, isForward=1)
            visionplaying = 0
            ShortVisionSound.run(self.key, state='on', fastforward=1)
            ShortVisionSound.run(self.key, state='off')
            speechKilled = 0
        else:
            print 'clftImager.StopVision: Don\'t know which vision to kill!'
        print ('PuzzleView = %s' % PuzzleView)
        avatar = PtGetLocalAvatar()
        if PuzzleView:
            avatar.draw.disable()
            PtAtTimeCallback(self.key, 0.5, imagerBrokenBtn.id)
        else:
            avatar.draw.enable()
            PtAtTimeCallback(self.key, 0.5, imagerBtn.id)


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



