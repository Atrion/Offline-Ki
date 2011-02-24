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
from PlasmaKITypes import *
from PlasmaNetConstants import *
import xLinkingBookDefs
import os
import re
import xLinkMgr
import xxConfig

availableBooks = ['Link19',
 'Link20',
 'Link21',
 'Link22',
 'Link23',
 'Link24',
 'Link25',
 'Link26',
 'Link27',
 'Link28',
 'Link29',
 'Link30',
 'Link31',
 'Link32',
 'Link33',
 'Link34',
 'Link35',
 'Link36']
_Books = {} # maps the above names to a Book instance

class _Book:
    def __init__(self, nr):
        self.pages = []
        self.cover = ''
        self.nr = nr
        print "xCustomReltoShelf: Creating new book %d" % nr
    
    def addPage(self, page):
        if page.isVisible(): # only add page if it is actually visible
            self.pages.append(page)
    
    def isVisible(self):
        for page in self.pages:
            if page.showBook():
                return True # we found a page that lets the book show, go on!
        return False # no, nothing triggers this book to be shown


class _LinkPage:
    def __init__(self, age, spawnpoint = None):
        self.age = age
        self.spawnpoint = spawnpoint
        self.isAge = True
        self.video = self._getVideoFile()
        print "xCustomReltoShelf: Adding link to %s" % age

    def _getVideoFile(self):
        files = ['avi/%s_%s.bik' % (self.age, self.spawnpoint), 'avi/%s.bik' % self.age]
        for file in files:
            if os.path.exists(file):
                print 'xCustomReltoShelf: Found video file %s for age %s' % (file, self.age)
                return file
        return None

    def showBook(self): # returns whether the book should be shown if only this page is visible
        return True

    def isVisible(self): # returns whether this page has anything to display
        return xLinkMgr.IsAgeAvailable(self.age)

    def getPanel(self):
        if self.video != None:
            return '<movie src="' + self.video + '" align=center link=%d resize=yes>'
        return '<img src="xLinkPanelBlackVoid*1#0.hsm" align=center link=%d blend=alpha>' # the cover might be replaced later on, when the book is actually shown
        
    def getTitle(self):
        return xLinkMgr.GetInstanceName(self.age)
        
    def getText(self):
        return xLinkMgr.GetDescription(self.age)
    
    def clicked(self):
        xLinkMgr.LinkToAge(self.age, self.spawnpoint)
        
    def linkingImage(self, width, height):
        if self.video != None:
            return None # do not put a cover on top of the video
        return xLinkMgr.GetLinkingImage(self.age, self.spawnpoint, width, height)


class _DescriptivePage:
    def __init__(self, title, text):
        self.title = title
        text = text.replace(';', ',')
        text = text.replace('\\n', '\n')
        self.text = text
        self.isAge = False
        print "xCustomReltoShelf: Adding descriptive text %s" % title

    def showBook(self):
        return False # do not show a book just because of the descriptive text

    def isVisible(self):
        return True # sure, always show if we are asked to!

    def getPanel(self):
        return '<font size=%d>' # it must have a %d so that the format string looks like expected!

    def getTitle(self):
        return self.title

    def getText(self):
        return self.text
        
    # this class does not implement clicked() on purpose - it was an error if it would ever be called
    
    def linkingImage(self, width, height):
        return None


