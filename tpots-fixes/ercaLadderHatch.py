# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import string
import PlasmaControlKeys
SDLHatch = ptAttribString(1, 'SDL: hatch unlocked')
SDLEmpty = ptAttribString(2, 'SDL: pool empty')
ActLddr = ptAttribActivator(3, 'rgn snsr: ladder hatch')
MltStgLddr = ptAttribBehavior(4, 'mlt stg: use hatch/climb ladder')
RespHatchOps = ptAttribResponder(5, 'resp: hatch ops', ['lockedabove', 'openabove', 'lockedbelow', 'openbelow', 'close'])
StrDirection = ptAttribString(6, 'Direction: Going up or down?', 'up')
RespHatchLocked = ptAttribResponder(7, 'resp: hatch locked - only at top')
boolHatch = 0
boolEmpty = 0
ClimbAvatar = None
msgCache = {}

class ercaLadderHatch(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 7028
        self.version = 4


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        global boolHatch
        global boolEmpty
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(SDLHatch.value, 1, 1)
        ageSDL.sendToClients(SDLHatch.value)
        ageSDL.setFlags(SDLEmpty.value, 1, 1)
        ageSDL.sendToClients(SDLEmpty.value)
        ageSDL.setNotify(self.key, SDLHatch.value, 0.0)
        ageSDL.setNotify(self.key, SDLEmpty.value, 0.0)
        try:
            boolHatch = ageSDL[SDLHatch.value][0]
        except:
            PtDebugPrint('ERROR: ercaLadderHatch.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolHatch = 0
        PtDebugPrint(('DEBUG: ercaLadderHatch.OnServerInitComplete():\t%s = %d' % (SDLHatch.value, ageSDL[SDLHatch.value][0])))
        try:
            boolEmpty = ageSDL[SDLEmpty.value][0]
        except:
            PtDebugPrint('ERROR: ercaLadderHatch.OnServerInitComplete():\tERROR reading SDL name for pool empty')
            boolEmpty = 0
        PtDebugPrint(('DEBUG: ercaLadderHatch.OnServerInitComplete():\t%s = %d' % (SDLEmpty.value, ageSDL[SDLEmpty.value][0])))


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global boolHatch
        global boolEmpty
        ageSDL = PtGetAgeSDL()
        if (VARname == SDLHatch.value):
            boolHatch = ageSDL[SDLHatch.value][0]
        if (VARname == SDLEmpty.value):
            boolEmpty = ageSDL[SDLEmpty.value][0]


    def OnNotify(self, state, id, events):
        global boolHatch
        global boolEmpty
        global ClimbAvatar
        ageSDL = PtGetAgeSDL()
        ClimbAvatar = PtFindAvatar(events)
        if (StrDirection.value == 'down'):
            if ((id == ActLddr.id) and state):
                if boolHatch:
                    MltStgLddr.run(ClimbAvatar)
                    return
                else:
                    RespHatchLocked.run(self.key, avatar=ClimbAvatar)
                    return
        if (StrDirection.value == 'up'):
            if ((id == ActLddr.id) and state):
                MltStgLddr.run(ClimbAvatar)
        for event in events:
            if (event[0] == kMultiStageEvent):
                if (not (PtWasLocallyNotified(self.key))) and ClimbAvatar == PtGetLocalAvatar():
                    continue
                value = "%d:%d" % (event[1], event[2])
                theKI = PtGetClientIDFromAvatarKey(ClimbAvatar.getKey())
                try:
                    entry = msgCache[theKI]
                    if entry == value:
                        continue
                except:
                    pass
                msgCache[theKI] = value
                if (StrDirection.value == 'up'):
                    if (event[2] == kAdvanceNextStage):
                        stageNum = event[1]
                        print ('Going up.  Got stage advance callback from stage %d' % stageNum)
                        if (stageNum == 1):
                            print 'In stage 2, negotiating hatch.'
                            self.INegotiateHatch()
                        elif (stageNum == 2):
                            MltStgLddr.gotoStage(ClimbAvatar, 1, 0, 0)
                        elif ((stageNum == 3) or (stageNum == 5)):
                            print 'Got through hatch: finishing & removing brain.'
                            MltStgLddr.gotoStage(ClimbAvatar, -1)
                elif (StrDirection.value == 'down'):
                    stageNum = event[1]
                    print ('Going down.  Message from multistage %i' % stageNum)
                    if (event[2] == kRegressPrevStage):
                        print ('Got stage Regress callback from stage %d' % stageNum)
                        self.INegotiateHatch()
                    elif (event[2] == kAdvanceNextStage):
                        if (stageNum == 1):
                            print 'checking drained'
                            if (boolEmpty == 0):
                                MltStgLddr.gotoStage(ClimbAvatar, 7, 0, 0)
                                print 'water not drained'
                        if (stageNum == 4):
                            if (boolEmpty == 0):
                                MltStgLddr.gotoStage(ClimbAvatar, 7, dirFlag=1, isForward=1)
                            else:
                                MltStgLddr.gotoStage(ClimbAvatar, 2, dirFlag=1, isForward=1)
                            print 'now stage 3/7 again'
                        elif (stageNum == 6):
                            print 'Got through hatch: finishing & removing brain.'
                            MltStgLddr.gotoStage(ClimbAvatar, -1)
                        elif (stageNum == 3):
                            print 'done with bottom'
                            MltStgLddr.gotoStage(ClimbAvatar, -1)
        if (id == RespHatchLocked.id):
            RespHatchOps.run(self.key, state='lockedabove')


    def INegotiateHatch(self):
        global boolHatch
        print 'Negotiating hatch'
        if (boolHatch == 0):
            self.IHatchLocked()
        else:
            self.IHatchUnlocked()


    def IHatchLocked(self):
        if (StrDirection.value == 'up'):
            print 'Going up.  Hatch is locked; Sending gotoStage(2)'
            RespHatchOps.run(self.key, state='lockedbelow')
            MltStgLddr.gotoStage(ClimbAvatar, 2, 0, 1)
        elif (StrDirection.value == 'down'):
            print 'Going down.  Hatch is locked; Sending gotoStage(4)'
            MltStgLddr.gotoStage(ClimbAvatar, 4, dirFlag=1, isForward=1, setTimeFlag=1, newTime=0.0)
            RespHatchOps.run(self.key, state='lockedbelow')


    def IHatchUnlocked(self):
        if (StrDirection.value == 'up'):
            print 'Going up.  Hatch is unlocked; Sending gotoStage(3)'
            MltStgLddr.gotoStage(ClimbAvatar, 4, 0, 0)
        elif (StrDirection.value == 'down'):
            print 'Going down.  Hatch is unlocked; Sending gotoStage(5)'
            MltStgLddr.gotoStage(ClimbAvatar, 5, dirFlag=1, isForward=1, setTimeFlag=1, newTime=0.0)


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



