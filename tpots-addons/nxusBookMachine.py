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
import xLocalization
from xPsnlVaultSDL import *
import time
import string
import whrandom
import os
import re
import xxConfig
import xLinkMgr

def Uni(string):
    try:
        retVal = unicode(string)
        return retVal
    except:
        retVal = unicode(string, 'latin-1')
        return retVal

NexusGUI = ptAttribGUIDialog(1, 'The Nexus GUI')
actKISlot = ptAttribActivator(2, 'Actvtr: KI Slot')
respKISlot = ptAttribResponder(3, 'Rspndr: KI Slot')
camMachineOps = ptAttribSceneobject(4, 'Camera: machine ops')
behMachineOps = ptAttribBehavior(5, 'Behavior: machine ops')
respKISlotReturn = ptAttribResponder(6, 'Rspndr: KI Slot Return')
respGUIOn = ptAttribResponder(7, 'Rspndr: GUI On')
respGUIOff = ptAttribResponder(8, 'Rspndr: GUI Off')
respBookSelect = ptAttribResponder(9, 'Rspndr: Enable GetBook Btn')
actLink = ptAttribActivator(11, 'Actvtr: Link')
respLink = ptAttribResponder(12, 'Rspndr: Link')
respBookRetract = ptAttribResponder(13, 'Rspndr: Retract Book')
actGetBook = ptAttribActivator(14, 'Actvtr: Get Book')
respGetBook = ptAttribResponder(15, 'Rspndr: Get Book')
respButtonPress = ptAttribResponder(16, 'Rspndr: GetBook Btn Press')
objlistLinkPanels = ptAttribSceneobjectList(17, 'Objct: Link Panels')
respKISlotGlow = ptAttribResponder(18, 'Rspndr: KI Slot Glow')
kShownCityLinks = ['Ferry Terminal', 'Library Courtyard', 'Concert Hall Foyer', 'Tokotah Alley', 'Palace Alcove']
kNexusDialogName = 'NexusAgeDialog'
kIDBtnLinkCategory01 = 100
kIDTxtLinkCategory01 = 101
kIDBtnLinkCategory02 = 110
kIDTxtLinkCategory02 = 111
kIDBtnLinkCategory03 = 120
kIDTxtLinkCategory03 = 121
kIDBtnLinkCategory04 = 130
kIDTxtLinkCategory04 = 131
kCategoryLabel01 = xLocalization.xNexus.xCategoryLabel01
kCategoryLabel02 = xLocalization.xNexus.xCategoryLabel02
kCategoryLabel03 = xLocalization.xNexus.xCategoryLabel03
kCategoryLabel04 = Uni('Restoration Links')
kIDBtnNeighborhoodCreate = 400
kIDBtnNeighborhoodSelect = 401
kIDTxtNeighborhoodName = 402
kIDTxtNeighborhoodInfo = 403
kIDBtnNeighborhoodPublic = 404
kIDTxtNeighborhoodPublic = 405
kIDBtnScrollUp = 500
kIDBtnScrollDn = 501
kIDTxtLinkDescription = 200
kIDBtnLinkSelect01 = 210
kIDBtnLinkSelect02 = 220
kIDBtnLinkSelect03 = 230
kIDBtnLinkSelect04 = 240
kIDBtnLinkSelect05 = 250
kIDBtnLinkSelect06 = 260
kIDBtnLinkSelect07 = 270
kIDBtnLinkSelect08 = 280
kIDTxtLinkName01 = 211
kIDTxtLinkName02 = 221
kIDTxtLinkName03 = 231
kIDTxtLinkName04 = 241
kIDTxtLinkName05 = 251
kIDTxtLinkName06 = 261
kIDTxtLinkName07 = 271
kIDTxtLinkName08 = 281
kIDTxtLinkInfo01 = 212
kIDTxtLinkInfo02 = 222
kIDTxtLinkInfo03 = 232
kIDTxtLinkInfo04 = 242
kIDTxtLinkInfo05 = 252
kIDTxtLinkInfo06 = 262
kIDTxtLinkInfo07 = 272
kIDTxtLinkInfo08 = 282
kIDBtnDeleteLink01 = 310
kIDBtnDeleteLink02 = 320
kIDBtnDeleteLink03 = 330
kIDBtnDeleteLink04 = 340
kIDBtnDeleteLink05 = 350
kIDBtnDeleteLink06 = 360
kIDBtnDeleteLink07 = 370
kIDBtnDeleteLink08 = 380
kIDNameHeaderText = 600
kIDPopHeaderText = 601
kIDNameHeaderBtn = 610
kIDPopHeaderBtn = 611
kIDNameAscArrow = 620
kIDPopAscArrow = 621
kIDNameDescArrow = 630
kIDPopDescArrow = 631
kIDEngCheckBox = 700
kIDFreCheckBox = 701
kIDGerCheckBox = 702
kIDEngCheck = 710
kIDFreCheck = 711
kIDGerCheck = 712
kIDEngText = 720
kIDFreText = 721
kIDGerText = 722
AgenGoldDk = ptColor(0.92500000000000004, 0.83999999999999997, 0.36499999999999999, 1.0)
AgenGoldDarker = ptColor(0.8, 0.7, 0.23, 1.0)
AgenGoldLt = ptColor(0.96999999999999997, 0.93700000000000006, 0.745, 1.0)
AgenGoldDkSoft = ptColor(0.92500000000000004, 0.83999999999999997, 0.36499999999999999, 0.25)
AgenGoldLtSoft = ptColor(0.96999999999999997, 0.93700000000000006, 0.745, 0.25)
colorNormal = AgenGoldDk
colorMarked = AgenGoldDarker
colorSelected = AgenGoldLt
colorPresented = AgenGoldLt
colorDisabled = AgenGoldDkSoft
avatar = None
waitingOnGUIAnim = false
idLinkSelected = 0
idBookPresented = 0
boolGetBookBtnUp = false
boolGetBookAfterBtnPress = false
boolBookPresented = false
boolGetBookAfterBookRetract = false
idDeleteCandidateName = 0
idCategorySelected = kIDBtnLinkCategory01
boolLinking = false
boolGettingBook = false
indexDisplayStart = 0
dialogLoaded = 0
kNumDisplayFields = 8
kEmptyGuid = '0000000000000000'
kMaxDisplayableChars = 20
cityInfoNode = None
kChronicleVarType = 0
boolGUIActivated = 0
fullNeighborhoodName = u''
fullLinkName = []
untranslatedNeighborhoodName = u''
untranslatedName = []
statusBarText = u''
numCityLinks = 0
numGZLinks = 0
GZLinkNode = None
dynLinkCategories = [kIDBtnLinkCategory03, kIDBtnLinkCategory04]
global dynLinkSortBy, dynLinkReverse # initailized when clicking the category
MagicHoods = {'KirelMOUL': 'kirelPerf-SpawnPointBevin02', 'NeighborhoodMOUL': 'LinkInPointDefault'}

