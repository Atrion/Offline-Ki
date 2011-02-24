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
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
actClickableBook = ptAttribActivator(1, 'Act: Clickable Yeesha Page')
PageNumber = ptAttribInt(2, 'Yeesha Page Number')
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
YeeshaPageIDList = [kYeeshaPage01, kYeeshaPage02, kYeeshaPage03, kYeeshaPage04, kYeeshaPage05, kYeeshaPage06, kYeeshaPage07, kYeeshaPage08, kYeeshaPage09, kYeeshaPage10, kYeeshaPage12, kYeeshaPage13, kYeeshaPage14, kYeeshaPage15, kYeeshaPage16, kYeeshaPage17, kYeeshaPage18, kYeeshaPage19, kYeeshaPage21, kYeeshaPage22, kYeeshaPage23, kYeeshaPage24, kYeeshaPage25, kYeeshaPage26]
 
class xYeeshaPages(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5225
        version = 6
        self.version = version
        print '__init__xYeeshaPages v.',
        print version


    def OnFirstUpdate(self):
        PtLoadDialog(DialogName, self.key)


    def __del__(self):
        PtUnloadDialog(DialogName)


    def OnNotify(self, state, id, events):
        if (state and ((id == actClickableBook.id) and PtWasLocallyNotified(self.key))):
            PtLoadDialog(DialogName, self.key)
            if PtIsDialogLoaded(DialogName):
                self.IDrawLinkPanel()
                PtShowDialog(DialogName)


    def OnGUINotify(self, id, control, event):
        if (event == kExitMode):
            PtHideDialog(DialogName)
            return
        btnID = 0
        if isinstance(control, ptGUIControlButton):
            btnID = control.getTagID()
        if ((event == 2) and (btnID in YeeshaPageIDList)):
            print 'xYeeshaPages.OnGUINotify():\tPicked up page number: ',
            print PageNumber.value
            PtHideDialog(DialogName)
            vault = ptVault()
            if (type(vault) != type(None)):
                psnlSDL = vault.getPsnlAgeSDL()
                if psnlSDL:
                    YeeshaPageVar = psnlSDL.findVar(('YeeshaPage' + str(PageNumber.value)))
                    PtDebugPrint(('xYeeshaPages.py: The previous value of the SDL variable %s is %s' % (('YeeshaPage' + str(PageNumber.value)), YeeshaPageVar.getInt())))
                    if (YeeshaPageVar.getInt() != 0):
                        PtDebugPrint(("xYeeshaPages.py: You've already found Yeesha Page #%s. Move along. Move along." % PageNumber.value))
                        return
                    else:
                        PtDebugPrint(('xYeeshaPages.py: Yeesha Page #%s is new to you.' % PageNumber.value))
                        PtDebugPrint(('xYeeshaPages.py: Trying to update the value of the SDL variable %s to 1' % ('YeeshaPage' + str(PageNumber.value))))
                        YeeshaPageVar.setInt(4)
                        vault.updatePsnlAgeSDL(psnlSDL)
                        PtSendKIMessageInt(kStartBookAlert, 0)
                else:
                    PtDebugPrint(('xYeeshaPages: Error trying to access the Chronicle psnlSDL. psnlSDL = %s' % psnlSDL))
            else:
                PtDebugPrint("xYeeshaPages: Error trying to access the Vault. Can't access YeeshaPageChanges chronicle.")
        elif ((event == 2) and (btnID == kYeeshaPageCancel)):
            PtHideDialog(DialogName)


    def IDrawLinkPanel(self):
        mydialog = PtGetDialogFromString(DialogName)
        ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage01)).hide()
        ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage02)).hide()
        ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage03)).hide()
        ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage04)).hide()
        ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage05)).hide()
        ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage06)).hide()
        ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage07)).hide()
        ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage08)).hide()
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
        if (PageNumber.value == 1):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage01)).show()
        elif (PageNumber.value == 2):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage02)).show()
        elif (PageNumber.value == 3):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage03)).show()
        elif (PageNumber.value == 4):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage04)).show()
        elif (PageNumber.value == 5):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage05)).show()
        elif (PageNumber.value == 6):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage06)).show()
        elif (PageNumber.value == 7):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage07)).show()
        elif (PageNumber.value == 8):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage08)).show()
        elif (PageNumber.value == 9):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage09)).show()
        elif (PageNumber.value == 10):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage10)).show()
        elif (PageNumber.value == 12):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage12)).show()
        elif (PageNumber.value == 13):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage13)).show()
        elif (PageNumber.value == 14):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage14)).show()
        elif (PageNumber.value == 15):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage15)).show()
        elif (PageNumber.value == 16):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage16)).show()
        elif (PageNumber.value == 17):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage17)).show()
        elif (PageNumber.value == 18):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage18)).show()
        elif (PageNumber.value == 19):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage19)).show()
        elif (PageNumber.value == 26):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage26)).show()
        elif (PageNumber.value == 21):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage21)).show()
        elif (PageNumber.value == 22):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage22)).show()
        elif (PageNumber.value == 23):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage23)).show()
        elif (PageNumber.value == 24):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage24)).show()
        elif (PageNumber.value == 25):
            ptGUIControlButton(mydialog.getControlFromTag(kYeeshaPage25)).show()
        else:
            print 'xYeeshaPages.IDrawLinkPanel():\tERROR: couldn\'t find page named ',
            print PageNumber.value
        return


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



