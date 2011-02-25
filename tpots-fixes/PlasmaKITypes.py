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
kEnterChatMode = 1
kSetChatFadeDelay = 2
kSetTextChatAdminMode = 3
kDisableKIandBB = 4
kEnableKIandBB = 5
kYesNoDialog = 6
kAddPlayerDevice = 7
kRemovePlayerDevice = 8
kUpgradeKILevel = 9
kDowngradeKILevel = 10
kRateIt = 11
kSetPrivateChatChannel = 12
kUnsetPrivateChatChannel = 13
kStartBookAlert = 14
kMiniBigKIToggle = 15
kKIPutAway = 16
kChatAreaPageUp = 17
kChatAreaPageDown = 18
kChatAreaGoToBegin = 19
kChatAreaGoToEnd = 20
kKITakePicture = 21
kKICreateJournalNote = 22
kKIToggleFade = 23
kKIToggleFadeEnable = 24
kKIChatStatusMsg = 25
kKILocalChatStatusMsg = 26
kKIUpSizeFont = 27
kKIDownSizeFont = 28
kKIOpenYeehsaBook = 29
kKIOpenKI = 30
kKIShowCCRHelp = 31
kKICreateMarker = 32
kKICreateMarkerFolder = 33
kKILocalChatErrorMsg = 34
kKIPhasedAllOn = 35
kKIPhasedAllOff = 36
kKIOKDialog = 37
kDisableYeeshaBook = 38
kEnableYeeshaBook = 39
kQuitDialog = 40
kTempDisableKIandBB = 41
kTempEnableKIandBB = 42
kDisableEntireYeeshaBook = 43
kEnableEntireYeeshaBook = 44
kKIOKDialogNoQuit = 45
kGZUpdated = 46
kGZInRange = 47
kGZOutRange = 48
kUpgradeKIMarkerLevel = 49
kKIShowMiniKI = 50
kGZFlashUpdate = 51
kStartJournalAlert = 52
kAddJournalBook = 53
kRemoveJournalBook = 54
kKIOpenJournalBook = 55
# Ahnonay Sphere 4 work-around BEGIN
kKISitOnNextLinkOut = 100
# Ahnonay Sphere 4 work-around END
kNanoKI = 0
kMicroKI = 1
kNormalKI = 2
kLowestKILevel = kNanoKI
kHighestKILevel = kNormalKI
kKIMarkerNotUpgraded = 0
kKIMarkerFirstLevel = 1
kKIMarkerSecondLevel = 2
kKIMarkerNormalLevel = 3
kGZMarkerInactive = '0'
kGZMarkerAvailable = '1'
kGZMarkerCaptured = '2'
kGZMarkerUploaded = '3'
kCGZMarkerInactive = '0'
kCGZMarkerAvailable = '1'
kCGZMarkerCaptured = '2'
kCGZMarkerUploaded = '3'
gCGZAllStates = [kCGZMarkerInactive, kCGZMarkerAvailable, kCGZMarkerCaptured, kCGZMarkerUploaded]
kCGZFirstGame = 0
kCGZFinalGame = 3
kCGZToransGame = 0
kCGZHSpansGame = 1
kCGZVSpansGame = 2
kCGZActivateGZ = 3
kChronicleKILevel = 'PlayerKILevel'
kChronicleKILevelType = 2
kChronicleCensorLevel = 'PlayerCensorLevel'
kChronicleCensorLevelType = 2
kChronicleKIMarkerLevel = 'KIMarkerLevel'
kChronicleKIMarkerLevelType = 2
kChronicleGZGames = 'GZGames'
kChronicleGZGamesType = 1
kChronicleGZMarkersAquired = 'GZMarkersAquired'
kChronicleGZMarkersAquiredType = 1
kChronicleCalGZMarkersAquired = 'CalGZMarkers'
kChronicleCalGZMarkersAquiredType = 1

def PtDetermineKILevel():
    import Plasma
    import string
    vault = Plasma.ptVault()
    entry = vault.findChronicleEntry(kChronicleKILevel)
    if (type(entry) != type(None)):
        level = string.atoi(entry.chronicleGetValue())
        if ((level >= kLowestKILevel) and (level <= kHighestKILevel)):
            return level
    return kNanoKI


