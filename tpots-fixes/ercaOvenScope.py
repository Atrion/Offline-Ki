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
import PlasmaControlKeys
import string
import xEnum
from math import *
Activate = ptAttribActivator(1, 'clk: Oven scope', netForce=1)
Camera = ptAttribSceneobject(2, 'Oven scope camera')
Behavior = ptAttribBehavior(3, 'Scope behavior (multistage)', netForce=1)
Vignette = ptAttribString(4, 'Vignette dialog - by Name')
SDLBakeryPwr = ptAttribString(5, 'SDL: bakery power')
SDLScopePwr = ptAttribString(6, 'SDL: scope power')
CameraBad = ptAttribSceneobject(7, 'Oven scope camera - no power')
VignetteBad = ptAttribString(8, 'Vignette dialog - no power')
ScopeNum = ptAttribInt(9, 'Oven scope #')
RespTimeSlider = ptAttribResponder(10, 'resp: time slider', ['off', 'on'])
RespAmountSlider = ptAttribResponder(11, 'resp: amount slider', ['off', 'on'])
RespTempSlider = ptAttribResponder(12, 'resp: temp slider', ['off', 'on'])
RespSoundTest = ptAttribResponder(13, 'resp: sound test')
RespMayBake = ptAttribResponder(14, 'resp: may bake', ['no', 'yes'])
RespSfxTimerWheel = ptAttribResponder(15, 'resp: timer wheel sfx', ['off', 'on'])
kTimeSlider = 100
kAmountSlider = 200
kTempSlider = 300
kBakeBtn = 400
kTimerWheel = 500
kTempWheel = 600
kTimeScale = 10
LocalAvatar = None
boolScopeOperator = 0
boolOperated = 0
Telescope = ptInputInterface()
boolBakeryPwr = 0
boolScopePwr = 0
WasPowered = 1
listTimeSDLs = ['ercaTimeSlider1', 'ercaTimeSlider2', 'ercaTimeSlider3', 'ercaTimeSlider4']
listAmountSDLs = ['ercaAmountSlider1', 'ercaAmountSlider2', 'ercaAmountSlider3', 'ercaAmountSlider4']
listTempSDLs = ['ercaTempSlider1', 'ercaTempSlider2', 'ercaTempSlider3', 'ercaTempSlider4']
timeSDL = None
amountSDL = None
tempSDL = None
byteTime = 0
byteAmount = 0
byteTemp = 0
timeSlider = None
amountSlider = None
tempSlider = None
bakeBtn = None
timerWheel = None
tempWheel = None
boolMayBake = 0
IsBaking = 0
exitScope = 0
setTempWheel = 0

