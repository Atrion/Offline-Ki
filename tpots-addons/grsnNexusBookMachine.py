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
from PlasmaConstants import *
from PlasmaKITypes import *
purpleResp = ptAttribResponder(1, 'purple responder')# no longer used
yellowResp = ptAttribResponder(2, 'yellow responder')
bookPurpleInPos = ptAttribActivator(3, 'Purple book in position event')
bookYellowInPos = ptAttribActivator(4, 'Yellow book in position event')
bookPurpleOutResponder = ptAttribResponder(5, 'Purple book out')
bookYellowOutResponder = ptAttribResponder(6, 'Yellow book out')
bookPurpleClickable = ptAttribActivator(7, 'purple book clickable')
bookYellowClickable = ptAttribActivator(8, 'yellow book clickable')
teamPurpleTeleport = ptAttribSceneobject(9, 'team purple teleport')
teamYellowTeleport = ptAttribSceneobject(10, 'team yellow teleport')
resetResponder = ptAttribResponder(11, 'reset floor', netForce=1)
entryTrigger = ptAttribActivator(12, 'entry trigger region', netForce=0)
fakeLinkBehavior = ptAttribBehavior(13, 'link out behavior', netForce=0)
waitingOnPBook = false
waitingOnYBook = false
yellowLink = false
suitDone = False

class grsnNexusBookMachine(ptResponder):


    def __init__(self):
        ptResponder.__init__(self)
        print 'book machine init'
        self.id = 53624
        self.version = 2


    def OnServerInitComplete(self):
        pass


    def OnFirstUpdate(self):
        pass


    def OnTimer(self, id):
        global yellowLink
        avatar = PtGetLocalAvatar()
        if (id == 0):
            if yellowLink:
                PtFakeLinkAvatarToObject(avatar.getKey(), teamYellowTeleport.value.getKey())
            else:
                PtFakeLinkAvatarToObject(avatar.getKey(), teamPurpleTeleport.value.getKey())
            #resetResponder.run(self.key, avatar=PtGetLocalAvatar())
            PtAtTimeCallback(self.key, 3.0, 1)
            PtSendKIMessage(kEnableEntireYeeshaBook, 0)
        else:
            resetResponder.run(self.key, avatar=PtGetLocalAvatar()) # don't reset too soon elevator or player will see it.


    def OnNotify(self, state, id, events):  # removed prints as it extends a LOT the log
        global yellowLink, suitDone
#        print 'id ',
#        print id
        avatar = PtFindAvatar(events)
        local = PtGetLocalAvatar()
        if (avatar != local):
            return
        if (id == fakeLinkBehavior.id):
            print 'notified of link behavior, yellow book ',
            print yellowLink
            for event in events:
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (event[2] == kEnterStage))):
                    print 'started touching book, set warp out timer'
                    PtAtTimeCallback(self.key, 1.0, 0)
                    return
        if (not (state)):
            return
        if (id == bookPurpleInPos.id):
#            print 'Purple book aligned'
            bookPurpleOutResponder.run(self.key)
        if (id == bookYellowInPos.id):
#            print 'Yellow book aligned'
            bookYellowOutResponder.run(self.key)
        if (id == entryTrigger.id):
            if not suitDone:
                suitDone = True
                PtWearMaintainerSuit(avatar.getKey(), false)
        if (id == bookPurpleClickable.id):
            print 'touched purple team room book'
            yellowLink = false
            avatar.avatar.runBehaviorSetNotify(fakeLinkBehavior.value, self.key, fakeLinkBehavior.netForce)
            suitDone = False
        if (id == bookYellowClickable.id):
            print 'touched yellow team room book'
            yellowLink = true
            avatar.avatar.runBehaviorSetNotify(fakeLinkBehavior.value, self.key, fakeLinkBehavior.netForce)
            suitDone = False


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


def glue_getParamDict():
    global glue_params
    global glue_paramKeys
    if (type(glue_params) == type(None)):
        glue_params = {}
        gd = globals()
        for obj in gd.values():
            if isinstance(obj, ptAttribute):
                if glue_params.has_key(obj.id):
                    if glue_verbose:
                        print 'WARNING: Duplicate attribute ids!'
                        print ('%s has id %d which is already defined in %s' % (obj.name, obj.id, glue_params[obj.id].name))
                else:
                    glue_params[obj.id] = obj
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



