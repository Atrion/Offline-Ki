# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2004-2011  The Offline KI contributors                      #
#    See the file AUTHORS for more info about the contributors (including      #
#    contact information)                                                      #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    Please see the file COPYING for the full GPLv3 license, or see            #
#    <http://www.gnu.org/licenses/>                                            #
#                                                                              #
#    Uru exception: In addition, this file may be used in combination with     #
#    (non-GPL) code within the context of Uru.                                 #
#                                                                              #
#==============================================================================#
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

# Global info variables and configuration
gGotoPlaces = {
    'city': {
        'ferry': [-216, -591, 9],
        'gallery': [168, -490, 163],
        'library': [792, -597, 260],
        'takotah': [0, -97, 221],
        'rooftop': [-60, -195, 275]
    },
    'Ercana': {
        'brokentrail': [-528, -964, -57],
        'factory': [0, -146, -13],
        'start': [-497, -588, -45],
        'trailend': [-886, -728, -48],
        'pellets': [0, 750, 80]
    },
    'Kadish': {
        'gallerylink': [48, 181, 15],
        'pyramid': [736, -121, 3],
        'vault': [1182, 210, 9]
    },
    'Minkata': {
        'cage': [-37, 1018, 14],
        'cave1': [106, 1402, -13],
        'cave2': [1515, 655, -13],
        'cave3': [-1021, 1864, -13],
        'cave4': [-885, -546, -13],
        'cave5': [-1452, 1069, -13]
    }
}
gColorNames = ['black', 'blue', 'brown', 'cyan', 'darkbrown', 'darkgreen', 'darkpurple', 'gray', 'green', 'magenta', 'maroon', 'navyblue', 'orange', 'pink', 'red', 'slateblue', 'steelblue', 'tan', 'white', 'yellow']

# Global helper variables
gOnlineState = None
gLastSpawnPos = []
gCommandList = []
gCrashResponsesPending = 0
gCrashTimerRunning = False
gStopCrashTimer = False


# Helper functions
def OpenCmdPipe(cmd, mode = 'r'):
    try:
        return os.popen(cmd, mode)
    except:
        os.putenv("COMSPEC", "cmd.exe")
        return os.popen(cmd, mode)


def GetClipboardContent():
    clp = OpenCmdPipe('clipboard.exe')
    c = clp.read()
    clp.close
    return c[:len(c)-1]


def SetClipboardContent(c):
    clp = OpenCmdPipe('clipboard.exe -', 'w')
    clp.write(c)
    clp.close()


def StrToColor(str):
    color = None
    exec('color = ptColor().%s()' % str.lower())
    return color


def FilterFilename(filename):
    filename = string.replace(filename, '<', '')
    filename = string.replace(filename, '>', '')
    filename = string.replace(filename, '/', '')
    filename = string.replace(filename, '\\', '')
    filename = string.replace(filename, '*', '')
    filename = string.replace(filename, '?', '')
    return filename


def ExportFile(ki, dirname, element):
    datatype = element.getType()
    # marker missions
    if datatype == PtVaultNodeTypes.kMarkerListNode:
        element = element.upcastToMarkerListNode()
        if type(element) != type(None):
            # First, the folder
            markerRefs = element.getChildNodeRefList()
            filename = FilterFilename(str(element.getID()) + ' - ' + element.folderGetName() + '.mfold')
            saveFile = open((dirname + '\\' + filename), 'w')
            saveFile.write(element.folderGetName() + '\n')
            saveFile.write(str(element.getGameType()) + '|' + str(element.getRoundLength()) + '\n')
            saveFile.close()
            ki.IAddRTChat(None, 'Marker Folder exported to %s' % filename, 0)
            # Now for the list
            filename = str(element.getID()) + ' - ' + element.folderGetName() + '.mlist'
            saveFile = open((dirname + '\\' + filename), 'w')
            saveFile.write(str(element.getChildNodeCount()) + '\n')
            for markerRef in markerRefs:
                marker = markerRef.getChild().upcastToMarkerNode()
                pos = marker.markerGetPosition()
                textpos = str(pos.getX()) + ',' + str(pos.getY()) + ',' + str(pos.getZ())
                torans = marker.markerGetTorans()
                hSpans = marker.markerGetHSpans()
                vSpans = marker.markerGetVSpans()
                dnitextpos = str(torans) + ',' + str(hSpans) + ',' + str(vSpans)
                agename = marker.markerGetAge()
                saveFile.write(textpos + ';' + dnitextpos + ';' + agename + ';' + marker.markerGetText() + '\n')
            saveFile.close()
            ki.IAddRTChat(None, ('Marker List exported to %s' % filename), 0)
            return
    # text notes
    elif datatype == PtVaultNodeTypes.kTextNoteNode:
        element = element.upcastToTextNoteNode()
        if type(element) != type(None):
            filename = FilterFilename(str(element.getID()) + ' - ' + element.getTitle() + '.txt')
            saveFile = open((dirname + '\\' + filename), 'w')
            saveFile.write(element.getText())
            saveFile.close()
            ki.IAddRTChat(None, 'KI Text saved as %s' % filename, 0)
            return
    # images
    elif datatype == PtVaultNodeTypes.kImageNode:
        element = element.upcastToImageNode()
        if type(element) != type(None):
            filename = FilterFilename(str(element.getID()) + ' - ' + element.getTitle() + '.jpg')
            element.imageGetImage().saveAsJPEG((dirname + '\\' + filename), 80)
            ki.IAddRTChat(None, 'Image saved as %s' % filename, 0)
            return
    # unknown type
    ki.IDoErrorChatMessage('This KI element can not be exported - only marker missions, pictures and text notes are supported')


