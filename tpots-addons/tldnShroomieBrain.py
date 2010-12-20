# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import whrandom
actLever = ptAttribActivator(1, 'act: Feeder Lever')
rgnShore01 = ptAttribActivator(2, 'act: Along Shore01')
rgnShore02 = ptAttribActivator(3, 'act: Along Shore02')
rgnShore03 = ptAttribActivator(4, 'act: Along Shore03')
SpawnFar01 = ptAttribSceneobject(5, 'spawnpt: Far 01')
SpawnFar02 = ptAttribSceneobject(6, 'spawnpt: Far 02')
SpawnFar03 = ptAttribSceneobject(7, 'spawnpt: Far 03')
SpawnFar04 = ptAttribSceneobject(8, 'spawnpt: Far 04')
SpawnFar05 = ptAttribSceneobject(9, 'spawnpt: Far 05')
SpawnMid01 = ptAttribSceneobject(10, 'spawnpt: Med 01')
SpawnMid02 = ptAttribSceneobject(11, 'spawnpt: Med 02')
SpawnMid03 = ptAttribSceneobject(12, 'spawnpt: Med 03')
SpawnMid04 = ptAttribSceneobject(13, 'spawnpt: Med 04')
SpawnMid05 = ptAttribSceneobject(14, 'spawnpt: Med 05')
SpawnNear01 = ptAttribSceneobject(15, 'spawnpt: Near 01')
SpawnNear02 = ptAttribSceneobject(16, 'spawnpt: Near 02')
SpawnNear03 = ptAttribSceneobject(17, 'spawnpt: Near 03')
SpawnNear04 = ptAttribSceneobject(18, 'spawnpt: Near 04')
SpawnNear05 = ptAttribSceneobject(19, 'spawnpt: Near 05')
respTrick01 = ptAttribResponder(20, 'Shroomie Trick #1')
respTrick02 = ptAttribResponder(21, 'Shroomie Trick #2')
respTrick03 = ptAttribResponder(22, 'Shroomie Trick #3')
respTrick04 = ptAttribResponder(23, 'Shroomie Trick #4')
ShroomieMaster = ptAttribSceneobject(24, 'Shroomie Dummmy')
respVisible = ptAttribResponder(25, 'resp: Shroomie Visible')
respInvisible = ptAttribResponder(26, 'resp: Shroomie Invisible')
LeverProb = 0.25
Shore01Prob = 0.10000000000000001
Shore02Prob = 0.10000000000000001
Shore03Prob = 0.10000000000000001
Delay1Min = 180
Dealy1Max = 600
Delay2Min = 180
Delay2Max = 600
Delay3Min = 300
Delay3Max = 600
Delay4Min = 300
Delay4Max = 600
ShroomieTotalTimesSeen = 0
ShroomieTimeLastSeen = 0

