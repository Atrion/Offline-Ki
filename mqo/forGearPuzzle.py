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
global gGearsOn
global gStopping
global gGear1Pos
global gGear2Pos
global gCompleted
global gCheckedQuest
global glue_cl
global glue_inst
global glue_params
global glue_paramKeys
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
#Dustin
#import xQManUtility
#from xWandCastUtil import *
#/Dustin
respGear00 = ptAttribResponder(1, 'Gear00 Rotation Responder')
respGear01 = ptAttribResponder(2, 'Gear01 Rotation Responder')
respGear02 = ptAttribResponder(3, 'Gear02 Rotation Responder')
respGear03 = ptAttribResponder(4, 'Gear03 Rotation Responder')
respGear04 = ptAttribResponder(5, 'Rotation Responder for 4 and 5')
actLever01 = ptAttribActivator(6, 'Lever 1 Clickable')
actLever02 = ptAttribActivator(7, 'Lever 2 Clickable')
actLever03 = ptAttribActivator(8, 'Lever 3 Clickable')
respLever01 = ptAttribResponder(9, 'Lever 1 Position Resp', ['on', 'off', 'fail'])
respLever02 = ptAttribResponder(10, 'Lever 2 Position Resp', ['on', 'off', 'fail'])
respLever03 = ptAttribResponder(11, 'Lever 3 Position Resp', ['on', 'off', 'fail'])
respDefaultPos = ptAttribResponder(12, 'Gear Default Resp', ['incomplete', 'complete'])
respBridgeState = ptAttribNamedResponder(13, 'Bridge Position Responder', ['down', 'up'])
gGearsOn = 0
gStopping = 0
gGear1Pos = 0
gGear2Pos = 0
gCompleted = 0
gCheckedQuest = 0

