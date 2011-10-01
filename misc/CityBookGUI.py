# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#    See the file AUTHORS for more info about the contributors.                #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                      #
#                                                                              #
#    You may re-use the code in this file within the context of Uru.           #
#                                                                              #
#==============================================================================#
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaNetConstants import *
import xLinkingBookDefs
import os
actClickableObject = ptAttribActivator(1, 'Act: Clickable Object')
ObjectMsg = ptAttribString(2, 'Object String')
ourBook = None
bkLinks = []
modPageDefs = __import__('CityPageDefs')
ageBooks = ['M-NegilahnBook',
 'M-DerenoBook',
 'M-PayiferenBook',
 'M-TetsonotBook',
 'jrnlNegilahn',
 'LIBMinkataBook',
 'LIBJalakBook',
 'DniLinkingBookToDelin',
 'DniLinkingBookToGZ',
 'EderTsogalLinkBook',
 'BahroRockBook',
 'jrnlJalak',
 'jrnlMinkata',
 'BahroBookDescent',
 'BahroBookKadish',
 'BahroStoneKveer',
 'MT-LinkingBook',
 'NbhoodLinkingBook',
 'LIBReleeshanBook',
 'M-TodelmerBook',
 'GuildRockBook',
 'SeretRockBook']
bookPages = [['M-NegilahnBook'],
 ['M-DerenoBook'],
 ['M-PayiferenBook'],
 ['M-TetsonotBook'],
 ['NegilahnJournal'],
 ['LIBMinkataBook'],
 ['LIBJalakBook'],
 ['DniLinkingBookToDelin'],
 ['DniLinkingBookToGZ'],
 ['EderTsogalLinkBook'],
 ['BahroRockBook'],
 ['JalakJournal'],
 ['MinkataJournal'],
 ['BahroBookDescent'],
 ['BahroBookKadish'],
 ['BahroStoneKveer'],
 ['MT-LinkingBook'],
 ['NbhoodLinkingBook'],
 ['LIBReleeshanBook'],
 ['M-TodelmerBook'],
 ['GuildRockBook'],
 ['SeretRockBook']]