def PtDetermineCensorLevel():
    import Plasma
    import string
    vault = Plasma.ptVault()
    entry = vault.findChronicleEntry(kChronicleCensorLevel)
    if (type(entry) != type(None)):
        level = string.atoi(entry.chronicleGetValue())
        return level
    return 0


def PtDetermineKIMarkerLevel():
    import Plasma
    import string
    vault = Plasma.ptVault()
    entry = vault.findChronicleEntry(kChronicleKIMarkerLevel)
    if (type(entry) != type(None)):
        level = string.atoi(entry.chronicleGetValue())
        return level
    return kKIMarkerNotUpgraded


def PtGetCGZGameState(whichGame):
    import Plasma
    import PlasmaTypes
    if ((whichGame >= kCGZFirstGame) and (whichGame <= kCGZFinalGame)):
        vault = Plasma.ptVault()
        entry = vault.findChronicleEntry(kChronicleCalGZMarkersAquired)
        if (type(entry) != type(None)):
            allStates = entry.chronicleGetValue()
            PlasmaTypes.PtDebugPrint(('PlasmaKITypes:PtGetCGZGameLevel current chronicle is %s' % allStates), level=PlasmaTypes.kDebugDumpLevel)
            state = kCGZMarkerInactive
            try:
                state = allStates[whichGame]
            except LookupError:
                PlasmaTypes.PtDebugPrint(('PlasmaKITypes:PtGetCGZGameLevel - CGZ marker game not there? chron=%s' % allStates), level=PlasmaTypes.kErrorLevel)
            return state
        else:
            PlasmaTypes.PtDebugPrint('PlasmaKITypes:PtGetCGZGameLevel no chronicle yet', level=PlasmaTypes.kDebugDumpLevel)
    else:
        PlasmaTypes.PtDebugPrint(('PlasmaKITypes:PtGetCGZGameLevel - invalid CGZ game of %d' % whichGame), level=PlasmaTypes.kErrorLevel)
    return kCGZMarkerInactive


def PtSetCGZGameState(whichGame, state):
    import Plasma
    import PlasmaTypes
    if ((whichGame >= kCGZFirstGame) and (whichGame <= kCGZFinalGame)):
        if ((type(state) == type('')) and (state in gCGZAllStates)):
            PlasmaTypes.PtDebugPrint(('PlasmaKITypes:PtSetCGZGameLevel - setting game %d to %s' % (whichGame, state)), level=PlasmaTypes.kDebugDumpLevel)
            vault = Plasma.ptVault()
            entry = vault.findChronicleEntry(kChronicleCalGZMarkersAquired)
            if (type(entry) != type(None)):
                allStates = entry.chronicleGetValue()
                newStates = ''
                for idx in range((kCGZFinalGame + 1)):
                    if (idx == whichGame):
                        newStates += state
                    else:
                        try:
                            newStates += allStates[idx]
                        except LookupError:
                            newStates += kCGZMarkerInactive
                newStates += allStates[(kCGZFinalGame + 1):]
                entry.chronicleSetValue(newStates)
                entry.save()
            else:
                newStates = ''
                for idx in range((kCGZFinalGame + 1)):
                    if (idx == whichGame):
                        newStates += state
                    else:
                        newStates += kCGZMarkerInactive
                vault.addChronicleEntry(kChronicleCalGZMarkersAquired, kChronicleCalGZMarkersAquiredType, newStates)
        else:
            PlasmaTypes.PtDebugPrint('PlasmaKITypes:PtSetCGZGameLevel - invalid CGZ game state of:', state, level=PlasmaTypes.kErrorLevel)
    else:
        PlasmaTypes.PtDebugPrint(('PlasmaKITypes:PtSetCGZGameLevel - invalid CGZ game of %d' % whichGame), level=PlasmaTypes.kErrorLevel)


