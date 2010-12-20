# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaConstants import *
from PlasmaKITypes import *
from xPsnlVaultSDL import *
import string
import time
SDLGotPellet = ptAttribString(1, 'SDL: got pellet')
RespDropPellet = ptAttribResponder(2, 'resp: got pellet')
RespFadeInPellet = ptAttribResponder(3, 'resp: fade-in pellet')
RespScanMeter = ptAttribResponder(4, 'resp: scan pellet meter', ['Level1', 'Level2', 'Level3', 'Level4', 'Level5', 'Level6', 'Level7', 'Level8', 'Level9', 'Level10', 'NoLevel'])
RespPlayDud = ptAttribResponder(5, 'resp: pellet dud')
RespPlayBubbles = ptAttribResponder(6, 'resp: pellet bubbles', ['Hi', 'Med', 'Low'])
RespPlaySteam = ptAttribResponder(7, 'resp: pellet steam', ['Hi', 'Med', 'Low'])
RespPlayOrangeGlow = ptAttribResponder(8, 'resp: pellet orange glow', ['Hi', 'Med', 'Low'])
RespPlayBoom = ptAttribResponder(9, 'resp: pellet explosion', ['Hi', 'Med', 'Low'])
RespPlayWhiteGlow = ptAttribResponder(10, 'resp: pellet white glow')
gotPellet = 0

