# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import string
import PlasmaControlKeys
import xEnum
from math import *
from xPsnlVaultSDL import *
import time
SDLPellet1 = ptAttribString(1, 'SDL: pellet 1')
SDLPellet2 = ptAttribString(2, 'SDL: pellet 2')
SDLPellet3 = ptAttribString(3, 'SDL: pellet 3')
SDLPellet4 = ptAttribString(4, 'SDL: pellet 4')
SDLPellet5 = ptAttribString(5, 'SDL: pellet 5')
SDLMachine = ptAttribString(6, 'SDL: big ol\' pellet machine')
ActUseMachine = ptAttribActivator(7, 'clk: use big machine btn')
RespUseMachine = ptAttribResponder(8, 'resp: use machine btn')
RespMachineEnable = ptAttribResponder(9, 'resp: machine enable/disable', ['Enable', 'Disable', 'IfOpening'])
RespMachineMode = ptAttribResponder(10, 'resp: machine open/close', ['Open', 'Close'])
ActSpitPellet = ptAttribActivator(11, 'clk: spit next pellet')
SDLChamber = ptAttribString(12, 'SDL: pellet machine chamber')
RespUseSpitBtn = ptAttribResponder(13, 'resp: use spit pellet btn')
RespRotateChamber = ptAttribResponder(14, 'resp: rotate pellet chamber', ['Chamber1', 'Chamber2', 'Chamber3', 'Chamber4', 'Chamber5'])
RespSpitPellet = ptAttribResponder(15, 'resp: spit out the pellet', ['Chamber1', 'Chamber2', 'Chamber3', 'Chamber4', 'Chamber5'])
RespDropPellet = ptAttribResponder(16, 'resp: drop the pellet')
RespShowAllPellets = ptAttribResponder(17, 'resp: show all pellets')
RespHidePellet = ptAttribResponder(18, 'resp: hide pellet', ['pellet1', 'pellet2', 'pellet3', 'pellet4', 'pellet5'])
ActTakePellet = ptAttribActivator(19, 'clk: take a pellet')
RespTouchPellet = ptAttribResponder(20, 'resp: touch pellet', ['Touch', 'Untouch'])
ActFlushLever = ptAttribActivator(21, 'clk: flush lever')
RespFlushOneShot = ptAttribResponder(22, 'resp: flush lever oneshot')
RespFlushLever = ptAttribResponder(23, 'resp: use flush lever')
SDLFlush = ptAttribString(24, 'SDL: flush lever')
RespFlushAPellet = ptAttribResponder(25, 'resp: flush a pellet', ['flush1', 'flush2', 'flush3', 'flush4', 'flush5'])
ActPelletToSilo = ptAttribActivator(26, 'clk: link to silo w/pellet')
ActPelletToCave = ptAttribActivator(27, 'clk: link to cave w/pellet')
RespLinkPellet = ptAttribResponder(28, 'resp: link w/pellet', ['CitySilo', 'BahroCave'])
MltStgLinkPellet = ptAttribBehavior(29, 'mlt stg: link w/pellet')
Pellet1 = 0
Pellet2 = 0
Pellet3 = 0
Pellet4 = 0
Pellet5 = 0
PelletReady = 0
boolMachine = 0
byteChamber = 0
TakePellet = 0
boolFlush = 0
MayFlush = 0
Toucher = None

