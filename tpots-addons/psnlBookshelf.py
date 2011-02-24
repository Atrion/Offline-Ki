# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    This is a patched file that was originally written by Cyan Worlds Inc.    #
#    See the file AUTHORS for more info about the contributors of the changes  #
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
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
import PlasmaControlKeys
import xLinkingBookDefs
import xLocalization
from xPsnlVaultSDL import *
import xCustomReltoShelf
import xxConfig
actBookshelf = ptAttribActivator(3, 'Actvtr:Bookshelf')
actBook = ptAttribActivator(4, 'Actvtr:Book', byObject=1)
respPresentBook = ptAttribResponder(5, 'Rspndr:PresentBook', byObject=1)
respShelveBook = ptAttribResponder(6, 'Rspndr:ShelveBook', byObject=1)
objLibrary = ptAttribSceneobjectList(7, 'Objct:Books')
objTrays = ptAttribSceneobjectList(8, 'Objct:Trays')
respDeleteBook = ptAttribResponder(9, 'Rspndr:DeleteBook', byObject=1)
respReturnTray = ptAttribResponder(10, 'Rspndr:ReturnTray', byObject=1)
actTray = ptAttribActivator(11, 'Actvtr:Tray', byObject=1)
objLocks = ptAttribSceneobjectList(12, 'Objct:Locks')
respOpenLock = ptAttribResponder(13, 'Rspndr:OpenLock', byObject=1)
respCloseLock = ptAttribResponder(14, 'Rspndr:CloseLock', byObject=1)
actLock = ptAttribActivator(15, 'Actvtr:Lock', byObject=1)
animLockOpen = ptAttribAnimation(16, 'open clasp anim', byObject=1)
animLockClose = ptAttribAnimation(17, 'close clasp anim', byObject=1)
SeekBehavior = ptAttribBehavior(18, 'Smart seek before GUI')
ShelfCamera = ptAttribSceneobject(19, 'Bookshelf camera')
respRaiseShelfClickable = ptAttribResponder(20, 'Rspndr:Raise Clickable (LocalOnly)')
respLowerShelfClickable = ptAttribResponder(21, 'Rspndr:Lower Clickable')
actDisengageShelf = ptAttribActivator(22, 'Actvtr: Disengage Shelf')
HutCamera = ptAttribSceneobject(23, 'Hut circle camera')
actLinkingBookGUIPopup = ptAttribNamedActivator(24, 'Actvr: LinkingBook GUI')
actBookshelfExit = ptAttribActivator(25, 'Actvr: Exit bookshelf')
linkLibrary = [
    # First Row
    'Cleft',
    'Garrison',
    'Teledahn',
    'Kadish',
    'Gira',
    'Garden',
    'city',
    'Neighborhood',
    'Nexus',
    'RestorationGuild',
    'Ercana',
    'Ahnonay',
    'AhnySphere01',
    'Myst',
    'Minkata',
    'Jalak',
    'Pods',
    'Direbo',
    # Second Row
    'Link19',
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
    'Link36'
]
objBookPicked = None
objLockPicked = None
boolLinkerIsMe = false
boolPresentAfterLockOpen = false
boolShelfBusy = false
SpawnPointName = None
SpawnPointTitle = None
LocalAvatar = None
ShelfAUserID = -1
ShelfABoolOperated = 0
AgeStartedIn = None
NBBookLocked = 1
CityBookAges = {
    'BaronCityOffice': ['BaronCityOffice', 'Default'],
    'Descent': ['dsntShaftFall'],
    'GreatZero': ['grtzGrtZeroLinkRm'],
    'spyroom': ['Spyroom'],
    'Kveer': ['kverKveer'],
    'DescentMystV': ['dsntMystV'],
    'KveerMOUL' : ['KveerMOUL']
}
sphere01Cloths = ['SaveClothPoint1', 'SaveClothPoint2', 'SaveClothPoint3', 'SaveClothPoint4', 'SaveClothPoint5', 'SaveClothPoint6']
sphere02Cloths = ['SaveClothPoint7', 'SaveClothPoint8', 'SaveClothPoint9', 'SaveClothPoint10', 'SaveClothPoint11', 'SaveClothPoint12']
sphere03Cloths = ['SaveClothPoint13', 'SaveClothPoint14', 'SaveClothPoint15', 'SaveClothPoint16', 'SaveClothPoint17', 'SaveClothPoint18']
sphere04Cloths = ['SaveClothPoint19', 'SaveClothPoint20', 'SaveClothPoint21', 'SaveClothPoint22', 'SaveClothPoint23', 'SaveClothPoint24', 'SaveClothPoint25', 'SaveClothPoint26', 'SaveClothPoint27']

