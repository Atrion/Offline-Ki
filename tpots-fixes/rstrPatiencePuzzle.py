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
import string
actSwitchA = ptAttribActivator(1, 'Act: Switch A')
actButtonB = ptAttribActivator(2, 'Act: Button B')
actButtonC = ptAttribActivator(3, 'Act: Button C')
actButtonD = ptAttribActivator(4, 'Act: Button D')
rgnPatienceZone = ptAttribActivator(5, 'Act: Patience Zone')
respTickSfxOn = ptAttribResponder(6, 'resp: Tick Sfx On')
respTickSfxOff = ptAttribResponder(7, 'resp: Tick Sfx Off')
respGizmoButtonOneshot = ptAttribResponder(8, 'resp: GizmoButton Oneshot')
respPlungeBall = ptAttribResponder(9, 'resp: Plunge Ball')
respRevealLadder = ptAttribResponder(10, 'resp: Reveal Ladder')
respConcealLadder = ptAttribResponder(11, 'resp: Conceal Ladder')
respExtendBridge = ptAttribResponder(12, 'resp: Extend Bridge')
respRetractBridge = ptAttribResponder(13, 'resp: Retract Bridge')
respButtonDEnable = ptAttribResponder(14, 'resp: Button D Enable')
respButtonDDisable = ptAttribResponder(15, 'resp: Button D Disable')
respDoorClose = ptAttribResponder(16, 'resp: Close Door')
respDoorOpen = ptAttribResponder(17, 'resp: Open Door')
SwitchAUpOneshot = ptAttribResponder(18, 'resp: SwitchAUp Oneshot')
SwitchADownOneshot = ptAttribResponder(19, 'resp: SwitchADown Oneshot')
respSwitchAUp = ptAttribResponder(20, 'resp: SwitchAUp Results')
respSwitchADown = ptAttribResponder(21, 'resp: SwitchADown Results')
respDoorButtonOneshot = ptAttribResponder(22, 'resp: Door Button Oneshot')
respEnableDoorButton = ptAttribResponder(23, 'resp: Enable Door Button')
respDisableDoorButton = ptAttribResponder(24, 'resp: Disable Door Button')
boolLadderRevealed = 0
boolInPatienceZone = 0
kPatienceTime = 870
boolStillInPatienceZone = 0
class rstrPatiencePuzzle(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5247
        version = 4
        self.version = version
        print '__init__rstrPatiencePuzzle v. ',
        print version,
        print '.0'


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        ageSDL.sendToClients('boolSwitchAUp')
        ageSDL.sendToClients('boolLadderRevealed')
        ageSDL.sendToClients('boolBridgeExtended')
        ageSDL.sendToClients('boolFirstTimeHere')
        ageSDL.setFlags('boolSwitchAUp', 1, 1)
        ageSDL.setFlags('boolLadderRevealed', 1, 1)
        ageSDL.setFlags('boolBridgeExtended', 1, 1)
        ageSDL.setFlags('boolFirstTimeHere', 1, 1)
        ageSDL.setNotify(self.key, 'boolSwitchAUp', 0.0)
        ageSDL.setNotify(self.key, 'boolLadderRevealed', 0.0)
        ageSDL.setNotify(self.key, 'boolBridgeExtended', 0.0)
        ageSDL.setNotify(self.key, 'boolFirstTimeHere', 0.0)
        boolSwitchAUp = ageSDL['boolSwitchAUp'][0]
        print 'rstrPatiencePuzzle: When I got here:'
        if boolSwitchAUp:
            print '\tSwitchA is up, so the Door should be DOWN.'
            respSwitchAUp.run(self.key, fastforward=1)
            respDoorClose.run(self.key, fastforward=1)
            respButtonDEnable.run(self.key, fastforward=1)
            TimeEnteredPatienceZone = ageSDL['TimeEnteredPatienceZone'][0]
            CurrentTime = PtGetDniTime()
            PtClearTimerCallbacks(self.key)
            if (ageSDL['boolFirstTimeHere'][0] == 1):
                print "\tYou've never opened the ball room door, so we don't care about the timer."
            elif (ageSDL['boolLadderRevealed'][0] == 1):
                print "\tThe ladder WAS revealed when we got here, so we don't care about the timer."
            elif ((CurrentTime - TimeEnteredPatienceZone) < kPatienceTime):
                print ('\tThe Patience Timer will expire in %d seconds.' % (kPatienceTime - (CurrentTime - TimeEnteredPatienceZone)))
                PtAtTimeCallback(self.key, (kPatienceTime - (CurrentTime - TimeEnteredPatienceZone)), 1)
                respTickSfxOn.run(self.key)
            else:
                print '\tThe Patience Timer expired in the time nobody was here.'
                ageSDL['boolSwitchAUp'] = (0,)
                ageSDL['boolLadderRevealed'] = (0,)
        else:
            print '\tSwitchA is down, so the Door should be UP.'
            respButtonDDisable.run(self.key, fastforward=1)
            respSwitchADown.run(self.key, fastforward=1)
            respDoorOpen.run(self.key, fastforward=1)
            actButtonD.disable()
        if (ageSDL['boolLadderRevealed'][0] == 1):
            if (not boolSwitchAUp):
                print "\tERROR: The ladder shouldn't be revealed if the door is open. I'll conceal it now."
                ageSDL['boolLadderRevealed'] = (0,)
            else:
                print '\tThe Ladder is revealed.'
                respRevealLadder.run(self.key, fastforward=1)
        else:
            print '\tThe ladder is not revealed.'
        if (ageSDL['boolBridgeExtended'][0] == 1):
            print '\tThe Bridge was already extended.'
            respExtendBridge.run(self.key, fastforward=1)
        elif (ageSDL['boolBridgeExtended'][0] == 0):
            print '\tThe Bridge was not extended.'


    def OnNotify(self, state, id, events):
        global boolInPatienceZone
        global boolStillInPatienceZone
        ageSDL = PtGetAgeSDL()
        if (not state):
            return
        if ((id == rgnPatienceZone.id) and (not boolLadderRevealed) and (PtWasLocallyNotified(self.key))):
            for event in events:
                if (event[1] == 0):
                    print 'The avatar just walked out of the Patience Zone'
                    boolInPatienceZone = 0
                    boolStillInPatienceZone = 0
                    break
                elif (event[1] == 1):
                    print 'The avatar just walked into the Patience Zone'
                    boolInPatienceZone = 1
                    break
            return
        elif (id == actSwitchA.id):
            boolSwitchAUp = ageSDL['boolSwitchAUp'][0]
            if boolSwitchAUp:
                SwitchADownOneshot.run(self.key, events=events)
            else:
                SwitchAUpOneshot.run(self.key, events=events)
        elif (id == SwitchADownOneshot.id):
            print 'Avatar finished pushing LeverA DOWN.'
            respSwitchADown.run(self.key)
            ageSDL.setTagString('boolSwitchAUp', 'foo')
            ageSDL['boolSwitchAUp'] = (0,)
        elif (id == SwitchAUpOneshot.id):
            print 'Avatar finished pushing LeverA UP.'
            boolStillInPatienceZone = 1
            respSwitchAUp.run(self.key)
            ageSDL.setTagString('boolSwitchAUp', 'foo')
            ageSDL['boolSwitchAUp'] = (1,)
        elif (id == actButtonB.id):
            print 'The Gizmo button was just clicked.'
            respGizmoButtonOneshot.run(self.key, events=events)
        elif (id == respGizmoButtonOneshot.id):
            print 'The Avatar just finished pushing the Gizmo button.'
            ageSDL['boolBridgeExtended'] = (1,)
            ageSDL['boolTreeDayLights'] = (1,)
            return
        elif (id == actButtonC.id):
            print 'The Button inside the great tree has just been manipulated.'
            return
        elif (id == actButtonD.id):
            respDoorButtonOneshot.run(self.key, events=events)
        elif (id == respDoorButtonOneshot.id):
            print 'D touched by avatar. Waiting 10 seconds to open the door.'
            PtAtTimeCallback(self.key, 10, 2)
            if (ageSDL['boolFirstTimeHere'][0] == 1):
                print "\tThat was the first time you've ever opened the ball room door."
                ageSDL['boolFirstTimeHere'] = (0,)
            return


    def RecordZoneEnterTime(self):
        ageSDL = PtGetAgeSDL()
        CurrentTime = PtGetDniTime()
        ageSDL['TimeEnteredPatienceZone'] = (CurrentTime,)


    def OnTimer(self, id):
        ageSDL = PtGetAgeSDL()
        if (id == 1):
            print 'rstrPatiencePuzzle: You started the Patience Timer',
            print kPatienceTime,
            print 'seconds ago.'
            if (not boolStillInPatienceZone):
                print '\tBut you are not currently in the zone.'
                ageSDL['boolSwitchAUp'] = (0,)
                return
            else:
                TimeEnteredPatienceZone = ageSDL['TimeEnteredPatienceZone'][0]
                CurrentTime = PtGetDniTime()
                print '\tYou are currently in the zone.'
                ElapsedTime = (CurrentTime - TimeEnteredPatienceZone)
                if (ElapsedTime >= kPatienceTime):
                    print '\tAnd you HAVE been in the zone for',
                    print kPatienceTime,
                    print 'consecutive seconds. Puzzle solved.'
                    print '\tReveal Ladder, Door stays closed, Lights stay on, Switch A stays up, ticking stops, plunge ball'
                    ageSDL['boolLadderRevealed'] = (1,)
                    respTickSfxOff.run(self.key)
                    respPlungeBall.run(self.key)
                else:
                    print '\tBut you have NOT been in the zone for',
                    print kPatienceTime,
                    print 'consecutive seconds.'
                    ageSDL['boolSwitchAUp'] = (0,)
        elif (id == 2):
            ageSDL.setTagString('boolSwitchAUp', 'ButtonDPushed')
            ageSDL['boolSwitchAUp'] = (0,)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        print 'OnSDLNotify: VARname =',
        print VARname,
        print ' value =',
        print ageSDL[VARname][0],
        print ' tag =',
        print tag
        if (VARname == 'boolSwitchAUp'):
            boolSwitchAUp = ageSDL['boolSwitchAUp'][0]
            if boolSwitchAUp:
                print '\tTimer Starts, Tick Sfx starts, Door closes, lights on, plunge ball'
                boolInPatienceZone = 1
                PtAtTimeCallback(self.key, kPatienceTime, 1)
                self.RecordZoneEnterTime()
                respTickSfxOn.run(self.key)
                respDoorClose.run(self.key)
                respPlungeBall.run(self.key)
            else:
                print '\tTimer Stops, Tick Sfx stops, Door opens, lights off, Switch A down'
                PtClearTimerCallbacks(self.key)
                respTickSfxOff.run(self.key)
                respDoorOpen.run(self.key)
                respSwitchADown.run(self.key)
                boolLadderRevealed = ageSDL['boolLadderRevealed'][0]
                if ageSDL['boolLadderRevealed'][0]:
                    print '\tAlso putting away ladder.'
                    ageSDL['boolLadderRevealed'] = (0,)
                if (tag == 'ButtonDPushed'):
                    boolTreeDayLights = ageSDL['boolTreeDayLights'][0]
                    if boolTreeDayLights:
                        print '\tBecause D was pushed, turning off day.'
                        ageSDL['boolTreeDayLights'] = (0,)
                    boolBridgeExtended = ageSDL['boolBridgeExtended'][0]
                    if boolBridgeExtended:
                        print '\tBecause D was pushed, retracting bridge.'
                        ageSDL['boolBridgeExtended'] = (0,)
        elif (VARname == 'boolBridgeExtended'):
            if (ageSDL['boolBridgeExtended'][0] == 1):
                print '\tExtending bridge'
                respExtendBridge.run(self.key)
            elif (ageSDL['boolBridgeExtended'][0] == 0):
                respRetractBridge.run(self.key)
                print '\tRetracting bridge'
        elif (VARname == 'boolLadderRevealed'):
            if (ageSDL['boolLadderRevealed'][0] == 1):
                print '\tRevealing ladder.'
                respRevealLadder.run(self.key)
            else:
                print '\tConcealing ladder.'
                respConcealLadder.run(self.key)


    def AvatarPage(self, avObj, pageIn, lastOut):
# Skip other Avatar's page out
        if (PtGetClientIDFromAvatarKey(avObj.getKey()) != PtGetLocalClientID()): return
# END Skip other Avatar's page out
        if (not (pageIn)):
            print 'rstrPatiencePuzzle: Turning off Patience Timer.'
            PtClearTimerCallbacks(self.key)


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