def ParseULMFile():
    global _Books
    _Books = {}
    if os.path.exists('ULMServerLinkBook.inf'):
        f = open('ULMServerLinkBook.inf')
    elif os.path.exists('ULMLinkBook.inf'):
        f = open('ULMLinkBook.inf')
    else:
        return
    try:
        linkBook = None
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            if not len(line) or line.startswith('#'): continue # skip
            m = re.search('^\\[Book( ([0-9][0-7]?))?\\]$', line)
            if (m != None):
                # a book header
                booknr = m.groups()[1] # the index 0 is the number including leading space
                if booknr != None: # a book number was given
                    linkBook = _Book(int(booknr)) # choose number given in the header
                elif linkBook != None:
                    linkBook = _Book(linkBook.nr+1) # choose next consecutive number
                else:
                    linkBook = _Book(0) # the very first book
                # save book in list
                _Books[availableBooks[linkBook.nr]] = linkBook
            else:
                if (linkBook == None): continue # we first need a book header before aprsing anything else
                # get header (type) of line and the data segments
                pos = line.find(':')
                if pos <= 0: continue # a comment
                type = line[:pos]
                data = line[pos+1:].split(",")
                # process line
                if type == 'cover':
                    if len(data) == 1:
                        # save cover
                        linkBook.cover = data[0]
                elif type == 'link':
                    # an old-style link - read only age name and spawn point, if it exists
                    # The syntax is as follows:
                    # link:agefilename,agefullname[,description[,condition]]
                    # (if the filename is empty in this case, it is trated as text-only descriptive page)
                    # OR
                    # link:agefilename,agefullname,spawnpoint,description,condition
                    # OR
                    # link:agefilename,agefullname,spawnpoint,description,imagename,condition
                    if len(data) >= 5: # spawnpoint given
                        linkBook.addPage(_LinkPage(data[0], data[4]))
                    elif len(data) >= 3 and not len(data[0]):
                        # old-style text
                        linkBook.addPage(_DescriptivePage(data[1], data[2]))
                    else:
                        linkBook.addPage(_LinkPage(data[0]))
                elif type == 'age':
                    # new-style link: either just the age name, or name and spawn point
                    if len(data) == 2:
                        linkBook.addPage(_LinkPage(data[0], data[1]))
                    elif len(data) == 1:
                        linkBook.addPage(_LinkPage(data[0]))
                elif type == "text":
                    # a text-only page with no link
                    if len(data) == 2:
                        linkBook.addPage(_DescriptivePage(data[0], data[1]))
    finally:
        f.close()


def GetLinkingImage(bookname, pageid, width, height):
    book = _Books[bookname]
    page = book.pages[pageid]
    return page.linkingImage(width, height)


def GetBookCover(bookname):
    global _Books
    if (not bookname in _Books): return ''
    return _Books[bookname].cover


def BuildBook(bookname):
    SpawnPoint_Dict = {}
    x = xLinkingBookDefs.kFirstLinkPanelID
    linkBookPrefix = 'xxCustomBookxx_' # the way xLinkMgrGUIPopup works requires us to write stuff into the global linking definition array - we use this name plus the index of the page to avoid overwriting anything
    print ('xCustomReltoShelf: Building up Linking book ' + bookname)
    for page in _Books[bookname].pages:
        pagename = linkBookPrefix+str(x) # the only important thing is that it is unique for the current book
        source = '<font size=28 face=Uru ><p align=center>%s\n\n<font size=24 face=Uru>%s<pb>%s' % (page.getTitle(), page.getText(), page.getPanel()) # this text has a %d for the panel ID!
        print "xCustomReltoShelf: Source of page %s is %s" % (pagename, source)
            
        # "communication" with xLinkMgrGUIPopup
        print 'xCustomReltoShelf: Setting xLinkingBookDefs entries'
        xLinkingBookDefs.xAgeLinkingBooks[pagename] = (0, 1.0, 1.0, '',
            '%s%s'+(source % xLinkingBookDefs.kFirstLinkPanelID)) # fill in panel ID
        xLinkingBookDefs.xLinkDestinations[pagename] = page # we can access that later, in the click handler
        xLinkingBookDefs.xLinkingPages[pagename] = '<pb>'+source # keep the panel ID (xLinkMgrGUIPopup will fill in)
        
        # some finalization
        SpawnPoint_Dict[x] = pagename
        x += 1
    return (SpawnPoint_Dict, SpawnPoint_Dict)


def PageClicked(spTitle): # xLinkMgrGUIPopup gives us the name we chose for that page in the build function
    page = xLinkingBookDefs.xLinkDestinations[spTitle]
    page.clicked()


def UpdateBooks(linkLibrary, objLibrary, actBook):
    for book in availableBooks:
        try:
            index = linkLibrary.index(book)
        except:
            print (('xCustomReltoShelf: ERROR: Custom book ' + book) + 'not in library!')
            continue
        activeBook = (book in _Books) and _Books[book].isVisible()
        print "xCustomReltoShelf: Book %s.active: %s" % (book, str(activeBook))
        # (de)activate current book
        objBook = objLibrary.value[index]
        if activeBook:
            objBook.draw.enable()
        else:
            objBook.draw.disable()
        objBook.physics.suppress(1)
        bookName = objBook.getName()
        for (key, value,) in actBook.byObject.items():
            parent = value.getParentKey()
            if parent:
                if (bookName == parent.getName()):
                    if activeBook:
                        actBook.enable(objectName=key)
                        objBook.physics.suppress(0)
                    else:
                        actBook.disable(objectName=key)
                        objBook.physics.suppress(1)
                    break
