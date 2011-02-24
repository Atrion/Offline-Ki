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
import string
import time
import os
variable = None
BooleanVARs = ['nb01LinkBookEderVis', 'nb01LinkBookGarrisonVis', 'nb01LinkBookTeledahnVis', 'nb01RatCreatureVis']
AgeStartedIn = None
nb01Ayhoheek5Man1StateMaxINT = 3
nb01PuzzleWallStateMaxINT = 3

# heek table objects
TPOTSHeekObjects = ['aAyoheekTable01', 'azAyoheekTable', 'Cylinder01', 'DnjiBBoard', 'DnjiBBoard01', 'DnjiBBoard02', 'DnjiBBoard03',  'DnjiDummy01', 'DnjiDummy03', 'DnjiDummy04', 'DnjiDummy05', 'DnjiDummyANIMATED', 'GameTableRTOmni', 'GameTableShadowDecal', 'HeekPiece', 'SfxHeekDrone01LEmit', 'SfxHeekDrone01REmit', 'Line01', 'Line02', 'Line03', 'Line04', 'Line05']
TPOTSHeekSoundObjects = {'cSfxHeekDroneL': 'SfxHeekDrone01LEmit', 'cSfxHeekDroneR': 'SfxHeekDrone01REmit'}
TPOTSHeekVisible = True


def TPOTSHeekTableState(visible):
    global TPOTSHeekVisible
    if visible == TPOTSHeekVisible: return
    for object in TPOTSHeekObjects:
        if visible:
            object.draw.enable()
            object.physics.suppress(False)
        else:
            object.draw.disable()
            object.physics.suppress(True)
    # Known issue: The sound will not be disabled/enabled correctly before doing a re-link
    for soundName in TPOTSHeekSoundObjects:
        object = TPOTSHeekSoundObjects[soundName]
        index = object.getSoundIndex(soundName)
        if visible:
            object.setSoundFilename(index, 'sfx/NB01AhyoheekDrone_Loop.ogg', 1)
        else:
            object.setSoundFilename(index, 'sound-which-does-not-exist.ogg', 1) # disable sound by passing a non-existing file
    TPOTSHeekVisible = visible


def OutOfRange(VARname, NewSDLValue, myMaxINT):
    PtDebugPrint(('ERROR: nb01EmgrPhase0.OutOfRange:\tERROR: Variable %s expected range from  0 - %d. Received value of %d' % (VARname, NewSDLValue, myMaxINT)))


def Ayhoheek5Man1State(VARname, NewSDLValue):
    if (NewSDLValue > nb01Ayhoheek5Man1StateMaxINT):
        OutOfRange(VARname, NewSDLValue, nb01Ayhoheek5Man1StateMaxINT)
        return
    if not os.path.exists('dat/Neighborhood_District_nb01Ayhoheek5Man1State.prp'):
        NewSDLValue = 3 # old broken table only
    TPOTSHeekTableState(NewSDLValue == 3)
    if (NewSDLValue == 0) or (NewSDLValue == 3):
        PtDebugPrint('DEBUG: nb01EmgrPhase0.Ayhoheek5Man1State:\t Paging out 5 Man Heek table completely.')
        PtPageOutNode('nb01Ayhoheek5Man1State')
        PtPageOutNode('nb01Ayhoheek5Man1Dead')
    elif (NewSDLValue == 1):
        PtDebugPrint('DEBUG: nb01EmgrPhase0.Ayhoheek5Man1State:\t Paging in broken 5 Man Heek table.')
        PtPageInNode('nb01Ayhoheek5Man1Dead')
        PtPageOutNode('nb01Ayhoheek5Man1State')
    elif (NewSDLValue == 2):
        PtDebugPrint('DEBUG: nb01EmgrPhase0.Ayhoheek5Man1State:\t Paging in functional 5 Man Heek table.')
        PtPageInNode('nb01Ayhoheek5Man1State')
        PtPageOutNode('nb01Ayhoheek5Man1Dead')
    else:
        PtDebugPrint(('ERROR: nb01EmgrPhase0.Ayhoheek5Man1State: \tERROR: Unexpected value. VARname: %s NewSDLValue: %s' % (VARname, NewSDLValue)))