class tldnShroomieBrain(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5237
        version = 3
        self.version = version
        print '__init__tldnShroomieBrain v.',
        print version,
        print '.2'


    def OnFirstUpdate(self):
        whrandom.seed()


    def OnServerInitComplete(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            print 'tldnShroomieBrain:\tERROR---Cannot find the Teledahn Age SDL'
            ageSDL['ShroomieTotalTimesSeen'] = (0,)
            ageSDL['ShroomieTimeLastSeen'] = (0,)
        ageSDL.sendToClients('ShroomieTotalTimesSeen')
        ageSDL.sendToClients('ShroomieTimeLastSeen')
        ageSDL.setFlags('ShroomieTotalTimesSeen', 1, 1)
        ageSDL.setFlags('ShroomieTimeLastSeen', 1, 1)
        ShroomieTotalTimesSeen = ageSDL['ShroomieTotalTimesSeen'][0]
        ShroomieTimeLastSeen = ageSDL['ShroomieTimeLastSeen'][0]
        print 'tldnShroomieBrain: When I got here:'
        print '\tShroomie has been seen',
        print ShroomieTotalTimesSeen,
        print ' times.'
        if ShroomieTotalTimesSeen:
            CurrentTime = PtGetDniTime()
            print '\tShroomie was last seen ',
            print (CurrentTime - ShroomieTimeLastSeen),
            print ' seconds ago.'


    def OnNotify(self, state, id, events):
        ageSDL = PtGetAgeSDL()
        if (not (state)):
            return
        if (id in [1, 2, 3, 4]):
            CurrentTime = PtGetDniTime()
            if self.CanShroomieBeSeen(CurrentTime):
                if (id == actLever.id):
                    if self.WillShroomieBeSeen(LeverProb):
                        self.ShroomieSurfaces(1)
                elif (id == rgnShore01.id):
                    if self.WillShroomieBeSeen(Shore01Prob):
                        self.ShroomieSurfaces(2)
                elif (id == rgnShore02.id):
                    if self.WillShroomieBeSeen(Shore02Prob):
                        self.ShroomieSurfaces(3)
                elif (id == rgnShore03.id):
                    if self.WillShroomieBeSeen(Shore03Prob):
                        self.ShroomieSurfaces(4)
        elif (id in [20, 21, 22, 23]):
            respInvisible.run(self.key)


    def CanShroomieBeSeen(self, CurrentTime):
        return true # CHANGED
        ageSDL = PtGetAgeSDL()
        CurrentTime = PtGetDniTime()
        ShroomieTimeLastSeen = ageSDL['ShroomieTimeLastSeen'][0]
        print 'tldnShroomieBrain: Shroomie was last seen',
        print (CurrentTime - ShroomieTimeLastSeen),
        print ' seconds ago.'
        if ((CurrentTime - ShroomieTimeLastSeen) > 240):
            print '\tShroomie CAN be seen.'
            return true
        else:
            print '\tShroomie CAN\'T be seen.'
            return false


    def WillShroomieBeSeen(self, probability):
        probability = probability*3 # CHANGED
        randnum = whrandom.randint(0, 100)
        if (randnum < (probability * 100)):
            print '\t Shroomie WILL be seen.'
            return true
        else:
            print '\tShroomie WON\'T be seen.'


    def ShroomieSurfaces(self, spawn):
        ageSDL = PtGetAgeSDL()
        respVisible.run(self.key)
        if (spawn == 1):
            tldnMainPowerOn = ageSDL['tldnMainPowerOn'][0]
            whichbehavior = whrandom.randint(1, 4)
            if tldnMainPowerOn:
                print 'tldnShroomieBrain: The Power Tower noise has scared Shroomie. He\'ll come, but not very close.'
                NearOrFar = 'Far'
            else:
                print 'tldnShroomieBrain: The Power Tower is down, so Shroomie isn\'t scared by the noise.'
                howclose = whrandom.randint(1, 100)
                if (howclose == 1):
                    NearOrFar = 'Near'
                elif ((howclose > 1) and (howclose < 50)):
                    NearOrFar = 'Mid'
                elif (howclose >= 50):
                    NearOrFar = 'Far'
        else:
            whichbehavior = whrandom.randint(2, 4)
            NearOrFar = 'Far'
        print 'tldnShroomieBrain: whichbehavior = ',
        print whichbehavior,
        print ' NearOrFar = ',
        print NearOrFar
        whichspawnpoint = whrandom.randint(1, 5)
        if (NearOrFar == 'Near'):
            code = (('target = SpawnNear0' + str(whichspawnpoint)) + '.sceneobject.getKey()')
        elif (NearOrFar == 'Mid'):
            code = (('target = SpawnMid0' + str(whichspawnpoint)) + '.sceneobject.getKey()')
        elif (NearOrFar == 'Far'):
            code = (('target = SpawnFar0' + str(whichspawnpoint)) + '.sceneobject.getKey()')
        print 'target code:',
        print code
        exec code
        ShroomieMaster.sceneobject.physics.warpObj(target)
        code = (('respTrick0' + str(whichbehavior)) + '.run(self.key)')
        exec code
        CurrentTime = PtGetDniTime()
        ageSDL['ShroomieTimeLastSeen'] = (CurrentTime,)
        ShroomieTotalTimesSeen = ageSDL['ShroomieTotalTimesSeen'][0]
        ShroomieTotalTimesSeen = (ShroomieTotalTimesSeen + 1)
        ageSDL['ShroomieTotalTimesSeen'] = (ShroomieTotalTimesSeen,)
        print 'tldnShroomieBrain: Shroomie has been seen',
        print ShroomieTotalTimesSeen,
        print 'times.'


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



