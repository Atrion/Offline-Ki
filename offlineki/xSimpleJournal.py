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
"""xSimpleJournal.py

Displays a very simple journal with content stored in a text file, instead of making the script yourself.

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
                file: xSimpleJournal
                parameters:
                    # activator: clickable object
                    - type: activator
                      ref: logicmod:<book object name>_click
                    
                    # journal name (ageresources/<YourAge>--<journal name>.txt, or <YourAge>_<journal name>.py)
                    - type: string
                      value: <journal name>
                    
                    # notebook (true) or normal book (false)
                    - type: bool
                      value: true
                    
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
from PlasmaConstants import *





## parameters:
bookClickable   = ptAttribActivator (1, "Activator: Clickable journal object")
journalFileName = ptAttribString    (2, "Text file with journal content", "MISSING")
isNotebook      = ptAttribBoolean   (3, "Is it a journal (true) or a normal book (false) ?", default=1)
bookWidth       = ptAttribFloat     (4, "Book x multiplier (optional)", default=1.0)
bookHeight      = ptAttribFloat     (5, "Book y multiplier (optional)", default=1.0)



## useful variables

errorContent = """<cover src="xurucreditsjournalcover*1#0.hsm"><font size=20 face=Arial color=400000>
<margin left=62 right=62 top=48>This book could not be found.

Make sure the file %s exists, or that the game has access to it."""

JournalGUI = None






class xSimpleJournal(ptResponder):
    
    
    def __init__(self):
        ptResponder.__init__(self)
        self.id = -1
        self.version = 1
    
    
    def OnNotify(self, state, id, events):
        if (id == bookClickable.id):  # a player clicked the activator
            if (PtWasLocallyNotified(self.key) and state):  # the player who clicked it was you
                print "Journal: you just clicked one."
                PtToggleAvatarClickability(false)
                self.IShowJournal()
                return
        else:
            for event in events:
                if (event[0] == PtEventType.kBook):
                    print "Journal: received BookNotify: event=%d, id=%d" % (event[1], event[2])
                    if (event[1] == PtBookEventTypes.kNotifyHide):
                        print "Journal: you just stopped reading."
                        PtToggleAvatarClickability(true)
    
    
    def IsThereACover(self, bookHtml):
        idx = bookHtml.find('<cover')
        if (idx >= 0):
            return 1
        return 0
    
    
    def ILocalizeJournal(self):
    
        if journalFileName.value.startswith("py_"):
            journalPython = journalFileName.value[3:]
            
            if (PtGetLanguage() == PtLanguage.kFrench):
                code = "from %s_%s_french import *"
            elif (PtGetLanguage() == PtLanguage.kGerman):
                code = "from %s_%s_german import *"
            else:
                code = "from %s_%s import *"
            
            try:
                exec code % (PtGetAgeName(), journalPython)
                content = xJournalContents
            except:
                if PtGetLanguage() != PtLanguage.kEnglish:
                    print "Journal: not available in your language. Sorry. Will default to English."
                    try:
                        code = "from %s_%s import *"
                        exec code % (PtGetAgeName(), journalPython)
                        content = xJournalContents
                        print "Journal: reading in English was successfull."
                    except:
                        print "ERROR: journal file does not existat all, or access permission is denied."
                        content = errorContent % (PtGetAgeName() + "_" + journalPython + ".py")
                else:
                    print "ERROR: journal file does not exist, or access permission is denied."
                    content = errorContent % (PtGetAgeName() + "_" + journalPython + ".py")
            
            return content
        
        
        else:
            if (PtGetLanguage() == PtLanguage.kFrench):
                fullJournalPath = "ageresources\\" + PtGetAgeName() + "--" + journalFileName.value + "_french.txt"
            elif (PtGetLanguage() == PtLanguage.kGerman):
                fullJournalPath = "ageresources\\" + PtGetAgeName() + "--" + journalFileName.value + "_german.txt"
            else:
                fullJournalPath = "ageresources\\" + PtGetAgeName() + "--" + journalFileName.value + ".txt"
            

            print "Journal: content file should be:", fullJournalPath
            
            
            try:
                journalFile = open(fullJournalPath, 'r')
                content = journalFile.read()
                print "Journal: Reading was successfull."
            
            except:
                
                if PtGetLanguage() != PtLanguage.kEnglish:
                    print "Journal: not available in your language. Sorry. Will default to English."
                    fullJournalPath = "ageresources\\" + PtGetAgeName() + "--" + journalFileName.value + ".txt"
                    try:
                        journalFile = open(fullJournalPath, 'r')
                        content = journalFile.read()
                        print "Journal: reading in English was successfull."
                    except:
                        print "ERROR: journal file does not existat all, or access permission is denied."
                        content = errorContent % fullJournalPath
                
                else:
                    print "ERROR: journal file does not exist, or access permission is denied."
                    content = errorContent % fullJournalPath
            
            return content


    def IShowJournal(self):
        global JournalGUI
        
        content = self.ILocalizeJournal()

        # create a journal book of the correct size
        JournalGUI = ptBook(content, self.key)
        JournalGUI.setSize(bookWidth.value, bookHeight.value)
        
        if isNotebook.value:
            JournalGUI.setGUI("bkNotebook")
        else:
            JournalGUI.setGUI("BkBook")
        
        JournalGUI.allowPageTurning(true)
        if self.IsThereACover(content):
            JournalGUI.show(0)
        else:
            JournalGUI.show(1)













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
