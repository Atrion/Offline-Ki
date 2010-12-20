# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
import string
import xLocalization
import xCensor
kAddingDevice = 1
kSettingDeviceInbox = 2
ImagerName = ptAttribString(1, 'Name of the Imager')
ImagerMap = ptAttribDynamicMap(2, 'The Dynamic Texture Map')
ImagerRegion = ptAttribActivator(3, 'The activate region')
ImagerTime = ptAttribInt(4, 'Number of seconds on each image', default=60)
ImagerMembersOnly = ptAttribBoolean(5, 'Members Only', 1)
ImagerObject = ptAttribSceneobject(6, 'Imager Object (for ownership test)')
ImagerMax = ptAttribInt(7, 'Maximum number of images', default=5)
ImagerButtonResp = ptAttribResponder(8, 'start or stop the button animation', ['buttonOn', 'buttonOff'])
ImagerInboxVariable = ptAttribString(9, 'Inbox SDL variable (optional)')
ImagerPelletUpload = ptAttribBoolean(10, 'Pellet Score Imager?', 0)
ImagerContents = []
CurrentContentIdx = 0
kTextFontSize = 18
kTextFontFace = 'arial'
kTextXStart = 100
kTextYStart = 100
kTextWrapWidth = 550
kTextWrapHeight = 400
theCensorLevel = 0
CurrentDisplayedElementID = -1
RegionMembers = 0
AgeStartedIn = None
kFlipImagesTimerStates = 5
kFlipImagesTimerCurrent = 0
Instance = None

class xSimpleImager(ptModifier):


    def __init__(self):
        global Instance
        ptModifier.__init__(self)
        Instance = self
        self.id = 196
        self.version = 3
        PtDebugPrint(('xSimpleImager: init  version=%d.%d' % (self.version, 2)), level=kWarningLevel)


    def vaultOperationStarted(self, context):
        PtDebugPrint(('xSimpleImager: vaultOperationStarted(%s)' % context), level=kDebugDumpLevel)


    def vaultOperationComplete(self, context, args, resultCode):
        global kFlipImagesTimerCurrent
        global CurrentContentIdx
        PtDebugPrint(('xSimpleImager: vaultOperationComplete(%s,%s)' % (context, resultCode)), level=kDebugDumpLevel)
        if (context == kAddingDevice):
            PtDebugPrint('\tkAddingDevice', level=kDebugDumpLevel)
            if (resultCode >= 0):
                node = args[0].upcastToTextNoteNode()
                if node:
                    PtDebugPrint(('\tAdded device: %s' % ImagerName.value), level=kDebugDumpLevel)
                    name = ''
                    if ((type(ImagerInboxVariable.value) == type('')) and (ImagerInboxVariable.value != '')):
                        ageSDL = PtGetAgeSDL()
                        name = ageSDL[ImagerInboxVariable.value][0]
                    else:
                        name = node.noteGetTitle()
                    PtDebugPrint(('\tSetting device inbox: %s' % name), level=kDebugDumpLevel)
                    node.setDeviceInbox(name, self, kSettingDeviceInbox)
                else:
                    PtDebugPrint('xSimpleImager:ERROR! device node not found', level=kErrorLevel)
        elif (context == kSettingDeviceInbox):
            PtDebugPrint('\tkSettingDeviceInbox', level=kDebugDumpLevel)
            if (resultCode >= 0):
                CurrentContentIdx = 0
                Instance.IRefreshImagerFolder()
                Instance.IChangeCurrentContent()
                kFlipImagesTimerCurrent = ((kFlipImagesTimerCurrent + 1) % kFlipImagesTimerStates)
                PtAtTimeCallback(Instance.key, ImagerTime.value, kFlipImagesTimerCurrent)
                ImagerButtonResp.run(Instance.key, state='buttonOff')
# GuildPub imager fix BEGIN
            if PtGetAgeName().find('GuildPub-') != -1:
                PtSendKIMessage(kAddPlayerDevice, ImagerName.value)
