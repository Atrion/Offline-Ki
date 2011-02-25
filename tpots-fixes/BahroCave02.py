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
from PlasmaConstants import *
from PlasmaKITypes import *
from xPsnlVaultSDL import *
import string
import time
SDLGotPellet = ptAttribString(1, 'SDL: got pellet')
RespDropPellet = ptAttribResponder(2, 'resp: got pellet', ['upper', 'lower'])
RespFadeInPellet = ptAttribResponder(3, 'resp: fade-in pellet')
RespPlayDud = ptAttribResponder(4, 'resp: pellet dud')
RespPlayBubbles = ptAttribResponder(5, 'resp: pellet bubbles', ['Hi', 'Med', 'Low'])
RespPlaySteam = ptAttribResponder(6, 'resp: pellet steam', ['Hi', 'Med', 'Low'])
RespPlayOrangeGlow = ptAttribResponder(7, 'resp: pellet orange glow', ['Hi', 'Med', 'Low'])
RespPlayBoom = ptAttribResponder(8, 'resp: pellet explosion', ['Hi', 'Med', 'Low'])
RespPlayWhiteGlow = ptAttribResponder(9, 'resp: pellet white glow')
gotPellet = 0
##############################################################################
# Show pellets.
##############################################################################
isMyPellet = 0
##############################################################################
# End show pellets.
##############################################################################
lowerCave = 0
prune = 0
kTimeWarp = 870

