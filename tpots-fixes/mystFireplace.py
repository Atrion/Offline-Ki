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
import xEnum
actButton = ptAttribActivator(1, 'Fireplace button')
respPressButton = ptAttribResponder(2, 'Fireplace button resp')
respFPDoor = ptAttribResponder(3, 'FP door open close', ['open', 'close'])
respFPRotate = ptAttribResponder(4, 'FP rotate', ['back', 'front'])
respResetPanel = ptAttribResponder(5, 'Reset panel', byObject=1)
actPanelButtons = ptAttribActivator(6, 'Panel buttons', byObject=1)
respMorphButtons = ptAttribResponder(7, 'Morph button resp', ['press', 'depress'], byObject=1)
strBookSDL = ptAttribString(8, 'Book SDL Var')
strYeeshaPageSDL = ptAttribString(9, 'Yeesha page SDL Var')
strByronsEggsSDL = ptAttribString(10, "Byron's Eggs SDL Var")
actExitFPClick = ptAttribActivator(11, 'FP Exit Clickable')
actExitFPRegion = ptAttribActivator(12, 'FP Exit Rgn Sensor')
respExitFP = ptAttribResponder(13, 'FP Exit Responder')
actEnterFPClick = ptAttribActivator(14, 'FP Enter Clickable')
actEnterFPRegion = ptAttribActivator(15, 'FP Enter Rgn Sensor')
respEnterFP = ptAttribResponder(16, 'FP Enter Responder')
soSubworld = ptAttribSceneobject(17, 'Subworld sceneobject')
actPanelView = ptAttribActivator(18, 'Panel view clickable')
camThirdPerson = ptAttribSceneobject(19, 'Third person cam')
camPanelView = ptAttribSceneobject(20, 'Panel camera')
respMovePanelEntry = ptAttribResponder(21, 'Move panel entry', ['up', 'down'])
CheckedButtons = []
InPanelView = 0
IgnorePanelClick = []
YeeshaPageSolution = ['A01', 'A03', 'A04', 'A05', 'A06', 'B01', 'B02', 'B05', 'B06', 'C02', 'C03', 'C06', 'D04', 'D06', 'E02', 'E05', 'E06', 'F05', 'G01', 'G02', 'G03', 'G04', 'G06', 'H01', 'H02', 'H03', 'H04']
EggSolution = ['A03', 'A04', 'B02', 'B05', 'C01', 'C03', 'C04', 'C06', 'D01', 'D03', 'D04', 'D06', 'E01', 'E06', 'F02', 'F05', 'G02', 'G05', 'H03', 'H04']
KveerSolution = ['A01', 'A05', 'B02', 'B05', 'C01', 'C04', 'D03', 'D06', 'E03', 'E05', 'F01', 'F03', 'G01', 'G03', 'G05', 'H02', 'H05']
States = xEnum.Enum('DoorOpen, DoorClosed, Rotated')
CurrentState = States.DoorClosed

