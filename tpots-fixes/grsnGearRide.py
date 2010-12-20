# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import cPickle
gearEnterExclude = ptAttribExcludeRegion(1, 'gear enter exclude')
failedEnterExclude = ptAttribExcludeRegion(2, 'failed enter exclude')
failedExitExclude = ptAttribExcludeRegion(3, 'failed exit exclude')
crackOpenEvent = ptAttribActivator(4, 'open crack event')
crackCloseEvent = ptAttribActivator(5, 'close crack event')
exitOpenEvent = ptAttribActivator(6, 'exit open event')
exitCloseEvent = ptAttribActivator(7, 'exit close event')
gearEnterRegion = ptAttribActivator(8, 'trigger subworld entry')
gearExitRegion = ptAttribActivator(9, 'exit subworld at gear')
gearSubWorld = ptAttribSceneobject(10, 'gear niche subworld')
safetyRegion1 = ptAttribActivator(11, 'safety region 1')
safetyRegion2 = ptAttribActivator(12, 'safety region 2')
safetyRegion3 = ptAttribActivator(13, 'safety region 3')
enterSafePoint = ptAttribSceneobject(14, 'enter safe point')
exitSafePoint = ptAttribSceneobject(15, 'exit safe point')
gearExitCrackRegion = ptAttribActivator(16, 'exit subworld at crack')
rideCamera = ptAttribSceneobject(17, 'ride camera')
gearExitCamera = ptAttribSceneobject(18, 'exit at gear camera')
crackExitCamera = ptAttribSceneobject(19, 'exit at crack camera')
popExitCrackCamera = ptAttribActivator(20, 'pop exit crack camera')
safetyRegion4 = ptAttribActivator(21, 'safety region 4')
safetyRegion5 = ptAttribActivator(22, 'safety region 5')
stringSDLVarPower = ptAttribString(23, 'SDL Bool Power')
keepAwayFromGear = ptAttribExcludeRegion(24, 'keep away from gear rgn')
keepAwayOn = ptAttribActivator(25, 'keep away region on')
keepAwayOff = ptAttribActivator(26, 'keep away region off')
gearTeleportSpot = ptAttribSceneobject(27, 'gear room teleport point')
AgeStartedIn = None

