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
actButton1 = ptAttribActivator(1, 'Act: Button 1')
actButton2 = ptAttribActivator(2, 'Act: Button 2')
actButton3 = ptAttribActivator(3, 'Act: Button 3')
actButton4 = ptAttribActivator(4, 'Act: Button 4')
actButton5 = ptAttribActivator(5, 'Act: Button 5')
actButton6 = ptAttribActivator(6, 'Act: Button 6')
actButton7 = ptAttribActivator(7, 'Act: Button 7')
actButton8 = ptAttribActivator(8, 'Act: Button 8')
actButton9 = ptAttribActivator(9, 'Act: Button 9')
respButton1 = ptAttribResponder(10, 'Resp: Button 1 Down')
respButton2 = ptAttribResponder(11, 'Resp: Button 2 Down')
respButton3 = ptAttribResponder(12, 'Resp: Button 3 Down')
respButton4 = ptAttribResponder(13, 'Resp: Button 4 Down')
respButton5 = ptAttribResponder(14, 'Resp: Button 5 Down')
respButton6 = ptAttribResponder(15, 'Resp: Button 6 Down')
respButton7 = ptAttribResponder(16, 'Resp: Button 7 Down')
respButton8 = ptAttribResponder(17, 'Resp: Button 8 Down')
respButton9 = ptAttribResponder(18, 'Resp: Button 9 Down')
respButtonsUp = ptAttribResponder(19, 'Resp: All Buttons Up')
Solution = ptAttribString(20, 'Solution sequence')
ButtonSDL = ptAttribString(21, 'Button SDL name')
SolvedSDL = ptAttribString(22, 'Solved SDL name')
boolReplay = ptAttribBoolean(23, 'Replay if solved?', 1)
floatTimeOut = ptAttribFloat(24, 'Click time-out', 1.2)
boolFirstUpdate = ptAttribBoolean(25, 'Init SDL on first update?', 0)
ButtonDict = {1: (actButton1, respButton1),
 2: (actButton2, respButton2),
 3: (actButton3, respButton3),
 4: (actButton4, respButton4),
 5: (actButton5, respButton5),
 6: (actButton6, respButton6),
 7: (actButton7, respButton7),
 8: (actButton8, respButton8),
 9: (actButton9, respButton9)}
class xSimplePanel(ptResponder,):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 1049699
        self.version = 1
        minor = 0
        self.me = self.__class__.__name__
        print ('__init__%s v. %d.%d' % (self.me,
         self.version,
         minor))



    def OnFirstUpdate(self):
        EmptyButtons = []
        for i in ButtonDict:
            (act, resp,) = ButtonDict[i]
            if ((not len(act.value)) or (not len(resp.value))):
                EmptyButtons.append(i)

        for i in EmptyButtons:
            del ButtonDict[i]

        print ('%s.OnFirstUpdate: Valid buttons: %d' % (self.me,
         len(ButtonDict)))
        if (len(ButtonDict) != len(Solution.value)):
            print ('%s.OnFirstUpdate: WARNING! Solution length mismatch: %d' % (self.me,
             len(Solution.value)))
        if boolFirstUpdate.value:
            self.OnServerInitComplete()



    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        ageSDL.sendToClients(ButtonSDL.value)
        ageSDL.sendToClients(SolvedSDL.value)
        ageSDL.setFlags(ButtonSDL.value, 1, 1)
        ageSDL.setFlags(SolvedSDL.value, 1, 1)
        ageSDL.setNotify(self.key, ButtonSDL.value, 0.0)
        ageSDL.setNotify(self.key, SolvedSDL.value, 0.0)
        ButtonsPushed = ageSDL[ButtonSDL.value][0]
        ButtonsPushed = str(ButtonsPushed)
        print ('%s.OnServerInitComplete: When I got here, ButtonsPushed = %s' % (self.me,
         ButtonsPushed))
        if (len(ButtonsPushed) >= len(Solution.value)):
            PuzzleSolved = ageSDL[SolvedSDL.value][0]
            if ((not PuzzleSolved) or boolReplay.value):
                respButtonsUp.run(self.key, fastforward=1)
                ageSDL[ButtonSDL.value] = (0,)
                return 
        for i in ButtonDict:
            if (str(i) in ButtonsPushed):
                (act, resp,) = ButtonDict[i]
                resp.run(self.key, fastforward=1)
                act.disable()

        if ('0' in ButtonsPushed):
            ageSDL[ButtonSDL.value] = (0,)



    def OnNotify(self, state, id, events):
        if ((id in ButtonDict) and (state and PtWasLocallyNotified(self.key))):
            ageSDL = PtGetAgeSDL()
            PtSetGlobalClickability(0)
            PtAtTimeCallback(self.key, floatTimeOut.value, 1)
            print ('%s.OnNotify: Button #%d pushed' % (self.me,
             id))
            PuzzleSolved = ageSDL[SolvedSDL.value][0]
            if (PuzzleSolved and boolReplay.value):
                print ('%s.OnNotify: Oops... you have reset the puzzle!' % self.me)
                ageSDL[SolvedSDL.value] = (0,)
            ButtonsPushed = ageSDL[ButtonSDL.value][0]
            ButtonsPushed = str(ButtonsPushed)
            print ('%s.OnNotify: Before, ButtonsPushed was %s' % (self.me,
             ButtonsPushed))
            ButtonsPushed = int((ButtonsPushed + str(id)))
            print ('%s.OnNotify: Now, ButtonsPushed is %s' % (self.me,
             ButtonsPushed))
            ageSDL[ButtonSDL.value] = (ButtonsPushed,)
            if (len(str(ButtonsPushed)) >= len(Solution.value)):
                PtAtTimeCallback(self.key, 1, 2)



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname == ButtonSDL.value):
            ageSDL = PtGetAgeSDL()
            ButtonsPushed = ageSDL[ButtonSDL.value][0]
            print ('%s.OnSDLNotify: New ButtonsPushed = %s' % (self.me,
             ButtonsPushed))
            if (ButtonsPushed == 0):
                for i in ButtonDict:
                    (act, resp,) = ButtonDict[i]
                    act.enable()

                return 
            ButtonsPushed = str(ButtonsPushed)
            LastButtonPushed = int(ButtonsPushed[-1:])
            (act, resp,) = ButtonDict[LastButtonPushed]
            resp.run(self.key, netPropagate=0)
            act.disable()



    def OnTimer(self, id):
        if (id == 1):
            PtSetGlobalClickability(1)
        elif (id == 2):
            ageSDL = PtGetAgeSDL()
            ButtonsPushed = ageSDL[ButtonSDL.value][0]
            print ('%s.OnTimer: Check solution. ButtonsPushed = %s' % (self.me,
             ButtonsPushed))
            if (ButtonsPushed == int(Solution.value)):
                print ('%s.OnTimer: Puzzle solved. Unlocking...' % self.me)
                ageSDL[SolvedSDL.value] = (1,)
                if (not boolReplay.value):
                    return 
            respButtonsUp.run(self.key)
            ageSDL[ButtonSDL.value] = (0,)



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



