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
MaxVersionNumber = 56
MinorVersionNumber = 50
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
from HTMLParser import *
import xLocalization
import xKIExtChatCommands
import time
import string
import xCensor
import xLinkingBookDefs
import xBookGUIs
import whrandom
import glob
import os
from xPsnlVaultSDL import *
# new imports
import re
import math
import xUserKI
import xLinkMgr
import xxConfig
# make it work offline just like online
def PtIsSinglePlayerMode(): return False

#Jalak
kJalakMiniIconBtn = 1200
kJalakRandomBtn = 1201
kJalakExtremeBtn = 1202
kJalakWallToggleBtn = 1203
kJalakColumnsLowBtn = 1204
kJalakColumnsMedBtn = 1205
kJalakColumnsHighBtn = 1206
kJalakRampBtn = 1207
kJalakSphereBtn = 1208
kJalakBigBoxBtn = 1209
kJalakLilBoxBtn = 1210
kJalakRectangleBtn = 1211
kJalakDestroyBtn = 1212
JalakBtnStates = [str(kJalakRandomBtn), str(kJalakExtremeBtn), str(kJalakWallToggleBtn), str(kJalakColumnsLowBtn), str(kJalakColumnsMedBtn), str(kJalakColumnsHighBtn), str(kJalakRampBtn), str(kJalakSphereBtn), str(kJalakBigBoxBtn), str(kJalakLilBoxBtn), str(kJalakRectangleBtn), str(kJalakDestroyBtn)]
#/Jalak
KIBlackbar = ptAttribGUIDialog(1, 'The Blackbar dialog')
KIMini = ptAttribGUIDialog(2, 'The KIMini dialog')
KIYesNo = ptAttribGUIDialog(3, 'The KIYesNo dialog')
BigKI = ptAttribGUIDialog(5, 'The BIG KI (Mr. BigStuff)')
NewItemAlert = ptAttribGUIDialog(7, 'The new item alert dialog')
KIListModeDialog = ptAttribGUIDialog(9, 'The list mode dialog')
KIPictureExpanded = ptAttribGUIDialog(10, 'The Picture expanded dialog')
KIJournalExpanded = ptAttribGUIDialog(11, 'The journal entry expanded dialog')
KIOnAnim = ptAttribAnimation(12, 'Turn on/off the KI on animation')
KIOnResp = ptAttribResponder(13, 'Turn On responder')
KIOffResp = ptAttribResponder(14, 'Turn Off responder')
KIPlayerExpanded = ptAttribGUIDialog(17, 'The player expanded dialog')
KIMicroBlackbar = ptAttribGUIDialog(18, 'The micro Blackbar dialog')
KIMicro = ptAttribGUIDialog(19, 'The micro KI dialog')
KINanoBlackBar = ptAttribGUIDialog(20, 'The nano Blackbar dialog')
KIVolumeExpanded = ptAttribGUIDialog(21, 'The volume control dialog')
KIAgeOwnerExpanded = ptAttribGUIDialog(22, 'The Age Owner settings dialog')
KIRateIt = ptAttribGUIDialog(23, 'The Rate It dialog')
KISettings = ptAttribGUIDialog(24, 'The KI settings dialog')
KIMarkerFolderExpanded = ptAttribGUIDialog(27, 'The Marker Folder dialog')
KIMarkerFolderPopupMenu = ptAttribGUIPopUpMenu(28, 'The MarkerFolder Time Popup Menu')
KIQuestionNote = ptAttribGUIDialog(29, 'The Question Note dialog')
KIMarkerTypePopupMenu = ptAttribGUIPopUpMenu(30, 'The MarkerFolder Type Popup Menu')
#Jalak
KIJalakMiniIconOn = ptAttribResponder(31, "Jalak KIMini icon 'on/off' resp", ['on', 'off'])
KIJalakGUIDialog = ptAttribGUIDialog(32, 'The Jalak GUI dialog')
KIJalakGUIOpen = ptAttribResponder(33, "Jalak GUI 'open' resp")
KIJalakGUIClose = ptAttribResponder(34, "Jalak GUI 'close' resp")
KIJalakBtnLights = ptAttribResponder(35, 'Jalak GUI btn lights resp', statelist=JalakBtnStates, netForce=0)
#/Jalak
#Dustin
ImagerMap = ptAttribDynamicMap(90, 'The Dynamic Texture Map')
BookMapLeft = ptAttribDynamicMap(91, 'The Dynamic Texture Map l')
BookMapRight = ptAttribDynamicMap(92, 'The Dynamic Texture Map r')
BookMapBack = ptAttribDynamicMap(93, 'The Dynamic Texture Map b')
BookMapFront = ptAttribDynamicMap(94, 'The Dynamic Texture Map f')
bhrLinkPanelMap = ptAttribDynamicMap(95, 'The Dynamic Texture Map b')
bhrShareButtonMap = ptAttribDynamicMap(96, 'The Dynamic Texture Map f')
#/Dustin
KIGUIInitialized = 0
#Jalak
AgeName = ''
JalakGUIState = 0
kLightStopID = 7
kJalakBtnDelayTimer = 8
kSphere = 'Sphere'
kLilBox = 'LilBox'
kBigBox = 'BigBox'
kRamp = 'Ramp'
kRect = 'Rect'
kJalakBtnDelaySeconds = 0.40000000000000002
jlakGUIButtons = []
kJalakPythonComponent = 'cPythField'
JalakScript = None
#/Jalak
#Pellets
kPelletScoreButton = 1020
#/Pellets
#MOUL marker buttons
kminiMGNewMarker = 1010
kminiMGNewGame = 1011
kminiMGInactive = 1012
#/MOUL marker buttons
IAmAdmin = 0
UserList = []
PlayerInfoName = None
IKIDisabled = 0
IKIHardDisabled = 0
IminiKIWasUp = 0
WaitingForAnimation = 0
LastPrivatePlayerID = None
ToReplyToLastPrivatePlayerID = None
CCRConversationInProgress = 0
WeAreTakingAPicture = 0
ChatLogFile = None
ISawTheKIAtleastOnce = 0
IsPlayingLookingAtKIMode = 0
PhasedKICreateNotes = 1
PhasedKICreateImages = 1
PhasedKIShareYeeshaBook = 0 # physics are broken after the link
PhasedKIInterAgeChat = 1
PhasedKINeighborsInDPL = 1
PhasedKIBuddies = 1
PhasedKIPlayMarkerGame = 1
PhasedKICreateMarkerGame = 1 # changed from 0 in UU
PhasedKISendNotes = 1
PhasedKISendImages = 1
PhasedKISendMarkerGame = 1 # changed from 0 in UU
PhasedKIShowMarkerGame = 1 # changed from 0 in UU
##############################################################################
# D'Lanor's Alcugs GPS fix
##############################################################################
gShowGPSCheat = 0
##############################################################################
# End D'Lanor's Alcugs GPS fix
##############################################################################
kFadeTimer = 1
kBKITODCheck = 2
kAlertHideTimer = 3
kTakeSnapShot = 4
kMarkerGameTimer = 5
if xxConfig.isOffline():
    kMaxPictures = 60 # the offline vault has problems with large amount of pictures, so DON'T INCREASE THIS!
    kMaxNotes = 500
    kMaxMarkerFolders = 500
    kMaxMarkers = 2000
else:
    kMaxPictures = 50
    kMaxNotes = 100
    kMaxMarkerFolders = 100
    kMaxMarkers = 300
NumberOfPictures = 0
NumberOfNotes = 0
NumberOfMarkerFolders = 0
NumberOfMarkers = 0
kJournalTextSize = 2048
theKILevel = kNanoKI
PrivateChatChannel = 0
theCensorLevel = 0
OnlyGetPMsFromBuddies = 0
OnlyAllowBuddiesOnRequest = 0
gKIMarkerLevel = 0
kContentListScrollSize = 5
gAlreadyCheckedCGZGame = 0
gKIHasJournal = 0
kChronicleFontSize = 'PlayerKIFontSize'
kChronicleFontSizeType = 2
kChronicleFadeTime = 'PlayerKIFadeTime'
kChronicleFadeTimeType = 2
kChronicleOnlyPMs = 'PlayerKIOnlyPMsBuddies'
kChronicleOnlyPMsType = 2
kChronicleBuddiesOnRequest = 'PlayerKIBuddiesOnRequest'
kChronicleBuddiesOnRequestType = 2
kChronCGZPlaying = 'CGZPlaying'
kChronicleHasJournal = 'PlayerKIHasJournal'
kChronicleHasJournalType = 2
kMiniMaximizeRGID = 34
kExitButtonID = 4
kPlayerBookCBID = 15
kJournalBookCBID = 35
kBBCCRButtonID = 200
kmicroChatButton = 100
kRolloverLeftID = 998
kRolloverRightID = 999
kChatCaretID = 12
kChatEditboxID = 5
kChatDisplayArea = 70
kFolderPlayerList = 30
kPlayerList = 31
kminiToggleBtnID = 1
kminiPutAwayID = 4
kminiTakePicture = 60
kminiMuteAll = 61
kminiPrivateToggle = 62
kminiCreateJournal = 63
kminiDragBar = 50
kminiChatScrollUp = 51
kminiChatScrollDown = 52
kminiPlayerListUp = 53
kminiPlayerListDown = 54
kmini7Indicator1 = 71
kmini7Indicator2 = 72
kmini7Indicator3 = 73
kmini7Indicator4 = 74
kminiMarkerIndicator01 = 601
kminiMarkerIndicatorLast = 625
gMarkerColors = {
    'off': 0.0,
    'redlt': 1.5,
    'red': 3.5,
    'yellowlt': 6.0,
    'yellow': 8.5,
    'purplelt': 11.0,
    'purple': 13.5,
    'greenlt': 16.0,
    'green': 18.5
}
kminiGZDrip = 700
kminiGZActive = 701
kminiGZMarkerGameActive = 702
kminiGZMarkerInRange = 703
kMaxChatSize = 2048
kMaxNumChatItems = 50
kStartNumChatItems = 9
kStartOffScreenLine = 0
kChatBlankLine = '  \n'
kChatSelfMsg = 1
kChatBroadcastMsg = 2
kChatPrivateMsg = 3
kChatAdminBroadcastMsg = 4
kChatAdminPrivateMsg = 5
kChatPrivateMsgSelf = 6
kChatOfferLink = 7
kChatSystemMessage = 8
kChatInterAge = 9
kChatInterAgeSelf = 10
kChatCCRMessage = 11
kChatCCRMessageSelf = 12
kChatCCRMessageFromPlayer = 13
kFadeNotActive = 0
kFadeFullDisp = 1
kFadeDoingFade = 2
kFadeStopping = 3
FadeMode = kFadeNotActive
MiniKIFirstTimeShow = 1
FadeEnableFlag = 1
CurrentFadeTick = 0
TicksOnFull = 30
kFadeTimeMax = 120
kFullTickTime = 1.0
TicksOnFade = 4
kFadeTickTime = 0.2
OriginalForeAlpha = 1.0
OriginalSelectAlpha = 1.0
OriginalminiKICenter = None
LastminiKICenter = None
FontSizeList = [7, 8, 10, 12, 14]
PreviousTime = '20:20'
TimeBlinker = 1
gFeather = 0
gImageDirectory = 'KIimages'
gImageFileNameTemplate = 'KIimage'
gImageFileSearch = (((('.\\' + gImageDirectory) + '\\') + gImageFileNameTemplate) + '*.jpg')
gLastImageFileNumber = 0
gJournalBookFilePath = '.\\MyJournals\\'
gJournalBookFileExt = 'Journal.html'
BKPlayerList = []
BKPlayerSelected = None
PreviouslySelectedPlayer = None
BKJournalFolderDict = {}
BKJournalListOrder = []
BKJournalFolderSelected = 0
BKJournalFolderTopLine = 0
BKPlayerFolderDict = {}
BKPlayerListOrder = []
BKPlayerFolderSelected = 0
BKPlayerFolderTopLine = 0
BKConfigFolderDict = {}
BKConfigListOrder = [xLocalization.xKI.xKIConfiguration]
BKConfigDefaultListOrder = [xLocalization.xKI.xKIConfiguration]
BKConfigFolderSelected = 0
BKConfigFolderTopLine = 0
BKFolderLineDict = BKJournalFolderDict
BKFolderListOrder = BKJournalListOrder
BKFolderSelected = BKJournalFolderSelected
BKFolderTopLine = BKJournalFolderTopLine
BKFolderSelectChanged = 0
BKIncomingFolder = None
BKNewItemsInInbox = 0
FolderOfDevices = None
BKCurrentContent = None
BKContentList = []
BKContentListTopLine = 0
BKInEditMode = 0
BKEditContent = None
BKEditField = -1
BKGettingPlayerID = 0
kBKListMode = 1
kBKJournalExpanded = 2
kBKPictureExpanded = 3
kBKPlayerExpanded = 4
kBKVolumeExpanded = 5
kBKAgeOwnerExpanded = 6
kBKKIExpanded = 7
kBKMarkerListExpanded = 8
kBKQuestionNote = 9
BKRightSideMode = kBKListMode
kBKToggleMiniID = 14
kBKIPutAwayID = 4
kBKFolderUpLine = 66
kBKFolderDownLine = 67
kBKLMUpButton = 110
kBKLMDownButton = 111
kBKDisabledPeopleButton = 300
kBKDisabledGearButton = 301
kBKICurAgeNameID = 60
kBKICurTimeID = 61
kBKIGPS1TextID = 62
kBKIGPS2TextID = 63
kBKIGPS3TextID = 64
kBKPlayerListID = 65
kBKRadioModeID = 68
kBKPlayerName = 200
kBKPlayerID = 201
kBKNeighborhoodAndID = 59
kBKIIncomingBtn = 70
kBKIFolderLineBtn01 = 71
kBKIFolderLineBtnLast = 78
kBKIToPlayerButton = 80
kBKIToIncomingButton = 81
kBKIToFolderButton01 = 82
kBKIToFolderButtonLast = 88
kBKIPlayerLine = 90
kBKIIncomingLine = 91
kBKIFolderLine01 = 92
kBKIFolderLineLast = 98
kLONGBKIIncomingLine = 591
kLONGBKIFolderLine01 = 592
kLONGBKIFolderLineLast = 598
kBKIListModeCreateBtn = 80
kBKIListModeLineBtn01 = 81
kBKIListModeLineBtnLast = 89
kBKILMTitleCreateLine = 101
kBKILMOffsetLine01 = 110
kBKILMOffsetLineLast = 190
kBKILMIconPictureOffset = 0
kBKILMTitleOffset = 1
kBKILMDateOffset = 2
kBKILMFromOffset = 3
kBKILMIconJournalOffset = 4
kBKILMIconPersonOffset = 5
kBKIJRNTitleButton = 80
kBKIJRNNoteButton = 81
kBKIJRNDeleteButton = 82
kBKIJRNTitleEdit = 85
kBKIJRNNoteEdit = 86
kBKIJRNAgeName = 90
kBKIJRNDate = 91
kBKIJRNTitle = 92
kBKIJRNNote = 93
kBKIJRNFrom = 94
kBKIJRNSentDate = 95
kBKIPICTitleButton = 80
kBKIPICDeleteButton = 82
kBKIPICTitleEdit = 85
kBKIPICAgeName = 90
kBKIPICDate = 91
kBKIPICTitle = 92
kBKIPICImage = 93
kBKIPICFrom = 94
kBKIPICSentDate = 95
kBKIImageStartX = 112
kBKIImageStartY = 212
kBKIPLYPlayerIDEditBox = 80
kBKIPLYDeleteButton = 82
kBKIPLYName = 90
kBKIPLYID = 91
kBKIPLYDetail = 92
kBKIKIFontSize = 80
kBKIKIFadeTime = 81
kBKIKIOnlyPM = 90
kBKIKIBuddyCheck = 91
kBKIKISettingsText = 570
kBKIKIFontSizeText = 580
kBKIKIFadeTimeText = 581
kBKIKIOnlyPMText = 590
kBKISoundFXVolSlider = 80
xBKIMusicVolSlider = 81
xBKIVoiceVolSlider = 82
kBKIAmbienceVolSlider = 83
kBKIMicLevelSlider = 84
kBKIGUIVolSlider = 85
kBKAgeOwnerTitleTB = 90
kBKAgeOwnerTitleBtn = 91
kBKAgeOwnerTitleEditbox = 92
kBKAgeOwnerStatusTB = 93
kBKAgeOwnerMakePublicTB = 94
kBKAgeOwnerMakePublicBtn = 95
kBKAgeOwnerGUIDTB = 96
kBKAgeOwnerDescription = 99
kBKAgeOwnerDescriptionTitle = 510
BKAgeOwnerEditDescription = 0
kBKEditIDtextbox = 0
kBKEditIDbutton = 1
kBKEditIDeditbox = 2
BKEditFieldIDs = [
    [kBKIJRNTitle, kBKIJRNTitleButton, kBKIJRNTitleEdit],
    [kBKIJRNNote, kBKIJRNNoteButton, kBKIJRNNoteEdit],
    [kBKIPICTitle, kBKIPICTitleButton, kBKIPICTitleEdit]
]
kBKEditFieldJRNTitle = 0
kBKEditFieldJRNNote = 1
kBKEditFieldPICTitle = 2
Clear = ptColor(0, 0, 0, 0)
AgenBlueDk = ptColor(0.65, 0.6353, 0.745, 1.0)
AgenGreenLt = ptColor(0.8745, 1.0, 0.85, 1.0)
AgenGreenDk = ptColor(0.65, 0.745, 0.6353, 1.0)
DniYellow = ptColor(0.851, 0.812, 0.576, 1.0)
DniCyan = ptColor(0.576, 0.867, 0.851, 1.0)
DniBlue = ptColor(0.78, 0.706, 0.87, 1.0)
DniRed = ptColor(1.0, 0.216, 0.38, 1.0)
DniGreen = ptColor(0.698, 0.878, 0.761, 1.0)
DniGreenDk = ptColor(0.0, 0.596, 0.211, 1.0)
DniPurple = ptColor(0.878, 0.698, 0.819, 1.0)
DniWhite = ptColor().white()
DniShowRed = ptColor(1.0, 0.851, 0.874, 1.0)
DniHideBlue = ptColor(0.78, 0.706, 0.87, 0.3)
DniColorShowBtn = DniShowRed
DniColorGhostBtn = DniHideBlue
ChatMessageColor = DniWhite
ChatHeaderBroadcastColor = DniBlue
ChatHeaderPrivateColor = DniYellow
ChatHeaderCCRColor = DniCyan
ChatHeaderStatusColor = DniBlue
ChatHeaderErrorColor = DniRed
ChatHeaderNeighborsColor = DniPurple
ChatHeaderBuddiesColor = DniGreen
DniSelectableColor = DniGreen
DniSelectedColor = DniWhite
DniStaticColor = DniBlue
kYesNoTextID = 12
kYesButtonID = 10
kNoButtonID = 11
kYesButtonTextID = 60
kNoButtonTextID = 61
kYNQuit = 0
kYNDelete = 1
kYNOfferLink = 2
kYNOutside = 3
kYNKIFull = 4
kYNWanaPlay = 5
kYNNoReason = 6
kYNForceQuit = 7 # added
YNWhatReason = kYNQuit
YNOutsideSender = None
kNotOffering = 0
kOfferee = 1
kOfferer = 2
OfferLinkFromWho = None
OfferedBookMode = 0
BookOfferer = None
PsnlOfferedAgeInfo = None
YeeshaBook = None
IsYeeshaBookEnabled = 1
IsEntireYeeshaBookEnabled = 1
JournalBook = None
gCurBookIsYeesha = 1
AlertTimerActive = 0
kAlertTimeDefault = 10.0
kMaxBookAlertTime = 20.0
AlertTimeToUse = kAlertTimeDefault
kAlertKIAlert = 60
kAlertBookAlert = 61
kAlertJournalAlert = 62
kAlertMicroJournalAlert = 63
kMarkerFolderTitleText = 80
kMarkerFolderTitleBtn = 81
kMarkerFolderTitleEB = 82
kMarkerFolderOwner = 84
kMarkerFolderStatus = 85
kMarkerFolderInvitePlayer = 90
kMarkerFolderEditStartGame = 93
kMarkerFolderPlayEndGame = 94
kMarkerFolderInvitePlayerTB = 100
kMarkerFolderEditStartGameTB = 103
kMarkerFolderPlayEndGameTB = 104
kMarkerFolderGameTimeTitleTB = 199
kMarkerFolderGameTimeTB = 200
kMarkerFolderTimePullDownBtn = 201
kMarkerFolderTimeArrow = 202
kMarkerFolderGameTypeTB = 210
kMarkerFolderTypePullDownBtn = 211
kMarkerFolderTypeArrow = 212
kMarkerFolderDeleteBtn = 150
kMarkerFolderToranIcon = 220
kMarkerFolderHSpanIcon = 221
kMarkerFolderVSpanIcon = 222
kMarkerFolderToranTB = 224
kMarkerFolderHSpanTB = 225
kMarkerFolderVSpanTB = 226
kMarkerFolderMarkListbox = 300
kMarkerFolderMarkerListUpBtn = 301
kMarkerFolderMarkerListDownBtn = 302
kMarkerFolderMarkerTextTB = 310
kMarkerFolderMarkerTextBtn = 311
kMarkerFolderMarkerTextEB = 312
kMGNotActive = 0
kMGGameCreation = 1
kMGGameOn = 2
MarkerGameState = kMGNotActive
WorkingMarkerFolder = None
CurrentPlayingMarkerGame = None
kMFOverview = 1
kMFEditing = 2
kMFEditingMarker = 3
kMFPlaying = 4
MFdialogMode = kMFOverview
MarkerGameTimeID = 0
MarkerJoinRequests = []
gGZPlaying = 0
gGZMarkerInRange = 0
gGZMarkerInRangeRepy = None
gMarkerToGetColor = 'off'
gMarkerGottenColor = 'off'
gMarkerToGetNumber = 0
gMarkerGottenNumber = 0
kQNTitle = 100
kQNMessage = 101
kQNAcceptBtn = 110
kQNAcceptText = 120
kQNDeclineBtn = 111
kQNDeclineText = 121
AmICCR = 0
DefaultKeyIgnoreList = [10, 27]
##############################################################################
# Slow link to Relto fix
##############################################################################
gVConnected = 0
##############################################################################
# End slow link to Relto fix
##############################################################################
##############################################################################
# Alcugs invite deficiency workaround
##############################################################################
kInviteFinish = 2703
InviteInProgress = None
InviteRecipient = 0
InviteParentNode = None
InviteTryCount = 0
##############################################################################
# End Alcugs invite deficiency workaround
##############################################################################
MaxRecents = 100
# Ahnonay Sphere 4 work-around BEGIN
gSitOnNextLinkOut = 0
# Ahnonay Sphere 4 work-around END
# Manage hidden players BEGIN
gShowHiddenPlayers = false
# Manage hidden players END
# Fix new players being shown as near BEGIN
kUpdatePlayerList = 2901
# Fix new players being shown as near END
kUserKITimerIdStart = 3000
kUserKITimerIdEnd = 3999
#AFK MESSAGE
gAfkMessage = ''
gAfkInformed = {} # map of KI numbers to timestamps
kAfkInformationWait = 120 # do not inform again within two minutes
#/AFK MESSAGE
# Fix for showing markers after linking BEGIN
gMarkerFolderWhileLinkingOut = None
# Fix for showing markers after linking END


class JournalHTMLParser(HTMLParser):


    def __init__(self):
        HTMLParser.__init__(self)
        self.titleText = ''
        self.bodyText = ''
        self.inBody = 0
        self.inTitle = 0



    def IAddText(self, text):
        if self.inTitle:
            self.titleText += text
        if self.inBody:
            self.bodyText += text



    def handle_starttag(self, tag, attrs):
        if (tag == 'body'):
            self.inBody = 1
        elif (tag == 'title'):
            self.inTitle = 1
        elif (tag == 'br'):
            self.IAddText('\n')
        elif (tag == 'p'):
            pass
        else:
            PtDebugPrint(('JournalHTMLParser: Dropping unused open tag: ' + tag))



    def handle_startendtag(self, tag, attrs):
        if (tag == 'br'):
            self.IAddText('\n')
        else:
            PtDebugPrint(('JournalHTMLParser: Dropping unused open/close tag: ' + tag))



    def handle_endtag(self, tag):
        if (tag == 'body'):
            self.inBody = 0
        elif (tag == 'title'):
            self.inTitle = 0
        elif (tag == 'p'):
            self.IAddText('\n')
        else:
            PtDebugPrint(('JournalHTMLParser: Dropping unused close tag: ' + tag))



    def handle_data(self, data):
        strippedData = ''
        for character in data:
            if (not (character == '\n')):
                strippedData += character

        self.IAddText(strippedData)


    def handle_charref(self, name):
        value = int(name)
        character = ascii.unctrl(value)
        self.IAddText(str(character))


    def handle_entityref(self, name):
        if (name == 'gt'):
            self.IAddText('>')
        elif (name == 'lt'):
            self.IAddText('<')
        elif (name == 'quot'):
            self.IAddText('"')
        elif (name == 'amp'):
            self.IAddText('&')
        elif (name == 'nbsp'):
            self.IAddText(' ')
        else:
            PtDebugPrint(('JournalHTMLParser: Unknown entity ref: ' + name))



def MakeJournalFilename():
    PlayerName = PtGetClientName()
    filteredName = ''
    for letter in PlayerName:
        if (not ((letter == '/') or ((letter == '\\') or ((letter == ':') or ((letter == '*') or ((letter == '?') or ((letter == '"') or ((letter == '<') or ((letter == '>') or (letter == '|')))))))))):
            filteredName += letter

    return ((gJournalBookFilePath + filteredName) + gJournalBookFileExt)



def WriteHTMLFile(title, bodyText, fileName):
    makeDirectory = 0
    try:
        JournalFile = file(fileName, 'w')
    except:
        PtDebugPrint("Error making the journal file, maybe the path doesn't exist, attempting to make the directory")
        makeDirectory = 1
    if makeDirectory:
        try:
            os.mkdir(gJournalBookFilePath)
            JournalFile = file(fileName, 'w')
        except:
            PtDebugPrint("Couldn't make the directory, aborting save of journal")
            return
    filteredText = ''
    for letter in bodyText:
        if (letter == '\n'):
            filteredText += '<br/>\n'
        elif (letter == '>'):
            filteredText += '&gt;'
        elif (letter == '<'):
            filteredText += '&lt;'
        elif (letter == '&'):
            filteredText += '&amp;'
        else:
            filteredText += letter

    JournalFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    JournalFile.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    JournalFile.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
    JournalFile.write((('<head><title>' + title) + '</title></head>\n'))
    JournalFile.write((('<body>' + filteredText) + '</body></html>'))
    JournalFile.close()



def DirectoryCmp(x, y):
    return cmp(os.stat(y).st_ctime, os.stat(x).st_ctime)



def CMPplayerOnline(playerA, playerB):
    elPlayerA = playerA.getChild()
    elPlayerB = playerB.getChild()
    if ((type(elPlayerA) != type(None)) and (type(elPlayerB) != type(None))):
        if ((elPlayerA.getType() == PtVaultNodeTypes.kPlayerInfoNode) and (elPlayerB.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
            elPlayerA = elPlayerA.upcastToPlayerInfoNode()
            elPlayerB = elPlayerB.upcastToPlayerInfoNode()
# Manage hidden players BEGIN
            playerAonline = elPlayerA.playerIsOnline() and (gShowHiddenPlayers or not len(elPlayerA.getCreateAgeName()))
            playerBonline = elPlayerB.playerIsOnline() and (gShowHiddenPlayers or not len(elPlayerB.getCreateAgeName()))
            if (playerAonline and playerBonline):
                return cmp(elPlayerA.playerGetName(), elPlayerB.playerGetName())
            if playerAonline:
                return -1
            if playerBonline:
                return 1
# Manage hidden players END
            return cmp(elPlayerA.playerGetName(), elPlayerB.playerGetName())
    return 0



def CMPNodeDate(nodeA, nodeB):
    elNodeA = nodeA.getChild()
    elNodeB = nodeB.getChild()
    if ((type(elNodeA) != type(None)) and (type(elNodeB) != type(None))):
        if (elNodeA.getModifyTime() > elNodeB.getModifyTime()):
            return -1
        else:
            return 1
    return 0


class xKI(ptModifier,):


    def __init__(self):
        global FolderOfDevices
        ptModifier.__init__(self)
        self.id = 199
        self.version = MaxVersionNumber
        self.isChatting = 0
        FolderOfDevices = DeviceFolder(xLocalization.xKI.xDevicesFolderName)
        PtDebugPrint(('__xKI: Max version %d - minor version %d.a' % (MaxVersionNumber, MinorVersionNumber)))
        xUserKI.OnEarlyInit(self)


    def DoesPlayerHaveRelto(self):
        vault = ptVault()
        entryCleft = vault.findChronicleEntry('CleftSolved')
        if (type(entryCleft) != type(None)):
            entryCleftValue = entryCleft.chronicleGetValue()
            if (entryCleftValue == 'yes'):
                return true
        return false


# Functions to access stuff from outside
    #Dustin
    def getgFeather(self):
        return gFeather
    def setgFeather(self, newval):
        global gFeather
        gFeather = newval
    #/Dustin



    # Manage hidden players BEGIN
    def setShowHiddenPlayers(self, showThem, update = True):
        global gShowHiddenPlayers
        if gShowHiddenPlayers != showThem:
            gShowHiddenPlayers = showThem
            if update: self.IRefreshPlayerListDisplay()
    # Manage hidden players END


    def getDialog(self):
        if (theKILevel < kNormalKI):return KIMicro.dialog
        else: return KIMini.dialog


    def setChatMessageColor(self, color):
        global ChatMessageColor
        ChatMessageColor = color


    def getCurrentAgeJournal(self):
        return BKJournalFolderDict[self.IGetAgeInstanceName()]
# END Functions to access stuff from outside


    def OnInit(self):
        # init imagedir
        try:
            os.mkdir(gImageDirectory)
            PtDebugPrint(('xKI: %s directory created' % gImageDirectory), level=kDebugDumpLevel)
        except OSError:
            PtDebugPrint(('xKI: %s already created' % gImageDirectory), level=kDebugDumpLevel)
        # init jalakdir: move old column states to new state directory (sav)
        try: os.mkdir("sav")
        except: pass # don't fail if dir already exists
        dirlist = os.listdir("./")
        for f in dirlist:
            if f.lower().endswith('.txt') and (not f.lower() in ['blacklist.txt', 'urustarter-checksums.txt', 'whitelist-checksums.txt', 'whitelist.txt']):
                try: os.rename(f, "sav/"+f)
                except: os.remove(f)
        # load KI
        PtLoadDialog('KIBlackBar', self.key)
        PtLoadDialog('KINanoBlackBar', self.key)
        PtLoadDialog('KIMicroBlackBar', self.key)
        if (not PtIsSinglePlayerMode()):
            PtLoadDialog('KIMicro', self.key)
            PtLoadDialog('KIMini', self.key)
            PtLoadDialog('KIMain', self.key)
            PtLoadDialog('KIListMode', self.key)
            PtLoadDialog('KIJournalExpanded', self.key)
            PtLoadDialog('KIPictureExpanded', self.key)
            PtLoadDialog('KIPlayerExpanded', self.key)
            PtLoadDialog('KIAgeOwnerSettings', self.key)
            PtLoadDialog('KISettings', self.key)
            PtLoadDialog('KIMarkerFolder', self.key)
            PtLoadDialog('KIMarkerTimeMenu', self.key)
            PtLoadDialog('KIQuestionNote', self.key)
            PtLoadDialog('KIMarkerTypeMenu', self.key)
        PtLoadDialog('KIYesNo', self.key)
        PtLoadDialog('KINewItemAlert', self.key)
        PtLoadDialog('OptionsMenuGUI')
        PtLoadDialog('IntroBahroBgGUI')
        PtLoadDialog('OptionsMenuGUI')
        PtLoadDialog('KIHelp')
        PtLoadDialog('KIHelpMenu')
        PtLoadDialog('KeyMapDialog')
        PtLoadDialog('GameSettingsDialog')
        PtLoadDialog('CalibrationGUI')
        PtLoadDialog('TrailerPreviewGUI')
        PtLoadDialog('KeyMap2Dialog')
        PtLoadDialog('AdvancedGameSettingsDialog')
        PtLoadDialog('OptionsHelpGUI')
        PtLoadDialog('bkNotebook')
        PtLoadDialog('bkBahroRockBook')
        PtLoadDialog('bkEditableBook')
        PtLoadDialog('YeeshaPageGUI')



    def OnControlKeyEvent(self, controlKey, activeFlag):
        xUserKI.OnControlKey(self, controlKey, activeFlag)



    def OnServerInitComplete(self):
# Ahnonay Sphere 4 work-around BEGIN
        global gSitOnNextLinkOut
        gSitOnNextLinkOut = 0
# Ahnonay Sphere 4 work-around END
# Fix for showing markers after linking BEGIN
        global gMissionPlayedWhileLinkingOut
        mgr = ptMarkerMgr()
        working = mgr.getWorkingMarkerFolder()
        if (type(working) != type(None)) and not mgr.isGameRunning():
            # looks as if we are editing a mission - we need to re-show the markers after linking
            ptMarkerMgr().hideMarkersLocal()
            ptMarkerMgr().showMarkersLocal()
        if gMarkerFolderWhileLinkingOut != None:
            # a game was stopepd while linking out, continue it!
            mgr.setWorkingMarkerFolder(gMarkerFolderWhileLinkingOut)
            mgr.createGame(gMarkerFolderWhileLinkingOut.getRoundLength(), gMarkerFolderWhileLinkingOut.getGameType(), [])
            gMissionPlayedWhileLinkingOut = None
# Fix for showing markers after linking END
#Jalak
        global AgeName
        AgeName = PtGetAgeName()
        print 'xKI.OnServerInitComplete(): age = ',
        print AgeName
        if (AgeName == 'Jalak'):
            PtLoadDialog('jalakControlPanel', self.key)
            KIJalakMiniIconOn.run(self.key, state='on', netPropagate=0)
            ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).show()
            ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).enable()
            KIJalakGUIClose.run(self.key, netPropagate=0, fastforward=1)
            self.IAlertKIStart()
        else:
            KIJalakMiniIconOn.run(self.key, state='off', netPropagate=0, fastforward=1)
            ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).disable()
            ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).hide()
#/Jalak
        PtGetLocalAvatar().avatar.registerForBehaviorNotify(self.key)
        xUserKI.OnNewAgeLoaded(self)




    def OnBehaviorNotify(self, type, id, state):
        if (type == PtBehaviorTypes.kBehaviorTypeLinkOut) and state:
            xUserKI.OnLinkingOut(self)
# Fix for showing markers after linking BEGIN
            global gMarkerFolderWhileLinkingOut
            mgr = ptMarkerMgr()
            gMarkerFolderWhileLinkingOut = None
            if mgr.isGameRunning():
                folder = mgr.getWorkingMarkerFolder()
                if type(folder) != type(None) and folder.getGameType() == PtMarkerMsgGameType.kGameTypeQuest:
                    # save the currently played game to continue it after linking
                    gMarkerFolderWhileLinkingOut = folder
                    mgr.endGame()
# Fix for showing markers after linking END
# Ahnonay Sphere 4 work-around BEGIN
            if gSitOnNextLinkOut and xxConfig.isOnline():
                PtAvatarSitOnGround()
# Ahnonay Sphere 4 work-around END



    def OnAvatarSpawn(self, null):
        xUserKI.OnAvatarSpawn(self)



#Jalak
    def BeginAgeUnLoad(self, avObj):
        if (AgeName == 'Jalak'):
            if JalakGUIState:
                self.JalakGUIToggle(1)
            PtUnloadDialog('jalakControlPanel')



    def JalakGUIInit(self):
        global JalakScript
        global jlakGUIButtons
        jlakRandom = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakRandomBtn))
        jlakExtreme = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakExtremeBtn))
        jlakWall = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakWallToggleBtn))
        jlakAllLow = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakColumnsLowBtn))
        jlakAllMed = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakColumnsMedBtn))
        jlakAllHigh = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakColumnsHighBtn))
        jlakRamp = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakRampBtn))
        jlakSphere = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakSphereBtn))
        jlakBigBox = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakBigBoxBtn))
        jlakLilBox = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakLilBoxBtn))
        jlakRect = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakRectangleBtn))
        jlakDestroy = ptGUIControlButton(KIJalakGUIDialog.dialog.getControlFromTag(kJalakDestroyBtn))
        jlakGUIButtons = [jlakRandom, jlakExtreme, jlakWall, jlakAllLow, jlakAllMed, jlakAllHigh, jlakRamp, jlakSphere, jlakBigBox, jlakLilBox, jlakRect, jlakDestroy]
        KIJalakGUIClose.run(self.key, netPropagate=0, fastforward=1)
        obj = PtFindSceneobject('JalakDONOTTOUCH', 'Jalak')
        pythonScripts = obj.getPythonMods()
        for script in pythonScripts:
            if (script.getName() == kJalakPythonComponent):
                JalakScript = script
                print "xKI.JalakGUIInit(): found Jalak's python component: ",
                print kJalakPythonComponent
                return

        print "xKI.JalakGUIInit():  ERROR! did NOT find Jalak's python component: ",
        print kJalakPythonComponent



    def JalakGUIToggle(self, ff = 0):
        global JalakGUIState
        print 'xKI.JalakGUIToggle()'
        ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).disable()
        if (AgeName != 'Jalak'):
            JalakGUIState = 0
            return
        if JalakGUIState:
            JalakGUIState = 0
            KIJalakGUIClose.run(self.key, netPropagate=0, fastforward=ff)
            if ff:
                PtHideDialog('jalakControlPanel')
                # the responder is not called due to using fastforward, we have to re-enable it
                ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).enable()
        else:
            if (WeAreTakingAPicture or WaitingForAnimation):
                PtDebugPrint('DEBUG: xKI.JalakGUIToggle():\tAborting request for Jalak GUI: user is busy!')
                return
            if ((theKILevel <= kMicroKI) or IKIDisabled):
                PtDebugPrint('DEBUG: xKI.JalakGUIToggle():\tAborting request for Jalak GUI: user does not have the KI!')
                return
            JalakGUIState = 1
            PtShowDialog('jalakControlPanel')
            KIJalakGUIOpen.run(self.key, netPropagate=0)



    def SetJalakGUIButtons(self, state):
        for btn in jlakGUIButtons:
            if state:
                btn.enable()
            else:
                btn.disable()




    def SendJalakBtnHit(self, btnID):
        if (btnID == kJalakRandomBtn):
            self.SendNote(('self.AutoColumns(%d)' % 3))
        elif (btnID == kJalakExtremeBtn):
            self.SendNote(('self.AutoColumns(%d)' % 4))
        elif (btnID == kJalakWallToggleBtn):
            self.SendNote('self.ToggleWall()')
        elif (btnID == kJalakColumnsLowBtn):
            self.SendNote(('self.AutoColumns(%d)' % 0))
        elif (btnID == kJalakColumnsMedBtn):
            self.SendNote(('self.AutoColumns(%d)' % 1))
        elif (btnID == kJalakColumnsHighBtn):
            self.SendNote(('self.AutoColumns(%d)' % 2))
        elif (btnID == kJalakRampBtn):
            self.SendNote(('self.DropWidget("%s")' % kRamp))
        elif (btnID == kJalakSphereBtn):
            self.SendNote(('self.DropWidget("%s")' % kSphere))
        elif (btnID == kJalakBigBoxBtn):
            self.SendNote(('self.DropWidget("%s")' % kBigBox))
        elif (btnID == kJalakLilBoxBtn):
            self.SendNote(('self.DropWidget("%s")' % kLilBox))
        elif (btnID == kJalakRectangleBtn):
            self.SendNote(('self.DropWidget("%s")' % kRect))
        elif (btnID == kJalakDestroyBtn):
            self.SendNote('self.ResetWidgets()')



    def SendNote(self, ExtraInfo):
        note = ptNotify(self.key)
        note.clearReceivers()
        note.addReceiver(JalakScript)
        note.netPropagate(0)
        note.netForce(0)
        note.setActivate(1.0)
        note.addVarNumber(str(ExtraInfo), 1.0)
        note.send()
#/Jalak




    def OnFirstUpdate(self):
        global AmICCR
        global ChatLogFile
        self.dnicoords = ptDniCoordinates()
        ChatLogFile = ptStatusLog()
        try:
            AmICCR = ptCCRMgr().getLevel()
            PtDebugPrint(('xKI: CCR level set at %d' % AmICCR), level=kDebugDumpLevel)
        except:
            PtDebugPrint('xKI: error - not CCR ', level=kDebugDumpLevel)
            AmICCR = 0
        xBookGUIs.LoadAllBookGUIs()
        #Dustin
        print 'Loading DynamicTextMaps...'
        import booksDustGlobal
        booksDustGlobal.ImagerMap = ImagerMap
        booksDustGlobal.BookMapLeft = BookMapLeft
        booksDustGlobal.BookMapRight = BookMapRight
        booksDustGlobal.BookMapBack = BookMapBack
        booksDustGlobal.BookMapFront = BookMapFront
        booksDustGlobal.bhrLinkPanelMap = bhrLinkPanelMap
        booksDustGlobal.bhrShareButtonMap = bhrShareButtonMap
        #/Dustin



    def __del__(self):
        PtUnloadDialog('KINanoBlackBar')
        PtUnloadDialog('KIMicroBlackBar')
        if (not PtIsSinglePlayerMode()):
            PtUnloadDialog('KIMicro')
            PtUnloadDialog('KIMini')
            PtUnloadDialog('KIMain')
            PtUnloadDialog('KIListMode')
            PtUnloadDialog('KIJournalExpanded')
            PtUnloadDialog('KIPictureExpanded')
            PtUnloadDialog('KIPlayerExpanded')
            PtUnloadDialog('KIAgeOwnerSettings')
            PtUnloadDialog('KISettings')
            PtUnloadDialog('KIMarkerFolder')
            PtUnloadDialog('KIMarkerTimeMenu')
            PtUnloadDialog('KIQuestionNote')
            PtUnloadDialog('KIMarkerTypeMenu')
        PtUnloadDialog('KIYesNo')
        PtUnloadDialog('KINewItemAlert')
        PtUnloadDialog('OptionsMenuGUI')
        PtUnloadDialog('IntroBahroBgGUI')
        PtUnloadDialog('OptionsMenuGUI')
        PtUnloadDialog('KIHelp')
        PtUnloadDialog('KIHelpMenu')
        PtUnloadDialog('KeyMapDialog')
        PtUnloadDialog('GameSettingsDialog')
        PtUnloadDialog('CalibrationGUI')
        PtUnloadDialog('TrailerPreviewGUI')
        PtUnloadDialog('KeyMap2Dialog')
        PtUnloadDialog('AdvancedGameSettingsDialog')
        PtUnloadDialog('OptionsHelpGUI')
        PtUnloadDialog('bkNotebook')
        PtUnloadDialog('bkBahroRockBook')
        PtUnloadDialog('bkEditableBook')
        PtUnloadDialog('YeeshaPageGUI')
#Jalak
        PtUnloadDialog('jalakControlPanel')
#/Jalak



    def ILocalizeQuitNoDialog(self):
        yesButton = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
        noButton = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
        yesButton.setString(xLocalization.xKI.xYesNoQuitbutton)
        noButton.setString(xLocalization.xKI.xYesNoNoButton)



    def ILocalizeYesNoDialog(self):
        yesButton = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
        noButton = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
        yesButton.setString(xLocalization.xKI.xYesNoYESbutton)
        noButton.setString(xLocalization.xKI.xYesNoNoButton)



    def OnDefaultKeyCaught(self, ch, isDown, isShift, isCtrl, keycode):
        if (ord(ch) != 0):
            if (not (ord(ch) in DefaultKeyIgnoreList)):
                if (isDown and (not isCtrl)):
                    if ((not IKIDisabled) and (not PtIsEnterChatModeKeyBound())):
                        self.IEnterChatMode(1, firstChar=ch)
            else:
                PtDebugPrint(('xKI:DEFAULTKEY not used char of = %d' % ord(ch)), level=kDebugDumpLevel)
        elif isDown:
            xUserKI.OnDefaultKey(self, isShift, isCtrl, keycode)



    def OnNotify(self, state, id, events):
        global BookOfferer
        global WaitingForAnimation
        global OfferedBookMode
        PtDebugPrint(('xKI: Notify  state=%f, id=%d' % (state, id)), level=kDebugDumpLevel)
        for event in events:
            if (event[0] == kOfferLinkingBook):
                PtDebugPrint('got offer book notification', level=kDebugDumpLevel)
                if ((theKILevel == kMicroKI) or PtIsSinglePlayerMode()):
                    plybkCB = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                else:
                    plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                if (event[2] == -999):
                    if (OfferedBookMode == kOfferee):
                        YeeshaBook.hide()
                        PtToggleAvatarClickability(true)
                        plybkCB.setChecked(0)
                    OfferedBookMode = kNotOffering
                    BookOfferer = None
                    PtDebugPrint('Offerer is rescinding the book offer', level=kDebugDumpLevel)
                    PtToggleAvatarClickability(true)
                    return
                elif (event[2] == 999):
                    OfferedBookMode = kOfferee
                    BookOfferer = event[1]
                    PtDebugPrint('offered book by ', BookOfferer.getName(), level=kDebugDumpLevel)
                    self.IShowYeeshaBook()
                    PtToggleAvatarClickability(false)
                    return
            elif (event[0] == PtEventType.kBook):
                PtDebugPrint(('xKI: BookNotify  event=%d, id=%d' % (event[1], event[2])), level=kDebugDumpLevel)
                if ((theKILevel == kMicroKI) or PtIsSinglePlayerMode()):
                    if gCurBookIsYeesha:
                        plybkCB = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                    else:
                        plybkCB = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kJournalBookCBID))
                elif gCurBookIsYeesha:
                    plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                else:
                    plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID))
                if (event[1] == PtBookEventTypes.kNotifyImageLink):
# uam API for linking books
                    if event[2] == 100:
                        try :
                            import uam
                            if uam._handleClick(): return
                        except: pass # we are using the actual UAM plugin
# END uam API for linking books
                    if (event[2] == xLinkingBookDefs.kYeeshaBookShareID):
                        if IsYeeshaBookEnabled:
                            PtClearOfferBookMode()
                            if (OfferedBookMode == kNotOffering):
                                YeeshaBook.hide()
                                PtToggleAvatarClickability(true)
                                plybkCB.setChecked(0)
                                PtSetOfferBookMode(self.key, 'Personal', 'Relto')
                    elif (event[2] == xLinkingBookDefs.kYeeshaBookLinkID):
                        if IsYeeshaBookEnabled:
                            PtDebugPrint('xKI:Book: hit linking panel', level=kDebugDumpLevel)
                            YeeshaBook.hide()
                            plybkCB.setChecked(0)
                            if (OfferedBookMode == kOfferee):
                                PtDebugPrint('accepted link, notifying offerer of such', level=kDebugDumpLevel)
                                OfferedBookMode = kNotOffering
                                avID = PtGetClientIDFromAvatarKey(BookOfferer.getKey())
                                PtNotifyOffererLinkAccepted(avID)
                                PtNotifyOffererLinkCompleted(avID)
                                BookOfferer = None
                            else:
                                curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                                if (IsEntireYeeshaBookEnabled and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                                    linkmgr = ptNetLinkingMgr()
                                    linkmgr.linkToMyPersonalAgeWithYeeshaBook()
                                    PtToggleAvatarClickability(true)
                    elif (event[2] >= xLinkingBookDefs.kYeeshaPageStartID):
# Custom relto pages BEGIN
                        import xCustomReltoPages
                        if xCustomReltoPages.TogglePage(event[2] - 200):
                            return
# Custom relto pages END
                        whatpage = (event[2] - xLinkingBookDefs.kYeeshaPageStartID)
                        sdlvar = xLinkingBookDefs.xYeeshaPages[whatpage][0]
                        self.IToggleYeeshaPageSDL(sdlvar, 1)
                elif (event[1] == PtBookEventTypes.kNotifyShow):
# uam API for linking books
                    try:
                        import uam
                        uam._bookShown()
                    except: pass
# END uam API for linking books
                elif (event[1] == PtBookEventTypes.kNotifyHide):
                    PtDebugPrint('xKI:Book: NotifyHide', level=kDebugDumpLevel)
                    PtToggleAvatarClickability(true)
                    plybkCB.setChecked(0)
                    if (OfferedBookMode == kOfferee):
                        PtDebugPrint('rejecting link, notifying offerer of such', level=kDebugDumpLevel)
                        OfferedBookMode = kNotOffering
                        avID = PtGetClientIDFromAvatarKey(BookOfferer.getKey())
                        PtNotifyOffererLinkRejected(avID)
                        BookOfferer = None
                    elif (not gCurBookIsYeesha):
                        JBText = JournalBook.getEditableText()
                        WriteHTMLFile((xLocalization.xJournalBookDefs.xPlayerJournalTitle % PtGetClientName()), JBText, MakeJournalFilename())
# uam API for linking books
                    try:
                        import uam
                        uam._bookHidden()
                    except: pass
# END uam API for linking books
                elif (event[1] == PtBookEventTypes.kNotifyNextPage):
                    pass
                elif (event[1] == PtBookEventTypes.kNotifyPreviousPage):
                    pass
                elif (event[1] == PtBookEventTypes.kNotifyCheckUnchecked):
                    if (event[2] >= xLinkingBookDefs.kYeeshaPageStartID):
# Custom relto pages BEGIN
                        import xCustomReltoPages
                        if xCustomReltoPages.TogglePage(event[2] - 200):
                            return
# Custom relto pages END
                        whatpage = (event[2] - xLinkingBookDefs.kYeeshaPageStartID)
                        sdlvar = xLinkingBookDefs.xYeeshaPages[whatpage][0]
                        self.IToggleYeeshaPageSDL(sdlvar, 0)
                return

        if state:
            if (id == KIOnResp.id):
                self.IBigKIShowMode()
                WaitingForAnimation = 0
                toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
                toggleCB.enable()
            elif (id == KIOffResp.id):
                BigKI.dialog.hide()
                WaitingForAnimation = 0
                toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
                toggleCB.enable()
#Jalak
        if (id == KIJalakGUIClose.id):
            PtHideDialog('jalakControlPanel')
            ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).enable()
        elif (id == KIJalakGUIOpen.id):
            KIJalakGUIDialog.dialog.enable()
            ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).enable()
        elif (id == KIJalakBtnLights.id):
            btnID = string.atoi(KIJalakBtnLights.getState())
            self.SendJalakBtnHit(btnID)
            PtAtTimeCallback(self.key, kJalakBtnDelaySeconds, kJalakBtnDelayTimer)
#/Jalak



    def OnPageLoad(self, what, room):
        global gGZMarkerInRange
        global gGZMarkerInRangeRepy
        global KIGUIInitialized
        global BKPlayerSelected
        if (not KIGUIInitialized):
            self.IDetermineCensorLevel()
            self.IDetermineKILevel()
            self.IDetermineKIFlags()
            self.IDetermineGZ()
            if (theKILevel == kNanoKI):
                PtDebugPrint('Its a nanoKI', level=kDebugDumpLevel)
                KINanoBlackBar.dialog.show()
            elif PtIsSinglePlayerMode():
                PtDebugPrint('Its a microKI', level=kDebugDumpLevel)
                KIMicroBlackbar.dialog.show()
            elif (theKILevel == kMicroKI):
                PtDebugPrint('Its a microKI', level=kDebugDumpLevel)
                KIMicroBlackbar.dialog.show()
                if (not gKIHasJournal):
                    ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kJournalBookCBID)).hide()
                KIMicro.dialog.show()
                self.IEnterChatMode(0)
            elif (theKILevel == kNormalKI):
                PtDebugPrint('Its a normalKI', level=kDebugDumpLevel)
                KIBlackbar.dialog.show()
                self.IClearBBMini()
                if (not gKIHasJournal):
                    ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID)).hide()
                self.ICheckInboxForUnseen()
            KIGUIInitialized = 1
        if ((what == kLoaded) and ((theKILevel > kMicroKI) and (not PtIsSinglePlayerMode()))):
            self.ICheckIfCGZShouldBeRunning()
            workingMF = ptMarkerMgr().getWorkingMarkerFolder()
            if (type(workingMF) != type(None)):
                if (workingMF.getGameType() != PtMarkerMsgGameType.kGameTypeQuest):
                    ptMarkerMgr().endGame()
                    self.IResetWorkingMarkerFolder()
            self.IBigKIRefreshFolders()
            self.IBigKISetStatics()
        if (what == kUnloaded):
            FolderOfDevices.removeAll()
            if ((theKILevel == kNormalKI) and (not PtIsSinglePlayerMode())):
                BKPlayerSelected = None
                sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
                sendToField.setString(' ')
            if gGZMarkerInRange:
                gGZMarkerInRange = 0
                gGZMarkerInRangeRepy = None
                self.IRefreshMiniKIMarkerDisplay()
                NewItemAlert.dialog.hide()
                kialert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertKIAlert))
                kialert.hide()



    def ICheckIfCGZShouldBeRunning(self):
        global gAlreadyCheckedCGZGame
        if (not gAlreadyCheckedCGZGame):
            gAlreadyCheckedCGZGame = 1
            vault = ptVault()
            entry = vault.findChronicleEntry(kChronCGZPlaying)
            if (type(entry) != type(None)):
                gCurrentMarkerGame = entry.chronicleGetValue()
                if (gCurrentMarkerGame != ''):
                    Mmgr = ptMarkerMgr()
                    if (not Mmgr.isGameRunning()):
                        PtDebugPrint("xKI::IDetermineEndGame - but it wasn't running in MarkTag world! - Restarting", level=kDebugDumpLevel)
                        curGameFolder = self.IFindGameInFolder(self.IFindHiddenFolder(), gCurrentMarkerGame)
                        if curGameFolder:
                            Mmgr.setWorkingMarkerFolder(curGameFolder)
                            Mmgr.createGame(120, PtMarkerMsgGameType.kGameTypeQuest, [])
                            Mmgr.startGame()



    def IFindHiddenFolder(self):
        vault = ptVault()
        jfolder = None
        master_agefolder = vault.getAgeJournalsFolder()
        if (type(master_agefolder) != type(None)):
            agefolderRefs = master_agefolder.getChildNodeRefList()
            for agefolderRef in agefolderRefs:
                agefolder = agefolderRef.getChild()
                agefolder = agefolder.upcastToFolderNode()
                if (type(agefolder) != type(None)):
                    if self.IsFolderHidden(agefolder):
                        jfolder = agefolder
                        break

        return jfolder



    def IFindGameInFolder(self, folder, gameName):
        if folder:
            folderRefs = folder.getChildNodeRefList()
            for jref in folderRefs:
                jnode = jref.getChild()
                jnode = jnode.upcastToMarkerListNode()
                if (type(jnode) != type(None)):
                    if (jnode.folderGetName() == gameName):
                        print ('Found %s marker game in folder %s' % (folder.folderGetName(), jnode.folderGetName()))
                        return jnode

        return None



    def OnGUINotify(self, id, control, event):
        global BKGettingPlayerID
        global FadeEnableFlag
        global BKJournalFolderSelected
        global BKConfigFolderTopLine
        global YNOutsideSender
        global OfferLinkFromWho
        global BKFolderListOrder
        global OriginalForeAlpha
        global BKConfigFolderSelected
        global OnlyAllowBuddiesOnRequest
        global BKFolderSelectChanged
        global BKFolderTopLine
        global OriginalSelectAlpha
        global MarkerGameTimeID
        global OriginalminiKICenter
        global TicksOnFull
        global OnlyGetPMsFromBuddies
        global BKPlayerSelected
        global BKContentListTopLine
        global PlayerInfoName
        global MiniKIFirstTimeShow
        global BKPlayerFolderSelected
        global BKInEditMode
        global BKFolderSelected
        global BKJournalFolderTopLine
        global BKAgeOwnerEditDescription
        global BKFolderLineDict
        global BKPlayerFolderTopLine
        global BKCurrentContent
        global YNWhatReason
        PtDebugPrint(('xKI::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
        if (id == KIBlackbar.id):
            if (event == kDialogLoaded):
                pass
            elif ((event == kAction) or (event == kValueChanged)):
                bbID = control.getTagID()
                if (bbID == kMiniMaximizeRGID):
                    if (control.getValue() == 0):
                        if PtIsDialogLoaded('KIMini'):
                            KIMini.dialog.show()
                    elif (control.getValue() == -1):
                        if PtIsDialogLoaded('KIMini'):
                            KIMini.dialog.hide()
                elif (bbID == kExitButtonID):
                    yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                    yesText.setString(xLocalization.xKI.xLeaveGameMessageNormal)
                    self.ILocalizeQuitNoDialog()
                    KIYesNo.dialog.show()
                elif (bbID == kPlayerBookCBID):
                    if control.isChecked():
                        curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                        if (IsEntireYeeshaBookEnabled and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                            if (not WaitingForAnimation):
                                self.IShowYeeshaBook()
                            else:
                                control.setChecked(0)
                        else:
                            control.setChecked(0)
                elif (bbID == kJournalBookCBID):
                    if control.isChecked():
                        curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                        if (gKIHasJournal and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                            if (not WaitingForAnimation):
                                self.IShowJournalBook()
                            else:
                                control.setChecked(0)
                        else:
                            control.setChecked(0)
                elif (bbID == kBBCCRButtonID):
                    PtShowDialog('OptionsMenuGUI')
                else:
                    PtDebugPrint(("xBlackbar: Don't know this control  bbID=%d" % bbID), level=kDebugDumpLevel)
            elif (event == kInterestingEvent):
                plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                jrnbkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID))
                try:
                    curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                    if (IsEntireYeeshaBookEnabled and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                        PtDebugPrint('xBlackbar: interesting - show playerbook', level=kDebugDumpLevel)
                        plybkCB.show()
                    else:
                        PtDebugPrint('xBlackbar: interesting - on ladder - hide playerbook', level=kDebugDumpLevel)
                        plybkCB.hide()
                    if (gKIHasJournal and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                        PtDebugPrint('xBlackbar: interesting - show journal book', level=kDebugDumpLevel)
                        jrnbkCB.show()
                    else:
                        PtDebugPrint('xBlackbar: interesting - on ladder - hide journal book', level=kDebugDumpLevel)
                        jrnbkCB.hide()
                except NameError:
                    if IsEntireYeeshaBookEnabled:
                        PtDebugPrint('xBlackbar: interesting - show playerbook', level=kDebugDumpLevel)
                        plybkCB.show()
                    else:
                        PtDebugPrint('xBlackbar: interesting - on ladder - hide playerbook', level=kDebugDumpLevel)
                        plybkCB.hide()
                    if gKIHasJournal:
                        PtDebugPrint('xBlackbar: interesting - show journal book', level=kDebugDumpLevel)
                        jrnbkCB.show()
                    else:
                        PtDebugPrint('xBlackbar: interesting - on ladder - hide journal book', level=kDebugDumpLevel)
                        jrnbkCB.hide()
        elif (id == KINanoBlackBar.id):
            PtDebugPrint(('nanoBlackbar::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kDialogLoaded):
                pass
            elif ((event == kAction) or (event == kValueChanged)):
                bbID = control.getTagID()
                if (bbID == kExitButtonID):
                    yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                    yesText.setString(xLocalization.xKI.xLeaveGameMessageNano)
                    self.ILocalizeQuitNoDialog()
                    KIYesNo.dialog.show()
                elif (bbID == kBBCCRButtonID):
                    PtShowDialog('OptionsMenuGUI')
                else:
                    PtDebugPrint(("xnanoBlackbar: Don't know this control  bbID=%d" % bbID), level=kDebugDumpLevel)
        elif (id == KIMicroBlackbar.id):
            PtDebugPrint(('microBlackbar::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kDialogLoaded):
                if PtIsSinglePlayerMode():
                    chatBtn = ptGUIControlButton(KIMicroBlackbar.dialog.getControlFromTag(kmicroChatButton))
                    chatBtn.hide()
                rollBtn = ptGUIControlButton(KIMicroBlackbar.dialog.getControlFromTag(kRolloverLeftID))
                rollBtn.setNotifyOnInteresting(1)
                rollBtn = ptGUIControlButton(KIMicroBlackbar.dialog.getControlFromTag(kRolloverRightID))
                rollBtn.setNotifyOnInteresting(1)
            elif ((event == kAction) or (event == kValueChanged)):
                bbID = control.getTagID()
                if (bbID == kExitButtonID):
                    yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                    yesText.setString(xLocalization.xKI.xLeaveGameMessageMicro)
                    self.ILocalizeQuitNoDialog()
                    KIYesNo.dialog.show()
                elif (bbID == kPlayerBookCBID):
                    if control.isChecked():
                        curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                        if (IsEntireYeeshaBookEnabled and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                            if (not WaitingForAnimation):
                                self.IShowYeeshaBook()
                            else:
                                control.setChecked(0)
                        else:
                            control.setChecked(0)
                elif (bbID == kJournalBookCBID):
                    if control.isChecked():
                        curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                        if (gKIHasJournal and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                            if (not WaitingForAnimation):
                                self.IShowJournalBook()
                            else:
                                control.setChecked(0)
                        else:
                            control.setChecked(0)
                elif (bbID == kBBCCRButtonID):
                    PtShowDialog('OptionsMenuGUI')
                else:
                    PtDebugPrint(("xmicroBlackbar: Don't know this control  bbID=%d" % bbID), level=kDebugDumpLevel)
            elif (event == kInterestingEvent):
                plybkCB = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                jrnbkCB = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kJournalBookCBID))
                try:
                    curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                    if (IsEntireYeeshaBookEnabled and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                        PtDebugPrint('xmicroBlackbar: interesting - show playerbook', level=kDebugDumpLevel)
                        plybkCB.show()
                    else:
                        PtDebugPrint('xmicroBlackbar: interesting - on ladder - hide playerbook', level=kDebugDumpLevel)
                        plybkCB.hide()
                    if (gKIHasJournal and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                        PtDebugPrint('xmicroBlackbar: interesting - show journal book', level=kDebugDumpLevel)
                        jrnbkCB.show()
                    else:
                        PtDebugPrint('xmicroBlackbar: interesting - on ladder - hide journal book', level=kDebugDumpLevel)
                        jrnbkCB.hide()
                except NameError:
                    if IsEntireYeeshaBookEnabled:
                        PtDebugPrint('xmicroBlackbar: interesting - show playerbook', level=kDebugDumpLevel)
                        plybkCB.show()
                    else:
                        PtDebugPrint('xmicroBlackbar: interesting - on ladder - hide playerbook', level=kDebugDumpLevel)
                        plybkCB.hide()
                    if gKIHasJournal:
                        PtDebugPrint('xmicroBlackbar: interesting - show journal book', level=kDebugDumpLevel)
                        jrnbkCB.show()
                    else:
                        PtDebugPrint('xmicroBlackbar: interesting - on ladder - hide journal book', level=kDebugDumpLevel)
                        jrnbkCB.hide()
        elif (id == KIMicro.id):
            PtDebugPrint(('microKI::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kDialogLoaded):
                chatarea = ptGUIControlMultiLineEdit(KIMicro.dialog.getControlFromTag(kChatDisplayArea))
                chatarea.lock()
                chatarea.unclickable()
                chatarea.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
                chatarea.disableScrollControl()
                btnUp = ptGUIControlButton(KIMicro.dialog.getControlFromTag(kminiChatScrollUp))
                btnUp.show()
                btnUp.hide()
                chatedit = ptGUIControlEditBox(KIMicro.dialog.getControlFromTag(kChatEditboxID))
                chatedit.setStringSize(500)
                chatedit.setChatMode(1)
            elif (event == kShowHide):
                if control.isEnabled():
                    if (not self.isChatting):
                        self.IFadeCompletely()
            elif ((event == kAction) or (event == kValueChanged)):
                ctrlID = control.getTagID()
                if (ctrlID == kChatEditboxID):
                    if ((not control.wasEscaped()) and (control.getString() != '')):
                        self.ISendRTChat(control.getString())
                    self.IEnterChatMode(0)
                elif (ctrlID == kChatDisplayArea):
                    self.IKillFadeTimer()
                    self.IStartFadeTimer()
            elif (event == kFocusChange):
                if self.isChatting:
                    KIMicro.dialog.setFocus(KIMicro.dialog.getControlFromTag(kChatEditboxID))
        elif (id == KIMini.id):
            if (event == kDialogLoaded):
                dragbar = ptGUIControlDragBar(KIMini.dialog.getControlFromTag(kminiDragBar))
                OriginalminiKICenter = dragbar.getObjectCenter()
                fore = control.getForeColor()
                OriginalForeAlpha = fore.getAlpha()
                sel = control.getSelectColor()
                OriginalSelectAlpha = sel.getAlpha()
                chatarea = ptGUIControlMultiLineEdit(KIMini.dialog.getControlFromTag(kChatDisplayArea))
                chatarea.lock()
                chatarea.unclickable()
                chatarea.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
                chatarea.disableScrollControl()
                btnUp = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiChatScrollUp))
                btnUp.show()
                privateChbox = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiPrivateToggle))
                privateChbox.disable()
                chatedit = ptGUIControlEditBox(KIMini.dialog.getControlFromTag(kChatEditboxID))
                chatedit.setStringSize(500)
                chatedit.setChatMode(1)
                btnmt = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiGZDrip))
                btnmt.hide()
                btnmt = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiGZActive))
                btnmt.hide()
                btnmt = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiGZMarkerGameActive))
                btnmt.hide()
                btnmt = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiGZMarkerInRange))
                btnmt.hide()
                for mcbid in range(kminiMarkerIndicator01, (kminiMarkerIndicatorLast + 1)):
                    mcb = ptGUIControlProgress(KIMini.dialog.getControlFromTag(mcbid))
                    mcb.setValue(gMarkerColors['off'])
#Pellets
                btnmt = ptGUIControlButton(KIMini.dialog.getControlFromTag(kPelletScoreButton))
                btnmt.hide()
#/Pellets
#MOUL marker buttons
                btnmt = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiMGNewMarker))
                btnmt.hide()
                btnmt = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiMGNewGame))
                btnmt.hide()
                btnmt = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiMGInactive))
                btnmt.hide()
#/MOUL marker buttons
            elif (event == kShowHide):
                if control.isEnabled():
                    if MiniKIFirstTimeShow:
                        self.IDetermineFontSize()
                        self.IDetermineFadeTime()
                        if (not self.isChatting):
                            self.IEnterChatMode(0)
                            self.IFadeCompletely()
                        MiniKIFirstTimeShow = 0
                    self.IRefreshPlayerList()
                    self.IRefreshPlayerListDisplay()
                    self.IRefreshMiniKIMarkerDisplay()
                else:
                    self.IEnterChatMode(0)
                    self.IClearBBMini()
            elif ((event == kAction) or (event == kValueChanged)):
                ctrlID = control.getTagID()
                PtDebugPrint(('xKImini:: tagID=%d, event=%d control=' % (ctrlID, event)), control, level=kDebugDumpLevel)
                if (ctrlID == kChatEditboxID):
                    if ((not control.wasEscaped()) and (control.getString() != '')):
                        self.ISendRTChat(control.getString())
                    self.IEnterChatMode(0)
                    self.IStartFadeTimer()
                elif (ctrlID == kPlayerList):
                    plyrsel = control.getSelection()
                    if (plyrsel >= control.getNumElements()):
                        control.setSelection(0)
                        plyrsel = 0
                    sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
                    caret = ptGUIControlTextBox(KIMini.dialog.getControlFromTag(kChatCaretID))
                    caret.setString('>')
                    privateChbox = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiPrivateToggle))
                    privateChbox.setChecked(0)
                    PlayerInfoName = None
                    if (plyrsel == -1):
                        BKPlayerSelected = None
                    else:
                        BKPlayerSelected = BKPlayerList[plyrsel]
                        if (isinstance(BKPlayerSelected, DeviceFolder) or (type(BKPlayerSelected) == type(''))):
                            pass
                        elif isinstance(BKPlayerSelected, Device):
                            sendToField.setString(BKPlayerSelected.name)
                        elif isinstance(BKPlayerSelected, ptVaultNodeRef):
                            plyrInfonode = BKPlayerSelected.getChild()
                            plyrInfo = plyrInfonode.upcastToPlayerInfoNode()
                            if (type(plyrInfo) != type(None)):
                                sendToField.setString(plyrInfo.playerGetName())
                                caret.setString(((xLocalization.xKI.xChatTOPrompt + plyrInfo.playerGetName()) + ' >'))
                                privateChbox.setChecked(1)
                            else:
                                BKPlayerSelected = None
                        elif isinstance(BKPlayerSelected, ptPlayer):
                            sendToField.setString(BKPlayerSelected.getPlayerName())
                            caret.setString(((xLocalization.xKI.xChatTOPrompt + BKPlayerSelected.getPlayerName()) + ' >'))
                            PlayerInfoName = BKPlayerSelected
                            privateChbox.setChecked(1)
                        elif isinstance(BKPlayerSelected, ptVaultPlayerInfoListNode):
                            fldrType = BKPlayerSelected.folderGetType()
                            if (fldrType != PtVaultStandardNodes.kAgeMembersFolder):
                                if (fldrType == PtVaultStandardNodes.kAgeOwnersFolder):
                                    fldrType = PtVaultStandardNodes.kHoodMembersFolder
                                caret.setString(((xLocalization.xKI.xChatTOPrompt + string.upper(xLocalization.FolderIDToFolderName(fldrType))) + ' >'))
                            privateChbox.setChecked(0)
                            BKPlayerSelected = None
                        elif isinstance(BKPlayerSelected, MarkerPlayer):
                            caret.setString(((xLocalization.xKI.xChatTOPrompt + BKPlayerSelected.player.getPlayerName()) + ' >'))
                            privateChbox.setChecked(1)
                            BKPlayerSelected = None
                        elif isinstance(BKPlayerSelected, MarkerGame):
                            caret.setString(xLocalization.xKI.xChatMarkerTOAllTeams)
                            privateChbox.setChecked(0)
                            BKPlayerSelected = None
                        elif isinstance(BKPlayerSelected, DPLBranchStatusLine):
                            if (type(CurrentPlayingMarkerGame) != type(None)):
                                if (BKPlayerSelected == CurrentPlayingMarkerGame.greenTeamDPL):
                                    caret.setString(xLocalization.xKI.xChatMarkerTOGreenTeam)
                                elif (BKPlayerSelected == CurrentPlayingMarkerGame.redTeamDPL):
                                    caret.setString(xLocalization.xKI.xChatMarkerTORedTeam)
                            privateChbox.setChecked(0)
                            BKPlayerSelected = None
                        else:
                            BKPlayerSelected = None
                    if (type(BKPlayerSelected) == type(None)):
                        sendToField.setString(' ')
                    self.IBigKISetToButtons()
                    if self.isChatting:
                        chatedit = ptGUIControlEditBox(KIMini.dialog.getControlFromTag(kChatEditboxID))
                        KIMini.dialog.setFocus(chatedit.getKey())
                    self.IKillFadeTimer()
                    self.IStartFadeTimer()
                elif (ctrlID == kminiPutAwayID):
                    self.IminiPutAwayKI()
                elif (ctrlID == kminiToggleBtnID):
                    self.IminiToggleKISize()
                elif (ctrlID == kminiTakePicture):
                    self.IminiTakePicture()
                elif (ctrlID == kminiCreateJournal):
                    self.IminiCreateJournal()
                elif (ctrlID == kminiMuteAll):
                    audio = ptAudioControl()
                    if control.isChecked():
                        audio.muteAll()
                    else:
                        audio.unmuteAll()
                elif (ctrlID == kminiPlayerListUp):
                    playerlist = ptGUIControlListBox(KIMini.dialog.getControlFromTag(kPlayerList))
                    self.IScrollUpListbox(playerlist, kminiPlayerListUp, kminiPlayerListDown)
                elif (ctrlID == kminiPlayerListDown):
                    playerlist = ptGUIControlListBox(KIMini.dialog.getControlFromTag(kPlayerList))
                    self.IScrollDownListbox(playerlist, kminiPlayerListUp, kminiPlayerListDown)
                elif (ctrlID == kminiGZMarkerInRange):
                    PtDebugPrint('miniKI::GetMarkerButton hit!', level=kDebugDumpLevel)
##############################################################################
# Changes for PotS markers
##############################################################################
                    if xxConfig.CollectMarkersUU: self.ICaptureGZMarker() # keep this to allow UU way
#                    self.IRefreshMiniKIMarkerDisplay() # remove unconditionally
##############################################################################
# End changes for PotS markers
##############################################################################
#MOUL marker buttons
                elif (ctrlID == kminiMGNewGame):
                    if MFdialogMode in [kMFOverview, kMFPlaying]:
                        self.ICreateMarkerFolder()
                    else:
                        self.ICreateAMarker()
#/MOUL marker buttons
                elif (ctrlID == kChatDisplayArea):
                    self.IKillFadeTimer()
                    self.IStartFadeTimer()
#Jalak
                elif (ctrlID == kJalakMiniIconBtn):
                    if (AgeName == 'Jalak'):
                        self.JalakGUIToggle()
                    else:
                        ptGUIControlButton(KIMini.dialog.getControlFromTag(kJalakMiniIconBtn)).disable()
#/Jalak
            elif (event == kFocusChange):
                if self.isChatting:
                    if (not BigKI.dialog.isEnabled()):
                        KIMini.dialog.setFocus(KIMini.dialog.getControlFromTag(kChatEditboxID))
                    elif (not BKInEditMode):
                        KIMini.dialog.setFocus(KIMini.dialog.getControlFromTag(kChatEditboxID))
        elif (id == BigKI.id):
            PtDebugPrint(('BigKI::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kDialogLoaded):
                BKInEditMode = 0
                KIOnAnim.animation.skipToTime(1.5)
                if PtIsSinglePlayerMode():
                    modeselector = ptGUIControlRadioGroup(BigKI.dialog.getControlFromTag(kBKRadioModeID))
                    modeselector.setValue(0)
                    modeselector.disable()
                else:
                    pdisable = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKDisabledPeopleButton))
                    pdisable.disable()
                    gdisable = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKDisabledGearButton))
                    gdisable.disable()
                self.IBigKISetNotifyForLong()
            elif (event == kShowHide):
                if control.isEnabled():
                    self.IBigKIHideLongFolderNames()
                    self.IBigKISetStatics()
                    self.IBigKISetChanging()
                    self.IRefreshPlayerList()
                    self.IRefreshPlayerListDisplay()
                    self.IKillFadeTimer()
                    self.IBigKIRefreshFolders()
                    self.IBigKIRefreshFolderDisplay()
                    self.IBigKIShowBigKI()
                else:
                    self.IStartFadeTimer()
            elif ((event == kAction) or (event == kValueChanged)):
                bkID = control.getTagID()
                PtDebugPrint(('BigKI::OnGUINotify event=%d controlID=%d' % (event, bkID)), level=kDebugDumpLevel)
                if ((bkID >= kBKIIncomingBtn) and (bkID <= kBKIFolderLineBtnLast)):
                    if (BKFolderLineDict is BKConfigFolderDict):
                        BKFolderSelected = ((bkID - kBKIIncomingBtn) + BKFolderTopLine)
                        self.IShowSelectedConfig()
                    else:
                        oldselect = BKFolderSelected
                        BKFolderSelected = ((bkID - kBKIIncomingBtn) + BKFolderTopLine)
                        if (oldselect != BKFolderSelected):
                            BKFolderSelectChanged = 1
                        else:
                            BKFolderSelectChanged = 0
                        self.IBigKIChangeMode(kBKListMode)
                elif (bkID == kBKFolderUpLine):
                    if (BKFolderTopLine > 0):
                        BKFolderTopLine -= 1
                        self.IBigKIRefreshFolderDisplay()
                        self.IBigKISetToButtons()
                elif (bkID == kBKFolderDownLine):
                    BKFolderTopLine += 1
                    self.IBigKIRefreshFolderDisplay()
                    self.IBigKISetToButtons()
                elif (bkID == kBKLMUpButton):
                    if (BKRightSideMode == kBKListMode):
                        if (BKContentListTopLine > 0):
                            BKContentListTopLine -= kContentListScrollSize
                            if (BKContentListTopLine < 0):
                                BKContentListTopLine = 0
                            self.IBigKIRefreshContentListDisplay()
                elif (bkID == kBKLMDownButton):
                    if (BKRightSideMode == kBKListMode):
                        BKContentListTopLine += kContentListScrollSize
                        self.IBigKIRefreshContentListDisplay()
                elif ((bkID >= kBKIToFolderButton01) and (bkID <= kBKIToFolderButtonLast)):
                    tofolderNum = (((bkID - kBKIToFolderButton01) + BKFolderTopLine) + 1)
                    if ((BKRightSideMode != kBKListMode) and (type(BKCurrentContent) != type(None))):
                        if isinstance(BKCurrentContent, ptPlayer):
                            try:
                                newfoldername = BKFolderListOrder[tofolderNum]
                                newfolder = BKFolderLineDict[newfoldername]
                                if (type(newfolder) != type(None)):
                                    if (newfolder.getType() == PtVaultNodeTypes.kPlayerInfoListNode):
                                        localplayer = PtGetLocalPlayer()
                                        if (BKCurrentContent.getPlayerID() != localplayer.getPlayerID()):
                                            newfolder.playerlistAddPlayer(BKCurrentContent.getPlayerID())
                            except (IndexError, KeyError):
                                tofolderNum = BKFolderSelected
                        else:
                            oldfolder = BKCurrentContent.getParent()
                            theElement = BKCurrentContent.getChild()
                            if (type(theElement) != type(None)):
                                try:
                                    newfoldername = BKFolderListOrder[tofolderNum]
                                    newfolder = BKFolderLineDict[newfoldername]
                                    if (type(newfolder) != type(None)):
                                        if (newfolder.getType() == PtVaultNodeTypes.kAgeInfoNode):
                                            theElement = theElement.upcastToPlayerInfoNode()
                                            localplayer = PtGetLocalPlayer()
                                            if ((type(theElement) != type(None)) and (theElement.playerGetID() != localplayer.getPlayerID())):
                                                self.IInviteToVisit(theElement.playerGetID(), newfolder)
                                        elif (newfolder.getType() == PtVaultNodeTypes.kPlayerInfoListNode):
                                            theElement = theElement.upcastToPlayerInfoNode()
                                            localplayer = PtGetLocalPlayer()
                                            if ((type(theElement) != type(None)) and (theElement.playerGetID() != localplayer.getPlayerID())):
                                                theElement = theElement.upcastToPlayerInfoNode()
                                                newfolder.playerlistAddPlayer(theElement.playerGetID())
                                        else:
                                            copynoderef = newfolder.addNode(theElement)
                                            BKCurrentContent = copynoderef
                                            if (type(oldfolder) != type(None)):
                                                oldfolder.removeNode(theElement)
                                except (IndexError, KeyError):
                                    tofolderNum = BKFolderSelected
                        BKFolderSelectChanged = 1
                        self.IBigKIChangeMode(kBKListMode)
                        self.IRefreshPlayerList()
                        self.IRefreshPlayerListDisplay()
                elif (bkID == kBKRadioModeID):
                    if (BKFolderLineDict is BKJournalFolderDict):
                        BKJournalFolderSelected = BKFolderSelected
                        BKJournalFolderTopLine = BKFolderTopLine
                    elif (BKFolderLineDict is BKPlayerFolderDict):
                        BKPlayerFolderSelected = BKFolderSelected
                        BKPlayerFolderTopLine = BKFolderTopLine
                    elif (BKFolderLineDict is BKConfigFolderDict):
                        BKConfigFolderSelected = BKFolderSelected
                        BKConfigFolderTopLine = BKFolderTopLine
                    modeselect = control.getValue()
                    if (modeselect == 0):
                        BKFolderLineDict = BKJournalFolderDict
                        BKFolderListOrder = BKJournalListOrder
                        BKFolderSelected = BKJournalFolderSelected
                        BKFolderTopLine = BKJournalFolderTopLine
                    elif (modeselect == 1):
                        BKFolderLineDict = BKPlayerFolderDict
                        BKFolderListOrder = BKPlayerListOrder
                        BKFolderSelected = BKPlayerFolderSelected
                        BKFolderTopLine = BKPlayerFolderTopLine
                    else:
                        BKFolderLineDict = BKConfigFolderDict
                        BKFolderListOrder = BKConfigListOrder
                        BKFolderSelected = BKConfigFolderSelected
                        BKFolderTopLine = BKConfigFolderTopLine
                    self.IBigKIRefreshFolderDisplay()
                    if ((modeselect == 0) and ((BKRightSideMode == kBKPictureExpanded) or ((BKRightSideMode == kBKJournalExpanded) or (BKRightSideMode == kBKMarkerListExpanded)))):
                        self.IBigKIInvertToFolderButtons()
                    elif (modeselect == 2):
                        self.IShowSelectedConfig()
                    else:
                        self.IBigKIChangeMode(kBKListMode)
                elif (bkID == kBKIToPlayerButton):
                    if ((type(BKCurrentContent) != type(None)) and (type(BKPlayerSelected) != type(None))):
                        sendElement = BKCurrentContent.getChild()
                        toplayerbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKIToPlayerButton))
                        if (type(sendElement) != type(None)):
                            if isinstance(BKPlayerSelected, DeviceFolder):
                                pass
                            elif isinstance(BKPlayerSelected, Device):
                                PtDebugPrint(('xKI: send to device %s of type %s' % (BKPlayerSelected.name, BKPlayerSelected.type)), level=kDebugDumpLevel)
                                PtDebugPrint('xKI: send to device', level=kDebugDumpLevel)
                                vault = ptVault()
                                vault.sendToDevice(sendElement, BKPlayerSelected.name)
                                toplayerbtn.hide()
                            elif isinstance(BKPlayerSelected, ptVaultNode):
                                if (BKPlayerSelected.getType() == PtVaultNodeTypes.kPlayerInfoListNode):
                                    PtDebugPrint(('xKI: we are sending a message to the entire %s folder' % BKPlayerSelected.folderGetName()), level=kDebugDumpLevel)
                                    plyrreflist = BKPlayerSelected.getChildNodeRefList()
                                    for plyrref in plyrreflist:
                                        plyr = plyrref.getChild()
                                        plyr = plyr.upcastToPlayerInfoNode()
                                        if (type(plyr) != type(None)):
                                            sendElement.sendTo(plyr.playerGetID())

                                elif (BKPlayerSelected.getType() == PtVaultNodeTypes.kPlayerInfoNode):
                                    sendElement.sendTo(BKPlayerSelected.playerGetID())
                                else:
                                    self.ISetPlayerNotFound(xLocalization.xKI.xSendToErrorMessage1)
                                toplayerbtn.hide()
                            elif isinstance(BKPlayerSelected, ptVaultNodeRef):
                                plyrElement = BKPlayerSelected.getChild()
                                if ((type(plyrElement) != type(None)) and (plyrElement.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
                                    plyrElement = plyrElement.upcastToPlayerInfoNode()
                                    sendElement.sendTo(plyrElement.playerGetID())
                                else:
                                    self.ISetPlayerNotFound(xLocalization.xKI.xSendToErrorMessage2)
                                toplayerbtn.hide()
                            elif isinstance(BKPlayerSelected, ptPlayer):
                                sendElement.sendTo(BKPlayerSelected.getPlayerID())
                                toplayerbtn.hide()
                            else:
                                self.ISetPlayerNotFound(xLocalization.xKI.xSendToErrorMessage3)
                        else:
                            self.ISetPlayerNotFound(xLocalization.xKI.xSendToErrorMessage4)
            elif (event == kInterestingEvent):
                if (type(control) != type(None)):
                    shortTB = ptGUIControlTextBox(BigKI.dialog.getControlFromTag((control.getTagID() + 21)))
                    longTB = ptGUIControlTextBox(BigKI.dialog.getControlFromTag((control.getTagID() + 521)))
                    if ((shortTB.getStringJustify() == kRightJustify) and control.isInteresting()):
                        longTB.setForeColor(shortTB.getForeColor())
                        longTB.setString(shortTB.getString())
                        shortTB.hide()
                        longTB.show()
                    else:
                        shortTB.show()
                        longTB.hide()
        elif (id == KIListModeDialog.id):
            PtDebugPrint(('KIListMode::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if ((event == kAction) or (event == kValueChanged)):
                lmID = control.getTagID()
                if ((lmID >= kBKIListModeLineBtn01) and (lmID <= kBKIListModeLineBtnLast)):
                    whichone = ((lmID - kBKIListModeLineBtn01) + BKContentListTopLine)
                    if (whichone < len(BKContentList)):
                        theContent = BKContentList[whichone]
                        if (type(theContent) != type(None)):
                            BKCurrentContent = theContent
                            if isinstance(BKCurrentContent, QuestionNote):
                                nextmode = kBKQuestionNote
                                self.IBigKIChangeMode(nextmode)
                            elif isinstance(BKCurrentContent, ptPlayer):
                                nextmode = kBKPlayerExpanded
                                self.IBigKIChangeMode(nextmode)
                            else:
                                theElement = theContent.getChild()
                                if (type(theElement) != type(None)):
                                    datatype = theElement.getType()
                                    if (datatype == PtVaultNodeTypes.kTextNoteNode):
                                        nextmode = kBKJournalExpanded
                                    elif (datatype == PtVaultNodeTypes.kImageNode):
                                        nextmode = kBKPictureExpanded
                                    elif (datatype == PtVaultNodeTypes.kPlayerInfoNode):
                                        nextmode = kBKPlayerExpanded
                                    elif ((datatype == PtVaultNodeTypes.kMarkerListNode) and (PhasedKIShowMarkerGame and (gKIMarkerLevel >= kKIMarkerNormalLevel))):
                                        nextmode = kBKMarkerListExpanded
                                    else:
                                        BKCurrentContent = None
                                        nextmode = kBKListMode
                                    self.IBigKIChangeMode(nextmode)
                                else:
                                    PtDebugPrint('xBigKI: ListMode - content is None for element!', level=kErrorLevel)
                elif (lmID == kBKIListModeCreateBtn):
                    if (BKFolderLineDict is BKPlayerFolderDict):
                        BKGettingPlayerID = 1
                        self.IBigKIChangeMode(kBKPlayerExpanded)
                    else:
                        self.IBigKICreateJournalNote()
                        self.IBigKIChangeMode(kBKJournalExpanded)
                        self.IBigKIEnterEditMode(kBKEditFieldJRNTitle)
        elif (id == KIPictureExpanded.id):
            PtDebugPrint(('KIPicture::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kDialogLoaded):
                editbox = ptGUIControlEditBox(KIPictureExpanded.dialog.getControlFromTag(BKEditFieldIDs[kBKEditFieldPICTitle][kBKEditIDeditbox]))
                editbox.hide()
            elif (event == kShowHide):
                if control.isEnabled():
                    self.IBigKIDisplayCurrentContentImage()
            elif ((event == kAction) or (event == kValueChanged)):
                peID = control.getTagID()
                if (peID == kBKIPICTitleButton):
                    if self.IsContentMutable(BKCurrentContent):
                        self.IBigKIEnterEditMode(kBKEditFieldPICTitle)
                elif (peID == kBKIPICDeleteButton):
                    YNWhatReason = kYNDelete
                    elem = BKCurrentContent.getChild()
                    elem = elem.upcastToImageNode()
                    if (type(elem) != type(None)):
                        pictitle = elem.imageGetTitle()
                    else:
                        pictitle = '<unknown>'
                    yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                    yesText.setString((xLocalization.xKI.xDeletePictureAsk % xCensor.xCensor(pictitle, theCensorLevel)))
                    self.ILocalizeYesNoDialog()
                    KIYesNo.dialog.show()
                elif (peID == kBKIPICTitleEdit):
                    self.IBigKISaveEdit()
            elif (event == kFocusChange):
                if self.IsContentMutable(BKCurrentContent):
                    self.IBigKICheckFocusChange()
        elif (id == KIJournalExpanded.id):
            PtDebugPrint(('KIJournal::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kDialogLoaded):
                editbox = ptGUIControlEditBox(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[kBKEditFieldJRNTitle][kBKEditIDeditbox]))
                editbox.hide()
            elif (event == kShowHide):
                if control.isEnabled():
                    self.IBigKIDisplayCurrentContentJournal()
            elif ((event == kAction) or (event == kValueChanged)):
                jeID = control.getTagID()
                if (jeID == kBKIJRNTitleButton):
                    if self.IsContentMutable(BKCurrentContent):
                        self.IBigKIEnterEditMode(kBKEditFieldJRNTitle)
                elif (jeID == kBKIJRNNoteButton):
                    if self.IsContentMutable(BKCurrentContent):
                        self.IBigKIEnterEditMode(kBKEditFieldJRNNote)
                elif (jeID == kBKIJRNDeleteButton):
                    YNWhatReason = kYNDelete
                    elem = BKCurrentContent.getChild()
                    elem = elem.upcastToTextNoteNode()
                    if (type(elem) != type(None)):
                        jrntitle = elem.noteGetTitle()
                    else:
                        jrntitle = '<unknown>'
                    yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                    yesText.setString((xLocalization.xKI.xDeleteJournalAsk % xCensor.xCensor(jrntitle, theCensorLevel)))
                    self.ILocalizeYesNoDialog()
                    KIYesNo.dialog.show()
                elif ((jeID == kBKIJRNTitleEdit) or kBKIJRNNoteEdit):
                    if self.IsContentMutable(BKCurrentContent):
                        self.IBigKISaveEdit()
            elif (event == kFocusChange):
                if self.IsContentMutable(BKCurrentContent):
                    if (type(control) != type(None)):
                        jeID = control.getTagID()
                        if (jeID == kBKIJRNNote):
                            self.IBigKIEnterEditMode(kBKEditFieldJRNNote)
                            return
                    self.IBigKICheckFocusChange()
        elif (id == KIPlayerExpanded.id):
            PtDebugPrint(('KIJournal::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kShowHide):
                if control.isEnabled():
                    self.IBigKIDisplayCurrentContentPlayer()
            elif ((event == kAction) or (event == kValueChanged)):
                plID = control.getTagID()
                if (plID == kBKIPLYDeleteButton):
                    YNWhatReason = kYNDelete
                    elem = BKCurrentContent.getChild()
                    elem = elem.upcastToPlayerInfoNode()
                    if (type(elem) != type(None)):
                        plyrname = elem.playerGetName()
                    else:
                        plyrname = '<unknown>'
                    try:
                        pfldname = BKFolderListOrder[BKFolderSelected]
                    except LookupError:
                        pfldname = '<unknown>'
                    yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                    yesText.setString((xLocalization.xKI.xDeletePlayerAsk % (xCensor.xCensor(plyrname, theCensorLevel), pfldname)))
                    self.ILocalizeYesNoDialog()
                    KIYesNo.dialog.show()
                elif (plID == kBKIPLYPlayerIDEditBox):
                    self.IBigKICheckSavePlayer()
            elif (event == kFocusChange):
                if BKGettingPlayerID:
                    if KIPlayerExpanded.dialog.isEnabled():
                        plyIDedit = ptGUIControlEditBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYPlayerIDEditBox))
                        plyIDedit.focus()
                        KIPlayerExpanded.dialog.setFocus(plyIDedit.getKey())
                    else:
                        BKGettingPlayerID = 0
                        self.IBigKIChangeMode(kBKListMode)
        elif (id == KISettings.id):
            PtDebugPrint(('KISettings::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kShowHide):
                if control.isEnabled():
                    tfield = ptGUIControlTextBox(KISettings.dialog.getControlFromTag(kBKIKISettingsText))
                    tfield.setString(xLocalization.xKI.xKIConfiguration)
                    tfield = ptGUIControlTextBox(KISettings.dialog.getControlFromTag(kBKIKIFontSizeText))
                    tfield.setString(xLocalization.xKI.xKISettingsFontSizeText)
                    tfield = ptGUIControlTextBox(KISettings.dialog.getControlFromTag(kBKIKIFadeTimeText))
                    tfield.setString(xLocalization.xKI.xKISettingChatFadeTimeText)
                    tfield = ptGUIControlTextBox(KISettings.dialog.getControlFromTag(kBKIKIOnlyPMText))
                    tfield.setString(xLocalization.xKI.xKISettingsOnlyBuddiesText)
                    self.IRefreshKISettings()
                else:
                    self.ISaveFontSize()
                    self.ISaveFadeTime()
                    self.ISaveKIFlags()
            elif ((event == kAction) or (event == kValueChanged)):
                kiID = control.getTagID()
                if (kiID == kBKIKIFontSize):
                    slidePerFont = (float(((control.getMax() - control.getMin()) + 1.0)) / float(len(FontSizeList)))
                    fontIndex = int(((control.getValue() / slidePerFont) + 0.25))
                    if (fontIndex >= len(FontSizeList)):
                        fontIndex = (len(FontSizeList) - 1)
                    self.ISetFontSize(FontSizeList[fontIndex])
                elif (kiID == kBKIKIFadeTime):
                    slidePerTime = (float((control.getMax() - control.getMin())) / float(kFadeTimeMax))
                    TicksOnFull = int(((control.getValue() / slidePerTime) + 0.25))
                    PtDebugPrint(('KISettings: FadeTime set to %d' % TicksOnFull), level=kWarningLevel)
                    if (TicksOnFull == kFadeTimeMax):
                        FadeEnableFlag = 0
                        PtDebugPrint('KISettings: FadeTime disabled', level=kWarningLevel)
                    else:
                        FadeEnableFlag = 1
                        PtDebugPrint('KISettings: FadeTime enabled', level=kWarningLevel)
                elif (kiID == kBKIKIOnlyPM):
                    OnlyGetPMsFromBuddies = control.isChecked()
                elif (kiID == kBKIKIBuddyCheck):
                    OnlyAllowBuddiesOnRequest = control.isChecked()
        elif (id == KIVolumeExpanded.id):
            PtDebugPrint(('KIVolume::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kShowHide):
                if control.isEnabled():
                    self.IRefreshVolumeSettings()
            elif ((event == kAction) or (event == kValueChanged)):
                plID = control.getTagID()
                audio = ptAudioControl()
                if (plID == kBKISoundFXVolSlider):
                    setting = control.getValue()
                    PtDebugPrint(('SoundFX being changed to %g (into %g)' % (setting, (setting / 10))), level=kDebugDumpLevel)
                    audio.setSoundFXVolume((setting / 10))
                elif (plID == xBKIMusicVolSlider):
                    setting = control.getValue()
                    PtDebugPrint(('Music being changed to %g (into %g)' % (setting, (setting / 10))), level=kDebugDumpLevel)
                    audio.setMusicVolume((setting / 10))
                elif (plID == xBKIVoiceVolSlider):
                    setting = control.getValue()
                    PtDebugPrint(('Voice being changed to %g (into %g)' % (setting, (setting / 10))), level=kDebugDumpLevel)
                    audio.setVoiceVolume((setting / 10))
                elif (plID == kBKIAmbienceVolSlider):
                    setting = control.getValue()
                    PtDebugPrint(('Ambience being changed to %g (into %g)' % (setting, (setting / 10))), level=kDebugDumpLevel)
                    audio.setAmbienceVolume((setting / 10))
                elif (plID == kBKIMicLevelSlider):
                    setting = control.getValue()
                    PtDebugPrint(('MicLevel being changed to %g (into %g)' % (setting, (setting / 10))), level=kDebugDumpLevel)
                    audio.setMicLevel((setting / 10))
                elif (plID == kBKIGUIVolSlider):
                    setting = control.getValue()
                    PtDebugPrint(('MicLevel being changed to %g (into %g)' % (setting, (setting / 10))), level=kDebugDumpLevel)
                    audio.setGUIVolume((setting / 10))
        elif (id == KIAgeOwnerExpanded.id):
            PtDebugPrint(('KIAgeOwner::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kShowHide):
                if control.isEnabled():
                    tfield = ptGUIControlTextBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerDescriptionTitle))
                    tfield.setString(xLocalization.xKI.xKIDescriptionText)
                    titleedit = ptGUIControlEditBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleEditbox))
                    titleedit.hide()
                    self.IRefreshAgeOwnerSettings()
            elif ((event == kAction) or (event == kValueChanged)):
                plID = control.getTagID()
                if (plID == kBKAgeOwnerMakePublicBtn):
                    PtDebugPrint('KIAgeOwner: make public button hit', level=kDebugDumpLevel)
                    try:
                        vault = ptVault()
                        myAge = BKConfigFolderDict[BKConfigListOrder[BKFolderSelected]]
                        myAgeStruct = myAge.asAgeInfoStruct()
                        makePublic = 1
                        if myAge.isPublic():
                            makePublic = 0
                            PtDebugPrint(('KIAgeOwner: making %s private' % myAge.getDisplayName()), level=kDebugDumpLevel)
                        else:
                            PtDebugPrint(('KIAgeOwner: making %s public' % myAge.getDisplayName()), level=kDebugDumpLevel)
                        vault.setAgePublic(myAgeStruct, makePublic)
                        control.disable()
                    except AttributeError:
                        PtDebugPrint('KIAgeOwner: change public/private error', level=kErrorLevel)
                elif (plID == kBKAgeOwnerTitleBtn):
                    PtDebugPrint('KIAgeOwner: change title button hit', level=kDebugDumpLevel)
                    control.disable()
                    title = ptGUIControlTextBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleTB))
                    title.hide()
                    titleedit = ptGUIControlEditBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleEditbox))
                    try:
                        myAge = BKConfigFolderDict[BKConfigListOrder[BKFolderSelected]]
                        titleedit.setString(myAge.getAgeUserDefinedName())
                    except LookupError:
                        titleedit.setString('')
                    titleedit.show()
                    titleedit.end()
                    KIAgeOwnerExpanded.dialog.setFocus(titleedit.getKey())
                elif (plID == kBKAgeOwnerTitleEditbox):
                    PtDebugPrint('KIAgeOwner: edit field set', level=kDebugDumpLevel)
                    self.ISaveUserNameFromEdit(control)
            elif (event == kFocusChange):
                PtDebugPrint('KIAgeOwner: focus change', level=kDebugDumpLevel)
                titleedit = ptGUIControlEditBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleEditbox))
                if titleedit.isVisible():
                    if ((type(control) == type(None)) or ((control.getTagID() != kBKAgeOwnerTitleEditbox) and (control.getTagID() != kBKAgeOwnerTitleBtn))):
                        self.ISaveUserNameFromEdit(titleedit)
                if (type(control) != type(None)):
                    plID = control.getTagID()
                    if (plID == kBKAgeOwnerDescription):
                        BKAgeOwnerEditDescription = 1
                        PtDebugPrint('KIAgeOwner: start edit of description', level=kDebugDumpLevel)
                    else:
                        if BKAgeOwnerEditDescription:
                            descript = ptGUIControlMultiLineEdit(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerDescription))
                            myAge = BKConfigFolderDict[BKConfigListOrder[BKFolderSelected]]
                            if (type(myAge) != type(None)):
                                PtDebugPrint(('KIAgeOwner: age description updated for %s' % myAge.getDisplayName()), level=kDebugDumpLevel)
                                myAge.setAgeDescription(descript.getString())
                                myAge.save()
                            else:
                                PtDebugPrint('KIAgeOwner: neighborhood is None while trying to update description', level=kDebugDumpLevel)
                        BKAgeOwnerEditDescription = 0
                else:
                    if BKAgeOwnerEditDescription:
                        descript = ptGUIControlMultiLineEdit(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerDescription))
                        myAge = BKConfigFolderDict[BKConfigListOrder[BKFolderSelected]]
                        if (type(myAge) != type(None)):
                            PtDebugPrint(('KIAgeOwner: age description updated for %s' % myAge.getDisplayName()), level=kDebugDumpLevel)
                            buf = descript.getEncodedBuffer()
                            myAge.setAgeDescription(str(buf))
                            myAge.save()
                        else:
                            PtDebugPrint('KIAgeOwner: neighborhood is None while trying to update description', level=kDebugDumpLevel)
                    BKAgeOwnerEditDescription = 0
        elif (id == KIYesNo.id):
            if ((event == kAction) or (event == kValueChanged)):
                ynID = control.getTagID()
                if (YNWhatReason in [kYNQuit, kYNForceQuit]):
                    if (ynID == kYesButtonID):
                        PtConsole('app.quit')
                    elif (ynID == kNoButtonID):
                        KIYesNo.dialog.hide()
                elif (YNWhatReason == kYNDelete):
                    if (ynID == kYesButtonID):
                        if (type(BKCurrentContent) != type(None)):
                            del_folder = BKCurrentContent.getParent()
                            del_elem = BKCurrentContent.getChild()
                            if ((type(del_folder) != type(None)) and (type(del_elem) != type(None))):
                                tfolder = del_folder.upcastToFolderNode()
                                if ((type(tfolder) != type(None)) and (tfolder.folderGetType() == PtVaultStandardNodes.kCanVisitFolder)):
                                    PtDebugPrint('xKI:del: revoking visitor', level=kDebugDumpLevel)
                                    del_elem = del_elem.upcastToPlayerInfoNode()
                                    agefoldername = BKFolderListOrder[BKFolderSelected]
                                    agefolder = BKFolderLineDict[agefoldername]
                                    self.IRevokeToVisit(del_elem.playerGetID(), agefolder)
                                elif ((del_folder.getType() == PtVaultNodeTypes.kPlayerInfoListNode) and (del_elem.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
                                    PtDebugPrint('xKI:del: removing player from folder', level=kDebugDumpLevel)
                                    del_folder = del_folder.upcastToPlayerInfoListNode()
                                    del_elem = del_elem.upcastToPlayerInfoNode()
                                    del_folder.playerlistRemovePlayer(del_elem.playerGetID())
                                    BKPlayerSelected = None
                                    sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
                                    sendToField.setString(' ')
                                else:
                                    if (del_elem.getType() == PtVaultNodeTypes.kMarkerListNode):
                                        mg = ptMarkerMgr()
                                        mg.hideMarkersLocal()
                                        mg.clearWorkingMarkerFolder()
                                    BKCurrentContent = None
                                    del_folder.removeNode(del_elem)
                                    PtDebugPrint('xKI:del: deleting element from folder', level=kDebugDumpLevel)
                            else:
                                PtDebugPrint('xKI: tried to delete bad vaultnode or delete from bad folder', level=kErrorLevel)
                            self.IBigKIChangeMode(kBKListMode)
                            self.IRefreshPlayerList()
                            self.IRefreshPlayerListDisplay()
                    elif (ynID == kNoButtonID):
                        pass
                    YNWhatReason = kYNQuit
                    KIYesNo.dialog.hide()
                elif (YNWhatReason == kYNOfferLink):
                    YNWhatReason = kYNQuit
                    KIYesNo.dialog.hide()
                    if (ynID == kYesButtonID):
                        if (type(OfferLinkFromWho) != type(None)):
                            PtDebugPrint(('xKI: Linking to offered age %s' % OfferLinkFromWho.getDisplayName()), level=kDebugDumpLevel)
                            link = ptAgeLinkStruct()
                            link.setLinkingRules(PtLinkingRules.kBasicLink)
                            link.setAgeInfo(OfferLinkFromWho)
                            ptNetLinkingMgr().linkToAge(link)
                            OfferLinkFromWho = None
                    elif (ynID == kNoButtonID):
                        pass
                    OfferLinkFromWho = None
                elif (YNWhatReason == kYNOutside):
                    YNWhatReason = kYNQuit
                    KIYesNo.dialog.hide()
                    if (type(YNOutsideSender) != type(None)):
                        note = ptNotify(self.key)
                        note.clearReceivers()
                        note.addReceiver(YNOutsideSender)
                        note.netPropagate(0)
                        note.netForce(0)
                        if (ynID == kYesButtonID):
                            note.setActivate(1)
                            note.addVarNumber('YesNo', 1)
                        elif (ynID == kNoButtonID):
                            note.setActivate(0)
                            note.addVarNumber('YesNo', 0)
                        note.send()
                    YNOutsideSender = None
                elif (YNWhatReason == kYNKIFull):
                    KIYesNo.dialog.hide()
                    noButton = ptGUIControlButton(KIYesNo.dialog.getControlFromTag(kNoButtonID))
                    noButton.show()
                    noBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
                    noBtnText.show()
                    yesBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
                    yesBtnText.setString(xLocalization.xKI.xYesNoYESbutton)
                    YNWhatReason = kYNQuit
                else:
                    YNWhatReason = kYNQuit
                    KIYesNo.dialog.hide()
                    noButton = ptGUIControlButton(KIYesNo.dialog.getControlFromTag(kNoButtonID))
                    noButton.show()
                    noBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
                    noBtnText.show()
                    yesBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
                    yesBtnText.setString(xLocalization.xKI.xYesNoYESbutton)
                    YNOutsideSender = None
            elif (event == kExitMode):
                if (YNWhatReason == kYNForceQuit):
                    PtConsole('app.quit')
                YNWhatReason = kYNQuit
                KIYesNo.dialog.hide()
                noButton = ptGUIControlButton(KIYesNo.dialog.getControlFromTag(kNoButtonID))
                noButton.show()
                noBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
                noBtnText.show()
                yesBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
                yesBtnText.setString(xLocalization.xKI.xYesNoYESbutton)
                YNOutsideSender = None
        elif (id == KIRateIt.id):
            if ((event == kAction) or (event == kValueChanged)):
                ynID = control.getTagID()
        elif (id == NewItemAlert.id):
            if (event == kDialogLoaded):
                kialert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertKIAlert))
                kialert.disable()
                kialert.hide()
                bookalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertBookAlert))
                bookalert.disable()
                bookalert.hide()
                journalalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertJournalAlert))
                journalalert.disable()
                journalalert.hide()
                microjournalalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertMicroJournalAlert))
                microjournalalert.disable()
                microjournalalert.hide()
            elif (event == kShowHide):
                if control.isEnabled():
                    self.IAlertStartTimer()
        elif (id == KIMarkerFolderExpanded.id):
            if (event == kDialogLoaded):
                typeField = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderGameTimeTB))
                typeField.setString(xLocalization.xKI.xMarkerFolderPopupMenu[MarkerGameTimeID][0])
            elif (event == kShowHide):
                if control.isEnabled():
                    titleedit = ptGUIControlEditBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTitleEB))
                    titleedit.hide()
                    markeredit = ptGUIControlEditBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerTextEB))
                    markeredit.hide()
                    self.IBigKIDisplayCurrentContentMarkerFolder()
            elif ((event == kAction) or (event == kValueChanged)):
                mfldrID = control.getTagID()
                if (mfldrID == kMarkerFolderEditStartGame):
                    PtDebugPrint('xKI:Marker: Hit the MF Edit/Start game button', level=kDebugDumpLevel)
                    if (MFdialogMode == kMFOverview):
                        PtDebugPrint('xKI:Marker: must be edit game button')
                        self.ISetWorkingToCurrentMarkerFolder()
                        ptMarkerMgr().showMarkersLocal()
                    elif (MFdialogMode == kMFEditing):
                        PtDebugPrint('xKI:Marker: must be done editing button')
                        self.IResetWorkingMarkerFolder()
                        ptMarkerMgr().hideMarkersLocal()
                    elif (MFdialogMode == kMFPlaying):
                        PtDebugPrint('xKI:Marker: must be stop playing button for quests / start game for non-quests')
                        workingMF = ptMarkerMgr().getWorkingMarkerFolder()
                        if (type(workingMF) != type(None)):
                            if (workingMF.getGameType() == PtMarkerMsgGameType.kGameTypeQuest):
                                ptMarkerMgr().endGame()
                            else:
                                ptMarkerMgr().startGame()
                                self.IminiToggleKISize()
                    elif (MFdialogMode == kMFEditingMarker):
                        PtDebugPrint('xKI:Marker: must be marker list button')
                        ptMarkerMgr().clearSelectedMarker()
                        self.IBKCheckContentRefresh(BKCurrentContent)
                elif (mfldrID == kMarkerFolderPlayEndGame):
                    PtDebugPrint('xKI:Marker: Hit the MF Play/End game button', level=kDebugDumpLevel)
                    if (MFdialogMode == kMFOverview):
                        PtDebugPrint('xKI:Marker: must be play game button')
                        element = self.ISetWorkingToCurrentMarkerFolder()
                        if element:
                            ptMarkerMgr().createGame(element.getRoundLength(), element.getGameType(), [])
                            self.IRefreshPlayerList()
                            self.IRefreshPlayerListDisplay()
                    elif (MFdialogMode == kMFEditing):
                        PtDebugPrint('xKI:Marker: must be add marker button')
                        self.ICreateAMarker()
                    elif (MFdialogMode == kMFPlaying):
                        PtDebugPrint('xKI:Marker: must be reset game button for quests / end game for non-quests')
                        workingMF = ptMarkerMgr().getWorkingMarkerFolder()
                        if (type(workingMF) != type(None)):
                            if (workingMF.getGameType() == PtMarkerMsgGameType.kGameTypeQuest):
                                ptMarkerMgr().endGame()
                                markerRefs = workingMF.getChildNodeRefList()
                                for markerRef in markerRefs:
                                    markerRef.unsetSeen()

                                element = self.ISetWorkingToCurrentMarkerFolder()
                                if element:
                                    ptMarkerMgr().createGame(element.getRoundLength(), element.getGameType(), [])
                                self.IBKCheckContentRefresh(BKCurrentContent)
                            else:
                                self.IDoStatusChatMessage(xLocalization.xKI.xMarkerGamePrematureEnding, netPropagate=1)
                                ptMarkerMgr().endGame()
                    elif (MFdialogMode == kMFEditingMarker):
                        PtDebugPrint('xKI:Marker: must be remvoe marker button')
                        mfelement = self.IGetCurrentMarkerFolder()
                        selID = ptMarkerMgr().getSelectedMarker()
                        if (selID and mfelement):
                            markerRefs = mfelement.getChildNodeRefList()
                            for markerRef in markerRefs:
                                marker = markerRef.getChild()
                                if marker:
                                    marker = marker.upcastToMarkerNode()
                                    if marker:
                                        if (marker.getID() == selID):
                                            mfelement.removeNode(marker)

                        ptMarkerMgr().clearSelectedMarker()
                        self.IBKCheckContentRefresh(BKCurrentContent)
                elif (mfldrID == kMarkerFolderMarkListbox):
                    workingMF = ptMarkerMgr().getWorkingMarkerFolder()
                    if (type(workingMF) != type(None)):
                        markerlistSelectable = 1
                        if (workingMF.getGameType() == PtMarkerMsgGameType.kGameTypeQuest):
                            if ptMarkerMgr().isGameRunning():
                                markerlistSelectable = 0
                        if markerlistSelectable:
                            markersel = control.getSelection()
                            mfelement = self.IGetCurrentMarkerFolder()
                            if mfelement:
                                markerRefs = mfelement.getChildNodeRefList()
                                try:
                                    marker = markerRefs[markersel].getChild()
                                    marker = marker.upcastToMarkerNode()
                                    if marker:
                                        ptMarkerMgr().setSelectedMarker(marker.getID())
                                        self.IBKCheckContentRefresh(BKCurrentContent)
                                except LookupError:
                                    pass
                elif (mfldrID == kMarkerFolderInvitePlayer):
                    PtDebugPrint('xKI:Marker: inviting a player', level=kDebugDumpLevel)
                    if (type(WorkingMarkerFolder) != type(None)):
                        userlbx = ptGUIControlListBox(KIMini.dialog.getControlFromTag(kPlayerList))
                        iselect = userlbx.getSelection()
                        if ((iselect >= 0) and (iselect < len(BKPlayerList))):
                            PtDebugPrint('xKI:Marker: valid player selection', level=kDebugDumpLevel)
                            toplyr = BKPlayerList[iselect]
                            if isinstance(toplyr, ptPlayer):
                                newplayer = 1
                                for mplayer in WorkingMarkerFolder.invitedPlayers:
                                    if (mplayer.ID == toplyr.getPlayerID()):
                                        newplayer = 0
                                        break

                                if newplayer:
                                    PtDebugPrint(('xKI:Marker: inviting player %s [%d] to the game' % (toplyr.getPlayerName(), toplyr.getPlayerID())), level=kDebugDumpLevel)
                                    WorkingMarkerFolder.invitedPlayers.append(MarkerPlayer(toplyr.getPlayerID()))
                                    ptMarkerMgr().invitePlayers([long(toplyr.getPlayerID())])
                                    self.IRefreshPlayerList()
                                    self.IRefreshPlayerListDisplay()
                            elif isinstance(toplyr, ptVaultPlayerInfoListNode):
                                PtDebugPrint('xKI:Marker: playerinfo list', level=kDebugDumpLevel)
                                plistnode = toplyr.upcastToPlayerInfoListNode()
                                ageplayers = self.IRemoveCCRPlayers(PtGetPlayerListDistanceSorted())
                                inviting = []
                                if (type(plistnode) == type(None)):
                                    PtDebugPrint('xKI:InvitePlayers: folder is AgePlayers', level=kDebugDumpLevel)
                                    for aplayer in ageplayers:
                                        inviting.append(long(aplayer.getPlayerID()))
                                        WorkingMarkerFolder.invitedPlayers.append(MarkerPlayer(aplayer.getPlayerID()))

                                elif (plistnode.folderGetType() == PtVaultStandardNodes.kBuddyListFolder):
                                    PtDebugPrint('xKI:InvitePlayers: folder is BuddyList', level=kDebugDumpLevel)
                                    buddies = ptVault().getBuddyListFolder()
                                    budlist = buddies.getChildNodeRefList()
                                    for bud in budlist:
                                        buddy = bud.getChild().upcastToPlayerInfoNode()
                                        for aplayer in ageplayers:
                                            if (aplayer.getPlayerID() == buddy.playerGetID()):
                                                inviting.append(long(aplayer.getPlayerID()))
                                                WorkingMarkerFolder.invitedPlayers.append(MarkerPlayer(aplayer.getPlayerID()))


                                elif (plistnode.folderGetType() == PtVaultStandardNodes.kAgeOwnersFolder):
                                    PtDebugPrint('xKI:InvitePlayers: folder is Neighbors', level=kDebugDumpLevel)
                                    neighbors = self.IGetNeighbors()
                                    if (type(neighbors) != type(None)):
                                        neighborlist = neighbors.getChildNodeRefList()
                                        for neighbor in neighborlist:
                                            hoody = neighbor.getChild().upcastToPlayerInfoNode()
                                            for aplayer in ageplayers:
                                                if (aplayer.getPlayerID() == hoody.playerGetID()):
                                                    inviting.append(long(aplayer.getPlayerID()))
                                                    WorkingMarkerFolder.invitedPlayers.append(MarkerPlayer(aplayer.getPlayerID()))


                                if (len(inviting) > 0):
                                    ptMarkerMgr().invitePlayers(inviting)
                                self.IRefreshPlayerList()
                                self.IRefreshPlayerListDisplay()
                            elif isinstance(toplyr, kiFolder):
                                ageplayers = self.IRemoveCCRPlayers(PtGetPlayerListDistanceSorted())
                                inviting = []
                                PtDebugPrint('xKI:InvitePlayers: folder is AgePlayers', level=kDebugDumpLevel)
                                for aplayer in ageplayers:
                                    inviting.append(long(aplayer.getPlayerID()))
                                    WorkingMarkerFolder.invitedPlayers.append(MarkerPlayer(aplayer.getPlayerID()))

                                if (len(inviting) > 0):
                                    ptMarkerMgr().invitePlayers(inviting)
                                self.IRefreshPlayerList()
                                self.IRefreshPlayerListDisplay()
                            else:
                                PtDebugPrint('xKI:Marker: unknown class type', level=kDebugDumpLevel)
                elif (mfldrID == kMarkerFolderTitleBtn):
                    PtDebugPrint('KIMarkerFolder: change title button hit', level=kDebugDumpLevel)
                    control.disable()
                    title = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTitleText))
                    titleedit = ptGUIControlEditBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTitleEB))
                    titleedit.setString(title.getString())
                    title.hide()
                    titleedit.show()
                    titleedit.end()
                    KIMarkerFolderExpanded.dialog.setFocus(titleedit.getKey())
                elif (mfldrID == kMarkerFolderTitleEB):
                    PtDebugPrint('KIMarkerFolder: edit field set', level=kDebugDumpLevel)
                    self.ISaveMarkerFolderNameFromEdit(control)
                elif (mfldrID == kMarkerFolderMarkerTextBtn):
                    PtDebugPrint('KIMarkerFolder: change marker text button hit', level=kDebugDumpLevel)
                    control.disable()
                    title = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerTextTB))
                    titleedit = ptGUIControlEditBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerTextEB))
                    titleedit.setString(title.getString())
                    title.hide()
                    titleedit.show()
                    titleedit.end()
                    KIMarkerFolderExpanded.dialog.setFocus(titleedit.getKey())
                elif (mfldrID == kMarkerFolderMarkerTextEB):
                    PtDebugPrint('KIMarkerFolder: edit field set', level=kDebugDumpLevel)
                    self.ISaveMarkerTextFromEdit(control)
                elif ((mfldrID == kMarkerFolderTimePullDownBtn) or (mfldrID == kMarkerFolderTimeArrow)):
                    KIMarkerFolderPopupMenu.menu.show()
                elif ((mfldrID == kMarkerFolderTypePullDownBtn) or (mfldrID == kMarkerFolderTypeArrow)):
                    KIMarkerTypePopupMenu.menu.show()
                elif (mfldrID == kMarkerFolderDeleteBtn):
                    YNWhatReason = kYNDelete
                    elem = BKCurrentContent.getChild()
                    elem = elem.upcastToMarkerListNode()
                    if (type(elem) != type(None)):
                        mftitle = elem.folderGetName()
                    else:
                        mftitle = '<unknown>'
                    yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                    yesText.setString((xLocalization.xKI.xDeletePictureAsk % xCensor.xCensor(mftitle, theCensorLevel)))
                    self.ILocalizeYesNoDialog()
                    KIYesNo.dialog.show()
            elif (event == kFocusChange):
                PtDebugPrint('KIMarkerFolder: focus change', level=kDebugDumpLevel)
                titleedit = ptGUIControlEditBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTitleEB))
                if titleedit.isVisible():
                    if ((type(control) == type(None)) or ((control.getTagID() != kMarkerFolderTitleEB) and (control.getTagID() != kMarkerFolderTitleBtn))):
                        self.ISaveMarkerFolderNameFromEdit(titleedit)
                if (MFdialogMode == kMFEditingMarker):
                    titleedit = ptGUIControlEditBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerTextEB))
                    if titleedit.isVisible():
                        if ((type(control) == type(None)) or ((control.getTagID() != kMarkerFolderMarkerTextEB) and (control.getTagID() != kMarkerFolderMarkerTextBtn))):
                            self.ISaveMarkerTextFromEdit(titleedit)
        elif (id == KIMarkerFolderPopupMenu.id):
            if (event == kDialogLoaded):
                for menuItem in xLocalization.xKI.xMarkerFolderPopupMenu:
                    KIMarkerFolderPopupMenu.menu.addNotifyItem(menuItem[0])

            elif (event == kAction):
                menuID = control.getTagID()
                MarkerGameTimeID = menuID
                typeField = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderGameTimeTB))
                typeField.setString(xLocalization.xKI.xMarkerFolderPopupMenu[MarkerGameTimeID][0])
                if (type(BKCurrentContent) != type(None)):
                    element = BKCurrentContent.getChild()
                    if (type(element) != type(None)):
                        datatype = element.getType()
                        if (datatype == PtVaultNodeTypes.kMarkerListNode):
                            element = element.upcastToMarkerListNode()
                            if element:
                                element.setRoundLength(xLocalization.xKI.xMarkerFolderPopupMenu[MarkerGameTimeID][1])
                                element.save()
            elif (event == kExitMode):
                if KIMarkerFolderPopupMenu.menu.isEnabled():
                    KIMarkerFolderPopupMenu.menu.hide()
                elif KIMarkerTypePopupMenu.menu.isEnabled():
                    KIMarkerTypePopupMenu.menu.hide()
        elif (id == KIMarkerTypePopupMenu.id):
            if (event == kDialogLoaded):
                KIMarkerTypePopupMenu.menu.addNotifyItem(xLocalization.xKI.xMarkerGameQuestGame)
                #KIMarkerTypePopupMenu.menu.addNotifyItem(xLocalization.xKI.xMarkerGameHoldGame)
                #KIMarkerTypePopupMenu.menu.addNotifyItem(xLocalization.xKI.xMarkerGameCaptureGame)
                # There are at least two problems preventing team games from working:
                # - When inviting a player, the game master also receives the "creaate" and "add" messages, so the old game is removed and a new one created
                # - When the invitee accepts the invite, the only thing happening is a "join" message to the game master containing the ID of the team set by the invitee - but without the invitee's ID or anything
                # While I could work around this using the UserKI's "RemoteCall" system, I doubt these are te only issues... Cyan simply never finished designing or implementing this :(
            elif (event == kAction):
                menuID = control.getTagID()
                typeField = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderGameTypeTB))
                if (menuID == 0):
                    typeField.setString(xLocalization.xKI.xMarkerGameQuestGame)
                    gametype = PtMarkerMsgGameType.kGameTypeQuest
                elif (menuID == 1):
                    typeField.setString(xLocalization.xKI.xMarkerGameHoldGame)
                    gametype = PtMarkerMsgGameType.kGameTypeHold
                elif (menuID == 2):
                    typeField.setString(xLocalization.xKI.xMarkerGameCaptureGame)
                    gametype = PtMarkerMsgGameType.kGameTypeCapture
                else: return
                if (type(BKCurrentContent) != type(None)):
                    element = BKCurrentContent.getChild()
                    if (type(element) != type(None)):
                        datatype = element.getType()
                        if (datatype == PtVaultNodeTypes.kMarkerListNode):
                            element = element.upcastToMarkerListNode()
                            if element:
                                element.setGameType(gametype)
                                element.save()
            elif (event == kExitMode):
                if KIMarkerFolderPopupMenu.menu.isEnabled():
                    KIMarkerFolderPopupMenu.menu.hide()
                elif KIMarkerTypePopupMenu.menu.isEnabled():
                    KIMarkerTypePopupMenu.menu.hide()
        elif (id == KIQuestionNote.id):
            PtDebugPrint(('KIQuestion::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kShowHide):
                if control.isEnabled():
                    self.IBigKIDisplayCurrentQuestionNote()
            elif ((event == kAction) or (event == kValueChanged)):
                qnID = control.getTagID()
                if (qnID == kQNAcceptBtn):
                    try:
                        BKCurrentContent.YesAction()
                        self.IBKCheckFolderRefresh(ptVault().getInbox())
                        self.IBigKIChangeMode(kBKListMode)
                    except AttributeError:
                        pass
                elif (qnID == kQNDeclineBtn):
                    try:
                        BKCurrentContent.NoAction()
                        self.IBKCheckFolderRefresh(ptVault().getInbox())
                        self.IBigKIChangeMode(kBKListMode)
                    except AttributeError:
                        pass
                # just in case something was updated (like the marker join request "YesAction")
                self.IRefreshPlayerList()
                self.IRefreshPlayerListDisplay()
#Jalak
        elif (id == KIJalakGUIDialog.id):
            if (event == kDialogLoaded):
                self.JalakGUIInit()
            elif ((event == kAction) or (event == kValueChanged)):
                if (type(control) != type(None)):
                    tagID = control.getTagID()
                    btn = str(tagID)
                    if (btn in JalakBtnStates):
                        KIJalakBtnLights.run(self.key, state=btn, netPropagate=0)
                        self.SetJalakGUIButtons(0)
#/Jalak



    def OnKIMsg(self, command, value):
        global IminiKIWasUp
        global FadeEnableFlag
        global PhasedKIInterAgeChat
        global YNOutsideSender
        global PrivateChatChannel
        global PhasedKICreateNotes
        global gGZMarkerInRangeRepy
        global PhasedKIBuddies
        global PhasedKIPlayMarkerGame
        global IsYeeshaBookEnabled
        global IKIHardDisabled
        global PhasedKISendImages
        global IAmAdmin
        global TicksOnFull
        global IKIDisabled
        global IsEntireYeeshaBookEnabled
        global gGZMarkerInRange
        global PhasedKINeighborsInDPL
        global PhasedKICreateImages
        global theKILevel
        global PhasedKISendNotes
        global PhasedKICreateMarkerGame
        global PhasedKIShowMarkerGame
        global PhasedKISendMarkerGame
        global PhasedKIShareYeeshaBook
        global YNWhatReason
##############################################################################
# D'Lanor's Alcugs GPS fix
##############################################################################
        global gShowGPSCheat
##############################################################################
# End D'Lanor's Alcugs GPS fix
##############################################################################
        # clear afk information list
        global gAfkInformed
        # /clear afk information list
        PtDebugPrint(('xKI: KIMsg: command = %d value =' % command), value, level=kDebugDumpLevel)
        if (command == kEnterChatMode):
            if ((not IKIDisabled) and (not PtIsSinglePlayerMode())):
                self.IEnterChatMode(1)
        elif (command == kSetChatFadeDelay):
            TicksOnFull = value
        elif (command == kSetTextChatAdminMode):
            IAmAdmin = value
        elif (command == kDisableKIandBB):
            PtDebugPrint('xKI: Disable KI', level=kDebugDumpLevel)
            # clear afk information list
            gAfkInformed = {}
            # /clear afk information list
            IKIDisabled = 1
            IKIHardDisabled = 1
            if (theKILevel == kNanoKI):
                KINanoBlackBar.dialog.hide()
            elif PtIsSinglePlayerMode():
                KIMicroBlackbar.dialog.hide()
            elif (theKILevel == kMicroKI):
                KIMicroBlackbar.dialog.hide()
                if KIMicro.dialog.isEnabled():
                    IminiKIWasUp = 1
                    KIMicro.dialog.hide()
                else:
                    IminiKIWasUp = 0
            else:
                KIBlackbar.dialog.hide()
                if KIMini.dialog.isEnabled():
                    IminiKIWasUp = 1
                    KIMini.dialog.hide()
                else:
                    IminiKIWasUp = 0
                if (not WaitingForAnimation):
                    KIListModeDialog.dialog.hide()
                    KIPictureExpanded.dialog.hide()
                    KIJournalExpanded.dialog.hide()
                    KIPlayerExpanded.dialog.hide()
                    BigKI.dialog.hide()
                    KIOnAnim.animation.skipToTime(1.5)
            if (YNWhatReason == kYNOutside):
                if (type(YNOutsideSender) != type(None)):
                    note = ptNotify(self.key)
                    note.clearReceivers()
                    note.addReceiver(YNOutsideSender)
                    note.netPropagate(0)
                    note.netForce(0)
                    note.setActivate(0)
                    note.addVarNumber('YesNo', 0)
                    note.send()
                YNOutsideSender = None
            if YeeshaBook:
                YeeshaBook.hide()
            if JournalBook:
                JournalBook.hide()
            PtToggleAvatarClickability(true)
            plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
            plybkCB.setChecked(0)
            plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID))
            plybkCB.setChecked(0)
            YNWhatReason = kYNQuit
            KIYesNo.dialog.hide()
        elif (command == kEnableKIandBB):
            PtDebugPrint('xKI: Enable KI', level=kDebugDumpLevel)
            IKIDisabled = 0
            IKIHardDisabled = 0
            if (theKILevel == kNanoKI):
                KINanoBlackBar.dialog.show()
            elif PtIsSinglePlayerMode():
                KIMicroBlackbar.dialog.show()
            elif (theKILevel == kMicroKI):
                KIMicroBlackbar.dialog.show()
                if IminiKIWasUp:
                    KIMicro.dialog.show()
            else:
                KIBlackbar.dialog.show()
                if IminiKIWasUp:
                    self.IClearBBMini(0)
                    KIMini.dialog.show()
        elif (command == kTempDisableKIandBB):
            PtDebugPrint('xKI: TEMP Disable KI', level=kDebugDumpLevel)
            # clear afk information list
            gAfkInformed = {}
            # /clear afk information list
            IKIDisabled = 1
            if (theKILevel == kNanoKI):
                KINanoBlackBar.dialog.hide()
            elif ((theKILevel == kMicroKI) or PtIsSinglePlayerMode()):
                KIMicroBlackbar.dialog.hide()
            else:
                KIBlackbar.dialog.hide()
            if YeeshaBook:
                YeeshaBook.hide()
            if JournalBook:
                JournalBook.hide()
            PtToggleAvatarClickability(true)
            plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
            plybkCB.setChecked(0)
            plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID))
            plybkCB.setChecked(0)
        elif (command == kTempEnableKIandBB):
            PtDebugPrint('xKI: TEMP Enable KI', level=kDebugDumpLevel)
            if (not IKIHardDisabled):
                IKIDisabled = 0
                if (theKILevel == kNanoKI):
                    KINanoBlackBar.dialog.showNoReset()
                elif ((theKILevel == kMicroKI) or PtIsSinglePlayerMode()):
                    KIMicroBlackbar.dialog.showNoReset()
                else:
                    KIBlackbar.dialog.showNoReset()
        elif (command == kYesNoDialog):
            YNWhatReason = kYNOutside
            YNOutsideSender = value[1]
            yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
            yesText.setString(value[0])
            self.ILocalizeYesNoDialog()
            KIYesNo.dialog.show()
        elif (command == kAddPlayerDevice):
            PtDebugPrint(('KI: add device %s to player list' % value), level=kDebugDumpLevel)
            try:
                FolderOfDevices.index(Device(value))
            except ValueError:
                FolderOfDevices.append(Device(value))
                self.IRefreshPlayerList()
                self.IRefreshPlayerListDisplay()
        elif (command == kRemovePlayerDevice):
            try:
                FolderOfDevices.remove(Device(value))
            except ValueError:
                pass
            self.IRefreshPlayerList()
            self.IRefreshPlayerListDisplay()
        elif (command == kUpgradeKILevel):
            if ((value >= kLowestKILevel) and (value <= kHighestKILevel)):
                if (value > theKILevel):
                    PtDebugPrint(('xKI: Upgrading from KIlevel %d to new KI level of %d' % (theKILevel, value)), level=kWarningLevel)
                    self.IRemoveKILevel(theKILevel, upgrading=1)
                    theKILevel = value
                    self.IUpdateKILevelChronicle()
                    self.IWearKILevel(theKILevel)
                elif (value == theKILevel):
                    PtDebugPrint(('xKI: Ignoring - trying to upgrading from KIlevel %d to new KI level of %d' % (theKILevel, value)), level=kWarningLevel)
                    self.IUpdateKILevelChronicle()
                    self.IMakeSureWeWereKILevel()
            else:
                PtDebugPrint(('xKI: Invalid KI level %d' % value), level=kErrorLevel)
        elif (command == kDowngradeKILevel):
            if (value == theKILevel):
                PtDebugPrint(('xKI: Remove KI level of %d' % value), level=kWarningLevel)
                if (value == kMicroKI):
                    self.IRemoveKILevel(kMicroKI)
                    theKILevel = kNanoKI
                    self.IUpdateKILevelChronicle()
                    self.IWearKILevel(theKILevel)
                elif (value == kNormalKI):
                    self.IRemoveKILevel(kNormalKI)
                    theKILevel = kMicroKI
                    self.IUpdateKILevelChronicle()
                    self.IWearKILevel(theKILevel)
                else:
                    PtDebugPrint(("xKI: Ignoring - can't remove to any lower than %d" % value), level=kWarningLevel)
            else:
                PtDebugPrint(('xKI: Ignoring - trying to remove KILevel %d, but currently at %d' % (value, theKILevel)), level=kWarningLevel)
        elif (command == kAddJournalBook):
            if (theKILevel >= kMicroKI):
                self.IAddJournalBook()
                self.IUpdateJournalBookChronicle()
        elif (command == kRemoveJournalBook):
            if (theKILevel >= kMicroKI):
                self.IRemoveJournalBook()
                self.IUpdateJournalBookChronicle()
        elif (command == kRateIt):
            rateText = ptGUIControlTextBox(KIRateIt.dialog.getControlFromTag(kYesNoTextID))
            rateText.setString(value[1])
            KIRateIt.dialog.show()
        elif (command == kSetPrivateChatChannel):
            PrivateChatChannel = value
        elif (command == kUnsetPrivateChatChannel):
            PrivateChatChannel = 0
        elif (command == kStartBookAlert):
            self.IAlertBookStart()
        elif (command == kStartJournalAlert):
            self.IAlertJournalStart()
        elif (command == kMiniBigKIToggle):
            if (not PtIsSinglePlayerMode()):
                self.IminiToggleKISize()
        elif (command == kKIPutAway):
            if (not PtIsSinglePlayerMode()):
                self.IminiPutAwayKI()
        elif (command == kChatAreaPageUp):
            self.IminiChatAreaPageUp()
        elif (command == kChatAreaPageDown):
            self.IminiChatAreaPageDown()
        elif (command == kChatAreaGoToBegin):
            self.IminiChatAreaGoToBegin()
        elif (command == kChatAreaGoToEnd):
            self.IminiChatAreaGoToEnd()
        elif (command == kKITakePicture):
            if (not PtIsSinglePlayerMode()):
                self.IminiTakePicture()
        elif (command == kKICreateJournalNote):
            if (not PtIsSinglePlayerMode()):
                self.IminiCreateJournal()
        elif (command == kKIToggleFade):
            if self.IsChatFaded():
                self.IKillFadeTimer()
                self.IStartFadeTimer()
            else:
                self.IFadeCompletely()
        elif (command == kKIToggleFadeEnable):
            self.IKillFadeTimer()
            if FadeEnableFlag:
                FadeEnableFlag = 0
            else:
                FadeEnableFlag = 1
            self.IStartFadeTimer()
        elif (command == kKIChatStatusMsg):
            self.IDoStatusChatMessage(value)
        elif (command == kKILocalChatStatusMsg):
            self.IDoStatusChatMessage(value, netPropagate=0)
        elif (command == kKILocalChatErrorMsg):
            self.IDoErrorChatMessage(value)
        elif (command == kKIUpSizeFont):
            self.IUpFontSize()
        elif (command == kKIDownSizeFont):
            self.IDownFontSize()
        elif (command == kKIOpenYeehsaBook):
            nm = ptNetLinkingMgr()
            if ((theKILevel >= kMicroKI) and ((not IKIDisabled) and ((not WaitingForAnimation) and nm.isEnabled()))):
                curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                if (IsEntireYeeshaBookEnabled and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                    self.IShowYeeshaBook()
                    if (theKILevel == kMicroKI):
                        plybkCB = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                    else:
                        plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                    plybkCB.setChecked(1)
        elif (command == kKIOpenJournalBook):
            if ((theKILevel >= kMicroKI) and ((not IKIDisabled) and ((not WaitingForAnimation) and gKIHasJournal))):
                curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
                if (gKIHasJournal and ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit)))):
                    self.IShowJournalBook()
                    if (theKILevel == kMicroKI):
                        plybkCB = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kJournalBookCBID))
                    else:
                        plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID))
                    plybkCB.setChecked(1)
        elif (command == kKIOpenKI):
            if (not PtIsSinglePlayerMode()):
                if (not WaitingForAnimation):
                    if (not KIMini.dialog.isEnabled()):
                        self.IminiPutAwayKI()
                    elif (not BigKI.dialog.isEnabled()):
                        if self.IsChatFaded():
                            self.IKillFadeTimer()
                            self.IStartFadeTimer()
##############################################################################
# diafero's F2 fix
##############################################################################
                            self.IminiToggleKISize() # fixes the problem that the KI is not opened with F2 when chat fadeout is disabled (by diafero)
##############################################################################
# End diafero's F2 fix
##############################################################################
                        else:
                            self.IminiToggleKISize()
                    else:
                        self.IminiPutAwayKI()
        elif (command == kKIShowCCRHelp):
            if YeeshaBook:
                YeeshaBook.hide()
            PtToggleAvatarClickability(true)
            if (theKILevel == kMicroKI):
                plybkCB = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                plybkCB.setChecked(0)
            elif (theKILevel > kMicroKI):
                plybkCB = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kPlayerBookCBID))
                plybkCB.setChecked(0)
            if ((not WaitingForAnimation) and (not IKIDisabled)):
                PtShowDialog('OptionsMenuGUI')
        elif (command == kKICreateMarker):
            self.ICreateAMarker()
        elif (command == kKICreateMarkerFolder):
            self.ICreateMarkerFolder()
        elif (command == kKIPhasedAllOn):
            PhasedKICreateNotes = 1
            PhasedKICreateImages = 1
            PhasedKIShareYeeshaBook = 1
            PhasedKIInterAgeChat = 1
            PhasedKINeighborsInDPL = 1
            PhasedKIBuddies = 1
            PhasedKIPlayMarkerGame = 1
            PhasedKICreateMarkerGame = 1
            PhasedKISendNotes = 1
            PhasedKISendImages = 1
            PhasedKISendMarkerGame = 1
            PhasedKIShowMarkerGame = 1
##############################################################################
# D'Lanor's Alcugs GPS fix
##############################################################################
            gShowGPSCheat = 1
##############################################################################
# End D'Lanor's Alcugs GPS fix
##############################################################################
        elif (command == kKIPhasedAllOff):
            PhasedKICreateNotes = 0
            PhasedKICreateImages = 0
            PhasedKIShareYeeshaBook = 0
            PhasedKIInterAgeChat = 0
            PhasedKINeighborsInDPL = 0
            PhasedKIBuddies = 0
            PhasedKIPlayMarkerGame = 0
            PhasedKICreateMarkerGame = 0
            PhasedKISendNotes = 0
            PhasedKISendImages = 0
            PhasedKISendMarkerGame = 0
            PhasedKIShowMarkerGame = 0
##############################################################################
# D'Lanor's Alcugs GPS fix
##############################################################################
            gShowGPSCheat = 0
##############################################################################
# End D'Lanor's Alcugs GPS fix
##############################################################################
        elif ((command == kKIOKDialog) or (command == kKIOKDialogNoQuit)):
            reasonField = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
            try:
                localized = xLocalization.xKI.xOKDialogDict[value] + ' ('+value+')'
            except KeyError:
                localized = value
            reasonField.setString(localized)
            noButton = ptGUIControlButton(KIYesNo.dialog.getControlFromTag(kNoButtonID))
            noButton.hide()
            noBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
            noBtnText.hide()
            yesBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
            yesBtnText.setString(xLocalization.xKI.xYesNoOKbutton)
            YNWhatReason = kYNForceQuit
            if (command == kKIOKDialogNoQuit):
                YNWhatReason = kYNNoReason
            KIYesNo.dialog.show()
        elif (command == kDisableYeeshaBook):
            IsYeeshaBookEnabled = 0
        elif (command == kEnableYeeshaBook):
            IsYeeshaBookEnabled = 1
        elif (command == kQuitDialog):
            yesText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
            yesText.setString(xLocalization.xKI.xLeaveGameMessageNormal)
            self.ILocalizeQuitNoDialog()
            KIYesNo.dialog.show()
        elif (command == kDisableEntireYeeshaBook):
            IsEntireYeeshaBookEnabled = 0
        elif (command == kEnableEntireYeeshaBook):
            IsEntireYeeshaBookEnabled = 1
        elif (command == kGZUpdated):
            if (value != 0):
                vault = ptVault()
                entry = vault.findChronicleEntry(kChronicleGZMarkersAquired)
                if (type(entry) != type(None)):
                    markers = entry.chronicleGetValue()
                    if (len(markers) < value):
                        markers += (kGZMarkerAvailable * (value - len(markers)))
                        entry.chronicleSetValue(markers)
                        entry.save()
                else:
                    markers = (kGZMarkerAvailable * value)
                    vault.addChronicleEntry(kChronicleGZMarkersAquired, kChronicleGZMarkersAquiredType, markers)
            self.IDetermineKILevel()
            self.IDetermineGZ()
            self.IRefreshMiniKIMarkerDisplay()
        elif (command == kGZFlashUpdate):
            self.IDetermineKILevel()
            self.IGZFlashUpdate(value)
            self.IRefreshMiniKIMarkerDisplay()
        elif (command == kGZInRange):
            if (gMarkerToGetNumber > gMarkerGottenNumber):
                gGZMarkerInRange = value[0]
                gGZMarkerInRangeRepy = value[1]
                self.IRefreshMiniKIMarkerDisplay()
                if (not KIMini.dialog.isEnabled()):
                    NewItemAlert.dialog.show()
                    kialert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertKIAlert))
                    kialert.show()
        elif (command == kGZOutRange):
            gGZMarkerInRange = 0
            gGZMarkerInRangeRepy = None
            self.IRefreshMiniKIMarkerDisplay()
            NewItemAlert.dialog.hide()
            kialert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertKIAlert))
            kialert.hide()
        elif (command == kUpgradeKIMarkerLevel):
            self.IUpgradeKIMarkerLevel(value)
            self.IRefreshMiniKIMarkerDisplay()
        elif (command == kKIShowMiniKI):
            if ((not PtIsSinglePlayerMode()) and (theKILevel >= kNormalKI)):
                self.IClearBBMini(0)
# Ahnonay Sphere 4 work-around BEGIN
        elif (command == kKISitOnNextLinkOut):
            global gSitOnNextLinkOut
            gSitOnNextLinkOut = 1
# Ahnonay Sphere 4 work-around END



    def IRemoveKILevel(self, level, upgrading = 0):
        if (level == kNanoKI):
            KINanoBlackBar.dialog.hide()
        elif (level == kMicroKI):
            if (not upgrading):
                avatar = PtGetLocalAvatar()
                gender = avatar.avatar.getAvatarClothingGroup()
                if (gender > kFemaleClothingGroup):
                    gender = kMaleClothingGroup
                avatar.netForce(1)
                if (gender == kFemaleClothingGroup):
                    avatar.avatar.removeClothingItem('FAccPlayerBook')
                else:
                    avatar.avatar.removeClothingItem('MAccPlayerBook')
                avatar.avatar.saveClothing()
                self.IRemoveJournalBook()
                self.IUpdateJournalBookChronicle()
            KIMicroBlackbar.dialog.hide()
            if (not PtIsSinglePlayerMode()):
                KIMicro.dialog.hide()
        elif (level == kNormalKI):
            avatar = PtGetLocalAvatar()
            gender = avatar.avatar.getAvatarClothingGroup()
            if (gender > kFemaleClothingGroup):
                gender = kMaleClothingGroup
            avatar.netForce(1)
            if (gender == kFemaleClothingGroup):
                avatar.avatar.removeClothingItem('FAccKI')
            else:
                avatar.avatar.removeClothingItem('MAccKI')
            avatar.avatar.saveClothing()
            if (not PtIsSinglePlayerMode()):
                chatarea = ptGUIControlMultiLineEdit(KIMini.dialog.getControlFromTag(kChatDisplayArea))
                chatarea.lock()
                chatarea.unclickable()
                chatarea.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
                chatarea.disableScrollControl()
                KIBlackbar.dialog.hide()
                KIMini.dialog.hide()
                KIListModeDialog.dialog.hide()
                KIPictureExpanded.dialog.hide()
                KIJournalExpanded.dialog.hide()
                KIPlayerExpanded.dialog.hide()
                BigKI.dialog.hide()
                KIOnAnim.animation.skipToTime(1.5)



    def IWearKILevel(self, level):
        if (level == kNanoKI):
            KINanoBlackBar.dialog.show()
        elif (level == kMicroKI):
            if self.DoesPlayerHaveRelto():
                avatar = PtGetLocalAvatar()
                gender = avatar.avatar.getAvatarClothingGroup()
                if (gender > kFemaleClothingGroup):
                    gender = kMaleClothingGroup
                avatar.netForce(1)
                if (gender == kFemaleClothingGroup):
                    avatar.avatar.wearClothingItem('FAccPlayerBook')
                else:
                    avatar.avatar.wearClothingItem('MAccPlayerBook')
                avatar.avatar.saveClothing()
            KIMicroBlackbar.dialog.show()
            self.IClearBBMini()
            if (not PtIsSinglePlayerMode()):
                KIMicro.dialog.show()
                self.IEnterChatMode(0)
        elif (level == kNormalKI):
            avatar = PtGetLocalAvatar()
            gender = avatar.avatar.getAvatarClothingGroup()
            if (gender > kFemaleClothingGroup):
                gender = kMaleClothingGroup
            avatar.netForce(1)
            if (gender == kFemaleClothingGroup):
                avatar.avatar.wearClothingItem('FAccKI')
            else:
                avatar.avatar.wearClothingItem('MAccKI')
            avatar.avatar.saveClothing()
            if (not PtIsSinglePlayerMode()):
                KIBlackbar.dialog.show()
                self.IClearBBMini()
                if (not gKIHasJournal):
                    PtDebugPrint("xKI: You don't have the journal, so removing it from the BB")
                    chkbox = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID))
                    chkbox.hide()
                    chkbox.disable()
                KIOnAnim.animation.skipToTime(1.5)
                self.IAlertKIStart()
                self.ICheckInboxForUnseen()
                self.IBigKIRefreshFolders()
            else:
                KIMicroBlackbar.dialog.show()
                self.IClearBBMini()



    def IMakeSureWeWereKILevel(self):
        if (theKILevel == kNanoKI):
            pass
        elif (theKILevel == kMicroKI) and self.DoesPlayerHaveRelto():
            try:
                avatar = PtGetLocalAvatar()
                gender = avatar.avatar.getAvatarClothingGroup()
                if (gender > kFemaleClothingGroup):
                    gender = kMaleClothingGroup
                avatar.netForce(1)
                if (gender == kFemaleClothingGroup):
                    avatar.avatar.wearClothingItem('FAccPlayerBook')
                else:
                    avatar.avatar.wearClothingItem('MAccPlayerBook')
                avatar.avatar.saveClothing()
            except NameError:
                pass
        elif (theKILevel == kNormalKI):
            try:
                avatar = PtGetLocalAvatar()
                gender = avatar.avatar.getAvatarClothingGroup()
                if (gender > kFemaleClothingGroup):
                    gender = kMaleClothingGroup
                avatar.netForce(1)
                if (gender == kFemaleClothingGroup):
                    avatar.avatar.wearClothingItem('FAccPlayerBook')
                    avatar.avatar.wearClothingItem('FAccKI')
                else:
                    avatar.avatar.wearClothingItem('MAccPlayerBook')
                    avatar.avatar.wearClothingItem('MAccKI')
                avatar.avatar.saveClothing()
            except NameError:
                pass



    def IAddJournalBook(self):
        global gKIHasJournal
        if ((theKILevel >= kMicroKI) and (not gKIHasJournal)):
            gKIHasJournal = 1
            if (theKILevel == kMicroKI):
                chkbox = ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kJournalBookCBID))
            else:
                chkbox = ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID))
            chkbox.show()
            chkbox.enable()
            chkbox.setChecked(0)
            self.IAlertJournalStart()



    def IRemoveJournalBook(self):
        global gKIHasJournal
        gKIHasJournal = 0
        ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kJournalBookCBID)).hide()
        ptGUIControlCheckBox(KIMicroBlackbar.dialog.getControlFromTag(kJournalBookCBID)).disable()
        ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID)).hide()
        ptGUIControlCheckBox(KIBlackbar.dialog.getControlFromTag(kJournalBookCBID)).disable()



    def OnRTChat(self, player, message, flags):
        if (type(message) != type(None)):
            cflags = ChatFlags(flags)
            # Special commands
            if player.getPlayerID() and cflags.status and message.startswith('/remote '):
                xUserKI.OnRemoteCall(self, message[len('/remote '):], player)
                return
            elif player.getPlayerID() == 0 and cflags.private and message.startswith('/!'):
                xUserKI.OnServerCommand(self, message[len('/!'):])
                return
            # END Special commands
            if cflags.broadcast:
                if (cflags.channel != PrivateChatChannel):
                    return
            if (theKILevel == kNanoKI):
                if (cflags.private or cflags.admin):
                    pass
                else:
                    return
            message = xCensor.xCensor(message, theCensorLevel)
            self.IAddRTChat(player, message, cflags, forceKI=(not ISawTheKIAtleastOnce))
            try:
                if player.getPlayerID() and (IKIDisabled or PtGetLocalAvatar().avatar.getCurrentMode() == PtBrainModes.kAFK) and (not cflags.status) and (cflags.private or cflags.interAge or cflags.neighbors): # don't reply to age chat or afk notifications (sent as status message)
                    # create message
                    message = PtGetClientName()
                    if cflags.interAge:
                        message = message + " in " + self.IGetAgeDisplayName()
                    if IKIDisabled:
                        message = message + " currently can not see the KI"
                    else:
                        message = message + " is afk"
                        # AFK MESSAGE
                        if len(gAfkMessage): message = message + ": " + gAfkMessage
                        #/AFK MESSAGE
                    # check if we already told him recently
                    global gAfkInformed
                    if (not cflags.private) and (player.getPlayerID() in gAfkInformed): # always inform for private messages
                        time = gAfkInformed[player.getPlayerID()]
                        if (PtGetTime()-time) < kAfkInformationWait: return
                    gAfkInformed[player.getPlayerID()] = PtGetTime()
                    # send it as status message
                    cflags.status = 1
                    PtSendRTChat(PtGetLocalPlayer(), [player], "<>"+message, cflags.flags)
            except NameError:
                pass



    def OnTimer(self, id):
        global CurrentFadeTick
        global FadeMode
##############################################################################
# Alcugs invite deficiency workaround
##############################################################################
        global InviteInProgress
        global InviteTryCount
##############################################################################
# End Alcugs invite deficiency workaround
##############################################################################
        if (id == kFadeTimer):
            if PtIsSinglePlayerMode():
                return
            if (FadeMode == kFadeFullDisp):
                CurrentFadeTick -= 1
                if (CurrentFadeTick > 0):
                    PtAtTimeCallback(self.key, kFullTickTime, kFadeTimer)
                else:
                    FadeMode = kFadeDoingFade
                    CurrentFadeTick = TicksOnFade
                    PtAtTimeCallback(self.key, kFadeTickTime, kFadeTimer)
            elif (FadeMode == kFadeDoingFade):
                CurrentFadeTick -= 1
                if (CurrentFadeTick > 0):
                    if (theKILevel < kNormalKI):
                        mKIdialog = KIMicro.dialog
                    else:
                        mKIdialog = KIMini.dialog
                    mKIdialog.setForeColor(-1, -1, -1, ((OriginalForeAlpha * CurrentFadeTick) / TicksOnFade))
                    mKIdialog.setSelectColor(-1, -1, -1, ((OriginalSelectAlpha * CurrentFadeTick) / TicksOnFade))
                    mKIdialog.refreshAllControls()
                    PtAtTimeCallback(self.key, kFadeTickTime, kFadeTimer)
                else:
                    self.IFadeCompletely()
            elif (FadeMode == kFadeStopping):
                FadeMode = kFadeNotActive
        elif (id == kBKITODCheck):
            if BigKI.dialog.isEnabled():
                self.IBigKISetChanging()
        elif (id == kMarkerGameTimer):
            if (type(CurrentPlayingMarkerGame) != type(None)):
                CurrentPlayingMarkerGame.updateGameTime()
                PtAtTimeCallback(self.key, 1, kMarkerGameTimer)
        elif (id == kAlertHideTimer):
            self.IAlertStop()
        elif (id == kTakeSnapShot):
##############################################################################
# Hide cursor in KI shots
##############################################################################
            PtForceCursorHidden()
##############################################################################
# End hide cursor in KI shots
##############################################################################
#Jalak
            if JalakGUIState:
                self.JalakGUIToggle(1)
#/Jalak
            print '*-*-*- Start screen capture -*-*-*-*'
            PtStartScreenCapture(self.key)
        elif (id >= kUserKITimerIdStart and id <= kUserKITimerIdEnd):
            xUserKI.OnTimer(self, id)
# Fix new players being shown as near BEGIN
        elif (id == kUpdatePlayerList):
            self.IRefreshPlayerList()
            self.IRefreshPlayerListDisplay()
# Fix new players being shown as near END
##############################################################################
# Alcugs invite deficiency workaround
##############################################################################
        elif (id == kInviteFinish):
            if InviteInProgress:
                if InviteInProgress.hasValidID():
                    InviteInProgress.sendTo(InviteRecipient)
                    InviteParentNode.removeNode(InviteInProgress)
                    InviteInProgress = None
                else:
                    InviteTryCount += 1
                    if InviteTryCount < 4:
                        PtAtTimeCallback(self.key, 0.5, kInviteFinish)
                    else:
                        InviteInProgress = None
##############################################################################
# End Alcugs invite deficiency workaround
##############################################################################
#Jalak
        elif (id == kJalakBtnDelayTimer):
            self.SetJalakGUIButtons(1)
#/Jalak



    def OnScreenCaptureDone(self, image):
        global WeAreTakingAPicture
        global LastminiKICenter
        global BKRightSideMode
        global gLastImageFileNumber
        print '#-#-#- capture screen received -#-#-#-#'
        self.IBigKICreateJournalImage(image)
##############################################################################
# Hide cursor in KI shots
##############################################################################
        PtForceCursorShown()
##############################################################################
# End hide cursor in KI shots
##############################################################################
        if (BKFolderLineDict is BKJournalFolderDict):
            pass
        else:
            modeselector = ptGUIControlRadioGroup(BigKI.dialog.getControlFromTag(kBKRadioModeID))
            modeselector.setValue(0)
        if (BKRightSideMode != kBKPictureExpanded):
            self.IBigKIHideMode()
        BKRightSideMode = kBKPictureExpanded
        self.IBigKIRefreshFolderDisplay()
        self.IBigKIEnterEditMode(kBKEditFieldPICTitle)
        BigKI.dialog.show()
        if (type(LastminiKICenter) == type(None)):
            if (type(OriginalminiKICenter) != type(None)):
                dragbar = ptGUIControlDragBar(KIMini.dialog.getControlFromTag(kminiDragBar))
                LastminiKICenter = dragbar.getObjectCenter()
                dragbar.setObjectCenter(OriginalminiKICenter)
                dragbar.anchor()
        KIMini.dialog.show()
        WeAreTakingAPicture = 0
        files = glob.glob(gImageFileSearch)
        found = 0
        while (not found):
            gLastImageFileNumber += 1
            tryName = (((('.\\' + gImageDirectory) + '\\') + gImageFileNameTemplate) + ('%04d.jpg' % gLastImageFileNumber))
            #print ('looking for %s' % tryName)
            if (tryName in files):
                pass
            else:
                found = 1

        image.saveAsJPEG(tryName, 90)



    def OnMemberUpdate(self):
        PtDebugPrint('xKI:OnMemberUpdate - refresh player list', level=kDebugDumpLevel)
        if PtIsDialogLoaded('KIMini'):
            self.IRefreshPlayerList()
            self.IRefreshPlayerListDisplay()
# Fix new players being shown as near BEGIN
            PtAtTimeCallback(self.key, 1.5, kUpdatePlayerList)
# Fix new players being shown as near END
        xUserKI.OnMemberUpdate(self)



    def OnRemoteAvatarInfo(self, player):
        global PlayerInfoName
        global BKPlayerSelected
        if (theKILevel < kNormalKI):
            return
        avatarSet = 0
        if (type(player) == type(0)):
            pass
        elif isinstance(player, ptPlayer):
            PlayerInfoName = player
            avatarSet = 1
            BKPlayerSelected = player
            sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
            sendToField.setString(PlayerInfoName.getPlayerName())
            self.IBigKISetToButtons()
            for pidx in range(len(BKPlayerList)):
                if (isinstance(BKPlayerList[pidx], ptPlayer) and (BKPlayerList[pidx] == player)):
                    playerlist = ptGUIControlListBox(KIMini.dialog.getControlFromTag(kPlayerList))
                    playerlist.setSelection(pidx)
                    caret = ptGUIControlTextBox(KIMini.dialog.getControlFromTag(kChatCaretID))
                    caret.setString(((xLocalization.xKI.xChatTOPrompt + player.getPlayerName()) + ' >'))
                    privateChbox = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiPrivateToggle))
                    privateChbox.setChecked(1)
                    break

        if avatarSet:
            if (not KIMini.dialog.isEnabled()):
                KIMini.dialog.show()
            self.IKillFadeTimer()
            self.IStartFadeTimer()



    def OnVaultNotify(self, event, tupdata):
        PtDebugPrint(('xKI:OnVaultNotify recvd. Event=%d and data= ' % event), tupdata, level=kDebugDumpLevel)
        if PtIsDialogLoaded('KIMain'):
            if ((event == PtVaultNotifyTypes.kRegisteredOwnedAge) or ((event == PtVaultNotifyTypes.kUnRegisteredOwnedAge) or (PtVaultNotifyTypes.kRegisteredVisitAge or PtVaultNotifyTypes.kUnRegisteredVisitAge))):
                PtDebugPrint(('xKI: kRegisteredOwnedAge event (id=%d,type=%d)' % (tupdata[0].getID(), tupdata[0].getType())), level=kDebugDumpLevel)
                if (theKILevel > kMicroKI):
                    if isinstance(tupdata[0], ptVaultAgeLinkNode):
                        ownedAge = tupdata[0].getAgeInfo()
                        if (type(ownedAge) != type(None)):
                            if self.IIsAgeMyNeighborhood(ownedAge):
                                self.IBigKIRefreshHoodStatics(ownedAge)
                                self.IRefreshPlayerList()
                                self.IRefreshPlayerListDisplay()
                            self.IBigKIRefreshFolders()
                            self.IBigKIRefreshFolderDisplay()
                            self.IBigKIRefreshContentList()
                            self.IBigKIRefreshContentListDisplay()
                            self.IRefreshAgeOwnerSettings()
                        else:
                            PtDebugPrint('xKI:kRegisteredOwnedAge: Error - where is the stinking ageInfo! ', level=kErrorLevel)
                    else:
                        PtDebugPrint('xKI:kRegisteringOwnedAge: Error - unknown tuple data type! ', level=kErrorLevel)
            else:
                PtDebugPrint(('xKI: OnVaultNotify - unknown event! %d' % event), level=kWarningLevel)
        else:
            PtDebugPrint('xKI: OnVaultNotify - bigKI dialog was not loaded... waiting...', level=kDebugDumpLevel)



    def OnAgeVaultEvent(self, event, tupdata):
        PtDebugPrint(('xKI:OnAgeVaultEvent recvd. Event=%d and data= ' % event), tupdata, level=kDebugDumpLevel)
        self.HandleVaultTypeEvents(event, tupdata)



    def OnVaultEvent(self, event, tupdata):
        PtDebugPrint(('xKI:OnVaultEvent recvd. Event=%d and data= ' % event), tupdata, level=kDebugDumpLevel)
        self.HandleVaultTypeEvents(event, tupdata)



    def HandleVaultTypeEvents(self, event, tupdata):
##############################################################################
# Slow link to Relto fix
##############################################################################
        global gVConnected
##############################################################################
# End slow link to Relto fix
##############################################################################
        if PtIsDialogLoaded('KIMain'):
            if (event == PtVaultCallbackTypes.kVaultConnected):
                PtDebugPrint('xKI: kVaultConnected event', level=kDebugDumpLevel)
##############################################################################
# Slow link to Relto fix
##############################################################################
                gVConnected = 1
##############################################################################
# End slow link to Relto fix
##############################################################################
            elif (event == PtVaultCallbackTypes.kVaultDisconnected):
                PtDebugPrint('xKI: kVaultDisconnected event', level=kDebugDumpLevel)
##############################################################################
# Slow link to Relto fix
##############################################################################
                gVConnected = 0
##############################################################################
# End slow link to Relto fix
##############################################################################
            elif (event == PtVaultCallbackTypes.kVaultNodeSaved):
                PtDebugPrint(('xKI: kVaultNodeSaved event (id=%d,type=%d)' % (tupdata[0].getID(), tupdata[0].getType())), level=kDebugDumpLevel)
                if (tupdata[0].getType() == PtVaultNodeTypes.kPlayerInfoNode):
                    self.IRefreshPlayerList()
                    self.IRefreshPlayerListDisplay()
                elif (tupdata[0].getType() == PtVaultNodeTypes.kAgeInfoNode):
                    self.IBigKISetStatics()
                    self.IBigKIRefreshFolders()
                    self.IBigKIOnlySelectedToButtons()
                    self.IRefreshAgeOwnerSettings()
                elif (tupdata[0].getType() == PtVaultNodeTypes.kMarkerNode):
                    if (BKRightSideMode == kBKMarkerListExpanded):
                        ptMarkerMgr().setSelectedMarker(tupdata[0].getID())
                        self.IBigKIDisplayCurrentContentMarkerFolder()
                self.IBigKIRefreshContentList()
                self.IBigKIRefreshContentListDisplay()
            elif (event == PtVaultCallbackTypes.kVaultNodeInitialized):
                PtDebugPrint(('xKI: kVaultNodeInitialized event (id=%d,type=%d)' % (tupdata[0].getID(), tupdata[0].getType())), level=kDebugDumpLevel)
                if (theKILevel > kMicroKI):
                    node = tupdata[0]
                    self.IBKCheckElementRefresh(tupdata[0])
            elif (event == PtVaultCallbackTypes.kVaultNodeAdded):
                PtDebugPrint('xKI: kVaultNodeAdded event', level=kDebugDumpLevel)
            elif (event == PtVaultCallbackTypes.kVaultNodeRefAdded):
                PtDebugPrint(('xKI: kVaultNodeRefAdded event (childID=%d,parentID=%d)' % (tupdata[0].getChildID(), tupdata[0].getParentID())), level=kDebugDumpLevel)
##############################################################################
# Slow link to Relto fix
##############################################################################
#                if (theKILevel > kMicroKI):
                if (theKILevel > kMicroKI and gVConnected):
##############################################################################
# End slow link to Relto fix
##############################################################################
                    folder = tupdata[0].getParent()
                    folder = folder.upcastToFolderNode()
                    if ((type(folder) != type(None)) and (folder.folderGetType() == PtVaultStandardNodes.kInboxFolder)):
                        if (not tupdata[0].beenSeen()):
                            if OnlyGetPMsFromBuddies:
                                vault = ptVault()
                                inbox = vault.getInbox()
                                buddies = vault.getBuddyListFolder()
                                if buddies.playerlistHasPlayer(tupdata[0].getSaverID()):
                                    self.IAlertKIStart()
                            else:
                                self.IAlertKIStart()
                    child = tupdata[0].getChild()
                    child = child.upcastToFolderNode()
                    if (type(child) != type(None)):
                        PtDebugPrint('xKI- adding a folder... refresh folder list', level=kDebugDumpLevel)
                        self.IBigKIRefreshFolders()
                    self.IBKCheckFolderRefresh(folder)
            elif (event == PtVaultCallbackTypes.kVaultRemovingNodeRef):
                PtDebugPrint(('xKI: kVaultRemovingNodeRef event (childID=%d,parentID=%d)' % (tupdata[0].getChildID(), tupdata[0].getParentID())), level=kDebugDumpLevel)
            elif (event == PtVaultCallbackTypes.kVaultNodeRefRemoved):
                PtDebugPrint('xKI: kVaultNodeRefRemoved event (childID,parentID) ', tupdata, level=kDebugDumpLevel)
##############################################################################
# Slow link to Relto fix
##############################################################################
#                if (theKILevel > kMicroKI):
                if (theKILevel > kMicroKI and gVConnected):
##############################################################################
# End slow link to Relto fix
##############################################################################
                    if (BKRightSideMode == kBKMarkerListExpanded):
                        self.IBigKIDisplayCurrentContentMarkerFolder()
                    self.IBKCheckFolderRefresh()
            elif (event == PtVaultCallbackTypes.kVaultOperationFailed):
                PtDebugPrint('xKI: kVaultOperationFailed event  (operation,resultCode) ', tupdata, level=kDebugDumpLevel)
            else:
                PtDebugPrint(('xBigKI: OnVaultEvent - unknown event! %d' % event), level=kWarningLevel)
        else:
            PtDebugPrint('xBigKI: OnVaultEvent - bigKI dialog was not loaded... waiting...', level=kDebugDumpLevel)



    def OnCCRMsg(self, msgtype, message, ccrplayerid):
        global CCRConversationInProgress
        PtDebugPrint(("xKI: CCR message recv'd type=%d,ccr=%d,msg=%s" % (msgtype, ccrplayerid, message)), level=kDebugDumpLevel)
        if (msgtype == kCCRBeginCommunication):
            self.IAddRTChat(None, xLocalization.xKI.xCCRConversationStarted, kChatCCRMessage)
            CCRConversationInProgress = ccrplayerid
            self.IAddRTChat(None, message, kChatCCRMessage)
        elif (msgtype == kCCREndCommunication):
            self.IAddRTChat(None, xLocalization.xKI.xCCRConversationEnded, kChatCCRMessage)
            CCRConversationInProgress = 0
        elif (msgtype == kCCRChat):
            self.IAddRTChat(None, message, kChatCCRMessage)
        elif (msgtype == kCCRReturnChatMsg):
            daPlayer = ptPlayer((xLocalization.xKI.xChatCCRFromPlayer % ccrplayerid), ccrplayerid)
            self.IAddRTChat(daPlayer, message, kChatCCRMessageFromPlayer)
        else:
            PtDebugPrint(('xKI - unknown CCR message of type %d' % msgtype), level=kWarningLevel)
        if PtGetLocalAvatar().avatar.getCurrentMode():
            if CCRConversationInProgress:
                PtSendChatToCCR('Player is AFK', CCRConversationInProgress)



    def OnMarkerMsg(self, msgType, gameMasterID, tupdata):
        global MarkerGameState
        global gMarkerGottenColor
        global gMarkerGottenNumber
        global CurrentPlayingMarkerGame
        global gMarkerToGetColor
        global gMarkerToGetNumber
        PtDebugPrint(('xKI: MarkerMsg type=%d, gamemaster=%d, tupdata=' % (msgType, gameMasterID)) + str(tupdata))
        if (msgType == PtMarkerMsgType.kGameCreate):
            if (theKILevel >= kNormalKI):
                if (gameMasterID != PtGetLocalPlayer().getPlayerID()):
                    q = MarkerGameJoinQuestion(gameMasterID, tupdata[0], tupdata[1], tupdata[2])
                    MarkerJoinRequests.append(q)
                    self.IAlertKIStart()
                    self.IBKCheckFolderRefresh(ptVault().getInbox())
                    self.IDoStatusChatMessage(xLocalization.xKI.xMarkerGameInviteRecvd, netPropagate=0)
                else:
                    MarkerGameState = kMGGameCreation
                    CurrentPlayingMarkerGame = MarkerGame(gameMasterID)
                    CurrentPlayingMarkerGame.setGame(tupdata[0], tupdata[1], tupdata[2])
                    self.IRefreshPlayerList()
                    self.IRefreshPlayerListDisplay()
                    if (BKRightSideMode == kBKMarkerListExpanded):
                        self.IBigKIDisplayCurrentContentMarkerFolder()
        elif (msgType == PtMarkerMsgType.kGameJoin):
            pass
        elif (msgType == PtMarkerMsgType.kGameAddPlayer):
            if (type(CurrentPlayingMarkerGame) != type(None)):
                if (CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeQuest):
                    CurrentPlayingMarkerGame.addPlayerToTeam(tupdata[0], tupdata[1])
                else:
                    CurrentPlayingMarkerGame.addPlayerToTeam(tupdata[0], tupdata[1])
                    if (type(WorkingMarkerFolder) != type(None)):
                        for iplayer in WorkingMarkerFolder.invitedPlayers:
                            if (iplayer.ID == tupdata[0]):
                                WorkingMarkerFolder.invitedPlayers.remove(iplayer)
                                break

                    self.IRefreshPlayerList()
                    self.IRefreshPlayerListDisplay()
                    if (BKRightSideMode == kBKMarkerListExpanded):
                        self.IBigKIDisplayCurrentContentMarkerFolder()
            else:
                for request in MarkerJoinRequests:
                    if (request.game.masterID == gameMasterID):
                        request.game.addPlayerToTeam(tupdata[0], tupdata[1])

        elif (msgType == PtMarkerMsgType.kGameStart):
            if (type(CurrentPlayingMarkerGame) != type(None)):
                MarkerGameState = kMGGameOn
                gMarkerToGetColor = 'yellowlt'
                gMarkerGottenColor = 'yellow'
                gMarkerToGetNumber = CurrentPlayingMarkerGame.numberMarkers
                gMarkerGottenNumber = (CurrentPlayingMarkerGame.numberMarkers - CurrentPlayingMarkerGame.markersRemaining)
                if (CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeQuest):
                    workingMF = ptMarkerMgr().getWorkingMarkerFolder()
                    if (type(workingMF) != type(None)):
                        CurrentPlayingMarkerGame.resetScores()
                        markerRefs = workingMF.getChildNodeRefList()
                        for markerRef in markerRefs:
                            if markerRef.beenSeen():
                                mplayer = None
                                if (len(CurrentPlayingMarkerGame.greenTeamPlayers) > 0):
                                    mplayer = CurrentPlayingMarkerGame.greenTeamPlayers[0]
                                elif (len(CurrentPlayingMarkerGame.redTeamPlayers) > 0):
                                    mplayer = CurrentPlayingMarkerGame.redTeamPlayers[0]
                                if mplayer:
                                    mplayer.score += 1
                                    mplayer.updateScore()
                                CurrentPlayingMarkerGame.updateScores()
                                gMarkerToGetNumber = CurrentPlayingMarkerGame.numberMarkers
                                gMarkerGottenNumber = (CurrentPlayingMarkerGame.numberMarkers - CurrentPlayingMarkerGame.markersRemaining)

                    else:
                        print '#### no working folder'
                else:
                    PtAtTimeCallback(self.key, 1, kMarkerGameTimer)
                    CurrentPlayingMarkerGame.startTimer()
                    self.IDoStatusChatMessage(xLocalization.xKI.xMarkerGameBegins, netPropagate=0)
                    if (CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeCapture):
                        for mplayer in (CurrentPlayingMarkerGame.greenTeamPlayers + CurrentPlayingMarkerGame.redTeamPlayers):
                            mplayer.updateScore()

                    self.IRefreshPlayerList()
                    self.IRefreshPlayerListDisplay()
                    if (BKRightSideMode == kBKMarkerListExpanded):
                        self.IBigKIDisplayCurrentContentMarkerFolder()
                self.IRefreshMiniKIMarkerDisplay()
        elif (msgType == PtMarkerMsgType.kGameEnd):
            for qn in MarkerJoinRequests:
                if (qn.game.masterID == gameMasterID):
                    MarkerJoinRequests.remove(qn)
                    if ((BKRightSideMode == kBKQuestionNote) and (BKCurrentContent == qn)):
                        self.IBigKIChangeMode(kBKListMode)
                    else:
                        self.IBKCheckFolderRefresh(ptVault().getInbox())

            if (type(CurrentPlayingMarkerGame) != type(None)):
                if (MarkerGameState == kMGGameOn):
                    if (CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeQuest):
                        pass
                    else:
                        if (CurrentPlayingMarkerGame.greenTeamScore > CurrentPlayingMarkerGame.redTeamScore):
                            winningTeam = (xLocalization.xKI.xMarkerGameGreenTeamWins % (CurrentPlayingMarkerGame.greenTeamScore, CurrentPlayingMarkerGame.redTeamScore))
                        elif (CurrentPlayingMarkerGame.greenTeamScore == CurrentPlayingMarkerGame.redTeamScore):
                            winningTeam = (xLocalization.xKI.xMarkerGameTieGame % (CurrentPlayingMarkerGame.greenTeamScore, CurrentPlayingMarkerGame.redTeamScore))
                        else:
                            winningTeam = (xLocalization.xKI.xMarkerGameRedTeamWins % (CurrentPlayingMarkerGame.redTeamScore, CurrentPlayingMarkerGame.greenTeamScore))
                        self.IDoStatusChatMessage((xLocalization.xKI.xMarkerGameEnded % winningTeam), netPropagate=0)
                        if (CurrentPlayingMarkerGame.gameType != PtMarkerMsgGameType.kGameTypeHold):
                            self.IDoStatusChatMessage(xLocalization.xKI.xMarkerGameResults, netPropagate=0)
                            scorelist = (CurrentPlayingMarkerGame.greenTeamPlayers + CurrentPlayingMarkerGame.redTeamPlayers)
                            scorelist.sort(lambda x, y:cmp(y.score, x.score))
                            for scorer in scorelist:
                                if (scorer.score == 0):
                                    markerText = xLocalization.xKI.xMarkerGameNoMarkers
                                elif (scorer.score == 1):
                                    markerText = xLocalization.xKI.xMarkerGameOneMarker
                                else:
                                    markerText = (xLocalization.xKI.xMarkerGameNMarkers % scorer.score)
                                capText = xLocalization.xKI.xMarkerGameCaptured
                                self.IDoStatusChatMessage(('    %s %s %s' % (scorer.player.getPlayerName(), capText, markerText)), netPropagate=0)

                gMarkerToGetColor = 'off'
                gMarkerGottenColor = 'off'
                gMarkerToGetNumber = 0
                gMarkerGottenNumber = 0
                self.IRefreshMiniKIMarkerDisplay()
                MarkerGameState = kMGNotActive
                CurrentPlayingMarkerGame = None
                self.IResetWorkingMarkerFolder()
                self.IRefreshPlayerList()
                self.IRefreshPlayerListDisplay()
                self.IRefreshMiniKIMarkerDisplay()
                if (BKRightSideMode == kBKMarkerListExpanded):
                    self.IBigKIDisplayCurrentContentMarkerFolder()
        elif (msgType == PtMarkerMsgType.kGamePoint):
            if (type(CurrentPlayingMarkerGame) != type(None)):
                scorer = '?unknown?'
                for mplayer in (CurrentPlayingMarkerGame.greenTeamPlayers + CurrentPlayingMarkerGame.redTeamPlayers):
                    if (mplayer.player.getPlayerID() == tupdata[0]):
                        if ((CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeCapture) or (CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeQuest)):
                            mplayer.score += 1
                            mplayer.updateScore()
                        scorer = mplayer.player.getPlayerName()
                CurrentPlayingMarkerGame.updateScores()
                gMarkerToGetNumber = CurrentPlayingMarkerGame.numberMarkers
                gMarkerGottenNumber = (CurrentPlayingMarkerGame.numberMarkers - CurrentPlayingMarkerGame.markersRemaining)
                self.IRefreshMiniKIMarkerDisplay()
                if (CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeQuest):
                    self.IDoStatusChatMessage((xLocalization.xKI.xMarkerGameFoundMarker % tupdata[1]), netPropagate=0)
                    if gMarkerGottenNumber >= gMarkerToGetNumber:
                        self.IDoStatusChatMessage(xLocalization.xKI.xMarkerGameStatusAllFound, netPropagate=0)
                else:
                    markerleft = ''
                    if (CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeCapture):
                        if (CurrentPlayingMarkerGame.markersRemaining == 0):
                            markerleft = xLocalization.xKI.xMarkerGameLastMarker
                        elif (CurrentPlayingMarkerGame.markersRemaining == 1):
                            markerleft = xLocalization.xKI.xMarkerGameOneMoreLeft
                    self.IDoStatusChatMessage((xLocalization.xKI.xMarkerGameCaptures % (scorer, tupdata[1], markerleft)), netPropagate=0)
                    self.IRefreshPlayerList()
                    self.IRefreshPlayerListDisplay()
                if (BKRightSideMode == kBKMarkerListExpanded):
                    self.IBigKIDisplayCurrentContentMarkerFolder()


    def IDetermineCensorLevel(self):
        global theCensorLevel
        theCensorLevel = xCensor.xRatedPG
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleCensorLevel)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleCensorLevel, kChronicleCensorLevelType, ('%d' % theCensorLevel))
        else:
            theCensorLevel = string.atoi(entry.chronicleGetValue())
        PtDebugPrint(('xKI: the censor level is %d' % theCensorLevel), level=kWarningLevel)


    def ISaveCensorLevel(self):
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleCensorLevel)
        if (type(entry) != type(None)):
            entry.chronicleSetValue(('%d' % theCensorLevel))
            entry.save()
        else:
            vault.addChronicleEntry(kChronicleCensorLevel, kChronicleCensorLevelType, ('%d' % theCensorLevel))
        PtDebugPrint(('xKI: Saving Censor level of %d' % theCensorLevel), level=kWarningLevel)


    def IDetermineKILevel(self):
        global gFeather
        global gKIHasJournal
        global theKILevel
        global gKIMarkerLevel
        theKILevel = kNanoKI
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleKILevel)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleKILevel, kChronicleKILevelType, ('%d' % theKILevel))
        else:
            oldLevel = string.atoi(entry.chronicleGetValue())
            if ((oldLevel >= kLowestKILevel) and (oldLevel <= kHighestKILevel)):
                theKILevel = oldLevel
        # don't start with a MicroKI, that does not work
        if theKILevel == kMicroKI: theKILevel = kNanoKI
        # END
        PtDebugPrint(('xKI: the KI level is %d' % theKILevel), level=kWarningLevel)
        gKIMarkerLevel = 0
        entry = vault.findChronicleEntry(kChronicleKIMarkerLevel)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleKIMarkerLevel, kChronicleKIMarkerLevelType, ('%d' % gKIMarkerLevel))
        else:
            gKIMarkerLevel = string.atoi(entry.chronicleGetValue())
        PtDebugPrint(('xKI: the KIMarker level is %d' % gKIMarkerLevel), level=kWarningLevel)
        entry = vault.findChronicleEntry('feather')
        if (type(entry) == type(None)):
            gFeather = 0
        else:
            try:
                gFeather = string.atoi(entry.chronicleGetValue())
            except ValueError:
                gFeather = 0
        gKIHasJournal = 0
        entry = vault.findChronicleEntry(kChronicleHasJournal)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleHasJournal, kChronicleHasJournalType, ('%d' % gKIHasJournal))
        else:
            gKIHasJournal = string.atoi(entry.chronicleGetValue())
        PtDebugPrint(('xKI: the hasJournal value is %d' % gKIHasJournal), level=kWarningLevel)


    def IUpgradeKIMarkerLevel(self, newLevel):
        global gKIMarkerLevel
        PtDebugPrint(('xKI: KIMarker going from %d to %d' % (gKIMarkerLevel, newLevel)), level=kWarningLevel)
        if (theKILevel > kMicroKI):
            if (newLevel > gKIMarkerLevel):
                gKIMarkerLevel = newLevel
                vault = ptVault()
                entry = vault.findChronicleEntry(kChronicleKIMarkerLevel)
                if (type(entry) == type(None)):
                    PtDebugPrint(('xKI: KIMarker level not found - set to %d' % gKIMarkerLevel), level=kWarningLevel)
                    vault.addChronicleEntry(kChronicleKIMarkerLevel, kChronicleKIMarkerLevelType, ('%d' % gKIMarkerLevel))
                else:
                    PtDebugPrint(('xKI: KIMarker upgrading existing level to %d' % gKIMarkerLevel), level=kWarningLevel)
                    entry.chronicleSetValue(('%d' % gKIMarkerLevel))
                    entry.save()


    def IDetermineFontSize(self):
        fontSize = self.IGetFontSize()
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleFontSize)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleFontSize, kChronicleFontSizeType, ('%d' % fontSize))
        else:
            fontSize = string.atoi(entry.chronicleGetValue())
            self.ISetFontSize(fontSize)
        PtDebugPrint(('xKI: the Saved Font Size is %d' % fontSize), level=kWarningLevel)



    def ISaveFontSize(self):
        fontSize = self.IGetFontSize()
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleFontSize)
        if (type(entry) != type(None)):
            entry.chronicleSetValue(('%d' % fontSize))
            entry.save()
        else:
            vault.addChronicleEntry(kChronicleFontSize, kChronicleFontSizeType, ('%d' % fontSize))
        PtDebugPrint(('xKI: Saving Font Size of %d' % fontSize), level=kWarningLevel)



    def IDetermineFadeTime(self):
        global TicksOnFull
        global FadeEnableFlag
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleFadeTime)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleFadeTime, kChronicleFadeTimeType, ('%d' % TicksOnFull))
        else:
            TicksOnFull = string.atoi(entry.chronicleGetValue())
            if (TicksOnFull == kFadeTimeMax):
                FadeEnableFlag = 0
                self.IKillFadeTimer()
                PtDebugPrint('KIDeterineFadeTime: FadeTime disabled', level=kWarningLevel)
            else:
                FadeEnableFlag = 1
        PtDebugPrint(('xKI: the Saved Fade Time is %d' % TicksOnFull), level=kWarningLevel)



    def ISaveFadeTime(self):
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleFadeTime)
        if (type(entry) != type(None)):
            entry.chronicleSetValue(('%d' % TicksOnFull))
            entry.save()
        else:
            vault.addChronicleEntry(kChronicleFadeTime, kChronicleFadeTimeType, ('%d' % TicksOnFull))
        PtDebugPrint(('xKI: Saving Fade Time of %d' % TicksOnFull), level=kWarningLevel)



    def IDetermineKIFlags(self):
        global OnlyAllowBuddiesOnRequest
        global OnlyGetPMsFromBuddies
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleOnlyPMs)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleOnlyPMs, kChronicleOnlyPMsType, ('%d' % OnlyGetPMsFromBuddies))
        else:
            OnlyGetPMsFromBuddies = string.atoi(entry.chronicleGetValue())
        entry = vault.findChronicleEntry(kChronicleBuddiesOnRequest)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleBuddiesOnRequest, kChronicleBuddiesOnRequestType, ('%d' % OnlyAllowBuddiesOnRequest))
        else:
            OnlyAllowBuddiesOnRequest = string.atoi(entry.chronicleGetValue())



    def ISaveKIFlags(self):
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleOnlyPMs)
        if (type(entry) != type(None)):
            entry.chronicleSetValue(('%d' % OnlyGetPMsFromBuddies))
            entry.save()
        else:
            vault.addChronicleEntry(kChronicleOnlyPMs, kChronicleOnlyPMsType, ('%d' % OnlyGetPMsFromBuddies))
        entry = vault.findChronicleEntry(kChronicleBuddiesOnRequest)
        if (type(entry) != type(None)):
            entry.chronicleSetValue(('%d' % OnlyAllowBuddiesOnRequest))
            entry.save()
        else:
            vault.addChronicleEntry(kChronicleBuddiesOnRequest, kChronicleBuddiesOnRequestType, ('%d' % OnlyAllowBuddiesOnRequest))



    def IDetermineGZ(self):
        global gMarkerToGetColor
        global gMarkerToGetNumber
        global gGZPlaying
        global gMarkerGottenColor
        global gMarkerGottenNumber
##############################################################################
# Changes for PotS markers
##############################################################################
#        if (gKIMarkerLevel > kKIMarkerNotUpgraded):
#            if (gKIMarkerLevel < kKIMarkerNormalLevel):
#                vault = ptVault()
#                entry = vault.findChronicleEntry(kChronicleGZGames)
#                if (type(entry) != type(None)):
#                    gameString = entry.chronicleGetValue()
#                    print ('xKI:GZ - game string is %s' % gameString)
#                    args = gameString.split()
#                    if (len(args) == 3):
#                        try:
#                            gGZPlaying = string.atoi(args[0])
#                            colors = args[1].split(':')
#                            gMarkerGottenColor = colors[0]
#                            gMarkerToGetColor = colors[1]
#                            outof = args[2].split(':')
#                            gMarkerGottenNumber = string.atoi(outof[0])
#                            gMarkerToGetNumber = string.atoi(outof[1])
#                            return
#                        except ValueError:
#                            print 'xKI:GZ - error trying to read GZGames Chronicle'
#                    else:
#                        print 'xKI:GZ - error GZGames string formation error'
#                gGZPlaying = 0
#                gMarkerToGetColor = 'off'
#                gMarkerGottenColor = 'off'
#                gMarkerToGetNumber = 0
#                gMarkerGottenNumber = 0
#            else:
#                gGZPlaying = 0
#                if ((MarkerGameState == kMGNotActive) or (type(CurrentPlayingMarkerGame) == type(None))):
#                    gMarkerToGetColor = 'off'
#                    gMarkerGottenColor = 'off'
#                    gMarkerToGetNumber = 0
#                    gMarkerGottenNumber = 0
#        else:
#            gGZPlaying = 0
#            gMarkerToGetColor = 'off'
#            gMarkerGottenColor = 'off'
#            gMarkerToGetNumber = 0
#            gMarkerGottenNumber = 0
        (GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber) = PtDetermineGZ()
        if (GZPlaying == 0):
            if ((MarkerGameState == kMGNotActive) or (type(CurrentPlayingMarkerGame) == type(None))):
                pass
            else:
                return
        gGZPlaying = GZPlaying
        gMarkerToGetColor = MarkerToGetColor
        gMarkerGottenColor = MarkerGottenColor
        gMarkerToGetNumber = MarkerToGetNumber
        gMarkerGottenNumber = MarkerGottenNumber
##############################################################################
# End changes for PotS markers
##############################################################################



    def IGZFlashUpdate(self, gameString):
        global gMarkerToGetColor
        global gMarkerToGetNumber
        global gGZPlaying
        global gMarkerGottenColor
        global gMarkerGottenNumber
        if (gKIMarkerLevel > kKIMarkerNotUpgraded):
            if (gKIMarkerLevel < kKIMarkerNormalLevel):
                print ('xKI:GZ FLASH - game string is %s' % gameString)
                args = gameString.split()
                if (len(args) == 3):
                    try:
                        GZPlaying = string.atoi(args[0])
                        colors = args[1].split(':')
                        MarkerGottenColor = colors[0]
                        MarkerToGetColor = colors[1]
                        outof = args[2].split(':')
                        MarkerGottenNumber = string.atoi(outof[0])
                        MarkerToGetNumber = string.atoi(outof[1])
                        gGZPlaying = GZPlaying
                        gMarkerGottenColor = MarkerGottenColor
                        gMarkerToGetColor = MarkerToGetColor
                        gMarkerGottenNumber = MarkerGottenNumber
                        gMarkerToGetNumber = MarkerToGetNumber
                        return
                    except ValueError:
                        print 'xKI:GZ FLASH - error trying to read GZGames Chronicle'
                else:
                    print 'xKI:GZ FLASH - error GZGames string formation error'


    def IUpdateGZGamesChonicles(self):
        if gGZPlaying:
            vault = ptVault()
            entry = vault.findChronicleEntry(kChronicleGZGames)
            upstring = ('%d %s:%s %d:%d' % (gGZPlaying, gMarkerGottenColor, gMarkerToGetColor, gMarkerGottenNumber, gMarkerToGetNumber))
            if (type(entry) != type(None)):
                entry.chronicleSetValue(upstring)
                entry.save()
            else:
                vault.addChronicleEntry(kChronicleGZGames, kChronicleGZGamesType, upstring)


    def IUpdateKILevelChronicle(self):
        if not self.DoesPlayerHaveRelto(): return
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleKILevel)
        if (type(entry) != type(None)):
            entry.chronicleSetValue(('%d' % theKILevel))
            entry.save()
        else:
            vault.addChronicleEntry(kChronicleKILevel, kChronicleKILevelType, ('%d' % theKILevel))


    def IUpdateJournalBookChronicle(self):
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleHasJournal)
        if (type(entry) != type(None)):
            entry.chronicleSetValue(('%d' % gKIHasJournal))
            entry.save()
        else:
            vault.addChronicleEntry(kChronicleHasJournal, kChronicleHasJournalType, ('%d' % gKIHasJournal))



    def IGetNeighborhood(self):
        try:
            return ptVault().getLinkToMyNeighborhood().getAgeInfo()
        except AttributeError:
            PtDebugPrint('xKI: neighborhood was not found', level=kDebugDumpLevel)
            return None



    def IGetNeighbors(self):
        try:
            return self.IGetNeighborhood().getAgeOwnersFolder()
        except AttributeError:
            PtDebugPrint('xKI: list of neighbors was not found', level=kDebugDumpLevel)
            return None



    def IGetAgeFileName(self, ageInfo = None):
        if (type(ageInfo) == type(None)):
            ageInfo = PtGetAgeInfo()
        if (type(ageInfo) != type(None)):
            return ageInfo.getAgeFilename()
        else:
            return '?UNKNOWN?'



    def IGetAgeInstanceName(self, ageInfo = None):
        if (type(ageInfo) == type(None)):
            ageInfo = PtGetAgeInfo()
        if (type(ageInfo) != type(None)):
            if (ageInfo.getAgeInstanceName() == "D'ni-Rudenna"):
                sdl = xPsnlVaultSDL()
                if ((sdl['TeledahnPoleState'][0] > 5) or ((sdl['KadishPoleState'][0] > 5) or ((sdl['GardenPoleState'][0] > 5) or (sdl['GarrisonPoleState'][0] > 5)))):
                    pass
                else:
                    return '???'
            if (ageInfo.getAgeInstanceName() == "Ae'gura"):
                return "D'ni-Ae'gura"
            return self.IFilterAgeName(xLocalization.xGlobal.LocalizeAgeName(ageInfo.getAgeInstanceName()))
        else:
            return '?UNKNOWN?'



    def IGetAgeDisplayName(self, ageInfo = None):
        if (type(ageInfo) == type(None)):
            ageInfo = PtGetAgeInfo()
        if (type(ageInfo) != type(None)):
            if (ageInfo.getAgeInstanceName() == "D'ni-Rudenna"):
                sdl = xPsnlVaultSDL()
                if ((sdl['TeledahnPoleState'][0] > 5) or ((sdl['KadishPoleState'][0] > 5) or ((sdl['GardenPoleState'][0] > 5) or (sdl['GarrisonPoleState'][0] > 5)))):
                    return "D'ni-Rudenna"
                else:
                    return '???'
            if (ageInfo.getAgeFilename() in xxConfig.PrivateAges) or (ageInfo.getAgeFilename() == "Neighborhood"):
                dispName = xLocalization.xGlobal.LocalizeAgeName(ageInfo.getDisplayName())
                return self.IFilterAgeName(dispName)
            return self.IFilterAgeName(xLocalization.xGlobal.LocalizeAgeName(ageInfo.getAgeInstanceName()))
        else:
            return '?UNKNOWN?'



    def IFilterAgeName(self, ageName):
        # This method is called for age names of an age info struct - some of them are not the way we want them to be
        if (ageName in ['Ae\'gura', 'city', 'spyroom', 'DniCityX2Finale']):
            return "D'ni-Ae'gura"
        if ((ageName == 'GreatZero') or (ageName == 'Great Zero')):
            return "D'ni-Rezeero"
        if (ageName == 'Descent'):
            return "D'ni-Tiwah"
        if (ageName in ['Kveer', "K'veer"]):
            return "D'ni-K'veer"
        for name in xxConfig.AgeNameReplace:
            if (ageName.find(name) != -1):
                return ageName.replace(name, xxConfig.AgeNameReplace[name])
        return ageName



    def ICanAgeBeMadePublic(self, ageInfo):
        try:
            if self.IIsAgeMyNeighborhood(ageInfo):
                return 1
        except AttributeError:
            pass
        return 0



    def ICanAgeInviteVistors(self, ageInfo, link):
        if xxConfig.isOffline(): return 0
        try:
##############################################################################
# diafero define ages one can send invites to
##############################################################################
            if not (ageInfo.getAgeFilename() in xxConfig.InviteAges):
                return 0
##############################################################################
# diafero define ages one can send invites to
##############################################################################
        except AttributeError:
            pass
        if link.getVolatile():
            return 0
        spawnPoints = link.getSpawnPoints()
        for spawnlink in spawnPoints:
            if (spawnlink.getTitle() == 'Default'):
                return 1

        return 0



    def ICanConfigAge(self, ageInfo):
        if (ageInfo.getAgeFilename() == 'Neighborhood'):
            return 1
        return 0



    def IConvertAgeName(self, ageName):
        # This method converts age file anmes to display names, it is used when only the filename is known and not the age info struct
        if (ageName == 'BahroCave'):
            sdl = xPsnlVaultSDL()
            if ((sdl['TeledahnPoleState'][0] > 5) or ((sdl['KadishPoleState'][0] > 5) or ((sdl['GardenPoleState'][0] > 5) or (sdl['GarrisonPoleState'][0] > 5)))):
                return "D'ni-Rudenna"
            else:
                return '???'
        if (ageName in ['Ae\'gura', 'city', 'spyroom', 'DniCityX2Finale']):
            return "D'ni-Ae'gura"
        if ((ageName == 'GreatZero') or (ageName == 'Great Zero')):
            return "D'ni-Rezeero"
        if (ageName == 'Descent'):
            return "D'ni-Tiwah"
        if (ageName == 'Personal02'):
            return "Relto" # this way, Phil's Relto looks like every other Relto in the KI
        return xLinkMgr.GetInstanceName(ageName)



    def IIsAgeMyNeighborhood(self, ageInfo):
        try:
            hoodGUID = ptVault().getLinkToMyNeighborhood().getAgeInfo().getAgeInstanceGuid()
            if ((type(hoodGUID) != type('')) or (hoodGUID == '')):
                PtDebugPrint('xKI: neighborhood GUID not valid', level=kWarningLevel)
                if (ageInfo.getAgeFilename() == 'Neighborhood'):
                    return 1
            elif (ageInfo.getAgeInstanceGuid() == hoodGUID):
                return 1
        except AttributeError:
            pass
        return 0



    def IUpdateKIUsage(self):
        global NumberOfMarkerFolders
        global NumberOfMarkers
        global NumberOfPictures
        global NumberOfNotes
        usage = ptVault().getKIUsage()
        NumberOfPictures = usage[0]
        NumberOfNotes = usage[1]
        NumberOfMarkerFolders = usage[2]
        NumberOfMarkers = usage[3]



    def ICanTakePicture(self):
        self.IUpdateKIUsage()
        if ((kMaxPictures == -1) or (NumberOfPictures < kMaxPictures)):
            return 1
        return 0



    def ICanMakeNote(self):
        self.IUpdateKIUsage()
        if ((kMaxNotes == -1) or (NumberOfNotes < kMaxNotes)):
            return 1
        return 0



    def ICanMakeMarkerFolder(self):
        self.IUpdateKIUsage()
        if ((kMaxMarkerFolders == -1) or (NumberOfMarkerFolders < kMaxMarkerFolders)):
            return 1
        return 0



    def ICanMakeMarker(self):
        self.IUpdateKIUsage()
        if ((kMaxMarkers == -1) or (NumberOfMarkers < kMaxMarkers)):
            return 1
        return 0



    def ICreateMarkerFolder(self):
        global BKFolderSelected
        global LastminiKICenter
        global BKJournalFolderTopLine
        global BKJournalFolderSelected
        global BKFolderTopLine
        global BKCurrentContent
        if PtIsSinglePlayerMode():
            return
        if (PhasedKICreateMarkerGame and (gKIMarkerLevel >= kKIMarkerNormalLevel)):
            if ((not WeAreTakingAPicture) and (not WaitingForAnimation)):
                if ((theKILevel > kMicroKI) and (not IKIDisabled)):
                    journal = BKJournalFolderDict[self.IGetAgeInstanceName()]
                    if (type(journal) != type(None)):
                        KIBlackbar.dialog.hide()
                        toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
                        toggleCB.setChecked(1)
                        modeselector = ptGUIControlRadioGroup(BigKI.dialog.getControlFromTag(kBKRadioModeID))
                        modeselector.setValue(0)
                        BKFolderTopLine = BKJournalFolderTopLine = 0
                        BKFolderSelected = BKJournalFolderSelected = BKJournalListOrder.index(self.IGetAgeInstanceName())
                        self.IBigKIRefreshFolderDisplay()
                        markerlist = ptVaultMarkerListNode(PtVaultNodePermissionFlags.kDefaultPermissions)
                        localplayer = PtGetLocalPlayer()
                        markerlist.folderSetName(("%s's Marker Game" % localplayer.getPlayerName()))
                        markerlist.setOwnerID(localplayer.getPlayerID())
                        markerlist.setOwnerName(localplayer.getPlayerName())
                        markerlist.setGameType(PtMarkerMsgGameType.kGameTypeQuest)
                        markerlist.setRoundLength(120)
                        BKCurrentContent = journal.addNode(markerlist)
                        self.IBigKIChangeMode(kBKMarkerListExpanded)
                        if BigKI.dialog.isEnabled():
                            self.IBigKIShowMode()
                        else:
                            KIMini.dialog.hide()
                            BigKI.dialog.show()
                            KIMini.dialog.show()
                        if (type(LastminiKICenter) == type(None)):
                            if (type(OriginalminiKICenter) != type(None)):
                                dragbar = ptGUIControlDragBar(KIMini.dialog.getControlFromTag(kminiDragBar))
                                LastminiKICenter = dragbar.getObjectCenter()
                                dragbar.setObjectCenter(OriginalminiKICenter)
                                dragbar.anchor()



    def ICreateAMarker(self):
        global YNWhatReason
        if PtIsSinglePlayerMode():
            return
        if ((not WeAreTakingAPicture) and (not WaitingForAnimation)):
            if ((theKILevel > kMicroKI) and (not IKIDisabled)):
                workingMF = ptMarkerMgr().getWorkingMarkerFolder()
                if (type(workingMF) != type(None)):
                    if self.ICanMakeMarker():
                        markerName = (workingMF.folderGetName() + ' marker')
                        ptMarkerMgr().createMarker(markerName)
                    else:
                        YNWhatReason = kYNKIFull
                        reasonField = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                        reasonField.setString(xLocalization.xKI.xKIFullMarkersError)
                        noButton = ptGUIControlButton(KIYesNo.dialog.getControlFromTag(kNoButtonID))
                        noButton.hide()
                        noBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
                        noBtnText.hide()
                        yesBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
                        yesBtnText.setString(xLocalization.xKI.xYesNoOKbutton)
                        KIYesNo.dialog.show()



    def ISetWorkingToCurrentMarkerFolder(self):
        global WorkingMarkerFolder
        MGmgr = ptMarkerMgr()
        WorkingMarkerFolder = MarkerGame(PtGetLocalPlayer().getPlayerID())
        MGmgr.hideMarkersLocal()
        if (type(BKCurrentContent) != type(None)):
            element = BKCurrentContent.getChild()
            if (type(element) != type(None)):
                datatype = element.getType()
                if (datatype == PtVaultNodeTypes.kMarkerListNode):
                    element = element.upcastToMarkerListNode()
                    if element:
                        MGmgr.setWorkingMarkerFolder(element)
                        self.IRefreshPlayerList()
                        self.IRefreshPlayerListDisplay()
                        self.IBKCheckContentRefresh(BKCurrentContent)
                        return element
        return None



    def IGetCurrentMarkerFolder(self):
        if (type(BKCurrentContent) != type(None)):
            element = BKCurrentContent.getChild()
            if (type(element) != type(None)):
                datatype = element.getType()
                if (datatype == PtVaultNodeTypes.kMarkerListNode):
                    element = element.upcastToMarkerListNode()
                    if element:
                        return element
        return None



    def IResetWorkingMarkerFolder(self):
        global WorkingMarkerFolder
        MGmgr = ptMarkerMgr()
        MGmgr.hideMarkersLocal()
        WorkingMarkerFolder = None
        MGmgr.clearWorkingMarkerFolder()
        self.IRefreshPlayerList()
        self.IRefreshPlayerListDisplay()
        self.IBKCheckContentRefresh(BKCurrentContent)



    def IShowYeeshaBook(self):
        global YeeshaBook
        global gCurBookIsYeesha
        if ((theKILevel >= kMicroKI) and ((not IKIDisabled) and (not WaitingForAnimation))):
            if (BigKI.dialog.isEnabled() or KIMini.dialog.isEnabled()):
                self.IminiPutAwayKI()
            startOpen = 0
            gCurBookIsYeesha = 1
            if IsYeeshaBookEnabled:
                if (OfferedBookMode == kNotOffering):
                    if (PhasedKIShareYeeshaBook and xxConfig.isOnline()):
                        YeeshaBDef = (xLinkingBookDefs.xYeeshaBookBase + self.IGetYeeshaPageDefs())
                    else:
                        YeeshaBDef = (xLinkingBookDefs.xYeeshaBookNoShare + self.IGetYeeshaPageDefs())
                else:
                    YeeshaBDef = xLinkingBookDefs.xYeeshaBookNoShare
                    startOpen = 1
            else:
                YeeshaBDef = (xLinkingBookDefs.xYeeshaBookBroke + self.IGetYeeshaPageDefs())
            YeeshaBook = ptBook(YeeshaBDef, self.key)
            YeeshaBook.setSize(xLinkingBookDefs.YeeshaBookSizeWidth, xLinkingBookDefs.YeeshaBookSizeHeight)
            YeeshaBook.show(startOpen)
            PtToggleAvatarClickability(false)



    def IGetYeeshaPageDefs(self):
        pagedef = ''
        vault = ptVault()
        if (type(vault) != type(None)):
            psnlSDL = vault.getPsnlAgeSDL()
            if psnlSDL:
                for (sdlvar, page) in xLinkingBookDefs.xYeeshaPages:
                    FoundValue = psnlSDL.findVar(sdlvar)
                    if (type(FoundValue) != type(None)):
                        state = (FoundValue.getInt() % 10)
                        if (state != 0):
                            active = 1
                            if ((state == 2) or (state == 3)):
                                active = 0
                            try:
                                pagedef += (page % active)
                            except LookupError:
                                pagedef += ('<pb><pb>Bogus page %s' % sdlvar)
                    else:
                        pagedef += ('<pb><pb>Bogus page %s' % sdlvar)

            else:
                PtDebugPrint(('xKI: Error trying to access the Chronicle psnlSDL. psnlSDL = %s' % psnlSDL), level=kErrorLevel)
        else:
            PtDebugPrint("xKI: Error trying to access the Vault. Can't access YeeshaPageChanges chronicle.", level=kErrorLevel)
# custom relto pages BEGIN
        import xCustomReltoPages
        return pagedef + xCustomReltoPages.CustomYeeshaPageDefs()
# custom relto pages END



    def IToggleYeeshaPageSDL(self, varname, on):
        vault = ptVault()
        if (type(vault) != type(None)):
            psnlSDL = vault.getPsnlAgeSDL()
            if psnlSDL:
                ypageSDL = psnlSDL.findVar(varname)
                if ypageSDL:
                    (size, state) = divmod(ypageSDL.getInt(), 10)
                    value = None
                    if ((state == 1) and (not on)):
                        value = 3
                    elif ((state == 3) and on):
                        value = 1
                    elif ((state == 2) and on):
                        value = 4
                    elif ((state == 4) and (not on)):
                        value = 2
                    if (value != None):
                        PtDebugPrint(('KI:Book: setting %s to %d' % (varname, value)), level=kDebugDumpLevel)
                        ypageSDL.setInt(((size * 10) + value))
                        vault.updatePsnlAgeSDL(psnlSDL)



    def IminiChatAreaPageUp(self):
        if PtIsSinglePlayerMode():
            return
        if (theKILevel < kNormalKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        self.IKillFadeTimer()
        self.IStartFadeTimer()
        chatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        chatarea.moveCursor(PtGUIMultiLineDirection.kPageUp)



    def IminiChatAreaPageDown(self):
        if PtIsSinglePlayerMode():
            return
        if (theKILevel < kNormalKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        self.IKillFadeTimer()
        self.IStartFadeTimer()
        chatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        chatarea.moveCursor(PtGUIMultiLineDirection.kPageDown)



    def IminiChatAreaGoToBegin(self):
        if PtIsSinglePlayerMode():
            return
        if (theKILevel < kNormalKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        self.IKillFadeTimer()
        self.IStartFadeTimer()
        chatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        chatarea.moveCursor(PtGUIMultiLineDirection.kBufferStart)



    def IminiChatAreaGoToEnd(self):
        if PtIsSinglePlayerMode():
            return
        if (theKILevel < kNormalKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        self.IKillFadeTimer()
        self.IStartFadeTimer()
        chatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        chatarea.moveCursor(PtGUIMultiLineDirection.kBufferEnd)



    def IGetFontSize(self):
        if PtIsSinglePlayerMode():
            return 0
        if (theKILevel < kNormalKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        MiniChatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        return MiniChatarea.getFontSize()



    def ISetFontSize(self, fontSize):
        PtDebugPrint(('ISetFontSize: Setting font size to %d' % fontSize), level=kWarningLevel)
        if PtIsSinglePlayerMode():
            return
        if (theKILevel < kNormalKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        MiniChatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        MiniChatarea.setFontSize(fontSize)
        MiniChatarea.refresh()
        MicroChatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        MicroChatarea.setFontSize(fontSize)
        MicroChatarea.refresh()
        notearea = ptGUIControlMultiLineEdit(KIJournalExpanded.dialog.getControlFromTag(kBKIJRNNote))
        notearea.setFontSize(fontSize)
        notearea.refresh()
        ownernotes = ptGUIControlMultiLineEdit(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerDescription))
        ownernotes.setFontSize(fontSize)
        ownernotes.refresh()



    def IUpFontSize(self):
        if PtIsSinglePlayerMode():
            return
        size = self.IGetFontSize()
        for i in range((len(FontSizeList) - 1)):
            if (size <= FontSizeList[i]):
                size = FontSizeList[(i + 1)]
                break

        self.ISetFontSize(size)
        self.ISaveFontSize()
        self.IRefreshKISettings()



    def IDownFontSize(self):
        if PtIsSinglePlayerMode():
            return
        size = self.IGetFontSize()
        for i in range((len(FontSizeList) - 1), 0, -1):
            if (size >= FontSizeList[i]):
                size = FontSizeList[(i - 1)]
                break

        self.ISetFontSize(size)
        self.ISaveFontSize()
        self.IRefreshKISettings()



    def IShowJournalBook(self):
        global JournalBook
        global gCurBookIsYeesha
        if ((theKILevel >= kMicroKI) and ((not IKIDisabled) and ((not WaitingForAnimation) and gKIHasJournal))):
            if (BigKI.dialog.isEnabled() or KIMini.dialog.isEnabled()):
                self.IminiPutAwayKI()
            startOpen = 0
            gCurBookIsYeesha = 0
            JournalBDef = xLocalization.xJournalBookDefs.xPlayerJournalSource
            JournalParser = JournalHTMLParser()
            try:
                JournalFile = file(MakeJournalFilename())
                JournalParser.feed(JournalFile.read())
                JournalBInitialText = JournalParser.bodyText
                JournalParser.close()
                JournalFile.close()
            except HTMLParseError, err:
                PtDebugPrint(('xKI: Malformed HTML file, ignoring anything past the error: ' + str(err)))
                JournalBInitialText = ((JournalParser.bodyText + '\n\nError in the HTML, anything past this point has been lost: ') + str(err))
                JournalFile.close()
            except:
                PtDebugPrint("xKI: Journal file doesn't exist, using default text")
                JournalBInitialText = (xLocalization.xJournalBookDefs.xPlayerJournalTitle % PtGetClientName())
            JournalBook = ptBook(JournalBDef, self.key)
            JournalBook.setGUI('bkEditableJournal')
            JournalBook.setSize(xLocalization.xJournalBookDefs.xPlayerJournalXScale, xLocalization.xJournalBookDefs.xPlayerJournalYScale)
            JournalBook.setEditableText(JournalBInitialText)
            JournalBook.show(startOpen)



    def IStartFadeTimer(self):
        global CurrentFadeTick
        global FadeMode
        if PtIsSinglePlayerMode():
            return
        if (not FadeEnableFlag):
            return
##############################################################################
# chat fade fix
# Avoid fading the chat while typing
##############################################################################
        if (self.isChatting):
            self.IKillFadeTimer()
            return
##############################################################################
# End chat fade fix
##############################################################################
        if (PtIsSinglePlayerMode() or (not BigKI.dialog.isEnabled())):
            if (FadeMode == kFadeNotActive):
                PtAtTimeCallback(self.key, kFullTickTime, kFadeTimer)
            FadeMode = kFadeFullDisp
            CurrentFadeTick = TicksOnFull



    def IKillFadeTimer(self):
        global CurrentFadeTick
        global FadeMode
        if PtIsSinglePlayerMode():
            return
        if (theKILevel < kNormalKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        if (FadeMode != kFadeNotActive):
            FadeMode = kFadeStopping
        CurrentFadeTick = TicksOnFull
        mKIdialog.setForeColor(-1, -1, -1, OriginalForeAlpha)
        mKIdialog.setSelectColor(-1, -1, -1, OriginalSelectAlpha)
        if (theKILevel == kNormalKI):
            playerlist = ptGUIControlListBox(mKIdialog.getControlFromTag(kPlayerList))
            playerlist.show()
##############################################################################
# chat fade fix
# not that anything was fading but the scroll arrows and player list before,
# which seems wrong in the first place
##############################################################################
        # diafero's fix for the problem that the chat is not faded but scrolled up (and scolling is wired when it is re-shown)
        # chat is no longer faded
        #chatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        #chatarea.enableScrollControl()
##############################################################################
# End chat fade fix
##############################################################################
        mKIdialog.refreshAllControls()



    def IFadeCompletely(self):
        global FadeMode
        if PtIsSinglePlayerMode():
            return
        if (theKILevel < kNormalKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        if BigKI.dialog.isEnabled():
            mKIdialog.setForeColor(-1, -1, -1, OriginalForeAlpha)
            mKIdialog.setSelectColor(-1, -1, -1, OriginalSelectAlpha)
            mKIdialog.refreshAllControls()
        else:
            mKIdialog.setForeColor(-1, -1, -1, 0)
            mKIdialog.setSelectColor(-1, -1, -1, 0)
            mKIdialog.refreshAllControls()
            if (theKILevel == kNormalKI):
                playerlist = ptGUIControlListBox(mKIdialog.getControlFromTag(kPlayerList))
                playerlist.hide()
##############################################################################
# chat fade fix
##############################################################################
            # diafero's fix for the problem that the chat is not faded but scrolled up (and scolling is wired when it is re-shown)
            # chat is no longer faded
            #chatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
            #chatarea.disableScrollControl()
##############################################################################
# End chat fade fix
##############################################################################
            FadeMode = kFadeNotActive



    def IsChatFaded(self):
        if PtIsSinglePlayerMode():
            return 0
        if (theKILevel >= kMicroKI):
            if ((not BigKI.dialog.isEnabled()) and (KIMini.dialog.isEnabled() or KIMicro.dialog.isEnabled())):
                if (FadeMode == kFadeNotActive):
                    return 1
        return 0



    def IClearBBMini(self, value = -1):
        if (theKILevel < kNormalKI):
            pass
        else:
            mmRG = ptGUIControlRadioGroup(KIBlackbar.dialog.getControlFromTag(kMiniMaximizeRGID))
            mmRG.setValue(value)



    def IEnterChatMode(self, entering, firstChar = None):
        global ToReplyToLastPrivatePlayerID
        if PtIsSinglePlayerMode():
            return
        if (theKILevel == kNanoKI):
            mKIdialog = KIMicro.dialog
            KIMicro.dialog.show()
        elif (theKILevel == kMicroKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        caret = ptGUIControlTextBox(mKIdialog.getControlFromTag(kChatCaretID))
        chatedit = ptGUIControlEditBox(mKIdialog.getControlFromTag(kChatEditboxID))
        if entering:
            if ((theKILevel == kNanoKI) and (CCRConversationInProgress == 0)):
                return
            self.isChatting = 1
            if (not KIMini.dialog.isEnabled()):
                self.IClearBBMini(0)
            if firstChar:
                chatedit.setString(firstChar)
                chatedit.end()
            else:
                chatedit.clearString()
            chatedit.show()
            caret.show()
            mKIdialog.setFocus(chatedit.getKey())
            ToReplyToLastPrivatePlayerID = LastPrivatePlayerID
            self.IKillFadeTimer()
        else:
            caret.hide()
            chatedit.hide()
            self.isChatting = 0
            self.IStartFadeTimer()



    def IGetPlayersInChatDistance(self, minPlayers = 8):
        plyrList = []
        ageplayers = PtGetPlayerListDistanceSorted()
        for ap in ageplayers:
            if (ap.getPlayerID() != 0):
##############################################################################
# BEGIN always shout
##############################################################################
                #if (ap.getDistanceSq() < PtMaxListenDistSq()):
                #    plyrList.append(ap)
                #elif (len(plyrList) <= minPlayers):
                #    plyrList.append(ap)
                plyrList.append(ap)
##############################################################################
# END always shout
##############################################################################
        return plyrList



    def IFindGroupOfBuddies(self, PList):
        outList = []
        for bud in PList:
            if isinstance(bud, ptVaultNodeRef):
                ebud = bud.getChild()
                ebud = ebud.upcastToPlayerInfoNode()
                if (type(ebud) != type(None)):
                    if ebud.playerIsOnline():
                        outList.append(ptPlayer(ebud.playerGetName(), ebud.playerGetID()))

        return outList



    def ISendRTChat(self, message):
        global LastPrivatePlayerID
        cflags = ChatFlags(0)
        cflags.toSelf = 1
        listenerOnly = 1
        betterTellEm = 0
        goesToFolder = None
        if (PtGetLocalAvatar().avatar.getCurrentMode() == PtBrainModes.kAFK):
            PtAvatarExitAFK()
        message = self.ICheckChatCommands(message)
        if (not message):
            return
        if IAmAdmin:
            cflags.admin = 1
        userlbx = ptGUIControlListBox(KIMini.dialog.getControlFromTag(kPlayerList))
        privateChbox = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiPrivateToggle))
        iselect = userlbx.getSelection()
        selPlyrList = []
        if message.startswith(xLocalization.xKI.xChatAllAgeCommand):
            listenerOnly = 0
            selPlyrList = []
            message = message[(len(xLocalization.xKI.xChatAllAgeCommand) + 1):]
        elif message.startswith(xLocalization.xKI.xChatReplyCommand):
            if (type(ToReplyToLastPrivatePlayerID) == type(None)):
                self.IAddRTChat(None, xLocalization.xKI.xChatNoOneToReply, kChatSystemMessage)
                return
            if (not ToReplyToLastPrivatePlayerID[2]):
                agemembers = self.IRemoveCCRPlayers(PtGetPlayerListDistanceSorted())
                hasplayer = 0
                for member in agemembers:
                    if (member.getPlayerID() == ToReplyToLastPrivatePlayerID[1]):
                        hasplayer = 1
                        break

                if (not hasplayer):
                    LastPrivatePlayerID = None
                    self.IAddRTChat(None, (xLocalization.xKI.xChatLeftTheAge % ToReplyToLastPrivatePlayerID[0]), kChatSystemMessage)
                    return
            else:
                vault = ptVault()
                PIKA = vault.getPeopleIKnowAboutFolder()
                if (type(PIKA) != type(None)):
                    if PIKA.playerlistHasPlayer(ToReplyToLastPrivatePlayerID[1]):
                        PIKArefs = PIKA.getChildNodeRefList()
                        for PIKAref in PIKArefs:
                            PIKAelem = PIKAref.getChild()
                            PIKAelem = PIKAelem.upcastToPlayerInfoNode()
                            if (type(PIKAelem) != type(None)):
                                if (PIKAelem.playerGetID() == ToReplyToLastPrivatePlayerID[1]):
                                    if (not PIKAelem.playerIsOnline()):
                                        LastPrivatePlayerID = None
                                        self.IAddRTChat(None, (xLocalization.xKI.xChatLeftTheGame % ToReplyToLastPrivatePlayerID[0]), kChatSystemMessage)
                                        return
                                    break

            message = message[(len(xLocalization.xKI.xChatReplyCommand) + 1):]
            selPlyrList = []
            selPlyrList.append(ptPlayer(ToReplyToLastPrivatePlayerID[0], ToReplyToLastPrivatePlayerID[1]))
            cflags.private = 1
            if ToReplyToLastPrivatePlayerID[2]:
                cflags.interAge = 1
                message = ((('<<' + self.IGetAgeDisplayName()) + '>>') + message)
        elif message.startswith(xLocalization.xKI.xChatPrivateCommand):
            pwords = message.split()
            foundBuddy = 0
            if ((len(pwords) > 1) and (pwords[0] == xLocalization.xKI.xChatPrivateCommand)):
                for daPlayer in BKPlayerList:
                    if isinstance(daPlayer, ptPlayer):
                        plyrName = daPlayer.getPlayerName()
                        if (pwords[1] == plyrName):
                            selPlyrList.append(daPlayer)
                            cflags.private = 1
                            message = message[((message.find(pwords[1]) + len(pwords[1])) + 1):]
                            foundBuddy = 1
                            self.IAddPlayerToRecents(daPlayer.getPlayerID())
                            break
                        if plyrName.startswith(pwords[1]):
                            mrest = message[(len(xLocalization.xKI.xChatPrivateCommand) + 1):]
                            if mrest.startswith(plyrName):
                                selPlyrList.append(daPlayer)
                                cflags.private = 1
                                message = mrest[(len(plyrName) + 1):]
                                foundBuddy = 1
                                self.IAddPlayerToRecents(daPlayer.getPlayerID())
                                break
                    elif isinstance(daPlayer, ptVaultNodeRef):
                        eplyr = daPlayer.getChild()
                        eplyr = eplyr.upcastToPlayerInfoNode()
                        if (type(eplyr) != type(None)):
                            plyrName = eplyr.playerGetName()
                            if (pwords[1] == plyrName):
                                selPlyrList.append(ptPlayer(eplyr.playerGetName(), eplyr.playerGetID()))
                                cflags.private = 1
                                cflags.interAge = 1
                                message = ((('<<' + self.IGetAgeDisplayName()) + '>>') + message[((message.find(pwords[1]) + len(pwords[1])) + 1):])
                                foundBuddy = 1
                                self.IAddPlayerToRecents(eplyr.playerGetID())
                                break
                            if plyrName.startswith(pwords[1]):
                                mrest = message[(len(xLocalization.xKI.xChatPrivateCommand) + 1):]
                                if mrest.startswith(plyrName):
                                    selPlyrList.append(ptPlayer(eplyr.playerGetName(), eplyr.playerGetID()))
                                    cflags.private = 1
                                    cflags.interAge = 1
                                    message = ((('<<' + self.IGetAgeDisplayName()) + '>>') + mrest[(len(plyrName) + 1):])
                                    foundBuddy = 1
                                    self.IAddPlayerToRecents(eplyr.playerGetID())
                                    break

            if (not foundBuddy):
                PtDebugPrint(("xKI:SendRTChat: /p command can't find player %s" % pwords[1]), level=kDebugDumpLevel)
                self.IAddRTChat(None, (xLocalization.xKI.xChatCannotFindBuddy % pwords[1]), kChatSystemMessage)
                return
        elif message.startswith(xLocalization.xKI.xChatNeighborsCommand):
            cflags.neighbors = 1
            message = message[(len(xLocalization.xKI.xChatNeighborsCommand) + 1):]
            neighbors = self.IGetNeighbors()
            if (type(neighbors) != type(None)):
                selPlyrList = self.IFindGroupOfBuddies(neighbors.getChildNodeRefList())
            else:
                selPlyrList = []
            if (len(selPlyrList) == 0):
                self.IAddRTChat(None, (xLocalization.xKI.xChatWentOffline % 'Everyone in your neighbor list'), kChatSystemMessage)
                return
            else:
                cflags.interAge = 1
                message = ((('<<' + self.IGetAgeDisplayName()) + '>>') + message)
                goesToFolder = string.upper(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kHoodMembersFolder))
        elif message.startswith(xLocalization.xKI.xChatBuddiesCommand):
            vault = ptVault()
            buddies = vault.getBuddyListFolder()
            message = message[(len(xLocalization.xKI.xChatBuddiesCommand) + 1):]
            if (type(buddies) != type(None)):
                selPlyrList = self.IFindGroupOfBuddies(buddies.getChildNodeRefList())
            else:
                selPlyrList = []
            if (len(selPlyrList) == 0):
                self.IAddRTChat(None, (xLocalization.xKI.xChatWentOffline % 'Everyone in your buddy list'), kChatSystemMessage)
                return
            else:
                cflags.interAge = 1
                message = ((('<<' + self.IGetAgeDisplayName()) + '>>') + message)
                goesToFolder = string.upper(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kBuddyListFolder))
        elif ((iselect >= 0) and (iselect < len(BKPlayerList))):
            toplyr = BKPlayerList[iselect]
            if isinstance(toplyr, ptPlayer):
                selPlyrList.append(toplyr)
                cflags.private = 1
                self.IAddPlayerToRecents(toplyr.getPlayerID())
                PtDebugPrint(('xKI:SendRTChat: private message to %s' % toplyr.getPlayerName()), level=kDebugDumpLevel)
            elif isinstance(toplyr, ptVaultNodeRef):
                eplyr = toplyr.getChild()
                eplyr = eplyr.upcastToPlayerInfoNode()
                if (type(eplyr) != type(None)):
                    if (not eplyr.playerIsOnline()):
                        self.IAddRTChat(None, (xLocalization.xKI.xChatWentOffline % eplyr.playerGetName()), kChatSystemMessage)
                        return
                    selPlyrList.append(ptPlayer(eplyr.playerGetName(), eplyr.playerGetID()))
                    cflags.private = 1
                    self.IAddPlayerToRecents(eplyr.playerGetID())
                    if PtValidateKey(PtGetAvatarKeyFromClientID(eplyr.playerGetID())):
                        pass
                    else:
                        cflags.interAge = 1
                        message = ((('<<' + self.IGetAgeDisplayName()) + '>>') + message)
            elif isinstance(toplyr, ptVaultPlayerInfoListNode):
                fldrType = toplyr.folderGetType()
                if (fldrType == PtVaultStandardNodes.kAgeOwnersFolder):
                    fldrType = PtVaultStandardNodes.kHoodMembersFolder
                    cflags.neighbors = 1
                selPlyrList = self.IFindGroupOfBuddies(toplyr.getChildNodeRefList())
                if (len(selPlyrList) == 0):
                    self.IAddRTChat(None, (xLocalization.xKI.xChatWentOffline % 'Everyone in list'), kChatSystemMessage)
                    return
                else:
                    cflags.interAge = 1
                    message = ((('<<' + self.IGetAgeDisplayName()) + '>>') + message)
                    goesToFolder = string.upper(xLocalization.FolderIDToFolderName(fldrType))
            elif isinstance(toplyr, kiFolder):
                listenerOnly = 1
                selPlyrList = self.IGetPlayersInChatDistance()
                ageplayers = PtGetPlayerListDistanceSorted()
                if ((len(ageplayers) > 0) and (len(selPlyrList) == 0)):
                    betterTellEm = 1
            elif isinstance(toplyr, MarkerPlayer):
                selPlyrList.append(toplyr.player)
                cflags.private = 1
                PtDebugPrint(('xKI:SendRTChat: private message to %s' % toplyr.player.getPlayerName()), level=kDebugDumpLevel)
            elif isinstance(toplyr, MarkerGame):
                for mplayer in (toplyr.greenTeamPlayers + toplyr.redTeamPlayers):
                    selPlyrList.append(mplayer.player)

                goesToFolder = xLocalization.xKI.xChatMarkerAllTeams
            elif isinstance(toplyr, DPLBranchStatusLine):
                if (type(CurrentPlayingMarkerGame) != type(None)):
                    if (toplyr == CurrentPlayingMarkerGame.greenTeamDPL):
                        for mplayer in CurrentPlayingMarkerGame.greenTeamPlayers:
                            selPlyrList.append(mplayer.player)

                        goesToFolder = xLocalization.xKI.xChatMarkerGreenTeam
                    elif (toplyr == CurrentPlayingMarkerGame.redTeamDPL):
                        for mplayer in CurrentPlayingMarkerGame.redTeamPlayers:
                            selPlyrList.append(mplayer.player)

                        goesToFolder = xLocalization.xKI.xChatMarkerRedTeam
# special characters fix
        if not message.startswith('<<'):
            # for some strange reason, messages are not received properly when  they start with a special charatcer, so make sure they
            # always start with "<" (a charcter which is also used for escaping the age name and can not be typed)
            message = '<>' + message
# END special characters fix
        cflags.channel = PrivateChatChannel
        if ((len(selPlyrList) == 0) and listenerOnly):
            if betterTellEm:
                self.IAddRTChat(None, xLocalization.xKI.xChatNoOneListening, kChatSystemMessage)
        else:
            if ((not PhasedKIInterAgeChat) and cflags.interAge):
                self.IAddRTChat(None, xLocalization.xKI.xChatInterAgeNotAvailable, kChatSystemMessage)
                return
            PtSendRTChat(PtGetLocalPlayer(), selPlyrList, message, cflags.flags)
        sender = PtGetLocalPlayer()
        if cflags.private:
            sender = selPlyrList[0]
        if cflags.interAge:
            if (goesToFolder and (type(goesToFolder) == type(''))):
                sender = ptPlayer(goesToFolder, 0)
            else:
                sender = selPlyrList[0]
        elif (goesToFolder and (type(goesToFolder) == type(''))):
            sender = ptPlayer(goesToFolder, 0)
        self.IAddRTChat(sender, message, cflags)



    def ICheckChatCommands(self, chatmessage, silent = false):
        global gFeather
        global ChatLogFile
        if (string.lower(chatmessage) == xLocalization.xKI.xChatClearAll):
            chatareaU = ptGUIControlMultiLineEdit(KIMicro.dialog.getControlFromTag(kChatDisplayArea))
            chatareaM = ptGUIControlMultiLineEdit(KIMini.dialog.getControlFromTag(kChatDisplayArea))
            chatareaU.clearBuffer()
            chatareaM.clearBuffer()
            return None
        if string.lower(chatmessage).startswith(xLocalization.xKI.xChatStartLogCommand):
            if (type(ChatLogFile) == type(None)):
                ChatLogFile = ptStatusLog()
            ChatLogFile.open('Chat.log', 30, (PtStatusLogFlags.kAppendToLast + PtStatusLogFlags.kTimestamp))
            self.IDoStatusChatMessage(xLocalization.xKI.xChatLogStarted, netPropagate=0)
            return None
        if string.lower(chatmessage).startswith(xLocalization.xKI.xChatStopLogCommand):
            if (type(ChatLogFile) != type(None)):
                if ChatLogFile.isOpen():
                    self.IDoStatusChatMessage(xLocalization.xKI.xChatLogStopped, netPropagate=0)
                ChatLogFile.close()
            return None
        if string.lower(chatmessage).startswith(xLocalization.xKI.xChatAddBuddyCmd):
            (pid, msg) = self.IGetPIDMsg(chatmessage[len(xLocalization.xKI.xChatAddBuddyCmd):])
            if pid:
                localplayer = PtGetLocalPlayer()
                if (pid != localplayer.getPlayerID()):
                    vault = ptVault()
                    buddies = vault.getBuddyListFolder()
                    if (type(buddies) != type(None)):
                        if buddies.playerlistHasPlayer(pid):
                            self.IAddRTChat(None, xLocalization.xKI.xPlayerAlreadyAdded, kChatSystemMessage)
                        else:
                            buddies.playerlistAddPlayer(pid)
                            self.IDoStatusChatMessage(xLocalization.xKI.xPlayerAdded, netPropagate=0)
                else:
                    self.IAddRTChat(None, xLocalization.xKI.xPlayerNotYourself, kChatSystemMessage)
            else:
                self.IAddRTChat(None, xLocalization.xKI.xPlayerNumberOnly, kChatSystemMessage)
            return None
        if string.lower(chatmessage).startswith(xLocalization.xKI.xChatRemoveBuddyCmd):
            (pid, ccrmsg) = self.IGetPIDMsg(chatmessage[len(xLocalization.xKI.xChatRemoveBuddyCmd):])
            if pid:
                vault = ptVault()
                buddies = vault.getBuddyListFolder()
                if (type(buddies) != type(None)):
                    if buddies.playerlistHasPlayer(pid):
                        buddies.playerlistRemovePlayer(pid)
                        self.IDoStatusChatMessage(xLocalization.xKI.xPlayerRemoved, netPropagate=0)
                    else:
                        self.IAddRTChat(None, xLocalization.xKI.xPlayerNotFound, kChatSystemMessage)
            else:
                vault = ptVault()
                buddies = vault.getBuddyListFolder()
                if (type(buddies) != type(None)):
                    buddyrefs = buddies.getChildNodeRefList()
                    theName = string.lstrip(chatmessage[len(xLocalization.xKI.xChatRemoveBuddyCmd):])
                    for plyr in buddyrefs:
                        if isinstance(plyr, ptVaultNodeRef):
                            PLR = plyr.getChild()
                            PLR = PLR.upcastToPlayerInfoNode()
                            if ((type(PLR) != type(None)) and (PLR.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
                                if theName.startswith(PLR.playerGetName()):
                                    buddies.playerlistRemovePlayer(PLR.playerGetID())
                                    self.IDoStatusChatMessage(xLocalization.xKI.xPlayerRemoved, netPropagate=0)
                                    return None

                self.IAddRTChat(None, xLocalization.xKI.xPlayerNumberOnly, kChatSystemMessage)
            return None
        if string.lower(chatmessage).startswith(xLocalization.xKI.xChatIgnoreCmd):
            (pid, ccrmsg) = self.IGetPIDMsg(chatmessage[len(xLocalization.xKI.xChatIgnoreCmd):])
            if pid:
                localplayer = PtGetLocalPlayer()
                if (pid != localplayer.getPlayerID()):
                    vault = ptVault()
                    ignores = vault.getIgnoreListFolder()
                    if (type(ignores) != type(None)):
                        if ignores.playerlistHasPlayer(pid):
                            self.IAddRTChat(None, xLocalization.xKI.xPlayerAlreadyAdded, kChatSystemMessage)
                        else:
                            ignores.playerlistAddPlayer(pid)
                            self.IDoStatusChatMessage(xLocalization.xKI.xPlayerAdded, netPropagate=0)
                else:
                    self.IAddRTChat(None, xLocalization.xKI.xPlayerNotYourself, kChatSystemMessage)
            else:
                self.IAddRTChat(None, xLocalization.xKI.xPlayerNumberOnly, kChatSystemMessage)
            return None
        if string.lower(chatmessage).startswith(xLocalization.xKI.xChatUnIgnoreCmd):
            (pid, ccrmsg) = self.IGetPIDMsg(chatmessage[len(xLocalization.xKI.xChatUnIgnoreCmd):])
            if pid:
                vault = ptVault()
                ignores = vault.getIgnoreListFolder()
                if (type(ignores) != type(None)):
                    if ignores.playerlistHasPlayer(pid):
                        ignores.playerlistRemovePlayer(pid)
                        self.IDoStatusChatMessage(xLocalization.xKI.xPlayerRemoved, netPropagate=0)
                    else:
                        self.IAddRTChat(None, xLocalization.xKI.xPlayerNotFound, kChatSystemMessage)
            else:
                vault = ptVault()
                ignores = vault.getIgnoreListFolder()
                if (type(ignores) != type(None)):
                    ignorerefs = ignores.getChildNodeRefList()
                    theName = string.lstrip(chatmessage[len(xLocalization.xKI.xChatUnIgnoreCmd):])
                    for plyr in ignorerefs:
                        if isinstance(plyr, ptVaultNodeRef):
                            PLR = plyr.getChild()
                            PLR = PLR.upcastToPlayerInfoNode()
                            if ((type(PLR) != type(None)) and (PLR.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
                                if theName.startswith(PLR.playerGetName()):
                                    ignores.playerlistRemovePlayer(PLR.playerGetID())
                                    self.IDoStatusChatMessage(xLocalization.xKI.xPlayerRemoved, netPropagate=0)
                                    return None

                self.IAddRTChat(None, xLocalization.xKI.xPlayerNumberOnly, kChatSystemMessage)
            return None

        #if (PtIsInternalRelease() and (chatmessage == '/revisitcleft')):
        #    vault = ptVault()
        #    chron = vault.findChronicleEntry('CleftSolved')
        #    if (type(chron) != type(None)):
        #        chronFolder = vault.getChronicleFolder()
        #        if (type(chronFolder) != type(None)):
        #            chronFolder.removeNode(chron)
        #    return None
        #if (PtIsInternalRelease() and (chatmessage == '/restart')):
        #    vault = ptVault()
        #    chron = vault.findChronicleEntry('InitialAvCustomizationsDone')
        #    if (type(chron) != type(None)):
        #        chronFolder = vault.getChronicleFolder()
        #        if (type(chronFolder) != type(None)):
        #            chronFolder.removeNode(chron)
        #    chron = vault.findChronicleEntry('IntroPlayed')
        #    if (type(chron) != type(None)):
        #        chronFolder = vault.getChronicleFolder()
        #        if (type(chronFolder) != type(None)):
        #            chronFolder.removeNode(chron)
        #    chron = vault.findChronicleEntry('CleftSolved')
        #    if (type(chron) != type(None)):
        #        chronFolder = vault.getChronicleFolder()
        #        if (type(chronFolder) != type(None)):
        #            chronFolder.removeNode(chron)
        #    return None
        # These commands are quite short and access local variables, so they are left here
#AFK MESSAGE
        if (chatmessage.lower() == '/'+xLocalization.xKI.xAfkCmd) or chatmessage.lower().startswith('/'+xLocalization.xKI.xAfkCmd+' '):
            global gAfkMessage
            # clear afk information list
            global gAfkInformed
            gAfkInformed = {}
            # /clear afk information list
            PtAvatarEnterAFK()
            if len(chatmessage) > len(xLocalization.xKI.xAfkCmd)+2: gAfkMessage = chatmessage[len(xLocalization.xKI.xAfkCmd)+2:]
            else: gAfkMessage = ''
            return None
#/AFK MESSAGE
#KI usage
        if (string.lower(chatmessage) == '/kiusage') or string.lower(chatmessage).startswith('/kiusage '):
            self.IUpdateKIUsage()
            self.IDoStatusChatMessage('Your current KI usage: %d pictures (out of %d), %d notes (out of %d), %d marker missions (out of %d) and %d total mrkers (out of %d)' % (NumberOfPictures, kMaxPictures, NumberOfNotes, kMaxNotes, NumberOfMarkerFolders, kMaxMarkerFolders, NumberOfMarkers, kMaxMarkers), netPropagate=0)
            return None
#/KI usage
#Jalak
        if (AgeName == 'Jalak') and (string.lower(chatmessage) == '/savecolumns' or string.lower(chatmessage).startswith('/savecolumns ')):
            fName = chatmessage[13:].strip()
            if fName:
                fName = (fName + '.txt')
            else:
                fName = 'JalakColumns.txt'
            self.SendNote('self.SaveColumns("sav/%s")' % fName)
            self.IDoStatusChatMessage('Saved Jalak columns to %s' % fName, netPropagate=0)
            return None
        if (AgeName == 'Jalak') and (string.lower(chatmessage) == '/loadcolumns' or string.lower(chatmessage).startswith('/loadcolumns ')):
            fName = chatmessage[13:].strip()
            if fName:
                fName = (fName + '.txt')
            else:
                fName = 'JalakColumns.txt'
            self.SendNote('self.LoadColumns("sav/%s")' % fName)
            self.IDoStatusChatMessage('Loaded Jalak columns from %s' % fName, netPropagate=0)
            return None
#/Jalak
        # special behaviour for server-side commands
        if xxConfig.isOnline() and (chatmessage.startswith('/!') or chatmessage.startswith('/%')): # french keyboards have problems with the !, so % is also possible
            chatmessage = '/!'+chatmessage[2:] # the server only understands the /% prefix
            PtSendRTChat(PtGetLocalPlayer(), [], chatmessage, ChatFlags(0).flags)
            if not silent: self.IDoStatusChatMessage("Sending command to server: "+chatmessage[2:], netPropagate=0)
            return None
        # special behaviour for server-side commands END
        # Check for further KI commands
        if chatmessage.startswith('/'): 
            # execute command
            if (xUserKI.OnCommand(self, chatmessage[1:], BKPlayerList, BKCurrentContent, silent)): return None
        # Check for xKIExtChatCommands
        if chatmessage.startswith('/'):
            words = chatmessage.split()
            try:
                emote = xKIExtChatCommands.xChatEmoteXlate[string.lower(words[0][1:])]
                PtEmoteAvatar(emote[0])
                statusMsg = ''
                try:
                    statusMsg = (emote[1] % PtGetLocalPlayer().getPlayerName())
                except TypeError:
                    avatar = PtGetLocalAvatar()
                    gender = avatar.avatar.getAvatarClothingGroup()
                    if (gender > kFemaleClothingGroup):
                        gender = kMaleClothingGroup
                    hisher = 'his'
                    if (gender == kFemaleClothingGroup):
                        hisher = 'her'
                    try:
                        statusMsg = (emote[1] % (PtGetLocalPlayer().getPlayerName(), hisher))
                    except TypeError:
                        statusMsg = emote[1]
                if not silent: self.IDoStatusChatMessage(statusMsg)
                chatmessage = chatmessage[len(words[0]):]
                if (chatmessage == ''):
                    return None
                return chatmessage[1:]
            except LookupError:
                try:
                    command = xKIExtChatCommands.xChatExtendedChat[string.lower(words[0][1:])]
                    if (type(command) == type('')):
                        args = chatmessage[len(words[0]):]
                        PtConsole((command + args))
                    else:
                        try:
                            args = chatmessage[(len(words[0]) + 1):]
                            if (args != ''):
                                try:
                                    retDisp = command(args)
                                except TypeError:
                                    retDisp = command()
                                    return args
                            else:
                                retDisp = command()
                            if (type(retDisp) == type('')):
                                self.IDoStatusChatMessage(retDisp, netPropagate=0)
                            elif (type(retDisp) == type(())):
                                if retDisp[0]:
                                    self.IAddRTChat(None, retDisp[1], kChatSystemMessage)
                                else:
                                    self.IDoStatusChatMessage(retDisp[1], netPropagate=0)
                        except:
                            PtDebugPrint('xKI: chat command function did not run', command, level=kErrorLevel)
                    return None
                except LookupError:
                    if (string.lower(words[0]) in xKIExtChatCommands.xChatSpecialHandledCommands):
                        return chatmessage
                    else:
                        self.IAddRTChat(None, (xLocalization.xKI.xCommandErrorMessage1 % chatmessage), kChatSystemMessage)
                    return None
        # No command at all
        return chatmessage


    def IGetPIDMsg(self, message):
        lmsg = message.split()
        try:
            pid = long(string.atoi(lmsg[0]))
            omsg = message[(message.index(lmsg[0]) + len(lmsg[0])):]
            return (pid, omsg)
        except IndexError:
            return (0, '')
        except ValueError:
            for daPlayer in BKPlayerList:
                if isinstance(daPlayer, ptPlayer):
                    plyrName = daPlayer.getPlayerName()
                    if (lmsg[0] == plyrName):
                        message = message[((message.find(lmsg[0]) + len(lmsg[0])) + 1):]
                        return (daPlayer.getPlayerID(), message)
                    if plyrName.startswith(lmsg[0]):
                        if message.startswith(plyrName):
                            message = message[(len(plyrName) + 1):]
                        return (daPlayer.getPlayerID(), message)
            return (0, '')


    def ICCRErrorMsg(self, res):
        if (res == -1):
            return 'Unknown error'
        elif (res == -2):
            return 'Not Authorized'
        elif (res == -3):
            return 'Nil Local Avatar'
        elif (res == -4):
            return ' CCR Already Allocated'
        elif (res == -5):
            return ' Networking Is Disabled'
        elif (res == -6):
            return "Can't Find Player"
        elif (res == -7):
            return 'Invalid Level'
        elif (res == -8):
            return 'Player Not In Age'



    def IAddRTChat(self, player, message, cflags, forceKI = 1):
        global LastPrivatePlayerID
        if PtIsSinglePlayerMode():
            return
        PtDebugPrint(('xKI:IAddRTChat: message=%s' % message), player, cflags, level=kDebugDumpLevel)
# special characters fix
        if message.startswith('<>'):
            message = message[2:]
# END special characters fix
#-#-#-# cjkelly1's control-character fix
        (message,RogueCount) = re.subn('[\x00-\x08\x0b-\x0c\x0e-\x1f]','',message)
        if (RogueCount > 0):
            PtDebugPrint(('xKI:IAddRTChat: Stripping out %u rogue control characters' % RogueCount))
#-#-#-# end cjkelly1's control-character fix
        if ((theKILevel == kMicroKI) or (theKILevel == kNanoKI)):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        pretext = ''
        headerColor = ChatHeaderBroadcastColor
        bodyColor = ChatMessageColor
        if isinstance(cflags, ChatFlags):
            if cflags.status:
                bodyColor = ChatHeaderStatusColor
                player = None
            elif cflags.interAge:
                if cflags.private:
                    headerColor = ChatHeaderPrivateColor
                    forceKI = 1
                elif cflags.neighbors:
                    headerColor = ChatHeaderNeighborsColor
                else:
                    headerColor = ChatHeaderBuddiesColor
                if cflags.toSelf:
                    pretext = xLocalization.xKI.xChatInterAgeSendTo
                    if (message[:2] == '<<'):
                        try:
                            idx = message.index('>>')
                            message = message[(idx + 2):]
                        except ValueError:
                            pass
                else:
                    if (not self.IIfOnlyBuddyCheck(player.getPlayerID())):
                        return
                    pretext = xLocalization.xKI.xChatInterAgeMsgRecvd
                    forceKI = 1
                    if (message[:2] == '<<'):
                        try:
                            idx = message.index('>>')
                            player = ptPlayer((xLocalization.xKI.xChatInterAgePlayerRecvd % (player.getPlayerName(), message[2:idx])), player.getPlayerID())
                            message = message[(idx + 2):]
                            # start code snippet by D'Lanor: add unknown buddy to recents
                            if ((not cflags.private) and (not cflags.neighbors)):
                                buddies = ptVault().getBuddyListFolder()
                                if (type(buddies) != type(None)):
                                    buddyID = player.getPlayerID()
                                    if (not buddies.playerlistHasPlayer(buddyID)):
                                        PtDebugPrint('xKI: Add unknown buddy %d to recents' % buddyID)
                                        self.IAddPlayerToRecents(buddyID)
                            # end code snippet
                        except ValueError:
                            pass
                    if cflags.private:
                        LastPrivatePlayerID = (player.getPlayerName(), player.getPlayerID(), 1)
                        self.IAddPlayerToRecents(player.getPlayerID())
            elif cflags.admin:
                if cflags.private:
                    headerColor = ChatHeaderErrorColor
                    pretext = xLocalization.xKI.xChatPrivateMsgRecvd
                    forceKI = 1
                else:
                    headerColor = ChatHeaderCCRColor
                    forceKI = 1
                    PtDebugPrint('xKI: an admin broadcast message!', level=kWarningLevel)
            elif cflags.broadcast:
                if cflags.toSelf:
                    headerColor = ChatHeaderBroadcastColor
                    pretext = xLocalization.xKI.xChatBroadcastSendTo
                else:
                    headerColor = ChatHeaderBroadcastColor
                    pretext = xLocalization.xKI.xChatBroadcastMsgRecvd
                    self.IAddPlayerToRecents(player.getPlayerID())
            elif cflags.private:
                if cflags.toSelf:
                    headerColor = ChatHeaderPrivateColor
                    pretext = xLocalization.xKI.xChatPrivateSendTo
                else:
                    if (not self.IIfOnlyBuddyCheck(player.getPlayerID())):
                        return
                    headerColor = ChatHeaderPrivateColor
                    pretext = xLocalization.xKI.xChatPrivateMsgRecvd
                    forceKI = 1
                    LastPrivatePlayerID = (player.getPlayerName(), player.getPlayerID(), 0)
                    self.IAddPlayerToRecents(player.getPlayerID())
        elif (cflags == kChatSystemMessage):
            headerColor = ChatHeaderErrorColor
            pretext = xLocalization.xKI.xChatErrorMsgRecvd
        elif (cflags == kChatCCRMessage):
            headerColor = ChatHeaderCCRColor
            pretext = xLocalization.xKI.xChatCCRMsgRecvd
        elif (cflags == kChatCCRMessageSelf):
            headerColor = ChatHeaderCCRColor
            pretext = xLocalization.xKI.xChatCCRSendTo
        elif (cflags == kChatCCRMessageFromPlayer):
            headerColor = ChatHeaderCCRColor
        else:
            headerColor = ChatHeaderBroadcastColor
            pretext = xLocalization.xKI.xChatBroadcastMsgRecvd
        if (forceKI and ((not IKIDisabled) and (not mKIdialog.isEnabled()))):
            mKIdialog.show()
        if (type(player) != type(None)):
            chatHeaderFormatted = ((('\n' + pretext) + player.getPlayerName()) + ':')
            chatMessageFormatted = (' ' + message)
        else:
            chatHeaderFormatted = ('\n' + pretext)
            if (pretext == ''):
                chatMessageFormatted = message
            else:
                chatMessageFormatted = (' ' + message)
        chatarea = ptGUIControlMultiLineEdit(mKIdialog.getControlFromTag(kChatDisplayArea))
        chatarea.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
        chatarea.insertColor(headerColor)
        chatarea.insertString(chatHeaderFormatted)
        chatarea.insertColor(bodyColor)
        chatarea.insertString(chatMessageFormatted)
        chatarea.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
        if ((type(ChatLogFile) != type(None)) and ChatLogFile.isOpen()):
            ChatLogFile.write((chatHeaderFormatted[1:] + chatMessageFormatted))
        if (chatarea.getBufferSize() > kMaxChatSize):
            excessChars = (chatarea.getBufferSize() - kMaxChatSize)
            PtDebugPrint(('xKImini: max chat buffer size reached. Removing %d characters' % excessChars), level=kDebugDumpLevel)
##############################################################################
# cjkelly1's Alcugs buffer fix
##############################################################################
#            chatarea.setSelection(0, excessChars)
#            chatarea.deleteSelection()
#            chatarea.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
            encbuff = chatarea.getEncodedBuffer()
            EncBuffList = encbuff.splitlines(True)
            BufferLength = len(EncBuffList)
            CurrNum = 0
            LenCount = 0
            while (CurrNum < excessChars):
                CurrNum += len(EncBuffList[LenCount])
                LenCount += 1
            TrimmedEncBuff = ''
            for ChatLine in range(LenCount,len(EncBuffList)):
                TrimmedEncBuff += EncBuffList[ChatLine]
            chatarea.clearBuffer()
            chatarea.setEncodedBuffer(TrimmedEncBuff)
            chatarea.refresh()
            chatarea.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
##############################################################################
# End cjkelly1's Alcugs buffer fix
##############################################################################
        if (theKILevel == kMicroKI):
            chatarea2 = ptGUIControlMultiLineEdit(KIMini.dialog.getControlFromTag(kChatDisplayArea))
            chatarea2.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
            chatarea2.insertColor(headerColor)
            chatarea2.insertString(chatHeaderFormatted)
            chatarea2.insertColor(bodyColor)
            chatarea2.insertString(chatMessageFormatted)
            chatarea2.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
            if (chatarea2.getBufferSize() > kMaxChatSize):
                excessChars = (chatarea2.getBufferSize() - kMaxChatSize)
                PtDebugPrint(('xKImicro: max chat buffer size reached. Removing %d characters' % excessChars), level=kDebugDumpLevel)
##############################################################################
# cjkelly1's Alcugs buffer fix
##############################################################################
#                chatarea2.setSelection(0, excessChars)
#                chatarea2.deleteSelection()
#                chatarea2.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
                encbuff = chatarea2.getEncodedBuffer()
                EncBuffList = encbuff.splitlines(True)
                BufferLength = len(EncBuffList)
                CurrNum = 0
                LenCount = 0
                while (CurrNum < excessChars):
                    CurrNum += len(EncBuffList[LenCount])
                    LenCount += 1
                TrimmedEncBuff = ''
                for ChatLine in range(LenCount,len(EncBuffList)):
                    TrimmedEncBuff += EncBuffList[ChatLine]
                chatarea2.clearBuffer()
                chatarea2.setEncodedBuffer(TrimmedEncBuff)
                chatarea2.refresh()
                chatarea2.moveCursor(PtGUIMultiLineDirection.kBufferEnd)
##############################################################################
# End cjkelly1's Alcugs buffer fix
##############################################################################
        mKIdialog.refreshAllControls()
        if (not self.isChatting):
            self.IKillFadeTimer()
            self.IStartFadeTimer()



    def IIfOnlyBuddyCheck(self, playerID):
        if OnlyGetPMsFromBuddies:
            buddies = ptVault().getBuddyListFolder()
            if (type(buddies) != type(None)):
                return buddies.playerlistHasPlayer(playerID)
            return 0
        return 1



    def IAddPlayerToRecents(self, playerID):
        vault = ptVault()
        PIKA = vault.getPeopleIKnowAboutFolder()
        if (type(PIKA) != type(None)):
            NumberOfRecents = PIKA.getChildNodeCount()
            if (NumberOfRecents >= MaxRecents):
                i = 0
                while (i < 3):
                    fldrContent = PIKA.getChildNodeRefList()
                    fldrContent.sort(CMPNodeDate)
                    fldrContent.reverse()
                    plyrElement = fldrContent[0].getChild()
                    PtDebugPrint(('xKI: removing element %d from recents' % plyrElement.getID()), level=kDebugDumpLevel)
                    PIKA.removeNode(plyrElement)
                    i = (i + 1)
            if (not PIKA.playerlistHasPlayer(playerID)):
                PIKA.playerlistAddPlayer(playerID)



    def IDoStatusChatMessage(self, statusMessage, netPropagate = 1):
        cflags = ChatFlags(0)
        cflags.toSelf = 1
        cflags.status = 1
        if netPropagate:
            plyrList = self.IGetPlayersInChatDistance()
            if (len(plyrList) > 0):
                PtSendRTChat(PtGetLocalPlayer(), plyrList, statusMessage, cflags.flags)
        self.IAddRTChat(None, statusMessage, cflags)



    def IDoErrorChatMessage(self, errorMessage):
        self.IAddRTChat(None, errorMessage, kChatSystemMessage)


    def IScrollUpListbox(self, control, upbtnID, downbtnID):
        if PtIsSinglePlayerMode():
            return
        if ((theKILevel == kMicroKI) or (theKILevel == kNanoKI)):
            return
        elif (theKILevel == kMicroKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        currPos = control.getScrollPos()
        if (currPos < control.getScrollRange()):
            PtDebugPrint(('xKI: Scroll listbox UP from %d to %d' % (currPos, (currPos + 1))), level=kDebugDumpLevel)
            control.setScrollPos((currPos + 1))
        else:
            PtDebugPrint(('xKI: Scroll listbox UP - No! currPos=%d and range=%d' % (currPos, control.getScrollRange())), level=kDebugDumpLevel)
        self.ICheckScrollButtons(control, upbtnID, downbtnID)
        mKIdialog.refreshAllControls()
        self.IKillFadeTimer()
        self.IStartFadeTimer()


    def IScrollDownListbox(self, control, upbtnID, downbtnID):
        if PtIsSinglePlayerMode():
            return
        if ((theKILevel == kMicroKI) or (theKILevel == kNanoKI)):
            return
        elif (theKILevel == kMicroKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        currPos = control.getScrollPos()
        if (currPos > 0):
            PtDebugPrint(('xKI: Scroll Chat area DOWN from %d to %d' % (currPos, (currPos - 1))), level=kDebugDumpLevel)
            control.setScrollPos((currPos - 1))
        else:
            PtDebugPrint(('xKI: Scroll Chat area DOWN - No! currPos=%d' % currPos), level=kDebugDumpLevel)
        self.ICheckScrollButtons(control, upbtnID, downbtnID)
        mKIdialog.refreshAllControls()
        self.IKillFadeTimer()
        self.IStartFadeTimer()


    def ICheckScrollButtons(self, control, upbtnID, downbtnID):
        if PtIsSinglePlayerMode():
            return
        if ((theKILevel == kMicroKI) or (theKILevel == kNanoKI)):
            return
        elif (theKILevel == kMicroKI):
            mKIdialog = KIMicro.dialog
        else:
            mKIdialog = KIMini.dialog
        currentPos = control.getScrollPos()
        PtDebugPrint(('xKI: Check scroll currPos=%d and range=%d' % (currentPos, control.getScrollRange())), level=kDebugDumpLevel)
        try:
            dbtn = ptGUIControlButton(mKIdialog.getControlFromTag(downbtnID))
            if (currentPos == 0):
                dbtn.hide()
            else:
                dbtn.show()
            ubtn = ptGUIControlButton(mKIdialog.getControlFromTag(upbtnID))
            if (currentPos >= control.getScrollRange()):
                ubtn.hide()
            else:
                ubtn.show()
        except KeyError:
            pass


    def IRefreshPlayerList(self, forceSmall = 0):
        global PreviouslySelectedPlayer
        global BKPlayerList
        if PtIsSinglePlayerMode():
            return
        PtDebugPrint('xBigKI: refresh playerlist', level=kDebugDumpLevel)
        playerlist = ptGUIControlListBox(KIMini.dialog.getControlFromTag(kPlayerList))
        select = playerlist.getSelection()
        if ((select >= 0) and (select < len(BKPlayerList))):
            PreviouslySelectedPlayer = BKPlayerList[select]
        else:
            PreviouslySelectedPlayer = None
        BKPlayerList = []
        vault = ptVault()

        # This code block used to be in here twice, one time with the devices, one time without them - I just simplified the code
        agemembers = kiFolder(PtVaultStandardNodes.kAgeMembersFolder)
        if (type(agemembers) != type(None)):
            BKPlayerList.append(agemembers)
# Manage hidden players BEGIN
            BKPlayerList += self.IRemoveCCRPlayers(PtGetPlayerListDistanceSorted(), true)
# Manage hidden players END
        else:
            BKPlayerList.append('?NOAgeMembers?')
        if PhasedKIBuddies:
            buddies = vault.getBuddyListFolder()
            if (type(buddies) != type(None)):
                BKPlayerList.append(buddies)
# Manage hidden players BEGIN
                BKPlayerList += self.IRemoveOfflinePlayers(buddies.getChildNodeRefList(), true)
# Manage hidden players END
            else:
                BKPlayerList.append('?NOBuddies?')
        if PhasedKINeighborsInDPL:
            neighbors = self.IGetNeighbors()
            if (type(neighbors) != type(None)):
                BKPlayerList.append(neighbors)
# Manage hidden players BEGIN
                BKPlayerList += self.IRemoveOfflinePlayers(neighbors.getChildNodeRefList(), true)
# Manage hidden players END
            else:
                BKPlayerList.append('NEIGHBORS')

        if (BigKI.dialog.isEnabled() and (not forceSmall)):
            if ((type(FolderOfDevices) != type(None)) and (len(FolderOfDevices) > 0)):
                BKPlayerList.append(FolderOfDevices)
                for device in FolderOfDevices:
                    BKPlayerList.append(device)

        if (MarkerGameState == kMGNotActive):
            if (type(WorkingMarkerFolder) != type(None)):
                markerGame = ptMarkerMgr().getWorkingMarkerFolder()
                if (type(markerGame) != type(None)):
                    BKPlayerList.append(markerGame)
                    if (markerGame.getGameType() != PtMarkerMsgGameType.kGameTypeQuest):
                        BKPlayerList += WorkingMarkerFolder.invitedPlayers
        elif (type(CurrentPlayingMarkerGame) != type(None)):
            if (CurrentPlayingMarkerGame.gameType == PtMarkerMsgGameType.kGameTypeQuest):
                pass
            else:
                CurrentPlayingMarkerGame.addToDPLPlaying(BKPlayerList)
                if ((MarkerGameState == kMGGameCreation) and (type(WorkingMarkerFolder) != type(None))):
                    inviteTitlePosted = 0
                    for invitePlayer in WorkingMarkerFolder.invitedPlayers:
                        if (not invitePlayer.isJoined):
                            if (not inviteTitlePosted):
                                BKPlayerList.append('Invited')
                                inviteTitlePosted = 1
                            BKPlayerList.append(invitePlayer)




    def IRemoveOfflinePlayers(self, playerlist, removeHidden = false):
        onlinelist = []
        ignores = ptVault().getIgnoreListFolder()
        for plyr in playerlist:
            if isinstance(plyr, ptVaultNodeRef):
                PLR = plyr.getChild()
                PLR = PLR.upcastToPlayerInfoNode()
                if ((type(PLR) != type(None)) and (PLR.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
                    if PLR.playerIsOnline():
                        if (not ignores.playerlistHasPlayer(PLR.playerGetID())):
# Manage hidden players BEGIN
                            if (gShowHiddenPlayers) or (not removeHidden) or (not len(PLR.getCreateAgeName())):
# Manage hidden players END
                                onlinelist.append(plyr)

        return onlinelist



    def IRemoveCCRPlayers(self, playerlist, removeHidden = false):
        nonCCRlist = []
        for plyr in playerlist:
            if isinstance(plyr, ptPlayer):
# Manage hidden players BEGIN
                if (gShowHiddenPlayers) or (not removeHidden) or ((not plyr.isCCR()) and (not plyr.isServer())):
# Manage hidden players END
                    nonCCRlist.append(plyr)

        return nonCCRlist



    def IRefreshPlayerListDisplay(self):
        global PreviouslySelectedPlayer
        global BKPlayerSelected
        if PtIsSinglePlayerMode():
            playerup = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiPlayerListUp))
            playerup.hide()
            playerdown = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiPlayerListDown))
            playerdown.hide()
            return
        PtDebugPrint('xKI: refresh playerlist display', level=kDebugDumpLevel)
        playerlist = ptGUIControlListBox(KIMini.dialog.getControlFromTag(kPlayerList))
        scrollPos = playerlist.getScrollPos()
        playerlist.lock()
        playerlist.clearAllElements()
        newselection = -1
        idx = 0
        for plyr in BKPlayerList:
            if isinstance(plyr, DeviceFolder):
                playerlist.closeBranch()
                playerlist.addBranch(string.upper(plyr.name), 1)
            elif isinstance(plyr, Device):
                playerlist.addStringWithColor(plyr.name, DniSelectableColor, kSelectUseGUIColor)
            elif isinstance(plyr, ptVaultNodeRef):
                PLR = plyr.getChild()
                PLR = PLR.upcastToPlayerInfoNode()
# Manage hidden players BEGIN
                if (type(PLR) != type(None)) and (PLR.getType() == PtVaultNodeTypes.kPlayerInfoNode):
                    if PLR.playerIsOnline() and not len(PLR.getCreateAgeName()):
                        playerlist.addStringWithColor(PLR.playerGetName(), DniSelectableColor, kSelectUseGUIColor)
                    else:
                        playerlist.addStringWithColor(PLR.playerGetName(), AgenBlueDk, kSelectUseGUIColor)
# Manage hidden players END
                else:
                    playerlist.addStringWithColor('?unknown user?', AgenBlueDk, kSelectDetermined)
            elif isinstance(plyr, ptPlayer):
                preText = ' '
                postText = ' '
                if (plyr.getPlayerID() != 0):
                    if (plyr.getDistanceSq() < PtMaxListenDistSq()):
                        preText = '>'
                        postText = '<'
                if (plyr.getPlayerName() != ''):
# Manage hidden players BEGIN
                    if ((not plyr.isCCR()) and (not plyr.isServer())):
                        playerlist.addStringWithColor(preText + plyr.getPlayerName() + postText, DniSelectableColor, kSelectUseGUIColor)
                    else:
                        playerlist.addStringWithColor(preText + plyr.getPlayerName() + postText, AgenBlueDk, kSelectUseGUIColor)
# Manage hidden players END
                elif (plyr.getPlayerID() != 0):
                    playerlist.addStringWithColor(((preText + ('[ID:%08d]' % plyr.getPlayerID())) + postText), AgenBlueDk, kSelectDetermined)
                else:
                    playerlist.addStringWithColor(((preText + '?unknown user?') + postText), AgenBlueDk, kSelectDetermined)
            elif isinstance(plyr, kiFolder):
                playerlist.closeBranch()
                playerlist.addBranch(string.upper(plyr.name), 1)
            elif isinstance(plyr, ptVaultPlayerInfoListNode):
                fldrType = plyr.folderGetType()
                if (fldrType == PtVaultStandardNodes.kAgeOwnersFolder):
                    fldrType = PtVaultStandardNodes.kHoodMembersFolder
                playerlist.closeBranch()
                playerlist.addBranch(string.upper(xLocalization.FolderIDToFolderName(fldrType)), 1)
            elif isinstance(plyr, ptVaultMarkerListNode):
                playerlist.closeBranch()
                playerlist.addBranch(plyr.folderGetName(), 1)
            elif isinstance(plyr, MarkerPlayer):
                if (type(plyr.player) != type(None)):
                    if (plyr.player.getPlayerName() != ''):
                        pcolor = AgenBlueDk
                        if plyr.isJoined:
                            if (plyr.team == PtMarkerMsgTeam.kGreenTeam):
                                pcolor = DniGreenDk
                            elif (plyr.team == PtMarkerMsgTeam.kRedTeam):
                                pcolor = DniRed
                        playerlist.addStringWithColor((plyr.player.getPlayerName() + plyr.scoreText), pcolor, kSelectUseGUIColor)
                    else:
                        playerlist.addStringWithColor(('?offline userID[%d]?' % plyr.player.getPlayerID()), AgenBlueDk, kSelectDetermined)
                else:
                    playerlist.addStringWithColor('?unknown user?', AgenBlueDk, kSelectDetermined)
            elif isinstance(plyr, MarkerGame):
                playerlist.closeBranch()
                playerlist.addBranch(plyr.gameName, 1)
            elif isinstance(plyr, DPLBranchStatusLine):
                if plyr.closePrev:
                    playerlist.closeBranch()
                plyr.position = idx
                playerlist.addBranch(plyr.text, 1)
            elif isinstance(plyr, DPLStatusLine):
                plyr.position = idx
                if (type(plyr.color) != type(None)):
                    clr = plyr.color
                else:
                    clr = DniSelectableColor
                playerlist.addStringWithColor(plyr.text, clr, kSelectUseGUIColor)
            elif (type(plyr) == type('')):
                playerlist.closeBranch()
                playerlist.addBranch(plyr, 1)
            else:
                PtDebugPrint('xBigKI: unknown list type ', plyr, level=kErrorLevel)
            if (type(PreviouslySelectedPlayer) != type(None)):
                PtDebugPrint('xKI: a previously selected player', PreviouslySelectedPlayer, level=kDebugDumpLevel)
                if (PreviouslySelectedPlayer.__class__ == plyr.__class__):
                    PtDebugPrint('xKI: Match class - previous player matches class', level=kDebugDumpLevel)
                    if (PreviouslySelectedPlayer == plyr):
                        PtDebugPrint(('xKI: Match object - previous player matches object, setting to %d' % idx), level=kDebugDumpLevel)
                        newselection = idx
                        PreviouslySelectedPlayer = None
                    else:
                        PtDebugPrint('xKI: Not Match object - previous does not match object', level=kDebugDumpLevel)
                else:
                    PtDebugPrint('xKI: Not Match class - previous does not match class', level=kDebugDumpLevel)
            idx += 1

        playerlist.setScrollPos(scrollPos)
        playerlist.unlock()
        if (newselection == -1):
            newselection = 0
            caret = ptGUIControlTextBox(KIMini.dialog.getControlFromTag(kChatCaretID))
            caret.setString('>')
        PtDebugPrint(('xKI:mini: setting new selection to %d' % newselection), level=kDebugDumpLevel)
        playerlist.setSelection(newselection)
        PreviouslySelectedPlayer = None
        self.ICheckScrollButtons(playerlist, kminiPlayerListUp, kminiPlayerListDown)
        sendToButton = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKIToPlayerButton))
        if (type(BKPlayerSelected) == type(None)):
            sendToButton.hide()
        elif isinstance(BKPlayerSelected, DeviceFolder):
            BKPlayerSelected = None
            sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
            sendToField.setString('  ')
            sendToButton.hide()
        elif isinstance(BKPlayerSelected, Device):
            try:
                FolderOfDevices.index(BKPlayerSelected)
            except ValueError:
                BKPlayerSelected = None
                sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
                sendToField.setString('  ')
                sendToButton.hide()


    def IRefreshMiniKIMarkerDisplay(self):
        print ('xKI:GZ: Refreshing MarkerDisplay  %d:%d' % (gMarkerGottenNumber, gMarkerToGetNumber))
        if ((theKILevel > kMicroKI) and (not PtIsSinglePlayerMode())):
            if ((gMarkerGottenNumber == gMarkerToGetNumber) and ((gMarkerToGetNumber % 25) == 0)):
                xMyMaxMarkers = gMarkerToGetNumber
                xMyGotMarkers = gMarkerGottenNumber
            else:
                xMyGotMarkers = (gMarkerGottenNumber % 25)
                if (gMarkerGottenNumber >= (math.floor((gMarkerToGetNumber / 25)) * 25)):
                    xMyMaxMarkers = (gMarkerToGetNumber % 25)
                else:
                    xMyMaxMarkers = 25
            for mcbid in range(kminiMarkerIndicator01, (kminiMarkerIndicatorLast + 1)):
                mcb = ptGUIControlProgress(KIMini.dialog.getControlFromTag(mcbid))
                markerNumber = ((mcbid - kminiMarkerIndicator01) + 1)
                try:
                    if ((not gKIMarkerLevel) or (markerNumber > xMyMaxMarkers)):
                        mcb.setValue(gMarkerColors['off'])
                    elif ((markerNumber <= xMyMaxMarkers) and (markerNumber > xMyGotMarkers)):
                        mcb.setValue(gMarkerColors[gMarkerToGetColor])
                    else:
                        mcb.setValue(gMarkerColors[gMarkerGottenColor])
                except LookupError:
                    print "xKI:GZ - coundn't find color - defaulting to off"
                    mcb.setValue(gMarkerColors['off'])

            btnmtDrip = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiGZDrip))
            btnmtActive = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiGZActive))
            btnmtPlaying = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiGZMarkerGameActive))
            btnmtInRange = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiGZMarkerInRange))
# MOUL marker Buttons
            btnmtNew = ptGUIControlButton(KIMini.dialog.getControlFromTag(kminiMGNewGame))
            btnmtNew.hide()
            btnmtNew.disable()
#/MOUL marker Buttons
            if gKIMarkerLevel:
                btnmtDrip.hide()
                if (gMarkerToGetNumber > gMarkerGottenNumber):
                    if gGZMarkerInRange:
                        btnmtInRange.show()
##############################################################################
# Changes for PotS markers
##############################################################################
                        if not xxConfig.CollectMarkersUU: btnmtInRange.disable() # add to enforce TPOTS way
##############################################################################
# End changes for PotS markers
##############################################################################
                        btnmtPlaying.hide()
                        btnmtActive.hide()
                    else:
                        btnmtInRange.hide()
                        btnmtPlaying.show()
                        btnmtActive.hide()
                else:
                    btnmtPlaying.hide()
                    btnmtInRange.hide()
#MOUL marker Buttons
                    if PhasedKICreateMarkerGame and (gKIMarkerLevel >= kKIMarkerNormalLevel):
                        btnmtActive.hide()
                        btnmtNew.show()
                        btnmtNew.enable()
                    else:
                        btnmtActive.show()
#/MOUL marker Buttons
            else:
                btnmtDrip.hide()
                btnmtActive.hide()
                btnmtPlaying.hide()
                btnmtInRange.hide()



    def IRefreshKISettings(self):
        global TicksOnFull
        fontSizeSlider = ptGUIControlKnob(KISettings.dialog.getControlFromTag(kBKIKIFontSize))
        fontSize = self.IGetFontSize()
        whichFont = 0
        for fs in FontSizeList:
            if (fontSize <= fs):
                break
            whichFont += 1

        if (whichFont >= len(FontSizeList)):
            whichFont = (len(FontSizeList) - 1)
        slidePerFont = (float(((fontSizeSlider.getMax() - fontSizeSlider.getMin()) + 1.0)) / float(len(FontSizeList)))
        FSslider = int(((slidePerFont * whichFont) + 0.25))
        fontSizeSlider.setValue(FSslider)
        fadeTimeSlider = ptGUIControlKnob(KISettings.dialog.getControlFromTag(kBKIKIFadeTime))
        slidePerTime = (float((fadeTimeSlider.getMax() - fadeTimeSlider.getMin())) / float(kFadeTimeMax))
        if (not FadeEnableFlag):
            TicksOnFull = kFadeTimeMax
        FTslider = (slidePerTime * TicksOnFull)
        fadeTimeSlider.setValue(FTslider)
        onlyPMCheckbox = ptGUIControlCheckBox(KISettings.dialog.getControlFromTag(kBKIKIOnlyPM))
        onlyPMCheckbox.setChecked(OnlyGetPMsFromBuddies)



    def IRefreshVolumeSettings(self):
        audio = ptAudioControl()
        soundFX = ptGUIControlValue(KIVolumeExpanded.dialog.getControlFromTag(kBKISoundFXVolSlider))
        setting = audio.getSoundFXVolume()
        soundFX.setValue((setting * 10))
        music = ptGUIControlValue(KIVolumeExpanded.dialog.getControlFromTag(xBKIMusicVolSlider))
        setting = audio.getMusicVolume()
        music.setValue((setting * 10))
        voice = ptGUIControlValue(KIVolumeExpanded.dialog.getControlFromTag(xBKIVoiceVolSlider))
        setting = audio.getVoiceVolume()
        voice.setValue((setting * 10))
        ambience = ptGUIControlValue(KIVolumeExpanded.dialog.getControlFromTag(kBKIAmbienceVolSlider))
        setting = audio.getAmbienceVolume()
        ambience.setValue((setting * 10))
        miclevel = ptGUIControlValue(KIVolumeExpanded.dialog.getControlFromTag(kBKIMicLevelSlider))
        setting = audio.getMicLevel()
        miclevel.setValue((setting * 10))
        guivolume = ptGUIControlValue(KIVolumeExpanded.dialog.getControlFromTag(kBKIGUIVolSlider))
        setting = audio.getGUIVolume()
        guivolume.setValue((setting * 10))



    def IRefreshAgeOwnerSettings(self):
        if (BigKI.dialog.isEnabled() and (BKRightSideMode == kBKAgeOwnerExpanded)):
            try:
                myAge = BKConfigFolderDict[BKConfigListOrder[BKFolderSelected]]
            except LookupError:
                myAge = None
            if (type(myAge) != type(None)):
                czar = myAge.getCzar()
                title = ptGUIControlTextBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleTB))
                title.setString(self.IGetAgeDisplayName(myAge))
                titlebtn = ptGUIControlButton(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleBtn))
                titlebtn.enable()
                titleedit = ptGUIControlEditBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleEditbox))
                titleedit.hide()
                status = ptGUIControlTextBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerStatusTB))
                visitors = myAge.getCanVisitFolder()
                owners = myAge.getAgeOwnersFolder()
                numvisitors = visitors.getChildNodeCount()
                numowners = owners.getChildNodeCount()
                vsess = 's'
                if (numvisitors == 1):
                    vsess = ''
                osess = 's'
                if (numowners == 1):
                    osess = ''
                makepublicTB = ptGUIControlTextBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerMakePublicTB))
                makepublicBtn = ptGUIControlButton(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerMakePublicBtn))
                makepublicBtn.disable()
                makepublicTB.hide()
                makepublicTB.setString(' ')
                status.setString((xLocalization.xKI.xAgeOwnedStatusLine % (numowners,
                    osess,
                    numvisitors,
                    vsess)))
                descript = ptGUIControlMultiLineEdit(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerDescription))
                encoded = buffer(myAge.getAgeDescription())
                descript.setEncodedBuffer(encoded)



    def IminiToggleKISize(self):
        global WaitingForAnimation
        global LastminiKICenter
        if ((theKILevel > kMicroKI) and (not IKIDisabled)):
            if (not WaitingForAnimation):
                toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
                if BigKI.dialog.isEnabled():
                    self.IBigKIHideBigKI()
                    self.IEnterChatMode(0)
                    KIBlackbar.dialog.show()
                    if (type(LastminiKICenter) != type(None)):
                        dragbar = ptGUIControlDragBar(KIMini.dialog.getControlFromTag(kminiDragBar))
                        dragbar.setObjectCenter(LastminiKICenter)
                        dragbar.unanchor()
                        LastminiKICenter = None
                    self.IRefreshPlayerList(forceSmall=1)
                    self.IRefreshPlayerListDisplay()
                    toggleCB.setChecked(0)
                elif (not KIMini.dialog.isEnabled()):
                    self.IClearBBMini(0)
                else:
                    WaitingForAnimation = 1
                    KIBlackbar.dialog.hide()
                    KIMini.dialog.hide()
                    self.IEnterChatMode(0)
                    BigKI.dialog.show()
                    if (type(OriginalminiKICenter) != type(None)):
                        dragbar = ptGUIControlDragBar(KIMini.dialog.getControlFromTag(kminiDragBar))
                        LastminiKICenter = dragbar.getObjectCenter()
                        PtDebugPrint(('xKI:distance to original = %f' % LastminiKICenter.distance(OriginalminiKICenter)), level=kDebugDumpLevel)
                        if (LastminiKICenter.distance(OriginalminiKICenter) < 0.027):
                            LastminiKICenter = OriginalminiKICenter
                        dragbar.setObjectCenter(OriginalminiKICenter)
                        dragbar.anchor()
                    KIMini.dialog.show()
                    toggleCB.setChecked(1)



    def IminiPutAwayKI(self):
        global ISawTheKIAtleastOnce
        global LastminiKICenter
        if ((theKILevel > kMicroKI) and (not IKIDisabled)):
            if KIMini.dialog.isEnabled():
                KIMini.dialog.hide()
                if (type(LastminiKICenter) != type(None)):
                    dragbar = ptGUIControlDragBar(KIMini.dialog.getControlFromTag(kminiDragBar))
                    dragbar.setObjectCenter(LastminiKICenter)
                    dragbar.unanchor()
                    LastminiKICenter = None
                if BigKI.dialog.isEnabled():
                    self.IBigKIHideBigKI()
                KIBlackbar.dialog.show()
                self.IClearBBMini(-1)
                toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
                toggleCB.setChecked(0)
                ISawTheKIAtleastOnce = 1
            else:
                self.IClearBBMini(0)



    def IminiTakePicture(self):
        global WeAreTakingAPicture
        global YNWhatReason
        if PhasedKICreateImages:
            if ((not WeAreTakingAPicture) and (not WaitingForAnimation)):
                if ((theKILevel > kMicroKI) and (not IKIDisabled)):
                    if self.ICanTakePicture():
                        WeAreTakingAPicture = 1
                        KIBlackbar.dialog.hide()
                        KIMini.dialog.hide()
                        self.IBigKIHideMode()
                        BigKI.dialog.hide()
                        toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
                        toggleCB.setChecked(1)
                        PtAtTimeCallback(self.key, 0.25, kTakeSnapShot)
                    else:
                        YNWhatReason = kYNKIFull
                        reasonField = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                        reasonField.setString(xLocalization.xKI.xKIFullImagesError)
                        noButton = ptGUIControlButton(KIYesNo.dialog.getControlFromTag(kNoButtonID))
                        noButton.hide()
                        noBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
                        noBtnText.hide()
                        yesBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
                        yesBtnText.setString(xLocalization.xKI.xYesNoOKbutton)
                        KIYesNo.dialog.show()



    def IminiCreateJournal(self):
        global LastminiKICenter
        global BKRightSideMode
        global YNWhatReason
        if PhasedKICreateNotes:
            if ((not WeAreTakingAPicture) and (not WaitingForAnimation)):
                if ((theKILevel > kMicroKI) and (not IKIDisabled)):
                    if self.ICanMakeNote():
                        KIBlackbar.dialog.hide()
                        toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
                        toggleCB.setChecked(1)
                        self.IBigKICreateJournalNote()
                        modeselector = ptGUIControlRadioGroup(BigKI.dialog.getControlFromTag(kBKRadioModeID))
                        modeselector.setValue(0)
                        if (BKRightSideMode != kBKJournalExpanded):
                            self.IBigKIHideMode()
                        BKRightSideMode = kBKJournalExpanded
                        self.IBigKIRefreshFolderDisplay()
                        self.IBigKIEnterEditMode(kBKEditFieldJRNTitle)
                        if BigKI.dialog.isEnabled():
                            self.IBigKIShowMode()
                        else:
                            KIMini.dialog.hide()
                            BigKI.dialog.show()
                            KIMini.dialog.show()
                        if (type(LastminiKICenter) == type(None)):
                            if (type(OriginalminiKICenter) != type(None)):
                                dragbar = ptGUIControlDragBar(KIMini.dialog.getControlFromTag(kminiDragBar))
                                LastminiKICenter = dragbar.getObjectCenter()
                                dragbar.setObjectCenter(OriginalminiKICenter)
                                dragbar.anchor()
                    else:
                        YNWhatReason = kYNKIFull
                        reasonField = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesNoTextID))
                        reasonField.setString(xLocalization.xKI.xKIFullNotesError)
                        noButton = ptGUIControlButton(KIYesNo.dialog.getControlFromTag(kNoButtonID))
                        noButton.hide()
                        noBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kNoButtonTextID))
                        noBtnText.hide()
                        yesBtnText = ptGUIControlTextBox(KIYesNo.dialog.getControlFromTag(kYesButtonTextID))
                        yesBtnText.setString(xLocalization.xKI.xYesNoOKbutton)
                        KIYesNo.dialog.show()



    def ICaptureGZMarker(self):
        global gGZMarkerInRange
        global gGZMarkerInRangeRepy
        global gMarkerGottenNumber
        if (gGZPlaying and (gMarkerToGetNumber > gMarkerGottenNumber)):
##############################################################################
# Changes for PotS markers
##############################################################################
#            vault = ptVault()
#            entry = vault.findChronicleEntry(kChronicleGZMarkersAquired)
#            if (type(entry) != type(None)):
#                markers = entry.chronicleGetValue()
#                markerIdx = (gGZMarkerInRange - 1)
#                if ((markerIdx >= 0) and (markerIdx < len(markers))):
#                    print ("starting with '%s' changing %d to '%s'" % (markers,
#                     gGZMarkerInRange,
#                     kGZMarkerCaptured))
#                    if ((len(markers) - (markerIdx + 1)) != 0):
#                        markers = ((markers[:markerIdx] + kGZMarkerCaptured) + markers[-(len(markers) - (markerIdx + 1)):])
#                    else:
#                        markers = (markers[:markerIdx] + kGZMarkerCaptured)
#                    print ("out string is '%s'" % markers)
#                    entry.chronicleSetValue(markers)
#                    entry.save()
#                    totalGotten = markers.count(kGZMarkerCaptured)
#                    if (gKIMarkerLevel > kKIMarkerFirstLevel):
#                        totalGotten -= 15
#                        if (totalGotten < 0):
#                            totalGotten = 0
#                    if (totalGotten > gMarkerToGetNumber):
#                        totalGotten = gMarkerToGetNumber
#                    gMarkerGottenNumber = totalGotten
#                    self.IUpdateGZGamesChonicles()
#                else:
#                    PtDebugPrint(('xminiKI:CaptureGZMarker: invalid marker serial number of %d' % gGZMarkerInRange))
#                    return
#            else:
#                PtDebugPrint('xminiKI:CaptureGZMarker: no chronicle entry found')
#                return
##############################################################################
# End changes for PotS markers
##############################################################################
            if (type(gGZMarkerInRangeRepy) != type(None)):
                note = ptNotify(self.key)
                note.clearReceivers()
                note.addReceiver(gGZMarkerInRangeRepy)
                note.netPropagate(0)
                note.netForce(0)
                note.setActivate(1)
                note.addVarNumber('Captured', 1)
                note.send()
            gGZMarkerInRangeRepy = None
            gGZMarkerInRange = 0



    def IBigKIShowBigKI(self):
        global WaitingForAnimation
        global IsPlayingLookingAtKIMode
        WaitingForAnimation = 1
        curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
        toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
        toggleCB.disable()
        if ((curBrainMode == PtBrainModes.kNonGeneric) or ((curBrainMode == PtBrainModes.kAFK) or (curBrainMode == PtBrainModes.kSit))):
            PtDebugPrint('xKI:ShowKI enter LookingAtKI mode', level=kDebugDumpLevel)
            PtAvatarEnterLookingAtKI()
            IsPlayingLookingAtKIMode = 1
        PtDisableMovementKeys()
        KIOnResp.run(self.key, netPropagate=0)



    def IBigKIHideBigKI(self):
        global WaitingForAnimation
        global IsPlayingLookingAtKIMode
        WaitingForAnimation = 1
        toggleCB = ptGUIControlCheckBox(KIMini.dialog.getControlFromTag(kminiToggleBtnID))
        toggleCB.disable()
        self.IBigKIHideMode()
        if IsPlayingLookingAtKIMode:
            curBrainMode = PtGetLocalAvatar().avatar.getCurrentMode()
            if (curBrainMode != PtBrainModes.kSit):
                PtDebugPrint('xKI:HideKI exit LookingAtKI mode', level=kDebugDumpLevel)
                PtAvatarExitLookingAtKI()
        IsPlayingLookingAtKIMode = 0
        PtEnableMovementKeys()
        KIOffResp.run(self.key, netPropagate=0)



    def IBigKIShowMode(self):
        global BKGettingPlayerID
        global BKCurrentContent
        if BigKI.dialog.isEnabled():
            self.IResetListModeArrows()
            if (BKRightSideMode == kBKListMode):
                KIListModeDialog.dialog.show()
                self.IBigKIOnlySelectedToButtons()
                BKCurrentContent = None
                BKGettingPlayerID = 0
            elif (BKRightSideMode == kBKJournalExpanded):
                KIJournalExpanded.dialog.show()
                if self.IsContentMutable(BKCurrentContent):
                    self.IBigKIInvertToFolderButtons()
                else:
                    self.IBigKIOnlySelectedToButtons()
                BKGettingPlayerID = 0
            elif (BKRightSideMode == kBKPictureExpanded):
                KIPictureExpanded.dialog.show()
                if self.IsContentMutable(BKCurrentContent):
                    self.IBigKIInvertToFolderButtons()
                else:
                    self.IBigKIOnlySelectedToButtons()
                BKGettingPlayerID = 0
            elif (BKRightSideMode == kBKPlayerExpanded):
                KIPlayerExpanded.dialog.show()
                localplayer = PtGetLocalPlayer()
                if (type(BKCurrentContent) != type(None)):
                    if isinstance(BKCurrentContent, ptPlayer):
                        if (BKCurrentContent.getPlayerID() == localplayer.getPlayerID()):
                            self.IBigKIOnlySelectedToButtons()
                            return
                    else:
                        elem = BKCurrentContent.getChild()
                        if (elem.getType() == PtVaultNodeTypes.kPlayerInfoNode):
                            elem = elem.upcastToPlayerInfoNode()
                            if (elem.playerGetID() == localplayer.getPlayerID()):
                                self.IBigKIOnlySelectedToButtons()
                                return
                self.IBigKIInvertToFolderButtons()
            elif (BKRightSideMode == kBKVolumeExpanded):
                KIVolumeExpanded.dialog.show()
                self.IBigKIOnlySelectedToButtons()
                BKCurrentContent = None
                BKGettingPlayerID = 0
            elif (BKRightSideMode == kBKKIExpanded):
                KISettings.dialog.show()
                self.IBigKIOnlySelectedToButtons()
                BKCurrentContent = None
                BKGettingPlayerID = 0
            elif (BKRightSideMode == kBKAgeOwnerExpanded):
                KIAgeOwnerExpanded.dialog.show()
                self.IBigKIOnlySelectedToButtons()
                BKCurrentContent = None
                BKGettingPlayerID = 0
            elif (BKRightSideMode == kBKMarkerListExpanded):
                KIMarkerFolderExpanded.dialog.show()
                if (PhasedKISendMarkerGame and self.IsContentMutable(BKCurrentContent)):
                    self.IBigKIInvertToFolderButtons()
                else:
                    self.IBigKIOnlySelectedToButtons()
                BKGettingPlayerID = 0
            elif (BKRightSideMode == kBKQuestionNote):
                KIQuestionNote.dialog.show()
                self.IBigKIOnlySelectedToButtons()
                BKGettingPlayerID = 0



    def IBigKIHideMode(self):
        if (BKRightSideMode == kBKListMode):
            KIListModeDialog.dialog.hide()
        elif (BKRightSideMode == kBKJournalExpanded):
            KIJournalExpanded.dialog.hide()
        elif (BKRightSideMode == kBKPictureExpanded):
            KIPictureExpanded.dialog.hide()
        elif (BKRightSideMode == kBKPlayerExpanded):
            KIPlayerExpanded.dialog.hide()
        elif (BKRightSideMode == kBKVolumeExpanded):
            KIVolumeExpanded.dialog.hide()
        elif (BKRightSideMode == kBKKIExpanded):
            KISettings.dialog.hide()
        elif (BKRightSideMode == kBKAgeOwnerExpanded):
            KIAgeOwnerExpanded.dialog.hide()
        elif (BKRightSideMode == kBKMarkerListExpanded):
            KIMarkerFolderExpanded.dialog.hide()
        elif (BKRightSideMode == kBKQuestionNote):
            KIQuestionNote.dialog.hide()



    def IBigKIChangeMode(self, newmode):
        global BKRightSideMode
        if (newmode != BKRightSideMode):
            self.IBigKIHideMode()
            BKRightSideMode = newmode
            self.IBigKIShowMode()
        elif (newmode == kBKListMode):
            self.IBigKIOnlySelectedToButtons()



    def IBigKISetToButtons(self):
        if (BKRightSideMode == kBKListMode):
            self.IBigKIOnlySelectedToButtons()
        elif (BKRightSideMode == kBKJournalExpanded):
            if self.IsContentMutable(BKCurrentContent):
                self.IBigKIInvertToFolderButtons()
            else:
                self.IBigKIOnlySelectedToButtons()
        elif (BKRightSideMode == kBKPictureExpanded):
            if self.IsContentMutable(BKCurrentContent):
                self.IBigKIInvertToFolderButtons()
            else:
                self.IBigKIOnlySelectedToButtons()
        elif (BKRightSideMode == kBKPlayerExpanded):
            localplayer = PtGetLocalPlayer()
            if (type(BKCurrentContent) != type(None)):
                if isinstance(BKCurrentContent, ptPlayer):
                    if (BKCurrentContent.getPlayerID() == localplayer.getPlayerID()):
                        self.IBigKIOnlySelectedToButtons()
                        return
                else:
                    elem = BKCurrentContent.getChild()
                    if (elem.getType() == PtVaultNodeTypes.kPlayerInfoNode):
                        elem = elem.upcastToPlayerInfoNode()
                        if (elem.playerGetID() == localplayer.getPlayerID()):
                            self.IBigKIOnlySelectedToButtons()
                            return
            self.IBigKIInvertToFolderButtons()
        elif (BKRightSideMode == kBKVolumeExpanded):
            self.IBigKIOnlySelectedToButtons()
        elif (BKRightSideMode == kBKKIExpanded):
            self.IBigKIOnlySelectedToButtons()
        elif (BKRightSideMode == kBKAgeOwnerExpanded):
            self.IBigKIOnlySelectedToButtons()
        elif (BKRightSideMode == kBKMarkerListExpanded):
            if (PhasedKISendMarkerGame and ((MFdialogMode != kMFPlaying) and self.IsContentMutable(BKCurrentContent))):
                self.IBigKIInvertToFolderButtons()
            else:
                self.IBigKIOnlySelectedToButtons()
        elif (BKRightSideMode == kBKQuestionNote):
            self.IBigKIOnlySelectedToButtons()



    def IBigKISetNotifyForLong(self):
        for id in range(kBKIIncomingBtn, kBKIFolderLineBtnLast):
            overBtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(id))
            overBtn.setNotifyOnInteresting(1)




    def IBigKIHideLongFolderNames(self):
        for id in range(kLONGBKIIncomingLine, (kLONGBKIFolderLineLast + 1)):
            longTB = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(id))
            longTB.hide()




    def IResetListModeArrows(self):
        upbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKLMUpButton))
        upbtn.hide()
        dwnbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKLMDownButton))
        dwnbtn.hide()



    def IBigKIOnlySelectedToButtons(self):
        toplayerbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKIToPlayerButton))
        toplayerbtn.hide()
        self.IBigKIRefreshFolderDisplay()
        for id in range(kBKIToIncomingButton, (kBKIToFolderButtonLast + 1)):
            tofolder = ptGUIControlButton(BigKI.dialog.getControlFromTag(id))
            tofolder.hide()

        self.IBigKINewContentList()



    def IBigKICanShowSendToPlayer(self):
        if (type(BKPlayerSelected) == type(None)):
            return false
        if ((BKRightSideMode == kBKPlayerExpanded) or ((BKRightSideMode == kBKVolumeExpanded) or (BKRightSideMode == kBKAgeOwnerExpanded))):
            return false
        if (BKRightSideMode == kBKJournalExpanded):
            if (not PhasedKISendNotes):
                return false
        if (BKRightSideMode == kBKPictureExpanded):
            if (not PhasedKISendImages):
                return false
        if isinstance(BKPlayerSelected, ptVaultNodeRef):
            plyrElement = BKPlayerSelected.getChild()
            if ((type(plyrElement) != type(None)) and (plyrElement.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
                plyrElement = plyrElement.upcastToPlayerInfoNode()
                if (plyrElement.playerGetID() == PtGetLocalClientID()):
                    return false
        return true



    def IBigKIInvertToFolderButtons(self):
        toplayerbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKIToPlayerButton))
        if self.IBigKICanShowSendToPlayer():
            toplayerbtn.show()
        else:
            toplayerbtn.hide()
        selectedButton = ((BKFolderSelected - BKFolderTopLine) + kBKIToIncomingButton)
        for id in range(kBKIToIncomingButton, (kBKIToFolderButtonLast + 1)):
            tofolder = ptGUIControlButton(BigKI.dialog.getControlFromTag(id))
            if (id == selectedButton):
                tofolder.hide()
            elif ((id - kBKIToIncomingButton) <= ((len(BKFolderListOrder) - 1) - BKFolderTopLine)):
                try:
                    if self.IsFolderContentsMutable(BKFolderLineDict[BKFolderListOrder[((id - kBKIToIncomingButton) + BKFolderTopLine)]]):
                        tofolder.show()
                    else:
                        tofolder.hide()
                except LookupError:
                    tofolder.hide()
            else:
                tofolder.hide()




    def IsFolderContentsMutable(self, folder):
        if ((type(folder) == type(None)) or (not isinstance(folder, ptVaultNode))):
            return 0
        if (folder.getType() == PtVaultNodeTypes.kAgeInfoNode):
            return 1
        if ((folder.getType() != PtVaultNodeTypes.kPlayerInfoListNode) and (folder.getType() != PtVaultNodeTypes.kFolderNode)):
            return 0
        if (folder.folderGetType() == PtVaultStandardNodes.kInboxFolder):
            return 0
        if (folder.folderGetType() == PtVaultStandardNodes.kAgeMembersFolder):
            return 0
        if (folder.folderGetType() == PtVaultStandardNodes.kHoodMembersFolder):
            return 0
        if (folder.folderGetType() == PtVaultStandardNodes.kAgeOwnersFolder):
            return 0
        return 1



    def IsFolderHidden(self, agefolder):
        if (agefolder.folderGetName() == 'Hidden'):
            return 1
        return 0



    def IsContentMutable(self, noderef):
        if isinstance(noderef, ptVaultNodeRef):
            folder = BKCurrentContent.getParent()
            if folder:
                folder = folder.upcastToFolderNode()
                if folder:
                    if (folder.folderGetType() == PtVaultStandardNodes.kGlobalInboxFolder):
                        return 0
        return 1



    def IBigKISetStatics(self):
        agetext = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKICurAgeNameID))
        ageName = self.IGetAgeDisplayName()
        PtDebugPrint(('xKI: displaying age name of %s' % ageName), level=kDebugDumpLevel)
        agetext.setString(ageName)
        playertext = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKPlayerName))
        idtext = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKPlayerID))
        localplayer = PtGetLocalPlayer()
        playertext.setString(localplayer.getPlayerName())
        if (not PtIsSinglePlayerMode()):
            idtext.setString(('[ID:%08d]' % localplayer.getPlayerID()))
        else:
            idtext.setString('  ')
        self.IBigKIRefreshHoodStatics()


    def IBigKIRefreshHoodStatics(self, neighborhood = None):
        neighbortext = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKNeighborhoodAndID))
        if (not PtIsSinglePlayerMode()):
            if (not neighborhood):
                neighborhood = self.IGetNeighborhood()
            if (type(neighborhood) != type(None)):
                neighborName = xLocalization.xGlobal.LocalizeAgeName(neighborhood.getDisplayName())
                if (neighborName == ''):
                    neighborName = xLocalization.xKI.xNeighborhoodNoName
                neighbortext.setString((xLocalization.xKI.xNeighborhoodBottomLine % (xLocalization.MemberStatusString(), neighborName)))
            else:
                neighbortext.setString(xLocalization.xKI.xNeighborhoodNone)
        else:
            neighbortext.setString('  ')


    def IBigKISetChanging(self):
        global PreviousTime
        global TimeBlinker
        dnitime = PtGetDniTime()
        if dnitime:
            tuptime = time.gmtime(dnitime)
            if TimeBlinker:
                curtime = time.strftime(xLocalization.xGlobal.xDateTimeFormat, tuptime)
                TimeBlinker = 0
            else:
                curtime = time.strftime(xLocalization.xGlobal.xDateTimeFormat, tuptime)
                TimeBlinker = 1
        else:
            curtime = xLocalization.xKI.xKITimeBroke
        if (curtime != PreviousTime):
            timetext = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKICurTimeID))
            timetext.setString(curtime)
            PreviousTime = curtime
        gps1 = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIGPS1TextID))
        gps2 = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIGPS2TextID))
        gps3 = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIGPS3TextID))
        self.dnicoords.update()
##############################################################################
# D'Lanor's Alcugs GPS fix
##############################################################################
#        if (gKIMarkerLevel == kKIMarkerNormalLevel):
#            sdl = xPsnlVaultSDL()
#            if sdl['GPSEnabled'][0]:
#                gps1.setString(('%d' % self.dnicoords.getTorans()))
#                gps2.setString(('%d' % self.dnicoords.getHSpans()))
#                gps3.setString(('%d' % self.dnicoords.getVSpans()))
#            else:
#                gps1.setString(('%d' % 0))
#                gps2.setString(('%d' % 0))
#                gps3.setString(('%d' % 0))
#        else:
#            gps1.setString(('%d' % 0))
#            gps2.setString(('%d' % 0))
#            gps3.setString(('%d' % 0))
#        PtAtTimeCallback(self.key, 5, kBKITODCheck)
        if (gShowGPSCheat != 1):
            if (gKIMarkerLevel == kKIMarkerNormalLevel):
                if (PtGetCGZGameState(kCGZToransGame) == kCGZMarkerUploaded):
                    gps1.setString(('%d' % self.dnicoords.getTorans()))
                else:
                    gps1.setString(('%d' % 0))
                if (PtGetCGZGameState(kCGZHSpansGame) == kCGZMarkerUploaded):
                    gps2.setString(('%d' % self.dnicoords.getHSpans()))
                else:
                    gps2.setString(('%d' % 0))
                if (PtGetCGZGameState(kCGZVSpansGame) == kCGZMarkerUploaded):
                    gps3.setString(('%d' % self.dnicoords.getVSpans()))
                else:
                    gps3.setString(('%d' % 0))
            else:
                gps1.setString(('%d' % 0))
                gps2.setString(('%d' % 0))
                gps3.setString(('%d' % 0))
        else:
            gps1.setString(('%d' % self.dnicoords.getTorans()))
            gps2.setString(('%d' % self.dnicoords.getHSpans()))
            gps3.setString(('%d' % self.dnicoords.getVSpans()))
        PtAtTimeCallback(self.key, 1, kBKITODCheck) 
##############################################################################
# End D'Lanor's Alcugs GPS fix
##############################################################################



    def IBKCheckFolderRefresh(self, folder = None, content = None):
        if (type(folder) != type(None)):
            if (folder.getType() == PtVaultNodeTypes.kPlayerInfoListNode):
                self.IRefreshPlayerList()
                self.IRefreshPlayerListDisplay()
        else:
            self.IRefreshPlayerList()
            self.IRefreshPlayerListDisplay()
        if (theKILevel > kMicroKI):
            self.IBigKIRefreshContentList()
            self.IBigKIRefreshContentListDisplay()



    def IBKCheckContentRefresh(self, content):
        if ((type(BKCurrentContent) != type(None)) and (content == BKCurrentContent)):
            if (BKRightSideMode == kBKListMode):
                self.IBigKIRefreshContentListDisplay()
            elif (BKRightSideMode == kBKJournalExpanded):
                self.IBigKIDisplayCurrentContentJournal()
            elif (BKRightSideMode == kBKPictureExpanded):
                self.IBigKIDisplayCurrentContentImage()
            elif (BKRightSideMode == kBKPlayerExpanded):
                self.IBigKIDisplayCurrentContentPlayer()
            elif (BKRightSideMode == kBKMarkerListExpanded):
                self.IBigKIDisplayCurrentContentMarkerFolder()



    def IBKCheckElementRefresh(self, element):
        if (type(BKCurrentContent) != type(None)):
            if (isinstance(BKCurrentContent, ptVaultNodeRef) and (element == BKCurrentContent.getChild())):
                if (BKRightSideMode == kBKListMode):
                    self.IBigKIRefreshContentListDisplay()
                elif (BKRightSideMode == kBKJournalExpanded):
                    self.IBigKIDisplayCurrentContentJournal()
                elif (BKRightSideMode == kBKPictureExpanded):
                    self.IBigKIDisplayCurrentContentImage()
                elif (BKRightSideMode == kBKPlayerExpanded):
                    self.IBigKIDisplayCurrentContentPlayer()
                elif (BKRightSideMode == kBKMarkerListExpanded):
                    self.IBigKIDisplayCurrentContentMarkerFolder()



    def IRemoveIgnoredPlayers(self, playerlist):
        nonIgnoredlist = []
        ignores = ptVault().getIgnoreListFolder()
        for plyr in playerlist:
            if isinstance(plyr, ptVaultNodeRef):
                PLR = plyr.getChild()
                PLR = PLR.upcastToPlayerInfoNode()
                if ((type(PLR) != type(None)) and (PLR.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
                    if (not ignores.playerlistHasPlayer(PLR.playerGetID())):
                        nonIgnored.append(plyr)

        return nonIgnored



    def IBigKIRefreshFolders(self):
        vault = ptVault()
        ageVault = ptAgeVault()
        if (not BKJournalFolderDict.has_key(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kInboxFolder))):
            infolder = vault.getInbox()
            if (type(infolder) != type(None)):
                BKJournalListOrder.insert(0, xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kInboxFolder))
                BKJournalFolderDict[xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kInboxFolder)] = infolder
        master_agefolder = vault.getAgeJournalsFolder()
        if (type(master_agefolder) != type(None)):
            agefolderRefs = master_agefolder.getChildNodeRefList()
            for agefolderRef in agefolderRefs:
                agefolder = agefolderRef.getChild()
                agefolder = agefolder.upcastToFolderNode()
                if (type(agefolder) != type(None)):
                    if (not self.IsFolderHidden(agefolder)):
                        agefoldername = agefolder.folderGetName()
                        if (agefoldername == ''):
                            agefoldername = '[invalid]'
                        agefoldername = self.IFilterAgeName(agefoldername)
                        if (not BKJournalFolderDict.has_key(agefoldername)):
                            BKJournalListOrder.append(agefoldername)
                        BKJournalFolderDict[agefoldername] = agefolder

            try:
                line = BKJournalListOrder.index(self.IGetAgeInstanceName())
                if (line != 1):
                    BKJournalListOrder.remove(self.IGetAgeInstanceName())
                    BKJournalListOrder.insert(1, self.IGetAgeInstanceName())
                    if ((BKRightSideMode == kBKJournalExpanded) or ((BKRightSideMode == kBKPictureExpanded) or (BKRightSideMode == kBKMarkerListExpanded))):
                        self.IBigKIChangeMode(kBKListMode)
            except ValueError:
                if ((self.IGetAgeFileName() != 'AvatarCustomization') and ((self.IGetAgeInstanceName() != 'UNKNOWN AGE') and (self.IGetAgeInstanceName() != '?UNKNOWN?'))):
                    vault = ptVault()
                    entry = vault.findChronicleEntry('CleftSolved')
                    cleftSolved = 0
                    if (type(entry) != type(None)):
                        if (entry.chronicleGetValue() == 'yes'):
                            cleftSolved = 1
                    if ((self.IGetAgeInstanceName() != "D'ni-Riltagamin") or cleftSolved):
                        instAgeName = self.IGetAgeInstanceName()
                        if (instAgeName and (len(instAgeName) > 0)):
                            nfolder = ptVaultFolderNode(PtVaultNodePermissionFlags.kDefaultPermissions)
                            if (type(nfolder) != type(None)):
                                nfolder.folderSetName(self.IGetAgeInstanceName())
                                nfolder.folderSetType(PtVaultStandardNodes.kAgeTypeJournalFolder)
                                master_agefolder.addNode(nfolder)
                            else:
                                PtDebugPrint(('xKI: could not create folder for %s' % self.IGetAgeInstanceName()), level=kErrorLevel)
        else:
            PtDebugPrint('xKI: could not find the master Age jounal folder', level=kErrorLevel)
        BKPlayerFolderDict.clear()
        del BKPlayerListOrder[:]
        agemembers = kiFolder(PtVaultStandardNodes.kAgeMembersFolder)
        if (type(agemembers) != type(None)):
            if (not BKPlayerFolderDict.has_key(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kAgeMembersFolder))):
                BKPlayerListOrder.append(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kAgeMembersFolder))
            BKPlayerFolderDict[xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kAgeMembersFolder)] = agemembers
            PtDebugPrint('xBigKI: updating agemembers ', level=kDebugDumpLevel)
        else:
            PtDebugPrint('xBigKI: AgeMembers folder is missing!', level=kWarningLevel)
        if PhasedKIBuddies:
            buddies = vault.getBuddyListFolder()
            if (type(buddies) != type(None)):
                if (not BKPlayerFolderDict.has_key(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kBuddyListFolder))):
                    BKPlayerListOrder.append(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kBuddyListFolder))
                BKPlayerFolderDict[xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kBuddyListFolder)] = buddies
            else:
                PtDebugPrint('xBigKI: Buddies folder is missing!', level=kWarningLevel)
        if PhasedKINeighborsInDPL:
            self.IBigKIRefreshNeighborFolders()
        PIKA = vault.getPeopleIKnowAboutFolder()
        if (type(PIKA) != type(None)):
            if (not BKPlayerFolderDict.has_key(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kPeopleIKnowAboutFolder))):
                BKPlayerListOrder.append(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kPeopleIKnowAboutFolder))
            BKPlayerFolderDict[xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kPeopleIKnowAboutFolder)] = PIKA
        else:
            PtDebugPrint('xBigKI: PeopleIKnowAbout folder is missing!', level=kWarningLevel)
        ignores = vault.getIgnoreListFolder()
        if (type(ignores) != type(None)):
            if (not BKPlayerFolderDict.has_key(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kIgnoreListFolder))):
                BKPlayerListOrder.append(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kIgnoreListFolder))
            BKPlayerFolderDict[xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kIgnoreListFolder)] = ignores
        else:
            PtDebugPrint("xBigKI: People I'm ignoring folder is missing!")
        visSep = SeparatorFolder(xLocalization.xKI.xFolderVisLists)
        BKPlayerListOrder.append(visSep.name)
        BKPlayerFolderDict[visSep.name] = visSep
        self.IBigKIRefreshAgeVisitorFolders()
        self.IBigKIRefreshAgesOwnedFolder()



    def IBigKIRefreshNeighborFolders(self):
        neighborhood = self.IGetNeighborhood()
        try:
            neighbors = neighborhood.getAgeOwnersFolder()
            if (not BKPlayerFolderDict.has_key(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kHoodMembersFolder))):
                BKPlayerListOrder.append(xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kHoodMembersFolder))
            PtDebugPrint('xKI: got the neighbors player folder', level=kDebugDumpLevel)
            BKPlayerFolderDict[xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kHoodMembersFolder)] = neighbors
        except AttributeError:
            PtDebugPrint('xBigKI: Neighborhood is missing!', level=kWarningLevel)



    def IBigKIRefreshAgeVisitorFolders(self):
        vault = ptVault()
        try:
            myAgesFolder = vault.getAgesIOwnFolder()
            listOfMyAgeLinks = myAgesFolder.getChildNodeRefList()
            for myAgeLinkRef in listOfMyAgeLinks:
                myAgeLink = myAgeLinkRef.getChild()
                myAgeLink = myAgeLink.upcastToAgeLinkNode()
                myAge = myAgeLink.getAgeInfo()
                if (type(myAge) != type(None)):
                    if self.ICanAgeInviteVistors(myAge, myAgeLink):
                        PtDebugPrint(('xKI: refreshing visitor list for %s' % self.IGetAgeDisplayName(myAge)), level=kDebugDumpLevel)
                        foldername = xCensor.xCensor((xLocalization.xKI.xOwnerVistors % self.IGetAgeDisplayName(myAge)), theCensorLevel)
                        if (not BKPlayerFolderDict.has_key(foldername)):
                            PtDebugPrint(('xKI: adding visitor list for %s' % self.IGetAgeDisplayName(myAge)), level=kDebugDumpLevel)
                            BKPlayerListOrder.append(foldername)
                        BKPlayerFolderDict[foldername] = myAge
                else:
                    PtDebugPrint(('xKI: age info for %s is not ready yet' % myAgeLink.getUserDefinedName()), level=kErrorLevel)

        except AttributeError:
            PtDebugPrint('xKI: error finding age visitors folder', level=kErrorLevel)



    def IBigKIRefreshAgesOwnedFolder(self):
        BKConfigFolderDict.clear()
        del BKConfigListOrder[:]
        for config in BKConfigDefaultListOrder:
            BKConfigListOrder.append(config)

        vault = ptVault()
        try:
            myAgesFolder = vault.getAgesIOwnFolder()
            listOfMyAgeLinks = myAgesFolder.getChildNodeRefList()
            for myAgeLinkRef in listOfMyAgeLinks:
                myAgeLink = myAgeLinkRef.getChild()
                myAgeLink = myAgeLink.upcastToAgeLinkNode()
                myAge = myAgeLink.getAgeInfo()
                if (type(myAge) != type(None)):
                    if self.ICanConfigAge(myAge):
                        PtDebugPrint(('xKI: refreshing owner config for Age %s' % self.IGetAgeDisplayName(myAge)), level=kDebugDumpLevel)
                        configname = xCensor.xCensor((xLocalization.xKI.xOwnerConfiguration % self.IGetAgeDisplayName(myAge)), theCensorLevel)
                        if (not BKConfigFolderDict.has_key(configname)):
                            PtDebugPrint(('xKI: adding owner config for Age %s' % self.IGetAgeDisplayName(myAge)), level=kDebugDumpLevel)
                            BKConfigListOrder.append(configname)
                        BKConfigFolderDict[configname] = myAge
                else:
                    PtDebugPrint(('xKI:(AgeOwnerRefresh) age info for %s is not ready yet' % myAgeLink.getUserDefinedName()), level=kErrorLevel)

        except AttributeError:
            PtDebugPrint('xKI:(AgeOwnerRefresh) error finding age folder', level=kErrorLevel)



    def IBigKIRefreshFolderDisplay(self):
        global BKFolderSelected
        global BKFolderTopLine
        id = kBKIIncomingLine
        if (len(BKFolderListOrder) != 0):
            if (BKFolderTopLine >= len(BKFolderListOrder)):
                BKFolderTopLine = (len(BKFolderListOrder) - 1)
            if (BKRightSideMode == kBKListMode):
                if (BKFolderSelected < BKFolderTopLine):
                    BKFolderSelected = BKFolderTopLine
                if (BKFolderSelected > (BKFolderTopLine + (kBKIFolderLineLast - kBKIIncomingLine))):
                    BKFolderSelected = (BKFolderTopLine + (kBKIFolderLineLast - kBKIIncomingLine))
                if (BKFolderSelected > ((BKFolderTopLine + len(BKFolderListOrder[BKFolderTopLine:])) - 1)):
                    BKFolderSelected = ((BKFolderTopLine + len(BKFolderListOrder[BKFolderTopLine])) - 1)
            selectedFolder = ((BKFolderSelected - BKFolderTopLine) + kBKIIncomingLine)
            for foldername in BKFolderListOrder[BKFolderTopLine:]:
                folderfield = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(id))
                LONGfolderfield = ptGUIControlTextBox(BigKI.dialog.getControlFromTag((id + 500)))
                buttonid = ((id - kBKIFolderLine01) + kBKIFolderLineBtn01)
                folderbutton = ptGUIControlButton(BigKI.dialog.getControlFromTag(buttonid))
                if ((foldername in BKFolderLineDict) and isinstance(BKFolderLineDict[foldername], SeparatorFolder)):
                    folderbutton.hide()
                    folderfield.setStringJustify(kLeftJustify)
                    folderfield.setForeColor(DniStaticColor)
                else:
                    folderbutton.show()
                    folderfield.setStringJustify(kRightJustify)
                    if (id == selectedFolder):
                        folderfield.setForeColor(DniSelectedColor)
                        LONGfolderfield.setForeColor(DniSelectedColor)
                    else:
                        folderfield.setForeColor(DniSelectableColor)
                        LONGfolderfield.setForeColor(DniSelectableColor)
                folderfield.setString(foldername)
                LONGfolderfield.setString(foldername)
                id += 1
                if (id > kBKIFolderLineLast):
                    break

        upbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKFolderUpLine))
        if (BKFolderTopLine > 0):
            upbtn.show()
        else:
            upbtn.hide()
        dwnbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKFolderDownLine))
        if (id > kBKIFolderLineLast):
            dwnbtn.show()
        else:
            dwnbtn.hide()
        for tagid in range(id, (kBKIFolderLineLast + 1)):
            folderfield = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(tagid))
            folderfield.setForeColor(DniSelectableColor)
            folderfield.setString(' ')
            buttonid = ((tagid - kBKIFolderLine01) + kBKIFolderLineBtn01)
            folderbutton = ptGUIControlButton(BigKI.dialog.getControlFromTag(buttonid))
            folderbutton.hide()




    def IBigKINewContentList(self):
        global BKContentList
        global BKContentListTopLine
        try:
            foldername = BKFolderListOrder[BKFolderSelected]
            folder = BKFolderLineDict[foldername]
            if (type(folder) != type(None)):
                if isinstance(folder, ptVaultNode):
                    if (folder.getType() == PtVaultNodeTypes.kAgeInfoNode):
                        try:
                            BKContentList = folder.getCanVisitFolder().getChildNodeRefList()
                        except AttributeError:
                            BKContentList = []
                    else:
                        BKContentList = folder.getChildNodeRefList()
                    self.IBigKIProcessContentList(removeInboxStuff=1)
                    if BKFolderSelectChanged:
                        BKContentListTopLine = 0
                elif isinstance(folder, kiFolder):
                    BKContentList = self.IRemoveCCRPlayers(PtGetPlayerListDistanceSorted())
                    self.IBigKIProcessContentList(removeInboxStuff=1)
                    if BKFolderSelectChanged:
                        BKContentListTopLine = 0
                else:
                    BKContentList = []
        except (IndexError, KeyError):
            del BKContentList[:]
        self.IBigKIRefreshContentListDisplay()


    def IBigKIRefreshContentList(self):
        global BKContentList
        try:
            foldername = BKFolderListOrder[BKFolderSelected]
            folder = BKFolderLineDict[foldername]
            if (type(folder) != type(None)):
                if isinstance(folder, ptVaultNode):
                    if (folder.getType() == PtVaultNodeTypes.kAgeInfoNode):
                        try:
                            BKContentList = folder.getCanVisitFolder().getChildNodeRefList()
                        except AttributeError:
                            BKContentList = []
                    else:
                        BKContentList = folder.getChildNodeRefList()
                    self.IBigKIProcessContentList()
                elif isinstance(folder, kiFolder):
                    BKContentList = self.IRemoveCCRPlayers(PtGetPlayerListDistanceSorted())
                    self.IBigKIProcessContentList()
            else:
                del BKContentList[:]
        except LookupError:
            pass



    def IBigKIProcessContentList(self, removeInboxStuff = 0):
        global BKContentList
        removelist = []
        if (BKFolderLineDict is BKPlayerFolderDict):
            ignores = ptVault().getIgnoreListFolder()
            if (len(BKContentList) > 0):
                if isinstance(BKContentList[0], ptPlayer):
                    for idx in range(len(BKContentList)):
                        player = BKContentList[idx]
                        if isinstance(player, ptPlayer):
                            if ignores.playerlistHasPlayer(player.getPlayerID()):
                                removelist.insert(0, idx)
                        else:
                            removelist.insert(0, idx)

                else:
                    BKContentList.sort(CMPplayerOnline)
                    for idx in range(len(BKContentList)):
                        ref = BKContentList[idx]
                        elem = ref.getChild()
                        if (type(elem) != type(None)):
                            if (elem.getType() == PtVaultNodeTypes.kPlayerInfoNode):
                                elem = elem.upcastToPlayerInfoNode()
                                if (elem.playerGetName() == ''):
                                    removelist.insert(0, idx)
                                elif ignores.playerlistHasPlayer(elem.playerGetID()):
                                    parent = ref.getParent()
                                    if parent:
                                        parent = parent.upcastToFolderNode()
                                    if (type(parent) != type(None)):
                                        if (parent.folderGetType() != PtVaultStandardNodes.kIgnoreListFolder):
                                            removelist.insert(0, idx)
                            else:
                                removelist.insert(0, idx)
                        else:
                            removelist.insert(0, idx)

        elif (OnlyGetPMsFromBuddies and (BKFolderListOrder[BKFolderSelected] == xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kInboxFolder))):
            vault = ptVault()
            inbox = vault.getInbox()
            buddies = vault.getBuddyListFolder()
            for idx in range(len(BKContentList)):
                ref = BKContentList[idx]
                if (type(ref) != type(None)):
                    if (not buddies.playerlistHasPlayer(ref.getSaverID())):
                        PtDebugPrint(('xKI:remove from inbox because from %s' % ref.getSaver().playerGetName()), level=kWarningLevel)
                        removelist.insert(0, idx)
                        if removeInboxStuff:
                            PtDebugPrint(('xKI:REALLY removed from inbox because from %s, this time' % ref.getSaver().playerGetName()), level=kWarningLevel)
                            element = ref.getChild()
                            inbox.removeNode(element)

        if len(removelist):
            PtDebugPrint(('xKI: removing %d contents from being displayed' % len(removelist)), level=kWarningLevel)
        for removeidx in removelist:
            del BKContentList[removeidx]

        if (BKFolderListOrder[BKFolderSelected] == xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kInboxFolder)):
            BKContentList = (MarkerJoinRequests + BKContentList)
            vault = ptVault()
            ginbox = vault.getGlobalInbox()
            if (type(ginbox) != type(None)):
                BKContentList = (ginbox.getChildNodeRefList() + BKContentList)
##############################################################################
# diafero: Sort all KI folders by date (not only the inbox)
##############################################################################
#                BKContentList.sort(CMPNodeDate)
        if not (BKFolderLineDict is BKPlayerFolderDict):
            BKContentList.sort(CMPNodeDate)
##############################################################################
# End diafero: Sort all KI folders by date
##############################################################################



    def IBigKIRefreshContentListDisplay(self):
        global BKContentListTopLine
        if (BKRightSideMode == kBKListMode):
            createfield = ptGUIControlTextBox(KIListModeDialog.dialog.getControlFromTag(kBKILMTitleCreateLine))
            createBtn = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag(kBKIListModeCreateBtn))
            try:
                if (BKFolderLineDict is BKPlayerFolderDict):
                    if (BKFolderListOrder[BKFolderSelected] == xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kBuddyListFolder)):
                        createfield.setString(xLocalization.xKI.xCreateBuddyTitle)
                        createBtn.show()
                    else:
                        createfield.setString(' ')
                        createBtn.hide()
                elif (BKFolderListOrder[BKFolderSelected] == xLocalization.FolderIDToFolderName(PtVaultStandardNodes.kInboxFolder)):
                    createfield.setString(' ')
                    createBtn.hide()
                else:
                    createfield.setString(' ')
                    createBtn.hide()
            except IndexError:
                createfield.setString(' ')
                createBtn.hide()
                if (len(BKFolderListOrder) != 0):
                    PtDebugPrint(('xKI: Index error BKFolderSelected=%d and list=' % BKFolderSelected), BKFolderListOrder, level=kWarningLevel)
                return
            id = kBKILMOffsetLine01
            if (len(BKContentList) != 0):
                if (BKContentListTopLine >= len(BKContentList)):
                    BKContentListTopLine = (len(BKContentList) - 1)
                for content in BKContentList[BKContentListTopLine:]:
                    if (type(content) != type(None)):
                        contentIconJ = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag((id + kBKILMIconJournalOffset)))
                        contentIconAva = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag((id + kBKILMIconPersonOffset)))
                        contentIconP = ptGUIControlDynamicText(KIListModeDialog.dialog.getControlFromTag((id + kBKILMIconPictureOffset)))
                        contentTitle = ptGUIControlTextBox(KIListModeDialog.dialog.getControlFromTag((id + kBKILMTitleOffset)))
                        contentDate = ptGUIControlTextBox(KIListModeDialog.dialog.getControlFromTag((id + kBKILMDateOffset)))
                        contentFrom = ptGUIControlTextBox(KIListModeDialog.dialog.getControlFromTag((id + kBKILMFromOffset)))
                        if isinstance(content, QuestionNote):
                            contentIconJ.show()
                            contentIconP.hide()
                            contentIconAva.hide()
                            contentTitle.setForeColor(DniSelectableColor)
                            contentTitle.setString(xCensor.xCensor(content.title, theCensorLevel))
                            contentTitle.show()
                            contentDate.setString(' ')
                            contentDate.hide()
                            contentFrom.setForeColor(DniSelectableColor)
                            contentFrom.setString(xCensor.xCensor(content.game.master.player.getPlayerName(), theCensorLevel))
                            contentFrom.show()
                            lmbutton = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag((((id - 100) / 10) + kBKIListModeCreateBtn)))
                            lmbutton.show()
                            id += 10
                            if (id > kBKILMOffsetLineLast):
                                break
                        elif isinstance(content, ptPlayer):
                            contentIconAva.show()
                            contentIconJ.hide()
                            contentIconP.hide()
                            contentTitle.setForeColor(DniSelectableColor)
                            contentTitle.setString(xCensor.xCensor(content.getPlayerName(), theCensorLevel))
                            contentTitle.show()
                            contentDate.hide()
                            contentFrom.setForeColor(DniSelectableColor)
                            contentFrom.setString(self.IGetAgeInstanceName())
                            contentFrom.show()
                            lmbutton = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag((((id - 100) / 10) + kBKIListModeCreateBtn)))
                            lmbutton.show()
                            id += 10
                            if (id > kBKILMOffsetLineLast):
                                break
                        else:
                            element = content.getChild()
                            if (type(element) != type(None)):
                                if (element.getType() == PtVaultNodeTypes.kTextNoteNode):
                                    element = element.upcastToTextNoteNode()
                                    contentIconJ.show()
                                    contentIconP.hide()
                                    contentIconAva.hide()
                                elif (element.getType() == PtVaultNodeTypes.kImageNode):
                                    element = element.upcastToImageNode()
                                    contentIconJ.hide()
                                    contentIconAva.hide()
                                    if (contentIconP.getNumMaps() > 0):
                                        dynmap = contentIconP.getMap(0)
                                        image = element.imageGetImage()
                                        dynmap.clearToColor(ptColor(0.1, 0.1, 0.1, 0.1))
                                        if (type(image) != type(None)):
                                            dynmap.drawImage(kBKIImageStartX, kBKIImageStartY, image, 0)
                                        dynmap.flush()
                                    contentIconP.show()
                                elif (element.getType() == PtVaultNodeTypes.kPlayerInfoNode):
                                    element = element.upcastToPlayerInfoNode()
                                    contentIconAva.show()
                                    contentIconJ.hide()
                                    contentIconP.hide()
                                elif (element.getType() == PtVaultNodeTypes.kMarkerListNode):
                                    element = element.upcastToMarkerListNode()
                                    contentIconAva.hide()
                                    contentIconJ.hide()
                                    contentIconP.hide()
                                else:
                                    contentIconAva.hide()
                                    contentIconJ.hide()
                                    contentIconP.hide()
                                if isinstance(element, ptVaultPlayerInfoNode):
                                    contentTitle.setForeColor(DniSelectableColor)
                                    contentTitle.setString(xCensor.xCensor(element.playerGetName(), theCensorLevel))
                                    contentTitle.show()
                                    contentDate.hide()
                                    contentFrom.setForeColor(DniSelectableColor)
# Manage hidden players BEGIN
                                    if element.playerIsOnline() and not len(element.getCreateAgeName()):
                                        contentFrom.setString(self.IConvertAgeName(element.playerGetAgeInstanceName()))
                                    elif element.playerIsOnline() and gShowHiddenPlayers:
                                        contentFrom.setString('Hidden')
                                    else:
                                        contentFrom.setString('  ')
# Manage hidden players END
                                    contentFrom.show()
                                else:
##############################################################################
# diafero: fix for new incoming KI messages to be shown as global Admin messages
##############################################################################
#                                    if (content.getSaverID() == 0):
                                    if (element.getOwnerNodeID() == 0):
                                        contentTitle.setForeColor(DniStaticColor)
                                        contentDate.setForeColor(DniStaticColor)
                                        contentFrom.setForeColor(DniStaticColor)
                                    else:
                                        contentTitle.setForeColor(DniSelectableColor)
                                        contentDate.setForeColor(DniSelectableColor)
                                        contentFrom.setForeColor(DniSelectableColor)
##############################################################################
# End diafero: fix for new incoming KI messages to be shown as global Admin messages
##############################################################################
                                    if isinstance(element, ptVaultImageNode):
                                        contentTitle.setString(xCensor.xCensor(element.imageGetTitle(), theCensorLevel))
                                    elif isinstance(element, ptVaultTextNoteNode):
                                        contentTitle.setString(xCensor.xCensor(element.noteGetTitle(), theCensorLevel))
                                    elif isinstance(element, ptVaultMarkerListNode):
                                        if (PhasedKIShowMarkerGame and (gKIMarkerLevel >= kKIMarkerNormalLevel)):
                                            contentTitle.setString(xCensor.xCensor(element.folderGetName(), theCensorLevel))
                                        else:
                                            contentTitle.setString('???')
                                    else:
                                        contentTitle.setString('?UNKNOWN?')
                                        PtDebugPrint(('xKI: error - unknown data type in content list. type=%d' % element.getType()), element, level=kErrorLevel)
                                    contentTitle.show()
                                    tuptime = time.gmtime(PtGMTtoDniTime(element.getModifyTime()))
                                    curtime = time.strftime(xLocalization.xGlobal.xDateFormat, tuptime)
                                    contentDate.setString(curtime)
                                    contentDate.show()
##############################################################################
# diafero: fix for new incoming KI messages to be shown as global Admin messages
##############################################################################
#                                    sender = content.getSaver()
#                                    localplayer = PtGetLocalPlayer()
#                                    if ((type(sender) != type(None)) and (localplayer.getPlayerID() != sender.playerGetID())):
#                                        if (content.getSaverID() == 0):
#                                            contentFrom.setForeColor(DniStaticColor)
#                                            contentFrom.setFontSize(13)
#                                            contentFrom.setString('DRC')
#                                        else:
#                                            contentFrom.setForeColor(DniSelectableColor)
#                                            contentFrom.setFontSize(10)
#                                            contentFrom.setString(sender.playerGetName())
#                                        contentFrom.show()
#                                    elif (content.getSaverID() == 0):
#                                        contentFrom.setString('DRC')
#                                        contentFrom.show()
#                                    else:
#                                        contentFrom.setString('  ')
#                                        contentFrom.hide()
                                    if (element.getOwnerNodeID() == 0):
                                        contentFrom.setString('Global Msg')
                                    else:
                                        try: # this fails for imagers, and in the KI when the player got deleted
                                            contentFrom.setString(element.getOwnerNode().playerGetName())
                                        except:
                                            contentFrom.setString('(unknown)')
                                    contentFrom.show()
##############################################################################
# End diafero: fix for new incoming KI messages to be shown as global Admin messages
##############################################################################
                                lmbutton = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag((((id - 100) / 10) + kBKIListModeCreateBtn)))
                                lmbutton.show()
                                id += 10
                                if (id > kBKILMOffsetLineLast):
                                    break
                            else:
                                PtDebugPrint('bigKI: no element inside the content. Doh!', level=kErrorLevel)
                    else:
                        PtDebugPrint('bigKI: no content, even though the folder said it was!', level=kErrorLevel)

            upbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKLMUpButton))
            if (BKContentListTopLine > 0):
                upbtn.show()
            else:
                upbtn.hide()
            dwnbtn = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKLMDownButton))
            if (id > kBKILMOffsetLineLast):
                dwnbtn.show()
            else:
                dwnbtn.hide()
            for tagid in range(id, (kBKILMOffsetLineLast + 10), 10):
                iconpic = ptGUIControlDynamicText(KIListModeDialog.dialog.getControlFromTag((tagid + kBKILMIconPictureOffset)))
                iconpic.hide()
                iconjrn = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag((tagid + kBKILMIconJournalOffset)))
                iconjrn.hide()
                iconava = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag((tagid + kBKILMIconPersonOffset)))
                iconava.hide()
                titlefield = ptGUIControlTextBox(KIListModeDialog.dialog.getControlFromTag((tagid + kBKILMTitleOffset)))
                titlefield.hide()
                datefield = ptGUIControlTextBox(KIListModeDialog.dialog.getControlFromTag((tagid + kBKILMDateOffset)))
                datefield.hide()
                fromfield = ptGUIControlTextBox(KIListModeDialog.dialog.getControlFromTag((tagid + kBKILMFromOffset)))
                fromfield.hide()
                lmbutton = ptGUIControlButton(KIListModeDialog.dialog.getControlFromTag((((tagid - 100) / 10) + kBKIListModeCreateBtn)))
                lmbutton.hide()




    def IBigKIDisplayCurrentContentJournal(self):
        jrnAgeName = ptGUIControlTextBox(KIJournalExpanded.dialog.getControlFromTag(kBKIJRNAgeName))
        jrnAgeName.hide()
        jrnDate = ptGUIControlTextBox(KIJournalExpanded.dialog.getControlFromTag(kBKIJRNDate))
        jrnDate.hide()
        jrnTitle = ptGUIControlTextBox(KIJournalExpanded.dialog.getControlFromTag(kBKIJRNTitle))
        jrnTitle.hide()
        jrnNote = ptGUIControlMultiLineEdit(KIJournalExpanded.dialog.getControlFromTag(kBKIJRNNote))
        jrnNote.hide()
        jrnNote.setBufferLimit(kJournalTextSize)
        jrnDeleteBtn = ptGUIControlButton(KIJournalExpanded.dialog.getControlFromTag(kBKIJRNDeleteButton))
        jrnDeleteBtn.hide()
        jrnTitleBtn = ptGUIControlButton(KIJournalExpanded.dialog.getControlFromTag(kBKIJRNTitleButton))
        if (type(BKCurrentContent) != type(None)):
            if self.IsContentMutable(BKCurrentContent):
                jrnDeleteBtn.show()
                jrnNote.unlock()
                if (BKInEditMode and (BKEditField == kBKEditFieldJRNTitle)):
                    pass
                else:
                    jrnTitleBtn.show()
            else:
                jrnNote.lock()
                jrnTitleBtn.hide()
            element = BKCurrentContent.getChild()
            if (type(element) != type(None)):
                datatype = element.getType()
                if (datatype == PtVaultNodeTypes.kTextNoteNode):
                    element = element.upcastToTextNoteNode()
                    jrnAgeName.setString(self.IConvertAgeName(xCensor.xCensor(element.getCreateAgeName(), theCensorLevel)))
                    jrnAgeName.show()
                    tuptime = time.gmtime(PtGMTtoDniTime(element.getModifyTime()))
                    curtime = time.strftime(xLocalization.xGlobal.xDateFormat, tuptime)
                    jrnDate.setString(curtime)
                    jrnDate.show()
                    if (BKInEditMode and (BKEditField == kBKEditFieldJRNTitle)):
                        pass
                    else:
                        jrnTitle.setString(xCensor.xCensor(element.noteGetTitle(), theCensorLevel))
                        jrnTitle.show()
                    if (BKInEditMode and (BKEditField == kBKEditFieldJRNNote)):
                        pass
                    else:
                        encoded = buffer(xCensor.xCensor(element.noteGetText(), theCensorLevel))
                        jrnNote.setEncodedBuffer(encoded)
                        jrnNote.show()
                    self.IBigKISetSeen(BKCurrentContent)
                    self.ICheckContentForSender(BKCurrentContent)
                else:
                    PtDebugPrint(('xBigKI: Display current content - wrong element type %d' % datatype), level=kErrorLevel)
            else:
                PtDebugPrint('xBigKI: Display current content - element is None', level=kErrorLevel)
        else:
            PtDebugPrint('xBigKI: Display current content - BKCurrentContent is None', level=kErrorLevel)



    def IBigKIDisplayCurrentContentImage(self):
        picAgeName = ptGUIControlTextBox(KIPictureExpanded.dialog.getControlFromTag(kBKIPICAgeName))
        picAgeName.hide()
        picDate = ptGUIControlTextBox(KIPictureExpanded.dialog.getControlFromTag(kBKIPICDate))
        picDate.hide()
        picTitle = ptGUIControlTextBox(KIPictureExpanded.dialog.getControlFromTag(kBKIPICTitle))
        picTitle.hide()
        picImage = ptGUIControlDynamicText(KIPictureExpanded.dialog.getControlFromTag(kBKIPICImage))
        picImage.hide()
        picDeleteBtn = ptGUIControlButton(KIPictureExpanded.dialog.getControlFromTag(kBKIPICDeleteButton))
        picDeleteBtn.hide()
        picTitleBtn = ptGUIControlButton(KIPictureExpanded.dialog.getControlFromTag(kBKIPICTitleButton))
        if (type(BKCurrentContent) != type(None)):
            if self.IsContentMutable(BKCurrentContent):
                picDeleteBtn.show()
                if (BKInEditMode and (BKEditField == kBKEditFieldPICTitle)):
                    pass
                else:
                    picTitleBtn.show()
            else:
                picTitleBtn.hide()
            element = BKCurrentContent.getChild()
            if (type(element) != type(None)):
                datatype = element.getType()
                if (datatype == PtVaultNodeTypes.kImageNode):
                    element = element.upcastToImageNode()
                    picAgeName.setString(self.IConvertAgeName(xCensor.xCensor(element.getCreateAgeName(), theCensorLevel)))
                    picAgeName.show()
                    tuptime = time.gmtime(PtGMTtoDniTime(element.getModifyTime()))
                    curtime = time.strftime(xLocalization.xGlobal.xDateFormat, tuptime)
                    picDate.setString(curtime)
                    picDate.show()
                    if (BKInEditMode and (BKEditField == kBKEditFieldPICTitle)):
                        pass
                    else:
                        picTitle.setString(xCensor.xCensor(element.imageGetTitle(), theCensorLevel))
                        picTitle.show()
                    if (picImage.getNumMaps() > 0):
                        dynmap = picImage.getMap(0)
                        image = element.imageGetImage()
                        dynmap.clearToColor(ptColor(0.1, 0.1, 0.1, 0.3))
                        if (type(image) != type(None)):
                            dynmap.drawImage(kBKIImageStartX, kBKIImageStartY, image, 0)
                        else:
                            dynmap.fillRect(kBKIImageStartX, kBKIImageStartY, (kBKIImageStartX + 800), (kBKIImageStartY + 600), ptColor(0.2, 0.2, 0.2, 0.1))
                        dynmap.flush()
                    picImage.show()
                    self.IBigKISetSeen(BKCurrentContent)
                    self.ICheckContentForSender(BKCurrentContent)
                else:
                    PtDebugPrint(('xBigKI: Display current content - wrong element type %d' % datatype), level=kErrorLevel)
            else:
                PtDebugPrint('xBigKI: Display current content - element is None', level=kErrorLevel)
        else:
            PtDebugPrint('xBigKI: Display current content - BKCurrentContent is None', level=kErrorLevel)



    def IBigKIDisplayCurrentContentPlayer(self):
        global BKPlayerSelected
        plyName = ptGUIControlTextBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYName))
        plyName.hide()
        plyID = ptGUIControlTextBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYID))
        plyID.hide()
        plyIDedit = ptGUIControlEditBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYPlayerIDEditBox))
        plyIDedit.hide()
        plyDetail = ptGUIControlTextBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYDetail))
        plyDetail.hide()
        plyDeleteBtn = ptGUIControlButton(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYDeleteButton))
        plyDeleteBtn.hide()
        if BKGettingPlayerID:
            plyName.setString(xLocalization.xKI.xPlayerEnterID)
            plyName.show()
            plyIDedit.setString('')
            plyIDedit.show()
            plyIDedit.focus()
            KIPlayerExpanded.dialog.setFocus(plyIDedit.getKey())
        elif (type(BKCurrentContent) != type(None)):
            if isinstance(BKCurrentContent, ptPlayer):
                plyName.setString(xCensor.xCensor(BKCurrentContent.getPlayerName(), theCensorLevel))
                plyName.show()
                idtext = ('%08d' % BKCurrentContent.getPlayerID())
                plyID.setString(idtext)
                plyID.show()
                plyDetail.setString((xLocalization.xKI.xPlayerInAge % self.IGetAgeDisplayName()))
                plyDetail.show()
                sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
                BKPlayerSelected = BKCurrentContent
                sendToField.setString(BKCurrentContent.getPlayerName())
            else:
                element = BKCurrentContent.getChild()
                if (type(element) != type(None)):
                    datatype = element.getType()
                    if (datatype == PtVaultNodeTypes.kPlayerInfoNode):
                        element = element.upcastToPlayerInfoNode()
                        plyName.setString(xCensor.xCensor(element.playerGetName(), theCensorLevel))
                        plyName.show()
                        idtext = ('%08d' % element.playerGetID())
                        plyID.setString(idtext)
                        plyID.show()
# Manage hidden players BEGIN
                        if element.playerIsOnline() and not len(element.getCreateAgeName()):
# Manage hidden players END
                            if (element.playerGetAgeInstanceName() == 'Cleft'):
                                plyDetail.setString(xLocalization.xKI.xPlayerInCleft)
                            elif (element.playerGetAgeInstanceName() == 'AvatarCustomization'):
                                plyDetail.setString(xLocalization.xKI.xPlayerInCloset)
                            else:
                                plyDetail.setString((xLocalization.xKI.xPlayerInAge % self.IConvertAgeName(element.playerGetAgeInstanceName())))
# Manage hidden players BEGIN
                        elif element.playerIsOnline() and gShowHiddenPlayers:
                            plyDetail.setString('This player is hidden in the %s Age.' % self.IConvertAgeName(element.playerGetAgeInstanceName()))
# Manage hidden players END
                        else:
                            plyDetail.setString(xLocalization.xKI.xPlayerOffline)
                        plyDetail.show()
                        folder = BKCurrentContent.getParent()
                        if folder:
                            folder = folder.upcastToFolderNode()
                        if (folder and self.IsFolderContentsMutable(folder)):
                            plyDeleteBtn.show()
                        sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
                        BKPlayerSelected = BKCurrentContent
                        sendToField.setString(element.playerGetName())
                    else:
                        PtDebugPrint(('xBigKI: Display current content - wrong element type %d' % datatype), level=kErrorLevel)
                else:
                    PtDebugPrint('xBigKI: Display current content - element is None', level=kErrorLevel)
        else:
            PtDebugPrint('xBigKI: Display current content - BKCurrentContent is None', level=kErrorLevel)



    def IBigKIDisplayCurrentContentMarkerFolder(self):
        global MFdialogMode
        mrkfldTitle = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTitleText))
        mrkfldTitle.hide()
        mrkfldStatus = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderStatus))
        mrkfldStatus.hide()
        mrkfldOwner = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderOwner))
        mrkfldOwner.hide()
        mrkfldMLUpBtn = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerListUpBtn))
        mrkfldMLDownBtn = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerListDownBtn))
        mrkfldMLUpBtn.hide()
        mrkfldMLDownBtn.hide()
        selectedMarker = None
        questGameFinished = 0
        MGmgr = ptMarkerMgr()
        if ((type(MGmgr) != type(None)) and (type(BKCurrentContent) != type(None))):
            element = BKCurrentContent.getChild()
            if (type(element) != type(None)):
                datatype = element.getType()
                if (datatype == PtVaultNodeTypes.kMarkerListNode):
                    element = element.upcastToMarkerListNode()
                    workingMF = MGmgr.getWorkingMarkerFolder()
                    if ((type(workingMF) != type(None)) and (workingMF.getID() == element.getID())):
                        if MGmgr.isGameRunning():
                            MFdialogMode = kMFPlaying
                        elif MGmgr.getSelectedMarker():
                            MFdialogMode = kMFEditingMarker
                        else:
                            MFdialogMode = kMFEditing
                    else:
                        MFdialogMode = kMFOverview
                    self.IBigKISetToButtons()
                    mbtnInvitePlayer = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderInvitePlayer))
                    mbtnEditStart = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderEditStartGame))
                    mbtnPlayEnd = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderPlayEndGame))
                    mtbInvitePlayer = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderInvitePlayerTB))
                    mtbEditStart = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderEditStartGameTB))
                    mtbPlayEnd = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderPlayEndGameTB))
                    mrkfldTitleBtn = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTitleBtn))
                    mbtnDelete = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderDeleteBtn))
                    mbtnGameTimePullD = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTimePullDownBtn))
                    mbtnGameTypePullD = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTypePullDownBtn))
                    mbtnGameTimeArrow = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTimeArrow))
                    mbtnGameTypeArrow = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTypeArrow))
                    mtbGameTime = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderGameTimeTB))
                    mtbGameTimeTitle = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderGameTimeTitleTB))
                    mtbGameTimeTitle.setString(xLocalization.xKI.xMarkerGameTimeText)
                    mtbGameType = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderGameTypeTB))
                    mlbMarkerList = ptGUIControlListBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkListbox))
                    mlbMarkerTextTB = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerTextTB))
                    mbtnMarkerText = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerTextBtn))
                    mbtnToran = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderToranIcon))
                    mbtnToran.disable()
                    mbtnHSpan = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderHSpanIcon))
                    mbtnHSpan.disable()
                    mbtnVSpan = ptGUIControlButton(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderVSpanIcon))
                    mbtnVSpan.disable()
                    mtbToran = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderToranTB))
                    mtbHSPan = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderHSpanTB))
                    mtbVSpan = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderVSpanTB))
                    if (MFdialogMode == kMFOverview):
                        mrkfldTitleBtn.disable()
                        mbtnDelete.show()
                        mbtnGameTimePullD.hide()
                        mbtnGameTypePullD.hide()
                        mbtnGameTimeArrow.hide()
                        mbtnGameTypeArrow.hide()
                        mbtnInvitePlayer.hide()
                        mtbInvitePlayer.setForeColor(Clear)
                        mtbInvitePlayer.setString(' ')
                        canBePlayed = (PhasedKIPlayMarkerGame and ((element.getGameType() == PtMarkerMsgGameType.kGameTypeQuest) or (PtGetAgeInfo().getAgeInstanceName() == element.getCreateAgeName()))) # this is a quest game or we are in the age the mission was created for
                        if (canBePlayed and (element.getOwnerID() == PtGetLocalPlayer().getPlayerID())):
                            mbtnEditStart.show()
                            mtbEditStart.setForeColor(DniColorShowBtn)
                        else:
                            mbtnEditStart.hide()
                            mtbEditStart.setForeColor(DniColorGhostBtn)
                        mtbEditStart.setString(xLocalization.xKI.xMarkerGameEditButton)
                        if canBePlayed:
                            mbtnPlayEnd.show()
                            mtbPlayEnd.setForeColor(DniColorShowBtn)
                        else:
                            mbtnPlayEnd.hide()
                            mtbPlayEnd.setForeColor(DniColorGhostBtn)
                        mtbPlayEnd.setString(xLocalization.xKI.xMarkerGamePlayButton)
                        mlbMarkerList.hide()
                        mlbMarkerTextTB.hide()
                        mbtnToran.hide()
                        mbtnHSpan.hide()
                        mbtnVSpan.hide()
                        mtbToran.hide()
                        mtbHSPan.hide()
                        mtbVSpan.hide()
                        mbtnMarkerText.disable()
                    elif ((MFdialogMode == kMFEditing) or (MFdialogMode == kMFEditingMarker)):
                        mrkfldTitleBtn.enable()
                        mbtnDelete.hide()
                        if len(element.getChildNodeRefList()):
                            mbtnGameTypePullD.hide()
                            mbtnGameTypeArrow.hide()
                        else:
                            # disable the game type button that does not offer any choice anyway
                            #mbtnGameTypePullD.show()
                            mbtnGameTypePullD.hide()
                            #mbtnGameTypeArrow.show()
                            mbtnGameTypeArrow.hide()
                        if (element.getGameType() != PtMarkerMsgGameType.kGameTypeQuest):
                            mbtnGameTimePullD.show()
                            mbtnGameTimeArrow.show()
                        else:
                            mbtnGameTimePullD.hide()
                            mbtnGameTimeArrow.hide()
                        mbtnInvitePlayer.hide()
                        mtbInvitePlayer.setForeColor(Clear)
                        mtbInvitePlayer.setString(' ')
                        mbtnEditStart.show()
                        mtbEditStart.setForeColor(DniColorShowBtn)
                        mbtnPlayEnd.show()
                        mtbPlayEnd.setForeColor(DniColorShowBtn)
                        if (MFdialogMode == kMFEditing):
                            mtbEditStart.setString(xLocalization.xKI.xMarkerGameDoneEditButton)
                            mtbPlayEnd.setString(xLocalization.xKI.xMarkerGameAddMarkerButton)
                            mlbMarkerList.clearAllElements()
                            mlbMarkerList.show()
                            markerRefs = element.getChildNodeRefList()
                            for markerRef in markerRefs:
                                marker = markerRef.getChild()
                                if marker:
                                    marker = marker.upcastToMarkerNode()
                                    if marker:
                                        if (element.getGameType() != PtMarkerMsgGameType.kGameTypeQuest):
                                            mlbMarkerList.addString(('[%d,%d,%d] %s' % (marker.markerGetTorans(), marker.markerGetHSpans(), marker.markerGetVSpans(), marker.markerGetText())))
                                        else:
                                            mlbMarkerList.addString(('[%s:%d,%d,%d] %s' % (self.IConvertAgeName(marker.getCreateAgeName()), marker.markerGetTorans(), marker.markerGetHSpans(), marker.markerGetVSpans(), marker.markerGetText())))
                            mlbMarkerTextTB.hide()
                            mbtnToran.hide()
                            mbtnHSpan.hide()
                            mbtnVSpan.hide()
                            mtbToran.hide()
                            mtbHSPan.hide()
                            mtbVSpan.hide()
                            mbtnMarkerText.disable()
                        else:
                            selID = MGmgr.getSelectedMarker()
                            PtDebugPrint(('xKI:Marker: looking for selected marker %d' % selID), level=kDebugDumpLevel)
                            selectedMarker = None
                            markerRefs = element.getChildNodeRefList()
                            for markerRef in markerRefs:
                                marker = markerRef.getChild()
                                if marker:
                                    marker = marker.upcastToMarkerNode()
                                    if marker:
                                        if (marker.getID() == selID):
                                            selectedMarker = marker

                            if (type(selectedMarker) != type(None)):
                                mtbEditStart.setString(xLocalization.xKI.xMarkerGameMarkerListButton)
                                mtbPlayEnd.setString(xLocalization.xKI.xMarkerGameRemoveMarkerButton)
                                mlbMarkerList.hide()
                                mlbMarkerTextTB.show()
                                mlbMarkerTextTB.setString(selectedMarker.markerGetText())
                                mbtnToran.show()
                                mbtnHSpan.show()
                                mbtnVSpan.show()
                                mtbToran.show()
                                mtbHSPan.show()
                                mtbVSpan.show()
                                mtbToran.setString(('%d' % selectedMarker.markerGetTorans()))
                                mtbHSPan.setString(('%d' % selectedMarker.markerGetHSpans()))
                                mtbVSpan.setString(('%d' % selectedMarker.markerGetVSpans()))
                                mbtnMarkerText.enable()
                            else:
                                PtDebugPrint(('xKI:Marker: could not find selected marker %d' % selID), level=kErrorLevel)
                                mtbEditStart.setString(xLocalization.xKI.xMarkerGameGoBackButton)
                                mtbPlayEnd.setString(' ')
                                mlbMarkerList.hide()
                                mlbMarkerTextTB.show()
                                mlbMarkerTextTB.setString('?Unknown mark?')
                                mbtnToran.hide()
                                mbtnHSpan.hide()
                                mbtnVSpan.hide()
                                mtbToran.hide()
                                mtbHSPan.hide()
                                mtbVSpan.hide()
                    elif (MFdialogMode == kMFPlaying):
                        mrkfldTitleBtn.disable()
                        mbtnDelete.hide()
                        mbtnGameTimePullD.hide()
                        mbtnGameTypePullD.hide()
                        mbtnGameTimeArrow.hide()
                        mbtnGameTypeArrow.hide()
                        mbtnToran.hide()
                        mbtnHSpan.hide()
                        mbtnVSpan.hide()
                        mtbToran.hide()
                        mtbHSPan.hide()
                        mtbVSpan.hide()
                        mbtnMarkerText.disable()
                        if ((element.getGameType() == PtMarkerMsgGameType.kGameTypeCapture) or (element.getGameType() == PtMarkerMsgGameType.kGameTypeHold)):
                            if (MarkerGameState == kMGGameOn):
                                mtbInvitePlayer.setForeColor(DniColorGhostBtn)
                                mbtnInvitePlayer.hide()
                                mtbEditStart.setForeColor(DniColorGhostBtn)
                                mbtnEditStart.hide()
                            else:
                                mbtnInvitePlayer.show()
                                mtbInvitePlayer.setForeColor(DniColorShowBtn)
                                mtbEditStart.setForeColor(DniColorShowBtn)
                                mbtnEditStart.show()
                            mtbInvitePlayer.setString(xLocalization.xKI.xMarkerGameInviteButton)
                            mtbEditStart.setString(xLocalization.xKI.xMarkerGameStartGameButton)
                            mbtnPlayEnd.show()
                            mtbPlayEnd.setForeColor(DniColorShowBtn)
                            mtbPlayEnd.setString(xLocalization.xKI.xMarkerGameEndGameButton)
                            mlbMarkerList.hide()
                            mlbMarkerTextTB.hide()
                        else:
                            mbtnInvitePlayer.hide()
                            mbtnEditStart.show()
                            mtbEditStart.setForeColor(DniColorShowBtn)
                            mtbEditStart.setString(xLocalization.xKI.xMarkerGameStopPlayingButton)
                            mbtnPlayEnd.show()
                            mtbPlayEnd.setForeColor(DniColorShowBtn)
                            mtbPlayEnd.setString(xLocalization.xKI.xMarkerGameResetGameButton)
                            mlbMarkerList.clearAllElements()
                            mlbMarkerList.show()
                            questGameFinished = 1
                            markerRefs = element.getChildNodeRefList()
                            for markerRef in markerRefs:
                                if markerRef.beenSeen():
                                    marker = markerRef.getChild()
                                    if marker:
                                        marker = marker.upcastToMarkerNode()
                                        if marker:
                                            mlbMarkerList.addString(('[%s:%d,%d,%d] %s' % (self.IConvertAgeName(marker.getCreateAgeName()), marker.markerGetTorans(), marker.markerGetHSpans(), marker.markerGetVSpans(), marker.markerGetText())))
                                else:
                                    questGameFinished = 0
                            mlbMarkerTextTB.hide()
                    mtbInvitePlayer.refresh()
                    mtbEditStart.refresh()
                    mtbPlayEnd.refresh()
                    mrkfldTitle.setString(xCensor.xCensor(element.folderGetName(), theCensorLevel))
                    mrkfldTitle.show()
                    count = element.getChildNodeCount()
                    if ((element.getGameType() != PtMarkerMsgGameType.kGameTypeQuest) or ((MFdialogMode == kMFEditing) or (MFdialogMode == kMFEditingMarker))):
                        if (count == 0):
                            statusLine = xLocalization.xKI.xMarkerGameStatusNoMarkers
                        elif (count == 1):
                            statusLine = xLocalization.xKI.xMarkerGameStatusOneMarker
                        else:
                            statusLine = (xLocalization.xKI.xMarkerGameStatusNMarkers % count)
                        if ((element.getGameType() == PtMarkerMsgGameType.kGameTypeCapture) or (element.getGameType() == PtMarkerMsgGameType.kGameTypeHold)):
                            statusLine += (xLocalization.xKI.xMarkerGameStatusIn % self.IConvertAgeName(element.getCreateAgeName()))
                    elif questGameFinished:
                        statusLine = xLocalization.xKI.xMarkerGameStatusAllFound
                    else:
                        statusLine = xLocalization.xKI.xMarkerGameStatusNotAllFound
                    mrkfldStatus.setString(statusLine)
                    mrkfldStatus.show()
                    mrkfldOwner.setString((xLocalization.xKI.xMarkerGameOwnerTitle + (' %s [ID:%08d]' % (element.getOwnerName(), element.getOwnerID()))))
                    mrkfldOwner.show()
                    minutes = int((element.getRoundLength() / 60))
                    mtbGameTime.setString(('%d min' % minutes))
                    gameType = '?Unknown? game'
                    if (element.getGameType() == PtMarkerMsgGameType.kGameTypeCapture):
                        gameType = xLocalization.xKI.xMarkerGameCaptureGame
                        mtbGameTime.show()
                        mtbGameTimeTitle.show()
                    elif (element.getGameType() == PtMarkerMsgGameType.kGameTypeHold):
                        gameType = xLocalization.xKI.xMarkerGameHoldGame
                        mtbGameTime.show()
                        mtbGameTimeTitle.show()
                    elif (element.getGameType() == PtMarkerMsgGameType.kGameTypeQuest):
                        gameType = xLocalization.xKI.xMarkerGameQuestGame
                        mtbGameTime.hide()
                        mtbGameTimeTitle.hide()
                    mtbGameType.setString(gameType)
                else:
                    PtDebugPrint(('xBigKI: Display current content - wrong element type %d' % datatype), level=kErrorLevel)
            else:
                PtDebugPrint('xBigKI: Display current content - element is None', level=kErrorLevel)
        else:
            PtDebugPrint('xBigKI: Display current content - BKCurrentContent is None', level=kErrorLevel)



    def IBigKIDisplayCurrentQuestionNote(self):
        qnTitle = ptGUIControlTextBox(KIQuestionNote.dialog.getControlFromTag(kQNTitle))
        qnNote = ptGUIControlMultiLineEdit(KIQuestionNote.dialog.getControlFromTag(kQNMessage))
        qnAcceptTB = ptGUIControlTextBox(KIQuestionNote.dialog.getControlFromTag(kQNAcceptText))
        qnDeclineTB = ptGUIControlTextBox(KIQuestionNote.dialog.getControlFromTag(kQNDeclineText))
        if (type(BKCurrentContent) != type(None)):
            if isinstance(BKCurrentContent, QuestionNote):
                qnTitle.setString(BKCurrentContent.title)
                qnNote.setString(BKCurrentContent.message)
                qnAcceptTB.setString(BKCurrentContent.YesBtnText)
                qnDeclineTB.setString(BKCurrentContent.NoBtnText)
            else:
                PtDebugPrint('xBigKI:QuestionNote: Unknown data type', level=kErrorLevel)
        else:
            PtDebugPrint('xBigKI:QuestionNote: Display current content - BKCurrentContent is None', level=kErrorLevel)



    def IBigKICheckSavePlayer(self):
        global BKGettingPlayerID
        if BKGettingPlayerID:
            BKGettingPlayerID = 0
            plyIDedit = ptGUIControlEditBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYPlayerIDEditBox))
            if (not plyIDedit.wasEscaped()):
                (id, msg) = self.IGetPIDMsg(plyIDedit.getString())
                if id:
                    localplayer = PtGetLocalPlayer()
                    if (id != localplayer.getPlayerID()):
                        vault = ptVault()
                        buddies = vault.getBuddyListFolder()
                        if (type(buddies) != type(None)):
                            if buddies.playerlistHasPlayer(id):
                                plyDetail = ptGUIControlTextBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYDetail))
                                plyDetail.setString(xLocalization.xKI.xPlayerAlreadyAdded)
                                plyDetail.show()
                                BKGettingPlayerID = 1
                            else:
                                buddies.playerlistAddPlayer(id)
                                self.IDoStatusChatMessage(xLocalization.xKI.xPlayerAdded, netPropagate=0)
                        if (not BKGettingPlayerID):
                            self.IBigKIChangeMode(kBKListMode)
                    else:
                        plyDetail = ptGUIControlTextBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYDetail))
                        plyDetail.setString(xLocalization.xKI.xPlayerNotYourself)
                        plyDetail.show()
                        BKGettingPlayerID = 1
                else:
                    plyDetail = ptGUIControlTextBox(KIPlayerExpanded.dialog.getControlFromTag(kBKIPLYDetail))
                    plyDetail.setString(xLocalization.xKI.xPlayerNumberOnly)
                    plyDetail.show()
                    BKGettingPlayerID = 1
            else:
                self.IBigKIChangeMode(kBKListMode)



    def IBigKICreateJournalNote(self):
        global BKJournalFolderSelected
        global BKJournalFolderTopLine
        global BKCurrentContent
        global BKFolderSelected
        global BKFolderTopLine
        PtDebugPrint('xBigKI: create text note message', level=kDebugDumpLevel)
        if (len(BKFolderListOrder) == 0):
            self.IBigKIRefreshFolders()
        try:
            journal = BKJournalFolderDict[self.IGetAgeInstanceName()]
            if (type(journal) != type(None)):
                BKFolderTopLine = BKJournalFolderTopLine = 0
                BKFolderSelected = BKJournalFolderSelected = BKJournalListOrder.index(self.IGetAgeInstanceName())
##############################################################################
# D'Lanor's Alcugs text note fix
##############################################################################
                try:
                    note = ptVaultTextNoteNode(PtVaultNodePermissionFlags.kDefaultPermissions)
                except:
                    note = ptVaultTextNoteNode()
##############################################################################
# End D'Lanor's Alcugs text note fix
##############################################################################
                note.noteSetText(xLocalization.xKI.xJournalInitialMessage)
                note.noteSetTitle(xLocalization.xKI.xJournalInitialTitle)
                BKCurrentContent = journal.addNode(note)
                return BKCurrentContent
            else:
                PtDebugPrint('xBigKI: create journal note, journal not ready', level=kErrorLevel)
                return None
        except KeyError:
            PtDebugPrint(('xKI:BigKI - could not find journal for this age -%s' % self.IGetAgeInstanceName()), level=kErrorLevel)



    def IBigKICreateJournalImage(self, image, useScreenShot = false):
        global BKJournalFolderSelected
        global BKJournalFolderTopLine
        global BKCurrentContent
        global BKFolderSelected
        global BKFolderTopLine
        PtDebugPrint('xBigKI: create a picture element from ', image, level=kDebugDumpLevel)
        if (len(BKFolderListOrder) == 0):
            self.IBigKIRefreshFolders()
        try:
            journal = BKJournalFolderDict[self.IGetAgeInstanceName()]
            if (type(journal) != type(None)):
                BKFolderTopLine = BKJournalFolderTopLine = 0
                BKFolderSelected = BKJournalFolderSelected = BKJournalListOrder.index(self.IGetAgeInstanceName())
                img_elem = ptVaultImageNode(PtVaultNodePermissionFlags.kDefaultPermissions)
                if useScreenShot:
                    img_elem.setImageFromScrShot()
                else:
                    img_elem.imageSetImage(image)
                img_elem.imageSetTitle(xLocalization.xKI.xImageInitialTitle)
                BKCurrentContent = journal.addNode(img_elem)
                return BKCurrentContent
            else:
                PtDebugPrint('xBigKI: create journal image, journal not ready', level=kErrorLevel)
                return None
        except KeyError:
            PtDebugPrint(('xKI:BigKI - could not find journal for this age -%s' % self.IGetAgeInstanceName()), level=kErrorLevel)



    def IBigKIEnterEditMode(self, whichfield):
        global BKEditContent
        global BKEditField
        global BKInEditMode
        self.IEnterChatMode(0)
        if BKInEditMode:
            self.IBigKISaveEdit()
        if (whichfield == kBKEditFieldJRNTitle):
            textbox = ptGUIControlTextBox(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[whichfield][kBKEditIDtextbox]))
            button = ptGUIControlButton(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[whichfield][kBKEditIDbutton]))
            editbox = ptGUIControlEditBox(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[whichfield][kBKEditIDeditbox]))
        elif (whichfield == kBKEditFieldPICTitle):
            textbox = ptGUIControlTextBox(KIPictureExpanded.dialog.getControlFromTag(BKEditFieldIDs[whichfield][kBKEditIDtextbox]))
            button = ptGUIControlButton(KIPictureExpanded.dialog.getControlFromTag(BKEditFieldIDs[whichfield][kBKEditIDbutton]))
            editbox = ptGUIControlEditBox(KIPictureExpanded.dialog.getControlFromTag(BKEditFieldIDs[whichfield][kBKEditIDeditbox]))
            editbox.setStringSize(56)
        else:
            textbox = None
            button = None
            editbox = None
        if (type(textbox) != type(None)):
            if (type(BKCurrentContent) != type(None)):
                ed_element = BKCurrentContent.getChild()
            else:
                ed_element = None
            if (type(ed_element) != type(None)):
                BKInEditMode = 1
                BKEditContent = BKCurrentContent
                BKEditField = whichfield
                textbox.hide()
                button.hide()
                if (BKEditField == kBKEditFieldJRNTitle):
                    ed_element = ed_element.upcastToTextNoteNode()
                    editbox.setString(xCensor.xCensor(ed_element.noteGetTitle(), theCensorLevel))
                    KIJournalExpanded.dialog.setFocus(editbox.getKey())
                elif (BKEditField == kBKEditFieldPICTitle):
                    ed_element = ed_element.upcastToImageNode()
                    editbox.setString(xCensor.xCensor(ed_element.imageGetTitle(), theCensorLevel))
                    KIPictureExpanded.dialog.setFocus(editbox.getKey())
                else:
                    editbox.setString('')
                editbox.end()
                editbox.show()
                editbox.focus()
                if ((whichfield == kBKEditFieldJRNTitle) or (whichfield == kBKEditFieldJRNNote)):
                    KIJournalExpanded.dialog.refreshAllControls()
                elif (whichfield == kBKEditFieldPICTitle):
                    KIPictureExpanded.dialog.refreshAllControls()
            else:
                PtDebugPrint('xKI:BigKI:EnterEdit content has no element to edit?')
        elif (whichfield == kBKEditFieldJRNNote):
            BKInEditMode = 1
            BKEditContent = BKCurrentContent
            BKEditField = whichfield



    def IBigKISaveEdit(self):
        global BKEditContent
        global BKEditField
        global BKInEditMode
        if BKInEditMode:
            if (BKEditField == kBKEditFieldJRNTitle):
                textbox = ptGUIControlTextBox(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDtextbox]))
                button = ptGUIControlButton(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDbutton]))
                editbox = ptGUIControlEditBox(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDeditbox]))
            elif (BKEditField == kBKEditFieldJRNNote):
                textbox = ptGUIControlMultiLineEdit(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDtextbox]))
                button = None
                editbox = None
            elif (BKEditField == kBKEditFieldPICTitle):
                textbox = ptGUIControlTextBox(KIPictureExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDtextbox]))
                button = ptGUIControlButton(KIPictureExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDbutton]))
                editbox = ptGUIControlEditBox(KIPictureExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDeditbox]))
            else:
                textbox = None
                button = None
                editbox = None
            if (type(textbox) != type(None)):
                if (type(BKEditContent) != type(None)):
                    ed_element = BKEditContent.getChild()
                    if (type(ed_element) != type(None)):
                        if (type(editbox) != type(None)):
                            if (not editbox.wasEscaped()):
                                textbox.setString(editbox.getString())
                                if (BKEditField == kBKEditFieldJRNTitle):
                                    ed_element = ed_element.upcastToTextNoteNode()
                                    jtitle = editbox.getString()
                                    if (jtitle[:len(xLocalization.xKI.xJournalInitialTitle)] == xLocalization.xKI.xJournalInitialTitle):
                                        if (jtitle != xLocalization.xKI.xJournalInitialTitle):
                                            jtitle = jtitle[len(xLocalization.xKI.xJournalInitialTitle):]
                                    ed_element.noteSetTitle(jtitle)
                                elif (BKEditField == kBKEditFieldPICTitle):
                                    ed_element = ed_element.upcastToImageNode()
                                    ptitle = editbox.getString()
                                    if (ptitle[:len(xLocalization.xKI.xImageInitialTitle)] == xLocalization.xKI.xImageInitialTitle):
                                        if (ptitle != xLocalization.xKI.xImageInitialTitle):
                                            ptitle = ptitle[len(xLocalization.xKI.xImageInitialTitle):]
                                    ed_element.imageSetTitle(ptitle)
                                ed_element.save()
                        elif (BKEditField == kBKEditFieldJRNNote):
                            buf = textbox.getEncodedBuffer()
                            if (buf[:len(xLocalization.xKI.xJournalInitialMessage)] == xLocalization.xKI.xJournalInitialMessage):
                                buf = buf[len(xLocalization.xKI.xJournalInitialMessage):]
                            ed_element = ed_element.upcastToTextNoteNode()
                            ed_element.noteSetText(str(buf))
                            ed_element.save()
                if (BKEditField != kBKEditFieldJRNNote):
                    textbox.show()
                    button.show()
                    editbox.hide()
            BKInEditMode = 0
            BKEditContent = None
            BKEditField = -1



    def IBigKICheckFocusChange(self):
        if BKInEditMode:
            if (BKEditField == kBKEditFieldJRNTitle):
                editbox = ptGUIControlEditBox(KIJournalExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDeditbox]))
            elif (BKEditField == kBKEditFieldPICTitle):
                editbox = ptGUIControlEditBox(KIPictureExpanded.dialog.getControlFromTag(BKEditFieldIDs[BKEditField][kBKEditIDeditbox]))
            else:
                editbox = None
            if (type(editbox) != type(None)):
                if editbox.isFocused():
                    return
            self.IBigKISaveEdit()



    def IBigKISetSeen(self, content):
        if BigKI.dialog.isEnabled():
            content.setSeen()



    def ISetPlayerNotFound(self, message):
        global BKPlayerSelected
        BKPlayerSelected = None
        sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
        sendToField.setString((('<' + message) + '>'))
        sendToButton = ptGUIControlButton(BigKI.dialog.getControlFromTag(kBKIToPlayerButton))
        sendToButton.hide()



    def ICheckContentForSender(self, content):
        global BKPlayerSelected
        folder = content.getParent()
        if folder:
            folder = folder.upcastToFolderNode()
        if ((type(folder) != type(None)) and (folder.folderGetType() == PtVaultStandardNodes.kInboxFolder)):
            sender = content.getSaver()
            if ((type(sender) != type(None)) and (sender.getType() == PtVaultNodeTypes.kPlayerInfoNode)):
                sendToField = ptGUIControlTextBox(BigKI.dialog.getControlFromTag(kBKIPlayerLine))
                BKPlayerSelected = sender
                sendToField.setString(sender.playerGetName())



    def IInviteToVisit(self, playerID, ageInfo):
        whereToLink = ptAgeLinkStruct()
        whereToLink.setAgeInfo(ageInfo.asAgeInfoStruct())
        ptVault().invitePlayerToAge(whereToLink, playerID)
        self.ISendInviteRevoke(playerID, ageInfo.getDisplayName(), xLocalization.xKI.xInviteVisitTitle, xLocalization.xKI.xInviteVisitBody)



    def IRevokeToVisit(self, playerID, ageInfo):
        ptVault().unInvitePlayerToAge(ageInfo.getAgeInstanceGuid(), playerID)



    def ISendInviteRevoke(self, playerID, ageName, title, message):
##############################################################################
# Alcugs invite deficiency workaround
##############################################################################
        global InviteInProgress
        global InviteRecipient
        global InviteParentNode
        global InviteTryCount
##############################################################################
# End Alcugs invite deficiency workaround
##############################################################################
        localPlayer = PtGetLocalPlayer()
##############################################################################
# D'Lanor's Alcugs text note fix
##############################################################################
        try:
            invite = ptVaultTextNoteNode(PtVaultNodePermissionFlags.kDefaultPermissions)
        except:
            invite = ptVaultTextNoteNode()
##############################################################################
# End D'Lanor's Alcugs text note fix
##############################################################################
        invite.noteSetText((message % (ageName, localPlayer.getPlayerName())))
        invite.noteSetTitle((title % ageName))
##############################################################################
# Alcugs invite deficiency workaround
##############################################################################
#        invite.sendTo(playerID)
        journal = BKJournalFolderDict[self.IGetAgeInstanceName()]
        if (type(journal) != type(None)):
            ref = journal.addNode(invite)
            # this works fine when you do it slowly enough, but...
            # when coded like this, the invite is not received by the
            # recipient nor deleted from the sender's journal; this is
            # a deficiency in the vault server
            #node = ref.getChild()
            #node.sendTo(playerID)
            #journal.removeNode(node)
            InviteInProgress = invite
            InviteRecipient = playerID
            InviteParentNode = journal
            InviteTryCount = 0
            PtAtTimeCallback(self.key, 0.5, kInviteFinish)
##############################################################################
# End Alcugs invite deficiency workaround
##############################################################################



    def IShowSelectedConfig(self):
        if (BKConfigListOrder[BKFolderSelected] == xLocalization.xKI.xKIConfiguration):
            self.IBigKIChangeMode(kBKKIExpanded)
        elif (BKConfigListOrder[BKFolderSelected] == xLocalization.xKI.xVolumeConfiguration):
            self.IBigKIChangeMode(kBKVolumeExpanded)
        elif (BKRightSideMode != kBKAgeOwnerExpanded):
            self.IBigKIChangeMode(kBKAgeOwnerExpanded)
        else:
            self.IRefreshAgeOwnerSettings()
            self.IBigKIOnlySelectedToButtons()



    def ISaveUserNameFromEdit(self, control):
        newtitle = ''
        try:
            myAge = BKConfigFolderDict[BKConfigListOrder[BKFolderSelected]]
            if (not control.wasEscaped()):
                myAge.setAgeUserDefinedName(control.getString())
                myAge.save()
                PtDebugPrint(('KIAgeOwner: updating title to: %s' % control.getString()), level=kDebugDumpLevel)
            else:
                PtDebugPrint('KIAgeOwner: escape hit!', level=kDebugDumpLevel)
            newtitle = myAge.getDisplayName()
        except LookupError:
            PtDebugPrint("KIAgeOwner: where's the stinking age!", level=kDebugDumpLevel)
            myAge = None
        control.hide()
        title = ptGUIControlTextBox(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleTB))
        title.setString(newtitle)
        title.show()
        titlebtn = ptGUIControlButton(KIAgeOwnerExpanded.dialog.getControlFromTag(kBKAgeOwnerTitleBtn))
        titlebtn.enable()



    def ISaveMarkerFolderNameFromEdit(self, control):
        title = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTitleText))
        if (type(BKCurrentContent) != type(None)):
            element = BKCurrentContent.getChild()
            if (type(element) != type(None)):
                datatype = element.getType()
                if (datatype == PtVaultNodeTypes.kMarkerListNode):
                    element = element.upcastToMarkerListNode()
                    if (type(element) != type(None)):
                        if ((not control.wasEscaped()) and (control.getString() != '')):
                            element.folderSetName(control.getString())
                            title.setString(control.getString())
                            element.save()
                            PtDebugPrint(('KIAgeOwner: updating title to: %s' % control.getString()), level=kDebugDumpLevel)
                            self.IRefreshPlayerList()
                            self.IRefreshPlayerListDisplay()
                        else:
                            PtDebugPrint('KIAgeOwner: escape hit!', level=kDebugDumpLevel)
        control.hide()
        titlebtn = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderTitleBtn))
        titlebtn.enable()
        title.show()



    def ISaveMarkerTextFromEdit(self, control):
        title = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerTextTB))
        if (type(BKCurrentContent) != type(None)):
            element = BKCurrentContent.getChild()
            if (type(element) != type(None)):
                datatype = element.getType()
                if (datatype == PtVaultNodeTypes.kMarkerListNode):
                    element = element.upcastToMarkerListNode()
                    if (type(element) != type(None)):
                        if ((not control.wasEscaped()) and (control.getString() != '')):
                            selID = ptMarkerMgr().getSelectedMarker()
                            markerRefs = element.getChildNodeRefList()
                            for markerRef in markerRefs:
                                marker = markerRef.getChild()
                                if marker:
                                    marker = marker.upcastToMarkerNode()
                                    if marker:
                                        PtDebugPrint(('\txKI:Marker: is it marker %d?' % marker.getID()), level=kDebugDumpLevel)
                                        if (marker.getID() == selID):
                                            marker.markerSetText(control.getString())
                                            title.setString(control.getString())
                                            marker.save()

                        else:
                            PtDebugPrint('KImarkerText: escape hit!', level=kDebugDumpLevel)
        control.hide()
        titlebtn = ptGUIControlTextBox(KIMarkerFolderExpanded.dialog.getControlFromTag(kMarkerFolderMarkerTextBtn))
        titlebtn.enable()
        title.show()



    def ICheckInboxForUnseen(self):
        vault = ptVault()
        infolder = vault.getInbox()
        if (type(infolder) != type(None)):
            inreflist = infolder.getChildNodeRefList()
            for inref in inreflist:
                if (not inref.beenSeen()):
                    self.IAlertKIStart()




    def IAlertKIStart(self):
        global AlertTimeToUse
        if (not PtIsSinglePlayerMode()):
            if (theKILevel >= kNormalKI):
                if (not AlertTimerActive):
                    PtDebugPrint('xKI: show KI alert', level=kDebugDumpLevel)
                    NewItemAlert.dialog.show()
                kialert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertKIAlert))
                AlertTimeToUse = kAlertTimeDefault
                kialert.show()



    def IAlertBookStart(self, time = kAlertTimeDefault):
        global AlertTimeToUse
        if (not AlertTimerActive):
            PtDebugPrint('xKI: show Book alert', level=kDebugDumpLevel)
            NewItemAlert.dialog.show()
        bookalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertBookAlert))
        AlertTimeToUse = time
        bookalert.show()



    def IAlertJournalStart(self, time = kAlertTimeDefault):
        global AlertTimeToUse
        if (not AlertTimerActive):
            PtDebugPrint('xKI: show Journal alert', level=kDebugDumpLevel)
            NewItemAlert.dialog.show()
#        if (theKILevel == kMicroKI):
#            journalalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertMicroJournalAlert))
#        else:
#            journalalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertJournalAlert))
        journalalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertJournalAlert))
        microjournalalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertMicroJournalAlert))
        AlertTimeToUse = time
        journalalert.show()
        microjournalalert.hide()



    def IAlertStop(self):
        global AlertTimerActive
        AlertTimerActive = 0
        NewItemAlert.dialog.hide()
        kialert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertKIAlert))
        kialert.hide()
        bookalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertBookAlert))
        bookalert.hide()
        journalalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertJournalAlert))
        journalalert.hide()
        microjournalalert = ptGUIControlButton(NewItemAlert.dialog.getControlFromTag(kAlertMicroJournalAlert))
        microjournalalert.hide()



    def IAlertStartTimer(self):
        global AlertTimerActive
        if (not AlertTimerActive):
            AlertTimerActive = 1
            PtAtTimeCallback(self.key, AlertTimeToUse, kAlertHideTimer)



class kiFolder:


    def __init__(self, foldertype):
        self.type = foldertype
        self.name = xLocalization.FolderIDToFolderName(self.type)



class Device:


    def __init__(self, name):
        try:
            idx = name.index('/type=')
            self.type = name[(idx + len('/type=')):]
            name = name[:idx]
        except (LookupError, ValueError):
            self.type = 'imager'
        self.name = name


    def __eq__(self, other):
        if (self.name == other.name):
            return 1
        else:
            return 0


    def __ne__(self, other):
        if (self.name == other.name):
            return 0
        else:
            return 1


class DeviceFolder:


    def __init__(self, name):
        self.name = name
        self.dflist = []



    def __getitem__(self, key):
        return self.dflist[key]



    def __setitem__(self, key, value):
        self.dflist[key] = value



    def append(self, value):
        self.dflist.append(value)



    def remove(self, value):
        self.dflist.remove(value)



    def removeAll(self):
        self.dflist = []



    def index(self, value):
        return self.dflist.index(value)



    def __getslice__(self, i, j):
        return self.self.dflist[i:j]



    def __len__(self):
        return len(self.dflist)



class SeparatorFolder:


    def __init__(self, name):
        self.name = name



class ChatFlags:


    def __init__(self, flags):
        self.__dict__['flags'] = flags
        self.__dict__['broadcast'] = 1
        self.__dict__['toSelf'] = 0
        if (flags & kRTChatPrivate):
            self.__dict__['private'] = 1
            self.__dict__['broadcast'] = 0
        else:
            self.__dict__['private'] = 0
        if (flags & kRTChatAdmin):
            self.__dict__['admin'] = 1
        else:
            self.__dict__['admin'] = 0
        if (flags & kRTChatInterAge):
            self.__dict__['interAge'] = 1
        else:
            self.__dict__['interAge'] = 0
        if (flags & kRTChatStatusMsg):
            self.__dict__['status'] = 1
        else:
            self.__dict__['status'] = 0
        if (flags & kRTChatNeighborsMsg):
            self.__dict__['neighbors'] = 1
        else:
            self.__dict__['neighbors'] = 0
        self.__dict__['channel'] = ((kRTChatChannelMask & flags) / 256)



    def __setattr__(self, name, value):
        if (name == 'broadcast'):
            if value:
                self.__dict__['flags'] &= (kRTChatFlagMask ^ kRTChatPrivate)
        elif (name == 'private'):
            self.__dict__['flags'] &= (kRTChatFlagMask ^ kRTChatPrivate)
            if value:
                self.__dict__['flags'] |= kRTChatPrivate
                self.__dict__['broadcast'] = 0
            else:
                self.__dict__['broadcast'] = 1
        elif (name == 'admin'):
            self.__dict__['flags'] &= (kRTChatFlagMask ^ kRTChatAdmin)
            if value:
                self.__dict__['flags'] |= kRTChatAdmin
        elif (name == 'interAge'):
            self.__dict__['flags'] &= (kRTChatFlagMask ^ kRTChatInterAge)
            if value:
                self.__dict__['flags'] |= kRTChatInterAge
        elif (name == 'status'):
            self.__dict__['flags'] &= (kRTChatFlagMask ^ kRTChatStatusMsg)
            if value:
                self.__dict__['flags'] |= kRTChatStatusMsg
        elif (name == 'neighbors'):
            self.__dict__['flags'] &= (kRTChatFlagMask ^ kRTChatNeighborsMsg)
            if value:
                self.__dict__['flags'] |= kRTChatNeighborsMsg
        elif (name == 'channel'):
            flagsNoChannel = (self.__dict__['flags'] & kRTChatNoChannel)
            self.__dict__['flags'] = (flagsNoChannel + (value * 256))
        self.__dict__[name] = value



    def __repr__(self):
        str = 'ChatFlag: '
        if self.toSelf:
            str += 'toSelf '
        if self.broadcast:
            str += 'broadcast '
        if self.private:
            str += 'private '
        if self.admin:
            str += 'admin '
        if self.interAge:
            str += 'interAge '
        if self.status:
            str += 'status '
        if self.neighbors:
            str += 'neighbors '
        str += ('channel=%d ' % self.channel)
        str += ('flags=%x' % self.flags)
        return str



class MarkerPlayer:


    def __init__(self, playerID, joined = 0):
        self.ID = playerID
        dpl = PtGetPlayerListDistanceSorted()
        self.player = None
        self.isUs = 0
        self.team = PtMarkerMsgTeam.kNoTeam
        for plyr in dpl:
            if (plyr.getPlayerID() == playerID):
                self.player = ptPlayer(plyr.getPlayerName(), plyr.getPlayerID())
                break

        if (type(self.player) == type(None)):
            us = PtGetLocalPlayer()
            if (us.getPlayerID() == playerID):
                self.player = us
                self.isUs = 1
        if (type(self.player) == type(None)):
            self.player = ptPlayer(('?UNKNOWN?ID:[%d]' % self.playerID), self.playerID)
        self.isJoined = joined
        self.score = 0
        self.scoreText = ''



    def updateScore(self):
        if (type(self.player) != type(None)):
            if (MarkerGameState == kMGGameOn):
                self.scoreText = ('(%d)' % self.score)
            else:
                self.scoreText = ''



class MarkerGame:


    def __init__(self, masterID, name = None):
        self.masterID = masterID
        self.gameName = name
        dpl = PtGetPlayerListDistanceSorted()
        self.master = None
        self.time = 0
        self.gameTimerOn = 0
        self.timeLeftDPL = None
        self.gameType = PtMarkerMsgGameType.kGameTypeCapture
        self.numberMarkers = 0
        self.markersRemaining = 0
        self.markersRemainingDPL = None
        self.invitedPlayers = []
        self.greenTeamPlayers = []
        self.greenTeamScore = 0
        self.greenTeamDPL = None
        self.redTeamPlayers = []
        self.redTeamScore = 0
        self.redTeamDPL = None
        self.master = MarkerPlayer(masterID)
        if (type(self.master.player) == type(None)):
            self.master.player = ptPlayer(('?UNKNOWN?ID:[%d]' % self.masterID), self.masterID)
        if (type(self.gameName) == type(None)):
            self.gameName = ("%s's MarkerGame" % self.master.player.getPlayerName())



    def setGame(self, time, type, markers):
        self.setTime(time)
        self.gameType = type
        self.numberMarkers = markers
        self.markersRemaining = markers



    def updateScores(self):
        self.greenTeamScore = 0
        for gplyr in self.greenTeamPlayers:
            self.greenTeamScore += gplyr.score

        self.redTeamScore = 0
        for rplyr in self.redTeamPlayers:
            self.redTeamScore += rplyr.score

        self.markersRemaining = (self.numberMarkers - (self.greenTeamScore + self.redTeamScore))



    def resetScores(self):
        self.greenTeamScore = 0
        for gplyr in self.greenTeamPlayers:
            gplyr.score = 0

        self.redTeamScore = 0
        for rplyr in self.redTeamPlayers:
            rplyr.score = 0

        self.markersRemaining = self.numberMarkers



    def setTime(self, time):
        self.time = time
        self.gameTimerOn = 0



    def startTimer(self):
        self.gameTimerOn = 1
        self.endTime = (PtGetTime() + self.time)



    def timeLeft(self):
        if self.gameTimerOn:
            if (PtGetTime() > self.endTime):
                return 0
            return int((self.endTime - PtGetTime()))
        else:
            return self.time



    def addPlayerToTeam(self, playerID, teamType):
        if (teamType == PtMarkerMsgTeam.kGreenTeam):
            teamplayers = self.greenTeamPlayers
        else:
            teamplayers = self.redTeamPlayers
        found = 0
        for mplayer in teamplayers:
            if (mplayer.player.getPlayerID() == playerID):
                mplayer.isJoined = 1
                mplayer.score = 0
                mplayer.team = teamType
                found = 1
                break

        if (not found):
            mgplayer = MarkerPlayer(playerID, joined=1)
            mgplayer.team = teamType
            teamplayers.append(mgplayer)


    def addToDPLWorking(self, DPList):
        pass


    def addToDPLPlaying(self, DPList):
        DPList.append(CurrentPlayingMarkerGame)
        if (MarkerGameState == kMGGameOn):
            gametime = self.timeLeft()
            self.timeLeftDPL = DPLStatusLine((xLocalization.xKI.xTimeRemainingText % (int((gametime / 60)), (gametime % 60))), AgenBlueDk)
        else:
            self.timeLeftDPL = DPLStatusLine(xLocalization.xKI.xWaitingForStartText, AgenBlueDk)
        if (self.gameType == PtMarkerMsgGameType.kGameTypeCapture):
            self.markersRemainingDPL = DPLStatusLine((xLocalization.xKI.xMarkerGameMarkersRemaining % self.markersRemaining), AgenBlueDk)
        else:
            self.markersRemainingDPL = DPLStatusLine((xLocalization.xKI.xMarkerGameMarkersUnclaimed % self.markersRemaining), AgenBlueDk)
        self.greenTeamDPL = DPLBranchStatusLine((xLocalization.xKI.xMarkerGameGreenTeamScore % self.greenTeamScore))
        self.redTeamDPL = DPLBranchStatusLine((xLocalization.xKI.xMarkerGameRedTeamScore % self.redTeamScore), closePrev=1)
        DPList.append(self.timeLeftDPL)
        DPList.append(self.markersRemainingDPL)
        DPList.append(self.greenTeamDPL)
        DPList += CurrentPlayingMarkerGame.greenTeamPlayers
        DPList.append(self.redTeamDPL)
        DPList += CurrentPlayingMarkerGame.redTeamPlayers


    def updateGameTime(self):
        if (type(self.timeLeftDPL) != type(None)):
            if (MarkerGameState == kMGGameOn):
                gametime = self.timeLeft()
                self.timeLeftDPL.updateText((xLocalization.xKI.xTimeRemainingText % (int((gametime / 60)), (gametime % 60))))
            else:
                self.timeLeftDPL.updateText(xLocalization.xKI.xWaitingForStartText)



class DPLStatusLine:
    def __init__(self, text, color = None):
        self.text = text
        self.color = color
        self.position = -1


    def updateText(self, newText):
        self.text = newText
        self.update()


    def update(self):
        if (self.position != -1):
            playerlist = ptGUIControlListBox(KIMini.dialog.getControlFromTag(kPlayerList))
            playerlist.setElement(self.position, self.text)
            playerlist.refresh()



class DPLBranchStatusLine(DPLStatusLine,):
    def __init__(self, text, closePrev = 0):
        DPLStatusLine.__init__(self, text)
        self.closePrev = closePrev



class QuestionNote:
    kNotDefined = 0
    kMarkerGameJoin = 1

    def __init__(self, type = kNotDefined, title = 'Question:', msg = '', yesBtn = xLocalization.xKI.xYesNoAcceptButton, noBtn = xLocalization.xKI.xYesNoDeclineButton):
        self.type = type
        self.title = title
        self.message = msg
        self.YesBtnText = yesBtn
        self.NoBtnText = noBtn



    def YesAction(self):
        return



    def NoAction(self):
        return



class MarkerGameJoinQuestion(QuestionNote):
    def __init__(self, gameMasterID, roundLength, gameType, numberMarkers):
        self.game = MarkerGame(gameMasterID)
        self.game.setGame(roundLength, gameType, numberMarkers)
        QuestionNote.__init__(self, type=QuestionNote.kMarkerGameJoin)
        masterName = self.game.master.player.getPlayerName()
        if (gameType == PtMarkerMsgGameType.kGameTypeCapture):
            gameName = xLocalization.xKI.xMarkerGameNameCapture
            ses = 's'
            if (int((self.game.time / 60)) == 1):
                ses = ''
            if (self.game.numberMarkers == 0):
                instruct = xLocalization.xKI.xMarkerGameInstructCapNoMarker
            elif (self.game.numberMarkers == 1):
                instruct = (xLocalization.xKI.xMarkerGameInstructCapOneMarker % (int((self.game.time / 60)), ses))
            else:
                instruct = (xLocalization.xKI.xMarkerGameInstructCapNMarkers % (self.game.numberMarkers, int((self.game.time / 60)), ses))
        elif (gameType == PtMarkerMsgGameType.kGameTypeHold):
            gameName = xLocalization.xKI.xMarkerGameNameHold
            ses = 's'
            if (int((self.game.time / 60)) == 1):
                ses = ''
            if (self.game.numberMarkers == 0):
                instruct = xLocalization.xKI.xMarkerGameInstructHoldNoMarker
            else:
                instruct = (xLocalization.xKI.xMarkerGameInstructHoldNMarkers % (self.game.numberMarkers, int((self.game.time / 60)), ses))
        elif (gameType == PtMarkerMsgGameType.kGameTypeQuest):
            gameName = xLocalization.xKI.xMarkerGameNameQuest
            instruct = xLocalization.xKI.xMarkerGameInstructQuest
        else:
            gameName = xLocalization.xKI.xMarkerGameNameUnknown
            instruct = ''
        self.title = (xLocalization.xKI.xMarkerGameQTitle % masterName)
        self.message = (xLocalization.xKI.xMarkerGameQMessage % (masterName, gameName, instruct))


    def YesAction(self):
        global MarkerGameState
        global CurrentPlayingMarkerGame
        ptMarkerMgr().joinGame(self.game.masterID, PtMarkerMsgTeam.kNoTeam)
        MarkerGameState = kMGGameCreation
        CurrentPlayingMarkerGame = self.game
        MarkerJoinRequests.remove(self)



    def NoAction(self):
        MarkerJoinRequests.remove(self)


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