class nxusBookMachine(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5017
        version = 5
        self.version = version
        print '__init__nxusBookMachine v.',
        print version


    def OnFirstUpdate(self):
        global kCategoryLabel04
        PtLoadDialog(kNexusDialogName, self.key, 'Nexus')
        respKISlotReturn.run(self.key, fastforward=1)
        respBookRetract.run(self.key, fastforward=1)
        respButtonPress.run(self.key, fastforward=1)
        for objPanel in objlistLinkPanels.value:
            objPanel.draw.disable()


    def OnServerInitComplete(self):
        global cityInfoNode
        vault = ptVault()
        cityLink = vault.getLinkToCity()
        if (cityLink == None):
            cityInfoNode = None
        else:
            cityInfoNode = cityLink.getAgeInfo().asAgeInfoStruct()


    def __del__(self):
        PtUnloadDialog(kNexusDialogName)


    def IFilterAgeName(self, ageName):
        for name in xxConfig.AgeNameReplace:
            if (ageName.find(name) != -1):
                return ageName.replace(name, xxConfig.AgeNameReplace[name])
        return ageName


    def IGetAgeLinkNode(self, ageFilename):
        vault = ptVault()
        folder = vault.getAgesIOwnFolder()
        contents = folder.getChildNodeRefList()
        for content in contents:
            link = content.getChild()
            link = link.upcastToAgeLinkNode()
            if (type(link) != type(None)):
                info = link.getAgeInfo()
            if (not info):
                continue
            ageName = info.getAgeFilename()
            if (ageName == ageFilename):
                return link
        return None


    def IGetBevinLinkNode(self):
        return self.IGetAgeLinkNode('Neighborhood')


    def IGetGZLinkNode(self):
        return self.IGetAgeLinkNode('GreatZero')


    def IGetKirelLinkNode(self):
        return self.IGetAgeLinkNode('Neighborhood02')


    def IGetKveerMOULLinkNode(self):
        return self.IGetAgeLinkNode('KveerMOUL')


    def IGetCityLinkNode(self):
        return self.IGetAgeLinkNode('city')


    def IGetHoodLinkNode(self):
        vault = ptVault()
        folder = vault.getAgesIOwnFolder()
        contents = folder.getChildNodeRefList()
        for content in contents:
            link = content.getChild()
            link = link.upcastToAgeLinkNode()
            if (type(link) != type(None)):
                info = link.getAgeInfo()
            if (not info):
                continue
            ageName = info.getAgeFilename()
            if (ageName == 'Neighborhood'):
                return link
        return None


    def OnVaultNotify(self, event, tupdata):
        global idBookPresented
        global boolGetBookAfterBookRetract
        global boolBookPresented
        self.IUpdateLinks()
        if ((event == PtVaultNotifyTypes.kUnRegisteredOwnedAge) or (event == PtVaultNotifyTypes.kUnRegisteredVisitAge)):
            PtDebugPrint('OnVaultNotify: A link was deleted, checking if we need to retract the book')
            try:
                clickedLinkName = ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idBookPresented + 1))).getString()
                if (boolBookPresented and (not clickedLinkName)):
                    PtDebugPrint('OnVaultNotify: The currently displayed link was deleted, retracting book')
                    actLink.disable()
                    idBookPresented = 0
                    respBookRetract.run(self.key)
                    boolBookPresented = false
                    boolGetBookAfterBookRetract = false
            except:
                pass


    def OnNotify(self, state, id, events):
        global idBookPresented
        global boolGUIActivated
        global boolGettingBook
        global boolGetBookBtnUp
        global boolGetBookAfterBtnPress
        global boolBookPresented
        global boolLinking
        global avatar
        global waitingOnGUIAnim
        global boolGetBookAfterBookRetract
        global idLinkSelected
        if (type(avatar) == type(None)):
            PtDebugPrint('OnNotify: Initing avatar with PtGetLocalAvatar()')
            avatar = PtGetLocalAvatar()
        if (id == -1):
            if state:
                self.IDeleteLink()
            return
        if (not state):
            return
        if (id == actKISlot.id):
            avatar = PtFindAvatar(events)
            kiLevel = PtDetermineKILevel()
            print 'nxusBookMachine.OnNotify:\tplayer ki level is',
            print kiLevel
            if (kiLevel < kNormalKI):
                respKISlot.run(self.key, events=events)
            else:
                virtCam = ptCamera()
                virtCam.undoFirstPerson()
                virtCam.disableFirstPersonOverride()
                respKISlotGlow.run(self.key, events=events)
            return
        if (id == respKISlotGlow.id):
            behMachineOps.run(avatar)
            virtCam = ptCamera()
            virtCam.save(camMachineOps.sceneobject.getKey())
            avatar.draw.disable()
            if PtIsDialogLoaded(kNexusDialogName):
                NexusGUI.dialog.show()
                respGUIOn.run(self.key)
                waitingOnGUIAnim = true
            PtEnableControlKeyEvents(self.key)
            PtSendKIMessage(kDisableKIandBB, 0)
        if (id == respGUIOn.id):
            waitingOnGUIAnim = false
            boolGUIActivated = 1
        if (id == respGUIOff.id):
            boolGUIActivated = 0
            NexusGUI.dialog.hide()
            virtCam = ptCamera()
            virtCam.restore(camMachineOps.sceneobject.getKey())
            virtCam.enableFirstPersonOverride()
            avatar.draw.enable()
            behMachineOps.gotoStage(avatar, -1)
            PtDisableControlKeyEvents(self.key)
            PtSendKIMessage(kEnableKIandBB, 0)
            respKISlotReturn.run(self.key)
            if boolBookPresented:
                respBookRetract.run(self.key)
                actLink.disable()
                boolBookPresented = false
                boolGetBookAfterBookRetract = false
            if boolGetBookBtnUp:
                boolGetBookAfterBtnPress = false
                respButtonPress.run(self.key)
                boolGetBookBtnUp = false
            if idLinkSelected:
                idLinkSelected = 0
                self.IUpdateLinks()
            if idBookPresented:
                idBookPresented = 0
                self.IUpdateLinks()
            return
        if (id == actGetBook.id):
            boolGettingBook = true
            respButtonPress.run(self.key)
            boolGetBookBtnUp = false
            linkName = self.IGetUntranslatedName((idLinkSelected + 1))
            if (linkName == ''):
                boolGetBookAfterBtnPress = false
                boolGetBookAfterBookRetract = false
                idLinkSelected = 0
                idBookPresented = 0
                self.IUpdateLinks()
                self.IDisableGUIButtons()
                return
            if idBookPresented:
                boolGetBookAfterBtnPress = false
                boolGetBookAfterBookRetract = true
            else:
                boolGetBookAfterBtnPress = true
                boolGetBookAfterBookRetract = false
            idBookPresented = idLinkSelected
            idLinkSelected = 0
            self.IUpdateLinks()
            self.IDisableGUIButtons()
            return
        if (id == respButtonPress.id):
            if boolGetBookAfterBtnPress:
                respGetBook.run(self.key)
                self.IDrawLinkPanel()
                boolBookPresented = true
            elif boolGetBookAfterBookRetract:
                respBookRetract.run(self.key)
                actLink.disable()
            else:
                self.IUpdateLinks()
            return
        if ((id == respBookRetract.id) and boolGetBookAfterBookRetract):
            respGetBook.run(self.key)
            self.IDrawLinkPanel()
            boolBookPresented = true
            return
        if (id == respGetBook.id):
            self.IUpdateLinks()
            actLink.enable()
            boolGettingBook = false
            return
        if (id == respBookSelect.id):
            self.IUpdateLinks()
        if (id == actLink.id):
            if (idBookPresented == 0):
                PtDebugPrint('Ignoring link clickable since no book is shown')
                return
            respGUIOff.run(self.key)
            boolLinking = true
            actGetBook.disable()
            self.IDisableGUIButtons()
            respGUIOff.run(self.key)
            self.ILink()
            return
        if (id == respLink.id):
            return


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            if ((not boolGettingBook) and boolGUIActivated):
                actGetBook.disable()
                self.IDisableGUIButtons()
                respGUIOff.run(self.key)
            return
        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
            if ((not boolGettingBook) and boolGUIActivated):
                actGetBook.disable()
                self.IDisableGUIButtons()
                respGUIOff.run(self.key)
            return


    def OnGUINotify(self, id, control, event):
        global statusBarText
        global idBookPresented
        global boolGetBookAfterBtnPress
        global dialogLoaded
        global idCategorySelected
        global boolBookPresented
        global boolGetBookBtnUp
        global boolGetBookAfterBookRetract
        global idDeleteCandidateName
        global idLinkSelected
        global indexDisplayStart
        global dynLinkReverse, dynLinkSortBy
        if (id != NexusGUI.id):
            print 'nxusBookMachine.OnGUINotify():\tunexpected message id'
            return
        if (event == kDialogLoaded):
            dialogLoaded = 1
            return
        if (event == kShowHide):
            dialogLoaded = 1
            self.IUpdateLinks()
            return
        if (event == kAction):
            ctrlID = control.getTagID()
            if (((ctrlID >= kIDBtnLinkSelect01) and (ctrlID <= kIDBtnLinkSelect08)) or (ctrlID == kIDBtnNeighborhoodSelect)):
                if idBookPresented:
                    actLink.disable()
                    idBookPresented = 0
                    respBookRetract.run(self.key)
                    boolBookPresented = false
                    boolGetBookAfterBookRetract = false
                idLinkSelected = ctrlID
                self.IUpdateLinks()
                if (not boolGetBookBtnUp):
                    respBookSelect.run(self.key)
                    boolGetBookBtnUp = true
                    self.IDisableGUIButtons()
                return
            if ((ctrlID >= kIDBtnDeleteLink01) and (ctrlID <= kIDBtnDeleteLink08)):
                idDeleteCandidateName = (ctrlID - 99)
                ageName = self.IGetFullName(idDeleteCandidateName)
                stringConfirm = (xLocalization.xNexus.xLinkDeleteConfirm % ageName)
                boolNewHoodDlg = 0
                PtYesNoDialog(self.key, stringConfirm)
                return
            if ((ctrlID >= kIDBtnLinkCategory01) and (ctrlID <= kIDBtnLinkCategory04)):
                if (idLinkSelected != kIDBtnNeighborhoodSelect):
                    actLink.disable()
                indexDisplayStart = 0
                idCategorySelected = ctrlID
                idLinkSelected = 0
                if (boolGetBookBtnUp and (idLinkSelected != kIDBtnNeighborhoodSelect)):
                    respButtonPress.run(self.key)
                    self.IDisableGUIButtons()
                    boolGetBookBtnUp = false
                    boolGetBookAfterBtnPress = false
                    return
                if (idBookPresented and (idBookPresented != kIDBtnNeighborhoodSelect)):
                    respBookRetract.run(self.key)
                    boolBookPresented = false
                    boolGetBookAfterBookRetract = false
                    idBookPresented = 0
                # reset sorting
                dynLinkSortBy = xLinkMgr.kSortByName
                dynLinkReverse = False
                # update GUI
                self.IUpdateLinks()
                return
            if ((ctrlID == kIDBtnScrollUp) and (indexDisplayStart > 0)):
                indexDisplayStart = (indexDisplayStart - 1)
                if ((idLinkSelected >= kIDBtnLinkSelect01) and (idLinkSelected <= kIDBtnLinkSelect08)):
                    idLinkSelected = (idLinkSelected + 10)
                    if (idLinkSelected > (kIDBtnLinkSelect01 + ((kNumDisplayFields - 1) * 10))):
                        idLinkSelected = 0
                        if boolGetBookBtnUp:
                            respButtonPress.run(self.key)
                            self.IDisableGUIButtons()
                            boolGetBookBtnUp = false
                            boolGetBookAfterBtnPress = false
                if ((idBookPresented >= kIDBtnLinkSelect01) and (idBookPresented <= kIDBtnLinkSelect08)):
                    idBookPresented = (idBookPresented + 10)
                    if (idBookPresented > (kIDBtnLinkSelect01 + ((kNumDisplayFields - 1) * 10))):
                        boolBookPresented = false
                        boolGetBookAfterBookRetract = false
                        idBookPresented = 0
                        respBookRetract.run(self.key)
                self.IUpdateLinks()
                return
            if (ctrlID == kIDBtnScrollDn):
                indexDisplayStart = (indexDisplayStart + 1)
                if ((idLinkSelected >= kIDBtnLinkSelect01) and (idLinkSelected <= kIDBtnLinkSelect08)):
                    idLinkSelected = (idLinkSelected - 10)
                    if (idLinkSelected < kIDBtnLinkSelect01):
                        idLinkSelected = 0
                        if boolGetBookBtnUp:
                            respButtonPress.run(self.key)
                            self.IDisableGUIButtons()
                            boolGetBookBtnUp = false
                            boolGetBookAfterBtnPress = false
                if ((idBookPresented >= kIDBtnLinkSelect01) and (idBookPresented <= kIDBtnLinkSelect08)):
                    idBookPresented = (idBookPresented - 10)
                    print idBookPresented
                    if (idBookPresented < kIDBtnLinkSelect01):
                        boolBookPresented = false
                        boolGetBookAfterBookRetract = false
                        idBookPresented = 0
                        respBookRetract.run(self.key)
                self.IUpdateLinks()
                return
            elif (ctrlID in (kIDNameHeaderBtn, kIDPopHeaderBtn)):
                if idCategorySelected in dynLinkCategories:
                    # update sorting and reversing
                    if ctrlID == kIDNameHeaderBtn: sortBy = xLinkMgr.kSortByName
                    else: sortBy = xLinkMgr.kSortByDate
                    if sortBy == dynLinkSortBy:
                        dynLinkReverse = not dynLinkReverse
                    else:
                        dynLinkSortBy = sortBy
                        dynLinkReverse = False
                    # reset the presented book
                    if idBookPresented:
                        boolBookPresented = False
                        boolGetBookAfterBookRetract = False
                        idBookPresented = 0
                        respBookRetract.run(self.key)
                    # reset the selected age
                    idLinkSelected = 0
                    if boolGetBookBtnUp:
                        respButtonPress.run(self.key)
                        self.IDisableGUIButtons()
                        boolGetBookBtnUp = False
                        boolGetBookAfterBtnPress = False
                    # update dynamic age list
                    self.IUpdateLinks()
        if (event == kInterestingEvent):
            if (type(control) != type(None)):
                if control.isInteresting() and not idBookPresented:
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkDescription)).setStringW(self.IGetFullName(control.getTagID()))
                else:
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkDescription)).setStringW(statusBarText)


    def IUpdateLinks(self):
        global fullLinkName
        global fullNeighborhoodName
        global untranslatedName
        global untranslatedNeighborhoodName
        global statusBarText
        if (not dialogLoaded):
            return
        fullLinkName = []
        untranslatedName = []
        self.IDisableGUIButtons()
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkCategory01)).setForeColor(colorNormal)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkCategory02)).setForeColor(colorNormal)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkCategory03)).setForeColor(colorNormal)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkCategory04)).setForeColor(colorNormal)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idCategorySelected + 1))).setForeColor(colorSelected)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkCategory01)).setStringW(kCategoryLabel01)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkCategory02)).setStringW(kCategoryLabel02)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkCategory03)).setStringW(kCategoryLabel03)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkCategory04)).setStringW(kCategoryLabel04)
        if idCategorySelected in dynLinkCategories:
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDNameHeaderText)).setStringW(xLocalization.xNexus.xNameHeader)
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDNameHeaderBtn)).enable()
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDPopHeaderText)).setString('Last update')
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDPopHeaderBtn)).enable()
        else:
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDNameHeaderText)).setString('')
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDNameHeaderBtn)).disable()
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDPopHeaderText)).setString('')
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDPopHeaderBtn)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDNameAscArrow)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDNameDescArrow)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDPopAscArrow)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDPopDescArrow)).hide()
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDEngText)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDFreText)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDGerText)).setString('')
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDEngCheckBox)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDFreCheckBox)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDGerCheckBox)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDEngCheck)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDFreCheck)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDGerCheck)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkCategory01)).enable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkCategory02)).enable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkCategory03)).enable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkCategory04)).enable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(idCategorySelected)).disable()
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkName01)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkName02)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkName03)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkName04)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkName05)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkName06)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkName07)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkName08)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo01)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo02)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo03)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo04)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo05)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo06)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo07)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo08)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect01)).setNotifyOnInteresting(1)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect02)).setNotifyOnInteresting(1)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect03)).setNotifyOnInteresting(1)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect04)).setNotifyOnInteresting(1)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect05)).setNotifyOnInteresting(1)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect06)).setNotifyOnInteresting(1)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect07)).setNotifyOnInteresting(1)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect08)).setNotifyOnInteresting(1)
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink01)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink02)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink03)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink04)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink05)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink06)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink07)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink08)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollDn)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollUp)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodCreate)).hide()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodPublic)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodPublic)).hide()
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodPublic)).setForeColor(colorDisabled)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodPublic)).setString('')
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodSelect)).setNotifyOnInteresting(1)
        if (idBookPresented == kIDBtnNeighborhoodSelect):
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodName)).setForeColor(colorPresented)
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodInfo)).setForeColor(colorPresented)
        elif (idLinkSelected == kIDBtnNeighborhoodSelect):
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodName)).setForeColor(colorSelected)
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodInfo)).setForeColor(colorSelected)
        else:
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodName)).setForeColor(colorNormal)
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodInfo)).setForeColor(colorNormal)
        vault = ptVault()
        if (type(vault) == type(None)):
            PtDebugPrint('nxusBookMachine.IUpdateLinks:\tplayer vault type None')
            return
        PAL = vault.getAgesIOwnFolder()
        PtAssert(PAL, 'vault.getAgesIOwnFolder return bad')
        contents = PAL.getChildNodeRefList()
        for content in contents:
            link = content.getChild()
            link = link.upcastToAgeLinkNode()
            if (type(link) != type(None)):
                info = link.getAgeInfo()
            else:
                link = content.getChild()
                info = link.upcastToAgeInfoNode()
            if (not info):
                continue
            ageName = info.getAgeFilename()
            if (ageName == 'Neighborhood'):
                hoodLink = self.IGetHoodLinkNode()
                if (not hoodLink.getVolatile()):
                    untranslatedNeighborhoodName = Uni(info.getDisplayName())
                    stringHoodName = Uni(xLocalization.xGlobal.LocalizeAgeName(Uni(info.getDisplayName())))
                    fullNeighborhoodName = stringHoodName
                    if (len(stringHoodName) > kMaxDisplayableChars):
                        stringHoodName = (stringHoodName[:kMaxDisplayableChars] + u'...')
                    dniCoords = link.getCreateAgeCoords()
                    try:
                        stringHoodInfo = (u'%05d%   04d%   04d' % (dniCoords.GetTorans(), dniCoords.getHSpans(), dniCoords.getVSpans()))
                    except:
                        stringHoodInfo = (u'%05d%   04d%   04d' % (0, 0, 0))
                    stringHoodDesc = Uni(info.getAgeDescription())
                    if (idBookPresented == kIDBtnNeighborhoodSelect):
                        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodSelect)).disable()
                    else:
                        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodSelect)).enable()
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodName)).setStringW(stringHoodName)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodInfo)).setStringW(stringHoodInfo)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodPublic)).setString('Public')
                else:
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodName)).setString('')
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtNeighborhoodInfo)).setString('')
        statusBarText = u''
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkDescription)).setStringW(statusBarText)
        if (idCategorySelected == kIDBtnLinkCategory01):
            self.IUpdateCityLinks()
            self.IUpdateGZLinks()
            self.IUpdateHoodLinks()
            return
        elif (idCategorySelected in dynLinkCategories):
            self.IUpdateDynLinks()
            return
        folder = None
        if (idCategorySelected == kIDBtnLinkCategory02):
            folder = vault.getAgesICanVisitFolder()
        elif (idCategorySelected == kIDBtnLinkCategory04):
            folder = vault.getAgesIOwnFolder()
        if (type(folder) == type(None)):
            PtDebugPrint('nxusBookMachine.IUpdateLinks:\tlink folder type None')
            return
        contents = folder.getChildNodeRefList()
        if (idCategorySelected == kIDBtnLinkCategory04):
            for content in contents[:]:
                link = content.getChild()
                link = link.upcastToAgeLinkNode()
                info = link.getAgeInfo()
                thisAgeName = info.getAgeFilename()
                spawnPoints = link.getSpawnPoints()
                defaultFound = false
                if not (thisAgeName in xxConfig.InviteAges):
                    PtDebugPrint(('nxusBookMachine.IUpdateLinks():\tnot displaying personal age: %s' % thisAgeName))
                    contents.remove(content)
                    continue
                for spawnPoint in spawnPoints:
                    if (spawnPoint.getName() == 'LinkInPointDefault'):
                        defaultFound = true
                        break
                if (not defaultFound):
                    info = link.getAgeInfo()
                    PtDebugPrint((('Removing link for ' + info.getAgeFilename()) + " since you don't have the default link-in point"))
                    contents.remove(content)
        if (indexDisplayStart > 0):
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollUp)).show()
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollUp)).enable()
        numLinks = len(contents)
        if (numLinks > (kNumDisplayFields + indexDisplayStart)):
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollDn)).show()
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollDn)).enable()
        idTextbox = kIDTxtLinkName01
        index = -1
        for content in contents:
            index = (index + 1)
            if (index < indexDisplayStart):
                continue
            if (index > ((indexDisplayStart + kNumDisplayFields) - 1)):
                break
            linkNode = content.getChild()
            linkNode = linkNode.upcastToAgeLinkNode()
            if (type(linkNode) != type(None)):
                info = linkNode.getAgeInfo()
            else:
                linkNode = content.getChild()
                info = linkNode.upcastToAgeInfoNode()
            if (type(info) == type(None)):
                PtDebugPrint("nxusBookMachine: Can't find ageInfo from link", level=kErrorLevel)
                continue
            if (isinstance(linkNode, ptVaultAgeLinkNode) and linkNode.getVolatile()):
                index = (index - 1)
                continue
            if (idBookPresented == (idTextbox - 1)):
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).disable()
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorPresented)
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorPresented)
            else:
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).enable()
                if (idLinkSelected == (idTextbox - 1)):
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorSelected)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorSelected)
                else:
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorNormal)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorNormal)
            untranslatedName.append(Uni(info.getDisplayName()))
            displayName = Uni(self.IFilterAgeName(xLocalization.xGlobal.LocalizeAgeName(Uni(info.getDisplayName()))))
            fullLinkName.append(displayName)
            if (len(displayName) > kMaxDisplayableChars):
                displayName = (displayName[:kMaxDisplayableChars] + u'...')
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setStringW(displayName)
            dniCoords = linkNode.getCreateAgeCoords()
            try:
                stringLinkInfo = (u'%05d%   04d%   04d' % (dniCoords.GetTorans(), dniCoords.getHSpans(), dniCoords.getVSpans()))
            except:
                stringLinkInfo = (u'%05d%   04d%   04d' % (0, 0, 0))
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setStringW(stringLinkInfo)
            if (ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).getStringW() == Uni(xLocalization.xGlobal.LocalizeAgeName(u'Ferry Terminal'))):
                idTextbox = (idTextbox + 10)
                continue
            elif ((idCategorySelected == kIDBtnLinkCategory03) or (idCategorySelected == kIDBtnLinkCategory04)):
                idTextbox = (idTextbox + 10)
                continue
            else:
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox + 99))).show()
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox + 99))).enable()
                idTextbox = (idTextbox + 10)


    def IUpdateCityLinks(self):
        global numCityLinks
        numCityLinks = 0
        vault = ptVault()
        if (type(vault) == type(None)):
            PtDebugPrint('nxusBookMachine.IUpdateCityLinks:\tWARNING player vault type None')
            return
        cityLink = vault.getLinkToCity()
        if (cityLink == None):
            spawnpoints = [u'LinkInPointFerry']
        else:
            spawnpoints = cityLink.getSpawnPoints()
            ferryTerminalSP = None
            for sp in spawnpoints[:]:
                t = sp.getTitle()
                if (t == 'Ferry Terminal'):
                    ferryTerminalSP = sp
                    spawnpoints.remove(sp)
                elif not t in kShownCityLinks:
                    spawnpoints.remove(sp)
            if (ferryTerminalSP == None):
                spawnpoints = ([u'LinkInPointFerry'] + spawnpoints)
            else:
                spawnpoints = ([ferryTerminalSP] + spawnpoints)
        idTextbox = kIDTxtLinkName01
        index = -1
        for spawnpoint in spawnpoints:
            index = (index + 1)
            numCityLinks = (numCityLinks + 1)
            if (index < indexDisplayStart):
                continue
            if (index > ((indexDisplayStart + kNumDisplayFields) - 1)):
                break
            if (idBookPresented == (idTextbox - 1)):
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).disable()
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorPresented)
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorPresented)
            else:
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).enable()
                if (idLinkSelected == (idTextbox - 1)):
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorSelected)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorSelected)
                else:
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorNormal)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorNormal)
            if (spawnpoint == u'LinkInPointFerry'):
                untranslatedName.append(u'Ferry Terminal')
                displayName = Uni(xLocalization.xGlobal.LocalizeAgeName(u'Ferry Terminal'))
            else:
                untranslatedName.append(Uni(spawnpoint.getTitle()))
                displayName = Uni(self.IFilterAgeName(xLocalization.xGlobal.LocalizeAgeName(Uni(spawnpoint.getTitle()))))
            fullLinkName.append(displayName)
            if (len(displayName) > kMaxDisplayableChars):
                displayName = (displayName[:kMaxDisplayableChars] + u'...')
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setStringW(displayName)
            try:
                dniCoords = cityLink.getCreateAgeCoords()
                stringLinkInfo = (u'%05d%   04d%   04d' % (dniCoords.GetTorans(), dniCoords.getHSpans(), dniCoords.getVSpans()))
            except:
                stringLinkInfo = (u'%05d%   04d%   04d' % (0, 0, 0))
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setStringW(stringLinkInfo)
            if (ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).getStringW() == Uni(xLocalization.xGlobal.LocalizeAgeName(u'Ferry Terminal'))):
                idTextbox = (idTextbox + 10)
            else:
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox + 99))).show()
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox + 99))).enable()
                idTextbox = (idTextbox + 10)


    def IUpdateGZLinks(self):
        global numGZLinks
        global GZLinkNode
        numGZLinks = 0
        GZLinkNode = self.IGetGZLinkNode()
        spawnpoints = []
        if (not (GZLinkNode == None)):
            spawnpoints = GZLinkNode.getSpawnPoints()
        else:
            return
        index = (numCityLinks - 1)
        idTextbox = (kIDTxtLinkName01 + (len(untranslatedName) * 10))
        for spawnpoint in spawnpoints:
            if (spawnpoint.getName() == 'BigRoomLinkInPoint'):
                index = (index + 1)
                numGZLinks = (numGZLinks + 1)
                if (index < indexDisplayStart):
                    continue
                if (index > ((indexDisplayStart + kNumDisplayFields) - 1)):
                    break
                if (idBookPresented == (idTextbox - 1)):
                    ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).disable()
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorPresented)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorPresented)
                else:
                    ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).enable()
                    if (idLinkSelected == (idTextbox - 1)):
                        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorSelected)
                        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorSelected)
                    else:
                        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorNormal)
                        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorNormal)
                untranslatedName.append(Uni(spawnpoint.getTitle()))
                displayName = Uni(self.IFilterAgeName(xLocalization.xGlobal.LocalizeAgeName(unicode(spawnpoint.getTitle()))))
                fullLinkName.append(displayName)
                if (len(displayName) > kMaxDisplayableChars):
                    displayName = (displayName[:kMaxDisplayableChars] + u'...')
                dniCoords = GZLinkNode.getCreateAgeCoords()
                try:
                    stringLinkInfo = (u'%05d%   04d%   04d' % (dniCoords.GetTorans(), dniCoords.getHSpans(), dniCoords.getVSpans()))
                except:
                    stringLinkInfo = (u'%05d%   04d%   04d' % (0, 0, 0))
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setStringW(displayName)
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setStringW(stringLinkInfo)
                idTextbox = (idTextbox + 10)
                return # there's never more than one GZ link


    def IUpdateHoodLinks(self):
        hoodLinks = []
        BevinNode = self.IGetBevinLinkNode()
        KirelNode = self.IGetKirelLinkNode()
