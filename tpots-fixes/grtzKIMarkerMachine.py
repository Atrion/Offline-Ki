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
MaxVersionNumber = 2
MinorVersionNumber = 5
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import xLocalization
import string
aKISlotAct = ptAttribActivator(1, 'KI Slot activator')
aKIAvatarResp = ptAttribResponder(2, 'Avatar Behavior resp', statelist=['Short', 'Longer'])
aKILogoResp = ptAttribResponder(3, 'Show KI Logo resp')
aKILightsResp = ptAttribResponderList(4, 'Light Responder List', statelist=['LightOn', 'LightOff'], byObject=1)
aKISoundsResp = ptAttribResponder(5, 'Sound responder', statelist=['UpLoadMarkers', 'DownLoadMarkers', 'ShowMarkers', 'UpLoadMarkers-05', 'DownLoadMarkers-05'])
gGZPlaying = 0
gGZMarkerInRange = 0
gGZMarkerInRangeRepy = None
gMarkerToGetColor = 'off'
gMarkerGottenColor = 'off'
gMarkerToGetNumber = 0
gMarkerGottenNumber = 0
gMarkerTargetToGetNumber = 0
gAvatar = None
gIsDownloadingLastGame = 0
kLightShiftOnDelaySeconds = 0.10000000000000001
kLightShiftOnID = 100
kTimeInbetweenDownAndUpload = 1.5
kLightShiftOffDelaySeconds = 0.10000000000000001
kLightShiftOffID = 200
kLightDelayDown1ID = 250
kLightDelayDown2ID = 275
kLightInbetweenDelaySeconds = 0.5
kLightInbetweenID = 300
kLightsOffSeconds = 2
kLightsOffDelayID = 10
kReEnableClickableSeconds = 8
kReEnableClickableID = 500
gLightRespNames = ['cRespKIMachLight01', 'cRespKIMachLight02', 'cRespKIMachLight03', 'cRespKIMachLight04', 'cRespKIMachLight05', 'cRespKIMachLight06', 'cRespKIMachLight07', 'cRespKIMachLight08', 'cRespKIMachLight09', 'cRespKIMachLight10', 'cRespKIMachLight11', 'cRespKIMachLight12', 'cRespKIMachLight13', 'cRespKIMachLight14', 'cRespKIMachLight15']

