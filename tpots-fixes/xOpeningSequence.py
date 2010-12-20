# -*- coding: utf-8 -*-
MaxVersionNumber = 1
MinorVersionNumber = 4
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaConstants import *
import xLocalization
import PlasmaControlKeys
import os
import xIniDisplay
IntroMovieDlg = ptAttribGUIDialog(1, 'The Intro Movie dialog')
FirstHelpDlg = ptAttribGUIDialog(2, 'The First Help dialog')
gIntroMovie = None
kAtrusIntroMovie = 'avi/AtrusIntro.bik'
gIntroStarted = 0
gOriginalAmbientVolume = 1.0
gOriginalSFXVolume = 1.0
gTotalTickTime = 20.0
gCurrentTick = 0.0
gIntroByTimer = 0
kIntroPauseID = 1
kIntroPauseSeconds = 3.0
kIntroFadeOutID = 2
kIntroFadeOutSeconds = 2.0
kHelpFadeInSeconds = 3.0
kStartGameFadeOutID = 3
kStartGameFadeOutSeconds = 0.5
kStartGameFadeInSeconds = 0.5
kFakeMovieTimeID = 50
kFakeMovieSeconds = 10.0
kSoundFadeInID = 99
kSoundTickTime = 0.10000000000000001
kIntroPlayedChronicle = 'IntroPlayed'
kFirstHelpOkBtn = 310
kNormNoviceRGID = 700
kHelpTitle = 600
kWalkText = 610
kRunText = 611
kTurnLeftText = 612
kBackwardsText = 613
kTurnRightText = 614
kToggleViewText = 615
kJumpText = 616
kMouseWalkText = 620
kMouseRunText = 621
kSelectText = 622
kMousePanCam = 623
kMouseBackwards = 624
kMousePresetsTitle = 630
kMouseNormalText = 631
kMouseNoviceText = 632
kOkButton = 650