def ImportFile(ki, dirname, filename):
    if not os.path.exists(dirname + '\\' + filename):
        ki.IDoErrorChatMessage('File %s does not exist in %s directory' % (filename, dirname))
        return
    folder = ki.getCurrentAgeJournal()
    # marker folders
    if filename.lower().endswith('.mfold'):
        if not ki.ICanMakeMarkerFolder():
            ki.IDoErrorChatMessage('Your KI is full, you can not add any more marker folders')
            return
        try:
            localplayer = PtGetLocalPlayer()
            loadFile = open((dirname + '\\' + filename), 'r')
            innode = ptVaultMarkerListNode(PtVaultNodePermissionFlags.kDefaultPermissions)
            fName = loadFile.readline()
            if fName[len(fName)-len('\n'):] == '\n':
                fName = fName[:len(fName)-len('\n')]
            innode.folderSetName(fName)
            innode.setOwnerID(localplayer.getPlayerID())
            innode.setOwnerName(localplayer.getPlayerName())
            #gInfo = loadFile.readline()
            #gInfo = string.split(gInfo, '|')
            gInfo = ['2', '120'] # other mission types are not supported
            innode.setGameType(int(gInfo[0]))
            innode.setRoundLength(int(gInfo[1]))
            folder.addNode(innode)
            loadFile.close()
            ki.IAddRTChat(None, ('Marker folder %s created from %s. Be sure to import the markers too!' % (fName, filename)), 0)
        except Exception, details:
            ki.IDoErrorChatMessage('Error reading Marker Folder file %s: %s' % (filename, details))
        return
    # markers
    elif filename.lower().endswith('.mlist'):
        try:
            mgr = ptMarkerMgr()
            working = mgr.getWorkingMarkerFolder() 
            if (type(working) == type(None)) or mgr.isGameRunning():
                ki.IDoErrorChatMessage('You must be editing a marker mission when importing a marker list')
                return
            if len(working.getChildNodeRefList()):
                ki.IDoErrorChatMessage('You can not import markers to a mission which already contains markers')
                return
            loadFile = open((dirname + '\\' + filename), 'r')
            numMarkers = int(loadFile.readline())
            for i in range(numMarkers):
                ptMarkerMgr().createMarker('Marker')
            # close the mission to prevent markers from being shown at wrong position
            ki.IResetWorkingMarkerFolder()
            ptMarkerMgr().hideMarkersLocal()
            # create markers
            markerRefs = working.getChildNodeRefList()
            for markerRef in markerRefs:
                if not ki.ICanMakeMarker():
                    ki.IDoErrorChatMessage('Your KI is full, you can not add any more marker')
                    return
                marker = markerRef.getChild().upcastToMarkerNode()
                markerData = loadFile.readline()
                markerData = string.split(markerData, ';', 3)
                markerPos = string.split(markerData[0], ',')
                markerDniPos = string.split(markerData[1], ',')
                markerText = markerData[3]
                if markerText[len(markerText)-len('\n'):] == '\n':
                    markerText = markerText[:len(markerText)-len('\n')]
                marker.markerSetAge(markerData[2])
                marker.markerSetPosition(ptPoint3(float(markerPos[0]), float(markerPos[1]), float(markerPos[2])))
                marker.markerSetGPS(int(markerDniPos[0]), int(markerDniPos[1]), int(markerDniPos[2]))
                marker.markerSetText(markerText)
                marker.save()
                #self.IAddRTChat(None, ('Marker %s inserted' % markerText), 0)
            loadFile.close()
            ki.IAddRTChat(None, ('%d markers imported from %s' % (len(working.getChildNodeRefList()), filename)), 0)
        except Exception, details:
            ki.IDoErrorChatMessage('Error reading Marker List file %s: %s' % (filename, details))
        return
    # text notes
    elif filename.lower().endswith('.txt'):
        if not ki.ICanMakeNote():
            ki.IDoErrorChatMessage('Your KI is full, you can not add any more notes')
            return
        try:
            loadFile = open((dirname + '\\' + filename), 'r')
            try:
                innode = ptVaultTextNoteNode(PtVaultNodePermissionFlags.kDefaultPermissions) # this doesn't work in TPOTS??
            except:
                innode = ptVaultTextNoteNode()
            textdata = loadFile.read()
            innode.noteSetText(textdata)
            innode.noteSetTitle(filename[:len(filename)-len('.txt')])
            folder.addNode(innode)
            loadFile.close()
            ki.IAddRTChat(None, ('Text file %s imported into current age journal' % filename), 0)
        except Exception, details:
            ki.IDoErrorChatMessage('Error reading text file %s: %s' % (filename, details))
        return
    # images
    elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        if not ki.ICanTakePicture():
            ki.IDoErrorChatMessage('Your KI is full, you can not take any more pictures')
            return
        try:
            loadfile = PtLoadJPEGFromDisk(dirname + '\\' + filename, 800, 600)
            innode = ptVaultImageNode(PtVaultNodePermissionFlags.kDefaultPermissions)
            innode.imageSetImage(loadfile)
            if filename.lower().endswith('.jpg'):
                innode.imageSetTitle(filename[:len(filename)-len('.jpg')])
            else:
                innode.imageSetTitle(filename[:len(filename)-len('.jpeg')])
            folder.addNode(innode)
            ki.IAddRTChat(None, ('Image %s imported current age journal' % filename), 0)
        except Exception, details:
            ki.IDoErrorChatMessage('Error reading image %s: %s' % (filename, details))
        return
    ki.IDoErrorChatMessage('File %s has an unsupported type!' % filename)