def CityLightsArchState(VARname, NewSDLValue):
    print 'CityLightsArchiState Notified.'
    print 'VARname = ',
    print VARname
    print 'Received value is ',
    print NewSDLValue


def PuzzleWallState(VARname, NewSDLValue):
    print 'PuzzleWallState Notified.'
    print 'VARname = ',
    print VARname
    print 'Received value is ',
    print NewSDLValue

StateVARs = {
    'nb01Ayhoheek5Man1State': Ayhoheek5Man1State,
    'nb01PuzzleWallState': PuzzleWallState
}

def UpdateRecentVisitors(timerKey, prevplayers = [], deviceName = 'D\'ni  Imager Right'):
    def FormatPlayerInfo(playername, timestr = None):
        if timestr == None:
            currenttime = time.gmtime(PtGetDniTime())
            timestr = time.strftime('%m/%d/%Y %I:%M %p', currenttime)
        return timestr + (' ' * (30 - len(timestr))) + playername
    
    try:
        AmCCR = ptCCRMgr().getLevel()
    except:
        AmCCR = 0
    if (not AmCCR):
        deviceNode = None
        deviceInbox = None
        playerlist = None
        avault = ptAgeVault()
        adevicesfolder = avault.getAgeDevicesFolder()
        adevices = adevicesfolder.getChildNodeRefList()
        for device in adevices:
            device = device.getChild()
            devicetn = device.upcastToTextNoteNode()
            if (devicetn and (devicetn.getTitle() == deviceName)):
                deviceNode = devicetn
                break
        if (not (deviceNode)):
            PtAtTimeCallback(timerKey, 1, 1)
        else:
            inboxes = deviceNode.getChildNodeRefList()
            for inbox in inboxes:
                inbox = inbox.getChild()
                inboxfolder = inbox.upcastToFolderNode()
                if inboxfolder:
                    deviceInbox = inboxfolder
                    break
            if (not (deviceInbox)):
                PtAtTimeCallback(timerKey, 1, 1)
            else:
                items = deviceInbox.getChildNodeRefList()
                for item in items:
                    item = item.getChild()
                    itemtn = item.upcastToTextNoteNode()
                    if itemtn:
                        if (itemtn.getTitle() == 'Visitors, Visiteurs, Besucher'):
                            playerlist = itemtn
                            break
                        elif (itemtn.getTitle() == 'Most Recent Visitors'):
                            itemtn.setTitle('Visitors, Visiteurs, Besucher')
                            playerlist = itemtn
                            break
                hiddentextstr = 'Exp1'
                if playerlist:
                    # existing player list found, update it
                    if (PtDetermineKILevel() == kNormalKI):
                        # get text (without those hiddentext leftovers)
                        thetext = playerlist.getText().replace('<hiddentext>Exp1</hiddentext>', '')
                        # build new text for us
                        newtext = FormatPlayerInfo(PtGetLocalPlayer().getPlayerName()) + '\n'
                        # truncate text if we add anything
                        while ((thetext.count('\n') + 1) > 15):
                            thetext = thetext[:thetext.rfind('\n')]
                        thetext = newtext + thetext
                        playerlist.setText(thetext)
                        playerlist.save()
                else: # also do this for players without the KI, so that they see the logger correctly initialized
                    thetext = ''
                    # build text for current player, if he should appear on it
                    if (PtDetermineKILevel() == kNormalKI):
                        thetext += FormatPlayerInfo(PtGetLocalPlayer().getPlayerName()) + '\n'
                    # add hard-coded "previous" players after current one
                    for p in prevplayers:
                        thetext += (FormatPlayerInfo(p[1], p[0]) + '\n')
                    # save to the vault
                    playerlist = ptVaultTextNoteNode()
                    playerlist.setTitle('Visitors, Visiteurs, Besucher')
                    playerlist.setText(thetext)
                    deviceInbox.addNode(playerlist)


