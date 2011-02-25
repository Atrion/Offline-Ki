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
import PlasmaControlKeys
Activate = ptAttribActivator(1, 'Activate Telescope', netForce=1)
Camera = ptAttribSceneobject(2, 'Telescope camera')
Behavior = ptAttribBehavior(3, 'Telescope behavior (multistage)', netForce=1)
ScopeNumber = ptAttribInt(4, 'Scope Number (1-3)')
actResetBtn = ptAttribActivator(5, 'act:Reset(only on scope3')
respResetBtn = ptAttribResponder(6, 'resp:Reset Button')
respSfxRings = ptAttribResponder(7, 'resp: Sfx Rings')
OnlyOneOwner = ptAttribSceneobject(8, 'OnlyOneOwner')
LocalAvatar = None
boolScopeOperator = 0
boolOperated = 0
Telescope = ptInputInterface()
kGUIRingTurnLeft = 110
kGUIRingTurnCenter = 111
kGUIRingTurnRight = 112
oldbearing = 0
OuterRing = 0
MiddleRing = 0
InnerRing = 0

class kdshTreeRings(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5228
        version = 12
        self.version = version
        print '__init__kdshTreeRings v.',
        print version,
        print '.1'


    def OnFirstUpdate(self):
        PtLoadDialog(('kdshScope0' + str(ScopeNumber.value)), self.key, 'Kadish')


    def OnServerInitComplete(self):
        global MiddleRing
        global OuterRing
        global InnerRing
        ageSDL = PtGetAgeSDL()
        OuterRing = ageSDL[('OuterRing0' + str(ScopeNumber.value))][0]
        MiddleRing = ageSDL[('MiddleRing0' + str(ScopeNumber.value))][0]
        InnerRing = ageSDL[('InnerRing0' + str(ScopeNumber.value))][0]
        print ('Current %s Ring settings:' % ScopeNumber.value)
        print '/tOuterRing: ',
        print OuterRing
        print '/tMiddleRing: ',
        print MiddleRing
        print '/tInnerRing: ',
        print InnerRing
        solo = true
        if len(PtGetPlayerList()):
            solo = false
        boolOperated = ageSDL[('boolOperatedScope0' + str(ScopeNumber.value))][0]
        if boolOperated:
            if solo:
                print ('kdshTreeRings.Load():\tboolOperated=%d but no one else here...correcting' % boolOperated)
                boolOperated = 0
                ageSDL[('boolOperatedScope0' + str(ScopeNumber.value))] = (0,)
                ageSDL[('OperatorIDScope0' + str(ScopeNumber.value))] = (-1,)
                Activate.enable()
            else:
                Activate.disable()
                print ('kdshTreeRings.Load():\tboolOperated=%d, disabling telescope clickable' % boolOperated)
        ageSDL.sendToClients(('boolOperatedScope0' + str(ScopeNumber.value)))
        ageSDL.setFlags(('boolOperatedScope0' + str(ScopeNumber.value)), 1, 1)
        ageSDL.sendToClients(('OperatorIDScope0' + str(ScopeNumber.value)))
        ageSDL.setFlags(('OperatorIDScope0' + str(ScopeNumber.value)), 1, 1)
        ageSDL.sendToClients(('OuterRing0' + str(ScopeNumber.value)))
        ageSDL.setFlags(('OuterRing0' + str(ScopeNumber.value)), 1, 1)
        ageSDL.sendToClients(('MiddleRing0' + str(ScopeNumber.value)))
        ageSDL.setFlags(('MiddleRing0' + str(ScopeNumber.value)), 1, 1)
        ageSDL.sendToClients(('InnerRing0' + str(ScopeNumber.value)))
        ageSDL.setFlags(('InnerRing0' + str(ScopeNumber.value)), 1, 1)


    def AvatarPage(self, avObj, pageIn, lastOut):
        ageSDL = PtGetAgeSDL()
        if pageIn:
            return
        avID = PtGetClientIDFromAvatarKey(avObj.getKey())
        if (avID == ageSDL[('OperatorIDScope0' + str(ScopeNumber.value))][0]):
            Activate.enable()
            ageSDL[('OperatorIDScope0' + str(ScopeNumber.value))] = (-1,)
            ageSDL[('boolOperatedScope0' + str(ScopeNumber.value))] = (0,)
            print 'kdshTreeRings.AvatarPage(): telescope operator paged out, reenabled telescope.'
        else:
            return


    def __del__(self):
        pass


    def OnNotify(self, state, id, events):
        global LocalAvatar
        global boolScopeOperator
        ageSDL = PtGetAgeSDL()
        if (state and ((id == Activate.id) and PtWasLocallyNotified(self.key))):
            LocalAvatar = PtFindAvatar(events)
            self.IStartTelescope()
        elif (id == actResetBtn.id):
            respResetBtn.run(self.key, events=events)
        elif ((id == respResetBtn.id) and OnlyOneOwner.sceneobject.isLocallyOwned()):
            print 'kdshTreeRing Reset Button Pushed. Puzzle resetting.'
            ageSDL.setTagString('TreeRingDoorClosed', 'fromInside')
            ageSDL['TreeRingDoorClosed'] = (1,)
            for scope in [1, 2, 3]:
                ageSDL[('OuterRing0' + str(scope))] = (1,)
                ageSDL[('MiddleRing0' + str(scope))] = (1,)
                ageSDL[('InnerRing0' + str(scope))] = (1,)
        for event in events:
            if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kAdvanceNextStage))):
                if boolScopeOperator:
                    self.IEngageTelescope()
                    boolScopeOperator = 0
                break


    def OnGUINotify(self, id, control, event):
        ageSDL = PtGetAgeSDL()
        if (event == kDialogLoaded):
            return
            print ('GUI Notify id=%d, event=%d control=' % (id, event)),
            print control
            PtShowDialog(('kdshScope0' + str(ScopeNumber.value)))
            print 'kdshTreeRings: Showing scope dialog ',
            print ('kdshScope0' + str(ScopeNumber.value))
        btnID = 0
        if isinstance(control, ptGUIControlButton):
            btnID = control.getTagID()
        if (event == 5):
            return
        if (btnID == kGUIRingTurnLeft):
            newbearing = (ageSDL[('OuterRing0' + str(ScopeNumber.value))][0] + 1)
            if (newbearing == 9):
                newbearing = 1
            ageSDL[('OuterRing0' + str(ScopeNumber.value))] = (newbearing,)
        if ((btnID == kGUIRingTurnCenter) or (btnID == kGUIRingTurnLeft)):
            newbearing = (ageSDL[('MiddleRing0' + str(ScopeNumber.value))][0] + 1)
            if (newbearing == 9):
                newbearing = 1
            ageSDL[('MiddleRing0' + str(ScopeNumber.value))] = (newbearing,)
        if ((btnID == kGUIRingTurnRight) or ((btnID == kGUIRingTurnCenter) or (btnID == kGUIRingTurnLeft))):
            respSfxRings.run(self.key)
            newbearing = (ageSDL[('InnerRing0' + str(ScopeNumber.value))][0] + 1)
            if (newbearing == 9):
                newbearing = 1
            ageSDL[('InnerRing0' + str(ScopeNumber.value))] = (newbearing,)


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            self.IQuitTelescope()
        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
            self.IQuitTelescope()


    def IStartTelescope(self):
        global boolScopeOperator
        ageSDL = PtGetAgeSDL()
        PtSendKIMessage(kDisableKIandBB, 0)
        Activate.disable()
        boolScopeOperator = 1
        ageSDL[('boolOperatedScope0' + str(ScopeNumber.value))] = (1,)
        avID = PtGetClientIDFromAvatarKey(LocalAvatar.getKey())
        ageSDL[('OperatorIDScope0' + str(ScopeNumber.value))] = (avID,)
        print 'kdshTreeRings.OnNotify:\twrote SDL - scope operator id = ',
        print avID
        Behavior.run(LocalAvatar)


    def IEngageTelescope(self):
        ageSDL = PtGetAgeSDL()
        Telescope.pushTelescope()
        note = ptNotify(self.key)
        note.setActivate(1.0)
        note.addVarNumber('FastForward', ScopeNumber.value)
        note.send()
        PtEnableControlKeyEvents(self.key)
        cam = ptCamera()
        cam.undoFirstPerson()
        cam.disableFirstPersonOverride()
        virtCam = ptCamera()
        virtCam.save(Camera.sceneobject.getKey())
        PtShowDialog(('kdshScope0' + str(ScopeNumber.value)))


    def IQuitTelescope(self):
        global boolScopeOperator
        ageSDL = PtGetAgeSDL()
        Telescope.popTelescope()
        PtHideDialog(('kdshScope0' + str(ScopeNumber.value)))
        PtHideDialog(('kdshScope0' + str(ScopeNumber.value)))
        virtCam = ptCamera()
        virtCam.restore(Camera.sceneobject.getKey())
        Behavior.nextStage(LocalAvatar)
        PtDisableControlKeyEvents(self.key)
        PtSendKIMessage(kEnableKIandBB, 0)
        boolScopeOperator = 0
        ageSDL[('boolOperatedScope0' + str(ScopeNumber.value))] = (0,)
        ageSDL[('OperatorIDScope0' + str(ScopeNumber.value))] = (-1,)
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        PtAtTimeCallback(self.key, 3, 1)


    def OnTimer(self, id):
        if (id == 1):
            Activate.enable()


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



