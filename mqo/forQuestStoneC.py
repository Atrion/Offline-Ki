# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    This is a patched file that was originally written by Cyan                #
#    See the file AUTHORS for more info about the contributors of the changes  #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                      #
#                                                                              #
#    You may re-use the code in this file within the context of Uru.           #
#                                                                              #
#==============================================================================#
global glue_cl
global glue_inst
global glue_params
global glue_paramKeys
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
#Dustin
#from xWandCastUtil import *
#import xQManUtility
#/Dustin
ActQuestStone = ptAttribActivator(1, 'clk: Quest Stone')
StrBinkStart = ptAttribString(2, 'str: Bink Start')
StrBinkFail = ptAttribString(3, 'str: Bink Fail')
ActDoorOutside = ptAttribActivator(4, 'clk: Outside Door')
ActDoorInside = ptAttribActivator(5, 'clk: Inside Door')
RespDoorOutside = ptAttribResponder(6, 'resp: Outside Door', ['success', 'fail'])
RespDoorInside = ptAttribResponder(7, 'resp: Inside Door')
RespWindmill = ptAttribResponder(8, 'resp: Windmill', ['on', 'off'])
ActOwl = ptAttribActivator(9, 'clk: Owl')
RespOwl = ptAttribResponder(10, 'resp: Owl', ['start', 'end'])
MapBinkLayer = ptAttribMaterialAnimation(11, 'map: Owl Bink Layer')
StrBinkNotHere = ptAttribString(12, 'str: Bink Not Here')
actHandleClick = ptAttribActivator(13, 'Handle Clickable')
respApproachHandle = ptAttribResponder(14, 'Handle Approach Responder')
respActivateHandle = ptAttribResponder(15, 'Handle Activate Responder', ['success', 'fail'])
objBattleBox = ptAttribSceneobject(16, 'Battle GUI Box')
respQuestStoneCast = ptAttribResponder(17, 'Quest Stone Responder')
respBridges = ptAttribResponder(18, 'Bridges Responder', ['on', 'off'])
RespQuestStoneActive = ptAttribResponder(19, 'resp: QuestStoneActive', ['Complete', 'Not Active', 'Active'])

