# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
actClickableBook = ptAttribNamedActivator(1, 'Act: Clickable Yeesha Page')
GUIDialogObject = ptAttribSceneobject(2, 'GUIDialog scene object')
RespOpen = ptAttribResponder(3, 'Open Responder')
RespLoop = ptAttribResponder(4, 'Loop Responder')
RespClose = ptAttribResponder(5, 'Close Responder')
DialogName = 'YeeshaPageGUI'
kPageButton = 100
kYeeshaPage01 = 201
kYeeshaPage02 = 202
kYeeshaPage03 = 203
kYeeshaPage04 = 204
kYeeshaPage05 = 205
kYeeshaPage06 = 206
kYeeshaPage07 = 207
kYeeshaPage08 = 208
kYeeshaPage09 = 209
kYeeshaPage10 = 210
kYeeshaPage12 = 212
kYeeshaPage13 = 213
kYeeshaPage14 = 214
kYeeshaPage15 = 215
kYeeshaPage16 = 216
kYeeshaPage17 = 217
kYeeshaPage18 = 218
kYeeshaPage19 = 219
kYeeshaPage21 = 221
kYeeshaPage22 = 222
kYeeshaPage23 = 223
kYeeshaPage24 = 224
kYeeshaPage25 = 225
kYeeshaPage26 = 220
kYeeshaPageCancel = 299

class clftYeeshaPage08(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5312
        self.version = 1
        print '__init__clftYeeshaPage08 v.',
        print self.version


    def OnFirstUpdate(self):
        PtLoadDialog(DialogName, self.key)


    def __del__(self):
        pass


    def OnNotify(self, state, id, events):
        if ((id == actClickableBook.id) and (state and PtWasLocallyNotified(self.key))):
            self.SetStdGUIVisibility(0)
            PtShowDialog(DialogName)
            RespOpen.run(self.key)
        elif (id == RespOpen.id):
            RespLoop.run(self.key)


    def OnGUINotify(self, id, control, event):
        btnID = 0
        if isinstance(control, ptGUIControlButton):
            btnID = control.getTagID()
        if ((event == kAction) and (btnID == kYeeshaPage08)):
            PtDebugPrint('DEBUG: clftYeeshaPage08.OnGUINotify():\tPicked up page')
            RespClose.run(self.key)
            PtHideDialog(DialogName)
            self.SetStdGUIVisibility(1)
            vault = ptVault()
            if (type(vault) != type(None)):
                psnlSDL = vault.getPsnlAgeSDL()
                if psnlSDL:
                    YeeshaPageVar = psnlSDL.findVar('YeeshaPage8')
                    PtDebugPrint(('DEBUG: clftYeeshaPage08.py: The previous value of the SDL variable %s is %s' % ('YeeshaPage8', YeeshaPageVar.getInt())))
                    if (YeeshaPageVar.getInt() != 0):
                        PtDebugPrint('DEBUG: clftYeeshaPage08.py: You\'ve already found Yeesha Page #8. Move along. Move along.')
                        return
                    else:
                        PtDebugPrint('DEBUG: clftYeeshaPage08.py: Yeesha Page #8 is new to you.')
                        PtDebugPrint(('DEBUG: clftYeeshaPage08.py: Trying to update the value of the SDL variable %s to 1' % 'YeeshaPage8'))
                        YeeshaPageVar.setInt(1)
                        vault.updatePsnlAgeSDL(psnlSDL)
                        PtSendKIMessageInt(kStartBookAlert, 0)
                else:
                    PtDebugPrint(('ERROR: clftYeeshaPage08: Error trying to access the Chronicle psnlSDL. psnlSDL = %s' % psnlSDL))
            else:
                PtDebugPrint('ERROR: clftYeeshaPage08: Error trying to access the Vault. Can\'t access YeeshaPageChanges chronicle.')
        elif ((event == kAction) and (btnID == kYeeshaPageCancel)):
            RespClose.run(self.key)
            PtHideDialog(DialogName)
            self.SetStdGUIVisibility(1)


    def SetStdGUIVisibility(self, visible):
        if visible:
            GUIDialogObject.value.draw.enable()
        else:
            mydialog = PtGetDialogFromString(DialogName)
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage01)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage02)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage03)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage04)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage05)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage06)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage07)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage09)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage10)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage12)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage13)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage14)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage15)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage16)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage17)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage18)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage19)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage26)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage21)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage22)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage23)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage24)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage25)).hide()
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage08)).show()
            GUIDialogObject.value.draw.disable()


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