# KveerMOUL BEGIN
        KveerNode = self.IGetKveerMOULLinkNode()
# KveerMOUL END
        if (BevinNode != None):
            spawnpoints = BevinNode.getSpawnPoints()
            for spawnpoint in spawnpoints:
                if (spawnpoint.getName() == 'LinkInPointBevinDummy'):
                    hoodLinks.append('Bevin')
        if (KirelNode != None):
            spawnpoints = KirelNode.getSpawnPoints()
            for spawnpoint in spawnpoints:
                if (spawnpoint.getName() == 'LinkInPointKirelDummy'):
                    hoodLinks.append('Kirel')
# Magic Hoods BEGIN
        for hood in MagicHoods.keys():
            if xLinkMgr.IsAgeAvailable(hood):
                hoodLinks.append(hood)
# Magic Hoods END
# KveerMOUL BEGIN
        if (KveerNode != None):
            spawnpoints = KveerNode.getSpawnPoints()
            for spawnpoint in spawnpoints:
                if (spawnpoint.getName() == 'LinkInPointKveerDummy'):
                    hoodLinks.append('New Kveer')
# KveerMOUL END

        if (indexDisplayStart > 0):
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollUp)).show()
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollUp)).enable()
        numLinks = ((len(hoodLinks) + numCityLinks) + numGZLinks)
        if (numLinks > (kNumDisplayFields + indexDisplayStart)):
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollDn)).show()
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollDn)).enable()
        index = ((numCityLinks + numGZLinks) - 1)
        idTextbox = (kIDTxtLinkName01 + (len(untranslatedName) * 10))
        for link in hoodLinks:
            index = (index + 1)
            if (index < indexDisplayStart):
                continue
            if (index > ((indexDisplayStart + kNumDisplayFields) - 1)):
                break
            if (idBookPresented == (idTextbox - 1)):
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).disable()
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorPresented)
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorPresented)
            else:
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).enable()
                if (idLinkSelected == (idTextbox - 1)):
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorSelected)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorSelected)
                else:
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorNormal)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorNormal)
            untranslatedName.append(Uni(link))
            displayName = Uni(self.IFilterAgeName(xLocalization.xGlobal.LocalizeAgeName(link)))
