# -*- coding: utf-8 -*-
MaxVersionNumber = 1
MinorVersionNumber = 1
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import string
aCGZGameType = ptAttribInt(1, 'CalGZ game type(1-4)')
aCGZRegionVis = ptAttribActivator(2, 'Region detector when marker is inRange')
aCGZSoundResponder = ptAttribResponder(3, 'Sound responder for marker', statelist=['SoundOn', 'SoundOff'])
aCGZClickOn = ptAttribActivator(4, 'Clickable on the CalGZ marker')
gSoundRespWasCalled = 0
gGZPlaying = 0
gMarkerToGetColor = 'off'
gMarkerGottenColor = 'off'
gMarkerToGetNumber = 0
gMarkerGottenNumber = 0

class xCGZMarker(ptMultiModifier):


    def __init__(self):
        ptMultiModifier.__init__(self)
        self.id = 216
        self.version = MaxVersionNumber
        PtDebugPrint(('__xCGZMarker: Max version %d - minor version %d' % (MaxVersionNumber, MinorVersionNumber)), level=kDebugDumpLevel)


    def OnServerInitComplete(self):
        self.DisableObject()


    def IsMarkerAvailable(self):
        if (PtDetermineKIMarkerLevel() >= kKIMarkerNormalLevel):
            self.IDetermineGZ()
            whichGame = (aCGZGameType.value - 1)
            if ((whichGame >= kCGZFirstGame) and (whichGame <= kCGZFinalGame)):
                if (PtGetCGZGameState(whichGame) == kCGZMarkerAvailable):
                    PtDebugPrint(('xCGZMarker: marker %d available' % aCGZGameType.value), level=kDebugDumpLevel)
                    return 1
                else:
                    PtDebugPrint(('xCGZMarker: marker not available - at %d is a \'%s\'' % (aCGZGameType.value, PtGetCGZGameState(whichGame))), level=kDebugDumpLevel)
            else:
                PtDebugPrint(('xCGZMarker - invalid CGZ game type of %d' % aCGZGameType.value))
        else:
            PtDebugPrint(('xCGZMarker - KI marker level %d not high enough' % PtDetermineKIMarkerLevel()))
        return 0


    def EnableObject(self):
        PtDebugPrint(('DEBUG: xCGZMarker.EnableObject:  Attempting to enable drawing and collision on %s...' % self.sceneobject.getName()), level=kDebugDumpLevel)
        self.sceneobject.draw.enable()
        self.sceneobject.physics.suppress(false)


    def DisableObject(self):
        PtDebugPrint(('DEBUG: xCGZMarker.DisableObject:  Attempting to disable drawing and collision on %s...' % self.sceneobject.getName()), level=kDebugDumpLevel)
        self.sceneobject.draw.disable()
        self.sceneobject.physics.suppress(true)


    def OnNotify(self, state, id, events):
        global gSoundRespWasCalled
        if (id == aCGZRegionVis.id):
            for event in events:
                if (event[0] == kCollisionEvent):
                    if (event[2] == PtGetLocalAvatar()):
                        if (event[1] == 1):
                            PtDebugPrint('xCGZMarker: enter region', level=kDebugDumpLevel)
                            if self.IsMarkerAvailable():
                                self.EnableObject()
##############################################################################
# Changes for PotS markers
##############################################################################
                                import xxConfig
                                if xxConfig.CollectMarkersUU: aGZClickOn.disable() # add to enforce UU way
##############################################################################
# Changes for PotS markers
##############################################################################
                                aCGZSoundResponder.run(self.key, state='SoundOn', netPropagate=0)
                                gSoundRespWasCalled = 1
                                PtSendKIGZMarkerMsg(aCGZGameType.value, self.key)
                        else:
                            PtDebugPrint('xCGZMarker: exit region', level=kDebugDumpLevel)
                            self.DisableObject()
                            if gSoundRespWasCalled:
                                aCGZSoundResponder.run(self.key, state='SoundOff', netPropagate=0)
                                gSoundRespWasCalled = 0
                            PtSendKIMessage(kGZOutRange, 0)
        elif ((id == aCGZClickOn.id) and state):
            for event in events:
                if (event[0] == kPickedEvent):
                    if (event[2] == PtGetLocalAvatar()):
                        if (event[1] == 1):
                            PtDebugPrint(('xCGZMarker: capture this marker(%d)' % aCGZGameType.value), level=kDebugDumpLevel)
                            self.ICaptureCGZ()
                            self.DisableObject()
                            if gSoundRespWasCalled:
                                aCGZSoundResponder.run(self.key, state='SoundOff', netPropagate=0)
                                gSoundRespWasCalled = 0
                            PtSendKIMessage(kGZOutRange, 0)
                            PtSendKIMessage(kGZUpdated, 0)
##############################################################################
# Changes for PotS markers
##############################################################################
        # add this to allow the UU way
        elif (id == -1):
            for event in events:
                if ((event[0] == kVariableEvent) and (event[1] == 'Captured')):
                    self.ICaptureCGZ()
                    self.DisableObject()
                    if gSoundRespWasCalled:
                        aCGZSoundResponder.run(self.key, state='SoundOff', netPropagate=0)
                        gSoundRespWasCalled = 0
                    PtSendKIMessage(kGZOutRange, 0)
                    PtSendKIMessage(kGZUpdated, 0)
##############################################################################
# Changes for PotS markers
##############################################################################


    def IDetermineGZ(self):
        global gMarkerToGetColor
        global gMarkerToGetNumber
        global gGZPlaying
        global gMarkerGottenColor
        global gMarkerGottenNumber
        (gGZPlaying, gMarkerGottenColor, gMarkerToGetColor, gMarkerGottenNumber, gMarkerToGetNumber) = PtDetermineGZ()


    def ICaptureCGZ(self):
        global gMarkerGottenNumber
        whichGame = (aCGZGameType.value - 1)
        if ((whichGame >= kCGZFirstGame) and (whichGame <= kCGZFinalGame)):
            PtSetCGZGameState(whichGame, kCGZMarkerCaptured)
            self.IDetermineGZ()
            gMarkerGottenNumber += 1
            if (gMarkerGottenNumber > gMarkerToGetNumber):
                gMarkerGottenNumber = gMarkerToGetNumber
            PtUpdateGZGamesChonicles(gGZPlaying, gMarkerGottenColor, gMarkerToGetColor, gMarkerGottenNumber, gMarkerToGetNumber)
        else:
            PtDebugPrint(('xCGZMarker - invalid CGZ game type of %d' % aCGZGameType.value))


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



