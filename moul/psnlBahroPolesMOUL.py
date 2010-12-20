# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaVaultConstants import *
import xEnum
from xPsnlVaultSDL import *
import xxConfig
clickTeledahnPole = ptAttribActivator(1, 'Teledahn clickable')
clickGarrisonPole = ptAttribActivator(2, 'Garrison clickable')
clickGardenPole = ptAttribActivator(3, 'Garden clickable')
clickKadishPole = ptAttribActivator(4, 'Kadish clickable')
respTeledahnPole = ptAttribResponder(5, 'Teledahn responder', ['0',
 '1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 '8',
 '9'])
respGarrisonPole = ptAttribResponder(6, 'Garrison responder', ['0',
 '1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 '8',
 '9'])
respGardenPole = ptAttribResponder(7, 'Garden responder', ['0',
 '1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 '8',
 '9'])
respKadishPole = ptAttribResponder(8, 'Kadish responder', ['0',
 '1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 '8',
 '9'])
respTeledahnHandGlow = ptAttribResponder(9, 'Teledahn hand glow', ['1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 'DropSheath',
 'ResetSheath'])
respGarrisonHandGlow = ptAttribResponder(10, 'Garrison hand glow', ['1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 'DropSheath',
 'ResetSheath'])
respGardenHandGlow = ptAttribResponder(11, 'Garden hand glow', ['1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 'DropSheath',
 'ResetSheath'])
respKadishHandGlow = ptAttribResponder(12, 'Kadish hand glow', ['1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 'DropSheath',
 'ResetSheath'])
strTeledahnEnabled = ptAttribString(17, 'Tldn enabled SDL var')
strGarrisonEnabled = ptAttribString(18, 'Grsn enabled SDL var')
strGardenEnabled = ptAttribString(19, 'Grdn enabled SDL var')
strKadishEnabled = ptAttribString(20, 'Kdsh enabled SDL var')
clickTeledahnBook = ptAttribActivator(21, 'Teledahn book clickable')
clickGarrisonBook = ptAttribActivator(22, 'Garrison book clickable')
clickGardenBook = ptAttribActivator(23, 'Garden book clickable')
clickKadishBook = ptAttribActivator(24, 'Kadish book clickable')
respTeledahnOneShot = ptAttribResponder(25, 'Teledahn one shot')
respGarrisonOneShot = ptAttribResponder(26, 'Garrison one shot')
respGardenOneShot = ptAttribResponder(27, 'Garden one shot')
respKadishOneShot = ptAttribResponder(28, 'Kadish one shot')
respFissureStage1 = ptAttribResponder(29, 'Fissure stage 1')
respFissureStage2 = ptAttribResponder(30, 'Fissure stage 2')
respFissureStage3 = ptAttribResponder(31, 'Fissure stage 3')
respFissureStage4 = ptAttribResponder(32, 'Fissure stage 4')
respFissureLinkOut = ptAttribResponder(34, 'Fissure link out resp', ['cleft',
 'personal'])
rgnFissureLink = ptAttribActivator(35, 'Fissure link region')
respTeledahnLinkOut = ptAttribResponder(36, 'Teledahn link out')
respGarrisonLinkOut = ptAttribResponder(37, 'Garrison link out')
respGardenLinkOut = ptAttribResponder(38, 'Garden link out')
respKadishLinkOut = ptAttribResponder(39, 'Kadish link out')
actBookshelf = ptAttribActivator(40, 'Bookshelf script')
soTeledahnSmoker = ptAttribSceneobject(41, 'Teledahn smoker')
soGarrisonSmoker = ptAttribSceneobject(42, 'Garrison smoker')
soGardenSmoker = ptAttribSceneobject(43, 'Garden smoker')
soKadishSmoker = ptAttribSceneobject(44, 'Kadish smoker')
rgnFissureForceCamera = ptAttribActivator(45, 'Fissure force cam rgn')
respBahroScream = ptAttribResponder(46, 'Bahro Screams', ['start',
 'stop'])
rgnFissureCam = ptAttribActivator(47, 'Fissure cam region')
#dustin
actCleftTotem = ptAttribActivator(48, 'clk: Cleft totem')
respTouchCleftTotem = ptAttribResponder(49, 'resp: touch Cleft totem', netForce=1)
respChangeCleftTotem = ptAttribResponder(50, 'resp: change Cleft totem', ['open',
 'close'])
