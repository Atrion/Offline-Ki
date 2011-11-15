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

# From _UamUtils
#For dealing with String->String dictionaries (musn't contain ; nor = nor rely on whitespace on the ends. )
def _DictToString(dict):
    str_list = []
    first = True
    for key in dict:
        val = dict[key]
        if not first:
            str_list.append(";")
        str_list.append(key+"="+val)
        first = False
    result = ''.join(str_list)
    return result
def _StringToDict(str):
    result = {}
    if str=="":
        return result
    list = str.split(";")
    for item in list:
        #parts = item.split("=")
        #if len(parts)==2:
        #    result[parts[0].strip()] = parts[1].strip()  #remove whitespace off the ends
        #else:
        #    #skip this part
        #    pass
        ind = item.find("=")
        if ind!=-1:
            result[item[:ind].strip()] = item[ind+1:].strip()  #remove whitespace off the ends
        else:
            #skip this part
            pass
    return result
def _ListToString(list):
    str_list = []
    first = True
    for val in list:
        if not first:
            str_list.append(";")
        str_list.append(val)
        first = False
    result = ''.join(str_list)
    return result
def _StringToList(str):
    result = []
    if str=="":
        return result
    list = str.split(";")
    for item in list:
        item = item.strip()
        if item!="":
            result.append(item)
    return result


# From uam
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