class mystFireplace(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5335
        self.version = 3
        print '__init__MystFireplace v.',
        print self.version


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        if (strBookSDL.value != ''):
            ageSDL.setFlags(strBookSDL.value, 1, 1)
            ageSDL.sendToClients(strBookSDL.value)
        if (strYeeshaPageSDL.value != ''):
            ageSDL.setFlags(strYeeshaPageSDL.value, 1, 1)
            ageSDL.sendToClients(strYeeshaPageSDL.value)
        if (strByronsEggsSDL.value != ''):
            ageSDL.setFlags(strByronsEggsSDL.value, 1, 1)
            ageSDL.sendToClients(strByronsEggsSDL.value)
        ageSDL['KveerBookVis'] = (0,)
        ageSDL['YeeshaPageVis'] = (0,)
        ageSDL['ByronsEggsVis'] = (0,)


    def OnFirstUpdate(self):
        respFPDoor.run(self.key, state='close', fastforward=1)


    def OnNotify(self, state, id, events):
        print 'onnotify: id -',
        print id
        if ((id == actButton.id) and state):
            if PtWasLocallyNotified(self.key):
                self.ExitPanelView(1)
            respPressButton.run(self.key, events=events)
        elif (id == respPressButton.id):
            self.OnButtonPressed(events)
        elif ((id == actPanelButtons.id) and state):
            self.OnPanelClick(events)
        elif ((id == actExitFPClick.id) or ((id == actExitFPRegion.id) and state)):
            if PtWasLocallyNotified(self.key):
                self.ExitFireplace(events)
        elif ((id == actEnterFPClick.id) or ((id == actEnterFPRegion.id) and state)):
            if PtWasLocallyNotified(self.key):
                self.EnterFireplace(events)
        elif ((id == actPanelView.id) and state):
            if PtWasLocallyNotified(self.key):
                self.EnterPanelView(events)
        elif (id == respMorphButtons.id):
            if (len(IgnorePanelClick) > 0):
                id = IgnorePanelClick[0]
                del IgnorePanelClick[0]
                for (rkey, rvalue) in actPanelButtons.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        pname = parent.getName()
                        if (id == pname[-3:]):
                            rvalue.enable()
                            break
        elif ((id == respEnterFP.id) or (id == respExitFP.id)):
            cam = ptCamera()
            cam.enableFirstPersonOverride()


    def OnButtonPressed(self, events):
        global CurrentState
        if (CurrentState == States.DoorOpen):
            respFPDoor.run(self.key, state='close')
            respMovePanelEntry.run(self.key, state='down', fastforward=1)
            CurrentState = States.DoorClosed
        elif (CurrentState == States.DoorClosed):
            actPanelView.disable()
            ageSDL = PtGetAgeSDL()
            if self.CheckForSolution(KveerSolution):
                vault = ptVault()
                entry = vault.findChronicleEntry('Blah')
                if (not entry):
                    vault.addChronicleEntry('Blah', 0, '1')
                elif (int(entry.chronicleGetValue()) < 1):
                    entry.chronicleSetValue('1')
                ageSDL['KveerBookVis'] = (1,)
                ageSDL['YeeshaPageVis'] = (0,)
                ageSDL['ByronsEggsVis'] = (0,)
                respFPRotate.run(self.key, state='back')
                CurrentState = States.Rotated
            elif self.CheckForSolution(YeeshaPageSolution):
                ageSDL['KveerBookVis'] = (0,)
                ageSDL['YeeshaPageVis'] = (1,)
                ageSDL['ByronsEggsVis'] = (0,)
                respFPRotate.run(self.key, state='back')
                CurrentState = States.Rotated
            elif self.CheckForSolution(EggSolution):
                ageSDL['KveerBookVis'] = (0,)
                ageSDL['YeeshaPageVis'] = (0,)
                ageSDL['ByronsEggsVis'] = (1,)
                respFPRotate.run(self.key, state='back')
                CurrentState = States.Rotated
            else:
                ageSDL['KveerBookVis'] = (0,)
                ageSDL['YeeshaPageVis'] = (0,)
                ageSDL['ByronsEggsVis'] = (0,)
                respFPDoor.run(self.key, state='open')
                respMovePanelEntry.run(self.key, state='up', fastforward=1)
                CurrentState = States.DoorOpen
        elif (CurrentState == States.Rotated):
            respFPRotate.run(self.key, state='front')
            CurrentState = States.DoorClosed
        self.ResetPanel()


    def OnPanelClick(self, events):
        for event in events:
            if (event[0] == kPickedEvent):
                panelPicked = event[3]
                panelName = panelPicked.getName()
                try:
                    id = panelName[-3:]
                except:
                    PtDebugPrint("mystFirePlace.OnPanelClick: Couldn't extract the panel id...not responding to click")
                    return
                if (id in IgnorePanelClick):
                    return
                else:
                    IgnorePanelClick.append(id)
                    for (rkey, rvalue) in actPanelButtons.byObject.items():
                        parent = rvalue.getParentKey()
                        if parent:
                            pname = parent.getName()
                            if (id == pname[-3:]):
                                rvalue.disable()
                                break
                if (id in CheckedButtons):
                    bstate = 'depress'
                    CheckedButtons.remove(id)
                else:
                    bstate = 'press'
                    CheckedButtons.append(id)
                print panelName,
                print bstate
                for (rkey, rvalue) in respMorphButtons.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        pname = parent.getName()
                        if (id == pname[-3:]):
                            respMorphButtons.run(self.key, objectName=rkey, state=bstate)
                            break
                break


    def EnterFireplace(self, events):
        cam = ptCamera()
        cam.undoFirstPerson()
        cam.disableFirstPersonOverride()
        respEnterFP.run(self.key, events=events)


    def ExitFireplace(self, events):
        cam = ptCamera()
        cam.undoFirstPerson()
        cam.disableFirstPersonOverride()
        PtFadeLocalAvatar(0)
        respExitFP.run(self.key, events=events)


    def EnterPanelView(self, events):
        global InPanelView
        actPanelView.disable()
        InPanelView = 1
        PtDisableMovementKeys()
        PtGetControlEvents(1, self.key)
        av = PtGetLocalAvatar()
        PtRecenterCamera()
        camPanelView.sceneobject.pushCutsceneCamera(0, av.getKey())
        av = PtGetLocalAvatar()
        av.draw.disable()
        cam = ptCamera()
        cam.disableFirstPersonOverride()
        respMovePanelEntry.run(self.key, state='up', fastforward=1)
        PtDisableMovementKeys()
        PtGetControlEvents(1, self.key)


    def ExitPanelView(self, buttonClicked):
        global InPanelView
        if InPanelView:
            respMovePanelEntry.run(self.key, state='down', fastforward=1)
            av = PtGetLocalAvatar()
            av.draw.enable()
            cam = ptCamera()
            cam.enableFirstPersonOverride()
            camPanelView.sceneobject.popCutsceneCamera(av.getKey())
            PtEnableMovementKeys()
            PtGetControlEvents(0, self.key)
            if (not (buttonClicked)):
                actPanelView.enable()
            InPanelView = 0


    def CheckForSolution(self, solution):
        CheckedButtons.sort()
        solution.sort()
        print 'CheckedButtons:',
        print CheckedButtons
        print 'solution      :',
        print solution
        return (CheckedButtons == solution)


    def ResetPanel(self):
        global CheckedButtons
        global IgnorePanelClick
        for but in CheckedButtons:
            id = but[-3:]
            for (rkey, rvalue) in respMorphButtons.byObject.items():
                parent = rvalue.getParentKey()
                if parent:
                    pname = parent.getName()
                    if (id == pname[-3:]):
                        respMorphButtons.run(self.key, objectName=rkey, state='depress')
                        break
        CheckedButtons = []
        IgnorePanelClick = []


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if InPanelView:
            if ((controlKey == PlasmaControlKeys.kKeyExitMode) or (controlKey == PlasmaControlKeys.kKeyMoveBackward)):
                self.ExitPanelView(0)


    def OnBackdoorMsg(self, target, param):
        global CheckedButtons
        global CurrentState
        if (target == 'fp'):
            if (param == 'dooropen'):
                respFPDoor.run(self.key, state='open')
                CurrentState = States.DoorOpen
            elif (param == 'kveer'):
                CheckedButtons = KveerSolution
            elif (param == 'yeeshapage'):
                CheckedButtons = YeeshaPageSolution
            elif (param == 'eggs'):
                CheckedButtons = EggSolution
            elif (param == 'open'):
                CheckedButtons = []


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