class grsnGearRide(ptResponder):


    def __init__(self):
        PtDebugPrint('grsnGearRide::init begin')
        ptResponder.__init__(self)
        self.id = 50113
        self.version = 3
        self.fFramesToWarp = -1
        PtDebugPrint('grsnGearRide::init end')


    def clearExcludeRegions(self):
        gearEnterExclude.clear(self.key)
        failedEnterExclude.clear(self.key)
        failedExitExclude.clear(self.key)


    def releaseExcludeRegions(self):
        gearEnterExclude.release(self.key)
        failedEnterExclude.release(self.key)
        failedExitExclude.release(self.key)


    def EnableSafetyRegions(self):
        safetyRegion1.enable()
        safetyRegion2.enable()
        safetyRegion3.enable()


    def DisableSafetyRegions(self):
        safetyRegion1.disable()
        safetyRegion2.disable()
        safetyRegion3.disable()


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        self.SDL.setDefault('exitOpen', (0,))
        self.SDL.setDefault('crackOpen', (0,))
        self.SDL.setDefault('avatarRidingGear', (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1))
        self.SDL.setDefault('avatarWithExitCam', (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1))
        self.clearExcludeRegions()


    def OnServerInitComplete(self):
        if self.SDL['exitOpen'][0]:
            PtDebugPrint('opening gear niche at load')
            self.releaseExcludeRegions()
        else:
            PtDebugPrint('closing gear niche at load')
            self.clearExcludeRegions()
        if self.SDL['crackOpen'][0]:
            PtDebugPrint('opening gear exit at load')
            gearExitRegion.enable()
            gearEnterExclude.release(self.key)
            failedExitExclude.release(self.key)
        else:
            PtDebugPrint('closing gear exit at load')
            self.clearExcludeRegions()
            gearExitRegion.disable()


    def OnUpdate(self, secs, delta):
        if (self.fFramesToWarp != -1):
            self.fFramesToWarp -= 1
            PtGetLocalAvatar().physics.warpObj(enterSafePoint.value.getKey())


    def OnNotify(self, state, id, events):
        if (id == crackOpenEvent.id):
            for event in events:
                if ((event[0] == kPickedEvent) and ((event[1] == 1) and (self.SDL['crackOpen'][0] == 0))):
                    gearEnterRegion.enable()
                    gearExitCrackRegion.enable()
                    self.releaseExcludeRegions()
                    self.SDL['crackOpen'] = (1,)
                    return
        if (id == crackCloseEvent.id):
            for event in events:
                if ((event[0] == kPickedEvent) and ((event[1] == 1) and (self.SDL['crackOpen'][0] == 1))):
                    gearEnterRegion.disable()
                    gearExitCrackRegion.disable()
                    self.clearExcludeRegions()
                    self.SDL['crackOpen'] = (0,)
                    return
        if (id == exitOpenEvent.id):
            for event in events:
                if ((event[0] == kPickedEvent) and ((event[1] == 1) and (self.SDL['exitOpen'][0] == 0))):
                    print 'opening gear exit'
                    self.DisableSafetyRegions()
                    gearExitRegion.enable()
                    gearEnterExclude.release(self.key)
                    failedExitExclude.release(self.key)
                    self.SDL['exitOpen'] = (1,)
                    return
        if (id == keepAwayOn.id):
            for event in events:
                if ((event[0] == kPickedEvent) and ((event[1] == 1) and (self.SDL['exitOpen'][0] == 0))):
                    print 'back off'
                    keepAwayFromGear.clear(self.key)
                    return
        if (id == keepAwayOff.id):
            for event in events:
                if ((event[0] == kPickedEvent) and ((event[1] == 1) and (self.SDL['exitOpen'][0] == 0))):
                    print 'back off'
                    keepAwayFromGear.release(self.key)
                    return
        if (id == exitCloseEvent.id):
            for event in events:
                if ((event[0] == kPickedEvent) and ((event[1] == 1) and (self.SDL['exitOpen'][0] == 1))):
                    print 'closing gear exit'
                    self.clearExcludeRegions()
                    gearExitRegion.disable()
                    self.SDL['exitOpen'] = (0,)
                    self.EnableSafetyRegions()
                    return
        if ((id == safetyRegion1.id) or ((id == safetyRegion2.id) or (id == safetyRegion3.id))):
            avatarRidingGear = PtFindAvatar(events)
            avatarID = PtGetClientIDFromAvatarKey(avatarRidingGear.getKey())
            for event in events:
                if (event[0] == kCollisionEvent):
                    if (event[1] == 1):
                        for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            if (self.SDL['avatarRidingGear'][count] == avatarID):
                                rgn = 0
                                if (id == safetyRegion1.id):
                                    rgn = 1
                                elif (id == safetyRegion2.id):
                                    rgn = 2
                                elif (id == safetyRegion3.id):
                                    rgn = 3
                                PtDebugPrint(((('avatar ID ' + `avatarID`) + ' entered safe region ') + `rgn`))
                                gearExitRegion.disable()
                                avatarRidingGear.avatar.enterSubWorld(gearSubWorld.value)
                                avatarRidingGear.physics.warpObj(enterSafePoint.value.getKey())
                                cam = ptCamera()
                                cam.disableFirstPersonOverride()
                                cam.undoFirstPerson()
                                rideCamera.value.pushCutsceneCamera(1, avatarRidingGear.getKey())
                                self.SDL.setIndex('avatarRidingGear', count, avatarID)
                                return
                        for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            if (self.SDL['avatarRidingGear'][count] == -1):
                                PtDebugPrint((('avatar ID ' + `avatarID`) + ' entered gear subworld'))
                                gearExitRegion.disable()
                                avatarRidingGear.avatar.enterSubWorld(gearSubWorld.value)
                                avatarRidingGear.physics.warpObj(enterSafePoint.value.getKey())
                                cam = ptCamera()
                                cam.disableFirstPersonOverride()
                                cam.undoFirstPerson()
                                rideCamera.value.pushCutsceneCamera(1, avatarRidingGear.getKey())
                                self.SDL.setIndex('avatarRidingGear', count, avatarID)
                                return
                            elif (self.SDL['avatarRidingGear'][count] == avatarID):
                                return
                        PtDebugPrint('error - more than 10 people in gear niche?!?')
        if (id == gearEnterRegion.id):
            avatarRidingGear = PtFindAvatar(events)
            avatarID = PtGetClientIDFromAvatarKey(avatarRidingGear.getKey())
            for event in events:
                if (event[0] == kCollisionEvent):
                    if (event[1] == 1):
                        for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            if (self.SDL['avatarRidingGear'][count] == avatarID):
                                PtDebugPrint((('avatar ID ' + `avatarID`) + ' entered gear subworld TWICE?!?'))
                                PtDebugPrint((('avatar ID ' + `avatarID`) + ' entered gear subworld'))
                                gearExitRegion.disable()
                                avatarRidingGear.avatar.enterSubWorld(gearSubWorld.value)
                                avatarRidingGear.physics.warpObj(enterSafePoint.value.getKey())
                                cam = ptCamera()
                                cam.disableFirstPersonOverride()
                                cam.undoFirstPerson()
                                avatarRidingGear.draw.enable()
                                PtFadeLocalAvatar(0)
                                rideCamera.value.pushCutsceneCamera(1, avatarRidingGear.getKey())
                                self.SDL.setIndex('avatarRidingGear', count, avatarID)
                                return
                        for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            if (self.SDL['avatarRidingGear'][count] == -1):
                                PtDebugPrint((('avatar ID ' + `avatarID`) + ' entered gear subworld'))
                                gearExitRegion.disable()
                                avatarRidingGear.avatar.enterSubWorld(gearSubWorld.value)
                                avatarRidingGear.physics.warpObj(enterSafePoint.value.getKey())
                                cam = ptCamera()
                                cam.disableFirstPersonOverride()
                                cam.undoFirstPerson()
                                avatarRidingGear.draw.enable()
                                PtFadeLocalAvatar(0)
                                rideCamera.value.pushCutsceneCamera(1, avatarRidingGear.getKey())
                                self.SDL.setIndex('avatarRidingGear', count, avatarID)
