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
import cPickle
northWall = ptAttribSceneobjectList(1, 'North Wall Decals', byObject=1)
southWall = ptAttribSceneobjectList(2, 'South Wall Decals', byObject=1)
northBlocker = ptAttribSceneobjectList(3, 'North Wall Blockers', byObject=1)
southBlocker = ptAttribSceneobjectList(4, 'South Wall Blockers', byObject=1)
NorthBlockers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
SouthBlockers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
ReceiveInit = false
NorthState = ptClimbingWallMsgState.kWaiting
SouthState = ptClimbingWallMsgState.kWaiting
kTeamLightsOn = 0
kTeamLightsOff = 1
kTeamLightsBlink = 2
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

class grsnMainWallPython(ptResponder):


    def __init__(self):
        PtDebugPrint('grsnMainWallPython::init begin')
        ptResponder.__init__(self)
        self.id = 52394
        self.version = 1
        PtDebugPrint('grsnMainWallPython::init end')


    def OnServerInitComplete(self):
        global ReceiveInit
        PtDebugPrint('grsnWallPython::OnServerInitComplete')
        solo = true
        if len(PtGetPlayerList()): # used to make sure we don't link-in while a game is playing
            solo = false
            ReceiveInit = true
            return
        else:
            print 'solo in climbing wall'


    def OnClimbingBlockerEvent(self, blocker):
        print 'looking for blocker named ',
        print blocker.getName()
        i = 0
        while ((i < 171)):
            if (northBlocker.value[i] == blocker):
                northWall.value[i].runAttachedResponder(kTeamLightsBlink)
                print 'found matching texture named ',
                print northWall.value[i].getName()
                return
            elif (southBlocker.value[i] == blocker):
                southWall.value[i].runAttachedResponder(kTeamLightsBlink)
                print 'found matching texture named ',
                print southWall.value[i].getName()
                return
            i = (i + 1)


    def OnClimbingWallInit(self, type, state, value):
        global ReceiveInit
        global SouthState
        global NorthState
        global SouthBlockers
        global NorthBlockers
        print 'grsnMainClimbingWall::OnClimbingWallInit type ',
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
            if ((SouthState == ptClimbingWallMsgState.kSouthWin) or ((NorthState == ptClimbingWallMsgState.kNorthWin) or ((NorthState == ptClimbingWallMsgState.kNorthQuit) or (SouthState == ptClimbingWallMsgState.kSouthQuit)))):
                i = 0
                while ((i < 20)):
                    value = SouthBlockers[i]
                    if (value > -1):
                        southWall.value[value].runAttachedResponder(kTeamLightsOn)
                        print 'drawing s wall index',
                        print value
                    value = NorthBlockers[i]
                    if (value > -1):
                        northWall.value[value].runAttachedResponder(kTeamLightsOn)
                        print 'drawing n wall index',
                        print value
                    i = (i + 1)
        if (type == ptClimbingWallMsgType.kTotalGameState):
            SouthState = state
            NorthState = value
            print 'begin receiving total game state'
        elif ((type == ptClimbingWallMsgType.kAddBlocker) and (state > 0)):
            self.SetWallIndex(state, true, value)


    def OnClimbingWallEvent(self, type, state, value):
        global NorthState
        global SouthState
        global SouthBlockers
        global NorthBlockers
        print 'grsnMainClimbingWall::OnClimbingWallInit type ',
        print type,
        print ' state ',
        print state,
        print ' value ',
        print value
        if (type == ptClimbingWallMsgType.kNewState):
            if (value == 1):
                NorthState = state
            else:
                SouthState = state
            if ((state == ptClimbingWallMsgState.kSouthWin) or ((state == ptClimbingWallMsgState.kNorthWin) or ((state == ptClimbingWallMsgState.kNorthQuit) or (state == ptClimbingWallMsgState.kSouthQuit)))):
                i = 0
                while ((i < 20)):
                    value = SouthBlockers[i]
                    if (value > -1):
                        southWall.value[value].runAttachedResponder(kTeamLightsOn)
                        print 'drawing s wall index',
                        print value
                    value = NorthBlockers[i]
                    if (value > -1):
                        northWall.value[value].runAttachedResponder(kTeamLightsOn)
                        print 'drawing n wall index',
                        print value
                    i = (i + 1)
            elif (state == ptClimbingWallMsgState.kSouthSelect):
                i = 0
                while ((i < 171)):
                    southWall.value[i].runAttachedResponder(kTeamLightsOff)
                    if (i < 20): # should help when drawing solution
                        SouthBlockers[i] = -1
                    i = (i + 1)
            elif (state == ptClimbingWallMsgState.kNorthSelect):
                i = 0
                while ((i < 171)):
                    if (i < 20): # same
                        NorthBlockers[i] = -1
                    northWall.value[i].runAttachedResponder(kTeamLightsOff)
                    i = (i + 1)
        elif (type == ptClimbingWallMsgType.kAddBlocker):
            self.SetWallIndex(state, true, value)
        elif (type == ptClimbingWallMsgType.kRemoveBlocker):
            self.SetWallIndex(state, false, value)


    def SetWallIndex(self, index, value, north):
        global NorthBlockers
        global SouthBlockers
        i = 0
        if value:
            if north:
                while ((NorthBlockers[i] >= 0)):
                    i = (i + 1)
                    if (i == 20):
                        print 'yikes - somehow overran the array!'
                        return
                NorthBlockers[i] = index
                print 'set north wall index ',
                print index,
                print ' in slot ',
                print i,
                print ' to true'
            else:
                while ((SouthBlockers[i] >= 0)):
                    i = (i + 1)
                    if (i == 20):
                        print 'yikes - somehow overran the array!'
                        return
                SouthBlockers[i] = index
                print 'set south wall index ',
                print index,
                print ' in slot ',
                print i,
                print ' to true'
        elif north:
            while ((NorthBlockers[i] != index)):
                i = (i + 1)
                if (i == 20):
                    print 'this should not get hit - looked for non-existent NorthWall entry!'
                    return
            NorthBlockers[i] = -1
            print 'removed index ',
            print index,
            print ' from list slot ',
            print i
        else:
            while ((SouthBlockers[i] != index)):
                i = (i + 1)
                if (i == 20):
                    print 'this should not get hit - looked for non-existent SouthWall entry!'
                    return
            SouthBlockers[i] = -1
            print 'removed index ',
            print index,
            print ' from list slot ',
            print i


    def OnNotify(self, state, id, events):
        if ((id == -1) and state):
            blocker = events[0][1]
            bNumber = int(blocker[2:])
            if (blocker[0] == "n"):
                northWall.value[bNumber-1].runAttachedResponder(kTeamLightsBlink)
            else:
                southWall.value[bNumber-1].runAttachedResponder(kTeamLightsBlink)


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