class ErcanaCitySilo(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 208
        self.version = 7


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        global gotPellet
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(SDLGotPellet.value, 1, 1)
        ageSDL.sendToClients(SDLGotPellet.value)
        vault = ptVault()
        entry = vault.findChronicleEntry('GotPellet')
        if (type(entry) != type(None)):
            entryValue = entry.chronicleGetValue()
            gotPellet = string.atoi(entryValue)
            if (gotPellet != 0):
                entry.chronicleSetValue(('%d' % 0))
                entry.save()
                avatar = PtGetLocalAvatar()
                avatar.avatar.registerForBehaviorNotify(self.key)
        else:
            gotPellet = 0
        try:
            ageSDL = PtGetAgeSDL()
        except:
            print 'ErcanaCitySilo.OnServerInitComplete():\tERROR---Cannot find the ErcanaCitySilo Age SDL'
            ageSDL[SDLGotPellet.value] = (0,)
        ageSDL.setNotify(self.key, SDLGotPellet.value, 0.0)
        pelletSDL = ageSDL[SDLGotPellet.value][0]
        if (pelletSDL != gotPellet):
            ageSDL[SDLGotPellet.value] = (gotPellet,)
        PtDebugPrint(('ErcanaCitySilo:OnServerInitComplete:  SDL for pellet is now %d' % gotPellet))


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
##############################################################################
# Show pellets.
##############################################################################
        global gotPellet
        ageSDL = PtGetAgeSDL()
        if (VARname == SDLGotPellet.value):
            pelletSDL = ageSDL[SDLGotPellet.value][0]
            if (pelletSDL != gotPellet):
                if (gotPellet == 0):
                    print 'somebody else came in with a pellet!'
                    gotPellet = pelletSDL
                elif (pelletSDL == 0):
                    print 'somebody else came in but I have a pellet'
                    # The new person won't see my pellet. Possibly we could
                    # reset the age SDL here to remedy this.
                else:
                    print 'somebody else came in with a pellet and I have one too'
                    # This is possible if two people link in a row and the
                    # first person links slower.
                    # Stick with my own gotPellet value.
                    # I won't see the new person's pellet after it drops
                    # and neither will anyone else.
#        pass
##############################################################################
# End show pellets.
##############################################################################


    def OnBehaviorNotify(self, type, id, state):
        global gotPellet
        PtDebugPrint(('ErcanaCitySilo.OnBehaviorNotify(): %d' % type))
        if ((type == PtBehaviorTypes.kBehaviorTypeLinkIn) and state):
            if (gotPellet != 0):
##############################################################################
# Show pellets.
##############################################################################
#                RespFadeInPellet.run(self.key)
                RespFadeInPellet.run(self.key, netForce=1)
##############################################################################
# End show pellets.
##############################################################################
                cam = ptCamera()
                cam.disableFirstPersonOverride()
                cam.undoFirstPerson()
        if ((type == PtBehaviorTypes.kBehaviorTypeLinkIn) and (not (state))):
            if (gotPellet != 0):
                print 'ErcanaCitySilo.OnBehaviorNotify: Will now call IDoMeter.'
                self.IDoMeter()
            else:
                print 'Says pellet is 0.  Shouldn\'t be possible, I\'m in OnBehaviorNotify.'
            avatar = PtGetLocalAvatar()
            avatar.avatar.unRegisterForBehaviorNotify(self.key)


    def IDoMeter(self):
        global gotPellet
        pellet = (gotPellet - 301)
        if (pellet <= -300):
            RespScanMeter.run(self.key, state='NoLevel')
        elif ((pellet > -300) and (pellet <= 0)):
            if ((pellet > -300) and (pellet <= -250)):
                RespScanMeter.run(self.key, state='Level1')
            elif ((pellet > -250) and (pellet <= -200)):
                RespScanMeter.run(self.key, state='Level2')
            elif ((pellet > -200) and (pellet <= -100)):
                RespScanMeter.run(self.key, state='Level3')
            elif ((pellet > -100) and (pellet <= -50)):
                RespScanMeter.run(self.key, state='Level2')
            elif ((pellet > -50) and (pellet <= 0)):
                RespScanMeter.run(self.key, state='Level1')
        elif ((pellet > 0) and (pellet <= 270)):
            if ((pellet > 0) and (pellet <= 74)):
                RespScanMeter.run(self.key, state='Level7')
            elif ((pellet > 74) and (pellet <= 149)):
                RespScanMeter.run(self.key, state='Level8')
            elif ((pellet > 149) and (pellet <= 209)):
                RespScanMeter.run(self.key, state='Level9')
            elif ((pellet > 209) and (pellet <= 270)):
                RespScanMeter.run(self.key, state='Level10')
        elif (pellet > 270):
            if ((pellet > 270) and (pellet <= 295)):
                RespScanMeter.run(self.key, state='Level4')
            elif ((pellet > 295) and (pellet <= 320)):
                RespScanMeter.run(self.key, state='Level5')
            elif (pellet > 320):
                RespScanMeter.run(self.key, state='Level6')


    def IDropPellet(self):
        RespDropPellet.run(self.key)


    def OnNotify(self, state, id, events):
##############################################################################
# Show pellets.
##############################################################################
        global gotPellet
        if (id == RespFadeInPellet.id):
            print 'OnNotify: got RespFadeInPellet'
##############################################################################
# End show pellets.
##############################################################################
        if (id == RespScanMeter.id):
            print 'ErcanaCitySilo.OnNotify: Received callback from RespScanMeter, will now call IDropPellet.'
            self.IDropPellet()
        if (id == RespDropPellet.id):
            pellet = (gotPellet - 301)
            if (pellet <= -300):
                RespPlayDud.run(self.key)
            elif ((pellet > -300) and (pellet <= 0)):
                if ((pellet > -300) and (pellet <= -250)):
                    RespPlaySteam.run(self.key, state='Low')
                    RespPlayBubbles.run(self.key, state='Low')
                elif ((pellet > -250) and (pellet <= -200)):
                    RespPlaySteam.run(self.key, state='Med')
                    RespPlayBubbles.run(self.key, state='Med')
                elif ((pellet > -200) and (pellet <= -100)):
                    RespPlaySteam.run(self.key, state='Hi')
                    RespPlayBubbles.run(self.key, state='Hi')
                elif ((pellet > -100) and (pellet <= -50)):
                    RespPlaySteam.run(self.key, state='Med')
                    RespPlayBubbles.run(self.key, state='Med')
                elif ((pellet > -50) and (pellet <= 0)):
                    RespPlaySteam.run(self.key, state='Low')
                    RespPlayBubbles.run(self.key, state='Low')
            elif ((pellet > 0) and (pellet <= 270)):
                if ((pellet > 0) and (pellet <= 74)):
                    RespPlayOrangeGlow.run(self.key, state='Low')
                elif ((pellet > 74) and (pellet <= 149)):
                    RespPlayOrangeGlow.run(self.key, state='Med')
                elif ((pellet > 149) and (pellet <= 209)):
                    RespPlayOrangeGlow.run(self.key, state='Hi')
                elif ((pellet > 209) and (pellet <= 270)):
                    RespPlayWhiteGlow.run(self.key)
            elif (pellet > 270):
                if ((pellet > 270) and (pellet <= 295)):
                    RespPlayBoom.run(self.key, state='Low')
                elif ((pellet > 295) and (pellet <= 320)):
                    RespPlayBoom.run(self.key, state='Med')
                elif (pellet > 320):
                    RespPlayBoom.run(self.key, state='Hi')
##############################################################################
# Show pellets.
##############################################################################
            # this is done so that when someone else links in with a pellet
            # their actual pellet value is used, not the first person's
            gotPellet = 0
            ageSDL = PtGetAgeSDL()
            ageSDL[SDLGotPellet.value] = (gotPellet,)
##############################################################################
# End show pellets.
##############################################################################
            PtAtTimeCallback(self.key, 5, 1)


    def OnTimer(self, id):
        if (id == 1):
            cam = ptCamera()
            cam.enableFirstPersonOverride()


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