class CityBookGUI(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.version = '3.0'
        print ('__init__%s v.%s' % (self.__class__.__name__,
         self.version))


    def OnNotify(self, state, id, events):
        print ('%s: OnNotify called' % self.__class__.__name__)
        if ((id == actClickableObject.id) and state):
            print ('Someone clicked on object %s' % ObjectMsg.value)
            if PtWasLocallyNotified(self.key):
                print 'It was you'
                for (a, b,) in zip(ageBooks, bookPages):
                    print ('Trying book %s with page(s) %s' % (a,
                     b))
                    if (ObjectMsg.value == a):
                        print 'Match found! Start opening book...'
                        self.IOpenBook(a, b)
                        break
                    else:
                        print 'No match'
        else:
            for event in events:
                if ((event[0] == PtEventType.kBook) and PtWasLocallyNotified(self.key)):
                    if (event[1] == PtBookEventTypes.kNotifyImageLink):
                        print ('BookNotify: Linking panel id=%d, event=%d' % (event[2],
                         event[1]))
                        ourBook.hide()
                        if (event[2] == 0):
                            print 'Warning: No link id, define proper link destination or use non-clickable image'
                        elif (event[2] >= xLinkingBookDefs.kFirstLinkPanelID):
                            for i in range(0, len(bkLinks)):
                                if (event[2] == bkLinks[i][0]):
                                    try:
                                        self.IlinkToAge(bkLinks[i][1], bkLinks[i][2], bkLinks[i][3], bkLinks[i][4], bkLinks[i][5])
                                    except Exception, detail:
                                        print ('ERROR: Unable to initialize link - %s' % detail)
                                    break
                    elif (event[1] == PtBookEventTypes.kNotifyShow):
                        print ('BookNotify: Show book, event=%d' % event[1])
                        PtToggleAvatarClickability(0)
                    elif (event[1] == PtBookEventTypes.kNotifyHide):
                        print ('BookNotify: Hide book, event=%d' % event[1])
                        PtToggleAvatarClickability(1)
                    elif (event[1] == PtBookEventTypes.kNotifyNextPage):
                        print ('BookNotify: To next page %d, event=%d' % (ourBook.getCurrentPage(),
                         event[1]))
                    elif (event[1] == PtBookEventTypes.kNotifyPreviousPage):
                        print ('BookNotify: To previous page %d, event=%d' % (ourBook.getCurrentPage(),
                         event[1]))
                    elif (event[1] == PtBookEventTypes.kNotifyCheckUnchecked):
                        print ('BookNotify: Relto page toggle, event=%d' % event[1])
                    elif (event[1] == PtBookEventTypes.kNotifyClose):
                        print ('BookNotify: Close book, event=%d' % event[1])



    def IOpenBook(self, ageBook, bkPages = None):
        global ourBook
        global bkLinks
        print ('%s: IOpenBook: Page(s) requested %s' % (self.__class__.__name__,
         bkPages))
        if (type(bkPages) == type(None)):
            print 'ERROR: no pages defined'
            return
        if (not (ageBook in modPageDefs.AgeBooks)):
            print ('ERROR: Definition %s does not exist in AgeBooks' % ageBook)
            return
        bkParams = modPageDefs.AgeBooks[ageBook]
        (bkCover, bkFont, startOpen, forceOwned, bookGUI, width, height,) = bkParams
        PageDef = (bkCover + bkFont)
        if (not startOpen):
            if (not self.IsThereACover(PageDef)):
                print 'Warning: Missing cover, forcing book open'
                startOpen = 1
        PageCount = xLinkingBookDefs.kFirstLinkPanelID
        bkLinks = []
        for bkPage in bkPages:
            if (not (bkPage in modPageDefs.LinkDestinations)):
                print ('Warning: %s skipped, definition does not exist in LinkDestinations' % bkPage)
                continue
            pgParams = modPageDefs.LinkDestinations[bkPage]
            (bkAge, spawnPoint, spTitle, linkRule,) = pgParams
            alink = 1
            if ((type(bkAge) != type(None)) and forceOwned):
                print ('Ownership check for %s book' % bkAge)
                vault = ptVault()
                ainfo = ptAgeInfoStruct()
                ainfo.setAgeFilename(bkAge)
                alink = vault.getOwnedAgeLink(ainfo)
            if alink:
                print ('Showing %s, link destination %s' % (bkPage,
                 bkAge))
                if (type(bkAge) != type(None)):
                    t = (PageCount,
                     bkPage,
                     bkAge,
                     spawnPoint,
                     spTitle,
                     linkRule)
                    bkLinks.append(t)
                    PageDef = ((PageDef + (modPageDefs.BookPages[bkPage] % PageCount)) + '<pb>')
                else:
                    PageDef = ((PageDef + modPageDefs.BookPages[bkPage]) + '<pb>')
                PageCount = (PageCount + 1)
            else:
                print ('No owner of age %s so we are not showing %s' % (bkAge,
                 bkPage))
        if (PageCount == xLinkingBookDefs.kFirstLinkPanelID):
            print 'No pages created...'
            return
        else:
            TotalCount = (PageCount - xLinkingBookDefs.kFirstLinkPanelID)
        print ('%d item(s) created, linking page(s): %d' % (TotalCount,
         len(bkLinks)))
        PageDef = PageDef[:-4]
        ourBook = ptBook(PageDef, self.key)
        ourBook.setSize(width, height)
        ourBook.setGUI(bookGUI)
        ourBook.show(startOpen)


    def IsThereACover(self, bookHtml):
        idx = bookHtml.find('<cover')
        if (idx >= 0):
            return 1
        return 0


    def IlinkToAge(self, bookPage, ageName, spawnPoint, spTitle, linkRule):
        import xLinkMgr
        xLinkMgr.LinkToAge(ageName, spawnPoint)
        print ('Linking to age %s, spawnpoint %s with title %s, using linkingrule %d' % (ageName,
         spawnPoint,
         spTitle,
         linkRule))


    def IConvertAgeInstanceName(self, ageName):
        if (ageName == 'Personal'):
            return 'Relto'
        if (ageName == 'Pahts'):
            return 'Ahra Pahts'
        if (ageName == 'KveerMOUL'):
            return 'New Kveer'
        if (ageName == 'EderDelin'):
            return 'Eder Delin'
        if (ageName == 'EderTsogal'):
            return 'Eder Tsogal'
        if (ageName == 'GreatZero'):
            return 'Great Zero'
        return ageName


    def IDoSpecialAction(self, bookPage):
        if (bookPage == '*YourPage*'):
            print ('Special action found for %s' % bookPage)
        else:
            print 'No special actions found'


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
    global glue_params
    global glue_paramKeys
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
                print ('%s has id %d which is already defined in %s' % (obj.name, obj.id, glue_params[obj.id].name))
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
    global glue_params
    global glue_paramKeys
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
    global glue_paramKeys
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
            print 'setParam: can\'t find id=',
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
    global glue_paramKeys
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