# Callback functions
def OnTimer(ki, id):
    if id == xUserKI.kEnableTimer:
        PtForceCursorShown()
        PtSendKIMessage(kEnableKIandBB, 0)
        return True
    # crash detection
    elif id == xUserKI.kCrashTimer:
        import xKI
        global gCrashResponsesPending, gCrashTimerRunning, gStopCrashTimer
        if gStopCrashTimer: # we are asked to stop
            gCrashTimerRunning = gStopCrashTimer = False
            return
        if (gCrashResponsesPending >= 2): # if we missed two or more pongs, we are most likely crashed
            print "Crash Detection: You crashed!"
            PtSendKIMessage(kKIOKDialog, 'Crash Detection: It seems you lost your connection to the server - please restart the game.') # quit game
            gCrashTimerRunning = False
        else:
            PtAtTimeCallback(ki.key, 30.0, xUserKI.kCrashTimer)
            PtSendRTChat(PtGetLocalPlayer(), [], "/!silentping", xKI.ChatFlags(0).flags)
            gCrashResponsesPending = gCrashResponsesPending+1
        return True
    return False


def OnDefaultKey(ki, isShift, isCtrl, keycode):
    # Don't use Scroll Lock here, for some reason it gets send twice as often as it should
    # Scripted commands
    if isCtrl and not isShift and keycode == 19: # Pause
        global gCommandList
        if len(gCommandList):
            ki.ICheckChatCommands(gCommandList[0], silent=True)
            gCommandList.remove(gCommandList[0])
            # don't tell user about last command... it would show the KI
        return
    # Clipbaord
    if isCtrl and isShift and ki.isChatting:
        addtxt = GetClipboardContent()
        if len(addtxt):
            import xKI
            # there is text, put it into the chat line edit
            chatedit = ptGUIControlEditBox(ki.getDialog().getControlFromTag(xKI.kChatEditboxID))
            txt = chatedit.getString()
            chatedit.setString(txt + addtxt)
            chatedit.hide()
            chatedit.end()
            chatedit.show() # hide and show to show the "|" at the right place
        return


def OnNewAgeLoaded(ki, firstAge):
    # load additional pages
    if PtGetAgeName() in xxConfig.AutoPages:
        PtPageInNode(xxConfig.AutoPages[PtGetAgeName()]) # we expect these pages to belong to the current age, so we do not care about unloading them
    # check if the POTS additions are installed (can only be done in Relto)
    if PtGetAgeName() == 'Personal':
        import booksDustGlobal
        if not booksDustGlobal.DynCoverLoaded:
            ki.IDoErrorChatMessage('You do not have the POTS Patches applied, so you will miss some functionality. To get them, select the "Coversion" tab '+
                'in Drizzle, select your POTS folder, and hit the "Start" button next to that selection.')
    if xxConfig.isOnline():
        # some online-only things
        global gOnlineState, gCrashTimerRunning
        # get local player info node
        plyrInfonode = ptVault().getPlayerInfo().upcastToPlayerInfoNode()
        # read state
        gOnlineState = not len(plyrInfonode.getCreateAgeName())
        if not gOnlineState:
            # tell current server that we are NOT online
            plyrInfonode.setCreateAgeName(plyrInfonode.getCreateAgeName()) # make sure the info node is sent
            plyrInfonode.save()
        # crash detection
        if not gCrashTimerRunning:
            gCrashTimerRuning = True
            PtAtTimeCallback(ki.key, 2.5, xUserKI.kCrashTimer)
        # get auth level
        import xKI
        PtSendRTChat(PtGetLocalPlayer(), [], "/!getauthlevel", xKI.ChatFlags(0).flags) # we update after every linking because it coud have changed
        # shard identifier (not expected to change)
        if firstAge:
            PtSendRTChat(PtGetLocalPlayer(), [], "/!getshardidentifier", xKI.ChatFlags(0).flags)
    else:
        # some offline-only things
        xxConfig.accessLevel = 0 # full access - everyone is an admin offline


def OnLinkingOut(ki):
    global gLastSpawnPos
    # reset spawn position
    gLastSpawnPos = []
    # crash detection
    global gStopCrashTimer
    gStopCrashTimer = True # stop the timer


def OnAvatarSpawn(ki):
    global gLastSpawnPos
    if not len(gLastSpawnPos):
        pos = PtGetLocalAvatar().position()
        gLastSpawnPos = [pos.getX(), pos.getY(), pos.getZ()]


def OnRemoteCall(ki, cmnd, args, sender):
    import xKI
    if (cmnd == 'ping'):
        if sender.getPlayerID() != PtGetLocalPlayer().getPlayerID(): # don't send it to ourselves - that wouldn't work anyway
            player = PtGetLocalPlayer()
            PtSendRTChat(player, [sender], 'Pong from %s (%d)' % (player.getPlayerName(), player.getPlayerID()), xKI.ChatFlags(kRTChatStatusMsg).flags)
        else:
            ki.IAddRTChat(None, 'You tried sending a ping to yourself - that does not work', 0)
        return True
    if (cmnd == 'getversion'):
        if sender.getPlayerID() != PtGetLocalPlayer().getPlayerID(): # don't send it to ourselves - that wouldn't work anyway
            player = PtGetLocalPlayer()
            PtSendRTChat(player, [sender], '%s has KI version %s' % (player.getPlayerName(), xUserKI.gUserKIVersion), xKI.ChatFlags(kRTChatStatusMsg).flags)
        else:
            ki.IAddRTChat(None, 'You tried requesting the version from yourself - why don\'t you use \'/info\'?', 0)
        return True
    if (cmnd in ['entercam','leavecam']):
        cameraSO = PtFindSceneobject(args[0], PtGetAgeName())
        if cmnd == 'entercam':
            ptCamera().undoFirstPerson()
            cameraSO.pushCutsceneCamera(0, PtGetLocalAvatar().getKey())
        else:
            cameraSO.popCutsceneCamera(PtGetLocalAvatar().getKey())
        return True
    return False