def PtWhichCGZPlaying():
    import Plasma
    whichGame = -1
    state = kCGZMarkerInactive
    vault = Plasma.ptVault()
    entry = vault.findChronicleEntry(kChronicleCalGZMarkersAquired)
    if (type(entry) != type(None)):
        allStates = entry.chronicleGetValue()
        if (len(allStates) > kCGZFinalGame):
            state = kCGZMarkerUploaded
            for i in range((kCGZFinalGame + 1)):
                if ((allStates[i] == kCGZMarkerAvailable) or (allStates[i] == kCGZMarkerCaptured)):
                    whichGame = i
                    state = allStates[i]
                    break
                if (allStates[i] != kCGZMarkerUploaded):
                    state = kCGZMarkerInactive
    return (whichGame, state)


def PtIsCGZDone():
    import Plasma
    isDone = 0
    vault = Plasma.ptVault()
    entry = vault.findChronicleEntry(kChronicleCalGZMarkersAquired)
    if (type(entry) != type(None)):
        allStates = entry.chronicleGetValue()
        if (len(allStates) > kCGZFinalGame):
            isDone = 1
            for i in range((kCGZFinalGame + 1)):
                if (allStates[i] != kCGZMarkerUploaded):
                    isDone = 0
                    break
    return isDone


def PtDetermineGZ():
    import Plasma
    import PlasmaTypes
    import string
    GZPlaying = 0
    MarkerToGetColor = 'off'
    MarkerGottenColor = 'off'
    MarkerToGetNumber = 0
    MarkerGottenNumber = 0
    KIMarkerLevel = PtDetermineKIMarkerLevel()
    if (KIMarkerLevel > kKIMarkerNotUpgraded):
        (whichGame, state) = PtWhichCGZPlaying()
        if ((KIMarkerLevel < kKIMarkerNormalLevel) or ((KIMarkerLevel == kKIMarkerNormalLevel) and (whichGame != -1))):
            vault = Plasma.ptVault()
            entry = vault.findChronicleEntry(kChronicleGZGames)
            if (type(entry) != type(None)):
                gameString = entry.chronicleGetValue()
                PlasmaTypes.PtDebugPrint(('PtDetermineGZ: - game string is %s' % gameString), level=PlasmaTypes.kDebugDumpLevel)
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
                    except ValueError:
                        PlasmaTypes.PtDebugPrint('xKI:GZ - error trying to read GZGames Chronicle', level=PlasmaTypes.kErrorLevel)
                        GZPlaying = 0
                        MarkerToGetColor = 'off'
                        MarkerGottenColor = 'off'
                        MarkerToGetNumber = 0
                        MarkerGottenNumber = 0
                else:
                    PlasmaTypes.PtDebugPrint('xKI:GZ - error GZGames string formation error', level=PlasmaTypes.kErrorLevel)
    PlasmaTypes.PtDebugPrint(('PtDetermineGZ: - returning game=%d colors=%s:%s markers=%d:%d' % (GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber)), level=PlasmaTypes.kDebugDumpLevel)
    return (GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber)


def PtCaptureGZMarker(GZMarkerInRange):
    import Plasma
    import PlasmaTypes
    (GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber) = PtDetermineGZ()
    if (GZPlaying and (MarkerToGetNumber > MarkerGottenNumber)):
        vault = Plasma.ptVault()
        entry = vault.findChronicleEntry(kChronicleGZMarkersAquired)
        if (type(entry) != type(None)):
            markers = entry.chronicleGetValue()
            markerIdx = (GZMarkerInRange - 1)
            if ((markerIdx >= 0) and (markerIdx < len(markers))):
                PlasmaTypes.PtDebugPrint(('PtCaptureGZMarker: starting with \'%s\' changing %d to \'%s\'' % (markers, GZMarkerInRange, kGZMarkerCaptured)), level=PlasmaTypes.kDebugDumpLevel)
                if ((len(markers) - (markerIdx + 1)) != 0):
                    markers = ((markers[:markerIdx] + kGZMarkerCaptured) + markers[(-((len(markers) - (markerIdx + 1)))):])
                else:
                    markers = (markers[:markerIdx] + kGZMarkerCaptured)
                entry.chronicleSetValue(markers)
                entry.save()
                totalGotten = markers.count(kGZMarkerCaptured)
                KIMarkerLevel = PtDetermineKIMarkerLevel()
                if (KIMarkerLevel > kKIMarkerFirstLevel):
                    totalGotten -= 5
                    if (totalGotten < 0):
                        totalGotten = 0
                if (totalGotten > MarkerToGetNumber):
                    totalGotten = MarkerToGetNumber
                MarkerGottenNumber = totalGotten
                PtUpdateGZGamesChonicles(GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber)
            else:
                PlasmaTypes.PtDebugPrint(('PtCaptureGZMarker: invalid marker serial number of %d' % gGZMarkerInRange), level=PlasmaTypes.kErrorLevel)
        else:
            PlasmaTypes.PtDebugPrint('PtCaptureGZMarker: no chronicle entry found', level=PlasmaTypes.kErrorLevel)
    else:
        PlasmaTypes.PtDebugPrint('PtCaptureGZMarker: no game or this game is complete', level=PlasmaTypes.kErrorLevel)


