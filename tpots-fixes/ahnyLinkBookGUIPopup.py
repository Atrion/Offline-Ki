# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import string
import xLinkingBookDefs
from xPsnlVaultSDL import *
import time
actClickableBook = ptAttribActivator(1, 'Actvtr: Clickable small book')
SeekBehavior = ptAttribBehavior(2, 'Smart seek before GUI (optional)')
respLinkResponder = ptAttribResponder(3, 'Rspndr: Link out')
TargetAge = ptAttribString(4, 'Name of Linking Panel', 'Teledahn')
actBookshelf = ptAttribActivator(5, 'Bookshelf (Only used in PsnlAge)')
shareRegion = ptAttribActivator(6, 'region in which the sharer must remain')
shareBookSeek = ptAttribBehavior(7, 'smart seek & use book for share acceptance')
IsDRCStamped = ptAttribBoolean(10, 'DRC Stamp', default=1)
respLinkSphere01 = ptAttribResponder(11, 'sphere 01 resp')
respLinkSphere02 = ptAttribResponder(12, 'sphere 02 resp')
respLinkSphere03 = ptAttribResponder(13, 'sphere 03 resp')
respLinkSphere04 = ptAttribResponder(14, 'sphere 04 resp')
LocalAvatar = None
OfferedBookMode = false
BookOfferer = None
stringAgeRequested = None
PageID_List = []
SpawnPointName_Dict = {}
SpawnPointTitle_Dict = {}
OffereeWalking = false
ClosedBookToShare = 0
BookNumber = 0
CurrentPage = 1
gLinkingBook = None
NoReenableBook = 0
kGrsnTeamBook = 99

