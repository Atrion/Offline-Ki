# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2004-2011  The Offline KI contributors                      #
#    See the file AUTHORS for more info about the contributors (including      #
#    contact information)                                                      #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    Please see the file COPYING for the full GPLv3 license, or see            #
#    <http://www.gnu.org/licenses/>                                            #
#                                                                              #
#    Uru exception: In addition, this file may be used in combination with     #
#    (non-GPL) code within the context of Uru.                                 #
#                                                                              #
#==============================================================================#
### GLOBALS
global isClimbing
global waiting
global usingEast
global AvatarPos
global lastKey
global jump
# script
global DisplayScript

# glue
global glue_cl
global glue_inst
global glue_params
global glue_paramKeys

### IMPORTS
from Plasma import *
from PlasmaTypes import *
from grsnClimbTypes import *
import PlasmaControlKeys

##### PythonFileMode Vars #####
# behaviors
climbBehaviorW      = ptAttribBehavior       (1, 'The climbing animations 1', netForce=1)
climbBehaviorE      = ptAttribBehavior       (2, 'The climbing animations 2', netForce=1)
# regions
actClimbTriggerW    = ptAttribActivator      (3, 'Climb trigger 1')
actClimbTriggerE    = ptAttribActivator      (4, 'Climb trigger 2')
# blockers
actBlockers         = ptAttribActivatorList  (5, 'All blockers')
# the Nexus release region
actNexus            = ptAttribActivator      (6, 'Nexus release region')
# the sceneobject holding the display script
soDisplay           = ptAttribSceneobject    (7, 'Display script sceneobject')

##### VARIABLES #####
# check keys
lastKey = -1
# grid size
gridMaxX = 40
gridMaxY = 38
# are we climbing ?
isClimbing     = False
# are we waiting the end of an anim ?
waiting        = False
# used behavior
usingEast      = False
# avatar position on the Wall
AvatarPos      = [0, 0]
# script for blockers layeranim
DisplayScript = None
# can jump from Wall
jump = False

# Will return the climb stage associated to the key.
StageFromDir = {direction.up:     8,
                direction.down:   9,
                direction.left:  10,
                direction.right: 11}

# All the coordinates of places you can't go on the Wall
# (can't find a better way to do it, but at least it is seamless)
restrictedArea = (
                 # left side
                 (0,23),
                 (1,23),
                 (2,22),
                 (2,21),
                 (3,20),
                 (3,19),
                 (3,18),
                 (3,17),
                 (3,16),
                 (3,15),
                 (3,14),
                 (3,13),
                 (3,12),
                 (3,11),
                 (3,10),
                 (3,9),
                 (3,8),
                 (2,7),
                 (1,6),
                 (0,5),
                 (1,4),
                 (2,4),
                 (3,4),
                 (4,4),
                 (5,4),
                 (6,4),
                 (7,4),
                 (8,4),
                 (9,4),
                 (10,3),
                 (11,2),
                 (12,2),
                 (13,1),
                 (14,0),
                 # right side
                 (26,0),
                 (27,1),
                 (28,2),
                 (29,2),
                 (30,3),
                 (31,4),
                 (32,4),
                 (33,4),
                 (34,4),
                 (35,4),
                 (36,4),
                 (37,4),
                 (38,4),
                 (39,4),
                 (40,5),
                 (39,6),
                 (38,7),
                 (37,8),
                 (37,9),
                 (37,10),
                 (37,11),
                 (37,12),
                 (37,13),
                 (37,14),
                 (37,15),
                 (37,16),
                 (37,17),
                 (37,18),
                 (37,19),
                 (37,20),
                 (38,21),
                 (38,22),
                 (39,23),
                 (40,23),
                 #top link region
                 (17,38),
                 (18,38),
                 (19,38),
                 (20,38),
                 (21,38),
                 (22,38),
                 (23,38),
                 (18,37),
                 (19,37),
                 (20,37),
                 (21,37),
                 (22,37),
                 (18,36),
                 (19,36),
                 (20,36),
                 (21,36),
                 (22,36)
                 )
##### /VARIABLES #####

##########################
##### Climb  stages ######
#                        #
# 0:  mount up           #
# 1:  mont down          #
# 2:  mount left         #
# 3:  mount right        #
# 4:  dismount up        #
# 5:  dismount down      #
# 6:  dismount left      #
# 7:  dismount right     #
# 8:  up                 #
# 9:  down               #
# 10: left               #
# 11: right              #
# 12: fall off           #
# 13: release            #
# 14: idle               #
# 15: up bugfix          #
# 16: down bugfix        #
# 17: left bugfix        #
# 18: right bugfix       #
##########################