def OnServerCommand(ki, cmnd, args):
    if (cmnd == 'silentpong'):
        global gCrashResponsesPending
        gCrashResponsesPending = 0
        return True
    elif (cmnd == 'authlevel'):
        xxConfig.accessLevel = int(args[0])
        # some things should always reflect the current state
        if xxConfig.hasStoryLevel(): ki.setShowHiddenPlayers(True)
        else: ki.setShowHiddenPlayers(False)
        return True
    elif (cmnd == 'shardidentifier'):
        xxConfig.shardIdentifier = args[0]
        return True
    elif (cmnd == 'relink'):
        linkMgr = ptNetLinkingMgr()
        linkMgr.linkToPlayersAge(PtGetLocalClientID())
        return True
    return False


# Main function
def OnCommand(ki, arg, cmnd, args, playerList, KIContent, silent):
    global gOnlineState # online state variable
# base commands
    if (cmnd in ['me', 'my']):
        if cmnd == 'my': suffix = '\'s'
        else: suffix = ''
        ki.IDoStatusChatMessage('%s%s %s' % (PtGetClientName(), suffix, arg))
        return True
    if (cmnd == 'createmarkerfolder'):
        ki.ICreateMarkerFolder()
        return True
    if (cmnd == 'copy'):
        import xKI
        chatarea = ptGUIControlEditBox(ki.getDialog().getControlFromTag(xKI.kChatDisplayArea))
        txt = chatarea.getString()
        SetClipboardContent(txt)
        ki.IAddRTChat(None, 'Copied that chat output you see above to the clipboard', 0)
        return True
# debug commands
    if (xxConfig.isOnline() and cmnd == 'ping'):
        (valid, player) = xUserKI.GetArg(ki, cmnd, args, '[player]',
          lambda args: len(args) == 0, lambda args: True, # below code will send the ping to everyone in the age if no player is specified
          lambda args: len(args) == 1, lambda args: xUserKI.GetPlayer(ki, args[0], playerList))
        if not valid or not player: return True
        if isinstance(player, ptPlayer):
            if not silent: ki.IAddRTChat(None, 'Sending ping to %s' % player.getPlayerName(), 0)
            xUserKI.SendRemoteCall(ki, 'ping', [player])
        else:
            if not len(PtGetPlayerList()):
                ki.IDoErrorChatMessage('There is noone to ping in the current age, so you can not get a reply. Perhaps you want to use \'/!ping\' to directly ping the server?')
            else:
                if not silent: ki.IAddRTChat(None, 'Sending ping to everyone in this age', 0)
                xUserKI.SendRemoteCall(ki, 'ping', toSelf = False)
        return True
    if (cmnd == 'clearcam'):
        PtClearCameraStack()
        if not silent: ki.IAddRTChat(None, 'Successfully cleared the camera stack', 0)
        return True
    if (cmnd == 'enablefp'):
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        if not silent: ki.IAddRTChat(None, '1st person switching enabled', 0)
        return True
    if (cmnd == 'checkaccess'):
        if silent: return True
        if xxConfig.isOnline():
            ki.IAddRTChat(None, 'You are playing online with an access level of %d' % xxConfig.accessLevel, 0)
        else:
            ki.IAddRTChat(None, 'You are playing offline with an access level of %d' % xxConfig.accessLevel, 0)
        return True
# link commands
    if (cmnd == 'hood'):
        if not xUserKI.DoesPlayerHaveRelto():
            ki.IDoErrorChatMessage('You have to collect a Relto-book before using this command')
            return True
        gender = PtGetLocalAvatar().avatar.getAvatarClothingGroup()
        if (gender == 0): hisher = 'his'
        elif (gender == 1): hisher = 'her'
        else: hisher = 'the'
        if not silent: ki.IDoStatusChatMessage('%s is linking to %s neighborhood' % (PtGetClientName(), hisher))
        linkMgr = ptNetLinkingMgr()
        linkMgr.linkToMyNeighborhoodAge()
        return True
    if (cmnd == 'nexus'):
        if not xUserKI.DoesPlayerHaveRelto():
            ki.IDoErrorChatMessage('You have to collect a Relto-book before using this command')
            return True
        als = xUserKI.GetAgeLinkStruct(ki, 'Nexus')
        if type(als) == type(None): return True
        # link us
        gender = PtGetLocalAvatar().avatar.getAvatarClothingGroup()
        if (gender == 0): hisher = 'his'
        elif (gender == 1): hisher = 'her'
        else: hisher = 'the'
        if not silent: ki.IDoStatusChatMessage('%s is linking to %s Nexus' % (PtGetClientName(), hisher))
        linkMgr = ptNetLinkingMgr()
        linkMgr.linkToAge(als)
        return True
