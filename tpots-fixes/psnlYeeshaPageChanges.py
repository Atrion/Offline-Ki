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
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
import string
import xxConfig
import os
PageNumber = ptAttribInt(1, 'Yeesha Page Number')
stringShowStates = ptAttribString(2, 'States in which shown')
respAudioStart = ptAttribResponder(3, 'Audio start responder')
respAudioStop = ptAttribResponder(4, 'Audio stop responder')
respEnable = ptAttribResponder(5, 'Enabled resp (if necessary)')
respDisable = ptAttribResponder(6, 'Disabled resp (if necessary)')
bushDistrib = ptAttribClusterList(7, 'Bush distributor')
isMOULPage = ptAttribInt(8, 'This is on the MOUL page', 0)
hasMOUL = os.path.exists('dat/Personal_District_psnlDustAdditions.prp')

class psnlYeeshaPageChanges(ptMultiModifier):


    def __init__(self):
        ptMultiModifier.__init__(self)
        self.id = 5232
        version = 8
        self.version = version
        PtDebugPrint(('__init__psnlYeeshaPageChanges v%d.%d' % (version, 1)), level=kWarningLevel)


    def OnFirstUpdate(self):
        try:
            self.enabledStateList = stringShowStates.value.split(',')
            for i in range(len(self.enabledStateList)):
                self.enabledStateList[i] = int(self.enabledStateList[i].strip())
        except:
            PtDebugPrint('psnlYeeshaPageChanges.OnFirstUpdate():\tERROR: couldn\'t process start state list')
        if isMOULPage.value or PageNumber.value >= 18: # the MOUL page is loaded dynamically
            self.OnServerInitComplete()


    def OnServerInitComplete(self):
        if PageNumber.value >= 18 and not hasMOUL:
            return # MOUL is not converted, don't do nothing (like hiding the green trees)
        FoundYPs = []
        CurrentPage = 0
        AgeVault = ptAgeVault()
        if (type(AgeVault) != type(None)):
            self.ageSDL = AgeVault.getAgeSDL()
            if self.ageSDL:
                try:
                    SDLVar = self.ageSDL.findVar(('YeeshaPage' + str(PageNumber.value)))
                    CurrentValue = SDLVar.getInt()
                except:
                    PtDebugPrint('psnlYeeshaPageChanges:\tERROR reading age SDLVar. Assuming CurrentValue = 0')
                    CurrentValue = 0
                if (PageNumber.value == 10):
                    MAX_SIZE = 10
                    (size, state) = divmod(CurrentValue, 10)
                    if ((len(PtGetPlayerList()) == 0) and (state != 0)):
                        growSizes = self.TimeToGrow()
                        if (growSizes and (size < MAX_SIZE)):
                            size = (size + growSizes)
                            if (size > MAX_SIZE):
                                size = MAX_SIZE
                            sizechanged = 1
                        else:
                            sizechanged = 0
                        newstate = self.UpdateState(state, size, SDLVar, AgeVault, sizechanged)
                    else:
                        newstate = state
                    state = ((size * 10) + newstate)
                    self.EnableDisable(newstate)
                    if (state in self.enabledStateList):
                        print 'psnlYeeshaPageChanges: tree stats: Growsizes: %d, CurrentValue: %d, size: %d, state %d' % (growSizes, CurrentValue, size, state)
                else:
                    if (len(PtGetPlayerList()) == 0):
                        newstate = self.UpdateState(CurrentValue, 0, SDLVar, AgeVault, 0)
                    else:
                        newstate = CurrentValue
                    self.EnableDisable(newstate)
            else:
                PtDebugPrint(('psnlYeeshaPageChanges: Error trying to access the Chronicle self.ageSDL. self.ageSDL = %s' % self.ageSDL))
        else:
            PtDebugPrint('psnlYeeshaPageChanges: Error trying to access the Vault. Can\'t access YeeshaPageChanges chronicle.')


    def EnableDisable(self, val):
        if (val in self.enabledStateList):
            if (PageNumber.value == 10):
                PtDebugPrint(('psnlYeeshaPageChanges: Attempting to enable drawing and collision on %s...' % self.sceneobject.getName()))
            self.sceneobject.draw.enable()
            self.sceneobject.physics.suppress(false)
            respAudioStart.run(self.key, avatar=None, fastforward=0)
            respEnable.run(self.key, avatar=None, fastforward=0)
            if (len(bushDistrib.value) > 0):
                for x in bushDistrib.value:
                    x.setVisible(1)
        else:
            if (PageNumber.value == 10):
                PtDebugPrint(('psnlYeeshaPageChanges: Attempting to disable drawing and collision on %s...' % self.sceneobject.getName()))
            self.sceneobject.draw.disable()
            self.sceneobject.physics.suppress(true)
            respAudioStop.run(self.key, avatar=None, fastforward=0)
            respDisable.run(self.key, avatar=None, fastforward=1)
            if (len(bushDistrib.value) > 0):
                for x in bushDistrib.value:
                    x.setVisible(0)


    def TimeToGrow(self):
        dayLength = 86400
        sdl = PtGetAgeSDL()
        currentTime = PtGetDniTime()
        lastGrowth = sdl['YP10LastTreeGrowth'][0]
        #PtDebugPrint(('Dni time: %d, last growth: %d' % (currentTime, lastGrowth)))
        if (lastGrowth == 0):
            sizes = 1
        else:
            timeDelta = (currentTime - lastGrowth)
            sizes = (timeDelta / (dayLength * 15))
        if (sizes > 0):
            sdl['YP10LastTreeGrowth'] = (currentTime,)
        return sizes


    def UpdateState(self, state, size, SDLVar, AgeVault, sizechanged):
        if (state == 3):
            state = 2
            print ('psnlYeeshaPageChanges: Updated value of YeeshaPage %s from 3 to 2.' % ('YeeshaPage' + str(PageNumber.value)))
            SDLVar.setInt(((size * 10) + state))
            AgeVault.updateAgeSDL(self.ageSDL)
        elif (state == 4):
            state = 1
            print ('psnlYeeshaPageChanges: Updated value of YeeshaPage %s from 4 to 1.' % ('YeeshaPage' + str(PageNumber.value)))
            SDLVar.setInt(((size * 10) + state))
            AgeVault.updateAgeSDL(self.ageSDL)
        elif sizechanged:
            SDLVar.setInt(((size * 10) + state))
            AgeVault.updateAgeSDL(self.ageSDL)
        return state


    def OnBackdoorMsg(self, target, param):
        if (target == 'yeesha'):
            if (param == 'on'):
                if (len(bushDistrib.value) > 0):
                    for x in bushDistrib.value:
                        x.setVisible(1)
            elif (param == 'off'):
                if (len(bushDistrib.value) > 0):
                    for x in bushDistrib.value:
                        x.setVisible(0)


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



