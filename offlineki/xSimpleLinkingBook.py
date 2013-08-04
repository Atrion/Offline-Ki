# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Copyright 2013      Sirius                                                #
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
"""xSimpleLinkingBook.py


Displays a very simple linking book, instead of making the script yourself.


note: fakelink does not cut the camera. It seems there isn't any way to reset the cam without a camregion in the age...


Not implemented:
    smart seek/animation behavior

"""


"""Default AlcScript:


<book object name>:
    physical:
        pinned: true
    logic:
        modifiers:
            - tag: click
              cursor: poised
              flags:
                - localelement
              activators:
                - type: objectinvolume
                  remote: <region name>
                  triggers:
                    - any
              conditions:
                - type: activator
                  activators:
                      - type: picking
                - type: objectinbox
                  satisfied: true
              actions:
                - type: pythonfile
                  ref: $click
        actions:
            - type: pythonfile
              tag: click
              pythonfile:
                file: xSimpleLinkingBook
                parameters:
                    # activator: clickable object
                    - type: activator
                      ref: logicmod:<book object name>_click
                    
                    # destination Age filename (skip will make this a book to Nexus)
                    - type: string
                      value: <age name>
                    
                    # name of spawn point to link to (skip to link to default link in point)
                    - type: string
                      value: <sp name>
                    
                    # name of linking panel texture (skip to let the script find one for you)
                    - type: string
                      value: <texture name>
                    
                    # name of the book's cover texture (skip to show open. Only works if you set your own linking panel texture)
                    - type: string
                      value: <texture name>
                    
                    # stamp/image on the left page (skip to show none)
                    - type: string
                      value: xGoWStamp
                    
                    # stamp/img X pos
                    - type: int
                      value: 150
                    
                    # stamp/img Y pos
                    - type: int
                      value: 110
                    
                    # book X scale
                    - type: float
                      value: 1.0
                    
                    # book Y scale
                    - type: float
                      value: 1.0

"""









## Plasma API
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaConstants import *

## Offline KI
import xLinkMgr
import booksDustGlobal





## Parameters:
# only the first is required, all other will default to show a linking
# book to the nexus.

bookClickable  = ptAttribActivator ( 1, "Activator: Clickable book object")

destinationAge = ptAttribString    ( 2, "Age to link to", "Nexus")
spawnPoint     = ptAttribString    ( 3, "Age spawn point to link to", "")

linkPanel      = ptAttribString    ( 4, "Link panel to use", "")
bookCover      = ptAttribString    ( 5, "Book cover to use", "")

# stamp/image
stampTexture   = ptAttribString    ( 6, "Left page image", "")
stampX         = ptAttribFloat     ( 7, "Image X position", default=0)
stampY         = ptAttribFloat     ( 8, "Image Y position", default=0)

bookWidth      = ptAttribFloat     ( 9, "Book x multiplier", default=1.0)
bookHeight     = ptAttribFloat     (10, "Book y multiplier", default=1.0)






## Variables/constants

BookGUI = None

destinationObject = None  # in case we use fakelink





