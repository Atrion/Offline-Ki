# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#    See the file AUTHORS for more info about the contributors.                #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                      #
#                                                                              #
#    You may re-use the code in this file within the context of Uru.           #
#                                                                              #
#==============================================================================#
### GLOBALS
global isClimbing
global LocalAvatar
global waiting
global usingEast
global action
global direction
global AvatarPos
global lastKey
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
climbBehaviorW      = ptAttribBehavior       ( 1, 'The climbing animations 1', netForce=1)
climbBehaviorE      = ptAttribBehavior       ( 2, 'The climbing animations 2', netForce=1)
# regions
actClimbTriggerW    = ptAttribActivator      ( 3, 'Climb trigger 1')
actClimbTriggerE    = ptAttribActivator      ( 4, 'Climb trigger 2')
# blockers (working, thanks to Chacal for his help !)
actBlockers         = ptAttribActivatorList  ( 5, 'All blockers') # not set. Will add it once climbing works properly.
# the Nexus release region (works as blockers, but it won't have an anim)
actNexus            = ptAttribActivator      ( 6, 'Nexus release region')
# the object holding the display script
soDisplay           = ptAttribSceneobject    ( 7, 'Display script sceneobject')

##### VARIABLES #####
# direction and action used
direction = ClimbDirection()
action    = ClimbAction()
# key checking
lastKey = -1
# other variables
gridMaxX = 40
gridMaxY = 38
isClimbing     = False
LocalAvatar    = None
waiting        = False
usingEast      = False # used to know which behavior we're using.
AvatarPos      = [0, 0]
#script
DisplayScript = None
# Will return the probe stage associated to the key.
StageFromDir = {direction.up:     8,
                direction.down:   9,
                direction.left:  10,
                direction.right: 11}
