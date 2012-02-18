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
import Plasma

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

# Relto page enabling
def EnableReltoPage(pagename):
    print "uam.EnableReltoPage: "+`pagename`
    #get current task list
    tasksstr = _GetPlayerChronicle("UamTasks")
    tasks = _StringToList(tasksstr)
    #add item
    tasks.append("EnableReltoPage="+pagename)
    #save task list
    taskstr = _ListToString(tasks)
    _SetPlayerChronicle("UamTasks",taskstr)
    Plasma.PtSendKIMessageInt(PlasmaKITypes.kStartBookAlert, 0)  #Flash the Relto book.
    print "current tasks: "+taskstr

# Misc little tools
def LinkToAge(agename, spawnpoint):
    #Use the OfflineKI for Pots/Alcugs:
    import xLinkMgr
    xLinkMgr.LinkToAge(agename,spawnpoint)
def PrintKiMessage(msg):
    _ki.IAddRTChat(None, msg, 0)
def SetTimer(callback, time):
    # will only work if UAM KI plugin is actually installed
    import _UamTimer
    _UamTimer.Timer(callback, time, False, True) #isweak=False, so that we can use local functions, and removewhenlink=True, so that timers are cancelled when linking out.