class ercaOvenScope(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 7030
        self.version = 9


    def OnFirstUpdate(self):
        self.SDL.setDefault('boolOperated', (0,))
        self.SDL.setDefault('OperatorID', (-1,))
        self.SDL.sendToClients('boolOperated')
        self.SDL.sendToClients('OperatorID')


    def OnServerInitComplete(self):
        global timeSDL
        global amountSDL
        global tempSDL
        global boolBakeryPwr
        global boolScopePwr
        global boolMayBake
        global IsBaking
        global byteTime
        global byteAmount
        global byteTemp
        timeSDL = listTimeSDLs[(ScopeNum.value - 1)]
        amountSDL = listAmountSDLs[(ScopeNum.value - 1)]
        tempSDL = listTempSDLs[(ScopeNum.value - 1)]
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(SDLBakeryPwr.value, 1, 1)
        ageSDL.sendToClients(SDLBakeryPwr.value)
        ageSDL.setFlags(SDLScopePwr.value, 1, 1)
        ageSDL.sendToClients(SDLScopePwr.value)
        ageSDL.setFlags(timeSDL, 1, 1)
        ageSDL.sendToClients(timeSDL)
        ageSDL.setFlags(amountSDL, 1, 1)
        ageSDL.sendToClients(amountSDL)
        ageSDL.setFlags(tempSDL, 1, 1)
        ageSDL.sendToClients(tempSDL)
        ageSDL.setFlags('ercaMayBake', 1, 1)
        ageSDL.sendToClients('ercaMayBake')
        ageSDL.setFlags('ercaBakeFinishTime', 1, 1)
        ageSDL.sendToClients('ercaBakeFinishTime')
        ageSDL.setNotify(self.key, SDLBakeryPwr.value, 0.0)
        ageSDL.setNotify(self.key, SDLScopePwr.value, 0.0)
        ageSDL.setNotify(self.key, timeSDL, 0.0)
        ageSDL.setNotify(self.key, amountSDL, 0.0)
        ageSDL.setNotify(self.key, tempSDL, 0.0)
        ageSDL.setNotify(self.key, 'ercaMayBake', 0.0)
        ageSDL.setNotify(self.key, 'ercaBakeFinishTime', 0.0)
        try:
            boolBakeryPwr = ageSDL[SDLBakeryPwr.value][0]
        except:
            PtDebugPrint('ERROR: ercaOvenScope.OnServerInitComplete():\tERROR reading SDL name for bakery power')
            boolBakeryPwr = 0
        PtDebugPrint(('DEBUG: ercaOvenScope.OnServerInitComplete():\t%s = %d' % (SDLBakeryPwr.value, ageSDL[SDLBakeryPwr.value][0])))
        try:
            boolScopePwr = ageSDL[SDLScopePwr.value][0]
        except:
            PtDebugPrint('ERROR: ercaOvenScope.OnServerInitComplete():\tERROR reading SDL name for scope power')
            boolScopePwr = 0
        PtDebugPrint(('DEBUG: ercaOvenScope.OnServerInitComplete():\t%s = %d' % (SDLScopePwr.value, ageSDL[SDLScopePwr.value][0])))
        try:
            boolMayBake = ageSDL['ercaMayBake'][0]
        except:
            PtDebugPrint('ERROR: ercaOvenScope.OnServerInitComplete():\tERROR reading SDL name for ercaMayBake')
            boolMayBake = 0
        PtDebugPrint(('DEBUG: ercaOvenScope.OnServerInitComplete():\tercaMayBake = %d' % ageSDL['ercaMayBake'][0]))
        try:
            IsBaking = ageSDL['ercaBakeFinishTime'][0]
        except:
            PtDebugPrint('ERROR: ercaOvenScope.OnServerInitComplete():\tERROR reading SDL name for ercaBakeFinishTime')
            IsBaking = 0
        PtDebugPrint(('DEBUG: ercaOvenScope.OnServerInitComplete():\tercaBakeFinishTime = %d' % ageSDL['ercaBakeFinishTime'][0]))
        byteTime = ageSDL[timeSDL][0]
        byteAmount = ageSDL[amountSDL][0]
        byteTemp = ageSDL[tempSDL][0]
        if ((type(Vignette.value) != type(None)) and (Vignette.value != '')):
            PtLoadDialog(Vignette.value, self.key)


    def Load(self):
        solo = true
        if len(PtGetPlayerList()):
            solo = false
        boolOperated = self.SDL['boolOperated'][0]
        if boolOperated:
            if solo:
                PtDebugPrint(('ercaOvenScope.Load():\tboolOperated=%d but no one else here...correcting' % boolOperated), level=kDebugDumpLevel)
                boolOperated = 0
                self.SDL['boolOperated'] = (0,)
                self.SDL['OperatorID'] = (-1,)
                Activate.enable()
            else:
                Activate.disable()
                PtDebugPrint(('ercaOvenScope.Load():\tboolOperated=%d, disabling telescope clickable' % boolOperated), level=kDebugDumpLevel)


    def AvatarPage(self, avObj, pageIn, lastOut):
        if pageIn:
            return
        avID = PtGetClientIDFromAvatarKey(avObj.getKey())
        if (avID == self.SDL['OperatorID'][0]):
            Activate.enable()
            self.SDL['OperatorID'] = (-1,)
            self.SDL['boolOperated'] = (0,)
            PtDebugPrint('ercaOvenScope.AvatarPage(): telescope operator paged out, reenabled telescope.', level=kDebugDumpLevel)
        else:
            return


    def __del__(self):
        PtUnloadDialog(Vignette.value)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global boolBakeryPwr
        global IsBaking
        global boolMayBake
        global boolScopePwr
        global timeSlider
        global amountSlider
        global tempSlider
        global bakeBtn
        global timerWheel
        global tempWheel
        global timeSDL
        global byteTime
        global amountSDL
        global byteAmount
        global tempSDL
        global byteTemp
        ageSDL = PtGetAgeSDL()
        if (VARname == SDLBakeryPwr.value):
            boolBakeryPwr = ageSDL[SDLBakeryPwr.value][0]
            if (boolBakeryPwr == 0):
                if (IsBaking != 0):
                    ageSDL['ercaBakeFinishTime'] = (0,)
                if boolMayBake:
                    ageSDL['ercaMayBake'] = (0,)
            else:
                self.ICheckScopes()
        if (VARname == SDLScopePwr.value):
            boolScopePwr = ageSDL[SDLScopePwr.value][0]
        if (VARname == 'ercaMayBake'):
            boolMayBake = ageSDL['ercaMayBake'][0]
            PtDebugPrint(('ercaOvenScope:OnSDLNotify:  SDL for ercaMayBake now set to %d' % boolMayBake))
            if boolMayBake:
                RespMayBake.run(self.key, state='yes')
            else:
                RespMayBake.run(self.key, state='no')
        if (VARname == 'ercaBakeFinishTime'):
            IsBaking = ageSDL['ercaBakeFinishTime'][0]
            if (IsBaking != 0):
                timeSlider.disable()
                amountSlider.disable()
                tempSlider.disable()
                bakeBtn.disable()
            else:
                timerWheel.setValue(0)
                tempWheel.setValue(0)
                timeSlider.enable()
                amountSlider.enable()
                tempSlider.enable()
                bakeBtn.enable()
        if (VARname == timeSDL):
            byteTimeOld = byteTime
            byteTime = ageSDL[timeSDL][0]
            PtDebugPrint(('ercaOvenScope:OnSDLNotify:  SDL for %s now set to %d' % (timeSDL, byteTime)))
##############################################################################
# Incorrect lights with multiple users fix
##############################################################################
#            RespSoundTest.run(self.key)
#            if ((byteTime == 0) and (byteTimeOld > 0)):
#                RespTimeSlider.run(self.key, state='off')
#                if (boolMayBake != 0):
#                    ageSDL['ercaMayBake'] = (0,)
#            elif ((byteTime > 0) and (byteTimeOld == 0)):
#                RespTimeSlider.run(self.key, state='on')
#                if (boolMayBake == 0):
#                    self.ICheckScopes()
            myID = PtGetLocalClientID()
            if self.SDL['boolOperated'][0] and self.SDL['OperatorID'][0] == myID:
                RespSoundTest.run(self.key)
                if ((byteTime == 0) and (byteTimeOld > 0)):
                    RespTimeSlider.run(self.key, state='off', netPropagate=0)
                    if (boolMayBake != 0):
                        ageSDL['ercaMayBake'] = (0,)
                elif ((byteTime > 0) and (byteTimeOld == 0)):
                    RespTimeSlider.run(self.key, state='on', netPropagate=0)
                    if (boolMayBake == 0):
                        self.ICheckScopes()
##############################################################################
# End incorrect lights with multiple users fix
##############################################################################
        if (VARname == amountSDL):
            byteAmountOld = byteAmount
            byteAmount = ageSDL[amountSDL][0]
            PtDebugPrint(('ercaOvenScope:OnSDLNotify:  SDL for %s now set to %d' % (amountSDL, byteAmount)))
##############################################################################
# Incorrect lights with multiple users fix
##############################################################################
#            RespSoundTest.run(self.key)
#            if ((byteAmount == 0) and (byteAmountOld > 0)):
#                RespAmountSlider.run(self.key, state='off')
#                if (boolMayBake != 0):
#                    ageSDL['ercaMayBake'] = (0,)
#            elif ((byteAmount > 0) and (byteAmountOld == 0)):
#                RespAmountSlider.run(self.key, state='on')
#                if (boolMayBake == 0):
#                    self.ICheckScopes()
            myID = PtGetLocalClientID()
            if self.SDL['boolOperated'][0] and self.SDL['OperatorID'][0] == myID:
                RespSoundTest.run(self.key)
                if ((byteAmount == 0) and (byteAmountOld > 0)):
                    RespAmountSlider.run(self.key, state='off', netPropagate=0)
                    if (boolMayBake != 0):
                        ageSDL['ercaMayBake'] = (0,)
                elif ((byteAmount > 0) and (byteAmountOld == 0)):
                    RespAmountSlider.run(self.key, state='on', netPropagate=0)
                    if (boolMayBake == 0):
                        self.ICheckScopes()
##############################################################################
# End incorrect lights with multiple users fix
##############################################################################
        if (VARname == tempSDL):
            byteTempOld = byteTemp
            byteTemp = ageSDL[tempSDL][0]
            PtDebugPrint(('ercaOvenScope:OnSDLNotify:  SDL for %s now set to %d' % (tempSDL, byteTemp)))
##############################################################################
# Incorrect lights with multiple users fix
##############################################################################
#            RespSoundTest.run(self.key)
#            if ((byteTemp == 0) and (byteTempOld > 0)):
#                RespTempSlider.run(self.key, state='off')
#                if (boolMayBake != 0):
#                    ageSDL['ercaMayBake'] = (0,)
#            elif ((byteTemp > 0) and (byteTempOld == 0)):
#                RespTempSlider.run(self.key, state='on')
#                if (boolMayBake == 0):
#                    self.ICheckScopes()
            myID = PtGetLocalClientID()
            if self.SDL['boolOperated'][0] and self.SDL['OperatorID'][0] == myID:
                RespSoundTest.run(self.key)
                if ((byteTemp == 0) and (byteTempOld > 0)):
                    RespTempSlider.run(self.key, state='off', netPropagate=0)
                    if (boolMayBake != 0):
                        ageSDL['ercaMayBake'] = (0,)
                elif ((byteTemp > 0) and (byteTempOld == 0)):
                    RespTempSlider.run(self.key, state='on', netPropagate=0)
                    if (boolMayBake == 0):
                        self.ICheckScopes()
##############################################################################
# End incorrect lights with multiple users fix
##############################################################################


    def ICheckScopes(self):
        global boolBakeryPwr
        ageSDL = PtGetAgeSDL()
        for xSDL in listTimeSDLs:
            xVal = ageSDL[xSDL][0]
            if (xVal == 0):
                break
        for ySDL in listAmountSDLs:
            yVal = ageSDL[ySDL][0]
            if (yVal == 0):
                break
        for zSDL in listTempSDLs:
            zVal = ageSDL[zSDL][0]
            if (zVal == 0):
                break
        if ((xVal != 0) and ((yVal != 0) and (zVal != 0))):
            if boolBakeryPwr:
                ageSDL['ercaMayBake'] = (1,)
            else:
                ageSDL['ercaMayBake'] = (0,)


    def OnNotify(self, state, id, events):
        global LocalAvatar
        global boolScopeOperator
        PtDebugPrint(('ercaOvenScope:OnNotify  state=%f id=%d events=' % (state, id)), events, level=kDebugDumpLevel)
        if (state and ((id == Activate.id) and PtWasLocallyNotified(self.key))):
            LocalAvatar = PtFindAvatar(events)
            self.IStartTelescope()
        for event in events:
            if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                if boolScopeOperator:
                    self.IEngageTelescope()
                    boolScopeOperator = 0
                break


    def OnGUINotify(self, id, control, event):
        global WasPowered
        global timeSlider
        global amountSlider
        global tempSlider
        global bakeBtn
        global timerWheel
        global tempWheel
        global IsBaking
        global byteTime
        global byteTemp
        global setTempWheel
        global timeSDL
        global byteAmount
        global amountSDL
        global tempSDL
        global boolMayBake
        PtDebugPrint(('GUI Notify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
        ageSDL = PtGetAgeSDL()
        if (event == kDialogLoaded):
            if (WasPowered == 0):
                return
            timeSlider = ptGUIControlKnob(control.getControlFromTag(kTimeSlider))
            amountSlider = ptGUIControlKnob(control.getControlFromTag(kAmountSlider))
            tempSlider = ptGUIControlKnob(control.getControlFromTag(kTempSlider))
            bakeBtn = ptGUIControlButton(control.getControlFromTag(kBakeBtn))
            timerWheel = ptGUIControlProgress(control.getControlFromTag(kTimerWheel))
            tempWheel = ptGUIControlProgress(control.getControlFromTag(kTempWheel))
        elif (event == kShowHide):
            if (WasPowered == 0):
                return
            if control.isEnabled():
                control.show()
                PtDebugPrint(('ercaOvenScope:OnGUINotify:  SDL %s is %d' % (timeSDL, byteTime)))
                PtDebugPrint(('ercaOvenScope:OnGUINotify:  SDL %s is %d' % (amountSDL, byteAmount)))
                PtDebugPrint(('ercaOvenScope:OnGUINotify:  SDL %s is %d' % (tempSDL, byteTemp)))
                if (IsBaking != 0):
                    print 'OnGUINotfiy.ShowHide: will now set timerWheel to: ',
                    print byteTime
                    print 'OInGUINotfiy.ShowHide: will now set tempWheel to: ',
                    print byteTemp
                    if setTempWheel:
                        tempWheel.setValue(byteTemp)
                    self.IDoTimerWheel()
                    timeSlider.disable()
                    amountSlider.disable()
                    tempSlider.disable()
                    bakeBtn.disable()
                else:
                    timerWheel.setValue(0)
                    tempWheel.setValue(0)
                    timeSlider.enable()
                    amountSlider.enable()
                    tempSlider.enable()
                    bakeBtn.enable()
        elif (event == kValueChanged):
            if (type(control) != type(None)):
                knobID = control.getTagID()
                if (knobID == kTimeSlider):
                    newVal = int(round(timeSlider.getValue()))
                    if (byteTime != newVal):
                        ageSDL[timeSDL] = (newVal,)
                elif (knobID == kAmountSlider):
                    newVal = int(round(amountSlider.getValue()))
                    if (byteAmount != newVal):
                        ageSDL[amountSDL] = (newVal,)
                elif (knobID == kTempSlider):
                    newVal = int(round(tempSlider.getValue()))
                    if (byteTemp != newVal):
                        ageSDL[tempSDL] = (newVal,)
        elif (event == kAction):
            if (type(control) != type(None)):
                btnID = control.getTagID()
                if (btnID == kBakeBtn):
                    if (isinstance(control, ptGUIControlButton) and control.isButtonDown()):
                        PtDebugPrint('ercaOvenScope:GUINotify Bake button down', level=kDebugDumpLevel)
                    else:
                        PtDebugPrint('ercaOvenScope:GUINotify Bake button up', level=kDebugDumpLevel)
                        if ((boolMayBake == 1) and (IsBaking == 0)):
                            timerPercent = (byteTime * 0.01)
                            timerWheel.animateToPercent(timerPercent)
                            ageSDL['ercaBakeFinishTime'] = (1,)
                            PtAtTimeCallback(self.key, 1, 2)


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            self.IQuitTelescope()
        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
            self.IQuitTelescope()


    def IStartTelescope(self):
        global boolScopeOperator
        global LocalAvatar
        PtSendKIMessage(kDisableKIandBB, 0)
        Activate.disable()
        boolScopeOperator = 1
        self.SDL['boolOperated'] = (1,)
        avID = PtGetClientIDFromAvatarKey(LocalAvatar.getKey())
        self.SDL['OperatorID'] = (avID,)
        PtDebugPrint('ercaOvenScope.OnNotify:\twrote SDL - scope operator id = ', avID, level=kDebugDumpLevel)
        Behavior.run(LocalAvatar)


    def IEngageTelescope(self):
        global exitScope
        global Telescope
        global boolBakeryPwr
        global boolScopePwr
        global WasPowered
        global timeSlider
        global byteTime
        global amountSlider
        global byteAmount
        global tempSlider
        global byteTemp
        global boolMayBake
        exitScope = 0
        Telescope.pushTelescope()
        cam = ptCamera()
        cam.undoFirstPerson()
        cam.disableFirstPersonOverride()
        virtCam = ptCamera()
        if (boolBakeryPwr and boolScopePwr):
            WasPowered = 1
            virtCam.save(Camera.sceneobject.getKey())
            if PtIsDialogLoaded(Vignette.value):
                timeSlider.setValue(byteTime)
                if (byteTime != 0):
                    RespTimeSlider.run(self.key, state='on', fastforward=1)
                else:
                    RespTimeSlider.run(self.key, state='off', fastforward=1)
                amountSlider.setValue(byteAmount)
                if (byteAmount != 0):
                    RespAmountSlider.run(self.key, state='on', fastforward=1)
                else:
                    RespAmountSlider.run(self.key, state='off', fastforward=1)
                tempSlider.setValue(byteTemp)
                if (byteTemp != 0):
                    RespTempSlider.run(self.key, state='on', fastforward=1)
                else:
                    RespTempSlider.run(self.key, state='off', fastforward=1)
                if boolMayBake:
                    RespMayBake.run(self.key, state='yes', fastforward=1)
                else:
                    RespMayBake.run(self.key, state='no', fastforward=1)
                PtLoadDialog(Vignette.value, self.key)
                if PtIsDialogLoaded(Vignette.value):
                    PtShowDialog(Vignette.value)
        else:
            WasPowered = 0
            virtCam.save(CameraBad.sceneobject.getKey())
            if ((type(VignetteBad.value) != type(None)) and (VignetteBad.value != '')):
                PtLoadDialog(VignetteBad.value, self.key)
                if PtIsDialogLoaded(VignetteBad.value):
                    PtShowDialog(VignetteBad.value)
        PtEnableControlKeyEvents(self.key)


    def IQuitTelescope(self):
        global exitScope
        global Telescope
        global WasPowered
        global timerWheel
        global tempWheel
        global LocalAvatar
        global boolScopeOperator
        exitScope = 1
        Telescope.popTelescope()
        if WasPowered:
            if ((type(Vignette.value) != type(None)) and (Vignette.value != '')):
                PtHideDialog(Vignette.value)
            virtCam = ptCamera()
            virtCam.restore(Camera.sceneobject.getKey())
            timerWheel.setValue(0)
            RespSfxTimerWheel.run(self.key, state='off')
            tempWheel.setValue(0)
        else:
            if ((type(VignetteBad.value) != type(None)) and (VignetteBad.value != '')):
                PtHideDialog(VignetteBad.value)
            virtCam = ptCamera()
            virtCam.restore(CameraBad.sceneobject.getKey())
            WasPowered = 1
        PtRecenterCamera()
        Behavior.nextStage(LocalAvatar)
        PtDisableControlKeyEvents(self.key)
        boolScopeOperator = 0
        self.SDL['boolOperated'] = (0,)
        self.SDL['OperatorID'] = (-1,)
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        PtAtTimeCallback(self.key, 3, 1)
        PtDebugPrint('ercaOvenScope.IQuitTelescope:\tdelaying clickable reenable', level=kDebugDumpLevel)


    def OnTimer(self, id):
        global exitScope
        if (id == 1):
            Activate.enable()
            PtDebugPrint('ercaOvenScope.OnTimer:\tclickable reenabled', level=kDebugDumpLevel)
            PtSendKIMessage(kEnableKIandBB, 0)
        if (id == 2):
            if (not (exitScope)):
                self.IDoTimerWheel()


    def IDoTimerWheel(self):
        global IsBaking
        global byteTime
        global setTempWheel
        global tempWheel
        global byteTemp
        global timerWheel
        print 'in IDoTimerWheel.'
        ageSDL = PtGetAgeSDL()
        if (not (IsBaking)):
            return
        print 'ercaOvenScope:IDoTimerWheel: IsBaking is true'
        StartTime = (IsBaking - (byteTime * kTimeScale))
        FinishTime = IsBaking
        CurTime = PtGetDniTime()
        TimeRemaining = (FinishTime - CurTime)
        BakeDuration = (FinishTime - StartTime)
        PreHeat = (StartTime - 3)
        PostHeat = (StartTime + 2)
        if (CurTime < FinishTime):
            if (PreHeat < CurTime):
                if (PostHeat < CurTime):
                    print 'setTempWheel =',
                    print setTempWheel
                    if (not (setTempWheel)):
                        tempWheel.setValue(byteTemp)
                        setTempWheel = 1
                elif (not (setTempWheel)):
                    tempPercent = (byteTemp * 0.01)
                    tempWheel.animateToPercent(tempPercent)
                    print 'animating Temp Wheel, byteTemp = ',
                    print byteTemp
                    print 'animating Temp Wheel, tempPercent = ',
                    print tempPercent
                    setTempWheel = 1
            if (StartTime < CurTime):
                PtDebugPrint(('ercaOvenScope:IDoTimerWheel:  Now updating timer wheel of scope# %d to %d seconds remaining' % (ScopeNum.value, TimeRemaining)))
                TimeRemaining = (TimeRemaining * 1.0)
                BakeDuration = (BakeDuration * 1.0)
                newTimerVal = ((TimeRemaining / BakeDuration) * (byteTime * 10))
                timerWheel.setValue(newTimerVal)
                RespSfxTimerWheel.run(self.key, state='on')
            else:
                timerWheel.setValue((byteTime * 10))
            PtAtTimeCallback(self.key, 1, 2)


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



