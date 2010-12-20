# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import PlasmaControlKeys
import string
actButton1 = ptAttribActivator(1, 'Act: Button 01')
actButton2 = ptAttribActivator(2, 'Act: Button 02')
actButton3 = ptAttribActivator(3, 'Act: Button 03')
actButton4 = ptAttribActivator(4, 'Act: Button 04')
actButton5 = ptAttribActivator(5, 'Act: Button 05')
actButton6 = ptAttribActivator(6, 'Act: Button 06')
respButton1 = ptAttribResponder(7, 'Resp: Button 01 Down')
respButton2 = ptAttribResponder(8, 'Resp: Button 02 Down')
respButton3 = ptAttribResponder(9, 'Resp: Button 03 Down')
respButton4 = ptAttribResponder(10, 'Resp: Button 04 Down')
respButton5 = ptAttribResponder(11, 'Resp: Button 05 Down')
respButton6 = ptAttribResponder(12, 'Resp: Button 06 Down')
Activate = ptAttribActivator(13, 'Act: VCP Clickable')
VCPCamera = ptAttribSceneobject(14, 'VCP camera')
Behavior = ptAttribBehavior(15, 'VCP idle behavior')
RaiseVCPClickable = ptAttribResponder(16, 'Raise VCP Clickable')
LowerVCPClickable = ptAttribResponder(17, 'Lower VCP Clickable')
RgnDisengage = ptAttribActivator(18, 'Act: Disengage Rgn')
VaultRoomCamera = ptAttribSceneobject(19, 'Release camera')
respResetButtons = ptAttribResponder(20, 'Reset All Buttons')
respOpenVault = ptAttribResponder(21, 'Open Vault Door')
respCloseVault = ptAttribResponder(22, 'Close Vault Door')
actResetBtn = ptAttribActivator(23, 'act:Reset Button')
respResetBtn = ptAttribResponder(24, 'resp:Reset Button')
OnlyOneOwner = ptAttribSceneobject(25, 'OnlyOneOwner')
LocalAvatar = None
VCPboolOperated = false
VCPVCPOperatorID = -1
ButtonsPushed = 0
VaultClosed = 1
VaultDoorMoving = 0

