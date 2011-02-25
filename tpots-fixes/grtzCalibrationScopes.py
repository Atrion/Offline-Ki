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
MaxVersionNumber = 1
MinorVersionNumber = 6
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import PlasmaControlKeys
import string
import time
Activate = ptAttribActivator(1, 'clk: Activate the scope')
Behavior = ptAttribBehavior(2, 'mlt stg: Scope behavior', netForce=1)
MarkerGameDlg = ptAttribGUIDialog(3, 'Calibration Marker GUI')
MGAnim = ptAttribAnimation(4, 'anim: Turn On/Off entire')
MGMachineOnResp = ptAttribResponder(5, 'resp: Turn On')
MGMachineOffResp = ptAttribResponder(6, 'resp: Turn Off')
ScopeNum = ptAttribInt(7, 'Scope #')
RespMarkerBtn = ptAttribResponder(8, 'resp: GUI marker btn', ['Dim', 'Glow', 'Blink'])
RespMarkerIcon = ptAttribResponder(9, 'resp: marker icon', ['Off', 'On'])
RespGZActive = ptAttribResponder(10, 'resp: GZ active', ['Off', 'On'])
RespGZActiveAtStart = ptAttribResponder(11, 'resp: GZ active - on init ONLY', ['Off', 'On'])
RespVignettes = ptAttribResponder(12, 'resp: marker GUI vignettes', ['Arc', 'Dist', 'Elev', 'Final', 'Off'])
RespSmallIcons = ptAttribResponder(13, 'resp: GUI small icons', ['Arc', 'Dist', 'Elev'])
kCalibrationBtn = 500
LocalAvatar = None
boolScopeOperator = 0
boolOperated = 0
Telescope = ptInputInterface()
listScopeMarkers = [kCGZToransGame, kCGZHSpansGame, kCGZVSpansGame, kCGZActivateGZ]
ThisMarker = 0
#GZon = 0
markerBtn = None
listVignettes = ['Arc', 'Dist', 'Elev', 'Final']
ThisVignette = None