##############################################################################
# Don't warp everyone into walls and stuff.
##############################################################################
#                                self.fFramesToWarp = 9
                                if PtGetLocalAvatar() == avatarRidingGear:
                                    self.fFramesToWarp = 9
##############################################################################
# End don't warp everyone into walls and stuff.
##############################################################################
                                return
                            elif (self.SDL['avatarRidingGear'][count] == avatarID):
                                return
                        PtDebugPrint('error - more than 10 people in gear niche?!?')
        if (id == gearExitRegion.id):
            avatarExitingGear = PtFindAvatar(events)
            avatarID = PtGetClientIDFromAvatarKey(avatarExitingGear.getKey())
            for event in events:
                if (event[0] == kCollisionEvent):
                    if (event[1] == 1):
                        for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            if (self.SDL['avatarRidingGear'][count] == avatarID):
                                PtDebugPrint((('avatar ID ' + `avatarID`) + ' entered exit region at gear room'))
                                cam = ptCamera()
                                gearExitCamera.value.pushCamera(avatarExitingGear.getKey())
                                rideCamera.value.popCutsceneCamera(avatarExitingGear.getKey())
                                avatarExitingGear.avatar.exitSubWorld()
                                avatarExitingGear.physics.warpObj(gearTeleportSpot.value.getKey())
                                cam.enableFirstPersonOverride()
                                avatarExitingGear.draw.enable()
                                self.SDL.setIndex('avatarRidingGear', count, -1)
                                return
                        PtDebugPrint((('avatar ID ' + `avatarID`) + ' entered gear exit region but wasn\'t in the niche?!?'))
        if (id == gearExitCrackRegion.id):
            avatarExitingGear = PtFindAvatar(events)
            avatarID = PtGetClientIDFromAvatarKey(avatarExitingGear.getKey())
            for event in events:
                if (event[0] == kCollisionEvent):
                    if (event[1] == 1):
                        for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            if (self.SDL['avatarRidingGear'][count] == avatarID):
                                PtDebugPrint((('avatar ID ' + `avatarID`) + ' entered exit region at crack'))
                                avatarExitingGear.avatar.exitSubWorld()
                                avatarExitingGear.physics.warpObj(exitSafePoint.value.getKey())
                                cam = ptCamera()
                                cam.enableFirstPersonOverride()
                                crackExitCamera.value.pushCutsceneCamera(1, avatarExitingGear.getKey())
                                avatarExitingGear.draw.enable()
                                cam.undoFirstPerson()
                                self.SDL.setIndex('avatarRidingGear', count, -1)
                                self.SDL.setIndex('avatarWithExitCam', count, avatarID)
                                return
                        PtDebugPrint((('avatar ID ' + `avatarID`) + " entered gear exit region but wasn't in the niche?!?"))
        if (id == popExitCrackCamera.id):
            avatarExitingCrack = PtFindAvatar(events)
            avatarID = PtGetClientIDFromAvatarKey(avatarExitingCrack.getKey())
            for event in events:
                if (event[0] == kCollisionEvent):
                    if (event[1] == 1):
                        for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            if (self.SDL['avatarWithExitCam'][count] == avatarID):
                                PtDebugPrint((('avatar ID ' + `avatarID`) + ' exiting crack after exiting niche - popping camera'))
                                cam = ptCamera()
                                crackExitCamera.value.popCutsceneCamera(avatarExitingCrack.getKey())
                                self.SDL.setIndex('avatarWithExitCam', count, -1)
                                return


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



