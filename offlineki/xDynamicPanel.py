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
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
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
#    Please see the file COPYING for the full GPLv2 license.                   #
#                                                                              #
#    Uru exception: In addition, this file may be used in combination with     #
#    (non-GPL) code within the context of Uru.                                 #
#                                                                              #
#==============================================================================#
from Plasma import *
from PlasmaTypes import *
import string
actButtons = ptAttribActivatorList(1, 'Act: Button List')
respButtons = ptAttribResponderList(2, 'Resp: Button List', statelist=['down',
 'up'], byObject=1)
actStart = ptAttribActivator(3, 'Act: Start Switch')
respStartOn = ptAttribResponder(4, 'Resp: Start Switch On')
respStartOff = ptAttribResponder(5, 'Resp: Start Switch Off')
respWrong = ptAttribResponder(6, 'Resp: Run if NOT solved')
respSolved = ptAttribResponder(7, 'Resp: Run if solved')
Solution = ptAttribString(8, 'Solution, Semicolon Separated!')
ButtonsSDL = ptAttribString(9, 'Buttons Pushed SDL')
StartedSDL = ptAttribString(10, 'Start Switch SDL')
floatTimeOut = ptAttribFloat(11, 'Click time-out', 1.2)
boolFirstUpdate = ptAttribBoolean(12, 'Init SDL On First Update?', 0)
ButtonDict = {}
SolutionList = []
class xDynamicPanel(ptResponder,):

    def __init__(self):
        ptResponder.__init__(self)
        self.id = 1049698
        self.version = 1
        minor = 1
        self.me = self.__class__.__name__
        print ('__init__%s v. %d.%d' % (self.me,
         self.version,
         minor))



    def OnFirstUpdate(self):
        global SolutionList
        try:
            actList = []
            objList = []
            for act in actButtons.value:
                actList.append(act)
                objList.append(act.getParentKey().getName())
            #print actList
            #print objList
            respList = []
            for resp in respButtons.value:
                respList.append(resp.getName())
            #print respList
            if (len(objList) != len(respList)):
                print ('ERROR: %s.OnFirstUpdate: ActivatorList and ResponderList mismatch' % self.me)
                return 
            for i in range(len(objList)):
                ButtonDict[(i + 1)] = (actList[i],
                 objList[i],
                 respList[i])

            print ('%s.OnFirstUpdate: Resulting dictionary = %s' % (self.me,
             ButtonDict))
        except Exception, detail:
            print ("ERROR: %s.OnFirstUpdate: Couldn't process Activator/Responder lists - %s" % (self.me,
             detail))
            return 
        try:
            SolutionList += map(int, Solution.value.split(';'))
            print ('%s.OnFirstUpdate: Solution list = %s' % (self.me,
             SolutionList))
            if (len(actList) < len(SolutionList)):
                print ('WARNING: %s.OnFirstUpdate: Solution list too long' % self.me)
        except Exception, detail:
            print ("ERROR: %s.OnFirstUpdate: Couldn't process solution list - %s" % (self.me,
             detail))
            return 
        if boolFirstUpdate.value:
            self.OnServerInitComplete()



    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        ageSDL.sendToClients(ButtonsSDL.value)
        ageSDL.sendToClients(StartedSDL.value)
        ageSDL.setFlags(ButtonsSDL.value, 1, 1)
        ageSDL.setFlags(StartedSDL.value, 1, 1)
        ageSDL.setNotify(self.key, ButtonsSDL.value, 0.0)
        ageSDL.setNotify(self.key, StartedSDL.value, 0.0)
        ButtonsPushed = self.SDLtoIntList(ButtonsSDL.value)
        print ('%s.OnServerInitComplete: When I got here: %s value = %s' % (self.me,
         ButtonsSDL.value,
         ButtonsPushed))
        if (0 in ButtonsPushed):
            ageSDL[ButtonsSDL.value] = ('0',)
            for i in ButtonDict:
                (act, obj, resp,) = ButtonDict[i]
                respButtons.run(self.key, state='up', objectName=resp, fastforward=1)

        else:
            for i in ButtonDict:
                (act, obj, resp,) = ButtonDict[i]
                if (i in ButtonsPushed):
                    respButtons.run(self.key, state='down', objectName=resp, fastforward=1)
                else:
                    respButtons.run(self.key, state='up', objectName=resp, fastforward=1)

        if ageSDL[StartedSDL.value][0]:
            respStartOn.run(self.key, fastforward=1)
            for i in ButtonDict:
                (act, obj, resp,) = ButtonDict[i]
                act.disable()
            self.CheckSolution(1)
        else:
            respStartOff.run(self.key, fastforward=1)



    def OnNotify(self, state, id, events):
        if (not PtWasLocallyNotified(self.key)):
            return 
        ageSDL = PtGetAgeSDL()
        if ((id == actButtons.id) and state):
            for event in events:
                if (event[0] == kPickedEvent):
                    xEvent = event[3]
                    btnName = xEvent.getName()
                    for d in ButtonDict:
                        (act, obj, resp,) = ButtonDict[d]
                        if (obj == btnName):
                            id = d
                            break


            print ('%s.OnNotify: Button #%d pushed' % (self.me,
             id))
            PtSetGlobalClickability(0)
            PtAtTimeCallback(self.key, floatTimeOut.value, 1)
            ButtonsPushed = self.SDLtoIntList(ButtonsSDL.value)
            print ('%s.OnNotify: Before, %s was %s' % (self.me,
             ButtonsSDL.value,
             ButtonsPushed))
            wasDown = 0
            for i in range(len(ButtonsPushed)):
                if (ButtonsPushed[i] == id):
                    del ButtonsPushed[i]
                    wasDown = 1
                    break

            objAvatar = PtFindAvatar(events)
            (act, obj, resp,) = ButtonDict[id]
            if wasDown:
                respButtons.run(self.key, state='up', avatar=objAvatar, objectName=resp, netForce=1)
            else:
                ButtonsPushed.append(id)
                respButtons.run(self.key, state='down', avatar=objAvatar, objectName=resp, netForce=1)
            if (len(ButtonsPushed) == 0):
                ButtonsPushed.append(0)
            elif (len(ButtonsPushed) > 1):
                for i in range(len(ButtonsPushed)):
                    if (ButtonsPushed[i] == 0):
                        del ButtonsPushed[i]
                        break

            print ('%s.OnNotify: Now, %s is %s' % (self.me,
             ButtonsSDL.value,
             ButtonsPushed))
            SDLvalue = ';'.join(map(str, ButtonsPushed))
            ageSDL[ButtonsSDL.value] = (SDLvalue,)
        elif ((id == actStart.id) and state):
            if ageSDL[StartedSDL.value][0]:
                ageSDL[StartedSDL.value] = (0,)
            else:
                ageSDL[StartedSDL.value] = (1,)
        elif (id == respStartOn.id):
            print ('%s.OnNotify: Responder %d ready, check solution' % (self.me,
             id))
            self.CheckSolution(0)



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        SDLvalue = ageSDL[VARname][0]
        print ('%s.OnSDLNotify: VARname %s, value = %s' % (self.me,
         VARname,
         SDLvalue))
        if playerID:
            objAvatar = ptSceneobject(PtGetAvatarKeyFromClientID(playerID), self.key)
            ff = 0
        else:
            objAvatar = None
            ff = 1
        if (VARname == StartedSDL.value):
            if (SDLvalue == 0):
                respStartOff.run(self.key, avatar=objAvatar, netPropagate=0, fastforward=ff)
                for i in ButtonDict:
                    (act, obj, resp,) = ButtonDict[i]
                    act.enable()
            else:
                respStartOn.run(self.key, avatar=objAvatar, netPropagate=0, fastforward=ff)
                for i in ButtonDict:
                    (act, obj, resp,) = ButtonDict[i]
                    act.disable()



    def OnTimer(self, id):
        if (id == 1):
            PtSetGlobalClickability(1)



    def CheckSolution(self, ff = 0):
        ButtonsPushed = self.SDLtoIntList(ButtonsSDL.value)
        print ('%s.CheckSolution: %s value = %s' % (self.me,
         ButtonsSDL.value,
         ButtonsPushed))
        ButtonsPushed.sort()
        SolutionList.sort()
        solved = 0
        if (ButtonsPushed == SolutionList):
            solved = 1
        print ('%s.CheckSolution: solved = %d' % (self.me,
         solved))
        if solved:
            respSolved.run(self.key, netPropagate=0, fastforward=ff)
        elif len(respWrong.value):
            respWrong.run(self.key, netPropagate=0, fastforward=ff)
        else:
            print ('%s.CheckSolution: No responder to run' % self.me)



    def SDLtoIntList(self, VARname):
        ageSDL = PtGetAgeSDL()
        SDLvalue = ageSDL[VARname][0]
        IntList = []
        try:
            IntList += map(int, SDLvalue.split(';'))
        except Exception, detail:
            print ('ERROR: %s.SDLtoIntList: %s' % (self.me,
             detail))
            IntList = [0]
        return IntList



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



