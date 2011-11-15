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
import PlasmaConstants
import os
import uam

ReltoPages = None #{}

### From _UamUtils
def AmInMyRelto():
    return Plasma.ptVault().inMyPersonalAge()

def HideObject(objectname):
    #Hides and disables a sceneobject
    #print "hide:"+objectname
    agename = GetAgeName()
    try:
        av = Plasma.PtFindSceneobject(objectname, agename)
    except:
        print "_UamUtils.HideObject unable to find object: "+objectname
        return False
    av.draw.disable()
    av.physics.suppress(1)
    return True

def GetLanguage():
    langnum = Plasma.PtGetLanguage()
    if langnum==0:
        return "en"
    elif langnum==1:
        return "fr"
    elif langnum==2:
        return "de"
    else:
        raise Exception("Unexpected language")



### From _UamMod_ReltoPages
def TogglePage(pagenum):
    #Get page for this pagenum
    pagedict = FindPage(pagenum)
    if pagedict==None:
        return False
    pagename = pagedict["pagename"]

    #Get the current status of the pages
    chronstr = uam.GetAgeChronicle("UamReltoPages") #on, off, or unattained
    pages = uam._StringToDict(chronstr)
    #print "chronstr: "+chronstr
    
    status = pages.get(pagename,pagedict["default"])  #Get the status or use the default for this page.
    if status=="on":
        status = "off"
    elif status=="off":
        status = "on"
    else:
        raise "Unexpected page state"
    
    #save the new status
    pages[pagename] = status
    pagesstr = uam._DictToString(pages)
    uam.SetAgeChronicle("UamReltoPages",pagesstr)
    #print "chronstr: "+pagesstr
    return True
    
def FindPage(pagenum):
    for page in ReltoPages:
        pagedict = ReltoPages[page]
        curpagenum = int(pagedict["pagenum"])
        if pagenum==curpagenum:
            return pagedict
    return None

#Read definitions from /img/UamRelto folder?
def ReadPageInfo():
    global ReltoPages
    ReltoPages = {}
    print "xCustomReltoPages: reading page info"
    if os.path.exists("img/UamRelto/"):
        files = os.listdir("img/UamRelto/")
    else:
        return
    for filename in files:
        if filename.startswith("UamRelto--") and filename.endswith(".txt"):
            pagename = filename[len("UamRelto--"):len(filename)-len(".txt")] #get the inside part
            #print "pagename: "+pagename
            f = file("img/UamRelto/"+filename,"r")
            contents = f.read()
            f.close()
            pagedict = uam._StringToDict(contents)
            pagenum = int(pagedict["pagenum"])
            if pagenum<100:
                raise Exception("pagenum must be over 100.")
            pagestate = pagedict["default"]
            if pagestate!="off" and pagestate!="unattained":
                raise Exception("default must be either 'off' or 'unattained'")
            en = pagedict.get("text--en")
            de = pagedict.get("text--de")
            fr = pagedict.get("text--fr")
            hidetxt = pagedict.get("hide") #looks like Object1,Object2,Object3
            hideitems = []
            if hidetxt!=None:
                for hideitem in hidetxt.split(","):
                    hideitem = hideitem.strip()
                    if hideitem!="":
                        hideitems.append(hideitem)
            #default text is English if we got it, otherwise just the pagename.
            if en!=None:
                dt = en
            else:
                dt = pagename
            if en==None:
                en = dt
            if de==None:
                de = dt
            if fr==None:
                fr = dt
            pagedict["text--en"] = en
            pagedict["text--de"] = de
            pagedict["text--fr"] = fr
            pagedict["pagename"] = pagename
            pagedict["hide"] = hideitems
            ReltoPages[pagename] = pagedict

#Listen for link-in to a Relto, so we can load the appropriate pages
def LoadReltoPages():
    #Read any updated pages
    ReadPageInfo()

    #Do tasks given from other Ages: The player collected a Relto page, enable it
    if AmInMyRelto():
        tasksstr = uam._GetPlayerChronicle("UamTasks")
        tasks = uam._StringToList(tasksstr)
        numtasks = len(tasks)
        for task in tasks:
            #print "task to do: "+task
            if task.startswith("EnableReltoPage="):
                page = task[len("EnableReltoPage="):]
                #enable the page
                pages = uam._StringToDict(uam.GetAgeChronicle("UamReltoPages"))
                pages[page] = "on"  #whether it was unset or on or off or unattained, it is on now!
                uam.SetAgeChronicle("UamReltoPages",uam._DictToString(pages))
                #remove from task list
                tasks.remove(task)
        if numtasks!=len(tasks):
            #removed some, so save
            uam._SetPlayerChronicle("UamTasks",uam._ListToString(tasks))
    
    #Load pages
    PagesToLoad = {} #set() #Sets don't exist in Python 2.2 :P
    ObjectsToHide = {} #set() #Sets don't exist in Python 2.2 :P
    print "xCustomReltoPages: Loading Uam pages..."
    chronstr = uam.GetAgeChronicle("UamReltoPages") #on, off, or unattained
    pages = uam._StringToDict(chronstr)
    #print "UamReltoPages: "+chronstr
    for pagename in pages:
        status = pages[pagename]
        if status=="on":
            #PagesToLoad.add(pagename)
            PagesToLoad[pagename] = None #we're using this dict as a set
            for hideitem in ReltoPages[pagename]["hide"]:
                #ObjectsToHide.add(hideitem)
                ObjectsToHide[hideitem] = None #we're using this dict as a set
    #Turn into sorted lists
    PagesToLoad = PagesToLoad.keys()
    ObjectsToHide = ObjectsToHide.keys()
    PagesToLoad.sort()
    ObjectsToHide.sort()
    #Hide the objects
    for hideitem in ObjectsToHide:
        #print "Hiding obj: "+hideitem
        HideObject(hideitem)
    #Load the pages
    for pagename in PagesToLoad:
        #print "Loading page: "+pagename
        Plasma.PtPageInNode("UamPage-"+pagename)  #doesn't throw an exception if page not present; simply doesn't load.

#Listen to page defs for the Relto book
def CustomYeeshaPageDefs():
    #print "_UamModReltopages._IGetYeeshaPageDefs"
    result = ''
    
    #Can only change this while in your Relto
    vault = Plasma.ptVault()
    if not vault.inMyPersonalAge():
        result += "<pb><pb><font size=32 face=Uru><p align=center>You can only change the fan-made pages while on your Relto."
        return result

    #Get the current status of the pages
    chronstr = uam.GetAgeChronicle("UamReltoPages") #on, off, or unattained
    pages = uam._StringToDict(chronstr)
    

    names = ReltoPages.keys()
    names.sort()
    for page in names:
        pagedict = ReltoPages[page]
        pagenum = int(pagedict["pagenum"])
        lang = GetLanguage()
        #print "language: "+`lang`
        linktext = pagedict["text--"+lang]
        linknum = pagenum + 200  #just to get it out of Cyan's hair
        turnedon = 1  #1 or 0
        status = pages.get(page,pagedict["default"])  #Get the status or use the default for this page.
        #print "status: "+status
        if status=="on":
            turnedon = 1
        else:
            turnedon = 0  #either off or unattained
        if status=="on" or status=="off":
            result += '<pb><font size=32 face=Uru ><p align=center>'+linktext
            result += '<pb><img src="xYeeshaPageAlphaSketchFiremarbles*1#0.hsm" align=center check=00ff18,00800c,'+str(turnedon)+' link='+str(linknum)+'>'
    return result
