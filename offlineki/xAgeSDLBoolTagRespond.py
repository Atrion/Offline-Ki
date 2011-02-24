# -*- coding: utf-8 -*-
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
#    (at your option) any later version, with the Cyan exception.              #
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
#    Please see the file COPYING for the full GPLv2 license. In addition,      #
#    this file may be used in combination with (non-GPL) Python code           #
#    by Cyan Worlds Inc.                                                       #
#                                                                              #
#==============================================================================#
from Plasma import *
from PlasmaTypes import *
import string
stringVarName = ptAttribString(1, 'Age SDL Var Name')
respBoolTrue = ptAttribResponder(2, 'Run if true')
respBoolFalse = ptAttribResponder(3, 'Run if false')
boolVltMgrFastForward = ptAttribBoolean(4, 'F-Forward on VM notify', 1)
boolFFOnInit = ptAttribBoolean(5, 'F-Forward on Init', 1)
stringInfo = ptAttribString(6, 'Extra info tag')
respBoolTrueTag = ptAttribResponder(7, 'Run if true and tagged')
respBoolFalseTag = ptAttribResponder(8, 'Run if false and tagged')
boolFirstUpdate = ptAttribBoolean(9, 'Init SDL On First Update?', 0)
AgeStartedIn = None
class xAgeSDLBoolTagRespond(ptResponder,):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5034999
        self.version = 1
        minor = 0
        print ('__init__%s v. %d.%d' % (self.__class__.__name__,
         self.version,
         minor))



    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        if (not ((type(stringVarName.value) == type('')) and (stringVarName.value != ''))):
            PtDebugPrint('ERROR: xAgeSDLBoolTagRespond.OnFirstUpdate():\tERROR: missing SDL var name')
        if boolFirstUpdate.value:
            self.OnServerInitComplete()



    def OnServerInitComplete(self):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            if ((type(stringVarName.value) == type('')) and (stringVarName.value != '')):
                ageSDL.setFlags(stringVarName.value, 1, 1)
                ageSDL.sendToClients(stringVarName.value)
                ageSDL.setNotify(self.key, stringVarName.value, 0.0)
                if ageSDL[stringVarName.value][0]:
                    PtDebugPrint(('DEBUG: xAgeSDLBoolTagRespond.OnServerInitComplete:\tRunning true responder on %s, fastforward=%d' % (self.sceneobject.getName(),
                     1)))
                    respBoolTrue.run(self.key, fastforward=1)
                else:
                    PtDebugPrint(('DEBUG: xAgeSDLBoolTagRespond.OnServerInitComplete:\tRunning false responder on %s, fastforward=%d' % (self.sceneobject.getName(),
                     1)))
                    respBoolFalse.run(self.key, fastforward=1)
            else:
                PtDebugPrint('ERROR: xAgeSDLBoolTagRespond.OnServerInitComplete():\tERROR: missing SDL var name')



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname != stringVarName.value):
            return 
        if (AgeStartedIn != PtGetAgeName()):
            return 
        ageSDL = PtGetAgeSDL()
        PtDebugPrint(('DEBUG: xAgeSDLBoolTagRespond.OnSDLNotify():\t VARname:%s, SDLname:%s, tag:%s, value:%d' % (VARname,
         SDLname,
         tag,
         ageSDL[stringVarName.value][0])))
        if playerID:
            objAvatar = ptSceneobject(PtGetAvatarKeyFromClientID(playerID), self.key)
            fastforward = 0
        else:
            objAvatar = None
            fastforward = boolVltMgrFastForward.value
        PtDebugPrint(('DEBUG: xAgeSDLBoolTagRespond.OnSDLNotify():\tnotification from playerID: %d' % playerID))
        if ageSDL[stringVarName.value][0]:
            PtDebugPrint(('DEBUG: xAgeSDLBoolTagRespond.OnSDLNotify:\tRunning true responder on %s, fastforward=%d' % (self.sceneobject.getName(),
             fastforward)))
            if (stringInfo.value == tag):
                respBoolTrueTag.run(self.key, avatar=objAvatar, netPropagate=0, fastforward=fastforward)
            else:
                respBoolTrue.run(self.key, avatar=objAvatar, netPropagate=0, fastforward=fastforward)
        else:
            PtDebugPrint(('DEBUG: xAgeSDLBoolTagRespond.OnSDLNotify:\tRunning false responder on %s, fastforward=%d' % (self.sceneobject.getName(),
             fastforward)))
            if (stringInfo.value == tag):
                respBoolFalseTag.run(self.key, avatar=objAvatar, netPropagate=0, fastforward=fastforward)
            else:
                respBoolFalse.run(self.key, avatar=objAvatar, netPropagate=0, fastforward=fastforward)



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
