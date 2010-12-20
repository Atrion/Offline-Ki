# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import PlasmaControlKeys
actBookshelf = ptAttribActivator(1, 'Actvtr:Bookshelf')
actBook = ptAttribActivator(2, 'Actvtr:Book')
respPresentBook = ptAttribResponder(3, 'Rspndr:PresentBook')
respShelveBook = ptAttribResponder(4, 'Rspndr:ShelveBook')
SeekBehavior = ptAttribBehavior(5, 'Smart seek before GUI')
ShelfCamera = ptAttribSceneobject(6, 'Bookshelf camera')
HutCamera = ptAttribSceneobject(7, 'Hut circle camera')
actBookshelfExit = ptAttribActivator(8, 'Actvr: Exit bookshelf')
respLinkOut = ptAttribResponder(9, 'Resp: link out')
respMoveShelf = ptAttribResponder(10, 'Resp: move shelf', ['raise', 'lower'])
theBook = None
LocalAvatar = None

class philBookshelf(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5327
        self.version = 1
        print '__init__philBookshelf v.',
        print self.version


    def OnServerInitComplete(self):
        global LocalAvatar
        respMoveShelf.run(self.key, state='lower', fastforward=1)
        actBookshelfExit.disable()
        LocalAvatar = PtGetLocalAvatar()


    def OnNotify(self, state, id, events):
        global theBook
        boolLinkerIsMe = false
        if PtWasLocallyNotified(self.key):
            boolLinkerIsMe = true
        print ('philBookshelf.OnNotify(): state = %d, id = %d, me = %s' % (state, id, boolLinkerIsMe))
        if (id == actBookshelfExit.id):
            self.IDisengageShelf(boolLinkerIsMe)
            return
        if (id == SeekBehavior.id):
            for event in events:
                avatar = PtFindAvatar(events)
                if ((event[0] == kMultiStageEvent) and ((event[1] == 0) and (LocalAvatar == avatar))):
                    SeekBehavior.gotoStage(avatar, -1)
                    print 'philBookshelf.OnNotify():\tengaging bookshelf'
                    avatar.draw.disable()
                    virtCam = ptCamera()
                    virtCam.save(ShelfCamera.sceneobject.getKey())
                    PtAtTimeCallback(self.key, 0.10000000000000001, 1)
        if ((id == actBookshelf.id) and state):
            respMoveShelf.run(self.key, state='raise', fastforward=1)
            avatar = PtFindAvatar(events)
            if (LocalAvatar == avatar):
                PtSendKIMessage(kDisableKIandBB, 0)
                cam = ptCamera()
                cam.undoFirstPerson()
                cam.disableFirstPersonOverride()
                PtRecenterCamera()
                SeekBehavior.run(avatar)
                PtDisableMovementKeys()
        elif ((id == actBook.id) and state):
            actBook.disable()
            respPresentBook.run(self.key)
        elif ((id == respPresentBook.id) and boolLinkerIsMe):
            bookcode = '<font size=10><img src="xDRCBookRubberStamp2*1#0.hsm" pos=125,120 blend=alpha><pb><img src="xLinkPanelKirel*1#0.hsm" align=center link=0 blend=alpha>'
            theBook = ptBook(bookcode, self.key)
            theBook.setGUI('BkBook')
            theBook.setSize(1.0, 1.0)
            theBook.show(1)
        elif (id == respShelveBook.id):
            actBook.enable()
        else:
            for event in events:
                if (event[0] == PtEventType.kBook):
                    PtDebugPrint(('philBookshelf: BookNotify  event=%d, id=%d' % (event[1], event[2])))
                    if (event[1] == PtBookEventTypes.kNotifyImageLink):
                        if (event[2] >= 0):
                            PtDebugPrint(('philBookshelf:Book: hit linking panel %s' % event[2]))
                            theBook.hide()
                            self.IDisengageShelf(boolLinkerIsMe)
                            # BEGIN linking rule fix
                            #respLinkOut.run(self.key) # Cyan uses the wrong linking rule here
                            import xLinkMgr
                            xLinkMgr.LinkToAge('Neighborhood02', 'LinkInPointDefault')
                            # END linking rule fix
                    elif (event[1] == PtBookEventTypes.kNotifyHide):
                        PtDebugPrint('philBookshelf:Book: NotifyHide')
                        respShelveBook.run(self.key)


    def IDisengageShelf(self, boolLinkerIsMe = false):
        print ('philBookshelf.IDisengageShelf(): me = %s' % boolLinkerIsMe)
        actBookshelfExit.disable()
        #fastforward removed because it disables netPropagate!
        respMoveShelf.run(self.key, state='lower')
        if boolLinkerIsMe:
            LocalAvatar.draw.enable()
            cam = ptCamera()
            cam.enableFirstPersonOverride()
            virtCam = ptCamera()
            virtCam.save(HutCamera.sceneobject.getKey())
            PtEnableMovementKeys()
            PtGetControlEvents(false, self.key)
            PtSendKIMessage(kEnableKIandBB, 0)


    def OnControlKeyEvent(self, controlKey, activeFlag):
        if ((controlKey == PlasmaControlKeys.kKeyExitMode) or (controlKey == PlasmaControlKeys.kKeyMoveBackward)):
            self.IDisengageShelf(true)


    def OnTimer(self, id):
        if (id == 1):
            PtGetControlEvents(true, self.key)
            actBookshelfExit.enable()


    def OnBackdoorMsg(self, target, param):
        if (target == 'book'):
            if (param == 'enable'):
                actBook.enable()
            elif (param == 'disable'):
                actBook.disable()
        elif (target == 'shelf'):
            if (param == 'enable'):
                actBookshelf.enable()
                actBookshelf.value[0].getSceneObject().physics.suppress(0)
            elif (param == 'disable'):
                actBookshelf.disable()
                actBookshelf.value[0].getSceneObject().physics.suppress(1)


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



