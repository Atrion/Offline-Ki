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
GroupSelector = ptAttribDropDownList(1, 'Group Selector', ('Hub', 'Eng Hut', 'Vogondola', 'Vogondola Throttle', 'Vogondola Reverse', 'Call buttons'))
actHubChairClick = ptAttribActivator(2, 'Hub chair clickable')
behHubChairClimb = ptAttribBehavior(3, 'Hub chair climb beh')
respHubChairLower = ptAttribNamedResponder(4, 'Hub chair lower resp', ['lower', 'raise'])
actVogEjectFront = ptAttribActivator(5, 'Vog eject front click')
actVogEjectRear = ptAttribActivator(6, 'Vog eject rear click')
actVogThrottleF = ptAttribActivator(7, 'Vog throttle forward click')
actVogThrottleB = ptAttribActivator(8, 'Vog throttle back click')
actVogThrottleRevF = ptAttribActivator(9, 'Vog throttle rev forward click')
actVogThrottleRevB = ptAttribActivator(10, 'Vog throttle rev back click')
actVogDirection = ptAttribActivator(11, 'Vog direction click')
actVogDirectionRev = ptAttribActivator(12, 'Vog direction rev click')
respVogChairLower = ptAttribResponder(13, 'Vog chair lower resp')
respVogRotate = ptAttribResponder(14, 'Vog rotate resp', ['back', 'front'])
respVogThrottle = ptAttribResponder(15, 'Vog throttle resp', ['start', 'stop'])
respVogThrottleRev = ptAttribResponder(16, 'Vog throttle rev resp', ['start', 'stop'])
respVogEjectHub = ptAttribResponder(17, 'Vog eject hub resp', ['norotate', 'rotate', 'oneshot'])
respVogEjectEngHut = ptAttribResponder(18, 'Vog eject eng hut resp', ['norotate', 'rotate', 'oneshot'])
soVogDummy = ptAttribSceneobject(19, 'Vog avatar dummy')
soVogSubworld = ptAttribSceneobject(20, 'Vog subworld')
actEngHutChairClick = ptAttribActivator(21, 'Eng Hut chair clickable')
behEngHutChairClimb = ptAttribBehavior(22, 'Eng Hut chair climb beh')
respEngHutChairLower = ptAttribNamedResponder(23, 'Eng Hut chair lower resp', ['lower', 'raise'])
actTubeEndFromHub = ptAttribActivator(24, 'Tube end from hub act')
actTubeEndFromEngHut = ptAttribActivator(25, 'Tube end from eng hut act')
actSailEndToEngHut = ptAttribActivator(26, 'Sail end to eng hut act')
actSailEndToHub = ptAttribActivator(27, 'Sail end to hub act')
actHubRideEnd = ptAttribActivator(28, 'Hub ride end act')
actEngHutRideEnd = ptAttribActivator(29, 'Eng hut ride end act')
respVogRideStart = ptAttribResponder(30, 'Vog ride start resp')
respVogRideStop = ptAttribResponder(31, 'Vog ride stop resp')
respVogRideStartRev = ptAttribResponder(32, 'Vog ride start rev resp')
respVogRideStopRev = ptAttribResponder(33, 'Vog ride stop rev resp')
respVogRideReset = ptAttribResponder(38, 'Vog ride reset resp', ['hub', 'eng hut'])
soEjectPointHub = ptAttribSceneobject(39, 'eject point hub')
soEjectPointEngHut = ptAttribSceneobject(40, 'eject point eng hut')
actCallbuttonHub = ptAttribNamedActivator(41, 'Hub vog call button')
actCallbuttonEngHut = ptAttribNamedActivator(42, 'Eng hut vog call button')
respHubCallbutton = ptAttribNamedResponder(43, 'Hub call button resp')
respEngHutCallbutton = ptAttribNamedResponder(44, 'Eng hut call button resp')
respSounds = ptAttribResponder(45, 'Sound responder', ['hubtubeout', 'hubtubein', 'sailtohub', 'sailtohut', 'huttubeout', 'huttubein', 'stop'])
actStopVogSoundForward = ptAttribActivator(46, 'Vog snd stop forward act')
actStopVogSoundBackward = ptAttribActivator(47, 'Vog snd stop backward act')
actHubChairClick.setVisInfo(1, ['Hub'])
behHubChairClimb.setVisInfo(1, ['Hub'])
respHubChairLower.setVisInfo(1, ['Hub'])
actVogEjectFront.setVisInfo(1, ['Vogondola'])
actVogEjectRear.setVisInfo(1, ['Vogondola'])
actVogThrottleF.setVisInfo(1, ['Vogondola Throttle'])
actVogThrottleB.setVisInfo(1, ['Vogondola Throttle'])
actVogThrottleRevF.setVisInfo(1, ['Vogondola Throttle'])
actVogThrottleRevB.setVisInfo(1, ['Vogondola Throttle'])
respVogThrottle.setVisInfo(1, ['Vogondola Throttle'])
respVogThrottleRev.setVisInfo(1, ['Vogondola Throttle'])
actVogDirection.setVisInfo(1, ['Vogondola Reverse'])
actVogDirectionRev.setVisInfo(1, ['Vogondola Reverse'])
respVogRotate.setVisInfo(1, ['Vogondola Reverse'])
respVogChairLower.setVisInfo(1, ['Vogondola'])
respVogEjectHub.setVisInfo(1, ['Vogondola'])
respVogEjectEngHut.setVisInfo(1, ['Vogondola'])
soVogDummy.setVisInfo(1, ['Vogondola'])
soVogSubworld.setVisInfo(1, ['Vogondola'])
actEngHutChairClick.setVisInfo(1, ['Eng Hut'])
behEngHutChairClimb.setVisInfo(1, ['Eng Hut'])
respEngHutChairLower.setVisInfo(1, ['Eng Hut'])
actTubeEndFromHub.setVisInfo(1, ['Vogondola'])
actTubeEndFromEngHut.setVisInfo(1, ['Vogondola'])
actSailEndToEngHut.setVisInfo(1, ['Vogondola'])
actSailEndToHub.setVisInfo(1, ['Vogondola'])
actHubRideEnd.setVisInfo(1, ['Vogondola'])
actEngHutRideEnd.setVisInfo(1, ['Vogondola'])
respVogRideStart.setVisInfo(1, ['Vogondola'])
respVogRideStop.setVisInfo(1, ['Vogondola'])
respVogRideStartRev.setVisInfo(1, ['Vogondola'])
respVogRideStopRev.setVisInfo(1, ['Vogondola'])
actCallbuttonHub.setVisInfo(1, ['Call buttons'])
actCallbuttonEngHut.setVisInfo(1, ['Call buttons'])
respHubCallbutton.setVisInfo(1, ['Call buttons'])
respEngHutCallbutton.setVisInfo(1, ['Call buttons'])
respVogRideReset.setVisInfo(1, ['Vogondola'])
soEjectPointHub.setVisInfo(1, ['Vogondola'])
soEjectPointEngHut.setVisInfo(1, ['Vogondola'])
respSounds.setVisInfo(1, ['Vogondola'])
actStopVogSoundForward.setVisInfo(1, ['Vogondola'])
actStopVogSoundBackward.setVisInfo(1, ['Vogondola'])
##############################################################################
# D'Lanor's Ahnonay fixes follow.
##############################################################################
#make avatar global so it can be remembered
theAvatar = None 