# avatar movement
    if (cmnd == 'jump'):
        (valid, height) = xUserKI.GetArg(ki, cmnd, args, 'number of D\'ni feet',
          lambda args: len(args) == 1, lambda args: int(args[0]))
        if not valid: return True
        if (not xxConfig.hasStoryLevel() and PtGetAgeName() in xxConfig.LockedAges):
            ki.IDoErrorChatMessage("You are in a locked age, some KI commands are disabled here")
            return True
        if (height == 0):
            ki.IDoErrorChatMessage('How do you want to jump 0 feet?!?')
            return True
        avatar = PtGetLocalAvatar()
        xUserKI.WarpObjectRelative(avatar, 0, 0, height)
        if silent: return True
        if (height > 0):
            if (height == 1): ki.IAddRTChat(None, 'You jump one foot into the air', 0)
            else: ki.IAddRTChat(None, 'You jump %s feet into the air' % height, 0)
        else:
            if (height == -1): ki.IAddRTChat(None, 'You jump one foot down', 0)
            else: ki.IAddRTChat(None, 'You jump %s feet down' % (-height), 0)
        return True
    if (cmnd in ['respawn', 'sav', 'a']):
        if not len(gLastSpawnPos):
            ki.IDoErrorChatMessage('I\'m sorry, I was unable to save your spawn point, so I can\'t bring you back there.')
        else:
            xUserKI.WarpObjectToPos(PtGetLocalAvatar(), gLastSpawnPos[0], gLastSpawnPos[1], gLastSpawnPos[2])
            if not silent: ki.IDoStatusChatMessage('%s re-spawns to the starting point' % PtGetClientName())
        return True
    if (cmnd == 'spawn'):
        if (not xxConfig.hasStoryLevel() and PtGetAgeName() in xxConfig.LockedAges):
            ki.IDoErrorChatMessage("You are in a locked age, some KI commands are disabled here")
            return True
        (valid, n) = xUserKI.GetArg(ki, cmnd, args, '[number of spawns]',
          lambda args: len(args) == 0, lambda args: 1,
          lambda args: len(args) == 1, lambda args: int(args[0]))
        if not valid: return True
        if (n < 1): n = 1
        i = 0
        while i < n:
            PtAvatarSpawnNext()
            i = i+1
        return True
    if (cmnd == 'goto'):
        (valid, target) = xUserKI.GetArg(ki, cmnd, args, 'goto place',
          lambda args: len(args) == 1, lambda args: args[0].lower())
        if not valid: return True
        if (not xxConfig.hasStoryLevel() and PtGetAgeName() in xxConfig.LockedAges):
            ki.IDoErrorChatMessage("You are in a locked age, some KI commands are disabled here")
            return True
        # get the place
        if target == 'listall':
            ki.IAddRTChat(None, 'The following goto places are available: %s' % xUserKI.JoinListRec(gGotoPlaces), 0)
            return True
        age = PtGetAgeName()
        if not age in gGotoPlaces:
            ki.IDoErrorChatMessage('There is no goto place in this age. goto places are available in: %s' % xUserKI.JoinList(gGotoPlaces))
            return True
        places = gGotoPlaces[age]
        if target == 'list':
            ki.IAddRTChat(None, 'The following goto places are available in this age: %s' % xUserKI.JoinList(places), 0)
            return True
        if not target in places:
            ki.IDoErrorChatMessage('There is no goto place called \'%s\' in this age. Use one of the following: %s' % (target, xUserKI.JoinList(places)))
            return True
        place = places[target]
        # warp to the place
        xUserKI.WarpObjectToPos(PtGetLocalAvatar(), place[0], place[1], place[2])
        if not silent: ki.IDoStatusChatMessage('%s warps to \'%s\'' % (PtGetClientName(), target))
        return True
    if (cmnd in ['float', 'nofloat']):
        if (not xxConfig.hasStoryLevel()) and (PtGetAgeName() in xxConfig.LockedAges):
            ki.IDoErrorChatMessage("You are in a locked age, some KI commands are disabled here")
            return True
        if xxConfig.hasAdminLevel():
            (valid, objects) = xUserKI.GetArg(ki, cmnd, args, '[list of objects]',
                lambda args: len(args) == 0, lambda args: xUserKI.GetObjects(ki, ['me'], playerList),
                lambda args: len(args) >= 1, lambda args: xUserKI.GetObjects(ki, args, playerList))
            if not valid or not objects: return True
        else:
            objects = [PtGetLocalAvatar()]
        # (un)float them
        for object in objects:
            object.netForce(1)
            object.physics.disable() # in order for kickables to correctly re-gain physics, it has to be disabled and enabled again
            if (cmnd == 'float'):
                if not silent: ki.IAddRTChat(None, 'Disabled physics for %s' % xUserKI.GetObjectName(object), 0)
            else:
                object.physics.enable()
                if not silent: ki.IAddRTChat(None, 'Enabled physics for %s' % xUserKI.GetObjectName(object), 0)
        return True