def PtVerifyGZMarker():
    import Plasma
    import PlasmaTypes
    (GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber) = PtDetermineGZ()
    if GZPlaying:
        vault = Plasma.ptVault()
        entry = vault.findChronicleEntry(kChronicleGZMarkersAquired)
        if (type(entry) != type(None)):
            markers = entry.chronicleGetValue()
            totalGotten = markers.count(kGZMarkerCaptured)
            KIMarkerLevel = PtDetermineKIMarkerLevel()
            if (KIMarkerLevel > kKIMarkerFirstLevel):
                totalGotten -= 5
                if (totalGotten < 0):
                    totalGotten = 0
            if (totalGotten > MarkerToGetNumber):
                totalGotten = MarkerToGetNumber
            if (totalGotten != MarkerGottenNumber):
                PlasmaTypes.PtDebugPrint(('PtVerifyGZMarker: Error! Gotten different than real. They say=%d We say=%d' % (MarkerGottenNumber, totalGotten)), level=PlasmaTypes.kErrorLevel)
                MarkerGottenNumber = totalGotten
                PtUpdateGZGamesChonicles(GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber)
                Plasma.PtSendKIMessage(kGZUpdated, 0)
    return (GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber)


def PtUpdateGZGamesChonicles(GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber):
    import Plasma
    import PlasmaTypes
    vault = Plasma.ptVault()
    entry = vault.findChronicleEntry(kChronicleGZGames)
    try:
        upstring = ('%d %s:%s %d:%d' % (GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber))
        if (type(entry) != type(None)):
            entry.chronicleSetValue(upstring)
            entry.save()
        else:
            vault.addChronicleEntry(kChronicleGZGames, kChronicleGZGamesType, upstring)
    except TypeError:
        if (type(GZPlaying) != type(0)):
            PlasmaTypes.PtDebugPrint('PtUpdateGZGamesChronicle: GZPlaying wrong type (should be integer)', level=PlasmaTypes.kErrorLevel)
        if (type(MarkerToGetColor) != type('')):
            PlasmaTypes.PtDebugPrint('PtUpdateGZGamesChronicle: GZPlaying wrong type (should be string)', level=PlasmaTypes.kErrorLevel)
        if (type(MarkerGottenColor) != type('')):
            PlasmaTypes.PtDebugPrint('PtUpdateGZGamesChronicle: GZPlaying wrong type (should be string)', level=PlasmaTypes.kErrorLevel)
        if (type(MarkerToGetNumber) != type(0)):
            PlasmaTypes.PtDebugPrint('PtUpdateGZGamesChronicle: GZPlaying wrong type (should be integer)', level=PlasmaTypes.kErrorLevel)
        if (type(MarkerGottenNumber) != type(0)):
            PlasmaTypes.PtDebugPrint('PtUpdateGZGamesChronicle: GZPlaying wrong type (should be integer)', level=PlasmaTypes.kErrorLevel)

kRTChatPrivate = 1
kRTChatAdmin = 2
kRTChatPrivateAdmin = 3
kRTChatInterAge = 8
kRTChatStatusMsg = 16
kRTChatNeighborsMsg = 32
kRTChatFlagMask = 65535
kRTChatChannelMask = 65280
kRTChatNoChannel = 255
kCCRBeginCommunication = 1
kCCRChat = 2
kCCREndCommunication = 3
kCCRReturnChatMsg = 4


