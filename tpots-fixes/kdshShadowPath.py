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
import string
actSwitch01 = ptAttribActivator(1, 'Actvr: Switch 01')
actSwitch02 = ptAttribActivator(2, 'Actvr: Switch 02')
actSwitch03 = ptAttribActivator(3, 'Actvr: Switch 03')
actSwitch04 = ptAttribActivator(4, 'Actvr: Switch 04')
actSwitch05 = ptAttribActivator(5, 'Actvr: Switch 05')
respSwitch01 = ptAttribResponder(6, 'Rspndr: Switch 01', ['on', 'off'])
respSwitch02 = ptAttribResponder(7, 'Rspndr: Switch 02', ['on', 'off'])
respSwitch03 = ptAttribResponder(8, 'Rspndr: Switch 03', ['on', 'off'])
respSwitch04 = ptAttribResponder(9, 'Rspndr: Switch 04', ['on', 'off'])
respSwitch05 = ptAttribResponder(10, 'Rspndr: Switch 05', ['on', 'off'])
respZone01 = ptAttribActivator(11, 'Stair Zone 01')
respZone02 = ptAttribActivator(12, 'Stair Zone 02')
respZone03 = ptAttribActivator(13, 'Stair Zone 03')
respZone04 = ptAttribActivator(14, 'Stair Zone 04')
respZone05 = ptAttribActivator(15, 'Stair Zone 05')
respZone06 = ptAttribActivator(16, 'Stair Zone 06')
respZone07 = ptAttribActivator(17, 'Stair Zone 07')
respZone08 = ptAttribActivator(18, 'Stair Zone 08')
respZone09 = ptAttribActivator(19, 'Stair Zone 09')
respZone10 = ptAttribActivator(20, 'Stair Zone 10')
RevealStairs = ptAttribResponder(21, 'resp:Open Floor')
FloorZone = ptAttribActivator(22, 'Floor Zone')
actResetBtn = ptAttribActivator(23, 'act:Reset Button')
respResetBtn = ptAttribResponder(24, 'resp:Reset Button')
ConcealStairs = ptAttribResponder(25, 'resp:Close Floor')
respBtnPush01 = ptAttribResponder(26, 'resp:Btn Push 01')
respBtnPush02 = ptAttribResponder(27, 'resp:Btn Push 02')
respBtnPush03 = ptAttribResponder(28, 'resp:Btn Push 03')
respBtnPush04 = ptAttribResponder(29, 'resp:Btn Push 04')
respBtnPush05 = ptAttribResponder(30, 'resp:Btn Push 05')
OnlyOneOwner = ptAttribSceneobject(31, 'OnlyOneOwner')
baton = 0
TwoOnFloor = false

