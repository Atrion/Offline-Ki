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
import PlasmaControlKeys
ActStart = ptAttribActivator(4, 'Starts the climb')
Climber = ptAttribBehavior(5, 'The multistage behavior')
respHatchOps = ptAttribResponder(6, 'Rspndr: Hatch Ops', ['lockedabove', 'openabove', 'lockedbelow', 'openbelow', 'close'])
ClimbAvatar = None
hatchLocked = 1
hatchOpen = 0
cabinDrained = 0
msgCache = {}
kStringAgeSDLCabinDrained = 'tldnCabinDrained'
kStringAgeSDLHatchOpen = 'tldnHatchOpen'
kStringAgeSDLHatchLocked = 'tldnHatchLocked'
AgeStartedIn = None

class tldnHatchLadderTop(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 7001
        version = 6
        self.version = version


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()


    def OnServerInitComplete(self):
        global cabinDrained
        global hatchLocked
        global hatchOpen
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags(kStringAgeSDLHatchOpen, 1, 1)
            ageSDL.sendToClients(kStringAgeSDLHatchOpen)
            ageSDL.setNotify(self.key, kStringAgeSDLCabinDrained, 0.0)
            ageSDL.setNotify(self.key, kStringAgeSDLHatchOpen, 0.0)
            ageSDL.setNotify(self.key, kStringAgeSDLHatchLocked, 0.0)
            try:
                cabinDrained = ageSDL[kStringAgeSDLCabinDrained][0]
                hatchOpen = ageSDL[kStringAgeSDLHatchOpen][0]
                hatchLocked = ageSDL[kStringAgeSDLHatchLocked][0]
            except:
                cabinDrained = false
                hatchOpen = false
                hatchLocked = true
                PtDebugPrint('tldnHatchLadderTop.OnServerInitComplete():\tERROR: age sdl read failed, defaulting:')
            PtDebugPrint(('tldnHatchLadderTop.OnServerInitComplete():\t%s=%d, %s=%d, %s=%d' % (kStringAgeSDLCabinDrained, cabinDrained, kStringAgeSDLHatchOpen, hatchOpen, kStringAgeSDLHatchLocked, hatchLocked)))
            if (hatchOpen and (not hatchLocked)):
                ActStart.enable()
            else:
                ActStart.disable()


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global cabinDrained
        global hatchLocked
        global hatchOpen
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            PtDebugPrint(('tldnHatchLadderTop.OnSDLNotify():\t VARname:%s, SDLname:%s, tag:%s, value:%d, playerID:%d' % (VARname, SDLname, tag, ageSDL[VARname][0], playerID)))
            if (VARname == kStringAgeSDLCabinDrained):
                cabinDrained = ageSDL[kStringAgeSDLCabinDrained][0]
            if (VARname == kStringAgeSDLHatchLocked):
                hatchLocked = ageSDL[kStringAgeSDLHatchLocked][0]
            if (VARname == kStringAgeSDLHatchOpen):
                hatchOpen = ageSDL[kStringAgeSDLHatchOpen][0]
                if hatchOpen:
                    ActStart.enable()
                else:
                    ActStart.disable()


    def OnNotify(self, state, id, events):
        global ClimbAvatar
        ClimbAvatar = PtFindAvatar(events)
        if state:
            if (id == ActStart.id):
                Climber.run(ClimbAvatar)
                return
        for event in events:
            if (event[0] == kMultiStageEvent):
                if ((not PtWasLocallyNotified(self.key)) and (ClimbAvatar == PtGetLocalAvatar())):
                    continue
                value = ('%d:%d' % (event[1], event[2]))
                theKI = PtGetClientIDFromAvatarKey(ClimbAvatar.getKey())
                print str(msgCache)
                try:
                    entry = msgCache[theKI]
                    if (entry == value):
                        continue
                except:
                    pass
                msgCache[theKI] = value
                stageNum = event[1]
                print ('message from multistage %i' % stageNum)
                if (event[2] == kRegressPrevStage):
                    print ('Got stage Regress callback from stage %d' % stageNum)
                    self.INegotiateHatch()
                elif (event[2] == kAdvanceNextStage):
                    if (stageNum == 1):
                        print 'checking drained'
                        if (not cabinDrained):
                            Climber.gotoStage(ClimbAvatar, 6, 0, 0)
                            print 'water not drained'
                    elif (stageNum == 4):
                        if (not cabinDrained):
                            Climber.gotoStage(ClimbAvatar, 6, dirFlag=1, isForward=1)
                        else:
                            Climber.gotoStage(ClimbAvatar, 2, dirFlag=1, isForward=1)
                        print 'now stage 2/6 again'
                    elif (stageNum == 5):
                        print 'Got through hatch: finishing & removing brain.'
                        Climber.gotoStage(ClimbAvatar, -1)
                    elif (stageNum == 3):
                        print 'done with bottom'
                        Climber.gotoStage(ClimbAvatar, -1)


    def INegotiateHatch(self):
        print 'Negotiating hatch'
        if hatchOpen:
            self.IHatchOpen()
        elif hatchLocked:
            self.IHatchLocked()
        else:
            self.IHatchUnlocked()


    def IHatchLocked(self):
        print 'Hatch is locked; Sending gotoStage(4)'
        Climber.gotoStage(ClimbAvatar, 4, dirFlag=1, isForward=1, setTimeFlag=1, newTime=0.0)
        respHatchOps.run(self.key, state='lockedbelow')


    def IHatchUnlocked(self):
        global hatchOpen
        print 'Hatch is unlocked; Sending gotoStage(5)'
        respHatchOps.run(self.key, state='openbelow')
        Climber.gotoStage(ClimbAvatar, 5, dirFlag=1, isForward=1, setTimeFlag=1, newTime=0.0)
        hatchOpen = 1
        if (AgeStartedIn == PtGetAgeName()):
            if (ClimbAvatar == PtGetLocalAvatar()):
                ageSDL = PtGetAgeSDL()
                ageSDL[kStringAgeSDLHatchOpen] = (1,)


    def IHatchOpen(self):
        print 'Hatch is open; Sending gotoStage(1)'
        Climber.gotoStage(ClimbAvatar, 1, setTimeFlag=1, newTime=1.2)


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



