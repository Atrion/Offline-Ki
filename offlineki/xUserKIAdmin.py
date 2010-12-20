# -*- coding: utf-8 -*-
import string
import os
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
from xPsnlVaultSDL import *
import xLinkMgr
import xUserKI
import xxConfig

import xUserKIData
import math

# global constant
kAutoLinkChronicle = 'OfflineKIAutoLink'

# tour variables
tourName = ''
tourInterval = 0
tourStep = 0
tourCam = {}
tourTimerActive = False


# /set data
setData = {
    'city': {
        'journeys': ['islmJourneyCloth01Vis', 'islmJourneyCloth02Vis', 'islmJourneyCloth03Vis', 'islmJourneyCloth04Vis', 'islmJourneyCloth05Vis'],
        'bahro': ['islmS1FinaleBahro'],
        'guildhall': ['islmGuildHallConstructionVis', 'islmExplosionRun'],
        'meeting': ['islmTokotahMeetingsVis'],
        'harborlights': ['islmUnderwaterHarborLightsRun'],
        'menorah': ['islmMinorahVis', 'islmMinorahNight01Vis', 'islmMinorahNight02Vis', 'islmMinorahNight03Vis', 'islmMinorahNight04Vis', 'islmMinorahNight05Vis', 'islmMinorahNight06Vis', 'islmMinorahNight07Vis', 'islmMinorahNight08Vis'],
        'lakemeter': ['islmLakeLightMeterVis'],
        'tickers': ['islmCourtyardTickerVis', 'islmLibraryTickerVis'],
        'mystvbooks': ['islmReleeshanBookVis', 'islmTodelmerBookVis'],
        'librarybooks': ['islmLibraryBannersVis', 'islmLibraryBooksVis'],
        'hoodstones': ['guildHoodStoneVis', 'seretHoodStoneVis'],
        'stage': []
    },
    'Neighborhood': {
        'webcam': ['nb01WebCamVis'],
        'thanksgiving': ['nb01ThanksgivingVis'],
        'newyear': ['nb01HappyNewYearVis', 'nb01FireworksOnFountain', 'nb01FireworksOnBanner', 'nb01FireworksOnBalcony'],
        'darkshape': ['nb01DarkShapeSwimsRun', 'nb01DarkShapeSwimsEnabled'],
        'boats': ['nb01BahroBoatsRun', 'nb01BahroBoatsEnabled'],
        'ticker': ['nb01TickerVis'],
        'gzglass': [],
        'delinglass': [],
        'tsogalglass': [],
        'heek': []
    },
    'EderDelin': {
        'winter': ['dlnWinterVis']
    },
    'GreatZero': {
        'active': ['grtzGZActive']
    },
    'GreatTreePub': {
        'bahro': ['grtpDeadBahroVis']
    },
    'BaronCityOffice': {
        'tree': ['bcoChristmasVis']
    },
    'AhnonayMOUL': {
        'sphere': []
    }
}

# loop variables
loopInterval = 0
loopCount = -1
loopCmd = ''
loopTimerActive = False


# Helper functions
def ExecPython(arg):
    exec arg


def GetCamera(ki, cameraName):
    age = PtGetAgeName()
    camera = []
    # if no name was specified, use the default one if available
    if not len(cameraName) or cameraName == 'default':
        if age in xUserKIData.CameraShortcuts and len(xUserKIData.CameraShortcuts[age]) == 1:
            for name in xUserKIData.CameraShortcuts[age]:
                camera = xUserKIData.CameraShortcuts[age][name] # there will be only one camera
                break
        else:
            ki.IDoErrorChatMessage('Can not choose default camera for this age - use "/list cameras" to see which ones are available, and specify it manually')
            return []
    # check if we got a shortcut or the camera name
    elif age in xUserKIData.CameraShortcuts:
        if cameraName in xUserKIData.CameraShortcuts[age]:
            camera = xUserKIData.CameraShortcuts[age][cameraName]
    if not len(camera):
        camera = [cameraName, cameraName+".Target"]
    # now check if that camera is valid
    try:
        PtFindSceneobject(camera[0], age)
        PtFindSceneobject(camera[1], age)
        # we are done :)
        return camera
    except:
        # one of them does not exist
        ki.IDoErrorChatMessage('Either %s or %s does not exist, so this is not a valid camera - use "/list cameras" to see which ones are available' % (camera[0], camera[1]))
        return []


def SetCamera(camera, pos):
    cameraSO = PtFindSceneobject(camera[0], PtGetAgeName())
    targetSO = PtFindSceneobject(camera[1], PtGetAgeName())
    cameraSO.netForce(1)
    cameraSO.physics.warp(ptPoint3(pos[0][0],pos[0][1],pos[0][2]))
    targetSO.netForce(1)
    targetSO.physics.warp(ptPoint3(pos[1][0],pos[1][1],pos[1][2]))