# avatar animations/appearance
    if (cmnd == 'hug'):
        PtAvatarEnterLookingAtKI()
        return True
    if (cmnd == 'unhug'):
        PtAvatarExitLookingAtKI()
        return True
    if (cmnd == 'glow'):
        if (not xxConfig.hasStoryLevel() and PtGetAgeName() in xxConfig.LockedAges):
            ki.IDoErrorChatMessage("You are in a locked age, some KI commands are disabled here")
            return True
        avatar = PtGetLocalAvatar()
        PtSetLightAnimStart(avatar.getKey(), True)
        if not silent: ki.IAddRTChat(None, 'You start glowing like fireflies', 0)
        return True
    if (cmnd  == 'noglow'):
        if (not xxConfig.hasStoryLevel() and PtGetAgeName() in xxConfig.LockedAges):
            ki.IDoErrorChatMessage("You are in a locked age, some KI commands are disabled here")
            return True
        avatar = PtGetLocalAvatar()
        PtSetLightAnimStart(avatar.getKey(), False)
        if not silent: ki.IAddRTChat(None, 'You stop glowing like fireflies', 0)
        return True
    if (cmnd == 'lite'):
        (valid, color) = xUserKI.GetArg(ki, cmnd, args, 'w|r|g|b',
          lambda args: len(args) == 1 and args[0] in ['w', 'r', 'g', 'b'], lambda args: args[0])
        if not valid: return True
        avatar = PtGetLocalAvatar()
        if (color == 'w'): PtSetLightValue(avatar.getKey(), 2, 2, 2, 2)
        elif (color == 'r'): PtSetLightValue(avatar.getKey(), 9, 2, 2, 2)
        elif (color == 'g'): PtSetLightValue(avatar.getKey(), 2, 9, 2, 2)
        elif (color == 'b'): PtSetLightValue(avatar.getKey(), 2, 2, 9, 2)
        if not silent: ki.IAddRTChat(None, 'You start glowing like a lantern (visible only for you)', 0)
        return True
    if (cmnd == 'nolite'):
        avatar = PtGetLocalAvatar()
        PtSetLightValue(avatar.getKey(), 0, 0, 0, 0)
        if not silent: ki.IAddRTChat(None, 'You stop glowing like a lantern (visible only for you)', 0)
        return True
    if (cmnd == 'suitup'):
        clothing = ['03_MLHand_Suit',
         '03_MRHand_Suit',
         '03_MTorso_Suit',
         '03_MLegs_Suit',
         '03_MLFoot_Suit',
         '03_MRFoot_Suit',
         '03_FLHand_Suit',
         '03_FRHand_Suit',
         '03_FTorso_Suit',
         '03_FLegs_Suit',
         '03_FLFoot_Suit',
         '03_FRFoot_Suit']
        avatar = PtGetLocalAvatar()
        avatar.netForce(1)
        for item in clothing[0:]:
            avatar.avatar.wearClothingItem(item, 0)
            avatar.avatar.tintClothingItem(item, ptColor().white(), 0)
            avatar.avatar.tintClothingItemLayer(item, ptColor().white(), 2, 1)
        avatar.avatar.saveClothing()
        if not silent: ki.IAddRTChat(None, 'Got you a maintainer suit', 0)
        return True
    if (cmnd in ['removeki', 'removereltobook']):
        if cmnd == 'removeki': clothing = 'KI'
        else: clothing = 'PlayerBook'
        avatar = PtGetLocalAvatar()
        avatar.netForce(1)
        gender = avatar.avatar.getAvatarClothingGroup()
        if (gender > kFemaleClothingGroup):
            gender = kMaleClothingGroup
        if (gender == kFemaleClothingGroup):
            avatar.avatar.removeClothingItem('FAcc' + clothing)
        else:
            avatar.avatar.removeClothingItem('MAcc' + clothing)
        avatar.avatar.saveClothing()
        if not silent: 
            if cmnd == 'removeki': ki.IAddRTChat(None, 'Your avatar no longer wears a KI. Use the KI dispenser to get it back.', 0)
            else: ki.IAddRTChat(None, 'Your avatar no longer wears a Relto book. Use the KI dispenser to get it back.', 0)
        return True
# commands regarding colors (fog, hair, skin, text)
    if (cmnd in ['fcol', 'fogcolor', 'skincolor', 'haircolor', 'eyecolor', 'textcolor']):
        # data[0] is the name of the color, data[1] either nonexistant (if the color has to be determined by name)
        # or an array with the r, g and b values
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'color name>|<red> <green> <blue',
          lambda args: len(args) == 3, lambda args: (float(args[0]), float(args[1]), float(args[2])),
          lambda args: len(args) == 1, lambda args: (args[0], ))
        if not valid: return True
        colorName = arg.lower()
        color = 0
        if (len(data) == 1):
            if data[0].lower() in gColorNames:
                color = StrToColor(data[0])
            else:
                ki.IDoErrorChatMessage('\'%s\' is no known color. Choose one of the following: %s' % (data[0], xUserKI.JoinList(gColorNames)))
                return True
        else:
            (r, g, b) = data
            if r > 1: r = 1
            elif r < 0: r = 0
            if g > 1: g = 1
            elif g < 0: g = 0
            if b > 1: b = 1
            elif b < 0: b = 0
            color = ptColor(r, g, b)
        # use it
        avatar = PtGetLocalAvatar()
        avatar.netForce(1)
        if cmnd in ['fcol', 'fogcolor']:
            if (not xxConfig.hasStoryLevel() and PtGetAgeName() in xxConfig.LockedAges):
                PtSendKIMessage(kKILocalChatErrorMsg, "You are in a locked age, some KI commands are disabled here")
                return True
            PtConsoleNet('Graphics.Renderer.Fog.SetDefColor %f %f %f' % (color.getRed(), color.getGreen(), color.getBlue()), 1)
            if not silent: ki.IDoStatusChatMessage('%s turns the fog %s' % (PtGetClientName(), colorName))
        elif cmnd == 'skincolor':
            avatar.avatar.tintSkin(color)
            avatar.avatar.saveClothing()
            if not silent: ki.IAddRTChat(None, 'Changed your skin color to %s' % colorName, 0)
        elif cmnd == 'haircolor':
            worn = avatar.avatar.getAvatarClothingList()
            for item in worn:
                if (item[1] == kHairClothingItem):
                    avatar.avatar.tintClothingItem(item[0], color)
                    avatar.avatar.saveClothing()
                    if not silent: ki.IAddRTChat(None, 'Changed your hair color to %s' % colorName, 0)
                    return True
            ki.IDoErrorChatMessage('Sorry, I can\'t find your hair.')
        elif cmnd == 'eyecolor':
            worn = avatar.avatar.getAvatarClothingList()
            for item in worn:
                if (item[1] == kFaceClothingItem):
                    avatar.avatar.tintClothingItem(item[0], color, 0)
                    avatar.avatar.tintClothingItemLayer(item[0], color, 2)
                    avatar.avatar.saveClothing()
                    if not silent: ki.IAddRTChat(None, 'Changed your eye color to %s' % colorName, 0)
                    return True
            ki.IDoErrorChatMessage('Sorry, I can\'t find your face.')
        elif cmnd == 'textcolor':
            ki.setChatMessageColor(color)
            if not silent: ki.IAddRTChat(None, 'Changed text color to %s' % colorName, 0)
        return True
