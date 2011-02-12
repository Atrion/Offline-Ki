# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2004-2011  The Offline KI contributors                      #
#    See the file AUTHORS for more info about the contributors                 #
#                                                                              #
#    This program is free software; you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation; either version 2 of the License, or         #
#    (at your option) any later version.                                       #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with this program; if not, write to the Free Software               #
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA #
#                                                                              #
#    Please see the file COPYING for the full license.                         #
#                                                                              #
#==============================================================================#
from Plasma import *
from PlasmaTypes import *
import xRandom
respRandom = ptAttribResponder(1, 'Random responder')
intChance = ptAttribInt(2, 'Chance percentage', 50)
intTime = ptAttribInt(3, 'Wait time in seconds', 30)
stringVarName = ptAttribString(4, 'Age SDL Var Name (optional)')
intRunState = ptAttribInt(5, 'State in which run (if SDL dependent)', 1)
boolRepeat = ptAttribBoolean(6, 'Repeat on?', 0)
intFluctuate = ptAttribInt(7, 'Wait time fluctuation (if repeat on)', 0)
boolFirstUpdate = ptAttribBoolean(8, 'Init SDL on first update?', 0)
kTimerID = 1
getSDL = false
SDLvalue = -1
class xRandomResp(ptModifier,):

    def __init__(self):
        ptModifier.__init__(self)
        self.id = 666999
        self.version = 1
        minor = 0
        self.me = self.__class__.__name__
        print ('__init__%s v. %d.%d' % (self.me, self.version, minor))



    def OnFirstUpdate(self):
        if boolFirstUpdate.value:
            self.OnServerInitComplete()



    def OnServerInitComplete(self):
        global getSDL
        global SDLvalue
        try:
            PtClearTimerCallbacks(self.key)
        except:
            PtDebugPrint(('%s: OnServerInitComplete: This Uru version cannot clear timer callbacks' % self.me))
        if ((type(stringVarName.value) == type('')) and (stringVarName.value != '')):
            PtDebugPrint(('%s: OnServerInitComplete: Responder is SDL dependent' % self.me))
            try:
                ageSDL = PtGetAgeSDL()
                ageSDL.setFlags(stringVarName.value, 1, 1)
                ageSDL.sendToClients(stringVarName.value)
                ageSDL.setNotify(self.key, stringVarName.value, 0.0)
                SDLvalue = ageSDL[stringVarName.value][0]
                getSDL = true
            except:
                PtDebugPrint(('%s: OnServerInitComplete: ERROR accessing ageSDL on %s' % (self.me, self.sceneobject.getName())))
        PtDebugPrint(('%s: OnServerInitComplete: Starting timer with interval %d for %s' % (self.me, intTime.value, self.sceneobject.getName())))
        PtAtTimeCallback(self.key, intTime.value, kTimerID)



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        global SDLvalue
        if (VARname == stringVarName.value):
            ageSDL = PtGetAgeSDL()
            SDLvalue = ageSDL[stringVarName.value][0]



    def OnTimer(self, id):
        PtDebugPrint(('%s: OnTimer: object = %s' % (self.me, self.sceneobject.getName())))
        if (id == kTimerID):
            if boolRepeat.value:
                fluTime = intFluctuate.value
                if (fluTime > intTime.value):
                    fluTime = intTime.value
                minTime = (intTime.value - fluTime)
                maxTime = (intTime.value + fluTime)
                newTime = xRandom.randint(minTime, maxTime)
                print (' - New interval for timer = %d' % newTime)
                PtAtTimeCallback(self.key, newTime, kTimerID)
            if (getSDL and (SDLvalue != intRunState.value)):
                print (' - SDL value %d does not match, abort chance roll' % SDLvalue)
                return 
            cur_chance = xRandom.randint(0, 100)
            print (' - Chance value = %d, Local chance roll = %d' % (intChance.value, cur_chance))
            if (cur_chance <= intChance.value):
                # Responders are netpropagated by default which means that every player will see/hear them.
                # We want the responder to be in synch for all players but letting everyone run them messes
                # up the chance rolls. So only one player must run the responder!
                # This should be the game owner, whom we can find with: self.sceneobject.isLocallyOwned()
                # If we are not repeating the event though, everyone who links in should be able to run it.
                if (self.sceneobject.isLocallyOwned() or (not boolRepeat.value)):
                    print (' - Running responder from %s' % self.sceneobject.getName())
                    respRandom.run(self.key)



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
    global glue_paramKeys
    global glue_params
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
                print ('%s has id %d which is already defined in %s' % (obj.name,
                 obj.id,
                 glue_params[obj.id].name))
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
    global glue_paramKeys
    global glue_params
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
            print "setParam: can't find id=",
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