def GetObservePos(object, cameraHeight, cameraBehindAvi, targetHeight):
    avatarPos = object.position()

    # This crazy magic calculates a position which is 3+cameraBehindAvi units behind the avatar and 5.5+cameraHeight units above his feet
    # I tried doing the same doing matrix multiplication, but that's WAY slower - so I sticked with this code taken from the old AdminKI
    MatZero = -(object.right().getX())
    MatOne = -(object.view().getX())
    MatTwo = object.up().getX()
    MatFour = -(object.right().getY())
    MatFive = -(object.view().getY())
    MatSix = object.up().getY()
    MatTen = object.up().getZ()
    Yaxis = math.asin(MatTwo)
    CosY = math.cos(Yaxis)
    if (math.fabs(CosY) > 0.005):
        xpt = MatZero / CosY
        ypt = -(MatOne) / CosY
    else:
        xpt = MatFive
        ypt = MatFour
    RotZ = -(math.atan2(ypt,xpt))
    rotateMatrix = ptMatrix44()
    rotateMatrix.makeRotateMat(2,RotZ)
    zmoveMatrix = ptMatrix44()
    zmoveMatrix.makeTranslateMat(ptVector3(0,3+cameraBehindAvi,0))
    zmoveMatrix.rotate(2,RotZ)
    moveVec = zmoveMatrix.getTranslate(ptVector3(0,0,0))
    X = avatarPos.getX() + moveVec.getX()
    Y = avatarPos.getY() + moveVec.getY()
    Z = avatarPos.getZ() + moveVec.getZ() + 5.5 + cameraHeight
    posvec = ptVector3(X,Y,Z)
    rotateMatrix.translate(posvec)
    cameraPos = rotateMatrix.getTranslate(ptVector3(0,0,0))

    # the target position is just 5.5+cameraHeight+targetHeight above the avatar's feet
    targetPos = ptPoint3(avatarPos.getX(), avatarPos.getY(), avatarPos.getZ() + 5.5 + cameraHeight + targetHeight)

    # we're done :)
    return (cameraPos, targetPos)


# Callback functions
def OnLinkingOut(ki): # called by xUserKI
    # stop when linking
    global loopCmd, tourName
    loopCmd = '' 
    tourName = ''


def OnTimer(ki, id): # called by xUserKI
    if not xxConfig.hasAdminLevel(): return
    global loopInterval, loopCount, loopCmd, loopTimerActive # loop variables
    global tourName, tourInterval, tourStep, tourCam, tourTimerActive # tour variables
    if id == xUserKI.kLoopTimer:
        loopTimerActive = False
        if not len(loopCmd):
            ki.IAddRTChat(None, 'Loop stopped', 0)
            return
        if (ki.ICheckChatCommands(loopCmd.strip(), silent=True) != None):
            ki.IDoErrorChatMessage("'%s' does not seem to be a KI command" % loopCmd.strip())
        if loopCount > 0:
            loopCount = loopCount-1
        if loopCount == 0:
            ki.IAddRTChat(None, 'Loop count reached, stopped it', 0)
            return
        PtAtTimeCallback(ki.key, loopInterval, xUserKI.kLoopTimer); loopTimerActive = True
        return True
    if id == xUserKI.kAutoLinkTimer:
        autoLinkAge = xUserKI.GetChronicle(kAutoLinkChronicle, '')
        if not len(autoLinkAge): return True
        als = xUserKI.GetAgeLinkStruct(ki, autoLinkAge)
        if not als: return True
        # link us
        ki.IAddRTChat(None, 'Linking you automatically to %s (type "/autolink disable" to disable this)' % als.getAgeInfo().getAgeInstanceName(), 0)
        linkMgr = ptNetLinkingMgr()
        linkMgr.linkToAge(als)
        return True
    if id == xUserKI.kTourTimer:
        tourTimerActive = False
        if not len(tourName): return
        # preparation
        age = PtGetAgeName()
        try:
            tourList = xUserKIData.CameraTours[age][tourName]
        except:
            tourName = ''
            ki.IDoErrorChatMessage('Specified tour not found')
            return
        # let's go
        if tourStep >= len(tourList):
            ki.IAddRTChat(None, 'Tour %s has completed!' % tourName , 0)
            tourName = ''
        else:
            try:
                SetCamera(tourCam, tourList[tourStep])
                tourStep = tourStep+1
                PtAtTimeCallback(ki.key, tourInterval, xUserKI.kTourTimer); tourTimerActive = True
            except:
                ki.IDoErrorChatMessage('Could not continue tour')
                tourName = ''
        return True
    return False


def OnNewAgeLoaded(ki, firstAge):
    if firstAge:
        PtAtTimeCallback(ki.key, 2, xUserKI.kAutoLinkTimer)


# Main function
def OnCommand(ki, arg, cmnd, args, playerList, KIContent, silent):
    if not xxConfig.hasAdminLevel(): return
    global loopInterval, loopCount, loopCmd, loopTimerActive # loop variables
    global tourName, tourInterval, tourStep, tourCam, tourTimerActive # tour variables
