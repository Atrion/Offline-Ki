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
global gBattleNum
global gInFirstPerson
global glue_cl
global glue_inst
global glue_params
global glue_paramKeys
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
#Dustin removed:
#import xQManUtility
#from xWandCastUtil import *
#/Dustin
actRubbleClick = ptAttribActivator(1, 'Rubble Clickable')
respRubbleStages = ptAttribResponder(2, 'Rubble Success Responder', ['1', '2', '3', 'fail', 'completed'])
respRubbleApproach = ptAttribResponder(3, 'Rubble Approach Responder')
objBattleBox1 = ptAttribSceneobject(4, 'Battle GUI Box1')
objBattleBox2 = ptAttribSceneobject(5, 'Battle GUI Box2')
objBattleBox3 = ptAttribSceneobject(6, 'Battle GUI Box3')
gBattleNum = 1
gInFirstPerson = 0

class forRubbleActivator(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 6511
        self.version = 1


    def OnFirstUpdate(self):
        #Dustin changed: Remove the rubble in the gear-room under the mill
        #rubbleDone = xQManUtility.getItemsObtainedFromItem('19', '1', '0')
        rubbleDone = 1
        PtFindSceneobject('BridgeBlocker', 'ForestMQ').physics.suppress(True)
        PtFindSceneobject('RubbleClickableBox', 'ForestMQ').physics.suppress(True)
        PtFindSceneobject('RubbleMesh04', 'ForestMQ').physics.suppress(True)
        PtFindSceneobject('RubbleMesh06', 'ForestMQ').physics.suppress(True)
        PtFindSceneobject('Box01', 'ForestMQ').physics.suppress(True)
        #/Dustin
        if int(rubbleDone):
            print 'Rubble Complete'
            respRubbleStages.run(self.key, avatar=PtGetLocalAvatar(), state='completed', netPropagate=0)


    def OnNotify(self, state, id, events):
        global gBattleNum
        global gInFirstPerson
        castUtil = xWandCastUtil()
        if ((id == actRubbleClick.id) and (state and (PtFindAvatar(events) == PtGetLocalAvatar()))):
            status = xQManUtility.getQuestStatusFromTitle('FOR:Tutorial')
            if (status == 'finalized'):
                respRubbleApproach.run(self.key, avatar=PtFindAvatar(events), netPropagate=0)
                QuestTitle = xQManUtility.getQuestDevTitleFromID('19')
                status = xQManUtility.getQuestStatusFromTitle(QuestTitle)
                response = xQManUtility.startQuest(QuestTitle, 0)
            else:
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastFailure)
                respRubbleStages.run(self.key, avatar=PtGetLocalAvatar(), state='fail', netPropagate=0)
        elif (id == respRubbleApproach.id):
            print ('forRubbleActivator:OnNotify - Activating BattleStage %d' % gBattleNum)
            if PtFirstPerson():
                cam = ptCamera()
                cam.undoFirstPerson()
                cam.disableFirstPersonOverride()
                gInFirstPerson = 1
            if (gBattleNum == 1):
                objBattleBox1.value.callPythonFunction('ActivateDialog', (self.key,))
            elif (gBattleNum == 2):
                objBattleBox2.value.callPythonFunction('ActivateDialog', (self.key,))
            elif (gBattleNum == 3):
                objBattleBox3.value.callPythonFunction('ActivateDialog', (self.key,))
        elif (id == -1):
            callback = events[0][1]
            print ('forRubbleActivator:OnNotify - callback %s' % callback)
            if (callback == 'success'):
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                print ('forRubbleActivator:OnNotify - Success reported by battle %d' % gBattleNum)
                respRubbleStages.run(self.key, avatar=PtGetLocalAvatar(), state=str(gBattleNum), netPropagate=0)
                gBattleNum += 1
                if (gBattleNum == 2):
                    objBattleBox2.value.callPythonFunction('ActivateDialog', (self.key, 0))
                elif (gBattleNum == 3):
                    objBattleBox3.value.callPythonFunction('ActivateDialog', (self.key, 0))
                elif (gBattleNum == 4):
                    spawnerCoords = ('%s%d%d%d' % (PtGetAgeName(), self.sceneobject.position().getX(), self.sceneobject.position().getY(), self.sceneobject.position().getZ()))
                    itemResponse = xQManUtility.modifyItemByAmount('FOR:RubbleBattle', 1, spawnerCoords, '')
                    print ('forRubbleActivator:OnNotify - QuestManager Add Item Status : %s' % itemResponse)
                    print ('Rubble Item Collected Response: %s' % itemResponse)
                if gInFirstPerson:
                    cam = ptCamera()
                    cam.enableFirstPersonOverride()
                    gInFirstPerson = 0
            else:
                castUtil.SetCastSFX(self.key, xWandCastType.kWandCastFailure)
                respRubbleStages.run(self.key, avatar=PtGetLocalAvatar(), state='fail', netPropagate=0)
                if gInFirstPerson:
                    cam = ptCamera()
                    cam.enableFirstPersonOverride()
                    gInFirstPerson = 0


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