class forGearPuzzle(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 6512
        self.version = 1


    def OnServerInitComplete(self):
        global gGear1Pos
        global gGear2Pos
        gGear1Pos = 0
        gGear2Pos = 1
        #Dustin: open the bridges
        #gearsDone = xQManUtility.getItemsObtainedFromItem('19', '2', '0')
        gearsDone = 1
        PtFindSceneobject('BridgeCollide01', 'ForestMQ').physics.suppress(True)
        PtFindSceneobject('BridgeCollide02', 'ForestMQ').physics.suppress(True)
        #/Dustin
        if int(gearsDone):
            print 'Gears Complete'
            respDefaultPos.run(self.key, avatar=PtGetLocalAvatar(), state='complete', netPropagate=0)
            respBridgeState.run(self.key, state='down', netPropagate=0)
        else:
            print 'Gears Incomplete'
            respDefaultPos.run(self.key, avatar=PtGetLocalAvatar(), state='incomplete', netPropagate=0)
            respBridgeState.run(self.key, state='up', netPropagate=0)


    def OnNotify(self, state, id, events):
        global gGearsOn
        global gStopping
        global gCompleted
        if (id == respGear00.id):
            print 'forGearPuzzle:OnNotify - Gear Responder Finished'
            if (gGearsOn == 1):
                print 'forGearPuzzle:OnNotify - Gears Are Going to Run'
                self.RunGears()
            elif (gStopping == 1):
                print 'forGearPuzzle:OnNotify - Finally Stopped'
                gStopping = 0
        elif (gCompleted == 0):
            if (id == respLever01.id):
                print 'forGearPuzzle:OnNotify - Lever Responder Finished'
                if (gGearsOn == 1):
                    print 'forGearPuzzle:OnNotify - Stopping Gears'
                    self.StopGears()
                else:
                    print 'forGearPuzzle:OnNotify - Gears are Going to Run'
                    self.RunGears()
            elif (PtFindAvatar(events) == PtGetLocalAvatar()):
                if ((id == actLever01.id) and state):
                    self.PullLever(1)
                elif ((id == actLever02.id) and state):
                    self.PullLever(2)
                elif ((id == actLever03.id) and state):
                    self.PullLever(3)


    def PullLever(self, lever):
        global gCheckedQuest
        global gStopping
        global gGearsOn
        global gGear2Pos
        global gGear1Pos
        print ('forGearPuzzle:PullLever - Lever %d Pulled' % lever)
        castUtil = xWandCastUtil()
        if (gCheckedQuest == 0):
            QuestTitle = xQManUtility.getQuestDevTitleFromID('19')
            response = xQManUtility.startQuest(QuestTitle, 0)
            gCheckedQuest = 1
        if (lever == 1):
            if (gStopping == 0):
                if (gGearsOn == 1):
                    castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                    print 'forGearPuzzle:PullLever - Turning Lever Off'
                    respLever01.run(self.key, avatar=PtGetLocalAvatar(), state='off', netPropagate=0)
                else:
                    castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                    print 'forGearPuzzle:PullLever - Turning Lever On'
                    respLever01.run(self.key, avatar=PtGetLocalAvatar(), state='on', netPropagate=0)
            else:
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastFailure)
                print 'forGearPuzzle:PullLever - Lever pull failed'
                respLever01.run(self.key, avatar=PtGetLocalAvatar(), state='fail', netPropagate=0)
        elif (lever == 2):
            if ((gGearsOn == 1) or ((gGear2Pos == 1) or (gStopping == 1))):
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastFailure)
                print 'forGearPuzzle:PullLever - lever pull failed'
                respLever02.run(self.key, avatar=PtGetLocalAvatar(), state='fail', netPropagate=0)
            elif (gGear1Pos == 0):
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                print 'forGearPuzzle:PullLever - Turning Lever On'
                gGear1Pos = 1
                respLever02.run(self.key, avatar=PtGetLocalAvatar(), state='on', netPropagate=0)
            elif (gGear1Pos == 1):
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                print 'forGearPuzzle:PullLever - Turning Lever Off'
                gGear1Pos = 0
                respLever02.run(self.key, avatar=PtGetLocalAvatar(), state='off', netPropagate=0)
        elif (lever == 3):
            if ((gGearsOn == 1) or gStopping):
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastFailure)
                print 'forGearPuzzle:PullLever - lever pull failed'
                respLever03.run(self.key, avatar=PtGetLocalAvatar(), state='fail', netPropagate=0)
            elif (gGear2Pos == 0):
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                print 'forGearPuzzle:PullLever - Turning Lever On'
                gGear2Pos = 1
                respLever03.run(self.key, avatar=PtGetLocalAvatar(), state='on', netPropagate=0)
            elif (gGear2Pos == 1):
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                print 'forGearPuzzle:PullLever - Turning Lever Off'
                gGear2Pos = 0
                respLever03.run(self.key, avatar=PtGetLocalAvatar(), state='off', netPropagate=0)


    def RunGears(self):
        global gGearsOn
        global gGear1Pos
        global gGear2Pos
        global gCompleted
        gears = []
        gGearsOn = 1
        respGear00.run(self.key, netPropagate=0)
        gears.append('0')
        if (gGear1Pos == 1):
            respGear01.run(self.key, netPropagate=0)
            gears.append('1')
            if (gGear2Pos == 1):
                respGear02.run(self.key, netPropagate=0)
                respGear03.run(self.key, netPropagate=0)
                respGear04.run(self.key, netPropagate=0)
                gears.append('2')
                gears.append('3')
                gears.append('4')
                gears.append('5')
                if (gCompleted == 0):
                    gCompleted = 1
                    actLever01.disable()
                    actLever02.disable()
                    actLever03.disable()
                    respBridgeState.run(self.key, state='down', netPropagate=0)
                    spawnerCoords = ('%s%d%d%d' % (PtGetAgeName(), self.sceneobject.position().getX(), self.sceneobject.position().getY(), self.sceneobject.position().getZ()))
                    itemResponse = xQManUtility.modifyItemByAmount('FOR:GearPuzzle', 1, spawnerCoords, '')
                    response = xQManUtility.endQuest('FOR:Windmill', '', 0)
                    print ('forGearPuzzle:RunGears - Gears Engaged -- %s' % str(gears))


    def StopGears(self):
        global gStopping
        global gGearsOn
        gStopping = 1
        gGearsOn = 0
        print 'forGearPuzzle:StopGears - Stopping Gears'


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