# developer commands
    if (cmnd == 'console' or (xxConfig.isOnline() and cmnd == 'consolenet')):
        (valid, null) = xUserKI.GetArg(ki, cmnd, args, 'UruConsole command',
          lambda args: len(args) > 0)
        if not valid: return True
        if cmnd == 'consolenet':
            PtConsoleNet(arg, 1)
            if not silent: ki.IAddRTChat(None, 'UruConsoleNet: %s' % arg, 0)
        else:
            PtConsole(arg)
            if not silent: ki.IAddRTChat(None, 'UruConsole: %s' % arg, 0)
        return True
    if (cmnd == 'loadpage'):
        (valid, null) = xUserKI.GetArg(ki, cmnd, args, 'page name',
          lambda args: len(args) > 0)
        if not valid: return True
        PtPageInNode(arg)
        if not silent: ki.IAddRTChat(None, 'Loaded page %s' % arg, 0)
        return True
    if (cmnd == 'exec'):
        (valid, null) = xUserKI.GetArg(ki, cmnd, args, 'Python command',
          lambda args: len(args) > 0)
        if not valid: return True
        ExecPython(arg)
        return True
    if (cmnd == 'getchron'):
        (valid, name) = xUserKI.GetArg(ki, cmnd, args, 'chronicle name',
          lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        value = xUserKI.GetChronicle(name)
        if (value != None):
            if not silent: ki.IAddRTChat(None, '%s = %s' % (name, value), 0)
        else:
            ki.IDoErrorChatMessage("Chronicle '%s' doesn't exist." % name)
        return True
    if (cmnd == 'getversion'):
        (valid, player) = xUserKI.GetArg(ki, cmnd, args, 'player',
          lambda args: len(args) == 1, lambda args: xUserKI.GetPlayer(ki, args[0], playerList))
        if not valid or not player: return True
        if isinstance(player, ptPlayer):
            if not silent: ki.IAddRTChat(None, 'Requesting KI version from %s' % player.getPlayerName(), 0)
            xUserKI.SendRemoteCall(ki, 'getversion', [player])
        return True
    if (cmnd == 'about'):
        (valid, object) = xUserKI.GetArg(ki, cmnd, args, 'object to analyze',
          lambda args: len(args) == 1, lambda args: xUserKI.GetObject(ki, args[0], playerList, mustHaveCoord = False))
        if not valid or not object: return True
        if object.isAvatar():
            curBrainMode = object.avatar.getCurrentMode()
            if (curBrainMode == PtBrainModes.kAFK):
                avmode = 'afk'
            elif (curBrainMode == PtBrainModes.kSit):
                avmode = 'sitting'
            elif (curBrainMode == PtBrainModes.kLadder):
                avmode = 'climbing a ladder'
            elif (curBrainMode == PtBrainModes.kNonGeneric):
                avmode = 'idle'
            else:
                avmode = 'in unknown state %d' % curBrainMode
            if not silent: ki.IAddRTChat(None, '%s is an avatar and currently %s' % (xUserKI.GetObjectName(object), avmode), 0)
        else:
            if object.isLocallyOwned():
                ownstr = 'locally owned'
            else:
                ownstr = 'not locally owned'
            if not silent: ki.IAddRTChat(None, '%s is an object and %s' % (xUserKI.GetObjectName(object), ownstr), 0)
        return True
    if (cmnd == 'autolink'):
        (valid, age) = xUserKI.GetArg(ki, cmnd, args, 'age filename|disable',
          lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        if age.lower() == 'disable':
            xUserKI.SetChronicle(kAutoLinkChronicle, '')
            ki.IAddRTChat(None, 'Disabled auto-linking on startup', 0)
        else:
            # verify auto-link age
            als = xUserKI.GetAgeLinkStruct(ki, age)
            if not als: return True
            xUserKI.SetChronicle(kAutoLinkChronicle, age)
            ki.IAddRTChat(None, 'On next startup, you will be auto-linked to %s' % als.getAgeInfo().getAgeInstanceName(), 0)
        return True
# linking commands
    if (cmnd in ['link', 'linksp']):
        if cmnd == 'link':
            (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'age filename> <[list of players]',
              lambda args: len(args) >= 1, lambda args: ((args[0], None), xUserKI.GetPlayers(ki, args[1:], playerList)))
        else:
            (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'age filename> <spawn point name> <[list of players]',
              lambda args: len(args) >= 2, lambda args: ((args[0], args[1]), xUserKI.GetPlayers(ki, args[2:], playerList)))
        if not valid or not data[1]: return True
        # find out where to link
        onlyMe = len(data[1]) == 1 and data[1][0].getPlayerID() == PtGetLocalClientID()
        als = xUserKI.GetAgeLinkStruct(ki, data[0][0], data[0][1], not onlyMe) # if a player was manually specified, we need the full UUID
        if type(als) == type(None): return True
        # link the players
        linkMgr = ptNetLinkingMgr()
        linkMgr.setEnabled(1)
        for player in data[1]:
            if not silent: ki.IAddRTChat(None, 'Linking %s to %s' % (player.getPlayerName(), als.getAgeInfo().getAgeInstanceName()), 0)
            if onlyMe: linkMgr.linkToAge(als) # we have an incomplete linking struct, so we need to use this linking function
            else: linkMgr.linkPlayerToAge(als, player.getPlayerID())
        return True
    if (cmnd == 'linkto'):
        (valid, player) = xUserKI.GetArg(ki, cmnd, args, 'player',
          lambda args: len(args) == 1, lambda args: xUserKI.GetPlayer(ki, args[0], playerList))
        if not valid or not player: return True
        # link the player
        linkMgr = ptNetLinkingMgr()
        linkMgr.setEnabled(1)
        linkMgr.linkToPlayersAge(player.getPlayerID())
        if not silent: ki.IAddRTChat(None, 'Linking you to %s' % player.getPlayerName(), 0)
        return True
    if (cmnd == 'linkhere'):
        (valid, players) = xUserKI.GetArg(ki, cmnd, args, 'list of players',
          lambda args: len(args) >= 1, lambda args: xUserKI.GetPlayers(ki, args, playerList))
        if not valid or not players: return True
        # link the players
        linkMgr = ptNetLinkingMgr()
        linkMgr.setEnabled(1)
        for player in players:
            linkMgr.linkPlayerHere(player.getPlayerID()) # thanks to DarkFalkon for this line
            if not silent: ki.IAddRTChat(None, 'Linking %s to you' % player.getPlayerName(), 0)
        return True
# loop commands
    if (cmnd == 'loopstart'):
        loopCmd = ''
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'interval> <command>|<interval> <count> <command',
          lambda args: xUserKI.IsFloat(args[0]) and (args[1].startswith('/') or ( xUserKI.IsInt(args[1]) and args[2].startswith('/') )) )
        if not valid: return True
        # get data
        loopInterval = float(args[0])
        loopCount = -1
        loopCmd = string.join(args[1:], " ")
        if not args[1].startswith('/'): # due to the GetArg args[1] must be an int in this case
            loopCount = int(args[1])
            loopCmd = string.join(args[2:], " ")
        # start timer
        OnTimer(ki, xUserKI.kLoopTimer)
        return True
    if (cmnd == 'loopstop'):
        loopCmd = ''
        return True
    if (cmnd == 'm'):
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'command 1> & <command 2> & ... & <command n',
          lambda args: args[0].startswith('/') and string.join(args).find('&') >= 0)
        if not valid: return True
        commands = arg.split('&')
        for command in commands:
            if (ki.ICheckChatCommands(command.strip(), silent) != None):
                ki.IDoErrorChatMessage("'%s' does not seem to be a KI command" % command.strip())
        return True