class kdshShadowPath(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5211
        version = 10
        self.version = version
        print '__init__kdshShadowPath v.',
        print version,
        print '.2'


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        ageSDL.setNotify(self.key, 'ShadowPathLight01', 0.0)
        ageSDL.setNotify(self.key, 'ShadowPathLight02', 0.0)
        ageSDL.setNotify(self.key, 'ShadowPathLight03', 0.0)
        ageSDL.setNotify(self.key, 'ShadowPathLight04', 0.0)
        ageSDL.setNotify(self.key, 'ShadowPathLight05', 0.0)
        ageSDL.setNotify(self.key, 'ShadowPathSolved', 0.0)
        ageSDL.sendToClients('ShadowPathLight01')
        ageSDL.sendToClients('ShadowPathLight02')
        ageSDL.sendToClients('ShadowPathLight03')
        ageSDL.sendToClients('ShadowPathLight04')
        ageSDL.sendToClients('ShadowPathLight05')
        ageSDL.sendToClients('ShadowPathSolved')
        ageSDL.setFlags('ShadowPathLight01', 1, 1)
        ageSDL.setFlags('ShadowPathLight02', 1, 1)
        ageSDL.setFlags('ShadowPathLight03', 1, 1)
        ageSDL.setFlags('ShadowPathLight04', 1, 1)
        ageSDL.setFlags('ShadowPathLight05', 1, 1)
        ageSDL.setFlags('ShadowPathSolved', 1, 1)
        print 'kdshShadowPath: When I got here:'
        for light in [1, 2, 3, 4, 5]:
            lightstate = ageSDL[('ShadowPathLight0' + str(light))][0]
            print ('\t ShadowPathLight0%s = %s ' % (light, lightstate))
            if (lightstate == 1):
                code = (('respSwitch0' + str(light)) + '.run(self.key,fastforward=1)')
                exec code
                print '\t\tTurning on light #',
                print light
        solved = ageSDL['ShadowPathSolved'][0]
        if solved:
            print '\tThe Shadow Path was already solved. Revealing stairs.'
            RevealStairs.run(self.key, fastforward=1)


    def Load(self):
        count = 1
        while (count < 5):
            print 'kdshShadowPath.Load(): ageSDL[ShadowPathLight0',
            print count,
            print (']=%d' % ageSDL[('ShadowPathLight0' + str(count))][0])
            count = (count + 1)


    def OnNotify(self, state, id, events):
        global baton
        global TwoOnFloor
        ageSDL = PtGetAgeSDL()
        if (id == FloorZone.id):
            for event in events:
                if (event[0] == 7):
                    return
                if (event[1] == 1):
                    TwoOnFloor = true
                    baton = 0
                elif (event[1] == 0):
                    TwoOnFloor = false
            print 'kdshShadowPath.OnNotify: TwoOnFloor = ',
            print TwoOnFloor
        elif (id in [1, 2, 3, 4, 5]):
            if (not state):
                return
            print 'Light ',
            print id,
            print ' clicked.'
            code = (('respBtnPush0' + str(id)) + '.run(self.key,events=events)')
            exec code
            return
        elif ((id in [26, 27, 28, 29, 30]) and OnlyOneOwner.sceneobject.isLocallyOwned()):
            print 'Light ',
            print (id - 25),
            print 'actually touched by avatar.'
            oldstate = ageSDL[('ShadowPathLight0' + str((id - 25)))][0]
            newstate = abs((oldstate - 1))
            ageSDL[('ShadowPathLight0' + str((id - 25)))] = (newstate,)
            return
        elif ((id >= 11) and (id <= 21)):
            if TwoOnFloor:
                print 'kdshShadowPath.OnNotify: No progress, since TwoOnFloor = ',
                print TwoOnFloor
                return
            if PtWasLocallyNotified(self.key):
                self.BatonPassCheck(id, events, ageSDL)
        elif (state and (id == actResetBtn.id)):
            print 'kdshShadowPath Reset Button clicked.'
            LocalAvatar = PtFindAvatar(events)
            respResetBtn.run(self.key, events=events)
        elif ((id == respResetBtn.id) and OnlyOneOwner.sceneobject.isLocallyOwned()):
            print 'kdshShadowPath Reset Button Pushed. Puzzle resetting.'
            for light in [1, 2, 3, 4, 5]:
                lightstate = ageSDL[('ShadowPathLight0' + str(light))][0]
                if (lightstate == 1):
                    if (light == 1):
                        ageSDL['ShadowPathLight01'] = (0,)
                    elif (light == 2):
                        ageSDL['ShadowPathLight02'] = (0,)
                    elif (light == 3):
                        ageSDL['ShadowPathLight03'] = (0,)
                    elif (light == 4):
                        ageSDL['ShadowPathLight04'] = (0,)
                    elif (light == 5):
                        ageSDL['ShadowPathLight05'] = (0,)
                    print '\tTurning off light #',
                    print light
            ageSDL['ShadowPathSolved'] = (0,)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        if (VARname == 'ShadowPathSolved'):
            if (ageSDL['ShadowPathSolved'][0] == 1):
                print 'kdshShadowPath: Opening floor'
                RevealStairs.run(self.key)
                respZone10.disable(self.key)
            else:
                print 'kdshShadowPath: Closing floor'
                ConcealStairs.run(self.key)
                respZone10.enable(self.key)
        elif (VARname[:15] == 'ShadowPathLight'):
            light = string.atoi(VARname[-2:])
            newstate = ageSDL[('ShadowPathLight0' + str(light))][0]
            if (newstate == 0):
                print 'kdshShadowPath.OnSDLNotify: Light',
                print light,
                print ' was on. Turning it off.'
                code = (('respSwitch0' + str(light)) + ".run(self.key, state='off')")
                exec code
            elif (newstate == 1):
                print 'kdshShadowPath.OnSDLNotify: Light',
                print light,
                print ' was off. Turning it on.'
                code = (('respSwitch0' + str(light)) + ".run(self.key, state='on')")
                exec code
            else:
                print 'Error. Not sure what the light thought it was.'


    def BatonPassCheck(self, id, events, ageSDL):
        global baton
        print '##'
        for event in events:
            if (event[0] == 7):
                break
            if (event[1] == 1):
                print 'kdshShadowPath: Entered Zone:',
                print (id - 10)
                if (id == 11):
                    baton = 1
                elif (id == (baton + 11)):
                    baton = (baton + 1)
                    if (baton == 10):
                        print 'kdshShadowPath: Puzzle solved.'
                        ageSDL['ShadowPathSolved'] = (1,)
                elif (baton != 0):
                    baton = 0
                    print 'Baton dropped. \n'
            elif (event[1] == 0):
                print 'kdshShadowPath: Exited Zone:',
                print (id - 10)
                if ((baton != 0) and (baton != (id - 9))):
                    print 'kdshShadowPath: Dropped the baton.'
                    baton = 0
        if (baton > 0):
            print 'Baton value is now:',
            print baton


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