class grsnWallClimb(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 3125
        self.version = 1
        print ("grsnWallClimb.__init__: version %d" % self.version)


    def OnServerInitComplete(self):
        """Prepare for Age exploring:
Get the script we'll send blocker event to."""
        global DisplayScript
        if (PtGetAgeName() != "Garrison"):
            raise NameError, 'This script is supposed to be used only in Garrison !'
        pythonScripts = soDisplay.value.getPythonMods()
        for script in pythonScripts:
            if (script.getName() == "cPythonBigWallDisplay"):
                DisplayScript = script


    def BeginAgeUnLoad(self, avatar):
        try: localavatar = PtGetLocalAvatar()
        except:
            print "grsnWallClimb: player quit. I'm not bothering with releasing him"
            return
        if avatar == localavatar:
            if isClimbing:
                print "grsnWallClimb: avatar seems to have linked out, so stop climbing to prevent errors."
                self.Climb(action.release, None)


    def OnNotify(self, state, id, events):
        """Manages input from regions, behaviors, etc."""
        global usingEast
        global AvatarPos
        global jump
        avatar = PtFindAvatar(events)
        if (avatar != PtGetLocalAvatar()): # every messages must come from the local player.
            return
        if (not PtWasLocallyNotified(self.key)): # every message must come from the local client
            return
        if (id == actClimbTriggerW.id):
            if (not (state)):
                return
            print "grsnWallClimb: Local avatar uses West climb trigger"
            if (not isClimbing): # if we are not climbing
                for event in events:
                    if (event[0] == kCollisionEvent):
                        if event[1]: # if we're entering the region
                            usingEast = False
                            AvatarPos = [22, 0]
                            self.Climb(action.mount, direction.up) # then mount up
                            return
        elif (id == actClimbTriggerE.id):
            if (not (state)):
                return
            print "grsnWallClimb: Local avatar uses East climb trigger"
            if (not isClimbing): # if we are not climbing
                for event in events:
                    if (event[0] == kCollisionEvent):
                        if event[1]: # if we're entering the region
                            usingEast = True
                            AvatarPos = [18, 0]
                            self.Climb(action.mount, direction.up) # then mount up
                            return
        elif (id == actNexus.id): # in case we're in the Nexus: dismount and go back to idle brain
            if isClimbing:
                for event in events:
                    if (event[0] == kCollisionEvent):
                        print "grsnWallClimb: Releasing Avatar..."
                        self.Climb(action.release, None)
                        return
        elif (id == actBlockers.id): # in case we hit a blocker: send the layer anim to the display script, dismount and go back to idle brain
            if isClimbing:
                for event in events:
                    if (event[0] == kCollisionEvent):
                        blocker = event[3].getName() # get the name of the blocker
                        self.SendBlocker(blocker) # ...so we can send it to the display script to run the layer anim
                        self.Climb(action.fallOff, None) # and then fall
                        return
        elif ((id == climbBehaviorE.id) or (id == climbBehaviorW.id)):
            for event in events:
                if ((event[0] == 10) and (event[2] == kAdvanceNextStage)):
                    if (event[1] in (  range(8, 12) + range(15, 19)  )): # if the last stage was a climb stage (added range 15-19: this is the bugfix for the avatar's head)
                        if lastKey != -1:
                            self.Climb(action.climb, lastKey)
                        else:
                            self.Climb(action.idle, None)
                    elif (event[1] in range(0, 4)):
                        jump = True
                        if lastKey != -1:
                            self.Climb(action.climb, lastKey)
                        else:
                            self.Climb(action.idle, None)


    def OnControlKeyEvent(self, controlKey, activeFlag):
        """Receives control keys and store them.
If the avatar is not actually going anywhere (waiting), then it will call self.Climb"""
        global lastKey
        global jump
        if (controlKey == PlasmaControlKeys.kKeyMoveForward):
            if (activeFlag):
                lastKey = direction.up
                if (waiting):
                    self.Climb(action.climb, lastKey)
            elif (lastKey == direction.up):
                lastKey = -1
        elif (controlKey == PlasmaControlKeys.kKeyMoveBackward):
            if (activeFlag):
                lastKey = direction.down
                if (waiting):
                    self.Climb(action.climb, lastKey)
            elif (lastKey == direction.down):
                lastKey = -1
        elif (controlKey == PlasmaControlKeys.kKeyRotateLeft):
            if (activeFlag):
                lastKey = direction.left
                if (waiting):
                    self.Climb(action.climb, lastKey)
            elif (lastKey == direction.left):
                lastKey = -1
        elif (controlKey == PlasmaControlKeys.kKeyRotateRight):
            if (activeFlag):
                lastKey = direction.right
                if (waiting):
                    self.Climb(action.climb, lastKey)
            elif (lastKey == direction.right):
                lastKey = -1
        elif ((controlKey == PlasmaControlKeys.kKeyExitMode) or (controlKey == PlasmaControlKeys.kKeyJump)):
            if (activeFlag and jump):
                self.Climb(action.fallOff, None)


    def Climb(self, cbAction, cbDirection):
        """Manages any kind of climbing action"""
        global waiting
        global isClimbing
        global usingEast
        global AvatarPos
        global lastKey
        global jump
        print "grsnWallClimb: Climbing action %s in direction %s" % (cbAction,cbDirection)
        LocalAvatar = PtGetLocalAvatar()
        LocalAvatar.avatar.setReplyKey(self.key) # make sure the behavior information go to us
        if (cbAction == action.climb):
            if ((cbDirection == direction.down) and (AvatarPos[1] == 0)):
                # we're at the lower part of the Wall, we must dismount
                self.Climb(action.dismount, cbDirection)
                return
            elif self.canIGoFarther(cbDirection):
                self.updatePos(cbDirection)
                waiting = False
                if usingEast:
                    climbBehaviorE.gotoStage(LocalAvatar, StageFromDir[cbDirection])
                else:
                    climbBehaviorW.gotoStage(LocalAvatar, StageFromDir[cbDirection])
            else:
                waiting = True
        elif (cbAction == action.mount):
            print "grsnWallClimb: Entering climbing brain."
            waiting = False
            isClimbing = True
            if usingEast:
                climbBehaviorE.run(LocalAvatar)
            else:
                climbBehaviorW.run(LocalAvatar)
            PtEnableControlKeyEvents(self.key)
        elif (cbAction == action.dismount):
            print "grsnWallClimb: Exiting climbing brain."
            PtDisableControlKeyEvents(self.key)
            waiting = False
            isClimbing = False
            if usingEast:
                usingEast = False
                climbBehaviorE.gotoStage(LocalAvatar, (StageFromDir[cbDirection] - 4))
            else:
                climbBehaviorW.gotoStage(LocalAvatar, (StageFromDir[cbDirection] - 4))
            AvatarPos = [0, 0]
            lastKey = -1
            jump = False
        elif ((cbAction == action.fallOff) or (cbAction == action.release)):
            print "grsnWallClimb: Falling from Wall."
            PtDisableControlKeyEvents(self.key)
            waiting = False
            isClimbing = False
            if usingEast:
                usingEast = False
                climbBehaviorE.gotoStage(LocalAvatar, -1)
            else:
                climbBehaviorW.gotoStage(LocalAvatar, -1)
            AvatarPos = [0, 0]
            lastKey = -1
            jump = False
        elif (cbAction == action.idle):
            waiting = True
            if usingEast:
                climbBehaviorE.gotoStage(LocalAvatar, 14)
            else:
                climbBehaviorW.gotoStage(LocalAvatar, 14)


    def canIGoFarther(self, fDirection):
        """Checks if the avatar can go in the specified direction"""
        global AvatarPos
        tmpPos = [0, 0]
        tmpPos[0], tmpPos[1] = AvatarPos[0], AvatarPos[1]
        if (fDirection == direction.up):
            tmpPos[1] += 1
            if (tmpPos[1] <= gridMaxY):
                if (not (tuple(tmpPos) in restrictedArea)):
                    return True
        if (fDirection == direction.down):
            tmpPos[1] -= 1
            if (tmpPos[1] >= 0):
                if (not (tuple(tmpPos) in restrictedArea)):
                    return True
        if (fDirection == direction.right):
            tmpPos[0] += 1
            if (tmpPos[0] <= gridMaxX):
                if (not (tuple(tmpPos) in restrictedArea)):
                    return True
        if (fDirection == direction.left):
            tmpPos[0] -= 1
            if (tmpPos[0] >= 0):
                if (not (tuple(tmpPos) in restrictedArea)):
                    return True
        print "grsnWallClimb: Can't go in direction %s" % (fDirection)
        return False


    def updatePos(self, fDirection):
        """Updates the position of the avatar"""
        global AvatarPos
        if (fDirection == direction.up):
            AvatarPos[1] += 1
        if (fDirection == direction.down):
            AvatarPos[1] -= 1
        if (fDirection == direction.right):
            AvatarPos[0] += 1
        if (fDirection == direction.left):
            AvatarPos[0] -= 1
        print "grsnWallClimb: Now avatar pos =", AvatarPos


    def SendBlocker(self, name):
        """Will send a blocker event to display script"""
        global DisplayScript
        if (DisplayScript):
            print "Sending blocker named", name
            note = ptNotify(self.key)
            note.clearReceivers()
            note.addReceiver(DisplayScript)
            note.netPropagate(1) # send it to every client so that everyone can see the layer anim
            note.netForce(0)
            note.setActivate(1.0)
            note.addVarNumber(name.lower(), 1.0)
            note.send()


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