class grtzKIMarkerMachine(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 206
        self.version = MaxVersionNumber
        PtDebugPrint(('grtzKIMarkerMachine: Max version %d - minor version %d.1' % (MaxVersionNumber, MinorVersionNumber)), level=kDebugDumpLevel)


    def OnNotify(self, state, id, events):
        global gIsDownloadingLastGame
        global gAvatar
        PtDebugPrint(('grtzKIMarkerMachine: Notify  state=%f, id=%d' % (state, id)), level=kDebugDumpLevel)
        if (id == aKISlotAct.id):
            avatar = PtFindAvatar(events)
            aKISlotAct.disable()
            gAvatar = avatar
            if state:
                if (PtDetermineKILevel() >= kNormalKI):
                    aKIAvatarResp.run(self.key, avatar=avatar, state='Longer')
                else:
                    aKIAvatarResp.run(self.key, avatar=avatar, state='Short')
            if (gAvatar != PtGetLocalAvatar()):
                PtAtTimeCallback(self.key, kReEnableClickableSeconds, kReEnableClickableID)
        if (id == aKIAvatarResp.id):
            if (gAvatar != PtGetLocalAvatar()):
                return
            if (PtDetermineKILevel() >= kNormalKI):
                aKILogoResp.run(self.key)
                PtSendKIMessage(kKIShowMiniKI, 0)
                markerKILevel = PtDetermineKIMarkerLevel()
                self.IGetGZGame()
                gIsDownloadingLastGame = 0
                if (markerKILevel == kKIMarkerNotUpgraded):
                    PtDebugPrint('grtzKIMarkerMachine: Starting first GZ game', level=kDebugDumpLevel)
                    PtSendKIMessageInt(kUpgradeKIMarkerLevel, kKIMarkerFirstLevel)
                    self.IUploadGame1()
                    PtSendKIMessageInt(kGZUpdated, 40)
                elif (markerKILevel == kKIMarkerFirstLevel):
                    if (gMarkerGottenNumber >= gMarkerToGetNumber):
                        PtDebugPrint('grtzKIMarkerMachine: Done with first game', level=kDebugDumpLevel)
                        PtSendKIMessageInt(kUpgradeKIMarkerLevel, kKIMarkerSecondLevel)
                        self.IDownloadGame1()
                    else:
                        PtDebugPrint('grtzKIMarkerMachine: In the middle of the first game...', level=kDebugDumpLevel)
                        self.IShowCurrentGame()
                        aKISlotAct.enable()
                elif (markerKILevel == kKIMarkerSecondLevel):
                    PtDebugPrint('grtzKIMarkerMachine: In the middle of the second game', level=kDebugDumpLevel)
                    if (gMarkerGottenNumber >= gMarkerToGetNumber):
                        PtDebugPrint('grtzKIMarkerMachine: Done with second game', level=kDebugDumpLevel)
                        gIsDownloadingLastGame = 1
                        self.IDownloadGame2()
                        PtSendKIMessage(kGZUpdated, 0)
                    else:
                        PtDebugPrint('grtzKIMarkerMachine: In the middle of the second game...', level=kDebugDumpLevel)
                        self.IShowCurrentGame()
                        aKISlotAct.enable()
                else:
                    PtDebugPrint("grtzKIMarkerMachine: They're all done with this!", level=kDebugDumpLevel)
                    aKISlotAct.enable()
            else:
                PtDebugPrint('grtzKIMarkerMachine: KI level not high enough', level=kDebugDumpLevel)
                aKISlotAct.enable()


    def IGetGZGame(self):
        global gMarkerToGetColor
        global gMarkerToGetNumber
        global gGZPlaying
        global gMarkerGottenColor
        global gMarkerGottenNumber
        (gGZPlaying, gMarkerGottenColor, gMarkerToGetColor, gMarkerGottenNumber, gMarkerToGetNumber) = PtVerifyGZMarker()


    def IFlashGZGame(self):
        upstring = ('%d %s:%s %d:%d' % (gGZPlaying, gMarkerGottenColor, gMarkerToGetColor, gMarkerGottenNumber, gMarkerToGetNumber))
        PtSendKIMessage(kGZFlashUpdate, upstring)


    def ISetGZGame(self):
        PtUpdateGZGamesChonicles(gGZPlaying, gMarkerGottenColor, gMarkerToGetColor, gMarkerGottenNumber, gMarkerToGetNumber)


    def IUploadGame1(self):
        global gMarkerTargetToGetNumber
        global gMarkerGottenColor
        global gMarkerGottenNumber
        global gMarkerToGetColor
        global gMarkerToGetNumber
        global gGZPlaying
        PtDebugPrint('grtzKIMarkerMachine - uploading game 1 - shifting lights', level=kDebugDumpLevel)
        aKISoundsResp.run(self.key, state='UpLoadMarkers-05')
        gGZPlaying = 1
        gMarkerGottenColor = 'green'
        gMarkerToGetColor = 'greenlt'
        gMarkerGottenNumber = 0
        gMarkerToGetNumber = 0
        gMarkerTargetToGetNumber = 5
        self.IRefreshNextLightOn()


    def IRefreshNextLightOn(self):
        global gMarkerToGetNumber
        if (gMarkerToGetNumber < gMarkerTargetToGetNumber):
            PtDebugPrint(('grtzKIMarkerMachine - lighting light %d' % (gMarkerToGetNumber + 1)), level=kDebugDumpLevel)
            lidx = gMarkerToGetNumber
            aKILightsResp.run(self.key, state='LightOn', objectName=gLightRespNames[lidx])
            gMarkerToGetNumber += 1
            self.IFlashGZGame()
            PtAtTimeCallback(self.key, kLightShiftOnDelaySeconds, kLightShiftOnID)
        else:
            PtDebugPrint('grtzKIMarkerMachine - all done shifting', level=kDebugDumpLevel)
            gMarkerToGetNumber = gMarkerTargetToGetNumber
            self.ISetGZGame()
            PtSendKIMessage(kGZUpdated, 0)
            PtAtTimeCallback(self.key, kLightsOffSeconds, kLightsOffDelayID)


    def IDownloadGame1(self):
        for idx in range(0, gMarkerToGetNumber):
            aKILightsResp.run(self.key, state='LightOn', objectName=gLightRespNames[idx])
        PtAtTimeCallback(self.key, kLightShiftOffDelaySeconds, kLightDelayDown1ID)


    def IRefreshNextLightOff(self):
        global gMarkerToGetNumber
        if (gMarkerToGetNumber > 0):
            gMarkerToGetNumber -= 1
            lidx = gMarkerToGetNumber
            aKILightsResp.run(self.key, state='LightOff', objectName=gLightRespNames[lidx])
            self.IFlashGZGame()
            PtAtTimeCallback(self.key, kLightShiftOffDelaySeconds, kLightShiftOffID)
        elif (not gIsDownloadingLastGame):
            PtAtTimeCallback(self.key, kLightInbetweenDelaySeconds, kLightInbetweenID)
        else:
            vault = ptVault()
            entry = vault.findChronicleEntry(kChronicleGZGames)
            if (type(entry) != type(None)):
                entry.chronicleSetValue('0')
                entry.save()
            PtSendKIMessageInt(kUpgradeKIMarkerLevel, kKIMarkerNormalLevel)
            aKISlotAct.enable()


    def IUploadGame2(self):
        global gMarkerTargetToGetNumber
        global gMarkerGottenColor
        global gMarkerGottenNumber
        global gMarkerToGetColor
        global gMarkerToGetNumber
        global gGZPlaying
        self.IUpdateNexusLink()
        PtDebugPrint('grtzKIMarkerMachine - uploading game 2 - shifting lights', level=kDebugDumpLevel)
        aKISoundsResp.run(self.key, state='UpLoadMarkers')
        gGZPlaying = 2
        gMarkerGottenColor = 'red'
        gMarkerToGetColor = 'redlt'
        gMarkerGottenNumber = 0
        gMarkerToGetNumber = 0
        gMarkerTargetToGetNumber = 15
        self.IRefreshNextLightOn()


    def IDownloadGame2(self):
        for idx in range(0, gMarkerToGetNumber):
            aKILightsResp.run(self.key, state='LightOn', objectName=gLightRespNames[idx])
        PtAtTimeCallback(self.key, kLightShiftOffDelaySeconds, kLightDelayDown2ID)


    def IShowCurrentGame(self):
        PtDebugPrint(('grtzKIMarkerMachine - turn only %d lights on' % (gMarkerToGetNumber - gMarkerGottenNumber)), level=kDebugDumpLevel)
        aKISoundsResp.run(self.key, state='ShowMarkers')
        for idx in range(gMarkerGottenNumber, gMarkerToGetNumber):
            aKILightsResp.run(self.key, state='LightOn', objectName=gLightRespNames[idx])
        PtAtTimeCallback(self.key, kLightsOffSeconds, kLightsOffDelayID)


    def IUpdateNexusLink(self):
        vault = ptVault()
        folder = vault.getAgesIOwnFolder()
        contents = folder.getChildNodeRefList()
        for content in contents:
            link = content.getChild()
            link = link.upcastToAgeLinkNode()
            name = link.getAgeInfo().getAgeFilename()
            if (name == 'GreatZero'):
                outerRoomSP = ptSpawnPointInfo('Great Zero', 'BigRoomLinkInPoint')
                link.addSpawnPoint(outerRoomSP)
                link.save()
# Show KI message
                PtSendKIMessage(kKILocalChatStatusMsg, xLocalization.xKI.xKIStatusNexusLinkAdded)
# END Show KI message
                PtDebugPrint('grtzKIMarkerMachine - setting new spawn point for GZ', level=kDebugDumpLevel)
                return
        PtDebugPrint('grtzKIMarkerMachine - error - could not find link to add spawnpoint to')
        return


    def OnTimer(self, id):
        if (id == kLightsOffDelayID):
            PtDebugPrint(('grtzKIMarkerMachine - turn only %d lights off' % (gMarkerToGetNumber - gMarkerGottenNumber)), level=kDebugDumpLevel)
            for idx in range(gMarkerGottenNumber, gMarkerToGetNumber):
                aKILightsResp.run(self.key, state='LightOff', objectName=gLightRespNames[idx])
            aKISlotAct.enable()
        elif (id == kLightShiftOnID):
            self.IRefreshNextLightOn()
        elif (id == kLightShiftOffID):
            self.IRefreshNextLightOff()
        elif (id == kReEnableClickableID):
            aKISlotAct.enable()
        elif (id == kLightInbetweenID):
            self.IUploadGame2()
        elif (id == kLightDelayDown1ID):
            aKISoundsResp.run(self.key, state='DownLoadMarkers-05')
            self.IRefreshNextLightOff()
        elif (id == kLightDelayDown2ID):
            aKISoundsResp.run(self.key, state='DownLoadMarkers')
            self.IRefreshNextLightOff()


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



