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
import string
import xRandom
import xxConfig
stringVarName = ptAttribString(1, 'Show/hide age SDL var name')
boolShowOnTrue = ptAttribBoolean(2, 'Show on true', 1)
actClickable = ptAttribActivator(3, 'Clothing clickable')
stringFClothingName = ptAttribString(4, 'Female clothing name')
stringMClothingName = ptAttribString(5, 'Male clothing name')
boolHasHairColor = ptAttribBoolean(6, 'Has hair color', 0)
stringChanceSDLName = ptAttribString(7, 'Chance SDL var name')
intTint1Red = ptAttribInt(8, 'Tint 1 Red', 255, (0, 255))
intTint1Green = ptAttribInt(9, 'Tint 1 Green', 255, (0, 255))
intTint1Blue = ptAttribInt(10, 'Tint 1 Blue', 255, (0, 255))
intTint2Red = ptAttribInt(11, 'Tint 2 Red', 255, (0, 255))
intTint2Green = ptAttribInt(12, 'Tint 2 Green', 255, (0, 255))
intTint2Blue = ptAttribInt(13, 'Tint 2 Blue', 255, (0, 255))
boolStayVisible = ptAttribBoolean(14, 'Stay visible after click', 0)
boolFirstUpdate = ptAttribBoolean(15, 'Eval On First Update?', 0)
AgeStartedIn = None
hairColor = ptColor().white()
kEnableClothingTimer = 99
kDisableClothingTimer = 100
kGetHairColorTimer = 101
kRollDiceTimer = 102
baseFClothing = ''
baseMClothing = ''
allFClothing = []
allMClothing = []
clothingTypeList = [kHairClothingItem, kFaceClothingItem, kShirtClothingItem, kRightHandClothingItem, kPantsClothingItem, kRightFootClothingItem]
removedSets = []