class ercaPelletRoom(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 7033
        self.version = 9


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        global Pellet1
        global Pellet2
        global Pellet3
        global Pellet4
        global Pellet5
        global boolMachine
        global byteChamber
        global boolFlush
        global pelletList
        global PelletReady
        global MayFlush
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(SDLPellet1.value, 1, 1)
        ageSDL.sendToClients(SDLPellet1.value)
        ageSDL.setFlags(SDLPellet2.value, 1, 1)
        ageSDL.sendToClients(SDLPellet2.value)
        ageSDL.setFlags(SDLPellet3.value, 1, 1)
        ageSDL.sendToClients(SDLPellet3.value)
        ageSDL.setFlags(SDLPellet4.value, 1, 1)
        ageSDL.sendToClients(SDLPellet4.value)
        ageSDL.setFlags(SDLPellet5.value, 1, 1)
        ageSDL.sendToClients(SDLPellet5.value)
        ageSDL.setFlags(SDLMachine.value, 1, 1)
        ageSDL.sendToClients(SDLMachine.value)
        ageSDL.setFlags(SDLChamber.value, 1, 1)
        ageSDL.sendToClients(SDLChamber.value)
        ageSDL.setFlags(SDLFlush.value, 1, 1)
        ageSDL.sendToClients(SDLFlush.value)
        try:
            ageSDL = PtGetAgeSDL()
        except:
            print 'ercaBakePellet.OnServerInitComplete():\tERROR---Cannot find the Ercana Age SDL'
            ageSDL[SDLPellet1.value] = (0,)
            ageSDL[SDLPellet2.value] = (0,)
            ageSDL[SDLPellet3.value] = (0,)
            ageSDL[SDLPellet4.value] = (0,)
            ageSDL[SDLPellet5.value] = (0,)
            ageSDL[SDLMachine.value] = (0,)
            ageSDL[SDLChamber.value] = (1,)
            ageSDL[SDLFlush.value] = (0,)
        ageSDL.setNotify(self.key, SDLPellet1.value, 0.0)
        ageSDL.setNotify(self.key, SDLPellet2.value, 0.0)
        ageSDL.setNotify(self.key, SDLPellet3.value, 0.0)
        ageSDL.setNotify(self.key, SDLPellet4.value, 0.0)
        ageSDL.setNotify(self.key, SDLPellet5.value, 0.0)
        ageSDL.setNotify(self.key, SDLMachine.value, 0.0)
        ageSDL.setNotify(self.key, SDLChamber.value, 0.0)
        ageSDL.setNotify(self.key, SDLFlush.value, 0.0)
        Pellet1 = ageSDL[SDLPellet1.value][0]
        if (Pellet1 == 0):
            RespHidePellet.run(self.key, state='pellet1')
        Pellet2 = ageSDL[SDLPellet2.value][0]
        if (Pellet2 == 0):
            RespHidePellet.run(self.key, state='pellet2')
        Pellet3 = ageSDL[SDLPellet3.value][0]
        if (Pellet3 == 0):
            RespHidePellet.run(self.key, state='pellet3')
        Pellet4 = ageSDL[SDLPellet4.value][0]
        if (Pellet4 == 0):
            RespHidePellet.run(self.key, state='pellet4')
        Pellet5 = ageSDL[SDLPellet5.value][0]
        if (Pellet5 == 0):
            RespHidePellet.run(self.key, state='pellet5')
        boolMachine = ageSDL[SDLMachine.value][0]
        byteChamber = ageSDL[SDLChamber.value][0]
        boolFlush = ageSDL[SDLFlush.value][0]
        pelletList = [Pellet1, Pellet2, Pellet3, Pellet4, Pellet5]
        for pellet in pelletList:
            if (pellet > 0):
                PelletReady = 1
                break
        print 'PelletReady = ',
        print PelletReady
        if PelletReady:
            if boolMachine:
                MayFlush = 1
                RespMachineMode.run(self.key, state='Open', fastforward=1)
                RespMachineEnable.run(self.key, state='IfOpening')
                if (byteChamber == 1):
                    RespRotateChamber.run(self.key, state='Chamber1', fastforward=1)
                elif (byteChamber == 2):
                    RespRotateChamber.run(self.key, state='Chamber2', fastforward=1)
                elif (byteChamber == 3):
                    RespRotateChamber.run(self.key, state='Chamber3', fastforward=1)
                elif (byteChamber == 4):
                    RespRotateChamber.run(self.key, state='Chamber4', fastforward=1)
                elif (byteChamber == 5):
                    RespRotateChamber.run(self.key, state='Chamber5', fastforward=1)
                ActSpitPellet.enableActivator()
            else:
                MayFlush = 0
                RespMachineMode.run(self.key, state='Close', fastforward=1)
                RespMachineEnable.run(self.key, state='Enable')
        else:
            RespMachineEnable.run(self.key, state='Disable')
            MayFlush = 0
            if boolMachine:
                print 'We shouldn\'t get here.  Just in case some states got hosed.'
                RespMachineMode.run(self.key, state='Close', fastforward=1)
                boolMachine = 0
                ageSDL[SDLMachine.value] = (0,)
                byteChamber = 0
                ageSDL[SDLChamber.value] = (0,)
            else:
                RespMachineMode.run(self.key, state='Close', fastforward=1)
                byteChamber = 0
                ageSDL[SDLChamber.value] = (0,)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global Pellet1
        global Pellet2
        global Pellet3
        global Pellet4
        global Pellet5
        global boolMachine
        global MayFlush
        global byteChamber
        global boolFlush
        global pelletList
        global PelletReady
        ageSDL = PtGetAgeSDL()
        pelletUpdate = 0
        if (VARname == SDLPellet1.value):
            Pellet1 = ageSDL[SDLPellet1.value][0]
            pelletUpdate = 1
        if (VARname == SDLPellet2.value):
            Pellet2 = ageSDL[SDLPellet2.value][0]
            pelletUpdate = 1
        if (VARname == SDLPellet3.value):
            Pellet3 = ageSDL[SDLPellet3.value][0]
            pelletUpdate = 1
        if (VARname == SDLPellet4.value):
            Pellet4 = ageSDL[SDLPellet4.value][0]
            pelletUpdate = 1
        if (VARname == SDLPellet5.value):
            Pellet5 = ageSDL[SDLPellet5.value][0]
            pelletUpdate = 1
        if (VARname == SDLMachine.value):
            boolMachine = ageSDL[SDLMachine.value][0]
            PtDebugPrint(('ercaBakePellets:OnSDLNotify:  SDL for BigMachine is now %d' % boolMachine))
            pelletUpdate = 0
            if boolMachine:
                RespShowAllPellets.run(self.key)
##############################################################################
# Attempt to fix button slurp - method 1
##############################################################################
# comment out following code
#                objAvatar = ptSceneobject(PtGetAvatarKeyFromClientID(playerID), self.key)
#                print 'Got boolMachine SDL = 1 notify, will now run RespUseMachine'
#                RespUseMachine.run(self.key, avatar=objAvatar)
##############################################################################
# End attempt to fix button slurp.
##############################################################################
            else:
                MayFlush = 0
                RespMachineMode.run(self.key, state='Close')
        if (VARname == SDLChamber.value):
            byteChamber = ageSDL[SDLChamber.value][0]
            if (byteChamber != 0):
                PtDebugPrint(('ercaBakePellets:OnSDLNotify:  SDL for machine chamber is now %d' % byteChamber))
##############################################################################
# Attempt to fix button slurp - method 1
##############################################################################
# comment out following code
#                print ' Got byteChamber change, running RespUseSPitBtn'
                pelletUpdate = 0
#                objAvatar = ptSceneobject(PtGetAvatarKeyFromClientID(playerID), self.key)
#                RespUseSpitBtn.run(self.key, avatar=objAvatar)
##############################################################################
# End attempt to fix button slurp.
##############################################################################
        if (VARname == SDLFlush.value):
            boolFlush = ageSDL[SDLFlush.value][0]
            PtDebugPrint(('ercaBakePellets:OnSDLNotify:  SDL for flush lever is now %d' % boolFlush))
            if boolFlush:
                ActSpitPellet.disableActivator()
##############################################################################
# Attempt to fix button slurp - method 1
##############################################################################
# comment out following code
#                objAvatar = ptSceneobject(PtGetAvatarKeyFromClientID(playerID), self.key)
#                print 'Got boolFlush SDL = 1 notify, will now run RespFlushOneShot'
#                RespFlushOneShot.run(self.key, avatar=objAvatar)
##############################################################################
# End attempt to fix button slurp.
##############################################################################
        if pelletUpdate:
            pelletList = [Pellet1, Pellet2, Pellet3, Pellet4, Pellet5]
            testVal = 0
            for pellet in pelletList:
                if (pellet > 0):
                    if boolMachine:
                        MayFlush = 1
                    testVal = 1
                    break
##############################################################################
# Fix funny-lookin' bug
##############################################################################
#            if ((testVal == 1) and (PelletReady == 1)):
            if ((testVal == 1) and (PelletReady == 1) and boolMachine):
##############################################################################
# End fix funny-lookin' bug.
##############################################################################
                ActSpitPellet.enableActivator()
            elif ((testVal == 1) and (PelletReady == 0)):
                PelletReady = 1
                RespMachineEnable.run(self.key, state='Enable')
            elif ((testVal == 0) and (PelletReady == 1)):
                PelletReady = 0
                ageSDL[SDLMachine.value] = (0,)


    def OnNotify(self, state, id, events):
        global MayFlush
        global byteChamber
        global TakePellet
        global Toucher
        global Pellet1
        global Pellet2
        global Pellet3
        global Pellet4
        global Pellet5
        ageSDL = PtGetAgeSDL()
        if ((id == ActUseMachine.id) and state):
##############################################################################
# Attempt to fix button slurp - method 1
##############################################################################
            if (PtWasLocallyNotified(self.key)):
                PtDebugPrint('OnNotify: You touched the machine button')
                ageSDL[SDLMachine.value] = (1,)
            else:
                PtDebugPrint('OnNotify: Someone else touched the machine button')
            RespUseMachine.run(self.key, avatar=PtFindAvatar(events))
##############################################################################
# End attempt to fix button slurp.
##############################################################################
        if (id == RespUseMachine.id):
            print 'Got notify from RespUseMachine, will now open machine'
            RespMachineEnable.run(self.key, state='IfOpening')
            RespMachineMode.run(self.key, state='Open')
        if (id == RespMachineMode.id):
            print 'ercaPelletRoom.OnNotify:  Machine has closed.'
            RespMachineEnable.run(self.key, state='Disable')
            ageSDL[SDLChamber.value] = (0,)
        if (id == RespMachineEnable.id):
            MayFlush = 1
        if ((id == ActSpitPellet.id) and state):
            ActSpitPellet.disableActivator()
            MayFlush = 0
            if (byteChamber == 5):
                print 'Trying to spit pellet, but we\'re on Chamber5.  This shouldn\'t be possible.'
                return
            newVal = (byteChamber + 1)
##############################################################################
# Attempt to fix button slurp - method 1
##############################################################################
            if (PtWasLocallyNotified(self.key)):
                PtDebugPrint('OnNotify: You touched the spit button')
                ageSDL[SDLChamber.value] = (newVal,)
            else:
                PtDebugPrint('OnNotify: Someone else touched the spit button')
            RespUseSpitBtn.run(self.key, avatar=PtFindAvatar(events))
##############################################################################
# End attempt to fix button slurp.
##############################################################################
        if (id == RespUseSpitBtn.id):
            if (byteChamber == 1):
                RespRotateChamber.run(self.key, state='Chamber1')
            elif (byteChamber == 2):
                RespRotateChamber.run(self.key, state='Chamber2')
            elif (byteChamber == 3):
                RespRotateChamber.run(self.key, state='Chamber3')
            elif (byteChamber == 4):
                RespRotateChamber.run(self.key, state='Chamber4')
            elif (byteChamber == 5):
                RespRotateChamber.run(self.key, state='Chamber5')
        if (id == RespRotateChamber.id):
            if (byteChamber == 1):
                RespSpitPellet.run(self.key, state='Chamber1')
            elif (byteChamber == 2):
                RespSpitPellet.run(self.key, state='Chamber2')
            elif (byteChamber == 3):
                RespSpitPellet.run(self.key, state='Chamber3')
            elif (byteChamber == 4):
                RespSpitPellet.run(self.key, state='Chamber4')
            elif (byteChamber == 5):
                RespSpitPellet.run(self.key, state='Chamber5')
        if (id == RespSpitPellet.id):
            TakePellet = 0
            ActTakePellet.enableActivator()
            PtAtTimeCallback(self.key, 10, 1)
        if ((id == ActTakePellet.id) and state):
            ActTakePellet.disableActivator()
            TakePellet = 1
##############################################################################
# Don't link everyone in the age.
##############################################################################
#            cam = ptCamera()
#            cam.disableFirstPersonOverride()
#            cam.undoFirstPerson()
#            RespTouchPellet.run(self.key, state='Touch')
#            Toucher = PtFindAvatar(events)
#            MltStgLinkPellet.run(Toucher)
#            PtEnableControlKeyEvents(self.key)
            if (PtWasLocallyNotified(self.key)):
                cam = ptCamera()
                cam.disableFirstPersonOverride()
                cam.undoFirstPerson()
            RespTouchPellet.run(self.key, state='Touch')
            Toucher = PtFindAvatar(events)
            MltStgLinkPellet.run(Toucher)
            if (PtWasLocallyNotified(self.key)):
                PtEnableControlKeyEvents(self.key)
##############################################################################
# End don't link everyone in the age.
##############################################################################
        if (id == RespTouchPellet.id):
            print 'RespTouchPellet callback for Untouch, will now try to kill multistage'
            MltStgLinkPellet.gotoStage(Toucher, -1)
##############################################################################
# Fix activator bug.
##############################################################################
            # yikes!!! the spit button gets enabled
            # We shouldn't enable the button if it's a normal Untouch but
            # we must let it be enabled it if it's an Untouch *after* the
            # pellet dropped.
            if (byteChamber == 1 and Pellet1 != 0) or (byteChamber == 2 and Pellet2 != 0) or (byteChamber == 3 and Pellet3 != 0) or (byteChamber == 4 and Pellet4 != 0) or (byteChamber == 5 and Pellet5 != 0):
                print 'pellet untouched, disabling spit activator'
                ActSpitPellet.disableActivator()
##############################################################################
# End fix activator bug.
##############################################################################
##############################################################################
# Don't link everyone in the age.
##############################################################################
            if Toucher != PtGetLocalAvatar():
                return
##############################################################################
# End don't link everyone in the age.
##############################################################################
            cam = ptCamera()
            cam.enableFirstPersonOverride()
        if ((id == ActPelletToSilo.id) and state):
            TakePellet = 2
            MltStgLinkPellet.gotoStage(Toucher, 1, dirFlag=1, isForward=1)
##############################################################################
# Don't link everyone in the age.
##############################################################################
            if Toucher != PtGetLocalAvatar():
                return
##############################################################################
# End don't link everyone in the age.
##############################################################################
            PtAtTimeCallback(self.key, 0.59999999999999998, 3)
        if ((id == ActPelletToCave.id) and state):
            TakePellet = 2
            MltStgLinkPellet.gotoStage(Toucher, 2, dirFlag=1, isForward=1)
##############################################################################
# Don't link everyone in the age.
##############################################################################
            if Toucher != PtGetLocalAvatar():
                return
##############################################################################
# End don't link everyone in the age.
##############################################################################
            PtAtTimeCallback(self.key, 0.59999999999999998, 4)
        if (id == RespLinkPellet.id):
            Recipe = 0
            if (byteChamber == 1):
                Recipe = Pellet1
                ageSDL[SDLPellet1.value] = (0,)
            elif (byteChamber == 2):
                Recipe = Pellet2
                ageSDL[SDLPellet2.value] = (0,)
            elif (byteChamber == 3):
                Recipe = Pellet3
                ageSDL[SDLPellet3.value] = (0,)
            elif (byteChamber == 4):
                Recipe = Pellet4
                ageSDL[SDLPellet4.value] = (0,)
            elif (byteChamber == 5):
                Recipe = Pellet5
                ageSDL[SDLPellet5.value] = (0,)
##############################################################################
# Don't link everyone in the age.
##############################################################################
            if Toucher != PtGetLocalAvatar():
##############################################################################
# Attempt to fix post-link weirdness.
##############################################################################
                # hmm... will this clean up the weirdness?
                #RespDropPellet.run(self.key, fastforward=1)
                PtAtTimeCallback(self.key, 0.5, 6)
##############################################################################
# End attempt to fix post-link weirdness.
##############################################################################
##############################################################################
# Fix activator bug.
##############################################################################
                ActFlushLever.enableActivator()
##############################################################################
# End fix activator bug.
##############################################################################
                return
##############################################################################
# End don't link everyone in the age.
##############################################################################
            cam = ptCamera()
            cam.enableFirstPersonOverride()
            vault = ptVault()
            entry = vault.findChronicleEntry('GotPellet')
            if (type(entry) != type(None)):
                entry.chronicleSetValue(('%d' % Recipe))
                entry.save()
                PtDebugPrint('Chronicle entry GotPellet already added, setting to Recipe value')
            else:
                vault.addChronicleEntry('GotPellet', 1, ('%d' % Recipe))
                PtDebugPrint('Chronicle entry GotPellet not present, adding entry and setting to Recipe value')
        if (id == RespDropPellet.id):
##############################################################################
# Fix funny-lookin' bug II.
##############################################################################
            # this line should not be run when the chamber is empty
#            ActSpitPellet.enableActivator()
            if (byteChamber < 5):
                ActSpitPellet.enableActivator()
##############################################################################
# End fix funny-lookin' bug II.
##############################################################################
            if (byteChamber == 1):
                ageSDL[SDLPellet1.value] = (0,)
            elif (byteChamber == 2):
                ageSDL[SDLPellet2.value] = (0,)
            elif (byteChamber == 3):
                ageSDL[SDLPellet3.value] = (0,)
            elif (byteChamber == 4):
                ageSDL[SDLPellet4.value] = (0,)
            elif (byteChamber == 5):
                ageSDL[SDLPellet5.value] = (0,)
        if ((id == ActFlushLever.id) and state):
##############################################################################
# Attempt to fix button slurp - method 1
##############################################################################
            if (PtWasLocallyNotified(self.key)):
                PtDebugPrint('OnNotify: You touched the flush button')
                ageSDL[SDLFlush.value] = (1,)
            else:
                PtDebugPrint('OnNotify: Somebody else touched the flush button')
            RespFlushOneShot.run(self.key, avatar=PtFindAvatar(events))
##############################################################################
# End attempt to fix button slurp.
##############################################################################
        if (id == RespFlushOneShot.id):
            RespFlushLever.run(self.key)
        if (id == RespFlushLever.id):
            if MayFlush:
                MayFlush = 0
                self.IFlushPellets()
            else:
                ageSDL[SDLFlush.value] = (0,)


    def OnControlKeyEvent(self, controlKey, activeFlag):
        global TakePellet
        global Toucher
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            if (TakePellet == 1):
                TakePellet = 0
                ActTakePellet.enableActivator()
                PtDisableControlKeyEvents(self.key)
                MltStgLinkPellet.gotoStage(Toucher, 0, newTime=1.2, dirFlag=1, isForward=0)
                PtAtTimeCallback(self.key, 0.80000000000000004, 5)
        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
            if (TakePellet == 1):
                TakePellet = 0
                ActTakePellet.enableActivator()
                PtDisableControlKeyEvents(self.key)
                MltStgLinkPellet.gotoStage(Toucher, 0, newTime=1.2, dirFlag=1, isForward=0)
                PtAtTimeCallback(self.key, 0.80000000000000004, 5)


    def OnTimer(self, id):
        global TakePellet
        global Toucher
        ageSDL = PtGetAgeSDL()
        if (id == 1):
            if (TakePellet != 2):
                ActTakePellet.disableActivator()
                RespDropPellet.run(self.key)
                if (TakePellet == 1):
                    TakePellet = 0
                    print 'onTimer, TakePellet = 1'
                    MltStgLinkPellet.gotoStage(Toucher, 0, newTime=1.2, dirFlag=1, isForward=0)
                    PtAtTimeCallback(self.key, 0.80000000000000004, 5)
        elif (id == 2):
            print 'OnTimer.Is taking a pellet reseting it\'s SDL to O???'
            ActSpitPellet.enableActivator()
        elif (id == 3):
            RespLinkPellet.run(self.key, avatar=Toucher, state='CitySilo')
        elif (id == 4):
            RespLinkPellet.run(self.key, avatar=Toucher, state='BahroCave')
        elif (id == 5):
            RespTouchPellet.run(self.key, state='Untouch')
##############################################################################
# Attempt to fix post-link weirdness.
##############################################################################
        elif (id == 6):
            RespDropPellet.run(self.key, fastforward=1)
##############################################################################
# End attempt to fix post-link weirdness.
##############################################################################


    def IFlushPellets(self):
        global Pellet1
        global Pellet2
        global Pellet3
        global Pellet4
        global Pellet5
        print 'in IFlushPellets.'
        ageSDL = PtGetAgeSDL()
        ageSDL[SDLFlush.value] = (0,)
        ActSpitPellet.disableActivator()
        if (Pellet1 != 0):
            RespFlushAPellet.run(self.key, state='flush1')
            ageSDL[SDLPellet1.value] = (0,)
        if (Pellet2 != 0):
            RespFlushAPellet.run(self.key, state='flush2')
            ageSDL[SDLPellet2.value] = (0,)
        if (Pellet3 != 0):
            RespFlushAPellet.run(self.key, state='flush3')
            ageSDL[SDLPellet3.value] = (0,)
        if (Pellet4 != 0):
            RespFlushAPellet.run(self.key, state='flush4')
            ageSDL[SDLPellet4.value] = (0,)
        if (Pellet5 != 0):
            RespFlushAPellet.run(self.key, state='flush5')
            ageSDL[SDLPellet5.value] = (0,)


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



