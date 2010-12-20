# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import string
respZone01 = ptAttribActivator(1, 'Path Zone 01')
respZone02 = ptAttribActivator(2, 'Path Zone 02')
respZone03 = ptAttribActivator(3, 'Path Zone 03')
respZone04 = ptAttribActivator(4, 'Path Zone 04')
respZone05 = ptAttribActivator(5, 'Path Zone 05')
respZone06 = ptAttribActivator(6, 'Path Zone 06')
respZone07 = ptAttribActivator(7, 'Path Zone 07')
respZone08 = ptAttribActivator(8, 'Path Zone 08')
respZone09 = ptAttribActivator(9, 'Path Zone 09')
respLink = ptAttribResponder(10, 'resp: Link Out')
actResetBtn = ptAttribActivator(11, 'act: Reset Button')
respResetBtn = ptAttribResponder(12, 'resp: Reset Button')
baton = 0

class rstrShellPath(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5248
        version = 2
        self.version = version
        print '__init__rstrShellPath v.',
        print version,
        print '.0'


    def OnNotify(self, state, id, events):
        global baton
        ageSDL = PtGetAgeSDL()
        if PtWasLocallyNotified(self.key) and ((id >= 1) and (id <= 9)):
            print '##'
            for event in events:
                if (event[0] == 7):
                    break
                if (event[1] == 1):
                    print 'rstrShellPath: Entered Zone:',
                    print id
                    if (id == 1):
                        baton = 1
                    elif (id == (baton + 1)):
                        baton = (baton + 1)
                        if (baton == 9):
# Ahnonay, Myst and Kveer linking rule work-around BEGIN
                            import xLinkMgr
                            xLinkMgr.LinkToAge("Myst", "LinkInPointDefault")
                            #respLink.run(self.key, events=events)
# Ahnonay, Myst and Kveer linking rule work-around END
                            print 'rstrShellPath: Puzzle solved.'
                    elif (baton != 0):
                        baton = 0
                        print 'Baton dropped. \n'
                elif (event[1] == 0):
                    print 'rstrShellPath: Exited Zone:',
                    print id
                    if ((baton != 0) and (baton != (id + 1))):
                        print 'rstrShellPath: Dropped the baton.'
                        baton = 0
            if (baton > 0):
                print 'Baton value is now:',
                print baton
        elif (id == actResetBtn.id):
            respResetBtn.run(self.key, events=events)
        elif (id == respResetBtn.id):
            print 'rstrShellPath: The reset button in the Tree was just touched by the avatar.'
            if (ageSDL['boolTreeDayLights'][0] == 1):
                print '\tSince it was previously on, turning OFF Tree Day Cycle.'
                ageSDL.setTagString('boolTreeDayLights', 'ResetButtonInTree')
                ageSDL['boolTreeDayLights'] = (0,)
            if (ageSDL['boolBridgeExtended'][0] == 1):
                print '\tToggling the bridge to the Retracted position.'
                ageSDL.setTagString('boolBridgeExtended', 'ResetButtonInTree')
                ageSDL['boolBridgeExtended'] = (0,)
            else:
                print '\tToggling the bridge to the Extended position.'
                ageSDL.setTagString('boolBridgeExtended', 'ResetButtonInTree')
                ageSDL['boolBridgeExtended'] = (1,)
            if (ageSDL['boolSwitchAUp'][0] == 1):
                print '\tToggling SwitchA to the DOWN position.'
                ageSDL.setTagString('boolSwitchAUp', 'ResetButtonInTree')
                ageSDL['boolSwitchAUp'] = (0,)
            else:
                print '\tToggling SwitchA to the UP position.'
                ageSDL.setTagString('boolSwitchAUp', 'ResetButtonInTree')
                ageSDL['boolSwitchAUp'] = (1,)
            if (ageSDL['boolLadderRevealed'][0] == 1):
                print '\tToggling the ladder to the Concealed position.'
                ageSDL.setTagString('boolLadderRevealed', 'ResetButtonInTree')
                ageSDL['boolLadderRevealed'] = (0,)
            else:
                print '\tToggling the ladder to the Revealed position.'
                ageSDL.setTagString('boolLadderRevealed', 'ResetButtonInTree')
                ageSDL['boolLadderRevealed'] = (1,)


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