class xOpeningSequence(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 194
        self.version = MaxVersionNumber
        PtDebugPrint(('__xOpeningSequence: Max version %d - minor version %d' % (MaxVersionNumber, MinorVersionNumber)))


    def OnFirstUpdate(self):
        global gCurrentTick
        global gOriginalAmbientVolume
        global gIntroByTimer
        global gOriginalSFXVolume
        PtLoadDialog('IntroMovieGUI', self.key)
        PtLoadDialog('StartupHelpGUI', self.key)
        PtLoadDialog('IntroBahroBgGUI', self.key)
        gCurrentTick = 0
        try:
            avatar = PtGetLocalAvatar()
            avatar.avatar.registerForBehaviorNotify(self.key)
            gIntroByTimer = 0
        except:
            PtDebugPrint('xOpeningSequence failed to get local avatar')
            gIntroByTimer = 1
            return
        PtDisableRenderScene()
        PtGUICursorOff()
        audio = ptAudioControl()
        gOriginalAmbientVolume = audio.getAmbienceVolume()
        audio.setAmbienceVolume(0.0)
        gOriginalSFXVolume = audio.getSoundFXVolume()
        audio.setSoundFXVolume(0.0)


    def __del__(self):
        PtDebugPrint('xOpeningSequence::destructor... we\'re gone!', level=kDebugDumpLevel)


    def AvatarPage(self, sobj, unload, lastout):
        pass


    def OnGUINotify(self, id, control, event):
        global gIntroMovie
        PtDebugPrint(('xOpeningSequence::OnGUINotify id=%d, event=%d control=' % (id, event)), control, level=kDebugDumpLevel)
        if (id == IntroMovieDlg.id):
            if (event == kDialogLoaded):
                pass
            elif (event == kShowHide):
                if control.isEnabled():
                    pass
            elif ((event == kAction) or (event == kValueChanged)):
                imID = control.getTagID()
            elif (event == kExitMode):
                self.IStartHelp()
        elif (id == FirstHelpDlg.id):
            if (event == kDialogLoaded):
                skipMovie = 1
                try:
                    os.stat(kAtrusIntroMovie)
                    PtShowDialog('IntroBahroBgGUI')
                    skipMovie = 0
                except:
                    skipMovie = 1
                if skipMovie:
                    PtEnableRenderScene()
                    PtGUICursorOn()
                    FirstHelpDlg.dialog.show()
                    PtDebugPrint('xOpeningSequence - no intro movie!!!', level=kDebugDumpLevel)
                PtDebugPrint('xOpeningSequence - quiet sounds and show background', level=kDebugDumpLevel)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kHelpTitle))
                textField.setString(xLocalization.xOptions.xSUHHelpTitle)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kWalkText))
                textField.setString(xLocalization.xOptions.xSUHWalkText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kRunText))
                textField.setString(xLocalization.xOptions.xSUHRunText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kTurnLeftText))
                textField.setString(xLocalization.xOptions.xSUHTurnLeftText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kBackwardsText))
                textField.setString(xLocalization.xOptions.xSUHBackwardsText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kTurnRightText))
                textField.setString(xLocalization.xOptions.xSUHTurnRightText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kToggleViewText))
                textField.setString(xLocalization.xOptions.xSUHToggleViewText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kJumpText))
                textField.setString(xLocalization.xOptions.xSUHJumpText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kMouseWalkText))
                textField.setString(xLocalization.xOptions.xSUHMouseWalkText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kMouseRunText))
                textField.setString(xLocalization.xOptions.xSUHMouseRunText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kSelectText))
                textField.setString(xLocalization.xOptions.xSUHSelectText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kMousePanCam))
                textField.setString(xLocalization.xOptions.xSUHMousePanCam)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kMouseBackwards))
                textField.setString(xLocalization.xOptions.xSUHMouseBackwards)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kMousePresetsTitle))
                textField.setString(xLocalization.xOptions.xSUHMousePresetsTitle)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kMouseNormalText))
                textField.setString(xLocalization.xOptions.xSUHMouseNormalText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kMouseNoviceText))
                textField.setString(xLocalization.xOptions.xSUHMouseNoviceText)
                textField = ptGUIControlTextBox(FirstHelpDlg.dialog.getControlFromTag(kOkButton))
                textField.setString(xLocalization.xOptions.xSUHOkButton)
            elif (event == kShowHide):
                if control.isEnabled():
                    nnRG = ptGUIControlRadioGroup(FirstHelpDlg.dialog.getControlFromTag(kNormNoviceRGID))
                    if PtIsClickToTurn():
                        nnRG.setValue(1)
                    else:
                        nnRG.setValue(0)
                    xIniDisplay.ReadIni()
                else:
                    xIniDisplay.WriteIni()
            elif ((event == kAction) or (event == kValueChanged)):
                helpID = control.getTagID()
                if (helpID == kFirstHelpOkBtn):
                    nnRG = ptGUIControlRadioGroup(FirstHelpDlg.dialog.getControlFromTag(kNormNoviceRGID))
                    if (nnRG.getValue() == 1):
                        PtSetClickToTurn(1)
                        xIniDisplay.SetClickToTurn()
                    else:
                        PtSetClickToTurn(0)
                        xIniDisplay.RemoveClickToTurn()
                    self.IStartGame()
            elif (event == kExitMode):
                self.IStartGame()
        elif (id == -1):
            if (event == kShowHide):
                if control.isEnabled():
                    gIntroMovie = ptMoviePlayer(kAtrusIntroMovie, self.key)
                    gIntroMovie.playPaused()
                    if gIntroByTimer:
                        PtAtTimeCallback(self.key, kIntroPauseSeconds, kIntroPauseID)


    def OnBehaviorNotify(self, type, id, state):
        PtDebugPrint(('xOpeningSequence.OnBehaviorNotify(): %d' % type))
        if ((type == PtBehaviorTypes.kBehaviorTypeLinkIn) and (not state)):
            self.IStartMovie()
            avatar = PtGetLocalAvatar()
            avatar.avatar.unRegisterForBehaviorNotify(self.key)


    def OnTimer(self, id):
        if (id == kIntroPauseID):
            self.IStartMovie()
        elif (id == kFakeMovieTimeID):
            self.IStartHelp()
        elif (id == kIntroFadeOutID):
            self.IFinishStartHelp()
        elif (id == kStartGameFadeOutID):
            self.IFinishStartGame()
        elif (id == kSoundFadeInID):
            self.IUpdateSounds()


    def OnMovieEvent(self, movieName, reason):
        PtDebugPrint('xOpeningSequence: movie done ', level=kDebugDumpLevel)
        if gIntroMovie:
            self.IStartHelp()


    def IStartMovie(self):
        global gIntroStarted
        if gIntroMovie:
            if (not gIntroStarted):
                IntroMovieDlg.dialog.show()
                gIntroMovie.resume()
                PtDebugPrint('xOpeningSequence - playing movie', level=kDebugDumpLevel)
            else:
                PtDebugPrint('xOpeningSequence - movie already playing', level=kDebugDumpLevel)
            gIntroStarted = 1


    def IStartHelp(self):
        PtFadeOut(kIntroFadeOutSeconds, 1)
        PtAtTimeCallback(self.key, kIntroFadeOutSeconds, kIntroFadeOutID)


    def IFinishStartHelp(self):
        global gIntroMovie
        PtHideDialog('IntroBahroBgGUI')
        if gIntroMovie:
            gIntroMovie.stop()
            gIntroMovie = None
        IntroMovieDlg.dialog.hide()
        PtEnableRenderScene()
        PtGUICursorOn()
        FirstHelpDlg.dialog.show()
        PtFadeIn(kHelpFadeInSeconds, 0)


    def IStartGame(self):
        vault = ptVault()
        entry = vault.findChronicleEntry(kIntroPlayedChronicle)
        if (type(entry) != type(None)):
            entry.chronicleSetValue('yes')
            entry.save()
        else:
            vault.addChronicleEntry(kIntroPlayedChronicle, 2, 'yes')
        self.IFinishStartGame()


    def IFinishStartGame(self):
        FirstHelpDlg.dialog.hide()
# Make it possible to enable 1st person after the video BEGIN
        cam = ptCamera()
        cam.enableFirstPersonOverride()
# Make it possible to enable 1st person after the video END
        PtAtTimeCallback(self.key, kSoundTickTime, kSoundFadeInID)
        PtSendKIMessage(kEnableKIandBB, 0)


    def IUpdateSounds(self):
        global gCurrentTick
        audio = ptAudioControl()
        gCurrentTick += 1
        if (gCurrentTick >= gTotalTickTime):
            audio.setAmbienceVolume(gOriginalAmbientVolume)
            audio.setSoundFXVolume(gOriginalSFXVolume)
            PtUnloadDialog('StartupHelpGUI')
            PtUnloadDialog('IntroMovieGUI')
        else:
            audio.setAmbienceVolume((gOriginalAmbientVolume * (gCurrentTick / gTotalTickTime)))
            audio.setSoundFXVolume((gOriginalSFXVolume * (gCurrentTick / gTotalTickTime)))
            PtAtTimeCallback(self.key, kSoundTickTime, kSoundFadeInID)


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