class BahroCave02(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 8000
        self.version = 6


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        global lowerCave
        global gotPellet
##############################################################################
# Show pellets.
##############################################################################
        global isMyPellet
##############################################################################
# End show pellets.
##############################################################################
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags(SDLGotPellet.value, 1, 1)
        ageSDL.sendToClients(SDLGotPellet.value)
        linkmgr = ptNetLinkingMgr()
        link = linkmgr.getCurrAgeLink()
        spawnPoint = link.getSpawnPoint()
        spTitle = spawnPoint.getTitle()
        spName = spawnPoint.getName()
        if (spName == 'LinkInPointLower'):
            lowerCave = 1
            avatar = 0
            try:
                avatar = PtGetLocalAvatar()
            except:
                print 'failed to get local avatar'
                return
            avatar.avatar.registerForBehaviorNotify(self.key)
        else:
            lowerCave = 0
            vault = ptVault()
            entry = vault.findChronicleEntry('GotPellet')
            if (type(entry) != type(None)):
                entryValue = entry.chronicleGetValue()
                gotPellet = string.atoi(entryValue)
                if (gotPellet != 0):
##############################################################################
# Show pellets.
##############################################################################
                    isMyPellet = 1
##############################################################################
# End show pellets.
##############################################################################
                    entry.chronicleSetValue(('%d' % 0))
                    entry.save()
                    avatar = PtGetLocalAvatar()
                    avatar.avatar.registerForBehaviorNotify(self.key)
            else:
                gotPellet = 0
            try:
                ageSDL = PtGetAgeSDL()
            except:
                print 'BahroCave02.OnServerInitComplete():\tERROR---Cannot find the ErcanaCitySilo Age SDL'
                ageSDL[SDLGotPellet.value] = (0,)
            ageSDL.setNotify(self.key, SDLGotPellet.value, 0.0)
            pelletSDL = ageSDL[SDLGotPellet.value][0]
            if (pelletSDL != gotPellet):
                ageSDL[SDLGotPellet.value] = (gotPellet,)
            PtDebugPrint(('BahroCave02:OnServerInitComplete:  SDL for pellet is now %d' % gotPellet))


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
##############################################################################
# Show pellets.
##############################################################################
        global gotPellet
        print 'OnSDLNotify: playerID = %d' % playerID
        ageSDL = PtGetAgeSDL()
        if (VARname == SDLGotPellet.value):
            pelletSDL = ageSDL[SDLGotPellet.value][0]
            print 'OnSDLNotify: SDLGotPellet: %d' % pelletSDL
            print 'OnSDLNotify: gotPellet currently is: %d' % gotPellet
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
        global lowerCave
        global gotPellet
        PtDebugPrint(('BahroCave02.OnBehaviorNotify(): %d' % type))
        if ((type == PtBehaviorTypes.kBehaviorTypeLinkIn) and state):
            if (not (lowerCave)):
                if (gotPellet != 0):
##############################################################################
# Show pellets.
##############################################################################
#                    RespFadeInPellet.run(self.key)
                    RespFadeInPellet.run(self.key, netForce=1)
##############################################################################
# End show pellets.
##############################################################################
                    cam = ptCamera()
                    cam.disableFirstPersonOverride()
                    cam.undoFirstPerson()
        if ((type == PtBehaviorTypes.kBehaviorTypeLinkIn) and (not (state))):
            if lowerCave:
                self.IPruneDrops()
            avatar = PtGetLocalAvatar()
            avatar.avatar.unRegisterForBehaviorNotify(self.key)


    def OnNotify(self, state, id, events):
##############################################################################
# Show pellets.
##############################################################################
        global gotPellet
##############################################################################
# End show pellets.
##############################################################################
        if (id == RespFadeInPellet.id):
            self.IDropUpper(gotPellet)
##############################################################################
# fix less-silly bug
##############################################################################
#        if (id == RespDropPellet.id):
        if (id == RespDropPellet.id) and (RespDropPellet.getState() == 'lower'):
##############################################################################
# end fix less-silly bug
##############################################################################
            print 'BahroCave02.OnNotify: RespDropPellet callback, will now play FX'
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
            print ' gotPellet is %d' % gotPellet
            gotPellet = 0
            ageSDL = PtGetAgeSDL()
            ageSDL[SDLGotPellet.value] = (gotPellet,)
##############################################################################
# End show pellets.
##############################################################################
##############################################################################
# fix less-silly bug
##############################################################################
#            PtAtTimeCallback(self.key, 0.5, 1)
        if (id == RespDropPellet.id) and (RespDropPellet.getState() == 'upper'):
            PtAtTimeCallback(self.key, 0.5, 1)
##############################################################################
# end fix less-silly bug
##############################################################################
##############################################################################
# Show pellets.
##############################################################################
            gotPellet = 0
            ageSDL = PtGetAgeSDL()
            ageSDL[SDLGotPellet.value] = (gotPellet,)
##############################################################################
# End show pellets.
##############################################################################


    def OnTimer(self, id):
        global prune
        if (id == 1):
            cam = ptCamera()
            cam.enableFirstPersonOverride()
        elif (id == 2):
            if prune:
                self.IPruneDrops()
            self.ICheckTime()


    def IDropUpper(self, recipe):
##############################################################################
# Show pellets.
##############################################################################
        global isMyPellet
##############################################################################
# End show pellets.
##############################################################################
        print 'in IDropUpper.'
        RespDropPellet.run(self.key, state='upper')
##############################################################################
# Show pellets.
##############################################################################
        if isMyPellet:
            isMyPellet = 0 # reset in case someone else arrives
        else:
            PtDebugPrint('That wasn\'t my pellet that just dropped')
            return
##############################################################################
# End show pellets.
##############################################################################
        DropTime = PtGetDniTime()
        vault = ptVault()
        entry = vault.findChronicleEntry('PelletDrops')
        if (type(entry) != type(None)):
            entryValue = entry.chronicleGetValue()
            if (entryValue == ''):
                entryValue = ('%d,%d' % (DropTime, recipe))
            else:
                entryValue += (';%d,%d' % (DropTime, recipe))
            entry.chronicleSetValue(entryValue)
            entry.save()
            PtDebugPrint('Chronicle entry PelletDrops already added, setting to Recipe value')
        else:
            vault.addChronicleEntry('PelletDrops', 1, ('%d,%d' % (DropTime, recipe)))
            PtDebugPrint('Chronicle entry PelletDrops not present, adding entry and setting time and recipe values')


    def IPruneDrops(self):
        global prune
        print 'in IPruneDrops.'
        vault = ptVault()
        entry = vault.findChronicleEntry('PelletDrops')
        if (type(entry) != type(None)):
            entryValue = entry.chronicleGetValue()
            Droppings = entryValue.split(';')
            print 'Droppings =',
            print Droppings
            resetChron = 0
            newValue = ''
            x = 0
            for xPellet in Droppings:
                if (x != len(Droppings)):
                    xPellet = xPellet.split(',')
##############################################################################
# fix silly bug
##############################################################################
                    # this apparently only comes up when a doof of an admin
                    # links to the lower cave with a pellet
                    if xPellet[0] == '':
                        continue
##############################################################################
# end fix silly bug
##############################################################################
                xTime = string.atoi(xPellet[0])
                xRecipe = string.atoi(xPellet[1])
                CurTime = (PtGetDniTime() - kTimeWarp)
                if (CurTime > xTime):
                    resetChron = 1
                elif (not (newValue)):
                    newValue = ('%d,%d' % (xTime, xRecipe))
                else:
                    newValue += (';%d,%d' % (xTime, xRecipe))
                x += 1
            if (not (newValue)):
                print 'BahroCave02.IPruneDrops(): all dropped pellots are old, clearing chronicle.  No pellets to be dropped.'
                entry.chronicleSetValue('')
                entry.save()
                if prune:
                    prune = 0
            else:
                if resetChron:
                    print 'BahroCave02.IPruneDrops(): some pellets were pruned, but some still waiting to drop... revising chronicle'
                    entry.chronicleSetValue(newValue)
                    entry.save()
                else:
                    print 'BahroCave02.IPruneDrops(): no pellets were pruned, all are still waiting to drop... leaving chronicle alone'
                print 'Pellets waiting to drop, chronicle =',
                print newValue
                if prune:
                    prune = 0
                else:
                    self.ICheckTime()


    def ICheckTime(self):
        global prune
#        print 'in ICheckTime.'
        vault = ptVault()
        entry = vault.findChronicleEntry('PelletDrops')
        if (type(entry) != type(None)):
            entryValue = entry.chronicleGetValue()
            Droppings = entryValue.split(';')
            xPellet = Droppings[0].split(',')
##############################################################################
# fix silly bug
##############################################################################
            if xPellet[0] == '':
                return
##############################################################################
# end fix silly bug
##############################################################################
            xTime = string.atoi(xPellet[0])
            CurTime = (PtGetDniTime() - kTimeWarp)
            if (CurTime == xTime):
                xRecipe = string.atoi(xPellet[1])
                self.IDropLower(xRecipe)
                prune = 1
            PtAtTimeCallback(self.key, 1, 2)


    def IDropLower(self, recipe):
        global gotPellet
        print 'in IDropLower.'
        gotPellet = recipe
##############################################################################
# Show pellets.
##############################################################################
        # send out the pellet value to any others in the age
        ageSDL = PtGetAgeSDL()
        ageSDL[SDLGotPellet.value] = (gotPellet,)
##############################################################################
# End show pellets.
##############################################################################
        RespDropPellet.run(self.key, state='lower')


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