class ahnyLinkBookGUIPopup(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5345
        version = 27
        minor = 4
        self.version = version
        PtDebugPrint(('__init__ahnyLinkBookGUIPopup v%d.%d' % (version, minor)))


    def OnServerInitComplete(self):
        if actBookshelf:
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags('CurrentPage', 1, 1)
            ageSDL.sendToClients('CurrentPage')


    def __del__(self):
        pass


    def OnNotify(self, state, id, events):
        global LocalAvatar
        global OfferedBookMode
        global BookOfferer
        global CurrentPage
        global gLinkingBook
        global ClosedBookToShare
        global NoReenableBook
        print 'id = ',
        print id
        if (id == actClickableBook.id):
            if (PtWasLocallyNotified(self.key) and state):
                actClickableBook.disable()
                PtToggleAvatarClickability(false)
                if (type(SeekBehavior.value) != type(None)):
                    PtDebugPrint('ahnyLinkBookGUIPopup: Smart seek used', level=kDebugDumpLevel)
                    LocalAvatar = PtFindAvatar(events)
                    SeekBehavior.run(LocalAvatar)
                    return
                self.IShowBookNoTreasure()
                OfferedBookMode = false
                BookOfferer = None
            return
        elif (id == SeekBehavior.id):
            if PtWasLocallyNotified(self.key):
                for event in events:
                    if ((event[0] == kMultiStageEvent) and (event[2] == kEnterStage)):
                        SeekBehavior.gotoStage(LocalAvatar, -1)
                        PtDebugPrint('ahnyLinkBookGUIPopup: attempting to draw link panel gui', level=kDebugDumpLevel)
                        self.IShowBookNoTreasure()
                        OfferedBookMode = false
                        BookOfferer = None
        else:
            for event in events:
                if (event[0] == PtEventType.kBook):
                    PtDebugPrint(('ahnyLinkBookGUIPopup: BookNotify  event=%d, id=%d' % (event[1], event[2])), level=kDebugDumpLevel)
                    if (event[1] == PtBookEventTypes.kNotifyImageLink):
                        if ((event[2] >= xLinkingBookDefs.kFirstLinkPanelID) or (event[2] == xLinkingBookDefs.kBookMarkID)):
                            PtDebugPrint(('ahnyLinkBookGUIPopup:Book: hit linking panel %s' % event[2]), level=kDebugDumpLevel)
                            self.HideBook(1)
                            respNum = self.GetCurrentSphere()
                            print 'respNum:',
                            print respNum
                            sdl = xPsnlVaultSDL()
                            resetSDL = sdl['AhnySphereDelete'][0]
                            if resetSDL:
                                vault = ptVault()
                                iown = vault.getAgesIOwnFolder()
                                for i in iown.getChildNodeRefList():
                                    i = i.getChild()
                                    link = i.upcastToAgeLinkNode()
                                    info = link.getAgeInfo()
                                    if info:
                                        name = info.getAgeFilename()
                                        if (name == 'Ahnonay'):
                                            print 'attempting to reset sdl for',
                                            print name
                                            asdl = info.getAgeSDL()
                                            sdr = asdl.getStateDataRecord()
                                            sdr.setFromDefaults(1)
                                            asdl.setStateDataRecord(sdr)
                                            asdl.save()
                                        elif ((name == 'AhnySphere01') or ((name == 'AhnySphere02') or ((name == 'AhnySphere03') or (name == 'AhnySphere04')))):
                                            link.setVolatile(1)
                                            link.save()
                                sdl['AhnySphereDelete'] = (0,)
                                respNum = 1
                            if ((respNum == 1) or (respNum == 0)):
                                respLinkSphere01.run(self.key, avatar=PtGetLocalAvatar())
                            elif (respNum == 2):
                                respLinkSphere02.run(self.key, avatar=PtGetLocalAvatar())
                            elif (respNum == 3):
                                respLinkSphere03.run(self.key, avatar=PtGetLocalAvatar())
                            elif (respNum == 4):
# Ahnonay Sphere 4 work-around BEGIN
                                PtSendKIMessage(kKISitOnNextLinkOut, 0)
# Ahnonay Sphere 4 work-around END
                                respLinkSphere04.run(self.key, avatar=PtGetLocalAvatar())
                            else:
                                print 'Whoa - invalid current sphere!'
                                return
                    elif (event[1] == PtBookEventTypes.kNotifyShow):
                        PtDebugPrint('ahnyLinkBookGUIPopup:Book: NotifyShow', level=kDebugDumpLevel)
                        PtSendKIMessage(kEnableKIandBB, 0)
                        if (CurrentPage > 1):
                            PtDebugPrint(('ahnyLinkBookGUIPopup: going to page %d (ptBook page %d)' % (CurrentPage, ((CurrentPage - 1) * 2))), level=kDebugDumpLevel)
                            gLinkingBook.goToPage(((CurrentPage - 1) * 2))
                    elif (event[1] == PtBookEventTypes.kNotifyHide):
                        PtDebugPrint('ahnyLinkBookGUIPopup:Book: NotifyHide', level=kDebugDumpLevel)
                        if (not (ClosedBookToShare)):
                            PtToggleAvatarClickability(true)
                            if (OfferedBookMode and BookOfferer):
                                avID = PtGetClientIDFromAvatarKey(BookOfferer.getKey())
                                PtNotifyOffererLinkRejected(avID)
                                PtDebugPrint('ahnyLinkBookGUIPopup: rejected link, notifying offerer as such', level=kDebugDumpLevel)
                                OfferedBookMode = false
                                BookOfferer = None
                        if (not (NoReenableBook)):
                            actClickableBook.enable()
                        ClosedBookToShare = 0
                    elif (event[1] == PtBookEventTypes.kNotifyCheckUnchecked):
                        PtDebugPrint('ahnyLinkBookGUIPopup:Book: NotifyCheckUncheck', level=kDebugDumpLevel)


    def IShowBookNoTreasure(self):
        global stringAgeRequested
        global SpawnPointName_Dict
        global SpawnPointTitle_Dict
        global gLinkingBook
        showOpen = 0
        if (len(actBookshelf.value) == 0):
            agePanel = TargetAge.value
            showOpen = 1
        else:
            agePanel = stringAgeRequested
            showOpen = 0
        if agePanel:
            try:
                params = xLinkingBookDefs.xAgeLinkingBooks[agePanel]
                if (len(params) == 6):
                    (sharable, width, height, stampdef, bookdef, gui) = params
                elif (len(params) == 5):
                    (sharable, width, height, stampdef, bookdef) = params
                    gui = 'BkBook'
                else:
                    return
                if (not (IsDRCStamped.value)):
                    stampdef = xLinkingBookDefs.NoDRCStamp
                if sharable:
                    PtDebugPrint(('ahnyLinkBookGUIPopup: %s\'s book definition can\'t be shared' % agePanel), level=kErrorLevel)
                else:
                    bookdef = (bookdef % ('', stampdef))
                SpawnPointName_Dict[0] = 'LinkInPointDefault'
                SpawnPointTitle_Dict[0] = agePanel
                PtSendKIMessage(kDisableKIandBB, 0)
                gLinkingBook = ptBook(bookdef, self.key)
                gLinkingBook.setSize(width, height)
                if (not (showOpen)):
                    if (not (self.IsThereACover(bookdef))):
                        showOpen = 1
                gLinkingBook.setGUI(gui)
                gLinkingBook.show(showOpen)
            except LookupError:
                PtDebugPrint(('ahnyLinkBookGUIPopup: could not find age %s\'s linking panel' % agePanel), level=kErrorLevel)
        else:
            PtDebugPrint(('ahnyLinkBookGUIPopup: no age link panel' % agePanel), level=kErrorLevel)


    def IsThereACover(self, bookHtml):
        idx = bookHtml.find('<cover')
        if (idx > 0):
            return 1
        return 0


    def HideBook(self, islinking = 0):
        global NoReenableBook
        global gLinkingBook
        if islinking:
            NoReenableBook = 1
        else:
            NoReenableBook = 0
        PtToggleAvatarClickability(true)
        if gLinkingBook:
            gLinkingBook.hide()


    def IGetAgeFilename(self):
        try:
            name = xLinkingBookDefs.xLinkDestinations[TargetAge.value][0]
        except:
            PtDebugPrint((('IGetAgeFilename(): ' + TargetAge.value) + ' is missing from the xLinkDestinations table, attempting to use it as the value'))
            name = TargetAge.value
        return name


    def IGetAgeInstanceName(self):
        try:
            name = xLinkingBookDefs.xLinkDestinations[TargetAge.value][0]
        except:
            PtDebugPrint((('IGetAgeInstanceName(): ' + TargetAge.value) + ' is missing from the xLinkDestinations table, attempting to use it as the value'))
            name = TargetAge.value
        return name


    def IGetAgeSpawnPoint(self):
        try:
            name = xLinkingBookDefs.xLinkDestinations[TargetAge.value][1]
        except:
            PtDebugPrint((('IGetAgeSpawnPoint(): ' + TargetAge.value) + ' is missing from the xLinkDestinations table, attempting to use an empty string as the value'))
            name = ''
        return name


    def OnTimer(self, id):
        global kGrsnTeamBook
        global gLinkingBook
        if (id == kGrsnTeamBook):
            print '\nahnyLinkBookGUIPopup.OnTimer:Got timer callback. Removing popup for a grsn team book.'
            gLinkingBook.hide()


    def GetCurrentSphere(self):
        vault = ptVault()
        myAges = vault.getAgesIOwnFolder()
        myAges = myAges.getChildNodeRefList()
        for ageInfo in myAges:
            link = ageInfo.getChild()
            link = link.upcastToAgeLinkNode()
            info = link.getAgeInfo()
            if (not (info)):
                continue
            ageName = info.getAgeFilename()
            if (ageName == 'Ahnonay'):
                ahnySDL = info.getAgeSDL()
                ahnyRecord = ahnySDL.getStateDataRecord()
                currentSphere = ahnyRecord.findVar('ahnyCurrentSphere')
                curSphere = currentSphere.getInt(0)
                return curSphere


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



