# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
actTubeRegion = ptAttribActivator(1, 'Tube region act')
respTubeDown = ptAttribResponder(2, 'Tube down resp')
respTubeUp = ptAttribResponder(3, 'Tube up resp')
MaleSuit = ['03_MHAcc_SuitHelmet', '03_MLHand_Suit', '03_MRHand_Suit', '03_MTorso_Suit', '03_MLegs_Suit', '03_MLFoot_Suit', '03_MRFoot_Suit']
FemaleSuit = ['03_FHair_SuitHelmet', '03_FLHand_Suit', '03_FRHand_Suit', '03_FTorso_Suit', '03_FLegs_Suit', '03_FLFoot_Suit', '03_FRFoot_Suit']

class grsnMaintainersSuit(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5337
        self.version = 1
        PtDebugPrint(('grsnMaintainersSuit.__init__ v. %d' % self.version), level=kWarningLevel)


    def OnServerInitComplete(self):
        pass


    def OnFirstUpdate(self):
        pass


    def Load(self):
        pass


    def OnNotify(self, state, id, events):
        print 'Notify:',
        print id,
        print state
        if ((id == actTubeRegion.id) and state):
            PtDisableMovementKeys()
            respTubeDown.run(self.key, events=events)
        elif (id == respTubeDown.id):
            avatar = PtGetLocalAvatar()
            currentgender = avatar.avatar.getAvatarClothingGroup()
            if (currentgender == kFemaleClothingGroup):
                clothing = FemaleSuit
            else:
                clothing = MaleSuit
            # add suit (represented by the helmet) to closet
            if (not self.IItemInCloset(avatar, clothing[0])):
                PtDebugPrint('DEBUG: grsnMaintainersSuit.OnNotify():  Adding ' + clothing[0] + ' to your closet')
                avatar.avatar.addWardrobeClothingItem(clothing[0], ptColor().white(), ptColor().white())
            # wear helmet
            worn = avatar.avatar.getAvatarClothingList()
            for item in worn:
                name = item[0]
                type = item[1]
                if (type == kHairClothingItem):
                    color1 = avatar.avatar.getTintClothingItem(name, 1)
                    color2 = avatar.avatar.getTintClothingItem(name, 2)
                    avatar.avatar.wearClothingItem(clothing[0], 0)
                    avatar.avatar.tintClothingItem(clothing[0], color1, 0)
                    avatar.avatar.tintClothingItemLayer(clothing[0], color2, 2, 1)
                    break
            # wear the rest
            for item in clothing[1:]:
                PtDebugPrint('DEBUG: grsnMaintainersSuit.OnNotify():  Wearing ' + item)
                avatar.avatar.wearClothingItem(item, 0)
                avatar.avatar.tintClothingItem(item, ptColor().white(), 0)
                avatar.avatar.tintClothingItemLayer(item, ptColor().white(), 2, 1)
            # done!
            avatar.avatar.saveClothing()
            respTubeUp.run(self.key, events=events)
        elif (id == respTubeUp.id):
            PtEnableMovementKeys()


    def IItemInCloset(self, avatar, clothingName):
        clothingList = avatar.avatar.getWardrobeClothingList()
        for item in clothingList:
            if (clothingName == item[0]):
                return 1
        return 0


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