class kdshVault(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5234
        version = 6
        self.version = version
        print '__init__kdshVault v. ',
        print version,
        print '.3'


    def OnServerInitComplete(self):
        global ButtonsPushed
        ageSDL = PtGetAgeSDL()
        ageSDL.sendToClients('ButtonsPushed')
        ageSDL.sendToClients('VaultClosed')
        ageSDL.sendToClients('VCPboolOperated')
        ageSDL.sendToClients('VCPVCPOperatorID')
        ageSDL.setFlags('ButtonsPushed', 1, 1)
        ageSDL.setFlags('VaultClosed', 1, 1)
        ageSDL.setFlags('VCPboolOperated', 1, 1)
        ageSDL.setFlags('VCPVCPOperatorID', 1, 1)
        ageSDL.setNotify(self.key, 'ButtonsPushed', 0.0)
        ageSDL.setNotify(self.key, 'VaultClosed', 0.0)
        ButtonsPushed = ageSDL['ButtonsPushed'][0]
        print 'kdshVault: When I got here:'
        print '\t ButtonsPushed = ',
        print ButtonsPushed
        ButtonsPushed = str(ButtonsPushed)
        if (len(ButtonsPushed) >= 6):
            print 'All 6 buttons were already pushed. Resetting.'
            respResetButtons.run(self.key)
            ageSDL['ButtonsPushed'] = (0,)
            return
        if ('1' in ButtonsPushed):
            print 'fast forwarding button 1'
            respButton1.run(self.key, fastforward=1)
            actButton1.disable()
        if ('2' in ButtonsPushed):
            print 'fast forwarding button 2'
            respButton2.run(self.key, fastforward=1)
            actButton2.disable()
        if ('3' in ButtonsPushed):
            print 'fast forwarding button 3'
            respButton3.run(self.key, fastforward=1)
            actButton3.disable()
        if ('4' in ButtonsPushed):
            print 'fast forwarding button 4'
            respButton4.run(self.key, fastforward=1)
            actButton4.disable()
        if ('5' in ButtonsPushed):
            print 'fast forwarding button 5'
            respButton5.run(self.key, fastforward=1)
            actButton5.disable()
        if ('6' in ButtonsPushed):
            print 'fast forwarding button 6'
            respButton6.run(self.key, fastforward=1)
            actButton6.disable()
        if ('0' in ButtonsPushed):
            print 'No buttons have been pushed.'
            ageSDL['ButtonsPushed'] = (0,)
        # always enable the book online BEGIN
        import xxConfig
        if xxConfig.isOnline():
            ageSDL['kdshYeeshaVaultLinkBook'] = (1,)
            return
        # always enable the book online END
        vault = ptVault()
        entry = vault.findChronicleEntry('Blah')
        if (type(entry) != type(None)):
            entryValue = entry.chronicleGetValue()
            MyBlah = string.atoi(entryValue)
            if (MyBlah == 4):
                print "kdshVault: MyBlah = 4. You've finished Exp2. Showing Yeesha's Vault link book."
                ageSDL['kdshYeeshaVaultLinkBook'] = (1,)
            else:
                print 'kdshVault: MyBlah =',
                print MyBlah,
                print " You haven't finished Exp2. Hiding Yeesha's Vault link book."
                ageSDL['kdshYeeshaVaultLinkBook'] = (0,)
        else:
            print 'kdshVault: I couldn\'t tell if you\'ve finished Exp2. Hiding Yeehsa\'s Vault link book.'
            ageSDL['kdshYeeshaVaultLinkBook'] = (0,)


    def Load(self):
        global VCPboolOperated
        ageSDL = PtGetAgeSDL()
        solo = true
        if len(PtGetPlayerList()):
            solo = false
        VCPboolOperated = ageSDL['VCPboolOperated'][0]
        if VCPboolOperated:
            if solo:
                print ('kdshVault.Load():\tVCPboolOperated=%d but no one else here...correcting' % VCPboolOperated)
                VCPboolOperated = 0
                ageSDL['VCPboolOperated'] = (0,)
                ageSDL['VCPOperatorID'] = (-1,)
                Activate.enable()
            else:
                Activate.disable()
                print ('kdshVault.Load():\tVCPboolOperated=%d, disabling Vault Control Panel clickable' % VCPboolOperated)


    def AvatarPage(self, avObj, pageIn, lastOut):
        ageSDL = PtGetAgeSDL()
        if pageIn:
            return
        avID = PtGetClientIDFromAvatarKey(avObj.getKey())
        if (avID == ageSDL['VCPOperatorID'][0]):
            Activate.enable()
            ageSDL['VCPOperatorID'] = (-1,)
            ageSDL['VCPboolOperated'] = (0,)
            LowerVCPClickable.run(self.key)
            print 'kdshVault.AvatarPage(): Vault Control Panel operator paged out, reenabled VCP clickable.'
        else:
            return


    def OnNotify(self, state, id, events):
        global ButtonsPushed
        global LocalAvatar
        global VaultDoorMoving
        ageSDL = PtGetAgeSDL()
        if (state and ((id == Activate.id) and PtWasLocallyNotified(self.key))):
            print "kdshVault: I'm engaging VCP."
            cam = ptCamera()
            cam.undoFirstPerson()
            cam.disableFirstPersonOverride()
            LocalAvatar = PtFindAvatar(events)
            Behavior.run(LocalAvatar)
            RaiseVCPClickable.run(self.key)
            Activate.disable()
            ageSDL = PtGetAgeSDL()
            ageSDL['VCPboolOperated'] = (1,)
            avID = PtGetClientIDFromAvatarKey(LocalAvatar.getKey())
            ageSDL['VCPOperatorID'] = (avID,)
        elif ((id == Behavior.id) and PtWasLocallyNotified(self.key)):
            LocalAvatar = PtFindAvatar(events)
            Behavior.gotoStage(LocalAvatar, -1)
            PtDisableForwardMovement()
            virtCam = ptCamera()
            virtCam.save(VCPCamera.sceneobject.getKey())
            PtGetControlEvents(true, self.key)
            PtAtTimeCallback(self.key, 0.20000000000000001, 2)
        elif (state and ((id in [1, 2, 3, 4, 5, 6]) and PtWasLocallyNotified(self.key))):
            if VaultDoorMoving:
                print 'Button has no effect. The Vault Door is already moving.'
                return
            print ('\tkdshVault.OnNotify: Button #%d pushed' % id)
            ButtonsPushed = ageSDL['ButtonsPushed'][0]
            ButtonsPushed = str(ButtonsPushed)
            print 'kdshVault.OnNotify: Before, ButtonsPushed was ',
            print ButtonsPushed
            ButtonsPushed = string.atoi((ButtonsPushed + str(id)))
            print 'kdshVault.OnNotify: Now, ButtonsPushed = ',
            print ButtonsPushed
            ageSDL['ButtonsPushed'] = (ButtonsPushed,)
            if (len(str(ButtonsPushed)) >= 6):
                PtAtTimeCallback(self.key, 1, 1)
        elif (state and (id == actResetBtn.id)):
            LocalAvatar = PtFindAvatar(events)
            respResetBtn.run(self.key, events=events)
        elif ((id == respResetBtn.id) and OnlyOneOwner.sceneobject.isLocallyOwned()):
            if VaultDoorMoving:
                print 'Button has no effect. The Vault Door is already moving.'
                return
            print 'kdshVault.OnNotify: Reset Button Pushed. Toggling Vault Door state.'
            vaultclosed = ageSDL['VaultClosed'][0]
            if (vaultclosed == 1):
                print '\t trying to open the Vault.'
                ageSDL.setTagString('VaultClosed', 'fromOutside')
                ageSDL['VaultClosed'] = (0,)
            elif (vaultclosed == 0):
                print '\t trying to close the Vault.'
                ageSDL.setTagString('VaultClosed', 'fromInside')
                ageSDL['VaultClosed'] = (1,)
            VaultDoorMoving = 1
            PtAtTimeCallback(self.key, 18, 3)


    def IDisengageVCP(self):
        LowerVCPClickable.run(self.key)
        Activate.enable()
        PtFadeLocalAvatar(0)
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        virtCam = ptCamera()
        virtCam.save(VaultRoomCamera.sceneobject.getKey())
        PtEnableForwardMovement()
        PtGetControlEvents(false, self.key)


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        print 'kdshVault.OnSDLNotify:\tVARname=',
        print VARname,
        print ' value=',
        print ageSDL[VARname][0]
        if (VARname == 'ButtonsPushed'):
            ButtonsPushed = ageSDL['ButtonsPushed'][0]
            if (ButtonsPushed == 0):
                return
            ButtonsPushed = str(ButtonsPushed)
            lastbuttonpushed = ButtonsPushed[-1:]
            print 'kdshVault.OnSDLNotify: new ButtonsPushed = ',
            print ButtonsPushed
            code = (('respButton' + str(lastbuttonpushed)) + '.run(self.key)')
            exec code
            code = (('actButton' + str(lastbuttonpushed)) + '.disable()')
            exec code


    def OnTimer(self, id):
        global VaultDoorMoving
        ageSDL = PtGetAgeSDL()
        if (id == 1):
            ButtonsPushed = ageSDL['ButtonsPushed'][0]
            print 'kdshVault: Check solution. ButtonsPushed = ',
            print ButtonsPushed
            if (ButtonsPushed == 152346):
                print 'kdshVault: Puzzle solved. Opening door.'
                ageSDL.setTagString('VaultClosed', 'fromOutside')
                ageSDL['VaultClosed'] = (0,)
                VaultDoorMoving = 1
                PtAtTimeCallback(self.key, 18, 3)
            respResetButtons.run(self.key)
            ageSDL['ButtonsPushed'] = (0,)
        elif (id == 2):
            PtFadeLocalAvatar(1)
        elif (id == 3):
            print 'kdshVault: The Vault door has stopped moving.'
            VaultDoorMoving = 0


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if (controlKey == PlasmaControlKeys.kKeyExitMode):
            self.IDisengageVCP()
        elif ((controlKey == PlasmaControlKeys.kKeyMoveBackward) or ((controlKey == PlasmaControlKeys.kKeyRotateLeft) or (controlKey == PlasmaControlKeys.kKeyRotateRight))):
            self.IDisengageVCP()


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