# fog density
    if (cmnd in ['fogdensity', 'fdens']):
        (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'start distance> <end distance> <density',
          lambda args: len(args) == 3, lambda args: (float(args[0]), float(args[1]), float(args[2])))
        if not valid: return True
        if (not xxConfig.hasStoryLevel() and PtGetAgeName() in xxConfig.LockedAges):
            PtSendKIMessage(kKILocalChatErrorMsg, "You are in a locked age, some KI commands are disabled here")
            return True
        (start, end, density) = data
        PtConsoleNet('Graphics.Renderer.Fog.SetDefLinear %f %f %f' % (start, end, density), 1)
        if not silent: ki.IDoStatusChatMessage('%s changes the fog density (%1.2f %1.2f %1.2f)' % (PtGetClientName(), start, end, density))
        return True
# camera control
    if (cmnd == 'stopcam'):
        PtConsole('Camera.SetGlobalAccel 0')
        PtConsole('Camera.SetGlobalVelocity 0')
        if not silent: ki.IAddRTChat(None, 'Your camera won\'t move anymore (sometimes it\'ll still follow the direction of the avatar, but it won\'t constantly show your back)', 0)
        return True
    if (cmnd == 'gocam'):
        PtConsole('Camera.SetGlobalAccel 40')
        PtConsole('Camera.SetGlobalVelocity 40')
        if not silent: ki.IAddRTChat(None, 'Your camera should now move (almost) as usual', 0)
        return True
# Age-specific commands
    if (cmnd == 'call'):
        age = PtGetAgeName()
        if (age == 'Negilahn'):
            (valid, what) = xUserKI.GetArg(ki, cmnd, args, 'Urwin|Monkey',
            lambda args: len(args) == 1, lambda args: args[0])
            if not valid: return True
            if what == 'Urwin':
                xUserKI.SetSDL('UrwinSpawnTimes', 0, PtGetDniTime()+2)
                if not silent: ki.IDoStatusChatMessage('%s called the Urwin' % PtGetClientName())
            elif what == 'Monkey':
                xUserKI.SetSDL('MonkeySpawnTimes', 0, PtGetDniTime()+2)
                if not silent: ki.IDoStatusChatMessage('%s called the Monkey' % PtGetClientName())
            else:
                ki.IDoErrorChatMessage('You have to call either \'Urwin\' or \'Monkey\' (this is case sensitive!)')
        elif (age == 'Payiferen'):
            xUserKI.SetSDL('UrwinSpawnTimes', 0, PtGetDniTime()+2)
            if not silent: ki.IDoStatusChatMessage('%s called the Urwin' % PtGetClientName())
        else:
            ki.IDoErrorChatMessage('This command can only be used in Negilahn and Payiferen')
        return True
    if (cmnd == 'getfissure'): # this is NOT a cheat as (a) you can't link with it and (b) there usually is no way to get it more than once
        if (PtGetAgeName() == 'Personal'):
            (valid, stage) = xUserKI.GetArg(ki, cmnd, args, 'fissure stage (1-4)',
            lambda args: len(args) == 1 and args[0] in ['1', '2', '3', '4'], lambda args: args[0])
            if not valid: return True
            objectsAndResponders = {
                '1': ['FissureCarvDummy01', 'RespFissureStage01'],
                '2': ['FissureCarvDummy02', 'RespFissureStage02'],
                '3': ['FissureCarvDummy03', 'RespFissureStage03'],
                '4': ['FissureAnimRegion', 'RespFissureStage04'] }
            (objectName, responderName) = objectsAndResponders[stage]
            obj = PtFindSceneobject(objectName, 'Personal')
            resplist = obj.getResponders()
            for resp in resplist:
                if (resp.getName() == responderName):
                    atResp = ptAttribResponder(999)
                    atResp.__setvalue__(resp)
                    atResp.run(ki.key)
                    if not silent: ki.IDoStatusChatMessage('%s created a fissure at stage %s' % (PtGetClientName(), stage))
                    return True
            ki.IDoErrorChatMessage('Error creating fissure: I could not find the correct responder')
        else:
            ki.IDoErrorChatMessage('This command can only be used in Relto')
        return True
    if (cmnd in ['reltostars', 'noreltostars']):
        if PtGetAgeName() != 'Personal':
            ki.IDoErrorChatMessage('This can only be done in your Relto')
            return True
        # Hide/show some objects
        for name in ['skyhigh', 'sunglow', 'sunround', 'cameraclouds']:
            object = PtFindSceneobject(name, 'Personal')
            object.netForce(1)
            if cmnd == 'reltostars': object.draw.disable()
            else: object.draw.enable()
        # Disable fog and change clear color, apply object positions
        if cmnd == 'reltostars':
            PtConsoleNet('Graphics.Renderer.Fog.SetDefLinear 0 0 0', 1)
            PtConsoleNet('Graphics.Renderer.SetClearColor .5 .5 .5', 1)
            xUserKI.ApplyStruct('reltostars2')
            if not silent: ki.IAddRTChat(None, 'Decorated your Relto with some stars', 0)
        else:
            PtConsoleNet('Graphics.Renderer.Fog.SetDefLinear 1 900 2', 1)
            PtConsoleNet('Graphics.Renderer.SetClearColor .4 .4 .5', 1)
            xUserKI.ApplyStruct('noreltostars')
            if not silent: ki.IAddRTChat(None, 'Removed the stars from your Relto', 0)
        return True
    if (cmnd == 'rotsphere'):
        if (PtGetAgeName() != 'AhnonayMOUL'):
            ki.IDoErrorChatMessage('This command can only be used in the MOUL version of Ahnonay')
            return True
        sphere = int(xUserKI.GetSDL('ahnyCurrentSphere', 0))+1
        if sphere < 1 or sphere > 4:
            sphere = 1 # handle overflow and invalid values
        xUserKI.SetSDL('ahnyCurrentSphere', 0, sphere)
        if not silent: ki.IAddRTChat(None, 'Switched to the next sphere.', 0)
        return True