class forQuestStoneC(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 6702
        self.version = 1


    def __del__(self):
        pass


    def OnFirstUpdate(self):
        #Dustin
        #PtLoadDialog('BinkFullscreenMovie')
        #PtLoadDialog('BinkLargeMovie')
        #MapBinkLayer.value.sender(self.key)
        #MapBinkLayer.value.setMovieFilename('avi\\OnlineOwl_DefaultClip.bik')
        #MapBinkLayer.value.play()
        #MapBinkLayer.value.stop()
        #handleDone = xQManUtility.getItemsObtainedFromItem('13', '1', '0')
        handleDone = 1
        #/Dustin
        print ('forQuestStoneC:OnFirstUpdate - Handle = %s' % handleDone)
        if int(handleDone):
            RespWindmill.run(self.key, netPropagate=0, state='on')
        else:
            RespWindmill.run(self.key, netPropagate=0, state='off')


    def OnNotify(self, state, id, events):
        #Dustin
        #castUtil = xWandCastUtil()
        #/Dustin
        if ((id == ActQuestStone.id) and (state and (PtFindAvatar(events) == PtGetLocalAvatar()))):
            print 'forQuestStoneC:OnNotify - Quest Stone triggered'
            #castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
            respQuestStoneCast.run(self.key, avatar=PtGetLocalAvatar(), netPropagate=0)
        elif (id == respQuestStoneCast.id):
            playingAudioResponder = 0
            prereqStatus = xQManUtility.getQuestStatusFromID('10')
            binkMovie = ''
            if (prereqStatus == 'finalized'):
                QuestTitle = xQManUtility.getQuestDevTitleFromID('13')
                response = xQManUtility.startQuest(QuestTitle, 1)
                questStatus = xQManUtility.getQuestStatusFromTitle(QuestTitle)
                binkMovie = ''
                if (response == 'success'):
                    binkMovie = StrBinkStart.value
                elif (questStatus != 'finalized'):
                    playingAudioResponder = 1
                    print 'forQuestStoneC:OnNotify - Quest Stone Active. Firing Audio Responder.'
                    RespQuestStoneActive.run(self.key, state='Active', netPropagate=0)
                else:
                    playingAudioResponder = 1
                    print 'forQuestStoneC:OnNotify - Quest Stone Completed. Firing Audio Responder.'
                    RespQuestStoneActive.run(self.key, state='Complete', netPropagate=0)
            else:
                playingAudioResponder = 1
                print 'forQuestStoneC:OnNotify - Quest Stone Not Active Yet. Firing Audio Responder.'
                RespQuestStoneActive.run(self.key, state='Not Active', netPropagate=0)
            if (playingAudioResponder == 0):
                PtSendKIMessage(kMQQuestUpdate, 0)
                print 'forQuestStoneC:OnNotify - Starting Fullscreen Bink: ',
                print binkMovie
                PtFindSceneobject('BinkGUI', 'GUI').callPythonFunction('startFullscreenMovie', (binkMovie,))
                PtShowDialog('BinkFullscreenMovie')
        elif ((id == ActDoorInside.id) and (state and (PtFindAvatar(events) == PtGetLocalAvatar()))):
            #Dustin
            #castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
            #/Dustin
            RespDoorInside.run(self.key, avatar=PtGetLocalAvatar(), netPropagate=0)
        elif ((id == ActDoorOutside.id) and (state and (PtFindAvatar(events) == PtGetLocalAvatar()))):
            #Dustin
            #handleDone = xQManUtility.getItemsObtainedFromItem('13', '1', '0')
            handleDone = 1
            #/Dustin
            if int(handleDone):
                #Dustin
                #castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                #/Dustin
                RespDoorOutside.run(self.key, avatar=PtGetLocalAvatar(), netPropagate=0, state='success')
            else:
                #castUtil.SetCastSFX(self.key, xWandCastType.kWandCastFailure)
                RespDoorOutside.run(self.key, avatar=PtGetLocalAvatar(), netPropagate=0, state='fail')
        elif ((id == ActOwl.id) and (state and (PtFindAvatar(events) == PtGetLocalAvatar()))):
            #castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
            RespOwl.run(self.key, avatar=PtGetLocalAvatar(), state='start')
        elif (id == RespOwl.id):
            PtSendKIMessage(kDisableKIandBB, 0)
            status = xQManUtility.getQuestStatusFromID('13')
            binkMovie = 'OnlineOwl_DefaultClip.bik'
            if (status == 'complete'):
                binkMovie = 'OnlineOwl_SuccessClip.bik'
                PtAtTimeCallback(self.key, 54, 1)
            PtSendKIMessage(kMQQuestUpdate, 0)
            print 'forQuestStoneC:OnNotify - Starting Bink: ',
            print binkMovie
            MapBinkLayer.value.setMovieFilename(('avi\\' + binkMovie))
            MapBinkLayer.value.play()
        elif ((id == actHandleClick.id) and (state and (PtFindAvatar(events) == PtGetLocalAvatar()))):
            print 'forQuestStoneC:OnNotify - Handle triggered, starting approach'
            respApproachHandle.run(self.key, avatar=PtFindAvatar(events), netPropagate=0)
        elif (id == respApproachHandle.id):
            if (xQManUtility.getQuestStatusFromTitle('FOR:Tutorial') in ['in_progress', 'received']):
                print 'forQuestStoneC:OnNotify - Approach callback, starting normal battle'
                objBattleBox.value.callPythonFunction('ActivateDialog', (self.key,))
            else:
                print 'forQuestStoneC:OnNotify - Approach callback, requirements not met'
                #castUtil.SetCastSFX(self.key, xWandCastType.kWandCastFailure)
                respActivateHandle.run(self.key, avatar=PtGetLocalAvatar(), state='fail', netPropagate=0)
        elif (id == -1):
            callback = events[0][1]
            if (callback == 'success'):
                print 'forQuestStoneC:OnNotify - Battle callback, finish normal open'
                #castUtil.SetCastSFX(self.key, xWandCastType.kWandCastSuccess)
                respActivateHandle.run(self.key, avatar=PtGetLocalAvatar(), state='success', netPropagate=0)
                spawnerCoords = ('%s%d%d%d' % (PtGetAgeName(), self.sceneobject.position().getX(), self.sceneobject.position().getY(), self.sceneobject.position().getZ()))
                itemResponse = xQManUtility.modifyItemByAmount('FOR:HandleBattle', 1, spawnerCoords, '')
                PtSendKIMessage(kMQQuestUpdate, 0)
            else:
                print 'forQuestStoneC:OnNotify - Battle callback, failed battle'
                #castUtil.SetCastSFX(self.key, xWandCastType.kWandCastFailure)
                respActivateHandle.run(self.key, avatar=PtGetLocalAvatar(), state='fail', netPropagate=0)
                PtSendKIMessage(kEnableKIandBB, 0)


    def OnMovieEvent(self, filename, event):
        if (event == 0):
            PtSendKIMessage(kEnableKIandBB, 0)
            RespOwl.run(self.key, avatar=PtGetLocalAvatar(), state='end', netPropagate=0)


    def OnTimer(self, id):
        if (id == 1):
            PtFindSceneobject('BinkLargeAlphaGUI', 'GUI').callPythonFunction('startLargeMovie', ('Rune Chisel given by Owl.bik',))
            PtShowDialog('BinkLargeMovie')
            response = xQManUtility.endQuest('FOR:Tutorial', 'GBL:ChiselRune', 1)
            PtSendKIMessage(kMQQuestUpdate, 0)


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



