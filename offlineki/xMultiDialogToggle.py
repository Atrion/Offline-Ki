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
import PlasmaControlKeys
import string
Activate = ptAttribActivator(1, ' clickable ', netForce=1)
Vignettes = ptAttribString(4, 'Toggle multiple dialogs - by Name')
SingleUser = ptAttribBoolean(5, 'One user only?', 0)
KeyMap = {}
KeyMap[PlasmaControlKeys.kKeyMoveForward] = PlasmaControlKeys.kKeyCamPanUp
KeyMap[PlasmaControlKeys.kKeyMoveBackward] = PlasmaControlKeys.kKeyCamPanDown
KeyMap[PlasmaControlKeys.kKeyRotateLeft] = PlasmaControlKeys.kKeyCamPanLeft
KeyMap[PlasmaControlKeys.kKeyRotateRight] = PlasmaControlKeys.kKeyCamPanRight
kExit = 99
Vignette = None
class xMultiDialogToggle(ptModifier,):

    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5104999
        self.version = 1
        minor = 0
        self.me = self.__class__.__name__
        self.VignetteList = []
        print ('__init__%s v. %d.%d' % (self.me, self.version, minor))



    def IGetAgeFilename(self):
        ageInfo = PtGetAgeInfo()
        if (type(ageInfo) != type(None)):
            return ageInfo.getAgeFilename()
        else:
            return 'GUI'



    def OnFirstUpdate(self):
        try:
            self.VignetteList += Vignettes.value.split(',')
            for i in range(len(self.VignetteList)):
                self.VignetteList[i] = self.VignetteList[i].strip()

            PtDebugPrint(('%s: Dialog list = %s' % (self.me,
             self.VignetteList)))
        except:
            PtDebugPrint(("ERROR: %s.OnFirstUpdate(): Couldn't process dialog list" % self.me))
            return 
        for i in range(len(self.VignetteList)):
            PtLoadDialog(self.VignetteList[i], self.key, self.IGetAgeFilename())




    def __del__(self):
        for i in range(len(self.VignetteList)):
            PtUnloadDialog(self.VignetteList[i])




    def OnNotify(self, state, id, events):
        global Vignette
        if (state and ((id == Activate.id) and PtWasLocallyNotified(self.key))):
            Vignette = self.VignetteList[0]
            self.IStartDialog(1)



    def OnGUINotify(self, id, control, event):
        global Vignette
        if (event == kAction):
            if (control.getTagID() == kExit):
                for i in range(len(self.VignetteList)):
                    if (self.VignetteList[i] == Vignette):
                        try:
                            tmpVignette = self.VignetteList[(i + 1)]
                        except IndexError:
                            self.IQuitDialog(1)
                            return 
                        self.IQuitDialog(0)
                        Vignette = tmpVignette
                        self.IStartDialog(0)
                        break

        elif (event == kExitMode):
            self.IQuitDialog(1)



    def OnControlKeyEvent(self, controlKey, activeFlag):
        PtDebugPrint(('Got controlKey event %d and its activeFlag is %d' % (controlKey,
         activeFlag)), level=kDebugDumpLevel)
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            self.IQuitDialog(1)



    def IStartDialog(self, init = 1):
        PtLoadDialog(Vignette, self.key, self.IGetAgeFilename())
        if PtIsDialogLoaded(Vignette):
            PtShowDialog(Vignette)
            PtDebugPrint(('%s: Dialog %s goes up' % (self.me,
             Vignette)))
        if init:
            PtGetControlEvents(true, self.key)
            if SingleUser.value:
                Activate.disable()



    def IQuitDialog(self, exit = 1):
        if ((type(Vignette) != type(None)) and (Vignette != '')):
            PtHideDialog(Vignette)
            PtDebugPrint(('%s: Dialog %s goes down' % (self.me,
             Vignette)))
        if exit:
            PtGetControlEvents(false, self.key)
            Activate.enable()



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

