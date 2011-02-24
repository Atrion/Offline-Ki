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
from PlasmaKITypes import *
from PlasmaNetConstants import *
import whrandom
kEmptyGuid = '0000000000000000'

class Personal(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5022
        self.version = 1
        PtDebugPrint(('Personal: __init__ version %d.%d' % (self.version, 1)), level=kWarningLevel)


    def gotPublicAgeList(self, ages):
        highestGuid = 0
        for age in ages:
            guid = age[0].getAgeInstanceGuid()
            if (guid > highestGuid):
                highestGuid = guid
        PtDebugPrint(('Personal.gotPublicAgeList(): Using city GUID ' + str(highestGuid)))
        vault = ptVault()
        l = ptAgeInfoStruct()
        l.setAgeFilename('city')
        myCity = vault.getOwnedAgeLink(l)
        if myCity:
            cityInfo = myCity.getAgeInfo()
            if cityInfo:
                cityInfo.setAgeInstanceGuid(highestGuid)
                cityInfo.save()


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        PtDebugPrint('Personal.OnServerInitComplete(): Grabbing first week clothing item boolean')
        try:
            firstWeekClothing = ageSDL['FirstWeekClothing'][0]
        except:
            PtDebugPrint('Unable to get the first week clothing item bool, not going to add it just to be safe')
            firstWeekClothing = 0
        avatar = PtGetLocalAvatar()
        currentgender = avatar.avatar.getAvatarClothingGroup()
        if firstWeekClothing:
            if (currentgender == kFemaleClothingGroup):
                clothingName = 'FReward_Beta'
            else:
                clothingName = 'MReward_Beta'
            clothingList = avatar.avatar.getWardrobeClothingList()
            if (clothingName not in clothingList):
                PtDebugPrint((('Adding ' + clothingName) + ' clothing item to your closet! Aren\'t you lucky?'))
                avatar.avatar.addWardrobeClothingItem(clothingName, ptColor().white(), ptColor().white())
            else:
                PtDebugPrint((('You already have ' + clothingName) + ' so I\'m not going to add it again.'))
        else:
            PtDebugPrint('I guess you\'re too late, you don\'t get the first week clothing item')
        PtDebugPrint('Personal.OnServerInitComplete(): Checking to see if we need to add reward clothing to your closet')
        try:
            rewardList = ageSDL['RewardClothing'][0]
        except:
            PtDebugPrint('Unable to grab the reward clothing list from SDL, not going to add anything')
            rewardList = ''
        PtDebugPrint('Personal.OnServerInitComplete(): Checking to see if we need to add global reward clothing to your closet')
        try:
            globalRewardList = ageSDL['GlobalRewardClothing'][0]
        except:
            PtDebugPrint('Unable to grab the global reward clothing list from SDL, not going to add anything')
            globalRewardList = ''
        nameSuffixList = []
        if (rewardList != ''):
            nameSuffixList += rewardList.split(';')
        if (globalRewardList != ''):
            nameSuffixList += globalRewardList.split(';')
        for suffix in nameSuffixList:
            suffix = suffix.strip()
            if (currentgender == kFemaleClothingGroup):
                genderPrefix = 'FReward_'
            else:
                genderPrefix = 'MReward_'
            clothingName = (genderPrefix + suffix)
            clothingList = avatar.avatar.getWardrobeClothingList()
            if (clothingName not in clothingList):
                PtDebugPrint((('Adding ' + clothingName) + ' to your closet'))
                avatar.avatar.addWardrobeClothingItem(clothingName, ptColor().white(), ptColor().white())
            else:
                PtDebugPrint((('You already have ' + clothingName) + ' so I\'m not going to add it again.'))
        if (rewardList != ''):
            ageSDL['RewardClothing'] = ('',)
        else:
            PtDebugPrint('Reward clothing list empty, not adding any clothing')
        vault = ptVault()
        info = ptAgeInfoStruct()
        info.setAgeFilename('RestorationGuild')
        rstrGuild = vault.getOwnedAgeLink(info)
        if (not rstrGuild):
            PtDebugPrint('We don\'t have a restoration guild so let\'s try making one')
            infos = ptAgeInfoStruct()
            infos.setAgeFilename('RestorationGuild')
            infos.setAgeInstanceName('Watcher\'s Guild')
            link = ptAgeLinkStruct()
            link.setAgeInfo(infos)
            link.setLinkingRules(PtLinkingRules.kOriginalBook)
            link.setSpawnPoint(ptSpawnPointInfo('Default', 'LinkInPointDefault'))
            vault.registerOwnedAge(link)
        else:
            PtDebugPrint('We have a restoration guild so just move on')
        PtAtTimeCallback(self.key, 0.0, 0) # wait till the MOUL page was loaded


    def OnFirstUpdate(self):
        import xSndLogTracks
        xSndLogTracks.UnsetLogMode()
        vault = ptVault()
        l = ptAgeInfoStruct()
        l.setAgeFilename('city')
        myCity = vault.getOwnedAgeLink(l)
        if myCity:
            cityInfo = myCity.getAgeInfo()
            if cityInfo:
                if (cityInfo.getAgeInstanceGuid() == kEmptyGuid):
                    PtGetPublicAgeList('city', self)
            else:
                PtDebugPrint('hmm. city link has no age info node')
        else:
            PtDebugPrint('hmm. player has no city link')


    def Load(self):
        pass


    def OnNotify(self, state, id, events):
        pass


    def OnTimer(self, id):
        PtSendKIMessageInt(kUpgradeKILevel, kMicroKI)
        PtSendKIMessage(kEnableKIandBB, 0)
        PtSendKIMessage(kEnableKIandBB, 0)
        PtSendKIMessage(kEnableEntireYeeshaBook, 0)
        PtSendKIMessage(kEnableYeeshaBook, 0)
# fix fog layer
# only execute this if MOUL got converted, and after the MOUL prp is loaded - that's why we use a timer
        import os
        if not os.path.exists('dat/Personal_District_psnlDustAdditions.prp'): return
        # hide the old fog layer
        PtFindSceneobject('FogLayer', 'Personal').draw.disable()
        PtFindSceneobject('FogLayerBill', 'Personal').draw.disable()
        # find out state
        vaultSDL = ptAgeVault().getAgeSDL()
        islandValue = vaultSDL.findVar('YeeshaPage7').getInt()
        # control new fog layer
        baseFog = PtFindSceneobject('DustinFogLayer', 'Personal')
        islandFog = PtFindSceneobject('DustinFogLayerBill', 'Personal')
        if islandValue in [0, 2, 4]: # show default fog, hide new one
            baseFog.draw.enable()
            islandFog.draw.disable()
        else: # hide default fog, show new one
            baseFog.draw.disable()
            islandFog.draw.enable()


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