class psnlBookshelf(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5012
        version = 10
        self.version = version
        self.initComplete = 0
        print '__init__psnlBookshelf v.',
        print version
        import xLinkMgr
        xLinkMgr.ResetAvailableLinks()
        xCustomReltoShelf.ParseULMFile()


    def OnServerInitComplete(self):
        ageSDL = PtGetAgeSDL()
        ageSDL.setNotify(self.key, 'ShelfAUserID', 0.0)
        ageSDL.setFlags('ShelfABoolOperated', 1, 1)
        ageSDL.setFlags('ShelfAUserID', 1, 1)
        ageSDL.sendToClients('ShelfABoolOperated')
        ageSDL.sendToClients('ShelfAUserID')
        ageSDL.setFlags('CurrentPage', 1, 1)
        ageSDL.sendToClients('CurrentPage')
        solo = true
        if len(PtGetPlayerList()):
            solo = false
        self.IUpdateLinks()
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            ShelfABoolOperated = ageSDL['ShelfABoolOperated'][0]
            if ((not (solo)) and ShelfABoolOperated):
                actBookshelf.disable()
                print ('psnlBookshelf.Load():\tShelfABoolOperated=%d, disabling shelf clickable' % ShelfABoolOperated)
            else:
                print ('psnlBookshelf.Load():\tShelfABoolOperated=%d but no one else here...correcting' % ShelfABoolOperated)
                self.IResetShelf()
        self.initComplete = 1


    def OnFirstUpdate(self):
        global AgeStartedIn
        global boolShelfBusy
        self.initComplete = 0
        self.UsingBook = 0
        AgeStartedIn = PtGetAgeName()
        for tray in objTrays.value:
            tray.draw.disable()
        for book in objLibrary.value:
            book.draw.disable()
        boolShelfBusy = false
        self.IUpdateLocksAndTrays()
        vault = ptVault()
        if (not (vault.inMyPersonalAge())):
            actLock.disable()
            actTray.disable()
        return


    def AvatarPage(self, avObj, pageIn, lastOut):
        if pageIn:
            return
        avID = PtGetClientIDFromAvatarKey(avObj.getKey())
        if (AgeStartedIn == PtGetAgeName()):
            try:
                ageSDL = PtGetAgeSDL()
                if (avID == ageSDL['ShelfAUserID'][0]):
                    print 'psnlBookshelf.AvatarPage(): Bookshelf A operator paged out, reenabled Bookshelf.'
                    self.IResetShelf()
                else:
                    return
            except:
                pass


    def OnAgeVaultEvent(self, event, tupdata):
        PtDebugPrint(('psnlBookshelf.OnAgeVaultEvent()\t:OnAgeKIEvent recvd. Event=%d and data= ' % event), tupdata)
        if (event == PtVaultCallbackTypes.kVaultConnected):
            print 'psnlBookshelf: kVaultConnected event'
        elif (event == PtVaultCallbackTypes.kVaultNodeSaved):
            print ('psnlBookshelf.OnAgeVaultEvent()\t: kVaultNodeSaved event (id=%d,type=%d)' % (tupdata[0].getID(), tupdata[0].getType()))
        elif (event == PtVaultCallbackTypes.kVaultNodeRefAdded):
            print ('psnlBookshelf.OnAgeVaultEvent()\t: kVaultNodeRefAdded event (childID=%d,parentID=%d)' % (tupdata[0].getChildID(), tupdata[0].getParentID()))
            if self.initComplete:
                self.IUpdateLinks()
                self.IUpdateLocksAndTrays()
        elif (event == PtVaultCallbackTypes.kVaultRemovingNodeRef):
            print ('psnlBookshelf.OnAgeVaultEvent()\t: kVaultRemovingNodeRef event (childID=%d,parentID=%d)' % (tupdata[0].getChildID(), tupdata[0].getParentID()))
        elif (event == PtVaultCallbackTypes.kVaultNodeRefRemoved):
            print 'psnlBookshelf.OnAgeVaultEvent()\t: kVaultNodeRefRemoved event (childID,parentID) ',
            print tupdata
        elif (event == PtVaultCallbackTypes.kVaultNodeInitialized):
            print 'psnlBookshelf.OnAgeVaultEvent()\t: kVaultNodeInitialized event (id=%d,type=%d)',
            print (tupdata[0].getID(), tupdata[0].getType())
        elif (event == PtVaultCallbackTypes.kVaultOperationFailed):
            print 'psnlBookshelf.OnAgeVaultEvent()\t: kVaultOperationFailed event  (operation,resultCode) ',
            print tupdata
        else:
            PtDebugPrint('psnlBookshelf: OnAgeVaultEvent - unknown event!')


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname == 'ShelfAUserID'):
            ageSDL = PtGetAgeSDL()
            if (type(ageSDL) != type(None)):
                if (ageSDL['ShelfAUserID'][0] == -1):
                    actBookshelf.enable()


    def OnNotify(self, state, id, events):
        global NBBookLocked
        global SpawnPointName
        global objBookPicked
        global boolShelfBusy
        global ShelfAUserID
        global boolLinkerIsMe
        global SpawnPointTitle
        global objLockPicked
        global boolPresentAfterLockOpen
        global ShelfABoolOperated
        if (id == actBookshelfExit.id):
            self.IDisengageShelf()
            return
        vault = ptVault()
        if ((id == SeekBehavior.id) and PtWasLocallyNotified(self.key)):
            for event in events:
                if ((event[0] == kMultiStageEvent) and (event[1] == 0)):
                    LocalAvatar = PtFindAvatar(events)
                    SeekBehavior.gotoStage(LocalAvatar, -1)
                    print 'psnlBookshelf.OnNotify():\tengaging bookshelf'
                    LocalAvatar.draw.disable()
                    virtCam = ptCamera()
                    virtCam.save(ShelfCamera.sceneobject.getKey())
                    PtAtTimeCallback(self.key, 0.10000000000000001, 1)
        if (id == actLinkingBookGUIPopup.id):
            for event in events:
                if (event[0] == kVariableEvent):
                    print 'psnlBookshelf: Received a message from the Book GUI: ',
                    print event[1]
                    if (event[1] == 'IShelveBook'):
                        self.IShelveBook()
                    if (event[1].split(',')[0] == 'ILink'):
                        LinkerID = event[3]
                        avatar = PtGetLocalAvatar()
                        myID = PtGetClientIDFromAvatarKey(avatar.getKey())
                        self.IShelveBook()
                        if (LinkerID == myID):
                            cam = ptCamera()
                            cam.enableFirstPersonOverride()
                            avatar.draw.enable()
                            virtCam = ptCamera()
                            virtCam.save(HutCamera.sceneobject.getKey())
                            PtGetControlEvents(false, self.key)
                            SpawnPointName = event[1].split(',')[1]
                            SpawnPointTitle = event[1].split(',')[2]
                            print 'psnlBookshelf: SpawnPointName = ',
                            print SpawnPointName,
                            print ' SpawnPointTitle = ',
                            print SpawnPointTitle
                            self.IResetShelf()
                            self.ILink()
                    stringAgeRequested = event[1]
                    idRequestor = event[3]
                    PtDebugPrint(('xLinkingBookGUI.OnNotify():\tpsnlBookshelf user id %d selected book %s from the shelf' % (idRequestor, stringAgeRequested)))
        if (id == -1):
            for event in events:
                if (event[0] == kVariableEvent):
                    print event[1],
                    print event[3]
                    if ((event[1] == 'YesNo') and (event[3] == 1)):
                        link = self.IGetLinkFromBook()
                        bookAge = self.IGetAgeFromBook()
                        if (bookAge == 'Ahnonay'):
                            bookVar = 'AhnyTempleDelete'
                        elif (bookAge == 'AhnySphere01'):
                            bookVar = 'AhnySphereDelete'
                        else:
                            bookVar = ''
                        if (bookVar == ''):
                            link.setVolatile(True)
                            link.save()
                        else:
                            sdl = xPsnlVaultSDL(1)
                            sdl[bookVar] = (1,)
                        PtDebugPrint('DEBUG: psnlBookshelf.OnNotify:\tSending volatile notify (hopefully)')
                        note = ptNotify(self.key)
                        note.setActivate(1.0)
                        note.addVarNumber(('Volatile' + bookAge), 1)
                        note.send()
                        bookName = objBookPicked.getName()
                        for (rkey, rvalue) in respDeleteBook.byObject.items():
                            parent = rvalue.getParentKey()
                            if parent:
                                if (bookName == parent.getName()):
                                    respDeleteBook.run(self.key, objectName=rkey)
                                    BookNumber = linkLibrary.index(bookAge)
                                    ageSDL = PtGetAgeSDL()
                                    ageSDL.setIndex('CurrentPage', BookNumber, 1)
                                    print ('Setting CurrentPage var of book %s to 1' % BookNumber)
                                    break
                        objBookPicked = None
                        return
            boolShelfBusy = false
            self.IUpdateLinks()
        if (not state):
            return
        if (id == actBookshelf.id):
            actBookshelf.disable()
            if PtWasLocallyNotified(self.key):
                PtSendKIMessage(kDisableKIandBB, 0)
                respRaiseShelfClickable.run(self.key)
                self.IUpdateLinks()
                for event in events:
                    if (event[0] == kPickedEvent):
                        if event[1]:
                            cam = ptCamera()
                            cam.undoFirstPerson()
                            cam.disableFirstPersonOverride()
                            PtRecenterCamera()
                            LocalAvatar = PtFindAvatar(events)
                            SeekBehavior.run(LocalAvatar)
                            ShelfABoolOperated = 1
                            if (AgeStartedIn == PtGetAgeName()):
                                ageSDL = PtGetAgeSDL()
                                ageSDL['ShelfABoolOperated'] = (1,)
                                avID = PtGetClientIDFromAvatarKey(LocalAvatar.getKey())
                                ageSDL['ShelfAUserID'] = (avID,)
                                ShelfAUserID = avID
                                print 'psnlBookshelf.OnNotify:\twrote SDL - Bookshelf A user id = ',
                                print avID
                                PtDisableMovementKeys()
                        break

        if (id == actBook.id):
            if PtWasLocallyNotified(self.key):
                boolLinkerIsMe = true
            ageSDL = PtGetAgeSDL()
            CurrentUser = ageSDL['ShelfAUserID'][0]
            avatar = PtGetLocalAvatar()
            myID = PtGetClientIDFromAvatarKey(avatar.getKey())
            boolShelfBusy = true
            actTray.disable()
            actBook.disable()
            actLock.disable()
            for event in events:
                if (event[0] == kPickedEvent):
                    objBookPicked = event[3]
                    bookName = objBookPicked.getName()
                    print 'psnlBookshelf.OnNotify():\tplayer picked book named ',
                    print bookName
                    try:
                        index = objLibrary.value.index(objBookPicked)
                    except:
                        print 'psnlBookshelf.OnNotify():\tERROR -- couldn\'t find ',
                        print objBookPicked,
                        print ' in objLibrary'
                        return
                    agename = self.IGetAgeFromBook()
                    if ((agename == 'city') and xxConfig.isOffline()):
                        ageVault = ptAgeVault()
                        citylink = self.GetOwnedAgeLink(ageVault, 'city')
                        bcolink = self.GetOwnedAgeLink(ageVault, 'BaronCityOffice')
                        citylinklocked = (citylink and citylink.getLocked())
                        bcolinklocked = (bcolink and bcolink.getLocked())
                        index = linkLibrary.index('city')
                        objLock = objLocks.value[index]
                        lockName = objLock.getName()
                        if (((type(citylinklocked) == type(None)) or citylinklocked) and ((type(bcolinklocked) == type(None)) or bcolinklocked)):
                            objLockPicked = objLocks.value[index]
                            lockName = objLockPicked.getName()
                            for (rkey, rvalue) in respOpenLock.byObject.items():
                                parent = rvalue.getParentKey()
                                if parent:
                                    if (lockName == parent.getName()):
                                        respOpenLock.run(self.key, objectName=rkey)
                                        break

                            boolPresentAfterLockOpen = true
                            break
                        else:
                            bookName = objBookPicked.getName()
                            for (rkey, rvalue) in respPresentBook.byObject.items():
                                parent = rvalue.getParentKey()
                                if parent:
                                    if (bookName == parent.getName()):
                                        respPresentBook.run(self.key, objectName=rkey)
                                        break
                        self.UsingBook = 1
                        actBookshelfExit.disable()
                        return
                    elif (agename == 'Neighborhood'):
                        agevault = ptAgeVault()
                        nblink = self.GetOwnedAgeLink(agevault, 'Neighborhood')
                        if (not nblink):
                            if NBBookLocked:
                                objLockPicked = objLocks.value[index]
                                lockName = objLockPicked.getName()
                                for (rkey, rvalue) in respOpenLock.byObject.items():
                                    parent = rvalue.getParentKey()
                                    if parent:
                                        if (lockName == parent.getName()):
                                            respOpenLock.run(self.key, objectName=rkey)
                                            break

                                boolPresentAfterLockOpen = true
                                break
                            else:
                                bookName = objBookPicked.getName()
                                for (rkey, rvalue) in respPresentBook.byObject.items():
                                    parent = rvalue.getParentKey()
                                    if parent:
                                        if (bookName == parent.getName()):
                                            respPresentBook.run(self.key, objectName=rkey)
                                            break
                                break
                    link = self.IGetLinkFromBook()
                    if (type(link) == type(None)):
                        return
                    if ((link in xCustomReltoShelf.availableBooks) or link.getLocked()):
                        objLockPicked = objLocks.value[index]
                        lockName = objLockPicked.getName()
                        for (rkey, rvalue) in respOpenLock.byObject.items():
                            parent = rvalue.getParentKey()
                            if parent:
                                if (lockName == parent.getName()):
                                    respOpenLock.run(self.key, objectName=rkey)
                                    break
                        boolPresentAfterLockOpen = true
                        break
                    else:
                        bookName = objBookPicked.getName()
                        for (rkey, rvalue) in respPresentBook.byObject.items():
                            parent = rvalue.getParentKey()
                            if parent:
                                if (bookName == parent.getName()):
                                    respPresentBook.run(self.key, objectName=rkey)
                                    break
            self.UsingBook = 1
            actBookshelfExit.disable()
            return
        if ((id == respPresentBook.id) and (type(objBookPicked) != type(None))):
            if boolLinkerIsMe:
                stringShowMeAge = self.IGetAgeFromBook()
                PtDebugPrint(('psnlBookshelf.OnNotify():\tsend message - show client %d age %s' % (ShelfAUserID, stringShowMeAge)))
                note = ptNotify(self.key)
                note.setActivate(1.0)
                note.addVarNumber(((stringShowMeAge + ',') + str(objLibrary.value.index(objBookPicked))), ShelfAUserID)
                note.send()
            return
        if (id == respShelveBook.id):
            agename = self.IGetAgeFromBook()
            if ((agename == 'city') and xxConfig.isOffline()):
                ageVault = ptAgeVault()
                citylink = self.GetOwnedAgeLink(ageVault, 'city')
                bcolink = self.GetOwnedAgeLink(ageVault, 'BaronCityOffice')
                citylinklocked = (citylink and citylink.getLocked())
                bcolinklocked = (bcolink and bcolink.getLocked())
                index = linkLibrary.index('city')
                objLock = objLocks.value[index]
                lockName = objLock.getName()
                if (((type(citylinklocked) == type(None)) or citylinklocked) and ((type(bcolinklocked) == type(None)) or bcolinklocked)):
                    lockName = objLockPicked.getName()
                    for (rkey, rvalue) in respCloseLock.byObject.items():
                        parent = rvalue.getParentKey()
                        if parent:
                            if (lockName == parent.getName()):
                                respCloseLock.run(self.key, objectName=rkey)
                                objLockPicked = None
                                break

                else:
                    boolShelfBusy = false
                    self.IUpdateLinks()
                return
            elif (agename == 'Pods'):
                if self.IsPodBookLocked():
                    lockName = objLockPicked.getName()
                    for (rkey, rvalue) in respCloseLock.byObject.items():
                        parent = rvalue.getParentKey()
                        if parent:
                            if (lockName == parent.getName()):
                                respCloseLock.run(self.key, objectName=rkey)
                                break
            elif (agename == 'Neighborhood'):
                agevault = ptAgeVault()
                nblink = self.GetOwnedAgeLink(agevault, 'Neighborhood')
                if (not nblink):
                    if NBBookLocked:
                        lockName = objLockPicked.getName()
                        for (rkey, rvalue) in respCloseLock.byObject.items():
                            parent = rvalue.getParentKey()
                            if parent:
                                if (lockName == parent.getName()):
                                    respCloseLock.run(self.key, objectName=rkey)
                                    objLockPicked = None
                                    break
                    else:
                        boolShelfBusy = false
                        self.IUpdateLinks()
                    return
            link = self.IGetLinkFromBook()
            if (type(link) == type(None)):
                return
            if ((link in xCustomReltoShelf.availableBooks) or link.getLocked()):
                lockName = objLockPicked.getName()
                for (rkey, rvalue) in respCloseLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respCloseLock.run(self.key, objectName=rkey)
                            objLockPicked = None
                            break
            else:
                boolShelfBusy = false
                self.IUpdateLinks()
            return
        if (id == actLock.id):
            boolShelfBusy = true
            actTray.disable()
            actBook.disable()
            actLock.disable()
            for event in events:
                if (event[0] == kPickedEvent):
                    objLockPicked = event[3]
                    try:
                        index = objLocks.value.index(objLockPicked)
                    except:
                        print "psnlBookshelf.OnNotify():\tERROR -- couldn't find ",
                        print objLockPicked,
                        print ' in objLocks'
                        return
                    objBookPicked = objLibrary.value[index]
                    lockName = objLockPicked.getName()
                    agename = self.IGetAgeFromBook()
                    if ((agename == 'city') and xxConfig.isOffline()):
                        agevault = ptAgeVault()
                        citylink = self.GetOwnedAgeLink(agevault, 'city')
                        bcolink = self.GetOwnedAgeLink(agevault, 'BaronCityOffice')
                        citylinklocked = (citylink and citylink.getLocked())
                        bcolinklocked = (bcolink and bcolink.getLocked())
                        if (((type(citylinklocked) == type(None)) or citylinklocked) and ((type(bcolinklocked) == type(None)) or bcolinklocked)):
                            for (rkey, rvalue) in respOpenLock.byObject.items():
                                parent = rvalue.getParentKey()
                                if parent:
                                    if (lockName == parent.getName()):
                                        respOpenLock.run(self.key, objectName=rkey)
                                        break
                            (citylink and citylink.setLocked(0))
                            (bcolink and bcolink.setLocked(0))
                        else:
                            for (rkey, rvalue) in respCloseLock.byObject.items():
                                parent = rvalue.getParentKey()
                                if parent:
                                    if (lockName == parent.getName()):
                                        respCloseLock.run(self.key, objectName=rkey)
                                        break
                            (citylink and citylink.setLocked(1))
                            (bcolink and bcolink.setLocked(1))
                        if vault.inMyPersonalAge():
                            (citylink and citylink.save())
                            (bcolink and bcolink.save())
                        return
                    elif (agename == 'Neighborhood'):
                        agevault = ptAgeVault()
                        nblink = self.GetOwnedAgeLink(agevault, 'Neighborhood')
                        if (not nblink):
                            if NBBookLocked:
                                for (rkey, rvalue) in respOpenLock.byObject.items():
                                    parent = rvalue.getParentKey()
                                    if parent:
                                        if (lockName == parent.getName()):
                                            respOpenLock.run(self.key, objectName=rkey)
                                            break
                                NBBookLocked = 0
                            else:
                                for (rkey, rvalue) in respCloseLock.byObject.items():
                                    parent = rvalue.getParentKey()
                                    if parent:
                                        if (lockName == parent.getName()):
                                            respCloseLock.run(self.key, objectName=rkey)
                                            break
                                NBBookLocked = 1
                            return
                    elif (agename == 'Pods'):
                        if self.IsPodBookLocked():
                            for (rkey, rvalue) in respOpenLock.byObject.items():
                                parent = rvalue.getParentKey()
                                if parent:
                                    if (lockName == parent.getName()):
                                        respOpenLock.run(self.key, objectName=rkey)
                                        break
                            self.SetPodBookLocked(0)
                        else:
                            for (rkey, rvalue) in respCloseLock.byObject.items():
                                parent = rvalue.getParentKey()
                                if parent:
                                    if (lockName == parent.getName()):
                                        respCloseLock.run(self.key, objectName=rkey)
                                        break
                            self.SetPodBookLocked(1)
                        return
                    link = self.IGetLinkFromBook()
                    if (type(link) == type(None)):
                        return
                    lockName = objLockPicked.getName()
                    if link.getLocked():
                        for (rkey, rvalue) in respOpenLock.byObject.items():
                            parent = rvalue.getParentKey()
                            if parent:
                                if (lockName == parent.getName()):
                                    respOpenLock.run(self.key, objectName=rkey)
                                    break
                        link.setLocked(False)
                        if vault.inMyPersonalAge():
                            link.save()
                    else:
                        for (rkey, rvalue) in respCloseLock.byObject.items():
                            parent = rvalue.getParentKey()
                            if parent:
                                if (lockName == parent.getName()):
                                    respCloseLock.run(self.key, objectName=rkey)
                                    break

                        link.setLocked(True)
                        if vault.inMyPersonalAge():
                            link.save()
                    break
            return
        if (id == respOpenLock.id):
            if boolPresentAfterLockOpen:
                bookName = objBookPicked.getName()
                for (rkey, rvalue) in respPresentBook.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (bookName == parent.getName()):
                            respPresentBook.run(self.key, objectName=rkey)
                            break
                boolPresentAfterLockOpen = false
            else:
                boolShelfBusy = false
                self.IUpdateLinks()
            return
        if (id == respCloseLock.id):
            boolShelfBusy = false
            self.IUpdateLinks()
            return
        if (id == actTray.id):
            boolShelfBusy = true
            actTray.disable()
            actBook.disable()
            actLock.disable()
            for event in events:
                if (event[0] == kPickedEvent):
                    objTrayPicked = event[3]
                    break
            try:
                index = objTrays.value.index(objTrayPicked)
            except:
                print "psnlBookshelf.OnNotify():\tERROR -- couldn't find ",
                print objTrayPicked,
                print ' in objTrays'
                return
            objBookPicked = objLibrary.value[index]
            objLockPicked = objLocks.value[index]
            link = self.IGetLinkFromBook()
            if (not link):
                return
            bookAge = self.IGetAgeFromBook()
            if bookAge in ['Pods', 'Direbo'] or (xxConfig.isOnline() and bookAge in ['Myst', 'Ahnonay', 'AhnySphere01']):
                if bookAge == 'Pods':
                    PtSendKIMessage(kKIOKDialogNoQuit, 'Resetting the pod age is not possible as it is a global, non-instanced age.')
                elif bookAge == 'AhnySphere01':
                    PtSendKIMessage(kKIOKDialogNoQuit, 'Resetting Ahnonay is not possible as it is a global, non-instanced age.')
                else:
                    PtSendKIMessage(kKIOKDialogNoQuit, 'Resetting %s is not possible as it is a global, non-instanced age.' % bookAge)
                objBookPicked = None
                boolShelfBusy = false
                self.IUpdateLinks()
                return
            if (bookAge == 'Ahnonay'):
                sdl = xPsnlVaultSDL(1)
                isVolatile = sdl['AhnyTempleDelete'][0]
                bookVar = 'AhnyTempleDelete'
            elif (bookAge == 'AhnySphere01'):
                sdl = xPsnlVaultSDL(1)
                isVolatile = sdl['AhnySphereDelete'][0]
                bookVar = 'AhnySphereDelete'
            else:
                isVolatile = link.getVolatile()
                bookVar = ''
            if isVolatile:
                if (bookVar == ''):
                    link.setVolatile(False)
                    link.save()
                else:
                    sdl = xPsnlVaultSDL(1)
                    sdl[bookVar] = (0,)
                PtDebugPrint('DEBUG: psnlBookshelf.OnNotify:\tSending notvolatile notify (hopefully)')
                note = ptNotify(self.key)
                note.setActivate(1.0)
                note.addVarNumber(('NotVolatile' + bookAge), 1)
                note.send()
                bookName = objBookPicked.getName()
                for (rkey, rvalue) in respReturnTray.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (bookName == parent.getName()):
                            respReturnTray.run(self.key, objectName=rkey)
                            break
                objBookPicked = None
            elif vault.inMyPersonalAge():
                if (bookAge == 'Neighborhood'):
                    PtYesNoDialog(self.key, xLocalization.xGlobal.xDeleteNeighborhoodBook)
                else:
                    PtYesNoDialog(self.key, xLocalization.xGlobal.xDeleteBook)
        if ((id == respReturnTray.id) or (id == respDeleteBook.id)):
            boolShelfBusy = false
            self.IUpdateLinks()
            return


    def IGetLinkFromBook(self, spTitle = None):
        global SpawnPointName
        ageName = self.IGetAgeFromBook()
        print 'returns link element associated with global objBookPicked or None ',
        print ageName
        if (ageName == 'city'):
            for (age, splist) in CityBookAges.items():
                if (spTitle in splist):
                    ageName = age
                    break
        elif (ageName == 'Pods'):
            vault = ptAgeVault()
            for (age, splist) in xLinkingBookDefs.PodAges.items():
                agelink = self.GetOwnedAgeLink(vault, age)
                if (type(agelink) != type(None)):
                    return agelink
        elif (ageName == 'AhnySphere01'):
            print 'spTitle ',
            print spTitle
            if (spTitle in sphere01Cloths):
                ageName = 'AhnySphere01'
            elif (spTitle in sphere02Cloths):
                ageName = 'AhnySphere02'
            elif (spTitle in sphere03Cloths):
                ageName = 'AhnySphere03'
            elif (spTitle in sphere04Cloths):
                ageName = 'AhnySphere04'
            elif (spTitle == 'Default'):
                ageName = SpawnPointName
                SpawnPointName = 'LinkInPointDefault'
        if (type(ageName) == type(None)):
            print 'psnlBookshelf.IGetLinkFromBook():\tERROR -- conversion from book to link element failed'
            return None
        ageVault = ptAgeVault()
        PAL = ageVault.getAgesIOwnFolder()
        contents = PAL.getChildNodeRefList()
        for content in contents:
            link = content.getChild()
            link = link.upcastToAgeLinkNode()
            info = link.getAgeInfo()
            if (info and (info.getAgeFilename() == ageName)):
                print 'psnlBookshelf.IGetLinkFromBook():\tfound link',
                print info.getAgeFilename()
                return link
        if (ageName in xCustomReltoShelf.availableBooks):
            return ageName
        print 'psnlBookshelf.IGetLinkFromBook():\tERROR -- couldn\'t find link to',
        print ageName
        return None


    def GetAhnonaySphere(self):
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
            if (ageName == 'Ahnonay'):
                ahnySDL = info.getAgeSDL()
                ahnyRecord = ahnySDL.getStateDataRecord()
                currentSphere = ahnyRecord.findVar('ahnyCurrentSphere')
                curSphere = currentSphere.getInt(0)
                return curSphere
        return 0


    def IUpdateLocksAndTrays(self):
        ageVault = ptAgeVault()
        PAL = ageVault.getAgesIOwnFolder()
        contents = PAL.getChildNodeRefList()
        if self.HasCityBook():
            citylink = self.GetOwnedAgeLink(ageVault, 'city')
            bcolink = self.GetOwnedAgeLink(ageVault, 'BaronCityOffice')
            citylinklocked = (citylink and citylink.getLocked())
            bcolinklocked = (bcolink and bcolink.getLocked())
            index = linkLibrary.index('city')
            objLock = objLocks.value[index]
            lockName = objLock.getName()
            if (((type(citylinklocked) == type(None)) or citylinklocked) and ((type(bcolinklocked) == type(None)) or bcolinklocked)):
                #print 'psnlBookshelf.IUpdateLocksAndTrays():\tsetting clasp to locked: ',lockName
                for (rkey, rvalue) in respCloseLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respCloseLock.run(self.key, objectName=rkey, fastforward=1)
            else:
                #print 'psnlBookshelf.IUpdateLocksAndTrays():\tsetting clasp to unlocked: ',lockName
                for (rkey, rvalue) in respOpenLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respOpenLock.run(self.key, objectName=rkey, fastforward=1)
        if self.HasPodBook():
            index = linkLibrary.index('Pods')
            objLock = objLocks.value[index]
            lockName = objLock.getName()
            if self.IsPodBookLocked():
                #print 'psnlBookshelf.IUpdateLocksAndTrays():\tsetting clasp to locked: ',lockName
                for (rkey, rvalue) in respCloseLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respCloseLock.run(self.key, objectName=rkey, fastforward=1)
            else:
                #print 'psnlBookshelf.IUpdateLocksAndTrays():\tsetting clasp to unlocked: ',lockName
                for (rkey, rvalue) in respOpenLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respOpenLock.run(self.key, objectName=rkey, fastforward=1)
        ageVault = ptAgeVault()
        nblink = self.GetOwnedAgeLink(ageVault, 'Neighborhood')
        if (not nblink):
            NBProcessed = 1
            index = linkLibrary.index('Neighborhood')
            objLock = objLocks.value[index]
            lockName = objLock.getName()
            if NBBookLocked:
                for (rkey, rvalue) in respCloseLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respCloseLock.run(self.key, objectName=rkey, fastforward=1)
            else:
                for (rkey, rvalue) in respOpenLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respOpenLock.run(self.key, objectName=rkey, fastforward=1)
        else:
            NBProcessed = 0
        for content in contents:
            link = content.getChild()
            link = link.upcastToAgeLinkNode()
            info = link.getAgeInfo()
            if (not info):
                continue
            ageName = info.getAgeFilename()
            try:
                index = linkLibrary.index(ageName)
            except:
                print 'psnlBookshelf.IUpdateLocksAndTrays():\tno matching book for KI\'s link to:',
                print ageName,
                print '...skipping to next'
                continue
            if ((((ageName == 'city') or (ageName == 'BaronCityOffice')) and xxConfig.isOffline()) or ((ageName in CityBookAges.keys()) or ((ageName == 'Neighborhood') and NBProcessed))):
                continue
            if (ageName in xLinkingBookDefs.PodAges.keys()):
                continue
            if (ageName == 'Cleft'):
                if (not link.getLocked()):
                    link.setLocked(True)
                    vault = ptVault()
                    if vault.inMyPersonalAge():
                        link.save()
                continue
            objLock = objLocks.value[index]
            lockName = objLock.getName()
            if link.getLocked():
                #print 'psnlBookshelf.IUpdateLocksAndTrays():\tsetting clasp to locked: ',lockName
                for (rkey, rvalue) in respCloseLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respCloseLock.run(self.key, objectName=rkey, fastforward=1)
            else:
                #print 'psnlBookshelf.IUpdateLocksAndTrays():\tsetting clasp to unlocked: ',lockName
                for (rkey, rvalue) in respOpenLock.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            respOpenLock.run(self.key, objectName=rkey, fastforward=1)

            if (ageName == 'Ahnonay'):
                sdl = xPsnlVaultSDL(1)
                isVolatile = sdl['AhnyTempleDelete'][0]
            elif (ageName == 'AhnySphere01'):
                sdl = xPsnlVaultSDL(1)
                isVolatile = sdl['AhnySphereDelete'][0]
            else:
                isVolatile = link.getVolatile()
            objBook = objLibrary.value[index]
            bookName = objBook.getName()
            if isVolatile:
                #print 'psnlBookshelf.IUpdateLocksAndTrays():\tsetting booktray to VOLATILE: ',bookName
                for (rkey, rvalue) in respDeleteBook.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (bookName == parent.getName()):
                            respDeleteBook.run(self.key, objectName=rkey, fastforward=1)
            else:
                #print 'psnlBookshelf.IUpdateLocksAndTrays():\tsetting booktray to NOT volatile: ',bookName
                for (rkey, rvalue) in respReturnTray.byObject.items():
                    parent = rvalue.getParentKey()
                    if parent:
                        if (bookName == parent.getName()):
                            respReturnTray.run(self.key, objectName=rkey, fastforward=1)
        return


    def IUpdateLinks(self):
        actTray.disable()
        actBook.disable()
        actLock.disable()
        vault = ptVault()
        boolInMyAge = vault.inMyPersonalAge()
        if self.HasCityBook():
            ageVault = ptAgeVault()
            citylink = self.GetOwnedAgeLink(ageVault, 'city')
            bcolink = self.GetOwnedAgeLink(ageVault, 'BaronCityOffice')
            citylinklocked = (citylink and citylink.getLocked())
            bcolinklocked = (bcolink and bcolink.getLocked())
            index = linkLibrary.index('city')
            objBook = objLibrary.value[index]
            objBook.draw.enable()
            objBook.physics.suppress(1)
            bookName = objBook.getName()
            if boolInMyAge or not (((type(citylinklocked) == type(None)) or citylinklocked) and ((type(bcolinklocked) == type(None)) or bcolinklocked)):
                for (key, value) in actBook.byObject.items():
                    parent = value.getParentKey()
                    if parent:
                        if (bookName == parent.getName()):
                            actBook.enable(objectName=key)
                            objBook.physics.suppress(0)
                            break
            objTray = objTrays.value[index]
            trayName = objTray.getName()
            objLock = objLocks.value[index]
            lockName = objLock.getName()
            if boolInMyAge:
                for (key, value) in actLock.byObject.items():
                    parent = value.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            actLock.enable(objectName=key)
                            break
        if self.HasPodBook():
            ageVault = ptAgeVault()
            index = linkLibrary.index('Pods')
            objBook = objLibrary.value[index]
            objBook.draw.enable()
            objBook.physics.suppress(1)
            bookName = objBook.getName()
            if boolInMyAge or not self.IsPodBookLocked():
                for (key, value) in actBook.byObject.items():
                    parent = value.getParentKey()
                    if parent:
                        if (bookName == parent.getName()):
                            actBook.enable(objectName=key)
                            objBook.physics.suppress(0)
                            break
            objTray = objTrays.value[index]
            trayName = objTray.getName()
            objLock = objLocks.value[index]
            lockName = objLock.getName()
            if boolInMyAge:
                for (key, value) in actLock.byObject.items():
                    parent = value.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            actLock.enable(objectName=key)
                            break
                for (key, value) in actTray.byObject.items():
                    parent = value.getParentKey()
                    if parent:
                        if (trayName == parent.getName()):
                            actTray.enable(objectName=key)
                            break
        ageVault = ptAgeVault()
        nblink = self.GetOwnedAgeLink(ageVault, 'Neighborhood')
        if (not nblink):
            NeighborhoodSet = 1
            index = linkLibrary.index('Neighborhood')
            objBook = objLibrary.value[index]
            objBook.draw.enable()
            objBook.physics.suppress(1)
            bookName = objBook.getName()
            if boolInMyAge or not NBBookLocked:
                for (key, value) in actBook.byObject.items():
                    parent = value.getParentKey()
                    if parent:
                        if (bookName == parent.getName()):
                            actBook.enable(objectName=key)
                            objBook.physics.suppress(0)
                            break
            if boolInMyAge:
                objLock = objLocks.value[index]
                lockName = objLock.getName()
                for (key, value) in actLock.byObject.items():
                    parent = value.getParentKey()
                    if parent:
                        if (lockName == parent.getName()):
                            actLock.enable(objectName=key)
                            break
        else:
            NeighborhoodSet = 0
        ageVault = ptAgeVault()
        PAL = ageVault.getAgesIOwnFolder()
        if (type(PAL) != type(None)):
            contents = PAL.getChildNodeRefList()
            sdl = xPsnlVaultSDL(1)
            cleftVis = sdl['CleftVisited'][0]
            for content in contents:
                link = content.getChild()
                link = link.upcastToAgeLinkNode()
                info = link.getAgeInfo()
                if (not info):
                    continue
                ageName = info.getAgeFilename()
                if (((ageName == 'Cleft') and (not cleftVis)) or (((ageName == 'city') or (ageName == 'BaronCityOffice')) or ((ageName in CityBookAges.keys()) or ((ageName == 'Neighborhood') and NeighborhoodSet)))):
                    continue
                if (ageName in xLinkingBookDefs.PodAges.keys()):
                    continue
                elif (ageName == 'AhnySphere01'):
                    if (self.GetAhnonaySphere() <= 0):
                        continue
                try:
                    index = linkLibrary.index(ageName)
                except:
                    print "psnlBookshelf.IUpdateLinks():\tno matching book for KI's link to:",
                    print ageName,
                    print '...skipping to next'
                    continue
                objBook = objLibrary.value[index]
                objBook.draw.enable()
                objBook.physics.suppress(1)
                if boolShelfBusy:
                    return
                print 'psnlBookshelf.IUpdateLinks():\tageName:',
                print ageName,
                print 'boolInMyAge:',
                print boolInMyAge,
                print 'getLocked():',
                print link.getLocked(),
                print 'getVolatile():',
                print link.getVolatile()
                if ((not boolInMyAge) and (link.getLocked() or (ageName == 'Cleft'))):
                    continue
                if (ageName == 'Ahnonay'):
                    sdl = xPsnlVaultSDL(1)
                    isVolatile = sdl['AhnyTempleDelete'][0]
                elif (ageName == 'AhnySphere01'):
                    sdl = xPsnlVaultSDL(1)
                    isVolatile = sdl['AhnySphereDelete'][0]
                else:
                    isVolatile = link.getVolatile()
                if (not isVolatile):
                    bookName = objBook.getName()
                    for (key, value) in actBook.byObject.items():
                        parent = value.getParentKey()
                        if parent:
                            if (bookName == parent.getName()):
                                actBook.enable(objectName=key)
                                objBook.physics.suppress(0)
                                break
                objTray = objTrays.value[index]
                trayName = objTray.getName()
                objLock = objLocks.value[index]
                lockName = objLock.getName()
                if (boolInMyAge and (ageName != 'Cleft')):
                    if (ageName != 'Neighborhood'):
                        if (ageName != 'RestorationGuild'):
                            for (key, value) in actTray.byObject.items():
                                parent = value.getParentKey()
                                if parent:
                                    if (trayName == parent.getName()):
                                        actTray.enable(objectName=key)
                                        break
                        for (key, value) in actLock.byObject.items():
                            parent = value.getParentKey()
                            if parent:
                                if (lockName == parent.getName()):
                                    actLock.enable(objectName=key)
                                    break
        else:
            print 'psnlBookshelf: The PAL folder is missing'
        xCustomReltoShelf.UpdateBooks(linkLibrary, objLibrary, actBook)


    def CheckForCityBookSpawnPoint(self, agefilename, sptitle):
        if (agefilename in CityBookAges.keys()):
            splist = CityBookAges[agefilename]
            if (sptitle in splist):
                return 1
        return 0


    def ILink(self):
        import xLinkMgr
        PtSendKIMessage(kEnableKIandBB, 0)
        if (self.IGetAgeFromBook() in xCustomReltoShelf.availableBooks):
            xCustomReltoShelf.PageClicked(SpawnPointTitle)
            return
