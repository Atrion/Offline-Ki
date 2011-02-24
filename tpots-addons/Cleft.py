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
from PlasmaConstants import *
from PlasmaKITypes import *
respFissureDropStart = ptAttribResponder(1, 'resp: fissure drop start')
respFissureDropMain = ptAttribResponder(2, 'resp: fissure drop main')
loadTomahna = 0
loadZandi = 0
loadBook = 0
fissureDrop = 0
kIntroPlayedChronicle = 'IntroPlayed'

class Cleft(ptResponder):


    def __init__(self):
        global loadBook
        global loadZandi
        global loadTomahna
        ptResponder.__init__(self)
        self.id = 5209
        self.version = 22
        loadTomahna = 0
        loadZandi = 0
        loadBook = 0
        vault = ptVault()
        entryCleft = vault.findChronicleEntry('CleftSolved')
        if (type(entryCleft) != type(None)):
            entryCleftValue = entryCleft.chronicleGetValue()
            if (entryCleftValue != 'yes'):
                loadZandi = 1
                loadBook = 1
        elif (type(entryCleft) == type(None)):
            loadZandi = 1
            loadBook = 1
        vault = ptVault()
        entryTomahna = vault.findChronicleEntry('TomahnaLoad')
        if (type(entryTomahna) != type(None)):
            entryTomahnaValue = entryTomahna.chronicleGetValue()
            if (entryTomahnaValue == 'yes'):
                loadTomahna = 1
        pages = []
        if loadTomahna:
            pages += ['Cleft', 'tmnaDesert', 'MaleShortIdle', 'FemaleShortIdle', 'YeeshaFinalEncounter', 'FemaleTurnRight180', 'MaleTurnRight180', 'clftSndLogTracks']
        else:
            pages += ['Desert', 'Cleft', 'FemaleCleftDropIn', 'MaleCleftDropIn']
        if loadZandi:
            pages += ['clftZandiVis', 'ZandiCrossLegs', 'ZandiDirections', 'ZandiDirections01', 'ZandiDirections02', 'ZandiDirections03']
            pages += ['ZandiIdle', 'ZandiRubNose', 'ZandiScratchHead', 'ZandiTurnPage', 'ZandiAllFace', 'ZandiOpen01Face']
            pages += ['ZandiOpen02Face', 'ZandiRand01Face', 'ZandiRand02Face', 'ZandiRand03Face', 'ZandiRand04Face', 'ZandiRand05Face']
            pages += ['ZandiRes01aFace', 'ZandiRes01bFace', 'ZandiRes02aFace', 'ZandiRes02bFace', 'ZandiRes03aFace', 'ZandiRes03bFace']
            pages += ['ZandiJC01aFace', 'ZandiJC01bFace', 'ZandiJC02aFace', 'ZandiJC02bFace', 'ZandiJC03aFace', 'ZandiJC03bFace']
            pages += ['ZandiJC04aFace', 'ZandiJC04bFace', 'ZandiJC05aFace', 'ZandiJC05bFace', 'ZandiJC06aFace', 'ZandiJC06bFace']
            pages += ['ZandiJC07aFace', 'ZandiJC07bFace']
        else:
            print 'Zandi seems to have stepped away from the Airstream. Hmmm...'
        if loadBook:
            pages += ['clftYeeshaBookVis', 'FemaleGetPersonalBook', 'MaleGetPersonalBook']
        pages += ['BookRoom', 'clftAtrusNote']
        pages += ['FemaleClimbOffTreeLadder', 'FemaleGetOnTreeLadder', 'FemaleWindmillLockedCCW', 'FemaleWindmillLockedCW', 'FemaleWindmillStart']
        pages += ['MaleClimbOffTreeLadder', 'MaleGetOnTreeLadder', 'MaleWindmillLockedCCW', 'MaleWindmillLockedCW', 'MaleWindmillStart']
        pages += ['YeeshaVisionBlocked', 'YeeshaFinalVision']
        PtPageInNode(pages)
        if loadTomahna:
            entryTomahna.chronicleSetValue('no')
            entryTomahna.save()


    def DoesPlayerHaveRelto(self):
        vault = ptVault()
        entryCleft = vault.findChronicleEntry('CleftSolved')
        if (type(entryCleft) != type(None)):
            entryCleftValue = entryCleft.chronicleGetValue()
            if (entryCleftValue == 'yes'):
                return true
        return false


    def OnFirstUpdate(self):
        vault = ptVault()
        entry = vault.findChronicleEntry(kIntroPlayedChronicle)
        if (type(entry) != type(None)):
            PtSendKIMessage(kEnableKIandBB, 0)
        else:
            PtSendKIMessage(kDisableKIandBB, 0)
            PtLoadDialog('IntroMovieGUI')
        if not self.DoesPlayerHaveRelto():
            PtAtTimeCallback(self.key, 1, 0)


    def OnTimer(self, id):
        PtSendKIMessageInt(kUpgradeKILevel, kMicroKI)
        PtSendKIMessage(kEnableKIandBB, 0)
        PtSendKIMessage(kEnableKIandBB, 0)
        PtSendKIMessage(kDisableEntireYeeshaBook, 0)


    def OnServerInitComplete(self):
        global fissureDrop
        ageSDL = PtGetAgeSDL()
        if loadTomahna:
            SDLVarName = 'clftTomahnaActive'
            ageSDL[SDLVarName] = (1,)
            PtDebugPrint('Cleft.OnServerInitComplete: loadTomahna is 1, setting clftTomahnaActive SDL to 1')
            PtFogSetDefLinear(0, 0, 0)
            PtSetClearColor(0.40000000000000002, 0.40000000000000002, 0.5)
            SDLVarSceneBahro = 'clftSceneBahroUnseen'
            boolSceneBahro = ageSDL[SDLVarSceneBahro][0]
            if boolSceneBahro:
                PtDebugPrint('Cleft.OnServerInitComplete: SDL says bahro hasn\'t played yet, paging in SceneBahro stuff...')
                PtPageInNode('clftSceneBahro')
            else:
                PtDebugPrint('Cleft.OnServerInitComplete: SDL says SceneBahro already played, will NOT page in')
            ageSDL.setNotify(self.key, SDLVarSceneBahro, 0.0)
            SDLVarSceneYeesha = 'clftSceneYeeshaUnseen'
            boolSceneYeesha = ageSDL[SDLVarSceneYeesha][0]
            if boolSceneYeesha:
                SDLVarOfficeDoor = 'clftOfficeDoorClosed'
                boolOfficeDoor = ageSDL[SDLVarOfficeDoor][0]
                if boolOfficeDoor:
                    PtDebugPrint('Cleft.OnServerInitComplete: SDL says Yeesha will play and office door is shut, will open it')
                    ageSDL[SDLVarOfficeDoor] = (0,)
            else:
                PtDebugPrint('Cleft.OnServerInitComplete: SDL says SceneYeesha already played, will NOT page in')
        else:
            SDLVarName = 'clftTomahnaActive'
            ageSDL[SDLVarName] = (0,)
            PtDebugPrint('Cleft.OnServerInitComplete: loadTomahna is 0, setting clftTomahnaActive SDL set to 0')
            PtFogSetDefLinear(0, 0, 0)
            PtSetClearColor(0, 0, 0)
        linkmgr = ptNetLinkingMgr()
        link = linkmgr.getCurrAgeLink()
        spawnPoint = link.getSpawnPoint()
        spTitle = spawnPoint.getTitle()
        spName = spawnPoint.getName()
        if (spName == 'LinkInPointFissureDrop'):
            fissureDrop = 1
            avatar = 0
            try:
                avatar = PtGetLocalAvatar()
            except:
                print 'failed to get local avatar'
                return
            avatar.avatar.registerForBehaviorNotify(self.key)
            cam = ptCamera()
            cam.disableFirstPersonOverride()
            cam.undoFirstPerson()
            PtDisableMovementKeys()
            PtSendKIMessage(kDisableEntireYeeshaBook, 0)
            respFissureDropStart.run(self.key, avatar=PtGetLocalAvatar())


    def Load(self):
        ageSDL = PtGetAgeSDL()
        SDLVarKitchenDoor = 'clftKitchenDoorClosed'
        SDLVarOfficeDoor = 'clftOfficeDoorClosed'
        boolKitchenDoor = ageSDL[SDLVarKitchenDoor][0]
        boolOfficeDoor = ageSDL[SDLVarOfficeDoor][0]
        if (boolKitchenDoor and boolOfficeDoor):
            PtDebugPrint('Cleft.OnLoad: both Kitchen and Office doors are closed... setting Kitchen door SDL to open')
            ageSDL[SDLVarKitchenDoor] = (0,)
        else:
            PtDebugPrint('Cleft.OnLoad: either Kitchen and/or Office door is already open... leaving Kitchen door alone')


    def OnNotify(self, state, id, events):
        global fissureDrop
        if (id == respFissureDropMain.id):
            print 'FISSUREDROP.OnNotify:  respFissureDropMain.id callback'
            if fissureDrop:
                cam = ptCamera()
                cam.enableFirstPersonOverride()
                fissureDrop = 0
                avatar = PtGetLocalAvatar()
                avatar.avatar.unRegisterForBehaviorNotify(self.key)
                PtEnableMovementKeys()
                PtSendKIMessage(kEnableEntireYeeshaBook, 0)


    def OnBehaviorNotify(self, type, id, state):
        if ((type == PtBehaviorTypes.kBehaviorTypeLinkIn) and (not (state))):
            print ('FISSUREDROP.OnBehaviorNotify: fissureDrop = %d' % fissureDrop)
            if fissureDrop:
                PtDebugPrint('Cleft.OnBehaviorNotify(): will run respFissureDropMain now.')
                respFissureDropMain.run(self.key, avatar=PtGetLocalAvatar())


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



