from Plasma import *
from PlasmaTypes import *
from PlasmaConstants import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
from xPsnlVaultSDL import *
import string
import time
RespBlah = ptAttribResponder(1, 'resp: do blah', ['first', 'second'])
SDLDebris = ptAttribString(2, 'SDL: debris')
RespEndingScreen = ptAttribResponder(3, 'resp: ending screen', ['begin', 'end'])
SDLRewards = ptAttribString(4, 'SDL: rewards')
MyBlah = 0
kFadeOutToGameID = 4
kHideBookID = 5
kFadeInToGameID = 6
kWaitNewEndingID = 7
kFadeOutToGameSeconds = 1.0
kFadeInToGameSeconds = 2.0
gOriginalAmbientVolume = 1.0
gOriginalSFXVolume = 1.0

class Kveer(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 8100
        self.version = 4


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        global MyBlah
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(SDLDebris.value, 1, 1)
        ageSDL.sendToClients(SDLDebris.value)
        ageSDL.setNotify(self.key, SDLDebris.value, 0.0)
        ageSDL.setFlags(SDLRewards.value, 1, 1)
        ageSDL.sendToClients(SDLRewards.value)
        ageSDL.setNotify(self.key, SDLRewards.value, 0.0)
        vault = ptVault()
        entry = vault.findChronicleEntry('Blah')
        if (type(entry) != type(None)):
            entryValue = entry.chronicleGetValue()
            MyBlah = string.atoi(entryValue)
            if ((MyBlah == 1) or (MyBlah == 3)):
                avatar = PtGetLocalAvatar()
                avatar.avatar.registerForBehaviorNotify(self.key)
                PtSendKIMessage(kDisableKIandBB, 0)
        else:
            MyBlah = 0


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        pass


    def OnBehaviorNotify(self, type, id, state):
        global MyBlah
        ageSDL = PtGetAgeSDL()
        PtDebugPrint(('Kveer.OnBehaviorNotify(): %d' % type))
        if ((type == PtBehaviorTypes.kBehaviorTypeLinkIn) and state):
            if (MyBlah == 3):
                cam = ptCamera()
                cam.disableFirstPersonOverride()
                cam.undoFirstPerson()
                PtDisableMovementKeys()
                PtSendKIMessage(kDisableKIandBB, 0)
                RespEndingScreen.run(self.key, state='begin', avatar=PtGetLocalAvatar())
                audio = ptAudioControl()
                gOriginalAmbientVolume = audio.getAmbienceVolume()
                audio.setAmbienceVolume(0.0)
                gOriginalSFXVolume = audio.getSoundFXVolume()
                audio.setSoundFXVolume(0.0)
        if ((type == PtBehaviorTypes.kBehaviorTypeLinkIn) and (not (state))):
            if (MyBlah == 1):
                RespBlah.run(self.key, state='first')
            elif (MyBlah == 3):
                RespBlah.run(self.key, state='second')
                ageSDL[SDLDebris.value] = (0,)
                ageSDL[SDLRewards.value] = (1,)
            avatar = PtGetLocalAvatar()
            avatar.avatar.unRegisterForBehaviorNotify(self.key)


    def OnNotify(self, state, id, events):
        global MyBlah
        if (id == RespBlah.id):
            if (MyBlah == 1):
                vault = ptVault()
                entry = vault.findChronicleEntry('Blah')
                entry.chronicleSetValue(('%d' % 2))
                entry.save()
                print 'do link to X2 finale version of ferry terminal'
                info = ptAgeInfoStruct()
                info.setAgeFilename('DniCityX2Finale')
                als = ptAgeLinkStruct()
                als.setAgeInfo(info)
                als.setLinkingRules(PtLinkingRules.kOwnedBook)
                spawnpoint = ptSpawnPointInfo()
                spawnpoint.setName('LinkInPointBlah')
                als.setSpawnPoint(spawnpoint)
                linkMgr = ptNetLinkingMgr()
                linkMgr.linkToAge(als)
                return
            elif (MyBlah == 3):
                print 'end blah stuff'
                self.IFadeOutFromScreen()
                vault = ptVault()
                entry = vault.findChronicleEntry('Blah')
                entry.chronicleSetValue(('%d' % 4))
                entry.save()
            MyBlah = 0
        if (id == RespEndingScreen.id):
            pass


    def OnTimer(self, id):
        print 'Kveer.OnTimer: Callback from id:',
        print id
        if (id == kFadeOutToGameID):
            self.IFadeInToGame()
        elif (id == kHideBookID):
            print 'The credits book is now hidden'
            RespEndingScreen.run(self.key, state='end', avatar=PtGetLocalAvatar())
            PtAtTimeCallback(self.key, kFadeOutToGameSeconds, kFadeOutToGameID)
        elif (id == kFadeInToGameID):
            PtFadeIn(kFadeInToGameSeconds, 1, 1)
            print 'Kveer.OnTimer FadeIn to game over',
            print kFadeInToGameSeconds,
            print ' seconds'
            PtEnableMovementKeys()
            PtSendKIMessage(kEnableKIandBB, 0)
            cam = ptCamera()
            cam.enableFirstPersonOverride()


    def IFadeOutFromScreen(self):
        print 'Kveer.IReturnToGame: fade out from ending screen'
        PtFadeOut(3, 1, 1)
        PtAtTimeCallback(self.key, 4, kHideBookID)


    def IFadeInToGame(self):
        global gOriginalAmbientVolume
        global gOriginalSFXVolume
        print 'Kveer.IFadeOutToGame: Returning to game now.'
        audio = ptAudioControl()
        audio.setAmbienceVolume(gOriginalAmbientVolume)
        audio.setSoundFXVolume(gOriginalSFXVolume)
        PtAtTimeCallback(self.key, 1, kFadeInToGameID)


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