sdlCleftTotem = ptAttribString(51, 'sdl: Cleft totem')
respCleftHandGlow = ptAttribResponder(52, 'resp: Cleft hand glow', ['1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7'], netForce=1)
clickCleftBook = ptAttribActivator(53, 'Cleft book clickable')
respCleftLinkOut = ptAttribResponder(54, 'Cleft link out', netForce=1)
#boolCleftTotem = 0
kTimerCleftTotemClk = 42
#boolCleftSolved = 0
#HidingPoles = 0
CleftPoleVisible = 0
#IsVisitorPlayer = true
#/dustin
#kWriteTimestamps = 8
#BahroPoles = xEnum.Enum('Teledahn = 1, Garrison, Garden, Kadish')
class psnlBahroPolesMOUL(ptModifier,):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 8313
        self.version = 14
        PtDebugPrint(('__init__psnlBahroPolesMOUL v. %d' % self.version))



    def OnFirstUpdate(self):
        global CleftPoleVisible
        PtDebugPrint('DEBUG: psnlBahroPolesMOUL.OnFirstUpdate():\tEverything ok so far')
        #Always start with it closed:
        #respChangeCleftTotem.run(self.key, state='close', fastforward=1)
        ageVault = ptAgeVault()
        if (type(ageVault) != type(None)):
            ageSDL = ageVault.getAgeSDL()
            if ageSDL:
                try:
                    SDLVar = ageSDL.findVar('YeeshaPage25')
                    CurrentValue = SDLVar.getInt()
                except:
                    PtDebugPrint('psnlBahroPoles.RunState():\tERROR reading age SDLVar for YeeshaPage25. Assuming CurrentValue = 0')
                    CurrentValue = 0
                if (CurrentValue in [0,
                 2,
                 4]):
                    PtDebugPrint("psnlBahroPoles.RunState():\tPoles are active but YeeshaPage25 is off, so we're gonna hide 'em")
                    CleftPoleVisible = 0
                else:
                    CleftPoleVisible = 1
        ageSDL = PtGetAgeSDL()
        if (sdlCleftTotem.value != ''):
            ageSDL.setFlags(sdlCleftTotem.value, 1, 1)
            ageSDL.sendToClients(sdlCleftTotem.value)
            ageSDL.setNotify(self.key, sdlCleftTotem.value, 0.0)
        if (ageSDL[sdlCleftTotem.value][0]):
            respChangeCleftTotem.run(self.key, state='open', fastforward=1)
        else:
            respChangeCleftTotem.run(self.key, state='close', fastforward=1)




    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        PtDebugPrint('DEBUG: psnlBahroPolesMOUL.OnSDLNotify():\tEverything ok so far')
        if (VARname == sdlCleftTotem.value):
            ageSDL = PtGetAgeSDL()
            boolCleftTotem = ageSDL[sdlCleftTotem.value][0]
            if boolCleftTotem:
                print 'psnlBahroPoles.OnSDLNotify(): now opening Cleft totem...'
                respChangeCleftTotem.run(self.key, state='open')
            else:
                print 'psnlBahroPoles.OnSDLNotify(): now closing Cleft totem...'
                if CleftPoleVisible:
                #if True:
                    respChangeCleftTotem.run(self.key, state='close')
                else:
                    respChangeCleftTotem.run(self.key, state='close', fastforward=1)
            return 


    def OnNotify(self, state, id, events):
        PtDebugPrint(('DEBUG: psnlBahroPolesMOUL.OnNotify():\tid = %d' % id))
        if (not state):
            return 
        #dustin
        if (id == actCleftTotem.id):
            if ptVault().amOwnerOfCurrentAge():
                respTouchCleftTotem.run(self.key, events=events)
            else:
                PtDebugPrint("DEBUG: psnlBahroPoles.OnNotify():\tI'm not the owner of this age...don't respond to Cleft totem click")
        elif (id == respTouchCleftTotem.id):
            if (not ptVault().amOwnerOfCurrentAge()):
                return 
            #if (not boolCleftSolved):
            if(True):
                #if boolCleftTotem:
                if(False):
                    progress = self.GetJCProgress('Cleft')
                    if ((progress > 0) and (progress < 8)):
                        respCleftHandGlow.run(self.key, state=str(progress))
                        print ('psnlBahroPoles.OnNotify(): touch responder done, have %s JCs and will play correct hand glow' % str(progress))
                        PtAtTimeCallback(self.key, 10.699999999999999, kTimerCleftTotemClk)
                    elif (progress == 0):
                        print 'psnlBahroPoles.OnNotify(): touch responder done, but have no JCs so no glow'
                        PtAtTimeCallback(self.key, 1, kTimerCleftTotemClk)
                else:
                    print 'psnlBahroPoles.OnNotify(): touch responder done, will now open Cleft totem'
                    entry = ptVault().findChronicleEntry('TomahnaLoad')
                    if (type(entry) != type(None)):
                        entry.chronicleSetValue('yes')
                    respCleftHandGlow.run(self.key, state='7')
                    PtAtTimeCallback(self.key, 10.699999999999999, kTimerCleftTotemClk)
                    ageSDL = PtGetAgeSDL()
                    curOpen = ageSDL[sdlCleftTotem.value][0]
                    if(curOpen):
                        ageSDL[sdlCleftTotem.value] = (0,)
                    else:
                        ageSDL[sdlCleftTotem.value] = (1,)
            else:
                respCleftHandGlow.run(self.key, state='7')
                PtAtTimeCallback(self.key, 10.699999999999999, kTimerCleftTotemClk)
                print 'psnlBahroPoles.OnNotify(): touch responder done, and Cleft is done, so play entire hand glow'
        elif (id == clickCleftBook.id):
            for event in events:
                if (event[0] == kVariableEvent):
                    print "pole!"
                    if ((event[1] == 'LinkOut') and PtWasLocallyNotified(self.key)):
                        entry = ptVault().findChronicleEntry('TomahnaLoad')
                        if (type(entry) != type(None)):
                            entry.chronicleSetValue('no')
                        respCleftLinkOut.run(self.key, avatar=PtGetLocalAvatar())
                    break
        #/dustin



    def OnTimer(self, id):
        #print "psnlBahroPolesMOUL: ontimer"
        #dustin
        if (id == kTimerCleftTotemClk):
            actCleftTotem.enableActivator()
            return 
        #/dustin



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