# Magic Hoods BEGIN
            if link in MagicHoods:
                displayName = Uni(xLinkMgr.GetInstanceName(link))
# Magic Hoods END
            fullLinkName.append(displayName)
            if (len(displayName) > kMaxDisplayableChars):
                displayName = (displayName[:kMaxDisplayableChars] + u'...')
            if (link == 'Bevin'):
                dniCoords = BevinNode.getCreateAgeCoords()
            elif (link == 'Kirel'):
                dniCoords = KirelNode.getCreateAgeCoords()
# KveerMOUL BEGIN
            elif (link == 'New Kveer'):
                dniCoords = KveerNode.getCreateAgeCoords()
# KveerMOUL END
            try:
                stringLinkInfo = (u'%05d%   04d%   04d' % (dniCoords.GetTorans(), dniCoords.getHSpans(), dniCoords.getVSpans()))
            except:
                stringLinkInfo = (u'%05d%   04d%   04d' % (0, 0, 0))
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setStringW(displayName)
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setStringW(stringLinkInfo)
            idTextbox = (idTextbox + 10)


    def IUpdateDynLinks(self):
        global statusBarText, dynLinkSortBy, dynLinkReverse
        if (idCategorySelected == kIDBtnLinkCategory03):
            dynLinks = xLinkMgr.GetPublicAges(dynLinkSortBy, dynLinkReverse)
        else:
            dynLinks = xLinkMgr.GetRestorationAges(dynLinkSortBy, dynLinkReverse)
        if xxConfig.isOnline():
            statusBarText = u'Ages displayed in darker color are those you have not yet visited'
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkDescription)).setStringW(statusBarText)
        if (indexDisplayStart > 0):
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollUp)).show()
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollUp)).enable()
        numLinks = len(dynLinks)
        if (numLinks > (kNumDisplayFields + indexDisplayStart)):
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollDn)).show()
            ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollDn)).enable()
        index = -1
        idTextbox = kIDTxtLinkName01
        for ageName in dynLinks:
            index = (index + 1)
            if (index < indexDisplayStart):
                continue
            if (index > ((indexDisplayStart + kNumDisplayFields) - 1)):
                break
            if (idBookPresented == (idTextbox - 1)):
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).disable()
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorPresented)
                ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorPresented)
            else:
                ptGUIControlButton(NexusGUI.dialog.getControlFromTag((idTextbox - 1))).enable()
                if (idLinkSelected == (idTextbox - 1)):
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorSelected)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorSelected)
                elif idCategorySelected != kIDBtnLinkCategory03 and not os.path.exists('dat\\%s.age' % ageName):
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorMarked)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorMarked)
                else:
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setForeColor(colorNormal)
                    ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setForeColor(colorNormal)
            untranslatedName.append(Uni(ageName))
            displayName = xLinkMgr.GetInstanceName(ageName)
            fullLinkName.append(Uni(displayName))
            if (len(displayName) > kMaxDisplayableChars):
                displayName = (displayName[:kMaxDisplayableChars] + '...')
            lastUpdate = xLinkMgr.GetAgeLastUpdate(ageName)
            if lastUpdate is None: stringLinkInfo = ''
            else: stringLinkInfo = time.strftime(xLocalization.xGlobal.xDateFormat, lastUpdate)
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(idTextbox)).setString(displayName)
            ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag((idTextbox + 1))).setString(stringLinkInfo)
            idTextbox = (idTextbox + 10)


    def IGetFullName(self, controlID):
        if ((controlID == kIDTxtNeighborhoodName) or (controlID == kIDBtnNeighborhoodSelect)):
            return fullNeighborhoodName
        index = (controlID - 210)
        index /= 10
        if (index < len(fullLinkName)):
            return fullLinkName[index]
        else:
            return u''


    def IGetUntranslatedName(self, controlID):
        if ((controlID == kIDTxtNeighborhoodName) or (controlID == kIDBtnNeighborhoodSelect)):
            return untranslatedNeighborhoodName
        index = (controlID - 210)
        index /= 10
        if (index < len(untranslatedName)):
            return untranslatedName[index]
        else:
            return u''


    def ILink(self):
        vault = ptVault()
        if (type(vault) == type(None)):
            PtDebugPrint('nxusBookMachine.ILink:\tplayer vault type None')
            return
        if (idBookPresented == 0):
            PtDebugPrint('Ignoring link request since idBookPresented is 0 (which is invalid)')
            return
        if (idBookPresented == kIDBtnNeighborhoodSelect):
            folder = vault.getAgesIOwnFolder()
            PtAssert(folder, 'vault.getAgesIOwnFolder return bad')
            contents = folder.getChildNodeRefList()
            for content in contents:
                link = content.getChild()
                link = link.upcastToAgeLinkNode()
                if (type(link) != type(None)):
                    info = link.getAgeInfo()
                else:
                    link = content.getChild()
                    info = link.upcastToAgeInfoNode()
                if (type(info) == type(None)):
                    continue
                if (info.getAgeFilename() == 'Neighborhood'):
                    als = link.asAgeLinkStruct()
                    als.setLinkingRules(PtLinkingRules.kOwnedBook)
                    linkMgr = ptNetLinkingMgr()
                    linkMgr.linkToAge(als)
                    return
            print "nxusBookMachine.ILink:\tERROR--couldn't find link to player's neighborhood in player's Vault"
            return
        folder = None
        if (idCategorySelected == kIDBtnLinkCategory01):
            index = (idBookPresented + 1)
            index = (index - 210)
            index /= 10
            index = index+indexDisplayStart
            PtDebugPrint(((((('index: ' + str(index)) + ' numCityLinks: ') + str(numCityLinks)) + ' numGZLinks: ') + str(numGZLinks)))
            if (index < numCityLinks):
                self.ILinkToCity()
            elif (index < (numCityLinks + numGZLinks)):
                self.ILinkToGZ()
            else:
                self.ILinkToHood()
            return
        elif (idCategorySelected in dynLinkCategories):
            self.ILinkToDynAge(self.IGetUntranslatedName((idBookPresented + 1)))
            return
        elif (idCategorySelected == kIDBtnLinkCategory02):
            folder = vault.getAgesICanVisitFolder()
        elif (idCategorySelected == kIDBtnLinkCategory04):
            folder = vault.getAgesIOwnFolder()
        if (type(folder) == type(None)):
            PtDebugPrint('nxusBookMachine.ILink:\tWARNING link folder type None')
            return
        contents = folder.getChildNodeRefList()
        clickedLinkName = self.IGetUntranslatedName((idBookPresented + 1))
        #PtDebugPrint(u'nxusBookMachine.ILink():\tattempting link to ' + clickedLinkName) # removed this line due to unicode problems
        if (not clickedLinkName):
            PtDebugPrint('Link name is empty, aborting link')
            return
        for content in contents:
            link = content.getChild()
            link = link.upcastToAgeLinkNode()
            if (type(link) != type(None)):
                info = link.getAgeInfo()
            else:
                link = content.getChild()
                info = link.upcastToAgeInfoNode()
            if (type(info) == type(None)):
                continue
            if (idCategorySelected == kIDBtnLinkCategory01):
                thisLinkName = Uni(info.getAgeFilename())
            else:
                thisLinkName = Uni(info.getDisplayName())
            if (thisLinkName == clickedLinkName):
                print '-- found link node --'
                if isinstance(link, ptVaultAgeLinkNode):
                    als = link.asAgeLinkStruct()
                else:
                    als = ptAgeLinkStruct()
                    als.setAgeInfo(info.asAgeInfoStruct())
                if (idCategorySelected == kIDBtnLinkCategory02):
                    als.setLinkingRules(PtLinkingRules.kVisitBook)
                elif (idCategorySelected == kIDBtnLinkCategory04):
                    als.setLinkingRules(PtLinkingRules.kOwnedBook)
                else:
                    als.setLinkingRules(PtLinkingRules.kBasicLink)
                print '-- linking --'
                linkMgr = ptNetLinkingMgr()
                linkMgr.linkToAge(als)
                return
        #PtDebugPrint(("nxusBookMachine.ILink():\tWARNING--couldn't find link to %s in player's Vault" % clickedLinkName)) # removed this line due to unicode problems
        return


    def ILinkToCity(self):
        vault = ptVault()
        if (type(vault) == type(None)):
            PtDebugPrint('nxusBookMachine.ILinkToCity:\tplayer vault type None')
            return
        spawnpointtitle = self.IGetUntranslatedName((idBookPresented + 1))
        PtDebugPrint(("nxusBookMachine.ILinkToCity():\tattempting link to city's %s" % spawnpointtitle))
        CityLinkNode = self.IGetCityLinkNode()
        if (CityLinkNode == None):
            PtDebugPrint("nxusBookMachine.ILinkToCity():\tWARNING couldn't find city link, so faking it (and linking to Ferry Terminal)")
            info = ptAgeInfoStruct()
            info.setAgeFilename('city')
            als = ptAgeLinkStruct()
            als.setAgeInfo(info)
            als.setLinkingRules(PtLinkingRules.kOwnedBook)
            spawnpoint = ptSpawnPointInfo()
            spawnpoint.setName('LinkInPointFerry')
            spawnpoint.setTitle('Ferry Terminal')
            als.setSpawnPoint(spawnpoint)
            linkMgr = ptNetLinkingMgr()
            linkMgr.linkToAge(als)
            return
        else:
            als = CityLinkNode.asAgeLinkStruct()
            als.setLinkingRules(PtLinkingRules.kOwnedBook)
            spawnpoints = CityLinkNode.getSpawnPoints()
            foundspawnpoint = false
            for spawnpoint in spawnpoints:
                if (spawnpoint.getTitle() == spawnpointtitle):
                    print '-- found spawn point --'
                    als.setSpawnPoint(spawnpoint)
                    foundspawnpoint = true
            if (not foundspawnpoint):
                PtDebugPrint(("nxusBookMachine.ILinkToCity():\tWARNING couldn't find city spawn point for %s" % spawnpointtitle))
                if (spawnpointtitle == 'Ferry Terminal'):
                    PtDebugPrint('nxusBookMachine.ILinkToCity():\tFaking a Ferry Terminal link')
                    spawnpoint = ptSpawnPointInfo()
                    spawnpoint.setName('LinkInPointFerry')
                    spawnpoint.setTitle('Ferry Terminal')
                    als.setSpawnPoint(spawnpoint)
                    foundspawnpoint = true
                else:
                    return
            print '-- linking --'
            linkMgr = ptNetLinkingMgr()
            linkMgr.linkToAge(als)


    def ILinkToGZ(self):
        spawnpointtitle = self.IGetUntranslatedName((idBookPresented + 1))
        PtDebugPrint(("nxusBookMachine.ILinkToGZ():\tattempting link to great zero's %s" % spawnpointtitle))
        if (GZLinkNode == None):
            PtDebugPrint("nxusBookMachine.ILinkToGZ():\tWARNING couldn't find great zero link node! Aborting link")
            return
        als = GZLinkNode.asAgeLinkStruct()
        als.setLinkingRules(PtLinkingRules.kOwnedBook)
        spawnpoints = GZLinkNode.getSpawnPoints()
        foundspawnpoint = false
        for spawnpoint in spawnpoints:
            if (spawnpoint.getTitle() == spawnpointtitle):
                print '-- found spawn point --'
                als.setSpawnPoint(spawnpoint)
                foundspawnpoint = true
        if (not foundspawnpoint):
            PtDebugPrint(("nxusBookMachine.ILinkToGZ():\tWARNING couldn't find great zero spawn point for %s" % spawnpointtitle))
            return
        print '-- linking --'
        linkMgr = ptNetLinkingMgr()
        linkMgr.linkToAge(als)


    def ILinkToHood(self):
        hoodName = self.IGetUntranslatedName((idBookPresented + 1))
        PtDebugPrint(('nxusBookMachine.ILinkToHood():\tattempting link to hood named %s' % hoodName))