# Dusitin special: Quit command
    if (cmnd == 'quit'):
        PtConsole('app.quit')
        return True
# Disabling the KI
    if (cmnd == 'hideki'):
        (valid, time) = xUserKI.GetArg(ki, cmnd, args, 'time the KI will be disabled',
            lambda args: len(args) == 1, lambda args: int(args[0]))
        if not valid: return True
        PtForceCursorHidden()
        PtSendKIMessage(kDisableKIandBB, 0)
        PtAtTimeCallback(ki.key, time, xUserKI.kEnableTimer)
        return True
# export command
    if (cmnd == 'export'):
        element = KIContent
        if type(element) != type(None): element = KIContent.getChild()
        if type(element) == type(None):
            ki.IDoErrorChatMessage('You must have a KI element selected to use this command')
            return True
        dirname = 'export'
        if not os.path.exists(dirname): os.mkdir(dirname)
        ExportFile(ki, dirname, element)
        return True
    if (xxConfig.isOffline() and cmnd == 'import'):
        (valid, null) = xUserKI.GetArg(ki, cmnd, args, 'filename',
          lambda args: len(args) > 0)
        if not valid: return True
        dirname = 'import'
        if not os.path.exists(dirname):
            ki.IDoErrorChatMessage('You have to create a folder called \'%s\' in your Uru directory and put the file(s) in there' % dirname)
            return True
        dirlist = os.listdir(dirname)
        # import
        if arg == 'allpics':
            dirlist = os.listdir(dirname)
            for f in dirlist:
                if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg'):
                    ImportFile(ki, dirname, f)
        else:
            ImportFile(ki, dirname, arg)
        return True
# scripting commands
    if (cmnd == 'loadscript'):
        global gCommandList
        (valid, filename) = xUserKI.GetArg(ki, cmnd, args, 'name of scriptfile',
            lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        if not os.path.exists(filename):
            ki.IDoErrorChatMessage('There is no file called %s in your Uru folder!' % filename)
            return True
        file = open(filename, 'r')
        gCommandList = []
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            if line.startswith('/'): gCommandList.append(line)
        if not silent: ki.IAddRTChat(None, 'Successfully loaded %d scripted commands. You can now use Ctrl+Pause or Ctrl+Num (depending on your keyboard layout) to run them one after the other.' % len(gCommandList), 0)
        return True
# linking command (restricted!)
    if (xxConfig.hasStoryLevel() and cmnd in ['link', 'linksp']):
        if cmnd == 'link':
            (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'age filename',
              lambda args: len(args) == 1, lambda args: (args[0], None))
        else:
            (valid, data) = xUserKI.GetArg(ki, cmnd, args, 'age filename> <spawn point name',
              lambda args: len(args) == 2, lambda args: (args[0], args[1]))
        if not valid: return True
        if not xUserKI.DoesPlayerHaveRelto():
            ki.IDoErrorChatMessage('You have to collect a Relto-book before using this command')
            return True
        # find out where to link
        als = xUserKI.GetAgeLinkStruct(ki, data[0], data[1])
        if type(als) == type(None): return True
        # link us
        if not silent: ki.IAddRTChat(None, 'Linking you to %s' % als.getAgeInfo().getAgeInstanceName(), 0)
        linkMgr = ptNetLinkingMgr()
        linkMgr.linkToAge(als)
        return True
# show/hide player command (restricted!)
    if (xxConfig.hasStoryLevel() and xxConfig.isOnline() and cmnd == 'toggleoffline'):
        if type(gOnlineState) == type(None):
            ki.IDoErrorChatMessage('Weird, I did not yet get your online state... how could this happen?')
            return True
        gOnlineState = not gOnlineState
        # get local player info node
        plyrInfonode = ptVault().getPlayerInfo().upcastToPlayerInfoNode()
        if gOnlineState:
            plyrInfonode.setCreateAgeName('')
            if not silent: ki.IAddRTChat(None, 'You are marked as online again', 0)
        else:
            plyrInfonode.setCreateAgeName('hidden') # we don't have many vault node elements we can freely set, the CreateAgeName is one
            if not silent: ki.IAddRTChat(None, 'You seem to be offline', 0)
        # save it
        plyrInfonode.save()
        return True
    return False
