# -*- coding: utf-8 -*-
global AreWeInRoom
global glue_cl
global glue_inst
global glue_params
global glue_paramKeys
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
actRegion = ptAttribActivator(2, 'Region')
numID = ptAttribInt(3, 'RoomID', 0)
doorVarName = ptAttribString(4, 'Age SDL Door Var Name')
AreWeInRoom = 0

class xChatChannelRegion(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5028
        version = 3
        self.version = version
        PtDebugPrint(('__init__xChatChannelRegion v%d.%d' % (version, 3)), level=kWarningLevel)


    def __del__(self):
        global AreWeInRoom
        PtDebugPrint('xChatChannel.__del__:', level=kDebugDumpLevel)
        if AreWeInRoom:
            try:
                PtClearPrivateChatList(PtGetLocalAvatar().getKey())
                self.IRemoveMember(PtGetLocalAvatar())
            except:
                pass
            PtDebugPrint(('xChatChannel.OnPageUnload:\tremoving ourselves from private chat channel %d' % numID.value), level=kDebugDumpLevel)
            PtSendKIMessageInt(kUnsetPrivateChatChannel, 0)
            AreWeInRoom = 0


    def OnServerInitComplete(self):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            self.SDL.setDefault('intSDLChatMembers', (-1, -1, -1, -1, -1, -1, -1, -1))
            if ((type(doorVarName.value) == type('')) and (doorVarName.value != '')):
                ageSDL.setNotify(self.key, doorVarName.value, 0.0)


    def OnFirstUpdate(self):
        global AgeStartedIn
        AgeStartedIn = PtGetAgeName()


    def OnPageLoad(self, what, room):
        global AreWeInRoom
        if (what == kUnloaded):
            PtDebugPrint('xChatChannel.OnPageUnload:', level=kDebugDumpLevel)
            if AreWeInRoom:
                try:
                    PtClearPrivateChatList(PtGetLocalAvatar().getKey())
                    self.IRemoveMember(PtGetLocalAvatar())
                except:
                    pass
                PtDebugPrint(('xChatChannel.OnPageUnload:\tremoving ourselves from private chat channel %d' % numID.value), level=kDebugDumpLevel)
                PtSendKIMessageInt(kUnsetPrivateChatChannel, 0)
                AreWeInRoom = 0


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname != doorVarName.value):
            return
        if (AgeStartedIn != PtGetAgeName()):
            return
        ageSDL = PtGetAgeSDL()
        if ageSDL[doorVarName.value][0]:
            PtDebugPrint('DEBUG: XChatChannel:OnSDLNotify:\tclosing door')
            self.ISendChatList()
        else:
            PtDebugPrint('DEBUG: XChatChannel:OnSDLNotify:\topening door')
            self.IUnSendChatList()


    def OnNotify(self, state, id, events):
        for event in events:
            if (event[0] != kCollisionEvent):
                continue
            if event[1]:
                self.IAddMember(event[2])
            else:
                self.IRemoveMember(event[2])


    def IAddMember(self, member):
        memberKey = member.getKey()
        memberID = PtGetClientIDFromAvatarKey(memberKey)
        memberName = memberKey.getName()
        for count in [0, 1, 2, 3, 4, 5, 6, 7]:
            if (self.SDL['intSDLChatMembers'][count] == memberID):
                PtDebugPrint(('xChatChannel: memberID=%d   already in list, aborting.' % memberID), level=kDebugDumpLevel)
                return
        for count in [0, 1, 2, 3, 4, 5, 6, 7]:
            if (self.SDL['intSDLChatMembers'][count] == -1):
                self.SDL.setIndex('intSDLChatMembers', count, memberID)
                PtDebugPrint(('xChatChannel: memberID=%d added to SDL.' % memberID), level=kDebugDumpLevel)
                return


    def IRemoveMember(self, member):
        memberKey = member.getKey()
        memberID = PtGetClientIDFromAvatarKey(memberKey)
        memberName = memberKey.getName()
        for count in [0, 1, 2, 3, 4, 5, 6, 7]:
            if (self.SDL['intSDLChatMembers'][count] == memberID):
                self.SDL.setIndex('intSDLChatMembers', count, -1)
                PtDebugPrint(('xChatChannel:removed %s  id # %d   from listen list' % (memberName, memberID)), level=kDebugDumpLevel)


    def ISendChatList(self):
        global AreWeInRoom
        memberList = []
        localPlayer = PtGetLocalPlayer()
        localID = localPlayer.getPlayerID()
        localIncluded = false
        for count in [0, 1, 2, 3, 4, 5, 6, 7]:
            if (not ((self.SDL['intSDLChatMembers'][count] == -1))):
                memberID = self.SDL['intSDLChatMembers'][count]
                memberKey = PtGetAvatarKeyFromClientID(memberID)
                memberName = memberKey.getName()
                memberList.append(ptPlayer(memberName, memberID))
                PtDebugPrint(('xChatChannel: added %s   id # %d  to listen list' % (memberName, memberID)), level=kDebugDumpLevel)
                if (memberID == localID):
                    localIncluded = true
        if localIncluded:
            PtSendPrivateChatList(memberList)
            PtDebugPrint(('xChatChannel.OnNotify:\tadding you to private chat channel %d' % numID.value), level=kDebugDumpLevel)
            PtSendKIMessageInt(kSetPrivateChatChannel, numID.value)
            AreWeInRoom = 1
        return


    def IUnSendChatList(self):
        global AreWeInRoom
        localPlayer = PtGetLocalPlayer()
        localID = localPlayer.getPlayerID()
        localIncluded = false
        for count in [0, 1, 2, 3, 4, 5, 6, 7]:
            if (self.SDL['intSDLChatMembers'][count] != -1):
                memberID = self.SDL['intSDLChatMembers'][count]
                if (memberID == localID):
                    localIncluded = true
        if localIncluded:
            PtClearPrivateChatList(PtGetLocalAvatar().getKey())
            PtDebugPrint(('xChatChannel.OnNotify:\tremoving ourselves from private chat channel %d' % numID.value), level=kDebugDumpLevel)
            PtSendKIMessageInt(kUnsetPrivateChatChannel, 0)
            AreWeInRoom = 0


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