# Magic Hoods BEGIN
        if hoodName in MagicHoods:
            xLinkMgr.LinkToAge(str(hoodName), str(MagicHoods[hoodName]))
            return
# Magic Hoods END
        if (hoodName == 'Bevin'):
            hoodLinkNode = self.IGetBevinLinkNode()
        elif (hoodName == 'Kirel'):
            hoodLinkNode = self.IGetKirelLinkNode()
# KveerMOUL BEGIN
        elif (hoodName == 'New Kveer'):
            hoodLinkNode = self.IGetKveerMOULLinkNode()
# KveerMOUL END
        if (hoodLinkNode == None):
            PtDebugPrint("nxusBookMachine.ILinkToHood():\tERROR couldn't find hood link node! Aborting link")
            return
        als = hoodLinkNode.asAgeLinkStruct()
        als.setLinkingRules(PtLinkingRules.kOwnedBook)
        print '-- linking --'
        linkMgr = ptNetLinkingMgr()
        linkMgr.linkToAge(als)


    def ILinkToDynAge(self, ageName):
        xLinkMgr.LinkToAge(str(ageName))


    def IDisableGUIButtons(self):
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink01)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink02)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink03)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink04)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink05)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink06)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink07)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnDeleteLink08)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect01)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect02)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect03)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect04)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect05)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect06)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect07)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkSelect08)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodCreate)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodSelect)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnNeighborhoodPublic)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkCategory01)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkCategory02)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkCategory03)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnLinkCategory04)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollDn)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDBtnScrollUp)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDNameHeaderBtn)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDPopHeaderBtn)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDNameAscArrow)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDNameDescArrow)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDPopAscArrow)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDPopDescArrow)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDEngCheckBox)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDFreCheckBox)).disable()
        ptGUIControlButton(NexusGUI.dialog.getControlFromTag(kIDGerCheckBox)).disable()
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo01)).setNotifyOnInteresting(0)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo02)).setNotifyOnInteresting(0)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo03)).setNotifyOnInteresting(0)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo04)).setNotifyOnInteresting(0)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo05)).setNotifyOnInteresting(0)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo06)).setNotifyOnInteresting(0)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo07)).setNotifyOnInteresting(0)
        ptGUIControlTextBox(NexusGUI.dialog.getControlFromTag(kIDTxtLinkInfo08)).setNotifyOnInteresting(0)
        return


    def IDeleteLink(self):
        global idBookPresented
        global boolGetBookAfterBtnPress
        global boolBookPresented
        global boolGetBookBtnUp
        global boolGetBookAfterBookRetract
        global idLinkSelected
        actLink.disable()
        stringDeleteCandidateName = self.IGetUntranslatedName(idDeleteCandidateName)
        vault = ptVault()
        if (type(vault) == type(None)):
            PtDebugPrint('nxusBookMachine.IDeleteLink:\tplayer vault type None')
            return
        vault = ptVault()
        if (idCategorySelected == kIDBtnLinkCategory01):
            cityLink = vault.getLinkToCity()
            spawnPoints = cityLink.getSpawnPoints()
            deletionCompleted = 0
            for spawnPoint in spawnPoints:
                if (spawnPoint.getTitle() == stringDeleteCandidateName):
                    PtDebugPrint(('Deleting link to ' + stringDeleteCandidateName))
                    cityLink.removeSpawnPoint(spawnPoint)
                    cityLink.save()
                    deletionCompleted = 1
                    break
            if (not deletionCompleted):
                if (GZLinkNode == None):
                    PtDebugPrint("No GZ Link node, so we aren't deleting a GZ link...")
                else:
                    spawnPoints = GZLinkNode.getSpawnPoints()
                    for spawnPoint in spawnPoints:
                        if (spawnPoint.getTitle() == stringDeleteCandidateName):
                            PtDebugPrint(('Deleting link to ' + stringDeleteCandidateName))
                            GZLinkNode.removeSpawnPoint(spawnPoint)
                            GZLinkNode.save()
                            deletionCompleted = 1
        elif (idCategorySelected == kIDBtnLinkCategory02):
            folder = vault.getAgesICanVisitFolder()
            contents = folder.getChildNodeRefList()
            for content in contents:
                linkNode = content.getChild()
                linkNode = linkNode.upcastToAgeLinkNode()
                if (type(linkNode) == type(None)):
                    linkNode = content.getChild()
                    info = linkNode.upcastToAgeInfoNode()
                else:
                    info = linkNode.getAgeInfo()
                if (type(info) == type(None)):
                    continue
                if (stringDeleteCandidateName == Uni(info.getDisplayName())):
                    #PtDebugPrint(('Deleting link to ' + stringDeleteCandidateName)) # removed this line due to Unicode problems
                    guid = info.getAgeInstanceGuid()
                    vault.unRegisterVisitAge(guid)
                    break
        else:
            PtDebugPrint('nxusBookMachine.IDeleteLink:\tdeletion of this link type not supported')
        if ((idDeleteCandidateName - 1) == idBookPresented):
            respBookRetract.run(self.key)
            boolGetBookAfterBookRetract = false
            boolBookPresented = false
            idBookPresented = 0
        if ((idDeleteCandidateName - 1) == idLinkSelected):
            respButtonPress.run(self.key)
            boolGetBookBtnUp = false
            boolGetBookAfterBtnPress = false
            idLinkSelected = 0
            return
        if ((idDeleteCandidateName - 1) < idLinkSelected):
            idLinkSelected = (idLinkSelected - 10)
        if ((idDeleteCandidateName - 1) < idBookPresented):
            idBookPresented = (idBookPresented - 10)
        self.IUpdateLinks()
        return


    def IDrawLinkPanel(self):
        for objPanel in objlistLinkPanels.value:
            objPanel.draw.disable()
        ageName = self.IGetUntranslatedName((idBookPresented + 1))
        if (ageName == u'New Kveer'):
            ageName = u'KveerMOUL'
        elif (idBookPresented == kIDBtnNeighborhoodSelect):
            ageName = 'Neighborhood'
        elif ((idCategorySelected == kIDBtnLinkCategory02) or (idCategorySelected == kIDBtnLinkCategory04)):
            vault = ptVault()
            if (idCategorySelected == kIDBtnLinkCategory02):
                folder = vault.getAgesICanVisitFolder()
            else:
                folder = vault.getAgesIOwnFolder()
            contents = folder.getChildNodeRefList()
            for content in contents:
                linkNode = content.getChild()
                linkNode = linkNode.upcastToAgeLinkNode()
                if (type(linkNode) != type(None)):
                    info = linkNode.getAgeInfo()
                else:
                    linkNode = content.getChild()
                    info = linkNode.upcastToAgeInfoNode()
                if (type(info) == type(None)):
                    continue
                if (ageName == Uni(info.getDisplayName())):
                    ageName = Uni(info.getAgeFilename())
                    break
        panelName = (u'LinkPanel_' + ageName)
        if (ageName == 'Tokotah Alley'):
            panelName = u'LinkPanel_Dakotah Alley'
        elif (ageName == 'Bevin'):
            panelName = u'LinkPanel_Neighborhood'
        elif ((ageName == 'GreatZero Observation') or ((idCategorySelected == kIDBtnLinkCategory04) and (ageName == 'GreatZero'))):
            panelName = u'LinkPanel_Great Zero Observation'
        elif (ageName in ['GreatZero', 'Great Zero']):
            panelName = u'LinkPanel_Great Zero'
        PtDebugPrint(('drawing link panel: %s' % panelName))
        for objPanel in objlistLinkPanels.value:
            PtDebugPrint(('name: ' + objPanel.getName()))
            if (objPanel.getName() == panelName):
                objPanel.draw.enable()
                return
        #Dustin
        import booksDustGlobal
        print 'nxusBookMachine.IDrawLinkPanel():\tThe Nexus is trying to read a linking image from a file...'
        image = xLinkMgr.GetLinkingImage(str(ageName), width=512, height=512)
        print 'nxusBookMachine.IDrawLinkPanel():\t image='+`image`
        booksDustGlobal.ImagerMap.textmap.drawImage(0, 0, image, 0)
        #booksDustGlobal.ImagerMap.textmap.flush()
        #/Dustin
        return


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