class nb01EmgrPhase0(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5222
        version = 7
        self.version = version
        self.prevplayers = [('03/03/2004 05:36 PM', 'Douglas Sharper'), ('03/02/2004 09:12 AM', 'Douglas Sharper'), ('02/09/2004 10:46 PM', 'tah'), ('02/09/2004 09:32 PM', 'RIUM+'), ('02/09/2004 09:15 PM', 'lonelyto25'), ('02/09/2004 08:29 PM', 'Tijara'), ('02/09/2004 08:18 PM', 'Kehrin'), ('02/09/2004 07:52 PM', 'Kirsehn'), ('02/09/2004 07:39 PM', 'Beefo laRue'), ('02/09/2004 07:26 PM', 'Loriendil'), ('02/09/2004 07:06 PM', 'Kahlis'), ('02/09/2004 06:45 PM', '75th Trombone'), ('02/09/2004 06:00 PM', 'Aloys'), ('02/09/2004 05:45 PM', 'Je\'uhl'), ('02/09/2004 05:38 PM', 'Toh\'mas')]
        print '__init__nb01EmgrPhase0 v.',
        print version


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        # TPOTS heek table. This has to be done in OnFirstUpdate - every other location I tried (including OnServerInitComplete and directly in the Python file) got some objects wrong
        global TPOTSHeekObjects, TPOTSHeekSoundObjects
        names = TPOTSHeekObjects
        TPOTSHeekObjects = [] # re-fill array with objects instead of names
        for name in names:
            TPOTSHeekObjects.append(PtFindSceneobject(name, 'Neighborhood'))
        for soundName in TPOTSHeekSoundObjects:
            TPOTSHeekSoundObjects[soundName] = PtFindSceneobject(TPOTSHeekSoundObjects[soundName], 'Neighborhood')


    def OnServerInitComplete(self):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            for variable in BooleanVARs:
                ageSDL.setNotify(self.key, variable, 0.0)
                self.IManageBOOLs(variable, '')
            for variable in StateVARs:
                ageSDL.setNotify(self.key, variable, 0.0)
                StateVARs[variable](variable, ageSDL[variable][0])
        UpdateRecentVisitors(self.key, self.prevplayers)
        self.AddSharperJournalChron()


    def AddSharperJournalChron(self):
        vault = ptVault()
        entry = vault.findChronicleEntry('sjBevinVisted')
        if (not entry):
            vault.addChronicleEntry('sjBevinVisted', 0, str(int(time.time())))


    def OnTimer(self, id):
        if (id == 1):
            UpdateRecentVisitors(self.key, self.prevplayers)


    def OnSDLNotify(self, VARname, SDLname, PlayerID, tag):
        if (VARname in BooleanVARs):
            self.IManageBOOLs(VARname, SDLname)
        elif (VARname in StateVARs.keys()):
            if (AgeStartedIn == PtGetAgeName()):
                ageSDL = PtGetAgeSDL()
                NewSDLValue = ageSDL[VARname][0]
                StateVARs[VARname](VARname, NewSDLValue)
        else:
            PtDebugPrint(('ERROR: nb01EmgrPhase0.OnSDLNotify:\tERROR: Variable %s was not recognized as a Boolean, Performance, or State Variable. ' % VARname))


    def IManageBOOLs(self, VARname, SDLname):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            try:
                if (ageSDL[VARname][0] == 1):
                    PtDebugPrint('DEBUG: nb01EmgrPhase0.IManageBOOLs:\tPaging in room ', VARname)
                    PtPageInNode(VARname)
                elif (ageSDL[VARname][0] == 0):
                    print 'variable = ',
                    print VARname
                    PtDebugPrint('DEBUG: nb01EmgrPhase0.IManageBOOLs:\tPaging out room ', VARname)
                    PtPageOutNode(VARname)
                else:
                    sdlvalue = ageSDL[VARname][0]
                    PtDebugPrint(('ERROR: nb01EmgrPhase0.IManageBOOLs:\tVariable %s had unexpected SDL value of %s' % (VARname, sdlvalue)))
            except:
                PtDebugPrint(('ERROR: nb01EmgrPhase0.IManageBOOLs: problem with %s' % VARname))


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