# GuildPub imager fix END


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()
        if (type(ImagerMap.textmap) == type(None)):
            if AgeStartedIn != 'RestorationGuild': # the PythonFileMod there is broken
                PtDebugPrint(('xSimpleImager:ERROR! simpleImager[%s]: Dynamic textmap is broken!' % ImagerName.value), level=kErrorLevel)
            return
        if (type(ImagerObject.sceneobject) == type(None)):
            PtDebugPrint(('xSimpleImager:ERROR! simpleImager[%s]: ImagerObject not specified!' % ImagerName.value), level=kErrorLevel)
            return
        if ((type(ImagerName.value) == type('')) and (ImagerName.value != '')):
            ageVault = ptAgeVault()
            ageVault.addDevice(ImagerName.value, self, kAddingDevice)
        else:
            PtDebugPrint('xSimpleImager: There was no imager name!', level=kErrorLevel)


    def OnServerInitComplete(self):
        if (AgeStartedIn == PtGetAgeName()):
            if ((type(ImagerInboxVariable.value) == type('')) and (ImagerInboxVariable.value != '')):
                ageSDL = PtGetAgeSDL()
                ageSDL.setNotify(self.key, ImagerInboxVariable.value, 0.0)
                ageVault = ptAgeVault()
                inbox = ''
                try:
                    inbox = ageSDL[ImagerInboxVariable.value][0]
                except:
                    PtDebugPrint('xSimpleImager: Problem reading the inbox from SDL')
                if (inbox == ''):
                    ageVault.setDeviceInbox(ImagerName.value, ImagerName.value, self, kSettingDeviceInbox)
                else:
                    ageVault.setDeviceInbox(ImagerName.value, inbox, self, kSettingDeviceInbox)


    def IDetermineCensorLevel(self):
        global theCensorLevel
        theCensorLevel = xCensor.xRatedPG
        vault = ptVault()
        entry = vault.findChronicleEntry(kChronicleCensorLevel)
        if (type(entry) == type(None)):
            vault.addChronicleEntry(kChronicleCensorLevel, kChronicleCensorLevelType, ('%d' % theCensorLevel))
        else:
            theCensorLevel = string.atoi(entry.chronicleGetValue())
        PtDebugPrint(('xSimpleImager: the censor level is %d' % theCensorLevel), level=kWarningLevel)


    def OnTimer(self, id):
        global CurrentContentIdx
        if (id == kFlipImagesTimerCurrent):
            if (len(ImagerContents) > 0):
                CurrentContentIdx += 1
                if (CurrentContentIdx >= len(ImagerContents)):
                    CurrentContentIdx = 0
            self.IChangeCurrentContent()
            PtAtTimeCallback(self.key, ImagerTime.value, kFlipImagesTimerCurrent)


    def OnAgeVaultEvent(self, event, tupdata):
        if (event == PtVaultCallbackTypes.kVaultConnected):
            pass
        if (event == PtVaultCallbackTypes.kVaultDisconnected):
            pass
        elif (event == PtVaultCallbackTypes.kVaultNodeAdded):
            PtDebugPrint(('xSimpleImager: kVaultNodeAdded event (id=%d,type=%d)' % (tupdata[0].getID(), tupdata[0].getType())), level=kDebugDumpLevel)
            self.IRefreshImagerFolder()
            self.IRefreshImagerElement(tupdata[0])
        elif (event == PtVaultCallbackTypes.kVaultNodeSaved):
            PtDebugPrint(('xSimpleImager: kVaultNodeSaved event (id=%d,type=%d)' % (tupdata[0].getID(), tupdata[0].getType())), level=kDebugDumpLevel)
            self.IRefreshImagerFolder()
            self.IRefreshImagerElement(tupdata[0])
        elif (event == PtVaultCallbackTypes.kVaultNodeRefAdded):
            PtDebugPrint(('xSimpleImager: kVaultNodeRefAdded event (childID=%d,parentID=%d)' % (tupdata[0].getChildID(), tupdata[0].getParentID())), level=kDebugDumpLevel)
            self.IRefreshImagerFolder()
            self.IRefreshImagerContent(tupdata[0])
        elif (event == PtVaultCallbackTypes.kVaultRemovingNodeRef):
            pass
        elif (event == PtVaultCallbackTypes.kVaultNodeRefRemoved):
            PtDebugPrint('xSimpleImager: kVaultNodeRefRemoved event (childID,parentID) ', tupdata, level=kDebugDumpLevel)
            self.IRefreshImagerFolder()
        elif (event == PtVaultCallbackTypes.kVaultOperationFailed):
            pass


    def OnNotify(self, state, id, events):
        global RegionMembers
        global CurrentDisplayedElementID
        if (id == ImagerRegion.id):
            if PtWasLocallyNotified(self.key):
                ageMgr = ptVault()
                if ((not (ImagerMembersOnly.value)) or ageMgr.amOwnerOfCurrentAge()):
                    if (id == ImagerRegion.id):
                        for event in events:
                            if (event[0] == kCollisionEvent):
                                kiLevel = PtDetermineKILevel()
                                if (kiLevel < kNormalKI):
                                    return
                                if ImagerPelletUpload.value:
                                    return #messagetoki = (str(ImagerName.value) + '<p>')
                                else:
                                    messagetoki = ImagerName.value
                                if event[1]:
                                    PtDebugPrint('xSimpleImager: add imager %s' % ImagerName.value)
                                    PtSendKIMessage(kAddPlayerDevice, messagetoki)
                                    RegionMembers = (RegionMembers + 1)
                                    if (RegionMembers == 1):
                                        ImagerButtonResp.run(self.key, state='buttonOn')
                                else:
                                    PtDebugPrint('xSimpleImager: remove imager %s' % ImagerName.value)
                                    PtSendKIMessage(kRemovePlayerDevice, messagetoki)
                                    RegionMembers = (RegionMembers - 1)
                                    if (RegionMembers == -1):
                                        RegionMembers = 0
                                    if (RegionMembers == 0):
                                        ImagerButtonResp.run(self.key, state='buttonOff')
        else:
            for event in events:
                if (event[0] == kVariableEvent):
                    if (event[1][:7] == 'dispID='):
                        newID = string.atoi(event[1][7:])
                        if (newID != CurrentDisplayedElementID):
                            CurrentDisplayedElementID = newID
                            self.IShowCurrentContent()


    def IRefreshImagerFolder(self):
        global ImagerContents
        ageVault = ptAgeVault()
        folder = ageVault.getDeviceInbox(ImagerName.value)
        if (type(folder) != type(None)):
            prevsize = len(ImagerContents)
            ImagerContents = folder.getChildNodeRefList()
            if ImagerObject.sceneobject.isLocallyOwned():
                if (len(ImagerContents) > ImagerMax.value):
                    relem = ImagerContents[0].getChild()
                    PtDebugPrint(('xSimpleImager[%s]: removing element %d' % (ImagerName.value, relem.getID())), level=kDebugDumpLevel)
                    folder.removeNode(relem)
            if ((prevsize == 0) and len(ImagerContents)):
                self.IChangeCurrentContent()
        else:
            ImagerContents = []


    def IRefreshImagerContent(self, updated_content):
        if (type(updated_content) != type(None)):
            updated_element = updated_content.getChild()
            if (type(updated_element) != type(None)):
                if (updated_element.getID() == CurrentDisplayedElementID):
                    self.IShowCurrentContent()
                elif (not updated_content.beenSeen()):
                    self.IChangeCurrentContent(updated_element.getID())


    def IRefreshImagerElement(self, updated_element):
        if (type(updated_element) != type(None)):
            if (updated_element.getID() == CurrentDisplayedElementID):
                self.IShowCurrentContent()
            else:
                ageVault = ptAgeVault()
                folder = ageVault.getDeviceInbox(ImagerName.value)
                if (type(folder) != type(None)):
                    frefs = folder.getChildNodeRefList()
                    for ref in frefs:
                        elem = ref.getChild()
                        if ((type(elem) != type(None)) and (elem.getID() == updated_element.getID())):
                            if (not ref.beenSeen()):
                                self.IChangeCurrentContent(updated_element.getID())
                                return


    def IChangeCurrentContent(self, next = None):
        if ImagerObject.sceneobject.isLocallyOwned():
            nextID = -1
            if (type(next) == type(None)):
                try:
                    element = ImagerContents[CurrentContentIdx].getChild()
                    if (type(element) != type(None)):
                        nextID = element.getID()
                except LookupError:
                    pass
            else:
                nextID = next
            selfnotify = ptNotify(self.key)
            selfnotify.clearReceivers()
            selfnotify.addReceiver(self.key)
            selfnotify.netPropagate(1)
            selfnotify.netForce(1)
            selfnotify.setActivate(1.0)
            sname = ('dispID=%d' % nextID)
            selfnotify.addVarNumber(sname, 1.0)
            selfnotify.send()


    def IShowCurrentContent(self):
        if (CurrentDisplayedElementID != -1):
            ageVault = ptAgeVault()
            folder = ageVault.getDeviceInbox(ImagerName.value)
            if (type(folder) != type(None)):
                fcontents = folder.getChildNodeRefList()
                for content in fcontents:
                    element = content.getChild()
                    if ((type(element) != type(None)) and (element.getID() == CurrentDisplayedElementID)):
                        content.setSeen()
                        elemType = element.getType()
                        if (elemType == PtVaultNodeTypes.kImageNode):
                            element = element.upcastToImageNode()
                            PtDebugPrint(('simpleImager: now showing image %s' % element.imageGetTitle()), level=kDebugDumpLevel)
                            ImagerMap.textmap.drawImage(0, 0, element.imageGetImage(), 0)
                            ImagerMap.textmap.flush()
                        elif (elemType == PtVaultNodeTypes.kTextNoteNode):
                            element = element.upcastToTextNoteNode()
                            textbody = element.noteGetText()
                            if (textbody == 'cleardaImager'):
                                PtDebugPrint(('xSimpleImager[%s]: clearing the imager of images' % ImagerName.value), level=kWarningLevel)
                                folder.removeAllNodes()
                            else:
                                self.IDetermineCensorLevel()
                                ImagerMap.textmap.clearToColor(ptColor().black())
                                ImagerMap.textmap.setTextColor(ptColor().white())
                                ImagerMap.textmap.setWrapping(kTextWrapWidth, kTextWrapHeight)
                                ImagerMap.textmap.setFont(kTextFontFace, kTextFontSize)
                                try:
                                    # Checking for the owner node ID does not help - sometimes, it can't get the owner node even though it knows its ID
                                    textfrom = element.getOwnerNode().playerGetName()
                                except:
                                    textfrom = 'System'
                                textsubject = element.noteGetTitle()
                                message = xCensor.xCensor((xLocalization.xGlobal.xImagerMessage % (textfrom, textsubject, textbody)), theCensorLevel)
                                message = self.RemoveHiddenText(message)[0]
                                ImagerMap.textmap.drawText(kTextXStart, kTextYStart, message)
                                ImagerMap.textmap.flush()
                        else:
                            PtDebugPrint(("xSimpleImager[%s]: Can't display element type %d" % (ImagerName.value, elemType)), level=kWarningLevel)
                        return
            else:
                PtDebugPrint(('xSimpleImager[%s]: Inbox for imager is None' % ImagerName.value), level=kWarningLevel)
        else:
            ImagerMap.textmap.clearToColor(ptColor(0, 0, 0, 0))
            ImagerMap.textmap.flush()
            PtDebugPrint(('xSimpleImager[%s]: no current element id to display' % ImagerName.value), level=kDebugDumpLevel)


    def RemoveHiddenText(self, msg):
        if (type(msg) == type('')):
            newmsg = msg
            hiddenlist = []
            hidTxtStart = 0
            while (hidTxtStart >= 0):
                hidTxtStart = newmsg.find('<hiddentext>')
                if (hidTxtStart >= 0):
                    hidTxtEnd = newmsg.find('</hiddentext>')
                    if (hidTxtEnd >= 0):
                        hiddenlist.append(newmsg[(hidTxtStart + len('<hiddentext>')):hidTxtEnd])
                        newmsg = (newmsg[:hidTxtStart] + newmsg[(hidTxtEnd + len('</hiddentext>')):])
            return (newmsg, hiddenlist)
        return (msg, [])


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname != ImagerInboxVariable.value):
            return
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            ageVault = ptAgeVault()
            inbox = ageSDL[ImagerInboxVariable.value][0]
            if (inbox == ''):
                ageVault.setDeviceInbox(ImagerName.value, ImagerName.value, self, kSettingDeviceInbox)
            else:
                ageVault.setDeviceInbox(ImagerName.value, ageSDL[ImagerInboxVariable.value][0], self, kSettingDeviceInbox)


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



