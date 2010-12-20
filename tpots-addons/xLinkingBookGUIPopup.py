# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import string
import xLinkingBookDefs
from xPsnlVaultSDL import *
import time
import xCustomReltoShelf
import os
import xxConfig
actClickableBook = ptAttribActivator(1, 'Actvtr: Clickable small book')
SeekBehavior = ptAttribBehavior(2, 'Smart seek before GUI (optional)')
respLinkResponder = ptAttribResponder(3, 'Rspndr: Link out')
TargetAge = ptAttribString(4, 'Name of Linking Panel', 'Teledahn')
actBookshelf = ptAttribActivator(5, 'Bookshelf (Only used in PsnlAge)')
shareRegion = ptAttribActivator(6, 'region in which the sharer must remain')
shareBookSeek = ptAttribBehavior(7, 'smart seek & use book for share acceptance')
IsDRCStamped = ptAttribBoolean(10, 'DRC Stamp', default=1)
ForceThirdPerson = ptAttribBoolean(11, 'Force 3rd person', default=0)
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
kAhnonayBookshelfBook = 12
kGrsnTeamBook = 99
#Dustin
kOverridePanel1 = 50
kOverridePanel1Time = 0.05
kOverridePanel2 = 51
kOverridePanel2Time = 0.85
#/Dustin
kFirstPersonEnable = 1
kFirstPersonEnableTime = 0.5
TreasureBook = None