restrictedArea = ( ### Might slow down the computer, will add new way to do it.
                 # left side
                 (0,23),
                 (1,23),
                 (2,22),
                 (2,21),
                 (3,20),
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
##### VARIABLES #####

#########################
##### Climb  stages ######
# 0:  mount up          #
# 1:  mont down         #
# 2:  mount left        #
# 3:  mount right       #
# 4:  dismount up       #
# 5:  dismount down     #
# 6:  dismount left     #
# 7:  dismount right    #
# 8:  up                #
# 9:  down              #
# 10: left              #
# 11: right             #
# 12: fall off          #
# 13: release           #
# 14: idle              #
# 15: climb up bugfix              #
# 16: climb down bugfix              #
# 17: climb left bugfix              #
# 18: climb right bugfix              #
#########################

class grsnWallClimb(ptResponder):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 3125
        self.version = 1
        print ("grsnWallClimb.__init__: version %d" % self.version)


    def OnServerInitComplete(self):
        """Prepare for Age exploring.
First, check if that's not a Fan-Age using the wrong script.
Second, get the script we'll send blocker event to."""
        global DisplayScript
        if (PtGetAgeName() != "Garrison"):
            raise NameError, 'This script is supposed to be used only in Garrison !'
        pythonScripts = soDisplay.value.getPythonMods()
        for script in pythonScripts:
            if (script.getName() == "cPythonBigWallDisplay"):
                DisplayScript = script


    def OnNotify(self, state, id, events):
        """Manages input from regions, behaviors, etc."""
        global LocalAvatar
        global usingEast
        global AvatarPos
        if (id == actClimbTriggerW.id):
            if (not (state)):
                return
            print "Message from West climb trigger"
            if PtWasLocallyNotified(self.key): # if it comes from our player
                LocalAvatar = PtFindAvatar(events)
                if PtGetLocalAvatar() != LocalAvatar:
                    return
                if (not isClimbing): # if he is not climbing
                    for event in events:
                        if (event[0] == kCollisionEvent):
                            if event[1]: # if we're entering
                                usingEast = False
                                print "Using West"
                                AvatarPos[0] = 22
                                AvatarPos[1] = 0
                                self.Climb(action.mount, direction.up) # then mount up
                                return
                else:
                    return
        elif (id == actClimbTriggerE.id):
            if (not (state)):
                return
            print "Message from East climb trigger"
            if PtWasLocallyNotified(self.key): # if it comes from our player
                LocalAvatar = PtFindAvatar(events)
                if PtGetLocalAvatar() != LocalAvatar:
                    return
                if (not isClimbing): # if he is not climbing
                    for event in events:
                        if (event[0] == kCollisionEvent):
                            if event[1]: # if we're entering
                                usingEast = True
                                print "Using East"
                                AvatarPos[0] = 18
                                AvatarPos[1] = 0
                                self.Climb(action.mount, direction.up) # then mount up
                                return
                else:
                    return
        elif (id == actNexus.id):
            if PtWasLocallyNotified(self.key):
                if PtGetLocalAvatar() != LocalAvatar:
                    return
                if isClimbing:
                    for event in events:
                        if (event[0] == kCollisionEvent):
                            print "Releasing Avatar..."
                            self.Climb(action.release, None)
                            return
        elif (id == actBlockers.id):
            if PtWasLocallyNotified(self.key): # if it comes from our player
                if PtGetLocalAvatar() != LocalAvatar:
                    return
                if isClimbing:
                    for event in events:
                        if (event[0] == kCollisionEvent):
                            blocker = event[3].getName() # blocker name
                            self.SendBlocker(blocker)
                            self.Climb(action.fallOff, None)
                            return
        elif ((id == climbBehaviorE.id) or (id == climbBehaviorW.id)):
            for event in events:
                if ((event[0] == 10) and (event[2] == kAdvanceNextStage)):
                    if (PtFindAvatar(events) == PtGetLocalAvatar()):
                        if (event[1] in (  range(0, 4) + range(8, 12) + range(15, 19)  )): # if the last stage was in climbing stage (added range 15-19: this is the bugfix for the head)
                            if lastKey != -1:
                                self.Climb(action.probe, lastKey)
                            else:
                                self.Climb(action.idle, None)


    def OnControlKeyEvent(self, controlKey, activeFlag):
        """Receives control keys and store them.
If we're waiting, then it will call self.Climb"""
        global lastKey
        if (controlKey == PlasmaControlKeys.kKeyMoveForward):
            if (activeFlag):
                lastKey = direction.up
                if (waiting):
                    self.Climb(action.probe, lastKey)
            elif (lastKey == direction.up):
                lastKey = -1
        elif (controlKey == PlasmaControlKeys.kKeyMoveBackward):
            if (activeFlag):
                lastKey = direction.down
                if (waiting):
                    self.Climb(action.probe, lastKey)
            elif (lastKey == direction.down):
                lastKey = -1
        elif (controlKey == PlasmaControlKeys.kKeyRotateLeft):
            if (activeFlag):
                lastKey = direction.left
                if (waiting):
                    self.Climb(action.probe, lastKey)
            elif (lastKey == direction.left):
                lastKey = -1
        elif (controlKey == PlasmaControlKeys.kKeyRotateRight):
            if (activeFlag):
                lastKey = direction.right
                if (waiting):
                    self.Climb(action.probe, lastKey)
            elif (lastKey == direction.right):
                lastKey = -1
        elif ((controlKey == PlasmaControlKeys.kKeyExitMode) or (controlKey == PlasmaControlKeys.kKeyJump)):
            self.Climb(action.fallOff, None)


    def Climb(self, cbAction, cbDirection):
        """Manages any kind of climbing action"""
        global waiting
        global isClimbing
        global usingEast
        global AvatarPos
        global LocalAvatar
        global lastKey
        if (cbAction == action.probe):
            if ((cbDirection == direction.down) and (AvatarPos[1] == 0)):
                self.Climb(action.dismount, cbDirection)
                return
            elif self.isGoingFarther(cbDirection):
                waiting = False
                if usingEast:
                    climbBehaviorE.gotoStage(LocalAvatar, StageFromDir[cbDirection])
                else:
                    climbBehaviorW.gotoStage(LocalAvatar, StageFromDir[cbDirection])
            else:
                waiting = True
        elif (cbAction == action.mount):
            print "Entering climbing brain."
            waiting = False
            isClimbing = True
            if usingEast:
                climbBehaviorE.run(LocalAvatar) # must use run and not gotoStage, unfortunately.
            else:
                climbBehaviorW.run(LocalAvatar)
            PtEnableControlKeyEvents(self.key)
        elif (cbAction == action.dismount):
            print "Exiting climbing brain."
            PtDisableControlKeyEvents(self.key)
            waiting = False
            isClimbing = False
            if usingEast:
                usingEast = False
                climbBehaviorE.gotoStage(LocalAvatar, (StageFromDir[cbDirection] - 4))
            else:
                climbBehaviorW.gotoStage(LocalAvatar, (StageFromDir[cbDirection] - 4))
            LocalAvatar = None
            AvatarPos[0] = 0
            AvatarPos[1] = 0
            lastKey = -1
        elif ((cbAction == action.fallOff) or (cbAction == action.release)):
            print "Falling from Wall."
            PtDisableControlKeyEvents(self.key)
            waiting = False
            isClimbing = False
            if usingEast:
                usingEast = False
                climbBehaviorE.gotoStage(LocalAvatar, -1)
            else:
                climbBehaviorW.gotoStage(LocalAvatar, -1)
            LocalAvatar = None
            AvatarPos[0] = 0
            AvatarPos[1] = 0
            lastKey = -1
        elif (cbAction == action.idle):
            waiting = True
            if usingEast:
                climbBehaviorE.gotoStage(LocalAvatar, 14)
            else:
                climbBehaviorW.gotoStage(LocalAvatar, 14)


    def isGoingFarther(self, fDirection):
        """Checks if the avatar can go in the specified direction.
If true, then the avatar pos is updated and it returns true.
Else it will only return false."""
        global AvatarPos
        tmpPos = [0, 0]
        tmpPos[0], tmpPos[1] = AvatarPos[0], AvatarPos[1]
        if (fDirection == direction.up):
            tmpPos[1] += 1
            if (tmpPos[1] <= gridMaxY):
                if (not (tuple(tmpPos) in restrictedArea)):
                    AvatarPos[1] += 1
                    return True
        if (fDirection == direction.down):
            tmpPos[1] -= 1
            if (tmpPos[1] >= 0):
                if (not (tuple(tmpPos) in restrictedArea)):
                    AvatarPos[1] -= 1
                    return True
        if (fDirection == direction.right):
            tmpPos[0] += 1
            if (tmpPos[0] <= gridMaxX):
                if (not (tuple(tmpPos) in restrictedArea)):
                    AvatarPos[0] += 1
                    return True
        if (fDirection == direction.left):
            tmpPos[0] -= 1
            if (tmpPos[0] >= 0):
                if (not (tuple(tmpPos) in restrictedArea)):
                    AvatarPos[0] -= 1
                    return True
        return False


    def SendBlocker(self, name):
        """Will send a blocker event to display script"""
        global DisplayScript
        if (DisplayScript):
            print "Sending blocker named ", name
            note = ptNotify(self.key)
            note.clearReceivers()
            note.addReceiver(DisplayScript)
            note.netPropagate(0)
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