# General age and SDL control
    if (cmnd == 'set'):
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'option to be set> <value',
          lambda args: len(args) == 2, lambda args: (args[0], int(args[1])),
          lambda args: len(args) == 1 and args[0] in ['list', 'listall'], lambda args: (args[0], -1))
        if not valid: return True
        (option, value) = data
        # get the option data
        if option == 'listall':
            ki.IAddRTChat(None, 'The following options are available: %s' % xUserKI.JoinListRec(setData), 0)
            return True
        age = PtGetAgeName()
        if not age in setData:
            ki.IDoErrorChatMessage('There\'s nothing to be set in this age. Options are available in: %s' % xUserKI.JoinList(setData))
            return True
        ageData = setData[age]
        if option == 'list':
            ki.IAddRTChat(None, 'The following options are available in this age: %s' % xUserKI.JoinList(ageData), 0)
            return True
        if not option in ageData:
            ki.IDoErrorChatMessage('There is no option called \'%s\' in this age. Use one of the following: %s' % (option, xUserKI.JoinList(ageData)))
            return True
        # apply option
        if len(ageData[option]):
            # it's a stanard boolean option
            if value not in [0, 1]:
                ki.IDoErrorChatMessage('Invalid value, allowed values are 0 and 1')
                return True
            for sdl in ageData[option]: xUserKI.SetSDL(sdl, 0, value)
        else:
            # one of the special options
            if age == 'AhnonayMOUL' and option == 'sphere':
                if value not in [1, 2, 3, 4]:
                    ki.IDoErrorChatMessage('Invalid value, allowed values are 1 to 4')
                    return True
                xUserKI.SetSDL('ahnyCurrentSphere', 0, value)
            elif age == 'city' and option == 'stage':
                if value not in [0, 1, 2]:
                    ki.IDoErrorChatMessage('Invalid value %d - must be 0 to 2' % value)
                    return True
                xUserKI.SetSDL('islmDRCStageState', 0, value)
            elif age == 'Neighborhood' and option in ['gzglass', 'delinglass', 'tsogalglass']:
                if value not in [1, 2, 3]:
                    ki.IDoErrorChatMessage('Invalid value %d - must be 1 to 3' % value)
                    return True
                values = [0, 0, 0]
                values[value-1] = 1 # everything is 0 except for the one we are speaking about
                # these are the prefices
                prefices = {'gzglass': 'nb01GZStainGlass0',
                    'delinglass': 'nb01EderDelinStainedGlass0',
                    'tsogalglass': 'nb01EderTsogalGlass0' }
                # set values
                for i in range(1, 4):
                    SDLName = '%s%dVis' % (prefices[option], i)
                    xUserKI.SetSDL(SDLName, 0, values[i-1])
            elif age == 'Neighborhood' and option == 'heek':
                if value not in [0, 1, 2, 3]:
                    ki.IDoErrorChatMessage('Invalid value %d - must be 0 to 3' % value)
                    return True
                xUserKI.SetSDL('nb01Ayhoheek5Man1State', 0, value)
            else:
                ki.IDoErrorChatMessage('Unexpected error - unknown special option %s' % option)
                return True
        if not silent: ki.IAddRTChat(None, 'Set %s to %d' % (option, value), 0)
        return True
    if (cmnd == 'listsdl'):
        (valid, grep) = xUserKI.GetArg(ki, cmnd, args, '[filter]',
          lambda args: len(args) == 0, lambda args: (''),
          lambda args: len(args) == 1, lambda args: (args[0].lower()))
        if not valid: return True
        sdl = ptAgeVault().getAgeSDL()
        vars = sdl.getVarList()
        if len(grep): vars = filter(lambda s: s.lower().find(grep) >= 0, vars)
        if len(vars) == 0:
            ki.IAddRTChat(None, 'No SDL Variable found', 0)
        else:
            ki.IAddRTChat(None, '%d SDL Variable(s) found:' % len(vars), 0)
            line = ''
            for var in vars:
                if len(line): line += ', '
                line += var
            ki.IAddRTChat(None, line, 0)
        return True
    if (cmnd == 'setsdl'):
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'SDL var name> <integer value',
          lambda args: len(args) == 2, lambda args: (args[0], int(args[1])))
        if not valid: return True
        try:
            oldval = int(xUserKI.GetSDL(data[0], 0))
            xUserKI.SetSDL(data[0], 0, data[1])
            if not silent: ki.IAddRTChat(None, 'Set SDL var %s to %d (old value: %d)' % (data[0], data[1], oldval), 0)
        except Exception, detail:
            ki.IDoErrorChatMessage('Unable to set SDL var %s: %s' % (data[0], detail))
        return True
    if (cmnd == 'getsdl'):
        (valid, name) = xUserKI.GetArg(ki, cmnd, args, 'SDL var name',
          lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        try:
            val = int(xUserKI.GetSDL(name, 0))
            if not silent: ki.IAddRTChat(None, 'SDL var %s has a value of %d' % (name, val), 0)
        except Exception, detail:
            ki.IDoErrorChatMessage('Unable to get SDL var %s: %s' % (name, detail))
        return True
    if (cmnd == 'setpsnlsdl'):
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'SDL var name> <integer value',
          lambda args: len(args) == 2, lambda args: (args[0], int(args[1])))
        if not valid: return True
        try:
            import xPsnlVaultSDL
            psnlSDL = xPsnlVaultSDL.xPsnlVaultSDL()
            oldval = psnlSDL[data[0]][0]
            psnlSDL[data[0]] = (data[1],)
            if not silent: ki.IAddRTChat(None, 'Set Personal SDL var %s to %d (old value: %d)' % (data[0], data[1], oldval), 0)
        except Exception, detail:
            ki.IDoErrorChatMessage('Unable to set Set Personal SDL var %s: %s' % (data[0], detail))
        return True
    if (cmnd == 'getpsnlsdl'):
        (valid, name) = xUserKI.GetArg(ki, cmnd, args, 'SDL var name',
          lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        try:
            import xPsnlVaultSDL
            psnlSDL = xPsnlVaultSDL.xPsnlVaultSDL()
            val = psnlSDL[name][0]
            if not silent: ki.IAddRTChat(None, 'Personal SDL var %s has a value of %d' % (name, val), 0)
        except Exception, detail:
            ki.IDoErrorChatMessage('Unable to get Set Personal SDL var %s: %s' % (name, detail))
        return True
# Bahro control
    if (cmnd == 'bahro'):
        (valid, name) = xUserKI.GetArg(ki, cmnd, args, 'bahro name',
          lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        SDLVarNames = {
            'Neighborhood': { 'shouter': 'nb01BahroPedestalShoutRun' },
            'NeighborhoodMOUL': { 'shouter': 'nb01BahroPedestalShoutRun' },
            'city': {
                '1': 'islmS1FinaleBahroCity1',
                '2': 'islmS1FinaleBahroCity2',
                '3': 'islmS1FinaleBahroCity3',
                '4': 'islmS1FinaleBahroCity4',
                '5': 'islmS1FinaleBahroCity5',
                '6': 'islmS1FinaleBahroCity6',
                'ferry': 'islmBahroShoutFerryRun',
                'library': 'islmBahroShoutLibraryRun',
                'palace': 'islmBahroShoutPalaceRun' }
        }
        age = PtGetAgeName()
        if not age in SDLVarNames:
            ki.IDoErrorChatMessage('There is no Bahro to run in this age - try the hood, Seret or the city')
            return True
        if not name in SDLVarNames[age]:
            ki.IDoErrorChatMessage('There is no such Bahro in this age. Try one of the following: %s' % xUserKI.JoinList(SDLVarNames[age]))
            return True
        xUserKI.SetSDL(SDLVarNames[age][name], 0, 1)
        if not silent: ki.IAddRTChat(None, 'Started Bahro %s' % name, 0)
        return True
# Avatar commands
    if (cmnd == 'name'):
        (valid, null) = xUserKI.GetArg(ki, cmnd, args, 'new avatar name',
          lambda args: len(args) > 0)
        if not valid: return True
        PtChangePlayerName(arg)
        if not silent: ki.IAddRTChat(None, 'You are now called %s' % arg, 0)
        return True
    if (cmnd == 'avatar'):
        (valid, avType) = xUserKI.GetArg(ki, cmnd, args, 'new avatar type',
          lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        if (avType.lower() not in ['female', 'male', 'drwatson', 'engberg', 'kodama', 'randmiller', 'sutherland', 'victor', 'yeesha', 'yeeshanoglow', 'zandi']):
            ki.IDoErrorChatMessage('%s is not a valid avatar type. Choose one of the following: Female, Male, DrWatson, Engberg, Kodama, RandMiller, Sutherland, Victor, Yeesha, YeeshaNoGlow, Zandi' % avType)
        else:
            PtChangeAvatar(avType)
            if not silent:
                ki.IAddRTChat(None, 'Your new avatar type is %s. Please note that your first person camera might act strange until you restart the game.' % avType, 0)
        return True
    if (cmnd == 'anim'):
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'animation> <[list of players]',
            lambda args: len(args) >= 1, lambda args: (args[0], xUserKI.GetPlayers(ki, args[1:], playerList, thisAgeOnly=True)))
        if not valid or not data[1]: return True
        if data[0] == 'list':
            ki.IAddRTChat(None, 'There are the following pre-defined animation sequences available: %s' % xUserKI.JoinList(xUserKIData.AnimLists), 0)
            return True
        if data[0] in xUserKIData.AnimLists:
            animLists = xUserKIData.AnimLists[data[0]]
        else:
            animLists = ([data[0]], [data[0]])
        for player in data[1]:
            objKey = PtGetAvatarKeyFromClientID(player.getPlayerID())
            object = objKey.getSceneObject()
            if not silent: ki.IAddRTChat(None, 'Trying to run %s on %s' % (data[0], xUserKI.GetObjectName(object)), 0)
            gender = object.avatar.getAvatarClothingGroup()
            if gender == 1: # female
                animList = animLists[1]
            else: # male and special characters
                animList = animLists[0]
            object.avatar.netForce(1)
            for anim in animList:
                object.avatar.oneShot(objKey, 1, 1, anim, 0, 0)
        return True
# object struct commands
    if (cmnd == 'printstruct'):
        (valid, objects) = xUserKI.GetArg(ki, cmnd, args, 'list of objects',
          lambda args: len(args) >= 1, lambda args: xUserKI.GetObjects(ki, args, playerList))
        if not valid or not objects: return True
        if silent: return True
        for object in objects:
            view = ('%f,%f,%f' % (object.view().getX(), object.view().getY(), object.view().getZ()))
            up = ('%f,%f,%f' % (object.up().getX(), object.up().getY(), object.up().getZ()))
            pos = ('%f,%f,%f' % (object.position().getX(),object.position().getY(),object.position().getZ()))
            ki.IAddRTChat(None, '[[\'%s\'],[%s],[%s],[%s]],' % (xUserKI.GetObjectName(object), view, up, pos), 0)
        return True
    if (cmnd == 'struct'):
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'name of a struct> <[struct mode]',
            lambda args: len(args) == 1, lambda args: (args[0], 'normal'),
            lambda args: len(args) == 2, lambda args: (args[0], args[1]))
        if not valid: return True
        if not data[1] in ['normal', 'here']:
            ki.IDoErrorChatMessage('There following modes are available: normal, here')
            return True
        if xUserKI.ApplyStruct(data[0], mode=data[1]):
            if not silent: ki.IAddRTChat(None, 'Built struct %s' % data[0], 0)
        else:
            ki.IDoErrorChatMessage('I could not find a struct called %s in this age - use "/list structs" to see which ones are available' % data[0])
        return True
# camera control commands
    if (cmnd == 'observe'):
        # get data
        (valid, object) = xUserKI.GetArg(ki, cmnd, args, '[object]> <[camera name]> <[offset for camera behind avatar]> <[camera height offset]> <[target height offset]',
          lambda args: len(args) == 0, lambda args: xUserKI.GetObject(ki, 'me', playerList),
          lambda args: len(args) <= 5 and (len(args) <= 4 or xUserKI.IsFloat(args[4])) and (len(args) <= 3 or xUserKI.IsFloat(args[3])) and (len(args) <= 2 or xUserKI.IsFloat(args[2])), lambda args: xUserKI.GetObject(ki, args[0], playerList))
        if not valid or not object: return True
        cameraBehindAvi = 0.0
        cameraHeight = 0.0
        targetHeight = 0.0
        cameraName = ''
        if len(args) > 1: cameraName = args[1]
        if len(args) > 2: cameraBehindAvi = float(args[2])
        if len(args) > 3: cameraHeight = float(args[3])
        if len(args) > 4: targetHeight = float(args[4])
        camera = GetCamera(ki, cameraName)
        if not len(camera): return True

        # get and set positions
        (cameraPos, targetPos) = GetObservePos(object, cameraHeight, cameraBehindAvi, targetHeight)
        SetCamera(camera, ((cameraPos.getX(), cameraPos.getY(), cameraPos.getZ()), (targetPos.getX(), targetPos.getY(), targetPos.getZ())) )

        # do the output
        if not silent: ki.IAddRTChat(None, 'The camera now observes %s' % xUserKI.GetObjectName(object), 0)
        return True
    if (cmnd == 'tour'):
        tourName = ''
        (valid, tour) = xUserKI.GetArg(ki, cmnd, args, 'tour name> <[camera name]> <[interval]',
          lambda args: len(args) >= 1 and len(args) <= 3 and (len(args) <= 2 or xUserKI.IsFloat(args[2])), lambda args: args[0])
        if not valid: return True
        interval = 5.0
        cameraName = ''
        if len(args) > 1: cameraName = args[1]
        if len(args) > 2: interval = float(args[2])
        camera = GetCamera(ki, cameraName)
        if not len(camera): return True
        # get tour data
        try:
            tourList = xUserKIData.CameraTours[PtGetAgeName()][tour]
        except:
            ki.IDoErrorChatMessage('I could not find a tour called %s in this age - use "/list tours" to see which ones are available' % tour)
            return True
        # start tour
        try:
            SetCamera(camera, tourList[0])
        except:
            ki.IDoErrorChatMessage('Tour camera object not found')
            return True
        tourName = tour
        tourInterval = interval
        tourCam = camera
        tourStep = 1
        if not tourTimerActive:
            PtAtTimeCallback(ki.key, 5, xUserKI.kTourTimer); tourTimerActive = True # a five second delay to allow you to get to camera
        if not silent: ki.IAddRTChat(None, 'Starting tour %s with a %1.1f sec dwell time.' % (tourName, tourInterval), 0)
        return True
    if (cmnd == 'tourstop'):
        if not silent:
            if len(tourName):
                ki.IAddRTChat(None, 'Stopped the currently running tour %s' % tourName, 0)
            else:
                ki.IAddRTChat(None, 'There is no tour running', 0)
        tourName = ''
        return True
    if (cmnd == 'printcam'):
        (valid, cameraName) = xUserKI.GetArg(ki, cmnd, args, '[camera name]',
          lambda args: len(args) == 0, lambda args: 'default',
          lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        camera = GetCamera(ki, cameraName)
        if not len(camera): return True
        if silent: return True
        cameraSO = PtFindSceneobject(camera[0], PtGetAgeName())
        cameraPos = cameraSO.position()
        targetSO = PtFindSceneobject(camera[1], PtGetAgeName())
        targetPos = targetSO.position()
        # print the data string to make it easy to create tour variables with a cut and paste from chatlog
        cameraStr = ('%f,%f,%f' % (cameraPos.getX(), cameraPos.getY(), cameraPos.getZ()))
        targetStr = ('%f,%f,%f' % (targetPos.getX(), targetPos.getY(), targetPos.getZ()))
        ki.IAddRTChat(None, '[(%s),(%s)],' % (cameraStr, targetStr), 0)
        return True
    if (cmnd in ['entercam', 'leavecam']):
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'camera name> <[list of players]',
          lambda args: len(args) >= 1, lambda args: (args[0], xUserKI.GetPlayers(ki, args[1:], playerList, thisAgeOnly=True)))
        if not valid or not data[1]: return True
        (cameraName, objects) = data
        camera = GetCamera(ki, cameraName)
        if not len(camera): return True
        xUserKI.SendRemoteCall(ki, '%s %s' % (cmnd, camera[0]), data[1])
        if not silent:
            if cmnd == 'entercam': ki.IAddRTChat(None, 'Forced players to use that camera', 0)
            else: ki.IAddRTChat(None, 'The players now control their camera again', 0)
        return True
# cheats
    if (cmnd == 'getgzmarker'):
        import xCheat
        ageName = PtGetAgeName()
        (GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber, MarkerToGetNumber) = PtDetermineGZ()
        warn = 0
        if (ageName in ['GreatZero', 'city', 'Neighborhood', 'Neighborhood02']):
            warn = 1
        if ((MarkerGottenColor == 'green') or (MarkerGottenColor == 'red')):
            if (MarkerGottenNumber < MarkerToGetNumber):
                xCheat.GZGetMarkers('1')
                if not silent:
                    ki.IAddRTChat(None, 'Successfully collected one marker', 0)
                    if (warn):
                        ki.IAddRTChat(None, 'Please be aware that it might have strange consequences when you click on the marker which was automatically collected. Link out to make sure that doesn\'t happen.', 0)
            else:
                ki.IDoErrorChatMessage('You already have all the markers')
        elif (MarkerGottenColor == 'yellow'):
            (whichGame, state,) = PtWhichCGZPlaying()
            if (whichGame != kCGZMarkerInactive):
                if ((state == kCGZMarkerAvailable) and (MarkerGottenNumber == 0)):
                    PtSetCGZGameState(whichGame, kCGZMarkerCaptured)
                    PtUpdateGZGamesChonicles(GZPlaying, MarkerGottenColor, MarkerToGetColor, MarkerGottenNumber+1, MarkerToGetNumber)
                    PtSendKIMessage(kGZUpdated, 0)
                    if not silent:
                        ki.IAddRTChat(None, 'Successfully collected one marker', 0)
                        if (warn):
                            ki.IAddRTChat(None, 'Please be aware that it might have strange consequences when you click on the marker which was automatically collected. Link out to make sure that doesn\'t happen.', 0)
                else:
                    ki.IDoErrorChatMessage('You already got that CGZ marker')
            else:
                ki.IDoErrorChatMessage('There\'s no GZ marker mission going (and the vault is not consistent)')
        else:
            ki.IDoErrorChatMessage('There\'s no GZ marker mission going')
        return True
    if (cmnd == 'getjourneys'):
        if (PtGetAgeName() in ['Gira', 'Garden', 'Teledahn', 'Garrison', 'Kadish', 'Cleft']):
            import xCheat
            xCheat.GetAgeJourneyCloths(0)
            if not silent: ki.IAddRTChat(None, 'Collected all the journey cloths for the current age.', 0)
        else:
            ki.IDoErrorChatMessage('Can\'t collect journey cloths for your current age.')
        return True
    if (cmnd == 'growtree' or cmnd == 'shrinktree'):
        vault = ptVault()
        psnlSDL = vault.getPsnlAgeSDL()
        treePage = psnlSDL.findVar("YeeshaPage10")
        size = treePage.getInt()
        if (cmnd == 'growtree'):
            if (size >= 100):
                ki.IAddRTChat(None, 'Your Relto tree already has it\'s maximal size', 0)
                return True
            treePage.setInt(size+10)
            verb = "Grew"
        if (cmnd == 'shrinktree'):
            if (size < 10):
                ki.IAddRTChat(None, 'Your Relto tree already has it\'s minimal size', 0)
                return True
            treePage.setInt(size-10)
            verb = "Shrunk"
        vault.updatePsnlAgeSDL(psnlSDL)
        if not silent:
            if (PtGetAgeName() == 'Personal'): ki.IAddRTChat(None, '%s your Relto tree. You may have to re-link to see the changes.' % verb, 0)
            else: ki.IAddRTChat(None, '%s your Relto tree.' % verb, 0)
        return True
    if (cmnd == 'getyeeshapages'):
        import xCheat
        xCheat.GetAllYeeshaPages(0)
        if not silent:
            if (PtGetAgeName() == 'Personal'): ki.IAddRTChat(None, 'Enabled all the Yeesha pages. Please re-link.', 0)
            else: ki.IAddRTChat(None, 'Enabled all the Yeesha pages.', 0)
        return True
    if (cmnd == 'getzandoni'):
        import xSndLogTracks
        xSndLogTracks.SetLogMode()
        if not silent: ki.IAddRTChat(None, 'Got you the Zandoni!', 0)
        return True
    if (cmnd == 'getfirstweek'):
        if (PtGetAgeName() == 'Personal'):
            xUserKI.SetSDL('FirstWeekClothing', 0, 1)
            if not silent: ki.IAddRTChat(None, 'Got you the frst week clothing!', 0)
        else:
            ki.IDoErrorChatMessage('You have to call this command in your Relto')
        return True
    return False