class xSimpleLinkingBook(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = -1
        self.version = 1
    
    
    def OnServerInitComplete(self):
        global destinationObject
        if destinationAge.value == "fakelink":
            print "Linking book: this book links to this same Age, fetching spawnpoint for fakelink."
            try:
                destinationObject = PtFindSceneobject(spawnPoint.value, PtGetAgeName())
            except NameError:
                pass
    
    
    def OnNotify(self, state, id, events):
        if id == bookClickable.id:
            if PtWasLocallyNotified(self.key) and state:
                print "Linking book: you just clicked one."
                self.IPickupBook()
        
        else:
            for event in events:
                if event[0] == PtEventType.kBook:
                    print "Linking book: got notify from interface, event=%d, id=%d" % (event[1], event[2])
                    
                    if event[1] == PtBookEventTypes.kNotifyImageLink:
                        print "Linking book: hit linking panel n#%s" % event[2]
                        if (event[2] == 1):  # linking image can only be 1
                            self.IPutDownBook(0)
                            self.HideBook()
                            self.ILink()
                    
                    elif event[1] == PtBookEventTypes.kNotifyShow:
                        print "Linking book: just came up"
                        if not linkPanel.value and destinationAge.value != 'void':
                            print "Linking book: time to find a link panel !"
                            self.AutoFindLinkingPanel(destinationAge.value, spawnPoint.value)
                    
                    elif event[1] == PtBookEventTypes.kNotifyHide:
                        print "Linking book: closed"
                        self.IPutDownBook()
    
    
    def AutoFindLinkingPanel(self, age, sp=None):
        if age == "fakelink":
            age = PtGetAgeName()

        image = xLinkMgr.GetLinkingImage(age, sp, width=410, height=168)
        if image != None:
            booksDustGlobal.BookMapRight.textmap.drawImage(50, 60, image, 0)
            print "Linking book: finding a linking panel was successfull."
        else:
            print "ERROR: no link panel found."
            self.IPutDownBook()
            self.HideBook()
            PtSendKIMessage(kKIOKDialogNoQuit, "Could not find any linking panel for the destination Age.")
    
    
    def ILink(self):
        if destinationAge.value == "fakelink":
            print "Linking book: We're linking to the same Age. Using fakelink."
            if destinationObject:
                PtFakeLinkAvatarToObject(PtGetLocalAvatar().getKey(), destinationObject.getKey())
                PtFadeOut(1.5, 1)
                PtAtTimeCallback(self.key, 1.5, 1)
            else:
                PtSendKIMessage(kKIOKDialogNoQuit, "This Age does not have any object named %s." % spawnPoint.value)
        
        else:
            print "Linking book: time to link !"
            # The link manager will display a message in case the age is not available :P
            if spawnPoint.value:
                xLinkMgr.LinkToAge(destinationAge.value, spawnPoint.value)
            else:
                xLinkMgr.LinkToAge(destinationAge.value)
    
    
    def IPickupBook(self):
        bookClickable.disable()
        PtToggleAvatarClickability(False)
        self.IShowLinkingBook()
    
    
    def IPutDownBook(self, reenableBook=1):
        PtToggleAvatarClickability(True)
        PtSendKIMessage(kEnableKIandBB, 0)
        # In case we're linking, we shouldn't let the user grab the book again.
        if reenableBook:
            bookClickable.enable()
    
    
    def HideBook(self):
        global BookGUI
        BookGUI.hide()
    
    
    
    
    
    
    def IShowLinkingBook(self):
        global BookGUI
        
        # create the book cover
        if bookCover.value:
            bookContent = '<cover src="%s"><font size=10>' % bookCover.value
        else:
            bookContent = '<font size=10>'
        
        
        # GoW stamp page + linking page
        if destinationAge.value.lower() == 'void':
            # if the book is broken, display only a broken linking panel
            bookContent += '<pb><img src="xlinkpanelblackvoid*1#0.hsm" align=center blend=alpha>'
        
        else:
            if stampTexture.value:
                bookContent += '<img src="%s" pos=%d,%d resize=no blend=alpha>' % (stampTexture.value,
                                                                                   stampX.value,
                                                                                   stampY.value)
            
            panelName = linkPanel.value
            if panelName:
                if panelName.endswith(".bik"):
                    bookContent += '<pb><movie src="avi\\%s" align=center link=1 resize=yes blend=alpha>' % panelName
                else:
                    bookContent += '<pb><img src="%s" align=center link=1 blend=alpha>' % panelName
            else:
                print "Linking book: No link panel texture given. Will attempt to find one when book is shown."
                bookContent += '<pb><img src="xlinkpanelblackvoid*1#0.hsm" align=center link=1 blend=alpha>'
        
        
        # finally, show the actual book
        PtSendKIMessage(kDisableKIandBB, 0)
        BookGUI = ptBook(bookContent, self.key)
        BookGUI.setSize(bookWidth.value, bookHeight.value)
        BookGUI.setGUI("BkBook")
        BookGUI.allowPageTurning(True)
        if bookCover.value and linkPanel.value:
            BookGUI.show(0)
        else:
            BookGUI.show(1)
        
        
    def OnTimer(self, id):
        print "Linking book: got timer callback id %d" % id
        
        if id == 1:
            print "Linking book: Fading in..."
            PtFadeIn(1.5, 1)
            bookClickable.enable()




















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
                print ('%s has id %d which is already defined in %s' %
                      (obj.name, obj.id, glue_params[obj.id].name))
        else:
            glue_params[obj.id] = obj
    elif type(obj) == type([]):
        for o in obj:
            glue_findAndAddAttribs(o, glue_params)
    elif type(obj) == type({}):
        for o in obj.values():
            glue_findAndAddAttribs(o, glue_params)
    elif type(obj) == type(()):
        for o in obj:
            glue_findAndAddAttribs(o, glue_params)


def glue_getParamDict():
    global glue_paramKeys
    global glue_params
    if type(glue_params) == type(None):
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
        if type(glue_paramKeys) == type([]):
            if (number >= 0) and (number < len(glue_paramKeys)):
                return pd[glue_paramKeys[number]].getdef()
            else:
                print ('glue_getParam: Error! %d out of range of attribute list' % number)
        else:
            pl = pd.values()
            if (number >= 0) and (number < len(pl)):
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
                        if type(pd[id].value) != type([]):
                            pd[id].value = []
                    except AttributeError:
                        pd[id].value = []
                    pd[id].value.append(value)
                else:
                    pd[id].value = value
        elif glue_verbose:
            print "setParam: can't find id=", id
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
    if pd != None:
        if type(glue_paramKeys) == type([]):
            if (number >= 0) and (number < len(glue_paramKeys)):
                return pd[glue_paramKeys[number]].getVisInfo()
            else:
                print ('glue_getVisInfo: Error! %d out of range of attribute list' % number)
        else:
            pl = pd.values()
            if (number >= 0) and (number < len(pl)):
                return pl[number].getVisInfo()
            elif glue_verbose:
                print ('glue_getVisInfo: Error! %d out of range of attribute list' % number)
    if glue_verbose:
        print 'GLUE: Attribute list error'
    return None
