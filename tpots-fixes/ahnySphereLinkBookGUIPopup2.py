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
zoneObjects = ptAttribSceneobjectList(7, 'main plate objects')
zones = ptAttribActivator(8, 'detector for main plates')
bookZone = ptAttribActivator(9, 'book plate detector')
sphere = ptAttribString(10, 'which sphere is this')
IsDRCStamped = ptAttribBoolean(11, 'DRC Stamp', default=1)
RespClockLights = ptAttribResponderList(12, 'clock lights', statelist=['on', 'off'], byObject=1)
ActTrees = ptAttribActivatorList(13, 'rgn snsr: trees')
ObjTrees = ptAttribSceneobjectList(14, 'objects: trees')
RespTrees = ptAttribResponderList(15, 'resp: trees', byObject=1)
PhysTrees = ptAttribSceneobjectList(16, 'phys: trees')
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
occupiedZones = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
inBookZone = 0
gLinkingBook = None
NoReenableBook = 0
kGrsnTeamBook = 99
PlatesDone = 0
respLightList = []
actTreeList = []
objTreeList = []
respTreeList = []
physTreeList = []
avatarZone = 0
OnInit = 1

class ahnySphereLinkBookGUIPopup2(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 547
        version = 3
        self.version = version
        print '__init__ahnySphereLinkBookGUIPopup2 v ',
        print version


    def OnFirstUpdate(self):
        global respLightList
        global actTreeList
        global objTreeList
        global respTreeList
        global physTreeList
        for light in RespClockLights.value:
            thisLight = light.getName()
            respLightList.append(thisLight)
        print 'respLightList = ',
        print respLightList
        for tree in ActTrees.value:
            thisTree = tree.getName()
            actTreeList.append(thisTree)
        print 'actTreeList = ',
        print actTreeList
        for obj in ObjTrees.value:
            thisObj = obj.getName()
            objTreeList.append(thisObj)
        print 'objTreeList = ',
        print objTreeList
        for resp in RespTrees.value:
            thisResp = resp.getName()
            respTreeList.append(thisResp)
        print 'respTreeList = ',
        print respTreeList
        for phys in PhysTrees.value:
            thisPhys = phys.getName()
            physTreeList.append(thisPhys)
        print 'physTreeList = ',
        print physTreeList


    def OnServerInitComplete(self):
        print 'sphere # ',
        print sphere.value
        PtAtTimeCallback(self.key, 1, 1)


    def OnTimer(self, id):
        global occupiedZones
        global respTreeList
        global OnInit
        if (id == 1):
            print 'On init, occupiedZones =',
            print occupiedZones
            i = 0
            for zone in zoneObjects.value:
                if (occupiedZones[i] == 0):
                    ActTrees.value[i].disable()
                    RespTrees.run(self.key, objectName=respTreeList[i], fastforward=1)
                i += 1
            OnInit = 0


    def EvalLinkingBook(self):
        global occupiedZones
        global inBookZone
        cleared = 1
        i = 0
        for zone in zoneObjects.value:
            zoneName = zone.getName()
            if (occupiedZones[i] == 1):
                print 'something in ',
                print zoneName
                cleared = 0
            else:
                print 'nobody in ',
                print zoneName
            i += 1
        if (not (cleared)):
            return false
        if (inBookZone == 1):
            print 'yes, in book zone'
            return true
        print 'not in book zone'
        return false


    def OnNotify(self, state, id, events):
        global inBookZone
        global respLightList
        global objTreeList
        global respTreeList
        global LocalAvatar
        global OfferedBookMode
        global BookOfferer
        global occupiedZones
        global avatarZone
        global OnInit
        global PlatesDone
        global CurrentPage
        global gLinkingBook
        global ClosedBookToShare
        global NoReenableBook
        ageSDL = PtGetAgeSDL()
        if (id == bookZone.id):
            for event in events:
                if (event[0] != 1):
                    return
                if (event[1] == 1):
                    inBookZone = (inBookZone + 1)
                    print 'yes, now in book zone'
                    if (respLightList != []):
                        RespClockLights.run(self.key, state='on', objectName=respLightList[0])
                else:
                    inBookZone = (inBookZone - 1)
                    print 'no longer in book zone'
                    if (respLightList != []):
                        RespClockLights.run(self.key, state='off', objectName=respLightList[0])
            return
        if ((id == ActTrees.id) and state):
            for event in events:
                if (event[0] == kCollisionEvent):
                    xEvent = event[3]
                    treeName = xEvent.getName()
                    i = 0
                    for obj in objTreeList:
                        if (obj == treeName):
                            treeNum = i
                            break
                        else:
                            i += 1
                    print 'ActTrees: tree =',
                    print (treeNum + 1)
                    ActTrees.value[treeNum].disable()
                    RespTrees.run(self.key, objectName=respTreeList[treeNum])
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
        if (id == SeekBehavior.id):
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
                if (event[0] == kCollisionEvent):
                    if ((id != zones.id) and (id != bookZone.id)):
                        return
                    avatar = PtGetLocalAvatar()
                    region = event[3]
                    regName = region.getName()
                    i = 0
                    for zone in zoneObjects.value:
                        zoneName = zone.getName()
                        if (zoneName == regName):
                            if (event[1] == 1):
                                occupiedZones[i] = 1
                                if (event[2] == avatar):
                                    avatarZone = i
                                    print 'avatar entered: ',
                                    print zoneName
                                else:
                                    print 'tree entered: ',
                                    print zoneName
                                    if (not (OnInit)):
                                        print 'occupiedZones =',
                                        print occupiedZones
                                RespClockLights.run(self.key, state='on', objectName=respLightList[i])
                            else:
                                occupiedZones[i] = 0
                                if (event[2] == avatar):
                                    print 'avatar exited: ',
                                    print zoneName
                                else:
                                    print 'tree exited: ',
                                    print zoneName
                                    if (not (OnInit)):
                                        print 'occupiedZones =',
                                        print occupiedZones
                                RespClockLights.run(self.key, state='off', objectName=respLightList[i])
                        i += 1
                elif (event[0] == PtEventType.kBook):
                    PtDebugPrint(('ahnyLinkBookGUIPopup: BookNotify  event=%d, id=%d' % (event[1], event[2])), level=kDebugDumpLevel)
                    if (event[1] == PtBookEventTypes.kNotifyImageLink):
                        if ((event[2] >= xLinkingBookDefs.kFirstLinkPanelID) or (event[2] == xLinkingBookDefs.kBookMarkID)):
                            PtDebugPrint(('ahnyLinkBookGUIPopup:Book: hit linking panel %s' % event[2]), level=kDebugDumpLevel)
                            self.HideBook(1)
                            if (PlatesDone == 0):
# Ahnonay linking rule work-around BEGIN
                                import xLinkMgr
                                xLinkMgr.LinkToAge("Ahnonay", "LinkInPointDefault")
                                #respLinkResponder.run(self.key, avatar=PtGetLocalAvatar())
# Ahnonay linking rule work-around END
                                return
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
                                spawnPoints = link.getSpawnPoints()
                                if (ageName == 'Ahnonay'):
                                    ahnySDL = info.getAgeSDL()
                                    ahnyRecord = ahnySDL.getStateDataRecord()
                                    currentSphere = ahnyRecord.findVar('ahnyCurrentSphere')
                                    if (sphere.value == '1'):
                                        currentSphere.setInt(2, 0)
                                    elif (sphere.value == '2'):
                                        currentSphere.setInt(3, 0)
                                    elif (sphere.value == '3'):
                                        currentSphere.setInt(1, 0)
                                    elif (sphere.value == '4'):
                                        currentSphere.setInt(1, 0)
                                    else:
                                        print 'missing sphere identifier string!'
                                    ahnySDL.setStateDataRecord(ahnyRecord)
                                    ahnySDL.save()
                                    print 'advanced from sphere ',
                                    print sphere.value
# Ahnonay linking rule work-around BEGIN
                                    import xLinkMgr
                                    xLinkMgr.LinkToAge("Ahnonay", "LinkInPointDefault")
                                    #respLinkResponder.run(self.key, avatar=PtGetLocalAvatar())
# Ahnonay linking rule work-around END
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
        global SpawnPointName_Dict
        global SpawnPointTitle_Dict
        global gLinkingBook
        global PlatesDone
        showOpen = 0
        agePanel = TargetAge.value
        showOpen = 1
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
                if (self.EvalLinkingBook() == false):
                    PlatesDone = 0
                else:
                    PlatesDone = 1
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



