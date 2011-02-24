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
from PlasmaNetConstants import *
from xPsnlVaultSDL import *
import time
import PlasmaControlKeys
import xLinkMgr

class TUruAgeManager(ptResponder):
    kDustinMovie = 4200
    movieReplayDelay = 0.0
    newfile = true
    debug = true
    f = None
    book = None
    callersKey = None
    curBookAge = None
    curBookSpawnpoint = None
    showFlybys = false
    movie = None
    inMovie = false

    def initSDL(self, varName, callingKey):
        sdl = PtGetAgeSDL()
        sdl.setFlags(varName, 1, 1)
        sdl.sendToClients(varName)
        sdl.setNotify(callingKey, varName, 0.0)


    def setSDL(self, varName, value, index = 0):
        sdl = PtGetAgeSDL()
        sdl.setIndex(varName, index, value)


    def getSDL(self, varName, index = 0):
        sdl = PtGetAgeSDL()
        return sdl[varName][index]


    def isObjectInRange(self, sceneObject, range):
        avpos = PtGetLocalAvatar().getKey().getSceneObject().position()
        bkpos = sceneObject.position()
        dissqr = ((((avpos.getX() - bkpos.getX()) * (avpos.getX() - bkpos.getX())) + ((avpos.getY() - bkpos.getY()) * (avpos.getY() - bkpos.getY()))) + ((avpos.getZ() - bkpos.getZ()) * (avpos.getZ() - bkpos.getZ())))
        uam.output('Dustin: UAM: closeness:', avpos.getX(), ' ', avpos.getY(), ' ', avpos.getZ(), ' ', bkpos.getX(), ' ', bkpos.getY(), ' ', bkpos.getZ())
        uam.output('Dustin: UAM: check close:', dissqr)
        if (dissqr < (range * range)):
            return true
        else:
            return false


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 4242
        self.version = 1
        print 'Dustin: Initialising UruAgeManager API'
        self.reset()


    def reset(self):
        print 'Dustin: Resetting UruAgeManager API'
        self.newfile = true
        self.debug = true
        self.f = None
        self.book = None
        self.callersKey = None
        self.curBookAge = None
        self.curBookSpawnpoint = None
        self.showFlybys = false
        self.movie = None
        self.inMovie = false


    def OnFirstUpdate(self):
        pass


    def OnServerInitComplete(self):
        pass


    def handleControlKeyEvent(self, controlKey, activeFlag):
        if (activeFlag == false):
            if (controlKey == PlasmaControlKeys.kKeyActionMouse):
                self.output('mouseclick')
                if self.inMovie:
                    if self.movie:
                        self.movie.stop()
                        self.movie = None
                    PtEnableRenderScene()
                    PtGUICursorOn()
                    PtSetGlobalClickability(true)
                    self.linkToAge(self.curBookAge, self.curBookSpawnpoint)
                    self.curBookAge = None
                    self.curBookSpawnpoint = None
                    self.inMovie = false
                    if self.movie:
                        self.movie.stop()
                        self.movie = None
            elif ((controlKey == PlasmaControlKeys.kKeyExitMode) or (controlKey == PlasmaControlKeys.kKeyMoveBackward)):
                self.output('excapepress')
                if self.inMovie:
                    self.curBookAge = None
                    self.curBookSpawnpoint = None
                    self.inMovie = false
                    if self.movie:
                        self.movie.stop()
                        self.movie = None
                    PtEnableRenderScene()
                    PtGUICursorOn()
                    PtSetGlobalClickability(true)


    def handleMovieEvent(self, movieName, reason):
        self.output('movieevent')
        if (self.showFlybys and self.inMovie):
            PtAtTimeCallback(self.callersKey, self.movieReplayDelay, self.kDustinMovie)


    def handleTimer(self, id):
        if (id == self.kDustinMovie):
            self.output('handletimer')
            if self.inMovie:
                movieName = self.getFlyby(self.curBookAge)
                if (movieName == ''):
                    movieName = 'avi/UruAgeManager.bik'
                else:
                    movieName = ('avi/' + self.getFlyby(self.curBookAge))
                self.movie = None
                self.movie = ptMoviePlayer(movieName, self.callersKey)
                self.movie.play()


    def handleNotify(self, state, id, events):
        for event in events:
            if (event[0] == PtEventType.kBook):
                if (event[1] == PtBookEventTypes.kNotifyImageLink):
                    if ((self.curBookAge != None) and (self.curBookSpawnpoint != None)):
                        if (not self.showFlybys):
                            self.book.hide()
                            self.linkToAge(self.curBookAge, self.curBookSpawnpoint)
                            self.curBookAge = None
                            self.curBookSpawnpoint = None
                            self.inMovie = false
                            if self.movie:
                                self.movie.stop()
                                self.movie = None
                        else:
                            self.book.hide()
                            PtSetGlobalClickability(false)
                            PtGUICursorDimmed()
                            PtDisableRenderScene()
                            self.inMovie = true
                            PtAtTimeCallback(self.callersKey, self.movieReplayDelay, self.kDustinMovie)
                elif (event[1] == PtBookEventTypes.kNotifyShow):
                    pass
                elif (event[1] == PtBookEventTypes.kNotifyHide):
                    self.output('notifyhide')
                    self.book = None



    def OnNotify(self, state, id, events):
        for event in events:
            self.output(((((('uam: event 0:' + str(event[0])) + ' 1:') + str(event[1])) + ' 2:') + str(event[2])))
        return


    def getVersion(self):
        return 16


    def useAgeBook(self, agename, keyToUse, cover = None, linkingImage = None, showText = false, showFlyby = false):
        self.showFlybys = showFlyby
        self.curBookAge = None
        self.curBookSpawnpoint = None
        contents = ''
        if (cover != None):
            contents = (((contents + '<cover src="') + cover) + '">')
        if self.isAgeInstalled(agename):
            self.curBookAge = agename
            self.curBookSpawnpoint = self.getSpawnpoint(agename)
        if ((self.curBookAge == None) or ((self.curBookSpawnpoint == None) or ((self.curBookAge == '') or (self.curBookSpawnpoint == '')))):
            self.curBookAge = None
            self.curBookSpawnpoint = None
            contents = (contents + '<font size=28 face=Uru ><p align=center >This Age is not installed.\n\n')
            if showText:
                contents = (((contents + self.getDescription(agename)) + '\n\n<font size=24 face=Uru>') + self.getText(agename))
            if (linkingImage != None):
                contents = (((contents + '<pb><img src="') + linkingImage) + '" align=center blend=alpha >')
            else:
                contents = (contents + '<pb><img src="xLinkPanelBlackVoid*1#0.hsm" align=center blend=alpha >')
        else:
            contents = (contents + '<font size=28 face=Uru ><p align=center >')
            if showText:
                contents = (((contents + self.getDescription(agename)) + '\n\n<font size=24 face=Uru>') + self.getText(agename))
            if (linkingImage != None):
                contents = (((contents + '<pb><img src="') + linkingImage) + '" align=center link=100 blend=alpha >')
            else:
                contents = (contents + '<pb><img src="xLinkPanelBlackVoid*1#0.hsm" align=center link=100 blend=alpha >')
        self.output('Dustin: UAM: ', contents)
        self.callersKey = keyToUse
        self.book = ptBook(contents, self.callersKey)
        self.book.setSize(1.0, 1.0)
        self.book.setGUI('BkBook')
        self.book.allowPageTurning(true)
        if (cover == None):
            self.book.show(1)
        else:
            self.book.show(0)
        self.output('uam10g')


    def showBook(self, contents, keyToUse):
        self.curBookAge = None
        self.curBookSpawnpoint = None
        self.output('got to showjournal')
        self.callersKey = keyToUse
        self.output('got to 2')
        self.book = ptBook(contents, self.callersKey)
        self.output('uamf10a')
        self.book.setSize(1.0, 1.0)
        self.output('10b')
        self.book.setGUI('BkBook')
        self.output('10c')
        self.book.allowPageTurning(true)
        self.output('10d')
        if (contents.find('<cover') > -1):
            self.output('cover')
            self.book.show(0)
        else:
            self.output('nocover')
            self.book.show(1)
        self.output('10e')
        self.output('10f')
        self.output('uam10g')


    def showBahroStone(self, contents, keyToUse):
        self.curBookAge = None
        self.curBookSpawnpoint = None
        self.output('got to showjournal')
        self.callersKey = keyToUse
        self.output('got to 2')
        self.book = ptBook(contents, self.callersKey)
        self.output('uamf10a')
        self.book.setSize(1.0, 1.0)
        self.output('10b')
        self.book.setGUI('bkBahroRockBook')
        self.output('10c')
        self.book.allowPageTurning(false)
        self.output('10d')
        self.book.show(1)
        self.output('10e')
        self.output('10f')
        self.output('uam10g')


    def showNotebook(self, contents, keyToUse):
        self.curBookAge = None
        self.curBookSpawnpoint = None
        self.output('got to showjournal')
        self.callersKey = keyToUse
        self.output('got to 2')
        self.book = ptBook(contents, self.callersKey)
        self.output('uamf10a')
        self.book.setSize(1.0, 1.0)
        self.output('10b')
        self.book.setGUI('bkNotebook')
        self.output('10c')
        self.book.allowPageTurning(true)
        self.output('10d')
        if (contents.find('<cover') > 0):
            self.output('cover')
            self.book.show(0)
        else:
            self.output('nocover')
            self.book.show(1)
        self.output('10e')
        self.output('10f')
        self.output('uam10g')


    def output(self, *messages):
        if self.debug:
            message = ''
            i = 0
            while (i < len(messages)):
                message = (message + str(messages[i]))
                i = (i + 1)
            #Dustin new start
            print message
            return
            #Dustin new end


    def getListOfAges(self):
        result = []
        ini = None
        return result


    def getLinkingImage(self, ageName):
        result = ''
        ini = None
        return result


    def getFlyby(self, ageName):
        result = ''
        ini = None
        return result


    def getText(self, ageName):
        result = ''
        ini = None
        return result


    def getDescription(self, ageName):
        result = ''
        ini = None
        return result


    def getSpawnpoint(self, ageName):
        #Dustin start new
        if(self.isAgeInstalled(ageName)):
            return "LinkInPointDefault"
        else:
            return ""
        #Dustin end new


    def isAgeInstalled(self, ageName):
        return xLinkMgr.IsAgeAvailable(ageName)


    def linkToAge(self, ageName, spawnPoint):
        xLinkMgr.LinkToAge(ageName, spawnPoint)


uam = TUruAgeManager()