class xLinkingBookGUIPopup(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5221
        version = 27
        minor = 4
        self.version = version
        PtDebugPrint(('__init__xLinkingBookGUIPopup v%d.%d' % (version, minor)))


    def OnServerInitComplete(self):
        if actBookshelf:
            ageSDL = PtGetAgeSDL()
            ageSDL.setFlags('CurrentPage', 1, 1)
            ageSDL.sendToClients('CurrentPage')
        # Fix Gahreesen link in Seret
        if TargetAge.value == 'GarrisonNoShare': TargetAge.value = 'Garrison'


    def __del__(self):
        pass


    #Dustin
    def OverrideLinkingImage(self, bookmap):
        import xLinkMgr
        import booksDustGlobal
        if (len(actBookshelf.value) != 0):
            agePanel = stringAgeRequested
            if agePanel in xCustomReltoShelf.availableBooks:
    #/Dustin
                image = xCustomReltoShelf.GetLinkingImage(agePanel, CurrentPage-1, width=410, height=168) # "-1" to compensate for the cover page
                # check if we should show an image
                if image != None:
                    bookmap.textmap.drawImage(50,60,image,0)


    def OnNotify(self, state, id, events):
        global BookOfferer
        global stringAgeRequested
        global ClosedBookToShare
        global OffereeWalking
        global CurrentPage
        global BookNumber
        global OfferedBookMode
        global LocalAvatar
        if (id == shareRegion.id):
            if PtWasLocallyNotified(self.key):
                for event in events:
                    if ((event[0] == kCollisionEvent) and (event[1] == false)):
                        PtDebugPrint('xLinkingBookGUIPopup: exited book offer region', level=kDebugDumpLevel)
                        PtClearOfferBookMode()
                        self.HideBook()
                return
        elif (id == shareBookSeek.id):
            PtDebugPrint('xLinkingBookGUIPopup: notified of share book seek beh', level=kDebugDumpLevel)
            for event in events:
                PtDebugPrint('xLinkingBookGUIPopup: event[0]=', event[0], level=kDebugDumpLevel)
                PtDebugPrint('xLinkingBookGUIPopup: event[1]=', event[1], level=kDebugDumpLevel)
                PtDebugPrint('xLinkingBookGUIPopup: event[2]=', event[2], level=kDebugDumpLevel)
                if ((event[0] == kMultiStageEvent) and ((event[2] == kEnterStage) and OffereeWalking)):
                    OffereeWalking = false
                    PtDebugPrint('xLinkingBookGUIPopup: accepted link, notifying offerer of such', level=kDebugDumpLevel)
                    OfferedBookMode = false
                    avID = PtGetClientIDFromAvatarKey(BookOfferer.getKey())
                    PtNotifyOffererLinkCompleted(avID)
                    BookOfferer = None
                    PtToggleAvatarClickability(true)
                    return
        elif (id == actBookshelf.id):
            if PtWasLocallyNotified(self.key):
                ageSDL = PtGetAgeSDL()
                ShelfABoolOperated = ageSDL['ShelfABoolOperated'][0]
                for event in events:
                    if (event[0] == kVariableEvent):
                        if ((event[1][:8] == 'Volatile') or (event[1][:11] == 'NotVolatile')):
                            return
                        stringAgeRequested = event[1].split(',')[0]
                        try:
                            BookNumber = string.atoi(event[1].split(',')[1])
                            CurrentPage = ageSDL['CurrentPage'][BookNumber]
                            PtDebugPrint(('xLinkingBookGUIPopup: The book was previously bookmarked on page #%d' % CurrentPage), level=kDebugDumpLevel)
                        except:
                            PtDebugPrint('xLinkingBookGUIPopup: Somebody lost my bookmark. Assuming CurrentPage = 1', level=kErrorLevel)
                            CurrentPage = 1
                        idRequestor = event[3]
                        PtDebugPrint(('xLinkingBookGUI.OnNotify():\tpsnlBookshelf user id %d selected book %s from the shelf' % (idRequestor, stringAgeRequested)), level=kDebugDumpLevel)
                        self.IShowBookTreasure()
                        OfferedBookMode = false
                        BookOfferer = None
        elif (id == actClickableBook.id):
            if (PtWasLocallyNotified(self.key) and state):
                actClickableBook.disable()
                PtToggleAvatarClickability(false)
                if ForceThirdPerson.value:
                    cam = ptCamera()
                    cam.undoFirstPerson()
                    cam.disableFirstPersonOverride()
                if (type(SeekBehavior.value) != type(None)):
                    PtDebugPrint('xLinkingBookGUIPopup: Smart seek used', level=kDebugDumpLevel)
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
                        PtDebugPrint('xLinkingBookGUIPopup: attempting to draw link panel gui', level=kDebugDumpLevel)
                        self.IShowBookNoTreasure()
                        OfferedBookMode = false
                        BookOfferer = None
        else:
            for event in events:
                if (event[0] == kOfferLinkingBook):
                    PtDebugPrint('xLinkingBookGUIPopup: got offer book notification', level=kDebugDumpLevel)
                    localAv = PtGetLocalClientID()
                    messageAv = event[3]
                    if (messageAv != localAv):
                        PtDebugPrint('xLinkingBookGUIPopup: offered book message for someone else', level=kDebugDumpLevel)
                        return
                    PtDebugPrint('xLinkingBookGUIPopup: offered book message for me', level=kDebugDumpLevel)
                    if (event[2] == -999):
                        if OffereeWalking:
                            return
                        OfferedBookMode = false
                        BookOfferer = None
                        self.HideBook()
                        return
                    elif (event[2] == 999):
                        OfferedBookMode = true
                        BookOfferer = event[1]
                        PtDebugPrint(('xLinkingBookGUIPopup: offered book by %s' % BookOfferer.getName()), level=kDebugDumpLevel)
                    PtToggleAvatarClickability(false)
                    self.IShowBookNoTreasure()
                    return
                elif (event[0] == PtEventType.kBook):
                    PtDebugPrint(('xLinkingBookGUIPopup: BookNotify  event=%d, id=%d' % (event[1], event[2])), level=kDebugDumpLevel)
                    if (event[1] == PtBookEventTypes.kNotifyImageLink):
                        if (event[2] == xLinkingBookDefs.kShareBookLinkID):
                            PtDebugPrint('xLinkingBookGUIPopup:Book: hit share panel', level=kDebugDumpLevel)
                            PtSetOfferBookMode(self.key, self.IGetAgeFilename(), self.IGetAgeInstanceName())
                            PtSetShareSpawnPoint(self.IGetAgeSpawnPoint())
                            ClosedBookToShare = 1
                            self.HideBook()
                        elif ((event[2] >= xLinkingBookDefs.kFirstLinkPanelID) or (event[2] == xLinkingBookDefs.kBookMarkID)):
                            PtDebugPrint(('xLinkingBookGUIPopup:Book: hit linking panel %s' % event[2]), level=kDebugDumpLevel)
                            if (OfferedBookMode and BookOfferer):
                                self.HideBook()
                                avatar = PtGetLocalAvatar()
                                avatar.avatar.setReplyKey(self.key)
                                shareBookSeek.run(avatar)
                                OffereeWalking = true
                                avID = PtGetClientIDFromAvatarKey(BookOfferer.getKey())
                                PtNotifyOffererLinkAccepted(avID)
                                ClosedBookToShare = 1
                                PtDebugPrint('xLinkingBookGUIPopup: seeking avatar to use book offered', level=kDebugDumpLevel)
                            else:
                                self.HideBook(1)
                                if (len(actBookshelf.value) == 0):
                                    if (len(respLinkResponder.value) == 0):
                                        note = ptNotify(self.key)
                                        note.setActivate(1.0)
                                        note.addVarNumber('LinkOut', 1)
                                        note.send()
                                    else:
# linking rule work-arounds and ages of which the existance has to be checked BEGIN
                                        import xLinkMgr
                                        if TargetAge.value in ['Ahnonay', 'Myst', 'Kveer', 'Neighborhood02', 'Personal02', 'MystMystV', 'AhnonayMOUL']:
                                            xLinkMgr.LinkToAge(TargetAge.value, "LinkInPointDefault")
                                            return
                                        elif TargetAge.value == 'KirelMOUL':
                                            xLinkMgr.LinkToAge(TargetAge.value, "kirelPerf-SpawnPointBevin02")
                                            return
                                        elif TargetAge.value == 'nb01BevinBalcony01':
                                            xLinkMgr.LinkToAge("Neighborhood", "LinkInPointBevinBalcony01")
                                            return
                                        elif TargetAge.value == 'Garrison' and PtGetAgeName() == 'NeighborhoodMOUL':
                                            xLinkMgr.LinkToAge(TargetAge.value, "LinkInPointDefault")
                                            return
# linking rule work-arounds and ages of which the existance has to be checked END
                                        respLinkResponder.run(self.key, avatar=PtGetLocalAvatar())
                                else:
                                    PtDebugPrint(('xLinkingBookGUIPopup: Placing a bookmark for book #%d on page %d' % (BookNumber, CurrentPage)), level=kDebugDumpLevel)
                                    ageSDL = PtGetAgeSDL()
                                    ageSDL.setIndex('CurrentPage', BookNumber, CurrentPage)
                                    if (BookNumber == kAhnonayBookshelfBook):
                                        curSphere = 1
                                        vault = ptVault()
                                        myAges = vault.getAgesIOwnFolder()
                                        myAges = myAges.getChildNodeRefList()
                                        for ageInfo in myAges:
                                            link = ageInfo.getChild()
                                            link = link.upcastToAgeLinkNode()
                                            info = link.getAgeInfo()
                                            if (not info):
                                                continue
                                            ageName = info.getAgeFilename()
                                            spawnPoints = link.getSpawnPoints()
                                            if (ageName == 'Ahnonay'):
                                                ahnySDL = info.getAgeSDL()
                                                ahnyRecord = ahnySDL.getStateDataRecord()
                                                currentSphere = ahnyRecord.findVar('ahnyCurrentSphere')
                                                currentCloth = ahnyRecord.findVar('ahnyCurrentSaveCloth')
                                                curSphere = currentSphere.getInt(0)
                                                clothNumber = currentCloth.getInt(0)
                                                saveSphere = currentCloth.getInt(1)
                                                break
                                        if (event[2] == xLinkingBookDefs.kBookMarkID):
                                            print 'going to a link point!'
                                            print 'curSphere ',
                                            print curSphere,
                                            print ' saveSphere ',
                                            print saveSphere
                                            if (clothNumber < 25):
                                                pos = (curSphere + saveSphere)
                                                if (pos > 4):
                                                    pos = (pos % 4)
                                                newCloth = (((pos - 1) * 6) + clothNumber)
                                                if (newCloth < 0):
                                                    newCloth = (24 - newCloth)
                                            else:
                                                newCloth = clothNumber
                                            avatar = PtGetLocalAvatar()
                                            myID = PtGetClientIDFromAvatarKey(avatar.getKey())
                                            note = ptNotify(self.key)
                                            note.setActivate(1.0)
                                            note.addVarNumber((((((('ILink' + ',') + 'SaveClothPoint') + str(newCloth)) + ',') + 'SaveClothPoint') + str(newCloth)), myID)
                                            note.send()
                                            return
                                        else:
                                            avatar = PtGetLocalAvatar()
                                            myID = PtGetClientIDFromAvatarKey(avatar.getKey())
                                            note = ptNotify(self.key)
                                            note.setActivate(1.0)
                                            note.addVarNumber(((((('ILink' + ',') + 'AhnySphere0') + str(curSphere)) + ',') + 'Default'), myID)
                                            note.send()
                                            return
                                    linkTitle = SpawnPointTitle_Dict[event[2]]
                                    if ((linkTitle == 'Tomahna') or (linkTitle == 'Cleft')):
                                        vault = ptVault()
                                        entry = vault.findChronicleEntry('TomahnaLoad')
                                        if (type(entry) != type(None)):
                                            if (linkTitle == 'Tomahna'):
                                                entry.chronicleSetValue('yes')
                                            else:
                                                entry.chronicleSetValue('no')
                                    avatar = PtGetLocalAvatar()
                                    myID = PtGetClientIDFromAvatarKey(avatar.getKey())
                                    note = ptNotify(self.key)
                                    note.setActivate(1.0)
                                    note.addVarNumber((((('ILink' + ',') + SpawnPointName_Dict[event[2]]) + ',') + SpawnPointTitle_Dict[event[2]]), myID)
                                    note.send()
                    elif (event[1] == PtBookEventTypes.kNotifyShow):
                        PtDebugPrint('xLinkingBookGUIPopup:Book: NotifyShow', level=kDebugDumpLevel)
                        if (CurrentPage > 1):
                            PtDebugPrint(('xLinkingBookGUIPopup: going to page %d (ptBook page %d)' % (CurrentPage, ((CurrentPage - 1) * 2))), level=kDebugDumpLevel)
                            gLinkingBook.goToPage(((CurrentPage - 1) * 2))
                        #Dustin
                        import booksDustGlobal
                        self.OverrideLinkingImage(booksDustGlobal.BookMapRight)
                        #/Dustin
                    elif (event[1] == PtBookEventTypes.kNotifyHide):
                        PtDebugPrint('xLinkingBookGUIPopup:Book: NotifyHide', level=kDebugDumpLevel)
                        if not TreasureBook:
                            PtSendKIMessage(kEnableKIandBB, 0)
                        if (not (ClosedBookToShare)):
                            PtToggleAvatarClickability(true)
                            if (OfferedBookMode and BookOfferer):
                                avID = PtGetClientIDFromAvatarKey(BookOfferer.getKey())
                                PtNotifyOffererLinkRejected(avID)
                                PtDebugPrint('xLinkingBookGUIPopup: rejected link, notifying offerer as such', level=kDebugDumpLevel)
                                OfferedBookMode = false
                                BookOfferer = None
                        if ForceThirdPerson.value:
                            PtAtTimeCallback(self.key, kFirstPersonEnableTime, kFirstPersonEnable)
                        if (not NoReenableBook):
                            actClickableBook.enable()
                        ClosedBookToShare = 0
                        if (len(actBookshelf.value) != 0):
                            PtDebugPrint('xLinkingBookGUIPopup: Roll back the personal age book.', level=kDebugDumpLevel)
                            note = ptNotify(self.key)
                            note.setActivate(1.0)
                            note.addVarNumber('IShelveBook', 1)
                            note.send()
                            PtDebugPrint(('xLinkingBookGUIPopup: Placing a bookmark for book #%d on page %d' % (BookNumber, CurrentPage)), level=kDebugDumpLevel)
                            ageSDL = PtGetAgeSDL()
                            ageSDL.setIndex('CurrentPage', BookNumber, CurrentPage)
                    elif (event[1] == PtBookEventTypes.kNotifyNextPage):
                        PtDebugPrint(('xLinkingBookGUIPopup:Book: NotifyNextPage  new current page=%d' % (CurrentPage + 1)), level=kDebugDumpLevel)
                        CurrentPage += 1
                        #Dustin
                        PtAtTimeCallback(self.key, kOverridePanel1Time, kOverridePanel1)
                        #/Dustin
                    elif (event[1] == PtBookEventTypes.kNotifyPreviousPage):
                        PtDebugPrint(('xLinkingBookGUIPopup:Book: NotifyPreviousPage new current page=%d' % (CurrentPage - 1)), level=kDebugDumpLevel)
                        CurrentPage -= 1
                        #Dustin
                        import booksDustGlobal
                        self.OverrideLinkingImage(booksDustGlobal.BookMapFront)
                        #/Dustin
                    elif (event[1] == PtBookEventTypes.kNotifyCheckUnchecked):
                        PtDebugPrint('xLinkingBookGUIPopup:Book: NotifyCheckUncheck', level=kDebugDumpLevel)



    def IShowBookNoTreasure(self):
        global gLinkingBook, TreasureBook
        TreasureBook = False
        showOpen = 0
        if (len(actBookshelf.value) == 0):
            agePanel = TargetAge.value
            showOpen = 1
        else:
            agePanel = stringAgeRequested
            showOpen = 0
        if agePanel:
            if (agePanel == 'TomahnaFromCleft'):
                vault = ptVault()
                entry = vault.findChronicleEntry('TomahnaLoad')
                sdl = xPsnlVaultSDL()
                if (type(entry) != type(None)):
                    if (not sdl['CleftVisited'][0]):
                        sdl['CleftVisited'] = (1,)
                        PtDebugPrint('Wrong SDL setting for CleftVisited, restoring to true')
                    entry.chronicleSetValue('yes')
                    entry.save()
                    PtDebugPrint('Chronicle entry TomahnaLoad already added, setting to yes')
                else:
                    sdl['CleftVisited'] = (1,)
                    vault.addChronicleEntry('TomahnaLoad', 1, 'yes')
                    PtDebugPrint('Chronicle entry TomahnaLoad not present, adding entry and setting to yes')
                respLinkResponder.run(self.key, avatar=PtGetLocalAvatar())
                return
            elif ((agePanel == 'grsnTeamRmPurple') or (agePanel == 'grsnTeamRmYellow')):
                PtAtTimeCallback(self.key, 5, kGrsnTeamBook)
            elif (agePanel == 'MystMystV' and os.path.exists('avi/mystWithAlpha.bik')):
                agePanel = 'MystMystVVideo'
            try:
                params = xLinkingBookDefs.xAgeLinkingBooks[agePanel]
                if (len(params) == 6):
                    (sharable, width, height, stampdef, bookdef, gui) = params
                elif (len(params) == 5):
                    (sharable, width, height, stampdef, bookdef) = params
                    gui = 'BkBook'
                else:
                    linkingPanel = params
                    self.IShowBahroBook(linkingPanel)
                    return
                if (not IsDRCStamped.value):
                    stampdef = xLinkingBookDefs.NoDRCStamp
                if sharable:
                    try:
                        bookdef = (bookdef % ('', stampdef, self.IAddShare()))
                    except:
                        PtDebugPrint(('xLinkingBookGUIPopup: %s\'s book definition can\'t be shared' % agePanel), level=kErrorLevel)
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
                PtDebugPrint(('xLinkingBookGUIPopup: could not find age %s\'s linking panel' % agePanel), level=kErrorLevel)
        else:
            PtDebugPrint(('xLinkingBookGUIPopup: no age link panel' % agePanel), level=kErrorLevel)


    def IShowBookTreasure(self):
        global SpawnPointName_Dict
        global gLinkingBook, TreasureBook
        global SpawnPointTitle_Dict
        TreasureBook = True
        showOpen = 0
        if (len(actBookshelf.value) == 0):
            agePanel = TargetAge.value
            showOpen = 1
            fromBookshelf = 0
        else:
            agePanel = stringAgeRequested
            fromBookshelf = 1
            showOpen = 0
            if (CurrentPage > 1):
                showOpen = 1
        if agePanel:
            if (agePanel == 'Cleft'):
                vault = ptVault()
                entry = vault.findChronicleEntry('TomahnaLoad')
                if (type(entry) != type(None)):
                    agePanel = 'CleftWithTomahna'
            if (agePanel == 'CleftWithTomahna'):
                print 'setting up cleft and tomahna spawn points'
                SpawnPointTitle_Dict = {
                    xLinkingBookDefs.kFirstLinkPanelID: 'Tomahna',
                    (xLinkingBookDefs.kFirstLinkPanelID + 1): 'Cleft'
                }
                SpawnPointName_Dict = {
                    xLinkingBookDefs.kFirstLinkPanelID: 'SpawnPointTomahna01',
                    (xLinkingBookDefs.kFirstLinkPanelID + 1): 'LinkInPointDefault'
                }
            elif (agePanel == 'city'):
                self.BuildCityBook()
                agePanel = SpawnPointTitle_Dict[xLinkingBookDefs.kFirstLinkPanelID]
            elif (agePanel == 'Pods'):
                self.BuildPodBook()
                agePanel = SpawnPointTitle_Dict[xLinkingBookDefs.kFirstLinkPanelID]
            elif (agePanel == 'Direbo'):
                SpawnPointTitle_Dict = {}
                SpawnPointName_Dict = {}
                if os.path.exists('avi/direboWithAlpha.bik'):
                    SpawnPointTitle_Dict[xLinkingBookDefs.kFirstLinkPanelID] = agePanel = 'DireboVideo'
                else:
                    SpawnPointTitle_Dict[xLinkingBookDefs.kFirstLinkPanelID] = agePanel = 'Direbo'
                SpawnPointName_Dict[xLinkingBookDefs.kFirstLinkPanelID] = 'LinkInPoint1'
            elif (agePanel == 'Neighborhood'):
                agevault = ptAgeVault()
                nblink = self.GetOwnedAgeLink(agevault, 'Neighborhood')
                if (not nblink):
                    SpawnPointTitle_Dict = {
                        xLinkingBookDefs.kFirstLinkPanelID: 'Default'
                    }
                    SpawnPointName_Dict = {
                        xLinkingBookDefs.kFirstLinkPanelID: 'LinkInPointDefault'
                    }
                else:
                    self.BuildTreasureLinks(agePanel)
            elif (agePanel in xCustomReltoShelf.availableBooks):
                (SpawnPointTitle_Dict, SpawnPointName_Dict) = xCustomReltoShelf.BuildBook(agePanel)
                agePanel = SpawnPointTitle_Dict[xLinkingBookDefs.kFirstLinkPanelID]
            else:
                print 'setting up treasure spawn points'
                self.BuildTreasureLinks(agePanel)
            #print SpawnPointTitle_Dict
            #print SpawnPointName_Dict
            try:
                params = xLinkingBookDefs.xAgeLinkingBooks[agePanel]
                if (len(params) == 6):
                    (sharable, width, height, stampdef, bookdef, gui) = params
                elif (len(params) == 5):
                    (sharable, width, height, stampdef, bookdef) = params
                    gui = 'BkBook'
                elif (not fromBookshelf):
                    linkingPanel = params
                    self.IShowBahroBook(linkingPanel)
                    return
                else:
                    (sharable, width, height, stampdef, gui) = (0, 1.0, 1.0, xLinkingBookDefs.NoDRCStamp, 'BkBook')
                    bookdef = (((((xLinkingBookDefs.BookStart1 + xLinkingBookDefs.DRCStampHolder) + xLinkingBookDefs.NoShare) + xLinkingBookDefs.LinkStart) + params) + xLinkingBookDefs.LinkEnd)
                if ('NotPossible' in SpawnPointTitle_Dict.values()):
                    bookdef = (((((xLinkingBookDefs.BookStart1 + xLinkingBookDefs.DRCStampHolder) + xLinkingBookDefs.NoShare) + xLinkingBookDefs.LinkStart) + 'xLinkPanelBlackVoid') + xLinkingBookDefs.LinkEndNoLink)
                    sharable = 0
                if (not IsDRCStamped.value):
                    stampdef = xLinkingBookDefs.NoDRCStamp
            except LookupError:
                PtDebugPrint(("xLinkingBookGUIPopup: could not find age %s's linking panel or SpawnPoint" % agePanel), level=kErrorLevel)
                return
            if (agePanel == 'AhnySphere01'):
                vault = ptVault()
                myAges = vault.getAgesIOwnFolder()
                myAges = myAges.getChildNodeRefList()
                for ageInfo in myAges:
                    link = ageInfo.getChild()
                    link = link.upcastToAgeLinkNode()
                    info = link.getAgeInfo()
                    if (not info):
                        continue
                    ageName = info.getAgeFilename()
                    spawnPoints = link.getSpawnPoints()
                    if (ageName == 'Ahnonay'):
                        ahnySDL = info.getAgeSDL()
                        ahnyRecord = ahnySDL.getStateDataRecord()
                        currentCloth = ahnyRecord.findVar('ahnyCurrentSaveCloth')
                        if (currentCloth.getInt(0) == 0):
                            bookmark = ''
                        else:
                            bookmark = xLinkingBookDefs.SCBookMark
                        break
            elif (fromBookshelf and (xLinkingBookDefs.kBookMarkID in SpawnPointTitle_Dict.keys())):
                if (SpawnPointTitle_Dict[xLinkingBookDefs.kBookMarkID] == 'JCSavePoint'):
                    bookmark = xLinkingBookDefs.JCBookMark
                elif (SpawnPointTitle_Dict[xLinkingBookDefs.kBookMarkID] == 'SCSavePoint'):
                    bookmark = xLinkingBookDefs.SCBookMark
                else:
                    bookmark = ''
                    PtDebugPrint('xLinkingBookGUIPopup: sorry, don\'t recognize your bookmark spawn point title')
            else:
                bookmark = ''
            if sharable:
                try:
                    allPagesDef = (bookdef % (bookmark, stampdef, self.IAddShare()))
                except:
                    PtDebugPrint(('xLinkingBookGUIPopup: %s\'s book definition can\'t be shared' % agePanel), level=kErrorLevel)
            elif (agePanel == 'CleftWithTomahna'):
                allPagesDef = (bookdef % (bookmark, stampdef, xLinkingBookDefs.kFirstLinkPanelID, (xLinkingBookDefs.kFirstLinkPanelID + 1)))
            else:
                allPagesDef = (bookdef % (bookmark, stampdef))
            if (agePanel != 'CleftWithTomahna'):
                sortedKeys = SpawnPointTitle_Dict.keys()
                sortedKeys.sort()
                for linkID in sortedKeys:
                    if ((linkID == xLinkingBookDefs.kFirstLinkPanelID) or (linkID == xLinkingBookDefs.kBookMarkID)):
                        continue
                    try:
                        pagedef = xLinkingBookDefs.xLinkingPages[SpawnPointTitle_Dict[linkID]]
                        try:
                            allPagesDef += (pagedef % linkID)
                        except:
                            PtDebugPrint(('xLinkingBookGUIPopup: Treasure page %s\'s book definition doesn\'t look like a page???' % SpawnPointTitle_Dict[linkID]), level=kErrorLevel)
                    except LookupError:
                        PtDebugPrint(('xLinkingBookGUIPopup: could not find treasure book page %s\'s linking panel' % SpawnPointTitle_Dict[linkID]), level=kErrorLevel)
            if (allPagesDef != ''):
                print "xLinkingBookGUIPopup full book source: "+allPagesDef
                PtSendKIMessage(kDisableKIandBB, 0)
                gLinkingBook = ptBook(allPagesDef, self.key)
                gLinkingBook.setSize(width, height)
                if (not showOpen):
                    if (not self.IsThereACover(allPagesDef)):
                        showOpen = 1
                gLinkingBook.setGUI(gui)
                vault = ptVault()
                if vault.amOwnerOfCurrentAge():
                    gLinkingBook.allowPageTurning(1)
                else:
                    gLinkingBook.allowPageTurning(0)
                gLinkingBook.show(showOpen)
            else:
                PtDebugPrint(("xLinkingBookGUIPopup: couldn't find the book definition for %s???" % agePanel), level=kErrorLevel)
        else:
            PtDebugPrint(('xLinkingBookGUIPopup: no age link panel' % agePanel), level=kErrorLevel)


    def BuildCityBook(self):
        global SpawnPointName_Dict
        global SpawnPointTitle_Dict
        SpawnPointTitle_Dict = {}
        SpawnPointName_Dict = {}
        vault = ptAgeVault()
        OwnedAges = vault.getAgesIOwnFolder().getChildNodeRefList()
        spawnPoints = []
        for NodeRef in OwnedAges:
            tmpLink = NodeRef.getChild().upcastToAgeLinkNode()
            if tmpLink:
                linkAge = tmpLink.getAgeInfo().getAgeFilename()
                if ((linkAge == 'city') or ((linkAge == 'Descent') or ((linkAge == 'spyroom') or (linkAge == 'Kveer') or (linkAge == 'KveerMOUL') or (linkAge == 'DescentMystV')))):
                    spawnPoints.extend(tmpLink.getSpawnPoints())
                elif (linkAge == 'GreatZero'):
                    sps = tmpLink.getSpawnPoints()
                    for sp in sps:
                        if (sp.getTitle() == 'grtzGrtZeroLinkRm'):
                            spawnPoints.append(sp)
                            break
                elif (linkAge == 'BaronCityOffice'):
                    bcosp = ptSpawnPointInfo('BaronCityOffice', 'LinkInPointDefault')
                    spawnPoints.append(bcosp)
        x = xLinkingBookDefs.kFirstLinkPanelID
        for sp in spawnPoints:
            if (sp.getTitle() in xLinkingBookDefs.CityBookLinks):
                SpawnPointTitle_Dict[x] = sp.getTitle()
                SpawnPointName_Dict[x] = sp.getName()
                x += 1


    def BuildPodBook(self):
        global SpawnPointName_Dict
        global SpawnPointTitle_Dict
        SpawnPointTitle_Dict = {}
        SpawnPointName_Dict = {}
        vault = ptAgeVault()
        OwnedAges = vault.getAgesIOwnFolder().getChildNodeRefList()
        x = xLinkingBookDefs.kFirstLinkPanelID
        for NodeRef in OwnedAges:
            tmpLink = NodeRef.getChild().upcastToAgeLinkNode()
            if tmpLink:
                linkAge = tmpLink.getAgeInfo().getAgeFilename()
                if (linkAge in xLinkingBookDefs.PodAges.keys()):
                    for sp in tmpLink.getSpawnPoints():
                        if sp.getTitle() in xLinkingBookDefs.PodAges[linkAge]:
                            SpawnPointTitle_Dict[x] = linkAge
                            SpawnPointName_Dict[x] = sp.getName()
                            x += 1
                            break


    def IShowBahroBook(self, linkingPanel):
        global gLinkingBook
        PtDebugPrint('xLinkingBookGUIPopup: It\'s a Bahro Linking Tablet (BLT), so we get to do fun stuff now!')
        agePanel = TargetAge.value
        # HACK most of the stones in POTS don't actually support sharing
        shareStoneWhitelist = ['xLinkPanelGarrisonPrison', 'xLinkPanelTeledahnChopShroom', 'xLinkPanelTeledahnDock']
        if (xxConfig.isOffline() or OfferedBookMode or not (linkingPanel in shareStoneWhitelist)):
            bookdef = ((((('<font size=10>' + xLinkingBookDefs.BahroNoShare) + '<pb>') + xLinkingBookDefs.TransLinkStart) + linkingPanel) + xLinkingBookDefs.LinkEnd)
        else:
            bookdef = ((((('<font size=10>' + xLinkingBookDefs.BahroShare) + '<pb>') + xLinkingBookDefs.TransLinkStart) + linkingPanel) + xLinkingBookDefs.LinkEnd)
        SpawnPointName_Dict[0] = 'LinkInPointDefault'
        SpawnPointTitle_Dict[0] = agePanel
        PtSendKIMessage(kDisableKIandBB, 0)
        gLinkingBook = ptBook(bookdef, self.key)
        gLinkingBook.setSize(1, 1)
        gLinkingBook.setGUI('bkBahroRockBook')
        gLinkingBook.show(1)


    def IAddShare(self):
        if (len(actBookshelf.value) == 0):
            if (not OfferedBookMode) and xxConfig.isOnline():
                return xLinkingBookDefs.ShareBook
        return ''


    def IsThereACover(self, bookHtml):
        idx = bookHtml.find('<cover')
        if (idx > 0):
            return 1
        return 0


    def BuildTreasureLinks(self, ageRequested):
        global SpawnPointTitle_Dict
        global SpawnPointName_Dict
        vault = ptAgeVault()
        OwnedAges = vault.getAgesIOwnFolder().getChildNodeRefList()
        spawnPoints = None
        for NodeRef in OwnedAges:
            tmpLink = NodeRef.getChild().upcastToAgeLinkNode()
            if tmpLink:
                if (type(tmpLink.getAgeInfo()) != type(None)):
                    if (ageRequested == tmpLink.getAgeInfo().getAgeFilename()):
                        spawnPoints = tmpLink.getSpawnPoints()
                        break
        SpawnPointName_Dict = {}
        SpawnPointTitle_Dict = {}
        PtDebugPrint(('xLinkingBookGUI.BuildTreasureLinks():The %s book has the following %s pages: ' % (ageRequested, len(spawnPoints))), level=kDebugDumpLevel)
        HasFoundOriginalBook = false
        for spawnPoint in spawnPoints:
            if (spawnPoint.getTitle() == 'Default'):
                HasFoundOriginalBook = true
                PtDebugPrint(("\tPage #1: You've found the original book. The first panel shows %s" % ageRequested), level=kDebugDumpLevel)
                SpawnPointName_Dict[xLinkingBookDefs.kFirstLinkPanelID] = 'LinkInPointDefault'
                SpawnPointTitle_Dict[xLinkingBookDefs.kFirstLinkPanelID] = 'Default'
            elif ((spawnPoint.getTitle() == 'JCSavePoint') or (spawnPoint.getTitle() == 'SCSavePoint')):
                if (len(actBookshelf.value) > 0):
                    SpawnPointTitle_Dict[xLinkingBookDefs.kBookMarkID] = spawnPoint.getTitle()
                    SpawnPointName_Dict[xLinkingBookDefs.kBookMarkID] = spawnPoint.getName()
            else:
                if HasFoundOriginalBook:
                    page = (len(SpawnPointTitle_Dict) + xLinkingBookDefs.kFirstLinkPanelID)
                else:
                    page = ((len(SpawnPointTitle_Dict) + xLinkingBookDefs.kFirstLinkPanelID) + 1)
                PtDebugPrint(('\tPage #%s: spawnpoint: %s, LinkPanel/Title: %s' % (page, spawnPoint.getName(), spawnPoint.getTitle())))
                SpawnPointName_Dict[page] = spawnPoint.getName()
                SpawnPointTitle_Dict[page] = spawnPoint.getTitle()
        if (not HasFoundOriginalBook):
            if (ageRequested == 'Neighborhood'):
                PtDebugPrint(("\tPage #1: You didn't find the original book, but you're looking at the neighborhood. The first panel shows %s" % ageRequested), level=kDebugDumpLevel)
                SpawnPointName_Dict[xLinkingBookDefs.kFirstLinkPanelID] = 'LinkInPointDefault'
                SpawnPointTitle_Dict[xLinkingBookDefs.kFirstLinkPanelID] = 'Default'
            else:
                PtDebugPrint("\tPage #1: You haven't found the original book. The first panel shows black.", level=kDebugDumpLevel)
                SpawnPointName_Dict[xLinkingBookDefs.kFirstLinkPanelID] = 'NotPossible'
                SpawnPointTitle_Dict[xLinkingBookDefs.kFirstLinkPanelID] = 'NotPossible'


    def HideBook(self, islinking = 0):
        global NoReenableBook
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
        if (id == kGrsnTeamBook):
            print '\nxLinkingBookGUIPopup.OnTimer:Got timer callback. Removing popup for a grsn team book.'
            gLinkingBook.hide()
        elif (id == kFirstPersonEnable):
            cam = ptCamera()
            cam.enableFirstPersonOverride()
        #Dustin
        elif (id == kOverridePanel1):
            import booksDustGlobal
            self.OverrideLinkingImage(booksDustGlobal.BookMapRight)
            PtAtTimeCallback(self.key, kOverridePanel2Time, kOverridePanel2)
        elif (id == kOverridePanel2):
            import booksDustGlobal
            self.OverrideLinkingImage(booksDustGlobal.BookMapRight)
        #/Dustin


    def GetOwnedAgeLink(self, vault, age):
        PAL = vault.getAgesIOwnFolder()
        if (type(PAL) != type(None)):
            contents = PAL.getChildNodeRefList()
            for content in contents:
                link = content.getChild().upcastToAgeLinkNode()
                info = link.getAgeInfo()
                if (not info):
                    continue
                ageName = info.getAgeFilename()
                if (ageName == age):
                    return link
        return None


    def OnBackdoorMsg(self, target, param):
        global kFirstPersonEnableTime
        if (target == 'time'):
            kFirstPersonEnableTime = float(param)


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