# Do our own linking for Myst V ages and Pods BEGIN
        if (self.IGetAgeFromBook() in ['Pods', 'Direbo']):
            if self.IGetAgeFromBook() == 'Pods':
                xLinkMgr.LinkToAge(SpawnPointTitle, SpawnPointName)
            else:
                xLinkMgr.LinkToAge('Direbo', 'LinkInPoint1')
            return
# Do our own linking for Myst V ages and Pods END
        if (self.IGetAgeFromBook() == 'Neighborhood'):
            agevault = ptAgeVault()
            nblink = self.GetOwnedAgeLink(agevault, 'Neighborhood')
            if (not nblink):
                als = ptAgeLinkStruct()
                ainfo = ptAgeInfoStruct()
                ainfo.setAgeFilename('Neighborhood')
                als.setAgeInfo(ainfo)
                als.setLinkingRules(PtLinkingRules.kOwnedBook)
                spnpnt = ptSpawnPointInfo(SpawnPointTitle, SpawnPointName)
                als.setSpawnPoint(spnpnt)
                PtSendKIMessage(kEnableKIandBB, 0)
                linkMgr = ptNetLinkingMgr()
                linkMgr.linkToAge(als)
                print 'ILink Done'
                return
        link = self.IGetLinkFromBook(SpawnPointTitle)
        if (type(link) == type(None)):
            print 'psnlBookshelf.ILink():\tERROR -- conversion from book to link failed -- aborting'
            return
        info = link.getAgeInfo()
        print ('psnlBookshelf.ILink():\tattempting link to %s(%s)' % (info.getAgeFilename(), info.getAgeInstanceName()))
