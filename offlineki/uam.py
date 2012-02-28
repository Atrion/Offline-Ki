# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Copyright 2005-2010 Dustin Bernard                                        #
#    Copyright 2011      Diafero                                               #
#                                                                              #
#    This file is part of the Offline KI, based on code from                   #
#    UruAgeManager/Drizzle.                                                    #
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
#==============================================================================#
import Plasma, PlasmaKITypes, PlasmaConstants

_book = None # needs to be a global variable so the book will actually be shown
_agename = None
_spawnpoint = None
_ki = None # will be set in xUserKIBase

# Chronicle helpers
def SetAgeChronicle(varname, value):
    #print "SetAgeChronicle name=" + `varname` + " value="+`value`
    ageVault = Plasma.ptAgeVault()
    _SetChronicle(varname,value,ageVault)
def _SetChronicle(varname, value, vault, type=1):
    chronnode = vault.findChronicleEntry(varname)
    #print "cronnode:"+`chronnode`
    if chronnode==None:
        #create it
        vault.addChronicleEntry(varname,1,value) #type 1 seems to be stuff that *might* be for other players.  I think it might be ignored.
    else:
        chronnode.chronicleSetValue(value)
        chronnode.save()
def _SetPlayerChronicle(varname, value, type=1):
    #print "SetPlayerChronicle name=" + `varname` + " value="+`value`
    vault = Plasma.ptVault()
    _SetChronicle(varname,value,vault,type)
def GetAgeChronicle(varname):
    #print "GetAgeChronicle name=" + `varname`
    ageVault = Plasma.ptAgeVault()
    return _GetChronicle(varname,ageVault)
def _GetChronicle(varname, vault):
    chronnode = vault.findChronicleEntry(varname)
    #print "cronnode:"+`chronnode`
    if chronnode==None:
        #print "chronnode not found: "+`varname`
        #return None
        return ""
    else:
        value = chronnode.chronicleGetValue()
        #print "chronnode value: "+`value`
        return value
def _GetPlayerChronicle(varname):        
    #print "GetPlayerChronicle name=" + `varname`
    vault = Plasma.ptVault()
    return _GetChronicle(varname,vault)

# SDL helpers
def SetAgeSdl(varname, value, index=0):
    sdl = Plasma.PtGetAgeSDL()
    sdl.setFlags(varname, 1, 1)
    sdl.sendToClients(varname)
    sdl.setIndex(varname, index, value)
def GetAgeSdl(varname, index=0):
    sdl = Plasma.PtGetAgeSDL()
    return sdl[varname][index]

# Relto page enabling
def EnableReltoPage(pagename):
    import xCustomReltoPages # I leave the string helpers out of here because the original does not have them - and I want to be compatible in both directions
    print "uam.EnableReltoPage: "+str(pagename)
    #get current task list
    tasksstr = _GetPlayerChronicle("UamTasks")
    tasks = xCustomReltoPages._StringToList(tasksstr)
    #add item
    tasks.append("EnableReltoPage="+pagename)
    #save task list
    taskstr = xCustomReltoPages._ListToString(tasks)
    _SetPlayerChronicle("UamTasks",taskstr)
    Plasma.PtSendKIMessageInt(PlasmaKITypes.kStartBookAlert, 0)  #Flash the Relto book.
    print "uam.EnableReltoPage: current tasks: "+taskstr

# Misc little tools
def LinkToAge(agename, spawnpoint):
    #Use the OfflineKI for Pots/Alcugs:
    import xLinkMgr
    xLinkMgr.LinkToAge(agename,spawnpoint)
def PrintKiMessage(msg):
    _ki.IAddRTChat(None, msg, 0)
def SetTimer(callback, time):
    # will only work if UAM KI plugin is actually installed
    try:
        import _UamTimer
    except:
        raise Exception("UAM KI plugin not installed, can not set timer")
    _UamTimer.Timer(callback, time, False, True) #isweak=False, so that we can use local functions, and removewhenlink=True, so that timers are cancelled when linking out.

# showing a Book
def DisplayJournal(text, isOpen):
    _DisplayBook(text, isOpen, "bkNotebook")
def DisplayBook(text, isOpen):
    _DisplayBook(text, isOpen, "bkBook")
def _DisplayBook(text, isOpen, booktype):
    #booktype can be bkNotebook, bkBook, or bkBahroRockBook
    global _book
    _book = Plasma.ptBook(text, _ki.key)
    _book.setSize(1.0, 1.0)
    _book.setGUI(booktype)
    _book.allowPageTurning(True)
    _book.show(isOpen)
def DisplayLinkingBook(agename, spawnpoint):
    global _book
    global _agename
    global _spawnpoint
    _agename = agename
    _spawnpoint = spawnpoint
    contents = '<pb><img src="xLinkPanelBlackVoid*1#0.hsm" align=center link=100 blend=alpha >'
    _book = Plasma.ptBook(contents, _ki.key)
    _book.setSize(1.0, 1.0)
    _book.setGUI('BkBook')
    _book.allowPageTurning(True)
    _book.show(1)
def _handleClick():
    #after this, the .kNotifyHide event will still be called, so the _book = None can be done then.
    if _book != None and _agename != None and _spawnpoint != None:
        print "uam._handleClick: linking"
        _book.hide()
        LinkToAge(_agename,_spawnpoint)
        return True #don't let xKI.py process the rest!
    return False
def _bookHidden():
    global _book
    _book = None
def _bookShown():
    if _book != None and _agename != None and _spawnpoint != None:
        import booksDustGlobal
        bookmap = booksDustGlobal.BookMapRight
        import xLinkMgr
        img = xLinkMgr.GetLinkingImage(_agename, _spawnpoint, width=410, height=168)
        if img != None:
            bookmap.textmap.drawImage(50, 60, img, 0)