def DisableVogControls(enabledControlList):
    disableControlList = [actVogEjectFront, actVogEjectRear, actVogThrottleF, actVogThrottleB, actVogThrottleRevF, actVogThrottleRevB, actVogDirection, actVogDirectionRev]
    if (type(enabledControlList) == type([])):
        for control in enabledControlList:
            disableControlList.remove(control)
            control.enable()
    for control in disableControlList:
        control.disable()


class InHubBrain:


    def __init__(self, parent):
        self.parent = parent
        self.name = 'In Hub Brain'
        print 'initing',
        print self.name
        #PtDisableMovementKeys() #we'll do this later on
        enabledControlList = [actVogEjectFront, actVogEjectRear, actVogThrottleB]
        if (self.parent.direction == 1):
            enabledControlList.append(actVogDirection)
        elif (self.parent.direction == -1):
            enabledControlList.append(actVogDirectionRev)
        DisableVogControls(enabledControlList)


    def OnNotify(self, state, id, events):
        global theAvatar
        #no avatar? trying to find one
        if (type(theAvatar) == type(None)):
            theAvatar = PtFindAvatar(events)
            #did we find an avatar?
            if (type(theAvatar) != type(None)):
                print (self.name + ': avatar found')
            else:
                PtDebugPrint('DEBUG In Hub Brain: No avatar found for id=%d, setting to local' % id)
                theAvatar = PtGetLocalAvatar()
        if ((id == actHubChairClick.id) and state):
            print 'disabling clickable on all chairs and buttons'
            actCallbuttonHub.disable()
            actCallbuttonEngHut.disable()
            actHubChairClick.disable()
            actEngHutChairClick.disable()
            #avatar = PtFindAvatar(events) #skipping: we already have an avatar
            behHubChairClimb.run(theAvatar)
        elif (id == behHubChairClimb.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    respHubChairLower.run(self.parent.key, events=events, state='lower')
                    print (self.name + ': finished smart-seek')
                elif ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                    #theAvatar = PtGetLocalAvatar() #using found avatar instead
                    #if (PtWasLocallyNotified(self.parent.key)): #does not work
                    if (theAvatar == PtGetLocalAvatar()):
                        PtDisableMovementKeys()
                        print (self.name + ': disabling local avatar movement')
                    theAvatar.physics.warpObj(soVogDummy.value.getKey())
                    PtAttachObject(theAvatar.getKey(), soVogDummy.value.getKey())
                    theAvatar.avatar.enterSubWorld(soVogSubworld.value)
                    print (self.name + ': pinned avatar')
                    respVogChairLower.run(self.parent.key, events=events)
        elif ((id == actVogDirection.id) and state):
            actVogDirection.disable()
            actVogThrottleB.disable()
            self.parent.direction = -1
            respVogRotate.run(self.parent.key, state='back')
            actVogDirectionRev.enable()
        elif ((id == actVogDirectionRev.id) and state):
            actVogDirectionRev.disable()
            self.parent.direction = 1
            respVogRotate.run(self.parent.key, state='front')
            actVogThrottleB.enable()
            actVogDirection.enable()
        elif ((id == actVogEjectFront.id) and state):
            DisableVogControls(None)
            respVogEjectHub.run(self.parent.key, state='norotate')
        elif ((id == actVogEjectRear.id) and state):
            DisableVogControls(None)
            respVogEjectHub.run(self.parent.key, state='rotate')
        elif ((id == actVogThrottleB.id) and state):
            DisableVogControls(None)
            respVogRideStart.run(self.parent.key)
            sdl = PtGetAgeSDL()
            sdl['ahnyVogLocation'] = (1,)
        elif (id == respVogRideStart.id):
            if (theAvatar != PtGetLocalAvatar()):
                print 'Other player notification: not running respSounds'
                return
            print 'running respSounds: state - hubtubeout loc - hub brain respvogridestart'
            respSounds.run(self.parent.key, state='hubtubeout')
        elif (id == actTubeEndFromHub.id):
            respVogRideStop.run(self.parent.key)
            self.parent.currentBrain = HubSailTubeTransitionBrain(self.parent)
            self.parent.direction = 1
        elif (id == respVogEjectHub.id):
            #theAvatar = PtGetLocalAvatar() #using found avatar instead
            respHubChairLower.run(self.parent.key, avatar=theAvatar, state='raise')
            PtDetachObject(theAvatar.getKey(), soVogDummy.value.getKey())
            theAvatar.avatar.exitSubWorld()
            theAvatar.physics.warpObj(soEjectPointHub.value.getKey())
            respVogEjectHub.run(self.parent.key, avatar=theAvatar, state='oneshot')
            self.parent.currentBrain = None
            PtEnableMovementKeys()
            print 'ejecting finished in vog at hub...setting current brain to none'
            #doing some extra stuff
            theAvatar = None
            print 'avatar set to None'
            actCallbuttonHub.disable()
            actCallbuttonEngHut.enable()
            actHubChairClick.enable()
            actEngHutChairClick.disable()
            print 'clickable on chair and button enabled'



class HubSailTubeTransitionBrain:


    def __init__(self, parent):
        self.parent = parent
        self.name = 'Hub Sail Tube Transition Brain'
        print 'initing',
        print self.name
        enabledControlList = [actVogThrottleB, actVogThrottleRevB]
        if (self.parent.direction == 1):
            enabledControlList.append(actVogDirection)
        elif (self.parent.direction == -1):
            enabledControlList.append(actVogDirectionRev)
        DisableVogControls(enabledControlList)


    def OnNotify(self, state, id, events):
        global theAvatar
        if ((id == actVogDirection.id) and state):
            actVogDirection.disable()
            actVogThrottleB.disable()
            self.parent.direction = -1
            respVogRotate.run(self.parent.key, state='back')
            actVogThrottleRevB.enable()
            actVogDirectionRev.enable()
        elif ((id == actVogDirectionRev.id) and state):
            actVogDirectionRev.disable()
            actVogThrottleRevB.disable()
            self.parent.direction = 1
            respVogRotate.run(self.parent.key, state='front')
            actVogThrottleB.enable()
            actVogDirection.enable()
        elif ((id == actVogThrottleB.id) and state):
            respVogRideStart.run(self.parent.key)
            self.parent.currentBrain = SailingBrain(self.parent)
            self.parent.direction = 1
        elif ((id == actVogThrottleRevB.id) and state):
            DisableVogControls(None)
            respVogRideStartRev.run(self.parent.key)
            sdl = PtGetAgeSDL()
            sdl['ahnyVogLocation'] = (0,)
        elif (id == respVogRideStartRev.id):
            if (theAvatar != PtGetLocalAvatar()):
                print 'Other player notification: not running respSounds'
                return
            print 'running respSounds: state - hubtubein loc - hubtransistion respvogridestartrev'
            respSounds.run(self.parent.key, state='hubtubein')
        elif (id == actHubRideEnd.id):
            respVogThrottle.run(self.parent.key, state='stop')
            self.parent.currentBrain = InHubBrain(self.parent)



class SailingBrain:


    def __init__(self, parent):
        self.parent = parent
        self.name = 'Sailing Brain'
        print 'initing',
        print self.name
        enabledControlList = None
        if (self.parent.direction == 1):
            enabledControlList = [actVogThrottleF]
        elif (self.parent.direction == -1):
            enabledControlList = [actVogThrottleRevF]
        DisableVogControls(enabledControlList)


    def OnNotify(self, state, id, events):
        global theAvatar
        if (((id == actVogThrottleF.id) or (id == actVogThrottleRevF.id)) and state):
            respVogRideStop.run(self.parent.key)
            enabledControlList = None
            if (self.parent.direction == 1):
                enabledControlList = [actVogThrottleB, actVogDirection]
            elif (self.parent.direction == -1):
                enabledControlList = [actVogThrottleRevB, actVogDirectionRev]
            DisableVogControls(enabledControlList)
        elif ((id == respVogRideStop.id) or (id == respVogRideStopRev.id)):
            if (theAvatar != PtGetLocalAvatar()):
                print 'Other player notification: not running respSounds'
                return
            print 'vog ride stop notify'
            respSounds.run(self.parent.key, state='stop')
        elif ((id == actVogDirection.id) and state):
            actVogDirection.disable()
            actVogThrottleB.disable()
            self.parent.direction = -1
            respVogRotate.run(self.parent.key, state='back')
            actVogThrottleRevB.enable()
            actVogDirectionRev.enable()
        elif ((id == actVogDirectionRev.id) and state):
            actVogDirectionRev.disable()
            actVogThrottleRevB.disable()
            self.parent.direction = 1
            respVogRotate.run(self.parent.key, state='front')
            actVogThrottleB.enable()
            actVogDirection.enable()
        elif ((id == actVogThrottleB.id) and state):
            DisableVogControls([actVogThrottleF])
            respVogRideStart.run(self.parent.key)
        elif ((id == actVogThrottleRevB.id) and state):
            DisableVogControls([actVogThrottleRevF])
            respVogRideStartRev.run(self.parent.key)
        elif (id == respVogRideStart.id):
            if (theAvatar != PtGetLocalAvatar()):
                print 'Other player notification: not running respSounds'
                return
            print 'running respSounds: state - sailtohut loc - sail brain vogridestart'
            respSounds.run(self.parent.key, state='sailtohut')
        elif (id == respVogRideStartRev.id):
            if (theAvatar != PtGetLocalAvatar()):
                print 'Other player notification: not running respSounds'
                return
            print 'running respSounds: state - sailtohub loc - sail brain vogridestartrev'
            respSounds.run(self.parent.key, state='sailtohub')
        elif ((id == actSailEndToEngHut.id) and (self.parent.direction == 1)):
            respVogRideStop.run(self.parent.key)
            self.parent.currentBrain = EngHutSailTubeTransitionBrain(self.parent)
        elif ((id == actSailEndToHub.id) and (self.parent.direction == -1)):
            respVogRideStop.run(self.parent.key)
            self.parent.currentBrain = HubSailTubeTransitionBrain(self.parent)



class EngHutSailTubeTransitionBrain:


    def __init__(self, parent):
        self.parent = parent
        self.name = 'Eng Hut Sail Tube Transition Brain'
        print 'initing',
        print self.name
        enabledControlList = [actVogThrottleB, actVogThrottleRevB]
        if (self.parent.direction == 1):
            enabledControlList.append(actVogDirection)
        elif (self.parent.direction == -1):
            enabledControlList.append(actVogDirectionRev)
        DisableVogControls(enabledControlList)


    def OnNotify(self, state, id, events):
        global theAvatar
        if ((id == actVogDirection.id) and state):
            actVogDirection.disable()
            actVogThrottleB.disable()
            self.parent.direction = -1
            respVogRotate.run(self.parent.key, state='back')
            actVogThrottleRevB.enable()
            actVogDirectionRev.enable()
        elif ((id == actVogDirectionRev.id) and state):
            actVogDirectionRev.disable()
            actVogThrottleRevB.disable()
            self.parent.direction = 1
            respVogRotate.run(self.parent.key, state='front')
            actVogThrottleB.enable()
            actVogDirection.enable()
        elif ((id == actVogThrottleRevB.id) and state):
            respVogRideStartRev.run(self.parent.key)
            self.parent.currentBrain = SailingBrain(self.parent)
            self.parent.direction = -1
        elif ((id == actVogThrottleB.id) and state):
            DisableVogControls(None)
            respVogRideStart.run(self.parent.key)
            sdl = PtGetAgeSDL()
            sdl['ahnyVogLocation'] = (2,)
        elif (id == respVogRideStart.id):
            if (theAvatar != PtGetLocalAvatar()):
                print 'Other player notification: not running respSounds'
                return
            print 'running respSounds: state - huttubein loc - hut transition vogridestart'
            respSounds.run(self.parent.key, state='huttubein')
        elif (id == actEngHutRideEnd.id):
            respVogThrottle.run(self.parent.key, state='stop')
            self.parent.currentBrain = InEngHutBrain(self.parent)



class InEngHutBrain:


    def __init__(self, parent):
        self.parent = parent
        self.name = 'In Eng Hut Brain'
        print 'initing',
        print self.name
        #PtDisableMovementKeys() #we'll do this later on
        enabledControlList = [actVogEjectFront, actVogEjectRear, actVogThrottleRevB]
        if (self.parent.direction == 1):
            enabledControlList.append(actVogDirection)
        elif (self.parent.direction == -1):
            enabledControlList.append(actVogDirectionRev)
        DisableVogControls(enabledControlList)


    def OnNotify(self, state, id, events):
        global theAvatar
        #no avatar? trying to find one
        if (type(theAvatar) == type(None)):
            theAvatar = PtFindAvatar(events)
            #did we find an avatar?
            if (type(theAvatar) != type(None)):
                print (self.name + ': avatar found')
            else:
                PtDebugPrint('DEBUG In Eng Hut Brain: No avatar found for id=%d, setting to local' % id)
                theAvatar = PtGetLocalAvatar()
        if ((id == actEngHutChairClick.id) and state):
            print 'disabling clickable on all chairs and buttons'
            actCallbuttonHub.disable()
            actCallbuttonEngHut.disable()
            actHubChairClick.disable()
            actEngHutChairClick.disable()
            #avatar = PtFindAvatar(events) #skipping: we already have an avatar
            behEngHutChairClimb.run(theAvatar)
        elif (id == behEngHutChairClimb.id):
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    respEngHutChairLower.run(self.parent.key, events=events, state='lower')
                    print (self.name + ': finished smart-seek')
                elif ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                    #theAvatar = PtGetLocalAvatar() #using found avatar instead
                    #if (PtWasLocallyNotified(self.parent.key)): #does not work
                    if (theAvatar == PtGetLocalAvatar()):
                        PtDisableMovementKeys()
                        print (self.name + ': disabling local avatar movement')
                    theAvatar.physics.warpObj(soVogDummy.value.getKey())
                    PtAttachObject(theAvatar.getKey(), soVogDummy.value.getKey())
                    theAvatar.avatar.enterSubWorld(soVogSubworld.value)
                    print (self.name + ': pinned avatar')
                    respVogChairLower.run(self.parent.key, events=events)
        elif ((id == actVogDirection.id) and state):
            actVogDirection.disable()
            self.parent.direction = -1
            respVogRotate.run(self.parent.key, state='back')
            actVogThrottleRevB.enable()
            actVogDirectionRev.enable()
        elif ((id == actVogDirectionRev.id) and state):
            actVogDirectionRev.disable()
            actVogThrottleRevB.disable()
            self.parent.direction = 1
            respVogRotate.run(self.parent.key, state='front')
            actVogDirection.enable()
        elif ((id == actVogEjectFront.id) and state):
            DisableVogControls(None)
            respVogEjectEngHut.run(self.parent.key, state='norotate')
            #theAvatar = PtGetLocalAvatar #skipping: going to use found avatar later
        elif ((id == actVogEjectRear.id) and state):
            DisableVogControls(None)
            respVogEjectEngHut.run(self.parent.key, state='rotate')
        elif ((id == actVogThrottleRevB.id) and state):
            DisableVogControls(None)
            respVogRideStartRev.run(self.parent.key)
            sdl = PtGetAgeSDL()
            sdl['ahnyVogLocation'] = (1,)
        elif (id == respVogRideStartRev.id):
            if (theAvatar != PtGetLocalAvatar()):
                print 'Other player notification: not running respSounds'
                return
            print 'running respSounds: huttubeout - stop loc - hut brain vogridestartrev'
            respSounds.run(self.parent.key, state='huttubeout')
        elif (id == actTubeEndFromEngHut.id):
            respVogRideStop.run(self.parent.key)
            self.parent.currentBrain = EngHutSailTubeTransitionBrain(self.parent)
            self.parent.direction = -1
        elif (id == respVogEjectEngHut.id):
            #theAvatar = PtGetLocalAvatar() #using found avatar instead
            respEngHutChairLower.run(self.parent.key, avatar=theAvatar, state='raise')
            PtDetachObject(theAvatar.getKey(), soVogDummy.value.getKey())
            theAvatar.avatar.exitSubWorld()
            theAvatar.physics.warpObj(soEjectPointEngHut.value.getKey())
            respVogEjectEngHut.run(self.parent.key, avatar=theAvatar, state='oneshot')
            self.parent.currentBrain = None
            PtEnableMovementKeys()
            print 'ejecting finished in vog at eng hut...setting current brain to none'
            #doing some extra stuff
            theAvatar = None
            print 'avatar set to None'
            actCallbuttonHub.enable()
            actCallbuttonEngHut.disable()
            actHubChairClick.disable()
            actEngHutChairClick.enable()
            print 'clickable on chair and button enabled'


class ahnyVogondolaRideV2(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5338
        self.version = 2
        self.currentBrain = None
        self.direction = 1
        self.throttle = 0


    def OnServerInitComplete(self):
        actCallbuttonHub.disable()
        actCallbuttonEngHut.disable()
        actHubChairClick.disable()
        actEngHutChairClick.disable()
        PtAtTimeCallback(self.key, 0, 1)


    def OnTimer(self, id):
        if (id == 1):
            print 'timer id 1 returned'
            sdl = PtGetAgeSDL()
            vogLoc = sdl['ahnyVogLocation'][0]
            if (vogLoc == 0):
                actCallbuttonEngHut.enable()
                actHubChairClick.enable()
            elif (vogLoc == 1):
                actCallbuttonEngHut.enable()
                actCallbuttonHub.enable()
                respHubChairLower.run(self.key, state='lower', fastforward=1)
            elif (vogLoc == 2):
                actCallbuttonHub.enable()
                actEngHutChairClick.enable()
                respEngHutChairLower.run(self.key, state='raise', fastforward=1)
                respHubChairLower.run(self.key, state='lower', fastforward=1)
                respVogRideStart.run(self.key, fastforward=1)
                respVogThrottle.run(self.key, state='stop', fastforward=1)
        elif (id == 2):
            print 'timer id 2 returned...run responder'
            respHubChairLower.run(self.key, state='raise')
        elif (id == 3):
            print 'timer id 3 returned...run responder'
            respEngHutChairLower.run(self.key, state='raise')


    def OnNotify(self, state, id, events):
        global theAvatar
        if ((id == actHubChairClick.id) and state):
            cam = ptCamera()
            cam.undoFirstPerson()
            cam.disableFirstPersonOverride()
            respVogRideReset.run(self.key, state='hub', fastforward=1)
            self.direction = 1
            self.currentBrain = InHubBrain(self)
            self.currentBrain.OnNotify(state, id, events)
        elif ((id == actEngHutChairClick.id) and state):
            cam = ptCamera()
            cam.undoFirstPerson()
            cam.disableFirstPersonOverride()
            respVogRideReset.run(self.key, state='eng hut', fastforward=1)
            self.direction = 1
            self.currentBrain = InEngHutBrain(self)
            self.currentBrain.OnNotify(state, id, events)
        elif ((id == actCallbuttonHub.id) and state):
            print 'call button hub clicked'
            actCallbuttonHub.disable()
            #actCallbuttonEngHut added for multiplayer compatibility
            actCallbuttonEngHut.enable()
            respHubCallbutton.run(self.key, events=events)
            respEngHutChairLower.run(self.key, state='lower', fastforward=1)
            sdl = PtGetAgeSDL()
            sdl['ahnyVogLocation'] = (0,)
        elif (id == respHubCallbutton.id):
            print 'call button hub returned'
            PtAtTimeCallback(self.key, 5, 2)
        elif ((id == actCallbuttonEngHut.id) and state):
            print 'call button hut clicked'
            actCallbuttonEngHut.disable()
            #actCallbuttonHub added for multiplayer compatibility
            actCallbuttonHub.enable()
            respEngHutCallbutton.run(self.key, events=events)
            respHubChairLower.run(self.key, state='lower', fastforward=1)
            sdl = PtGetAgeSDL()
            sdl['ahnyVogLocation'] = (2,)
        elif (id == respEngHutCallbutton.id):
            print 'call button hut returned'
            PtAtTimeCallback(self.key, 5, 3)
        elif ((id == respHubChairLower.id) and (self.currentBrain == None)):
            actHubChairClick.enable()
            #actEngHutChairClick added for multiplayer compatibility
            actEngHutChairClick.disable()
            cam = ptCamera()
            cam.enableFirstPersonOverride()
        elif ((id == respEngHutChairLower.id) and (self.currentBrain == None)):
            actEngHutChairClick.enable()
            #actHubChairClick added for multiplayer compatibility
            actHubChairClick.disable()
            cam = ptCamera()
            cam.enableFirstPersonOverride()
        elif (((id == actStopVogSoundForward.id) or (id == actStopVogSoundBackward.id)) and state):
            actStopVogSoundForward.disable()
            actStopVogSoundBackward.disable()
            #if (not PtWasLocallyNotified(self.key)): #does not work
            if (theAvatar != PtGetLocalAvatar()):
                print 'Other player notification: not running respSounds'
                return
            print 'running respSounds: state - stop loc - anim event det',
            print id,
            print state
            respSounds.run(self.key, state='stop')
        elif (self.currentBrain != None):
            self.currentBrain.OnNotify(state, id, events)


    def OnBackdoorMsg(self, target, param):
        global theAvatar
        print 'Look mummy, a backdoor message!'
        if (target == 'vog'):
            if (param == 'currentbrain'):
                if (self.currentBrain == None):
                    print 'Vog Current Brain: None'
                else:
                    print 'Vog Current Brain:',
                    print self.currentBrain.name
            elif (param == 'beh'):
                if (type(theAvatar) == type(None)):
                    PtDebugPrint('DEBUG OnBackdoorMsg: No avatar set, default to local')
                    theAvatar = PtGetLocalAvatar()
##############################################################################
# End D'Lanor's Ahnonay fixes.
##############################################################################


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