# Do our own linking for Myst V ages and Pods BEGIN
        if (info.getAgeFilename() == 'DescentMystV'):
            xLinkMgr.LinkToAge('DescentMystV', 'LinkInPointDefault')
            return
# Do our own linking for Myst V ages and Pods END
# Ahnonay Sphere 4 work-around BEGIN
        if (info.getAgeFilename() == 'AhnySphere04'):
            PtSendKIMessage(kKISitOnNextLinkOut, 0)
# Ahnonay Sphere 4 work-around END
        als = link.asAgeLinkStruct()
        vault = ptVault()
        if vault.inMyPersonalAge():
            als.setLinkingRules(PtLinkingRules.kOwnedBook)
        elif (info.getAgeFilename() == 'Neighborhood'):
            als.setLinkingRules(PtLinkingRules.kOriginalBook)
        else:
            als.setLinkingRules(PtLinkingRules.kBasicLink)
        print 'Ilink: SpawnPointName = ',
        print SpawnPointName,
        print 'SpawnPointTitle = ',
        print SpawnPointTitle
        spnpnt = None
        spawnPoints = link.getSpawnPoints()
        for sp in spawnPoints:
            if (((sp.getTitle() == SpawnPointTitle) and (sp.getName() == SpawnPointName)) or self.CheckForCityBookSpawnPoint(info.getAgeFilename(), SpawnPointTitle)):
                #print 'psnlBookshelf.ILink():found spawn point: %s, %s' % (sp.getTitle(),sp.getName())
                spnpnt = sp
                break
        if (not spnpnt):
            spnpnt = ptSpawnPointInfo(SpawnPointTitle, SpawnPointName)
        als.setSpawnPoint(spnpnt)
        linkMgr = ptNetLinkingMgr()
        linkMgr.linkToAge(als)
        #print 'ILink Done'


    def IShelveBook(self):
        bookName = objBookPicked.getName()
        for (rkey, rvalue) in respShelveBook.byObject.items():
            parent = rvalue.getParentKey()
            if parent:
                if (bookName == parent.getName()):
                    respShelveBook.run(self.key, objectName=rkey)
                    break
        self.UsingBook = 0
        actBookshelfExit.enable()


    def IGetAgeFromBook(self):
        try:
            index = objLibrary.value.index(objBookPicked)
        except:
            print "psnlBookshelf.IUpdateLinks():\tERROR -- couldn't find",
            print objBookPicked,
            print ' in objLibrary'
            return None
        print 'psnlBookshelf.IGetAgeFromBook():\tpicked book goes to',
        print linkLibrary[index]
        return linkLibrary[index]


    def IResetShelf(self):
        global ShelfAUserID
        global ShelfABoolOperated
        PtDebugPrint('psnlBookshelf.IResetShelf:\tResetting shelf')
        ShelfABoolOperated = 0
        ShelfAUserID = -1
        respLowerShelfClickable.run(self.key)
        actBookshelf.enable()
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            ageSDL['ShelfABoolOperated'] = (0,)
            ageSDL['ShelfAUserID'] = (-1,)


    def IDisengageShelf(self):
        if ((AgeStartedIn == PtGetAgeName()) and (not self.UsingBook)):
            ageSDL = PtGetAgeSDL()
            CurrentBookshelfUser = ageSDL['ShelfAUserID'][0]
            PtDebugPrint(('psnlBookshelf.IDisengageShelf(): Player %s is done with the bookshelf.' % CurrentBookshelfUser))
            self.IResetShelf()
            avatar = PtGetLocalAvatar()
            myID = PtGetClientIDFromAvatarKey(avatar.getKey())
            if (myID == CurrentBookshelfUser):
                print "psnlBookshelf.IDisengageShelf(): I was the Shelf User, and I'm done with the Shelf now."
                avatar.draw.enable()
                cam = ptCamera()
                cam.enableFirstPersonOverride()
                virtCam = ptCamera()
                virtCam.save(HutCamera.sceneobject.getKey())
                PtEnableMovementKeys()
                actBookshelfExit.disable()
                PtGetControlEvents(false, self.key)
                PtSendKIMessage(kEnableKIandBB, 0)


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if ((controlKey == PlasmaControlKeys.kKeyExitMode) or (controlKey == PlasmaControlKeys.kKeyMoveBackward)):
            self.IDisengageShelf()


    def OnTimer(self, id):
        if (id == 1):
            PtGetControlEvents(true, self.key)
            actBookshelfExit.enable()


    def HasCityBook(self):
        vault = ptAgeVault()
        for (age, splist) in CityBookAges.items():
            agelink = self.GetOwnedAgeLink(vault, age)
            if (type(agelink) != type(None)):
                spawnPoints = agelink.getSpawnPoints()
                for sp in spawnPoints:
                    if (sp.getTitle() in splist):
                        print 'psnlBookshelf.HasCityBook(): found a city book link:',
                        print age,
                        print sp.getTitle()
                        return 1
        agelink = self.GetOwnedAgeLink(vault, 'city')
        if (type(agelink) != type(None)):
            spawnPoints = agelink.getSpawnPoints()
            for sp in spawnPoints:
                if (sp.getTitle() in xLinkingBookDefs.CityBookLinks):
                    print 'psnlBookshelf.HasCityBook(): found a city book link: city',
                    print sp.getTitle()
                    return 1
        print 'found no city book links'
        return 0


    def HasPodBook(self):
        vault = ptAgeVault()
        for (age, splist) in xLinkingBookDefs.PodAges.items():
            agelink = self.GetOwnedAgeLink(vault, age)
            if (type(agelink) != type(None)):
                spawnPoints = agelink.getSpawnPoints()
                for sp in spawnPoints:
                    if (sp.getTitle() in splist):
                        print 'psnlBookshelf.HasPodBook(): found a pod book link:',age,sp.getTitle()
                        return 1
        return 0


    def IsPodBookLocked(self):
        vault = ptAgeVault()
        for (age, splist) in xLinkingBookDefs.PodAges.items():
            agelink = self.GetOwnedAgeLink(vault, age)
            if (type(agelink) != type(None)):
                if not agelink.getLocked():
                    return 0
        return 1


    def SetPodBookLocked(self, isLocked):
        vault = ptAgeVault()
        for (age, splist) in xLinkingBookDefs.PodAges.items():
            agelink = self.GetOwnedAgeLink(vault, age)
            if (type(agelink) != type(None)):
                agelink.setLocked(isLocked)
                agelink.save()


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



