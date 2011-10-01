# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2004-2011  The Offline KI contributors                      #
#    See the file AUTHORS for more info about the contributors (including      #
#    contact information)                                                      #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    Please see the file COPYING for the full GPLv3 license, or see            #
#    <http://www.gnu.org/licenses/>                                            #
#                                                                              #
#    Uru exception: In addition, this file may be used in combination with     #
#    (non-GPL) code within the context of Uru.                                 #
#                                                                              #
#==============================================================================#
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import os
import PlasmaControlKeys
actMovieStart = ptAttribActivator(1, 'Movie activator')
strMovie = ptAttribString(2, 'Movie name', 'Intro1')
respCamMV = ptAttribResponder(3, 'Resp: Movie transition camera')
respCamAV = ptAttribResponder(4, 'Resp: Avatar camera')
boolFadeScene = ptAttribBoolean(5, 'Fade render scene?', 1)
fltOpacity = ptAttribFloat(6, 'Opacity', 1.0)
fltVolume = ptAttribFloat(7, 'Sound volume', 1.0)
strGUI = ptAttribString(8, 'Movie GUI', 'TrailerPreviewGUI')
gMovie = None
gWasMuted = 0
kGameFadeOutSeconds = 1.0
kGameFadeOutID = 1
kMovieFadeInSeconds = 0.5
kMovieFadeInID = 2
kMovieFadeOutSeconds = 0.5
kMovieFadeOutID = 3
kGameFadeInSeconds = 1.0
kExit = 99
class xMoviePlayer(ptModifier,):

    def __init__(self):
        ptModifier.__init__(self)
        self.id = 1049697
        self.version = 1
        minor = 0
        self.MovieFullName = None
        print ('__init__%s v. %d.%d' % (self.__class__.__name__, self.version, minor))



    def OnFirstUpdate(self):
        self.MovieFullName = (('avi/' + strMovie.value) + '.bik')
        if (strGUI.value != ''):
            PtLoadDialog(strGUI.value, self.key)



    def __del__(self):
        if (strGUI.value != ''):
            PtUnloadDialog(strGUI.value)



    def OnNotify(self, state, id, events):
        if ((id == actMovieStart.id) and state):
            if PtWasLocallyNotified(self.key):
                PtDebugPrint(('xMoviePlayer: Local player requested movie %s' % strMovie.value))
                try:
                    os.stat(self.MovieFullName)
                except:
                    PtDebugPrint(('xMoviePlayer ERROR: %s is missing!!!' % self.MovieFullName))
                    return 
                PtSendKIMessage(kDisableKIandBB, 0)
                if len(respCamMV.value):
                    respCamMV.run(self.key, netPropagate=0)
                if boolFadeScene.value:
                    PtFadeOut(kGameFadeOutSeconds, 1)
                PtAtTimeCallback(self.key, kGameFadeOutSeconds, kGameFadeOutID)



    def OnTimer(self, id):
        global gMovie
        global gWasMuted
        if (id == kGameFadeOutID):
            PtDisableMovementKeys()
            PtDisableMouseMovement()
            PtSetGlobalClickability(0)
            PtToggleAvatarClickability(0)
            if PtIsDialogLoaded(strGUI.value):
                PtDebugPrint(('xMoviePlayer: Dialog %s goes up' % strGUI.value))
                PtShowDialog(strGUI.value)
            else:
                PtEnableControlKeyEvents(self.key)
            if boolFadeScene.value:
                PtDisableRenderScene()
                PtFadeIn(kMovieFadeInSeconds, 0)
            audio = ptAudioControl()
            if audio.isMuted():
                gWasMuted = 1
            else:
                gWasMuted = 0
                audio.muteAll()
            gMovie = ptMoviePlayer(self.MovieFullName, self.key)
            gMovie.setOpacity(fltOpacity.value)
            gMovie.setVolume(fltVolume.value)
            gMovie.playPaused()
            PtAtTimeCallback(self.key, kMovieFadeInSeconds, kMovieFadeInID)
        elif (id == kMovieFadeInID):
            if (type(gMovie) != type(None)):
                PtDebugPrint('xMoviePlayer: Roll the movie')
                gMovie.resume()
        elif (id == kMovieFadeOutID):
            PtDebugPrint('xMoviePlayer: Done')
            if (type(gMovie) != type(None)):
                gMovie.stop()
                gMovie = None
            PtEnableMovementKeys()
            PtEnableMouseMovement()
            PtSetGlobalClickability(1)
            PtToggleAvatarClickability(1)
            if PtIsDialogLoaded(strGUI.value):
                PtDebugPrint(('xMoviePlayer: Dialog %s goes down' % strGUI.value))
                PtHideDialog(strGUI.value)
            else:
                PtDisableControlKeyEvents(self.key)
            if boolFadeScene.value:
                PtEnableRenderScene()
                PtFadeIn(kGameFadeInSeconds, 0)
            if (not gWasMuted):
                audio = ptAudioControl()
                audio.unmuteAll()
            PtSendKIMessage(kEnableKIandBB, 0)
            if len(respCamAV.value):
                respCamAV.run(self.key, netPropagate=0)



    def OnMovieEvent(self, movieName, reason):
        PtDebugPrint(('xMoviePlayer: Got movie done event on %s, reason=%d' % (movieName, reason)))
        self.IStopMovie()



    def IStopMovie(self):
        if (type(gMovie) != type(None)):
            if boolFadeScene.value:
                PtFadeOut(kMovieFadeOutSeconds, 1)
            PtAtTimeCallback(self.key, kMovieFadeOutSeconds, kMovieFadeOutID)



    def OnControlKeyEvent(self, controlKey, activeFlag):
        if ((controlKey == PlasmaControlKeys.kKeyExitMode) or (controlKey == PlasmaControlKeys.kKeyActionMouse)):
            if (activeFlag == 0):
                return 
            PtDebugPrint('xMoviePlayer: User abort')
            self.IStopMovie()



    def OnGUINotify(self, id, control, event):
        if (event == kDialogLoaded):
            PtDebugPrint(('xMoviePlayer: Dialog %s loaded' % control.getName()))
        elif (event == kAction):
            if (control.getTagID() == kExit):
                PtDebugPrint('xMoviePlayer: User hit back button')
                self.IStopMovie()
        elif (event == kExitMode):
            PtDebugPrint('xMoviePlayer: User hit escape')
            self.IStopMovie()



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