class grtzCalibrationScopes(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 215
        self.version = MaxVersionNumber
        PtDebugPrint(('grtzCalibrationScopes: Max version %d - minor version %d' % (MaxVersionNumber, MinorVersionNumber)), level=kDebugDumpLevel)


    def OnFirstUpdate(self):
        self.SDL.setDefault('boolOperated', (0,))
        self.SDL.setDefault('OperatorID', (-1,))
        self.SDL.sendToClients('boolOperated')
        self.SDL.sendToClients('OperatorID')


    def OnServerInitComplete(self):
        global ThisMarker
        global ThisVignette
        ageSDL = PtGetAgeSDL()
        ageSDL.setFlags('grtzGZActive', 1, 1)
        ageSDL.sendToClients('grtzGZActive')
        ageSDL.setNotify(self.key, 'grtzGZActive', 0.0)
        ThisMarker = listScopeMarkers[(ScopeNum.value - 1)]
        ThisVignette = listVignettes[(ScopeNum.value - 1)]
        PtLoadDialog('CalibrationMarkerGameGUI', self.key)
        RespMarkerBtn.run(self.key, state='Dim', fastforward=1)
        RespMarkerIcon.run(self.key, state='Off', fastforward=1)
        RespVignettes.run(self.key, state='Off', fastforward=1)
        try:
            boolGZActive = ageSDL['grtzGZActive'][0]
        except:
            PtDebugPrint('ERROR: grtzCalibrationScopes.OnServerInitComplete():\tERROR reading SDL name for GZActive')
            boolGZActive = 0
        PtDebugPrint(('DEBUG: grtzCalibrationScopes.OnServerInitComplete():\t grtzGZActive = %d' % ageSDL['grtzGZActive'][0]))
        if boolGZActive:
            RespGZActiveAtStart.run(self.key, state='On')
        else:
            RespGZActiveAtStart.run(self.key, state='Off')
        MarkerState = PtGetCGZGameState(ThisMarker)
        if (ScopeNum.value != 4):
            if (MarkerState == '3'):
                RespSmallIcons.run(self.key, state=ThisVignette)
        self.AddSharperJournalChron('sjGreatZeroVisited')


    def AddSharperJournalChron(self, var):
        vault = ptVault()
        entry = vault.findChronicleEntry(var)
        if (not entry):
            vault.addChronicleEntry(var, 0, str(int(time.time())))


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
# Manually control GZ machine BEGIN
        if (VARname != 'grtzGZActive'):
            return
        ageSDL = PtGetAgeSDL()
        if ageSDL['grtzGZActive'][0]:
            RespGZActive.run(self.key, state='On')
        else:
            RespGZActive.run(self.key, state='Off')
# Manually control GZ machine END


    def Load(self):
        solo = true
        if len(PtGetPlayerList()):
            solo = false
        boolOperated = self.SDL['boolOperated'][0]
        if boolOperated:
            if solo:
                PtDebugPrint(('grtzCalibrationScopes.Load():\tboolOperated=%d but no one else here...correcting' % boolOperated), level=kDebugDumpLevel)
                boolOperated = 0
                self.SDL['boolOperated'] = (0,)
                self.SDL['OperatorID'] = (-1,)
                Activate.enable()
            else:
                Activate.disable()
                PtDebugPrint(('grtzCalibrationScopes.Load():\tboolOperated=%d, disabling telescope clickable' % boolOperated), level=kDebugDumpLevel)


    def AvatarPage(self, avObj, pageIn, lastOut):
        if pageIn:
            return
        avID = PtGetClientIDFromAvatarKey(avObj.getKey())
        if (avID == self.SDL['OperatorID'][0]):
            Activate.enable()
            self.SDL['OperatorID'] = (-1,)
            self.SDL['boolOperated'] = (0,)
            PtDebugPrint('grtzCalibrationScopes.AvatarPage(): telescope operator paged out, reenabled telescope.', level=kDebugDumpLevel)
        else:
            return


    def __del__(self):
        PtUnloadDialog('CalibrationMarkerGameGUI')


    def OnNotify(self, state, id, events):
        global LocalAvatar
        global boolScopeOperator
        PtDebugPrint(('grtzCalibrationScopes:OnNotify  state=%f id=%d events=' % (state, id)), events, level=kDebugDumpLevel)
        if (state and ((id == Activate.id) and PtWasLocallyNotified(self.key))):
            RespVignettes.run(self.key, state=ThisVignette, fastforward=1)
            LocalAvatar = PtFindAvatar(events)
            self.IStartTelescope()
        for event in events:
            if ((event[0] == kMultiStageEvent) and (((event[1] == 0) or (event[1] == 1)) and (event[2] == kAdvanceNextStage))):
                if boolScopeOperator:
                    self.IEngageTelescope()
                    boolScopeOperator = 0
                break
        if (id == MGMachineOffResp.id):
            self.IQuitTelescope()
        if (id == RespGZActive.id):
            Activate.enable()
            PtDebugPrint('grtzCalibrationScopes.OnTimer:\tclickable reenabled', level=kDebugDumpLevel)
            PtSendKIMessage(kEnableKIandBB, 0)


    def OnGUINotify(self, id, control, event):
        global markerBtn
        if (id == MarkerGameDlg.id):
            PtDebugPrint(('grtzCalibrationScopes.OnGUINotify: id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
            if (event == kDialogLoaded):
                markerBtn = ptGUIControlButton(MarkerGameDlg.dialog.getControlFromTag(kCalibrationBtn))
                MGAnim.animation.skipToTime(1.5)
            elif (event == kShowHide):
                if control.isEnabled():
                    if (PtDetermineKIMarkerLevel() < kKIMarkerNormalLevel):
                        markerBtn.disable()
                    else:
                        MGMachineOnResp.run(self.key, netPropagate=0)
                        PtDebugPrint(('grtzCalibrationScopes: This is Scope# %d' % ScopeNum.value))
                        MarkerState = PtGetCGZGameState(ThisMarker)
                        if (MarkerState == '3'):
                            RespMarkerIcon.run(self.key, state='On', fastforward=1)
                        print 'PtGetCGZGameState = ',
                        print MarkerState
                        if (ScopeNum.value != 4):
                            for marker in listScopeMarkers:
                                CurState = PtGetCGZGameState(marker)
                                if (CurState == '2'):
                                    if (marker == ThisMarker):
                                        CurState = '0'
                                    else:
                                        break
                            if (CurState == '2'):
                                RespMarkerBtn.run(self.key, state='Dim', fastforward=1)
                                markerBtn.disable()
                            elif (MarkerState == '0'):
                                RespMarkerBtn.run(self.key, state='Glow', fastforward=1)
                                markerBtn.enable()
                            else:
                                if (MarkerState == '1'):
                                    RespMarkerBtn.run(self.key, state='Blink')
                                elif (MarkerState == '2'):
                                    print 'Marker was captured, will now upload...'
                                    RespMarkerBtn.run(self.key, state='Dim')
                                    RespMarkerIcon.run(self.key, state='On')
                                    RespSmallIcons.run(self.key, state=ThisVignette)
                                    PtSetCGZGameState(ThisMarker, kGZMarkerUploaded)
                                    PtUpdateGZGamesChonicles(0, 'off', 'off', 0, 0)
                                    PtSendKIMessage(kGZUpdated, 0)
                                elif (MarkerState == '3'):
                                    RespMarkerBtn.run(self.key, state='Dim', fastforward=1)
                                markerBtn.disable()
                        else:
                            for marker in listScopeMarkers:
                                if (marker != ThisMarker):
                                    CurState = PtGetCGZGameState(marker)
                                    if (CurState != '3'):
                                        break
                            if (CurState != '3'):
                                RespMarkerBtn.run(self.key, state='Dim', fastforward=1)
                                markerBtn.disable()
                            elif (MarkerState == '0'):
                                RespMarkerBtn.run(self.key, state='Glow')
                                markerBtn.enable()
                            elif (MarkerState == '1'):
                                RespMarkerBtn.run(self.key, state='Blink')
                                markerBtn.disable()
                            elif (MarkerState == '2'):
                                print 'Final marker was captured!  Will now upload marker and activate GZ...'
                                RespMarkerBtn.run(self.key, state='Dim')
                                RespMarkerIcon.run(self.key, state='On')
                                markerBtn.disable()
                                PtSetCGZGameState(ThisMarker, kGZMarkerUploaded)
                                PtUpdateGZGamesChonicles(0, 'off', 'off', 0, 0)
                                PtSendKIMessage(kGZUpdated, 0)
                                PtAtTimeCallback(self.key, 1.5, 3)
                            elif (MarkerState == '3'):
                                RespMarkerBtn.run(self.key, state='Dim', fastforward=1)
                                markerBtn.disable()
                else:
                    MGAnim.animation.skipToTime(1.5)
            elif (event == kAction):
                if (type(control) != type(None)):
                    btnID = control.getTagID()
                    if (btnID == kCalibrationBtn):
                        if (isinstance(control, ptGUIControlButton) and control.isButtonDown()):
                            PtDebugPrint('grtzCalibrationScopes.GUINotify: Calibration button down', level=kDebugDumpLevel)
                        else:
                            PtDebugPrint('grtzCalibrationScopes.GUINotify: Calibration button up', level=kDebugDumpLevel)
                            print 'Marker button pressed...'
                            RespMarkerBtn.run(self.key, state='Dim', fastforward=1)
                            RespMarkerBtn.run(self.key, state='Blink')
                            markerBtn.disable()
                            for marker in listScopeMarkers:
                                CurState = PtGetCGZGameState(marker)
                                if (CurState == '1'):
                                    if (marker != ThisMarker):
                                        PtSetCGZGameState(marker, kCGZMarkerInactive)
                            PtSetCGZGameState(ThisMarker, kCGZMarkerAvailable)
                            PtUpdateGZGamesChonicles(1, 'yellow', 'yellowlt', 0, 1)
                            PtSendKIMessage(kGZUpdated, 0)


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            MGMachineOffResp.run(self.key, netPropagate=0)
        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
            MGMachineOffResp.run(self.key, netPropagate=0)


    def IStartTelescope(self):
        global boolScopeOperator
        PtSendKIMessage(kDisableKIandBB, 0)
        Activate.disable()
        boolScopeOperator = 1
        self.SDL['boolOperated'] = (1,)
        avID = PtGetClientIDFromAvatarKey(LocalAvatar.getKey())
        self.SDL['OperatorID'] = (avID,)
        PtDebugPrint('grtzCalibrationScopes.OnNotify:\twrote SDL - scope operator id = ', avID, level=kDebugDumpLevel)
        Behavior.run(LocalAvatar)


    def IEngageTelescope(self):
        Telescope.pushTelescope()
        if PtIsDialogLoaded('CalibrationMarkerGameGUI'):
            PtLoadDialog('CalibrationMarkerGameGUI', self.key)
            if PtIsDialogLoaded('CalibrationMarkerGameGUI'):
                PtShowDialog('CalibrationMarkerGameGUI')
        PtEnableControlKeyEvents(self.key)


    def IQuitTelescope(self):
        global boolScopeOperator
        Telescope.popTelescope()
        PtHideDialog('CalibrationMarkerGameGUI')
        RespMarkerBtn.run(self.key, state='Dim', fastforward=1)
        RespMarkerIcon.run(self.key, state='Off', fastforward=1)
        RespVignettes.run(self.key, state='Off', fastforward=1)
        PtAtTimeCallback(self.key, 0.5, 1)
        PtDisableControlKeyEvents(self.key)
        boolScopeOperator = 0
        self.SDL['boolOperated'] = (0,)
        self.SDL['OperatorID'] = (-1,)
        PtDebugPrint('grtzCalibrationScopes.IQuitMarkerScope:\tdelaying clickable reenable', level=kDebugDumpLevel)


    def OnTimer(self, id):
        #global GZon
        if (id == 1):
            Behavior.gotoStage(LocalAvatar, 3)
            PtAtTimeCallback(self.key, 1.5, 2)
        if (id == 2):
            #if GZon:
            #    GZon = 0
            #else:
                Activate.enable()
                PtDebugPrint('grtzCalibrationScopes.OnTimer:\tclickable reenabled', level=kDebugDumpLevel)
                PtSendKIMessage(kEnableKIandBB, 0)
        if (id == 3):
            self.AddSharperJournalChron('sjGreatZeroCompleted')
# Manually control GZ machine online BEGIN
            #ageSDL = PtGetAgeSDL()
            #ageSDL['grtzGZActive'] = (1,)
            import xxConfig
            if xxConfig.isOffline(): PtAtTimeCallback(self.key, 1, 4)
        if (id == 4):
            ageSDL = PtGetAgeSDL()
            ageSDL['grtzGZActive'] = (1,)
            #GZon = 1
            #RespGZActive.run(self.key, state='On')
            MGMachineOffResp.run(self.key, netPropagate=0)
# Manually control GZ machine online END


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