class xTakableClothing(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 211
        self.version = 3


    def OnFirstUpdate(self):
        global AgeStartedIn
        global baseMClothing
        global allMClothing
        global baseFClothing
        global allFClothing
        AgeStartedIn = PtGetAgeName()
        if xxConfig.isOnline() and AgeStartedIn in ['Personal02', 'spyroom', 'RestorationGuild', 'Myst', 'AhnySphere04', 'city']:
            # keep clothes in non-instanced ages
            boolStayVisible.value = true
        self.useChance = true
        self.shown = false
        if (not (((type(stringVarName.value) == type('')) and (stringVarName.value != '')))):
            PtDebugPrint(('ERROR: xTakableClothing.OnFirstUpdate():\tERROR: missing SDL var name on %s' % self.sceneobject.getName()))
        if (not (((type(stringFClothingName.value) == type('')) and (stringFClothingName.value != '')))):
            PtDebugPrint(('ERROR: xTakableClothing.OnFirstUpdate():\tERROR: missing female clothing name on %s' % self.sceneobject.getName()))
        if (not (((type(stringMClothingName.value) == type('')) and (stringMClothingName.value != '')))):
            PtDebugPrint(('ERROR: xTakableClothing.OnFirstUpdate():\tERROR: missing male clothing name on %s' % self.sceneobject.getName()))
        if (not (((type(stringChanceSDLName.value) == type('')) and (stringChanceSDLName.value != '')))):
            PtDebugPrint(('DEBUG: xTakableClothing.OnFirstUpdate(): Chance SDL var name is empty, so we will not use chance rolls for showing %s' % self.sceneobject.getName()))
            self.useChance = false
        allFClothing = stringFClothingName.value.split(';')
        for i in range(len(allFClothing)):
            allFClothing[i] = allFClothing[i].strip()
        baseFClothing = allFClothing[0]
        allMClothing = stringMClothingName.value.split(';')
        for i in range(len(allMClothing)):
            allMClothing[i] = allMClothing[i].strip()
        baseMClothing = allMClothing[0]
        if boolFirstUpdate.value:
            self.Initialize()


    def OnServerInitComplete(self):
        if (not boolFirstUpdate.value):
            self.Initialize()


    def Initialize(self):
        if (AgeStartedIn == PtGetAgeName()):
            ageSDL = PtGetAgeSDL()
            if ((type(stringVarName.value) == type('')) and (stringVarName.value != '')):
                try:
                    ageSDL.setNotify(self.key, stringVarName.value, 0.0)
                    if (not (ageSDL[stringVarName.value][0] ^ boolShowOnTrue.value)):
                        PtAtTimeCallback(self.key, 1, kEnableClothingTimer)
                        self.shown = true
                    else:
                        PtAtTimeCallback(self.key, 1, kDisableClothingTimer)
                except:
                    PtDebugPrint(("ERROR: xTakableClothing.OnServerInitComplete():\tERROR accessing ageSDL on %s so we're disabling" % self.sceneobject.getName()))
                    PtAtTimeCallback(self.key, 1, kDisableClothingTimer)
            else:
                PtDebugPrint(("ERROR: xTakableClothing.OnServerInitComplete():\tERROR: missing SDL var name on %s so we're disabling" % self.sceneobject.getName()))
                PtAtTimeCallback(self.key, 1, kDisableClothingTimer)
            if (self.useChance and (not self.shown)):
                try:
                    self.chanceAppearing = int(ageSDL[stringChanceSDLName.value][0])
                    PtDebugPrint(('DEBUG: xTakableClothing.OnServerInitComplete(): Chance of %s appearing is %d percent' % (self.sceneobject.getName(), self.chanceAppearing)))
                    PtAtTimeCallback(self.key, 1.5, kRollDiceTimer)
                except:
                    PtDebugPrint(('ERROR: xTakableClothing.OnServerInitComplete():\tERROR missing SDL var %s so we will not use chance rolls on %s' % (stringChanceSDLName.value, self.sceneobject.getName())))
                    self.useChance = false
                    self.chanceAppearing = 0
            else:
                self.chanceAppearing = 0
        if boolHasHairColor.value:
            PtAtTimeCallback(self.key, 1, kGetHairColorTimer)


    def OnTimer(self, id):
        global hairColor
        if (id == kEnableClothingTimer):
            self.IEnableClothing()
        elif (id == kDisableClothingTimer):
            self.IDisableClothing()
        elif (id == kGetHairColorTimer):
            hairColor = self.IGetHairColor()
        elif (id == kRollDiceTimer):
            rint = xRandom.randint(1, 100)
            PtDebugPrint(('DEBUG: xTakableClothing.OnTimer(): Rolled a %d against a DC of %d on %s, success on <=' % (rint, self.chanceAppearing, self.sceneobject.getName())))
            if (rint <= self.chanceAppearing):
                ageSDL = PtGetAgeSDL()
                ageSDL[stringVarName.value] = (boolShowOnTrue.value,)
                self.IEnableClothing()


    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        if (VARname != stringVarName.value):
            return
        if (AgeStartedIn != PtGetAgeName()):
            return
        ageSDL = PtGetAgeSDL()
        try:
            if (not (ageSDL[stringVarName.value][0] ^ boolShowOnTrue.value)):
                self.IEnableClothing()
            else:
                self.IDisableClothing()
        except:
            PtDebugPrint(("ERROR: xTakableClothing.OnSDLNotify():\tERROR reading age SDL on %s so we're disabling" % self.sceneobject.getName()))
            self.IDisableClothing()


    def IItemInCloset(self):
        avatar = PtGetLocalAvatar()
        clothingList = avatar.avatar.getWardrobeClothingList()
        currentgender = avatar.avatar.getAvatarClothingGroup()
        if (currentgender == kFemaleClothingGroup):
            clothingName = baseFClothing
        else:
            clothingName = baseMClothing
        for item in clothingList:
            if (clothingName == item[0]):
                return 1
        return 0


    def IGetHairColor(self):
        avatar = PtGetLocalAvatar()
        worn = avatar.avatar.getAvatarClothingList()
        for item in worn:
            name = item[0]
            type = item[1]
            if (type == kHairClothingItem):
                PtDebugPrint(('DEBUG: xTakableClothing.IGetHairColor():  Found current hair item: ' + name))
                color = avatar.avatar.getTintClothingItem(name, 1)
                PtDebugPrint(('DEBUG: xTakableClothing.IGetHairColor():  Hair color (r,g,b) = (%d,%d,%d)' % (color.getRed(), color.getGreen(), color.getBlue())))
                return color
        PtDebugPrint("ERROR: xTakableClothing.IGetHairColor():  Couldn't find the currently worn hair item, defaulting to white")
        return ptColor().white()


    def IGetTint(self, oneOrTwo):
        if (oneOrTwo == 1):
            red = intTint1Red.value
            green = intTint1Green.value
            blue = intTint1Blue.value
        else:
            red = intTint2Red.value
            green = intTint2Green.value
            blue = intTint2Blue.value
        red = (float(red) / 255)
        green = (float(green) / 255)
        blue = (float(blue) / 255)
        PtDebugPrint((((((((('Tint ' + str(oneOrTwo)) + ' is (') + str(red)) + ',') + str(green)) + ',') + str(blue)) + ')'))
        return ptColor(red, green, blue, 1)


    def IGetItem(self, name):
        avatar = PtGetLocalAvatar()
        for clothingType in clothingTypeList:
            clothingList = avatar.avatar.getClosetClothingList(clothingType)
            for clothingItem in clothingList:
                tempItem = ClothingItem(clothingItem)
                if (tempItem.name == name):
                    return tempItem
        accList = avatar.avatar.getClosetClothingList(kAccessoryClothingItem)
        for accItem in accList:
            tempAcc = ClothingItem(accItem)
            if (tempAcc.name == name):
                return tempAcc
        return None


    def IConflictsWithSet(self, name):
        clothingItem = self.IGetItem(name)
        if clothingItem:
            avatar = PtGetLocalAvatar()
            worn = avatar.avatar.getAvatarClothingList()
            for item in worn:
                tempItem = ClothingItem(item)
                if (tempItem.type == clothingItem.type):
                    if tempItem.isClothingSet:
                        return tempItem.clothingSet
        return ''


    def IRemoveWornSet(self, setName):
        if (setName == ''):
            return
        if (setName in removedSets):
            PtDebugPrint((('xTakableClothing: Set ' + setName) + ' already removed, skipping'))
            return
        PtDebugPrint(('xTakableClothing: Removing worn set ' + setName))
        removedSets.append(setName)
        avatar = PtGetLocalAvatar()
        worn = avatar.avatar.getAvatarClothingList()
        typesToReplace = []
        for item in worn:
            tempItem = ClothingItem(item)
            if (tempItem.isClothingSet and (tempItem.clothingSet == setName)):
                if (not (tempItem.accessoryType == -1)):
                    avatar.avatar.removeClothingItem(tempItem.name)
                else:
                    typesToReplace.append(tempItem.type)
        if (len(typesToReplace) > 0):
            for clothingType in typesToReplace:
                PtWearDefaultClothingType(avatar.getKey(), clothingType)


    def OnNotify(self, state, id, events):
        if (not (state)):
            return
        if (not (PtWasLocallyNotified(self.key))):
            PtDebugPrint('DEBUG: xTakableClothing.OnNotify(): Message didn\'t come from our player, ignoring')
            return
        if (id == actClickable.id):
            avatar = PtGetLocalAvatar()
            currentgender = avatar.avatar.getAvatarClothingGroup()
            if (currentgender == kFemaleClothingGroup):
                base = baseFClothing
            else:
                base = baseMClothing
            if (not boolStayVisible.value):
                ageSDL = PtGetAgeSDL()
                ageSDL[stringVarName.value] = ((not boolShowOnTrue.value),)
            if (not (self.IItemInCloset())):
                avatar.avatar.addWardrobeClothingItem(base, ptColor().white(), ptColor().white())
            PtYesNoDialog(self.key, 'Would you like to wear this item now?')
        elif (id == -1):
            for event in events:
                if ((event[1] == 'YesNo') and (event[3] == 1.0)):
                    avatar = PtGetLocalAvatar()
                    currentgender = avatar.avatar.getAvatarClothingGroup()
                    if (currentgender == kFemaleClothingGroup):
                        clothingNames = allFClothing
                        base = baseFClothing
                    else:
                        clothingNames = allMClothing
                        base = baseMClothing
                    color1 = self.IGetTint(1)
                    color2 = self.IGetTint(2)
                    if boolHasHairColor.value:
                        PtDebugPrint('DEBUG: xTakableClothing.OnNotify():  Using existing hair color since this is a hair item')
                        color1 = hairColor
                    self.IRemoveWornSet(self.IConflictsWithSet(base))
                    for name in clothingNames:
                        self.IRemoveWornSet(self.IConflictsWithSet(name))
                        PtDebugPrint(('DEBUG: xTakableClothing.OnNotify():  Wearing ' + name))
                        avatar.avatar.netForce(1)
                        avatar.avatar.wearClothingItem(name, 0)
                        avatar.avatar.tintClothingItem(name, color1, 0)
                        avatar.avatar.tintClothingItemLayer(name, color2, 2, 1)
                        matchingItem = avatar.avatar.getMatchingClothingItem(name)
                        if (type(matchingItem) == type([])):
                            avatar.avatar.wearClothingItem(matchingItem[0], 0)
                            avatar.avatar.tintClothingItem(matchingItem[0], color1, 0)
                            avatar.avatar.tintClothingItemLayer(matchingItem[0], color2, 2, 1)
                        avatar.avatar.saveClothing()
            else:
                PtDebugPrint((('DEBUG: xTakableClothing.OnNotify():  You already have ' + base) + " so I'm not going to give it to you again"))


    def IEnableClothing(self):
        if (not boolStayVisible.value) and (not ptVault().amOwnerOfCurrentAge()):
            PtDebugPrint(('DEBUG: xTakableClothing.IEnableClothing():  Disabling clickable on %s because this is not our age...' % self.sceneobject.getName()))
            actClickable.disable()
        else:
            PtDebugPrint(('DEBUG: xTakableClothing.IEnableClothing():  Enabling clickable on %s...' % self.sceneobject.getName()))
            actClickable.enable()


    def IDisableClothing(self):
        PtDebugPrint(('DEBUG: xAgeSDLBoolShowHide.IDisableClothing():  Disabling clickable on %s...' % self.sceneobject.getName()))
        actClickable.disable()



class ClothingItem:


    def __init__(self, clothing):
        self.name = ''
        self.type = 0
        self.groupwith = -1
        self.accessoryType = -1
        self.wornwith = []
        self.donotwear = 0
        self.coloredAsHair = 0
        self.isClothingSet = 0
        self.clothingSet = ''
        try:
            self.name = clothing[0]
            self.type = clothing[1]
            try:
                if (clothing[2] != ''):
                    self.description = xLocalization.xACA.xClothesXRef[clothing[2]]
            except:
                self.description = (('*' + clothing[2]) + '*')
            self.thumbnail = clothing[3]
            if (len(clothing[4]) > 0):
                parts = clothing[4].split(';')
                for part in parts:
                    parm = part.split('=')
                    try:
                        ls = string.lower(parm[0].strip())
                    except LookupError:
                        ls = ''
                    try:
                        rs = parm[1].strip()
                    except LookupError:
                        rs = ''
                    if (ls == 'clothingtype'):
                        rs = string.lower(rs)
                        if (rs == 'pants'):
                            self.groupwith = kPantsClothingItem
                        elif (rs == 'shirt'):
                            self.groupwith = kShirtClothingItem
                        elif (rs == 'hands'):
                            self.groupwith = kRightHandClothingItem
                        elif (rs == 'face'):
                            self.groupwith = kFaceClothingItem
                        elif (rs == 'hair'):
                            self.groupwith = kHairClothingItem
                        elif (rs == 'feet'):
                            self.groupwith = kRightFootClothingItem
                        else:
                            PtDebugPrint(('xTakableClothing: Unknown ClothingType %s' % rs))
                    elif (ls == 'accessorytype'):
                        self.accessoryType = 0
                    elif (ls == 'accessory'):
                        self.accessoryType = 0
                    elif (ls == 'wornwith'):
                        wearlist = rs.split(',')
                        for wearitem in wearlist:
                            self.wornwith.append(wearitem.strip())

                    elif (ls == 'donotwear'):
                        self.donotwear = 1
                    elif (ls == 'coloredashair'):
                        self.coloredAsHair = 1
                    elif (ls == 'clothingset'):
                        self.isClothingSet = 1
                        self.clothingSet = rs
        except (TypeError, LookupError):
            PtDebugPrint(('xTakableClothing: some kind of error on clothing ' + str(clothing)))


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



