# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
from colorsys import *
import string
import xLocalization
import PlasmaControlKeys
import time
InRoomActivator = ptAttribActivator(1, 'In the Room Activator')
AvCustGUI = ptAttribGUIDialog(2, 'The AvatarCustomizaion GUI')
ZoomCamera = ptAttribSceneobject(3, 'The Zoom in Camera')
Color1Map = ptAttribDynamicMap(4, 'Color 1 Dynamic Texture Map')
Color2Map = ptAttribDynamicMap(6, 'Color 2 Dynamic Texture Map')
SkinMap = ptAttribDynamicMap(7, 'Skin Color Dynamic Texture Map')
ColorMaterial = ptAttribMaterial(8, 'Color Material')
HairMaterial = ptAttribMaterial(9, 'Hair Color Material')
SkinMaterial = ptAttribMaterial(10, 'Skin Color Material')
kAvCustDialogName = 'AvatarCustomization'
kCalibrationDialogName = 'CalibrationGUI'
kCalibrationFadeOutID = 3
kCalibrationFadeOutSeconds = 0.5
kCalibrationFadeInSeconds = 1.0
InAvatarCloset = 0
kAvaCustaIsDone = 'InitialAvCustomizationsDone'
kAvaCustaIsDoneType = 0
kCleftSolved = 'CleftSolved'
kCalMessageText = 700
kPanelsRGID = 1
kLinkBackBtnID = 50
kQuitBtnID = 51
kAvatarResetID = 52
kAvatarReadID = 53
kAvatarSaveID = 54
kNameEBID = 5
kNameTBID = 55
kGenderRGID = 6
kHeightTBID = 7
kMaleCheckbox = 56
kFemaleCheckbox = 57
kYesNoTextID = 12
kYesButtonID = 10
kNoButtonID = 11
kNumberOfMorphs = 9
kMorphSliderOffset = 200
kWeightKnob = 200
kEyebrowsKnob = 201
kNoseWidthKnob = 202
kNoseLengthKnob = 203
kNoseAngleKnob = 204
kCheeksKnob = 205
kMouthKnob = 206
kChinWidthKnob = 207
kChinAngleKnob = 208
kNumberOfTexMorphs = 4
kTexMorphSliderOffset = 250
kAgeTexMorph = 251
kEthnic1TexMorph = 252
kEthnic2TexMorph = 253
kEthnic3TexMorph = 254
kZoomButton = 300
kColor1ClickMap = 63
kColor2ClickMap = 64
kSkinClickMap = 65
kHairClickMap = 66
kClothingDesc = 60
kColorbarName1 = 61
kColorbarName2 = 62
kFakeColorSlideBtn1 = 63
kFakeColorSlideBtn2 = 64
kFakeSkinSlideBtn = 65
kFakeHairSlideBtn = 66
kSliderMax = 12.0
kHairOptionsLB = 70
kHeadOptionsLB = 71
kUpperBodyOptionsLB = 72
kHandsOptionsLB = 73
kLwrBodyOptionsLB = 74
kFeetOptionsLB = 75
kAccessOptionsLB = 76
kAccessoryLBOffset = 10
kHairAccLB = 80
kHeadAccLB = 81
kUpperBodyAccLB = 82
kHandsAccLB = 83
kLwrBodyAccLB = 84
kFeetAccLB = 85
kAccessAccLB = 86
listboxDict = {}
panelOptListboxOffset = 70
panelAccListboxOffset = 80
kIDBtnLeftAccOffset = 320
kIDBtnHairLeftAccArrow = 400
kIDBtnHeadLeftAccArrow = 401
kIDBtnUpperBodyLeftAccArrow = 402
kIDBtnHandsLeftAccArrow = 403
kIDBtnLwrBodyLeftAccArrow = 404
kIDBtnFeetLeftAccArrow = 405
kIDBtnRightAccOffset = 330
kIDBtnHairRightAccArrow = 410
kIDBtnHeadRightAccArrow = 411
kIDBtnUpperBodyRightAccArrow = 412
kIDBtnHandsRightAccArrow = 413
kIDBtnLwrBodyRightAccArrow = 414
kIDBtnFeetRightAccArrow = 415
kIDBtnLeftOptOffset = 350
kIDBtnHairLeftOptArrow = 420
kIDBtnHeadLeftOptArrow = 421
kIDBtnUpperBodyLeftOptArrow = 422
kIDBtnHandsLeftOptArrow = 423
kIDBtnLwrBodyLeftOptArrow = 424
kIDBtnFeetLeftOptArrow = 425
kIDBtnRightOptOffset = 360
kIDBtnHairRightOptArrow = 430
kIDBtnHeadRightOptArrow = 431
kIDBtnUpperBodyRightOptArrow = 432
kIDBtnHandsRightOptArrow = 433
kIDBtnLwrBodyRightOptArrow = 434
kIDBtnFeetRightOptArrow = 435
kCLBMinWidth = 96
kCLBMinHeight = 104
kCLBImageX = 19
kCLBImageY = 18
kCLBImageWidth = 91
kCLBImageHeight = 97
kPrimaryListBoxSize = 8
kAccessoryLBSize = 8
TheCloset = None
kColorTypeNone = 0
kColorTypeNormal = 1
kColorTypeSkin = 2
kColorTypeHair = 3
CLxref = [
    [kHairClothingItem, kHairOptionsLB, kColorTypeHair, 0.25, 1, 1, 1, 1],
    [kFaceClothingItem, kHeadOptionsLB, kColorTypeSkin, 0.25, 1, 0, 1, 0],
    [kShirtClothingItem, kUpperBodyOptionsLB, kColorTypeNormal, 0.40000000000000002, 1, 1, 1, 1],
    [kRightHandClothingItem, kHandsOptionsLB, kColorTypeNone, 0.0, 2, 1, 1, 1],
    [kPantsClothingItem, kLwrBodyOptionsLB, kColorTypeNormal, 0.25, 1, 1, 1, 1],
    [kRightFootClothingItem, kFeetOptionsLB, kColorTypeNormal, 0.25, 2, 1, 1, 1]
]

def FindSaturationAndCloset(itemname, itemtype):
    for xref in CLxref:
        if (xref[0] == itemtype):
            return (xref[2], xref[3], xref[5], xref[6], xref[7])
    return (0, 0, 1, 1, 1)

kTimerUpdateMorphs = 99
kTimerUpdateControls = 100
WornList = []
DefaultClothing = []
DefaultColor1 = []
DefaultColor2 = []
DefaultSkinColor = None
DefaultGeomMorphs = []
DefaultTexMorphs = []
DefaultAgeMorph = None
untintableHeadAcc = ['03_FAccGoggles', '03_MAccGoggles', 'FReward_Goggles', 'MReward_Goggles']
clothingSets = []
clothingSetContents = {}
clothingGroups = []
clothingGroupContents = {}
clothingGroupIcons = {}
groupsAllowingAccessories = ['Catherine', 'Atrus']

def SetDefaultSettings():
    global DefaultClothing
    global DefaultAgeMorph
    global DefaultTexMorphs
    global DefaultSkinColor
    global DefaultGeomMorphs
    avatar = PtGetLocalAvatar()
    worn = avatar.avatar.getAvatarClothingList()
    DefaultClothing = []
    for item in worn:
        (colortype, saturation, inCloset, inClosClr1, inClosClr2) = FindSaturationAndCloset(item[0], item[1])
        DefaultClothing.append(ClothingItem(item, colortype, saturation, inCloset, inClosClr1, inClosClr2))
        DefaultColor1.append(avatar.avatar.getTintClothingItem(item[0], 1))
        DefaultColor2.append(avatar.avatar.getTintClothingItem(item[0], 2))
    DefaultSkinColor = avatar.avatar.getTintSkin()
    gender = avatar.avatar.getAvatarClothingGroup()
    geomMorphs = []
    for morphID in range(kNumberOfMorphs):
        morphVal = 0
        try:
            if (gender == kFemaleClothingGroup):
                morphVal = avatar.avatar.getMorph('FFace', morphID)
            else:
                morphVal = avatar.avatar.getMorph('MFace', morphID)
            geomMorphs.append(morphVal)
        except:
            pass
    if (len(geomMorphs) == kNumberOfMorphs):
        DefaultGeomMorphs = geomMorphs
    texMorphs = []
    for texMorphID in range(kNumberOfTexMorphs):
        try:
            morphVal = avatar.avatar.getSkinBlend(texMorphID)
            texMorphs.append(morphVal)
        except:
            pass
    if (len(texMorphs) == kNumberOfTexMorphs):
        DefaultTexMorphs = texMorphs
    try:
        morphVal = avatar.avatar.getSkinBlend(4)
        DefaultAgeMorph = morphVal
    except:
        pass


def SaveAvatarToDisk():
    avatar = PtGetLocalAvatar()
    worn = avatar.avatar.getAvatarClothingList()
    clothingList = []
    color1 = []
    color2 = []
    for item in worn:
        clothingList.append(item[0])
        color1.append(avatar.avatar.getTintClothingItem(item[0], 1))
        color2.append(avatar.avatar.getTintClothingItem(item[0], 2))
    skinColor = avatar.avatar.getTintSkin()
    gender = avatar.avatar.getAvatarClothingGroup()
    geomMorphs = []
    for morphID in range(kNumberOfMorphs):
        morphVal = 0
        try:
            if (gender == kFemaleClothingGroup):
                morphVal = avatar.avatar.getMorph('FFace', morphID)
            else:
                morphVal = avatar.avatar.getMorph('MFace', morphID)
        except:
            pass
        geomMorphs.append(morphVal)
    texMorphs = []
    for texMorphID in range(kNumberOfTexMorphs):
        morphVal = 0
        try:
            morphVal = avatar.avatar.getSkinBlend(texMorphID)
        except:
            pass
        texMorphs.append(morphVal)
    ageMorph = 0
    try:
        ageMorph = avatar.avatar.getSkinBlend(4)
    except:
        pass
    name = PtGetLocalPlayer().getPlayerName()
    saveFile = file((name + '.avatar.ava'), 'w')
    saveFile.write((str(len(clothingList)) + '\n'))
    for i in range(len(clothingList)):
        item = clothingList[i]
        item += (((((' ' + str(color1[i].getRed())) + ' ') + str(color1[i].getGreen())) + ' ') + str(color1[i].getBlue()))
        item += (((((' ' + str(color2[i].getRed())) + ' ') + str(color2[i].getGreen())) + ' ') + str(color2[i].getBlue()))
        saveFile.write((item + '\n'))
    saveFile.write((((((str(skinColor.getRed()) + ' ') + str(skinColor.getGreen())) + ' ') + str(skinColor.getBlue())) + '\n'))
    saveFile.write((str(len(geomMorphs)) + '\n'))
    for i in range(len(geomMorphs)):
        saveFile.write((str(geomMorphs[i]) + '\n'))
    saveFile.write((str(len(texMorphs)) + '\n'))
    for i in range(len(texMorphs)):
        saveFile.write((str(texMorphs[i]) + '\n'))
    saveFile.write((str(ageMorph) + '\n'))
    saveFile.close()


def GetClothingWorn():
    global WornList
    avatar = PtGetLocalAvatar()
    worn = avatar.avatar.getAvatarClothingList()
    WornList = []
    for item in worn:
        (colortype, saturation, inCloset, inClosClr1, inClosClr2) = FindSaturationAndCloset(item[0], item[1])
        WornList.append(ClothingItem(item, colortype, saturation, inCloset, inClosClr1, inClosClr2))


def IsWearing(item):
    for wornitem in WornList:
        if (wornitem.name == item.name):
            return 1
    return 0


def FindWornItem(clothing_type):
    for item in WornList:
        if (item.type == clothing_type):
            return item
    return None


def DateInRange(date, range):
    dateDay = date[2]
    dateMonth = date[1]
    dateYear = date[0]
    rangeDayMin = range[1][0]
    rangeDayMax = range[1][1]
    rangeMonthMin = range[0][0]
    rangeMonthMax = range[0][1]
    rangeYearMin = range[2][0]
    rangeYearMax = range[2][1]
    inRange = true
    if (not (((rangeYearMin == 0) or (rangeYearMax == 0)))):
        if ((dateYear < rangeYearMin) or (dateYear > rangeYearMax)):
            inRange = false
    if (not (((rangeMonthMin == 0) or (rangeMonthMax == 0)))):
        if ((dateMonth < rangeMonthMin) or (dateMonth > rangeMonthMax)):
            inRange = false
    if (not (((rangeDayMin == 0) or (rangeDayMax == 0)))):
        if ((dateDay < rangeDayMin) or (dateDay > rangeDayMax)):
            inRange = false
    return inRange


def CanShowSeasonal(clothingItem):
    if clothingItem.seasonal:
        if ItemInWardrobe(clothingItem):
            return true
        showTime = clothingItem.seasonTime
        if PtIsInternalRelease():
            curTime = time.localtime(time.time())
        else:
            curTime = time.localtime(PtGetServerTime())
        for timeRange in showTime:
            if DateInRange(curTime, timeRange):
                return true
        return false
    return true


def CanShowClothingItem(clothingItem):
    #if ((clothingItem.internalOnly and PtIsInternalRelease()) or (not (clothingItem.internalOnly))):
        if ((clothingItem.nonStandardItem and ItemInWardrobe(clothingItem)) or (not (clothingItem.nonStandardItem))):
            #if ((xxConfig.isOffline() and clothingItem.singlePlayer) or xxConfig.isOnline()):
                if CanShowSeasonal(clothingItem):
                    return true
                else:
                    PtDebugPrint((('CanShowClothingItem(): Hiding item ' + clothingItem.name) + ' because it is seasonal'))
            #else:
            #    PtDebugPrint((('CanShowClothingItem(): Hiding item ' + clothingItem.name) + ' because it is a multiplayer-only option'))
        else:
            PtDebugPrint((('CanShowClothingItem(): Hiding item ' + clothingItem.name) + ' because it is optional and isn\'t in your closet'))
    #else:
    #    PtDebugPrint((('CanShowClothingItem(): Hiding item ' + clothingItem.name) + ' because it is an internal-only option'))
        return false


def ItemInWardrobe(clothingItem):
    avatar = PtGetLocalAvatar()
    clothingList = avatar.avatar.getWardrobeClothingList()
    for item in clothingList:
        (ctype, saturation, inCloset, inClosClr1, inClosClr2) = FindSaturationAndCloset(item[0], item[1])
        closetItem = ClothingItem(item, ctype, saturation, inCloset, inClosClr1, inClosClr2)
        if (clothingItem.name == closetItem.name):
            return 1
    return 0


def GetAllWithSameGroup(name):
    retVal = []
    avatar = PtGetLocalAvatar()
    targetGroup = ''
    clothinglist = []
    groupFound = 0
    for idx in range(len(CLxref)):
        clothingType = CLxref[idx][0]
        clothinglist = avatar.avatar.getClosetClothingList(clothingType)
        for item in clothinglist:
            (ctype, saturation, inCloset, inClosClr1, inClosClr2) = FindSaturationAndCloset(item[0], item[1])
            newitem = ClothingItem(item, ctype, saturation, inCloset, inClosClr1, inClosClr2)
            if (newitem.name == name):
                targetGroup = newitem.groupName
                groupFound = 1
                break
        if groupFound:
            break
    if (targetGroup in clothingGroupContents):
        PtDebugPrint(('GetAllWithSameGroup(): Using pre-cached group for ' + targetGroup))
        return clothingGroupContents[targetGroup]
    PtDebugPrint(('GetAllWithSameGroup(): Manually calculating group for ' + targetGroup))
    for item in clothinglist:
        (ctype, saturation, inCloset, inClosClr1, inClosClr2) = FindSaturationAndCloset(item[0], item[1])
        newitem = ClothingItem(item, ctype, saturation, inCloset, inClosClr1, inClosClr2)
        if ((newitem.groupName == targetGroup) and (not newitem.meshicon)):
            if CanShowClothingItem(newitem):
                retVal.append(newitem)
    return retVal


def GroupHasClothing(iconItem):
    name = iconItem.name
    if TheCloset:
        clothingInGroup = TheCloset.getTextureGroup(name)
    else:
        clothingInGroup = GetAllWithSameGroup(name)
    if (len(clothingInGroup) > 0):
        return 1
    return 0


def UsesSameGroup(name1, name2):
    if TheCloset:
        group = TheCloset.getTextureGroup(name1)
    else:
        group = GetAllWithSameGroup(name1)
    for item in group:
        if (item.name == name2):
            return 1
    return 0


def IsRightArrow(id):
    if (((id >= kIDBtnHairRightAccArrow) and (id <= kIDBtnFeetRightAccArrow)) or ((id >= kIDBtnHairRightOptArrow) and (id <= kIDBtnFeetRightOptArrow))):
        return 1
    return 0


def IsLeftArrow(id):
    if (((id >= kIDBtnHairLeftAccArrow) and (id <= kIDBtnFeetLeftAccArrow)) or ((id >= kIDBtnHairLeftOptArrow) and (id <= kIDBtnFeetLeftOptArrow))):
        return 1
    return 0


def IsAccArrow(id):
    if (((id >= kIDBtnHairLeftAccArrow) and (id <= kIDBtnFeetLeftAccArrow)) or ((id >= kIDBtnHairRightAccArrow) and (id <= kIDBtnFeetRightAccArrow))):
        return 1
    return 0


def IsOptArrow(id):
    if (((id >= kIDBtnHairLeftOptArrow) and (id <= kIDBtnFeetLeftOptArrow)) or ((id >= kIDBtnHairRightOptArrow) and (id <= kIDBtnFeetRightOptArrow))):
        return 1
    return 0


class xAvatarCustomization(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 198
        self.version = 23
        minorVersion = 2
        PtDebugPrint(('__init__xAvatarCustomization v. %d.%d' % (self.version, minorVersion)))
        self.morphsLoaded = 0
        self.numTries = 0
        self.dirty = 0


    def SetupCamera(self):
        PtDebugPrint('Disabling first person...')
        cam = ptCamera()
        cam.undoFirstPerson()
        cam.disableFirstPersonOverride()
        PtDisableAvatarCursorFade()


    def OnAvatarSpawn(self, x):
        self.SetupCamera()


    def OnServerInitComplete(self):
        self.IInitFirst()


    def __del__(self):
        PtUnloadDialog(kAvCustDialogName)
        cam = ptCamera()
        cam.enableFirstPersonOverride()
        PtEnableAvatarCursorFade()


    def ILocalizeStaticText(self):
        kAgeText = 500
        kWeightText = 501
        kSkinColorText = 502
        kTexture1Text = 503
        kTexture2Text = 504
        kTexture3Text = 505
        kNoseAngleText = 506
        kNoseWidthText = 507
        kMouthText = 508
        kChinAngleText = 509
        kEyebrowsText = 510
        kNoseLengthText = 511
        kCheeksText = 512
        kChinWidthText = 513
        locStrings = xLocalization.xACA
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kAgeText)).setString(locStrings.xAge)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kWeightText)).setString(locStrings.xWeight)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kSkinColorText)).setString(locStrings.xSkinColor)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kTexture1Text)).setString(locStrings.xTexture1)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kTexture2Text)).setString(locStrings.xTexture2)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kTexture3Text)).setString(locStrings.xTexture3)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kNoseAngleText)).setString(locStrings.xNoseAngle)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kNoseWidthText)).setString(locStrings.xNoseWidth)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kMouthText)).setString(locStrings.xMouth)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kChinAngleText)).setString(locStrings.xChinAngle)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kEyebrowsText)).setString(locStrings.xEyebrows)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kNoseLengthText)).setString(locStrings.xNoseLength)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kCheeksText)).setString(locStrings.xCheeks)
        ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kChinWidthText)).setString(locStrings.xChinWidth)


    def OnNotify(self, state, id, events):
        if (state and (id == InRoomActivator.id)):
            PtSendKIMessage(kDisableKIandBB, 0)
            PtEnableMovementKeys()
            if (not InAvatarCloset):
                if PtIsDialogLoaded(kCalibrationDialogName):
                    PtLoadDialog(kCalibrationDialogName, self.key)
                    PtShowDialog(kCalibrationDialogName)
                PtLoadDialog(kAvCustDialogName, self.key)
            elif PtIsDialogLoaded(kAvCustDialogName):
                self.IInitAvaCusta()
            else:
                PtLoadDialog(kAvCustDialogName, self.key)
        elif (id == -1):
            if state:
                self.dirty = 0
                ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarResetID)).hide()
                self.IResetAvatar()


    def OnGUINotify(self, id, control, event):
        if (id == -1):
            if ((event == kAction) or (event == kValueChanged)):
                if isinstance(control, ptGUIControlButton):
                    PtFadeOut(kCalibrationFadeOutSeconds, 1)
                    PtAtTimeCallback(self.key, kCalibrationFadeOutSeconds, kCalibrationFadeOutID)
            if (event == kShowHide):
                if control.isEnabled():
                    textField = ptGUIControlTextBox(control.getControlFromTag(kCalMessageText))
                    textField.setString(xLocalization.xOptions.xCalMessageText)
        elif (id == AvCustGUI.id):
            if (event == kDialogLoaded):
                if InAvatarCloset:
                    self.IInitAvaCusta()
            elif ((event == kAction) or (event == kValueChanged)):
                tagID = control.getTagID()
                if isinstance(control, ptGUIControlValue):
                    self.dirty = 1
                    ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarResetID)).show()
                    if ((tagID >= kMorphSliderOffset) and (tagID < (kMorphSliderOffset + kNumberOfMorphs))):
                        self.IMorphItem(tagID)
                    else:
                        self.ITexMorphItem(tagID)
                elif isinstance(control, ptGUIControlClickMap):
                    self.dirty = 1
                    ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarResetID)).show()
                    self.IColorShowingItem(tagID)
                elif isinstance(control, ptGUIControlListBox):
                    self.dirty = 1
                    ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarResetID)).show()
                    clothing_group = TheCloset[tagID]
                    if ((tagID == kUpperBodyOptionsLB) or (tagID == kLwrBodyOptionsLB)):
                        itemselect = control.getSelection()
                        if (itemselect == -1):
                            avatar = PtGetLocalAvatar()
                            self.ISetWhatWearing(avatar)
                        else:
                            listboxDict[tagID].SelectItem(itemselect)
                            selectedItem = listboxDict[tagID].GetSelectedItem()
                            texGroup = TheCloset.getTextureGroup(selectedItem.name)
                            if (not texGroup):
                                listboxDict[(tagID + kAccessoryLBOffset)].SetClothingList([])
                            else:
                                listboxDict[(tagID + kAccessoryLBOffset)].SetClothingList(texGroup.clothingItems)
                            listboxDict[(tagID + kAccessoryLBOffset)].SelectItem(0)
                            listboxDict[(tagID + kAccessoryLBOffset)].UpdateScrollArrows()
                            listboxDict[(tagID + kAccessoryLBOffset)].UpdateListbox()
                            listbox = ptGUIControlListBox(AvCustGUI.dialog.getControlFromTag((tagID + kAccessoryLBOffset)))
                            self.OnGUINotify(AvCustGUI.id, listbox, kValueChanged)
                    elif (type(clothing_group) != type(None)):
                        itemselect = control.getSelection()
                        if (itemselect == -1):
                            avatar = PtGetLocalAvatar()
                            self.ISetWhatWearing(avatar)
                        else:
                            listboxDict[tagID].SelectItem(itemselect)
                            newitem = listboxDict[tagID].GetSelectedItem()
                            wornset = self.IIsWearingSetPiece(clothing_group.clothingType)
                            newset = newitem.clothingSet
                            if ((wornset != newset) and (wornset != '')):
                                self.IRemoveWornSet()
                            if newitem.isClothingSet:
                                self.IWearClothingSet(newitem.clothingSet)
                                return
                            lastitem = FindWornItem(clothing_group.clothingType)
                            avatar = PtGetLocalAvatar()
                            if (type(lastitem) != type(None)):
                                lastcolor1 = avatar.avatar.getTintClothingItem(lastitem.name, 1)
                                lastcolor2 = avatar.avatar.getTintClothingItem(lastitem.name, 2)
                            else:
                                lastcolor1 = ptColor().white()
                                lastcolor2 = ptColor().white()
                            if (clothing_group.numberItems > 1):
                                matchingItem = avatar.avatar.getMatchingClothingItem(newitem.name)
                                if (type(matchingItem) == type([])):
                                    avatar.avatar.wearClothingItem(matchingItem[0], 0)
                                    avatar.avatar.tintClothingItem(matchingItem[0], lastcolor1, 0)
                                    avatar.avatar.tintClothingItemLayer(matchingItem[0], lastcolor2, 2, 0)
                            avatar.avatar.wearClothingItem(newitem.name, 0)
                            avatar.avatar.tintClothingItem(newitem.name, lastcolor1, 0)
                            avatar.avatar.tintClothingItemLayer(newitem.name, lastcolor2, 2)
                            self.IMorphOneItem(kWeightKnob, newitem.name)
                            descbox = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kClothingDesc))
                            descbox.setString(newitem.description)
                            colorbar1 = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName1))
                            if (newitem.colorlabel1 == ''):
                                self.IHideColorPicker(kColor1ClickMap)
                            else:
                                self.IShowColorPicker(kColor1ClickMap)
                                colorbar1.setString(newitem.colorlabel1)
                                if (newitem.type == kHairClothingItem):
                                    self.IDrawPickerThingy(kHairClickMap, lastcolor1)
                                else:
                                    self.IDrawPickerThingy(kColor1ClickMap, lastcolor1)
                            colorbar2 = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName2))
                            if (newitem.colorlabel2 == ''):
                                self.IHideColorPicker(kColor2ClickMap)
                            else:
                                self.IShowColorPicker(kColor2ClickMap)
                                colorbar2.setString(newitem.colorlabel2)
                                self.IDrawPickerThingy(kColor2ClickMap, lastcolor2)
                    else:
                        clothing_group = TheCloset[(tagID - kAccessoryLBOffset)]
                        if (((tagID - kAccessoryLBOffset) == kUpperBodyOptionsLB) or ((tagID - kAccessoryLBOffset) == kLwrBodyOptionsLB)):
                            clothing_group = TheCloset[(tagID - kAccessoryLBOffset)]
                            if (type(clothing_group) != type(None)):
                                itemselect = control.getSelection()
                                if (len(listboxDict[tagID].clothingList) == 1):
                                    itemselect = 0
                                if (itemselect == -1):
                                    avatar = PtGetLocalAvatar()
                                    self.ISetWhatWearing(avatar)
                                else:
                                    listboxDict[tagID].SelectItem(itemselect)
                                    newitem = listboxDict[tagID].GetSelectedItem()
                                    wornset = self.IIsWearingSetPiece(clothing_group.clothingType)
                                    newset = newitem.clothingSet
                                    if ((wornset != newset) and (wornset != '')):
                                        self.IRemoveWornSet()
                                    if newitem.isClothingSet:
                                        self.IWearClothingSet(newitem.clothingSet)
                                        return
                                    avatar = PtGetLocalAvatar()
                                    lastitem = FindWornItem(clothing_group.clothingType)
                                    if (type(lastitem) != type(None)):
                                        lastcolor1 = avatar.avatar.getTintClothingItem(lastitem.name, 1)
                                        lastcolor2 = avatar.avatar.getTintClothingItem(lastitem.name, 2)
                                    else:
                                        lastcolor1 = ptColor().white()
                                        lastcolor2 = ptColor().white()
                                    avatar.avatar.wearClothingItem(newitem.name, 0)
                                    avatar.avatar.tintClothingItem(newitem.name, lastcolor1, 0)
                                    avatar.avatar.tintClothingItemLayer(newitem.name, lastcolor2, 2)
                                    self.IMorphOneItem(kWeightKnob, newitem.name)
                                    descbox = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kClothingDesc))
                                    descbox.setString(newitem.description)
                                    colorbar1 = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName1))
                                    if (newitem.colorlabel1 == ''):
                                        self.IHideColorPicker(kColor1ClickMap)
                                    else:
                                        self.IShowColorPicker(kColor1ClickMap)
                                        colorbar1.setString(newitem.colorlabel1)
                                        self.IDrawPickerThingy(kColor1ClickMap, lastcolor1)
                                    colorbar2 = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName2))
                                    if (newitem.colorlabel2 == ''):
                                        self.IHideColorPicker(kColor2ClickMap)
                                    else:
                                        self.IShowColorPicker(kColor2ClickMap)
                                        colorbar2.setString(newitem.colorlabel2)
                                        self.IDrawPickerThingy(kColor2ClickMap, lastcolor2)
                        elif (type(clothing_group) != type(None)):
                            itemselect = control.getSelection()
                            if (itemselect == -1):
                                avatar = PtGetLocalAvatar()
                                self.ISetWhatWearing(avatar)
                            else:
                                listboxDict[tagID].SelectItem(itemselect)
                                newitem = listboxDict[tagID].GetSelectedItem()
                                wornset = self.IIsWearingSetPiece(clothing_group.clothingType)
                                newset = newitem.clothingSet
                                if ((wornset != newset) and (wornset != '')):
                                    self.IRemoveWornSet()
                                if newitem.isClothingSet:
                                    self.IWearClothingSet(newitem.clothingSet)
                                    return
                                avatar = PtGetLocalAvatar()
                                lastitem = ''
                                for aitem in clothing_group.accessories:
                                    if (IsWearing(aitem) and (aitem.name != newitem.name)):
                                        avatar.avatar.removeClothingItem(aitem.name)
                                        lastitem = aitem.name
                                if (not newitem.donotwear):
                                    if newitem.coloredAsHair:
                                        haircolor = self.IGetHairColor()
                                        if (type(haircolor) != type(None)):
                                            avatar.avatar.wearClothingItem(newitem.name, 0)
                                            avatar.avatar.tintClothingItem(newitem.name, haircolor)
                                        else:
                                            avatar.avatar.wearClothingItem(newitem.name)
                                    else:
                                        avatar.avatar.wearClothingItem(newitem.name)
                                        if ((tagID == kHeadAccLB) and (not (newitem.name in untintableHeadAcc))):
                                            self.IShowColorPicker(kColor2ClickMap)
                                            colorbar2 = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName2))
                                            colorbar2.setString(xLocalization.xACA.xGlassesName)
                                            if (not (lastitem == '')):
                                                lastcolor = avatar.avatar.getTintClothingItem(lastitem, 1)
                                            else:
                                                lastcolor = ptColor(1, 1, 1, 1)
                                            avatar.avatar.tintClothingItem(newitem.name, lastcolor)
                                            self.IDrawPickerThingy(kColor2ClickMap, lastcolor)
                                        else:
                                            self.IHideColorPicker(kColor2ClickMap)
                                    self.IMorphOneItem(kWeightKnob, newitem.name)
                                elif (tagID == kHeadAccLB):
                                    self.IHideColorPicker(kColor2ClickMap)
                elif isinstance(control, ptGUIControlRadioGroup):
                    if (tagID == kPanelsRGID):
                        panelRG = ptGUIControlRadioGroup(AvCustGUI.dialog.getControlFromTag(kPanelsRGID))
                        rgVal = panelRG.getValue()
                        zoomBtn = ptGUIControlCheckBox(AvCustGUI.dialog.getControlFromTag(kZoomButton))
                        if (rgVal == 1):
                            zoomBtn.show()
                            zoomBtn.setChecked(true)
                            ZoomCamera.sceneobject.pushCutsceneCamera(1, PtGetLocalAvatar().getKey())
                            panelRG.hide()
                            self.SetupCamera()
                        else:
                            zoomBtn.hide()
                        descbox = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kClothingDesc))
                        descbox.setString('')
                        self.ISetStandardControls()
                elif isinstance(control, ptGUIControlButton):
                    btnID = control.getTagID()
                    if (btnID == kLinkBackBtnID):
                        if (not (ptNetLinkingMgr().isEnabled())):
                            PtDebugPrint('OnGuiNotify():\tAborting linkout attempt because the linking managar isn\'t ready')
                            return
                        avatar = PtGetLocalAvatar()
                        self.ISaveSeasonalToCloset()
                        avatar.avatar.saveClothing()
                        PtEnableAvatarJump()
                        # BEGIN DarkFalkon's 1st/3rd person patch
                        cam = ptCamera()
                        cam.enableFirstPersonOverride()
                        # END DarkFalkon's 1st/3rd person patch
                        if InAvatarCloset:
                            vault = ptVault()
                            entry = vault.findChronicleEntry(kCleftSolved)
                            linkmgr = ptNetLinkingMgr()
                            if (type(entry) != type(None)):
                                self.ILinkToCloset()
                            else:
                                ageLink = ptAgeLinkStruct()
                                ageInfo = ageLink.getAgeInfo()
                                temp = ptAgeInfoStruct()
                                temp.copyFrom(ageInfo)
                                ageInfo = temp
                                if PtIsDemoMode():
                                    ageInfo.setAgeFilename('Demo')
                                else:
                                    ageInfo.setAgeFilename('Cleft')
                                ageInfo.setAgeInstanceName("D'ni-Riltagamin")
                                ageLink.setAgeInfo(ageInfo)
                                ageLink.setLinkingRules(PtLinkingRules.kOriginalBook)
                                linkmgr.linkToAge(ageLink)
                        else:
                            vault = ptVault()
                            vault.addChronicleEntry(kAvaCustaIsDone, kAvaCustaIsDoneType, '1')
                            entry = vault.findChronicleEntry(kCleftSolved)
                            if (type(entry) != type(None)):
                                linkmgr = ptNetLinkingMgr()
                                ageLink = ptAgeLinkStruct()
                                ageInfo = ageLink.getAgeInfo()
                                temp = ptAgeInfoStruct()
                                temp.copyFrom(ageInfo)
                                ageInfo = temp
                                ageInfo.setAgeFilename('Personal')
                                ageLink.setAgeInfo(ageInfo)
                                ageLink.setLinkingRules(PtLinkingRules.kOriginalBook)
                                linkmgr.linkToAge(ageLink)
                            else:
                                ageLink = ptAgeLinkStruct()
                                ageInfo = ageLink.getAgeInfo()
                                temp = ptAgeInfoStruct()
                                temp.copyFrom(ageInfo)
                                ageInfo = temp
                                if PtIsDemoMode():
                                    ageInfo.setAgeFilename('Demo')
                                else:
                                    ageInfo.setAgeFilename('Cleft')
                                ageInfo.setAgeInstanceName("D'ni-Riltagamin")
                                ageLink.setAgeInfo(ageInfo)
                                ageLink.setLinkingRules(PtLinkingRules.kOriginalBook)
                                linkmgr = ptNetLinkingMgr()
                                linkmgr.linkToAge(ageLink)
                    elif (btnID == kQuitBtnID):
                        avatar = PtGetLocalAvatar()
                        self.ISaveSeasonalToCloset()
                        avatar.avatar.saveClothing()
                        PtSendKIMessage(kQuitDialog, 0)
                    elif IsAccArrow(btnID):
                        panelRG = ptGUIControlRadioGroup(AvCustGUI.dialog.getControlFromTag(kPanelsRGID))
                        rgVal = panelRG.getValue()
                        listboxID = (panelAccListboxOffset + rgVal)
                        if IsLeftArrow(btnID):
                            listboxDict[listboxID].DecrementOffset()
                        else:
                            listboxDict[listboxID].IncrementOffset()
                        listboxDict[listboxID].UpdateScrollArrows()
                        listboxDict[listboxID].UpdateListbox()
                    elif IsOptArrow(btnID):
                        panelRG = ptGUIControlRadioGroup(AvCustGUI.dialog.getControlFromTag(kPanelsRGID))
                        rgVal = panelRG.getValue()
                        listboxID = (panelOptListboxOffset + rgVal)
                        if IsLeftArrow(btnID):
                            listboxDict[listboxID].DecrementOffset()
                        else:
                            listboxDict[listboxID].IncrementOffset()
                        listboxDict[listboxID].UpdateScrollArrows()
                        listboxDict[listboxID].UpdateListbox()
                    elif (btnID == kAvatarResetID):
                        PtDebugPrint('Confirming reset...')
                        PtYesNoDialog(self.key, xLocalization.xACA.xResetConfirm)
                    elif (btnID == kAvatarReadID):
                        if PtIsInternalRelease():
                            self.IRestoreAvatarFromDisk()
                            self.dirty = 1
                            ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarResetID)).show()
                    elif (btnID == kAvatarSaveID):
                        if PtIsInternalRelease():
                            SaveAvatarToDisk()
                elif isinstance(control, ptGUIControlCheckBox):
                    chkBoxID = control.getTagID()
                    if (chkBoxID == kZoomButton):
                        zoomBtn = ptGUIControlCheckBox(AvCustGUI.dialog.getControlFromTag(chkBoxID))
                        radioGroup = ptGUIControlRadioGroup(AvCustGUI.dialog.getControlFromTag(kPanelsRGID))
                        if zoomBtn.isChecked():
                            ZoomCamera.sceneobject.pushCutsceneCamera(1, PtGetLocalAvatar().getKey())
                            radioGroup.hide()
                            self.SetupCamera()
                        else:
                            ZoomCamera.sceneobject.popCutsceneCamera(PtGetLocalAvatar().getKey())
                            radioGroup.show()
                            self.SetupCamera()


    def IResetAvatar(self):
        PtDebugPrint('Resetting avatar...')
        avatar = PtGetLocalAvatar()
        for item in WornList:
            if (item.accessoryType >= 0):
                found = 0
                for acc in DefaultClothing:
                    if (acc.name == item.name):
                        found = 1
                        break
                if (not found):
                    avatar.avatar.removeClothingItem(item.name)
        for i in range(len(DefaultClothing)):
            item = DefaultClothing[i]
            color1 = DefaultColor1[i]
            color2 = DefaultColor2[i]
            avatar.avatar.wearClothingItem(item.name, 0)
            avatar.avatar.tintClothingItem(item.name, color1, 0)
            avatar.avatar.tintClothingItemLayer(item.name, color2, 2)
            matchingItem = avatar.avatar.getMatchingClothingItem(item.name)
            if (type(matchingItem) == type([])):
                avatar.avatar.wearClothingItem(matchingItem[0], 0)
                avatar.avatar.tintClothingItem(matchingItem[0], color1, 0)
                avatar.avatar.tintClothingItemLayer(matchingItem[0], color2, 2, 0)
        avatar.avatar.tintSkin(DefaultSkinColor)
        for morphID in range(len(DefaultGeomMorphs)):
            gender = avatar.avatar.getAvatarClothingGroup()
            if (gender == kFemaleClothingGroup):
                avatar.avatar.setMorph('FFace', morphID, DefaultGeomMorphs[morphID])
            else:
                avatar.avatar.setMorph('MFace', morphID, DefaultGeomMorphs[morphID])
        for morphID in range(len(DefaultTexMorphs)):
            avatar.avatar.setSkinBlend(morphID, DefaultTexMorphs[morphID])
        avatar.avatar.setSkinBlend(4, DefaultAgeMorph)
        PtAtTimeCallback(self.key, 1, kTimerUpdateControls)


    def IRestoreAvatarFromDisk(self):
        name = PtGetLocalPlayer().getPlayerName()
        try:
            saveFile = file((name + '.avatar.ava'), 'r')
            numClothingItems = int(saveFile.readline())
            clothingList = []
            color1 = []
            color2 = []
            for i in range(numClothingItems):
                line = saveFile.readline()
                items = string.split(line)
                clothingList.append(items[0])
                color1.append(ptColor(float(items[1]), float(items[2]), float(items[3])))
                color2.append(ptColor(float(items[4]), float(items[5]), float(items[6])))
            line = saveFile.readline()
            items = string.split(line)
            skinColor = ptColor(float(items[0]), float(items[1]), float(items[2]))
            numMorphs = int(saveFile.readline())
            geomMorphs = []
            for i in range(numMorphs):
                morphVal = float(saveFile.readline())
                geomMorphs.append(morphVal)
            numMorphs = int(saveFile.readline())
            texMorphs = []
            for i in range(numMorphs):
                morphVal = float(saveFile.readline())
                texMorphs.append(morphVal)
            ageMorph = float(saveFile.readline())
            saveFile.close()
            avatar = PtGetLocalAvatar()
            for item in WornList:
                if (item.accessoryType >= 0):
                    found = 0
                    for acc in DefaultClothing:
                        if (acc.name == item.name):
                            found = 1
                            break
                    if (not found):
                        avatar.avatar.removeClothingItem(item.name)
            for i in range(len(clothingList)):
                item = clothingList[i]
                clr1 = color1[i]
                clr2 = color2[i]
                avatar.avatar.wearClothingItem(item, 0)
                avatar.avatar.tintClothingItem(item, clr1, 0)
                avatar.avatar.tintClothingItemLayer(item, clr2, 2)
                matchingItem = avatar.avatar.getMatchingClothingItem(item)
                if (type(matchingItem) == type([])):
                    avatar.avatar.wearClothingItem(matchingItem[0], 0)
                    avatar.avatar.tintClothingItem(matchingItem[0], clr1, 0)
                    avatar.avatar.tintClothingItemLayer(matchingItem[0], clr2, 2, 0)
            avatar.avatar.tintSkin(skinColor)
            for morphID in range(len(geomMorphs)):
                gender = avatar.avatar.getAvatarClothingGroup()
                if (gender == kFemaleClothingGroup):
                    avatar.avatar.setMorph('FFace', morphID, geomMorphs[morphID])
                else:
                    avatar.avatar.setMorph('MFace', morphID, geomMorphs[morphID])
            for morphID in range(len(texMorphs)):
                avatar.avatar.setSkinBlend(morphID, texMorphs[morphID])
            avatar.avatar.setSkinBlend(4, ageMorph)
            PtAtTimeCallback(self.key, 1, kTimerUpdateControls)
        except IOError:
            pass


    def IIsWearingSetPiece(self, type):
        item = FindWornItem(type)
        return item.clothingSet


    def IWearClothingSet(self, setName):
        try:
            theSet = clothingSetContents[setName]
        except:
            PtDebugPrint((('Non-existant set ' + setName) + ' requested, not wearing'))
            return
        PtDebugPrint(('Wearing clothing set ' + setName))
        avatar = PtGetLocalAvatar()
        if (not ((setName in groupsAllowingAccessories))):
            PtDebugPrint((('Set ' + setName) + ' doesn\'t allow accessories, removing them'))
            for item in WornList:
                if (item.accessoryType >= 0):
                    avatar.avatar.removeClothingItem(item.name)
        for newitem in theSet:
            if (newitem.accessoryType == -1):
                lastitem = FindWornItem(newitem.type)
                if (type(lastitem) != type(None)):
                    lastcolor1 = avatar.avatar.getTintClothingItem(lastitem.name, 1)
                    lastcolor2 = avatar.avatar.getTintClothingItem(lastitem.name, 2)
                else:
                    lastcolor1 = ptColor().white()
                    lastcolor2 = ptColor().white()
            else:
                lastcolor1 = ptColor().white()
                lastcolor2 = ptColor().white()
            avatar.avatar.wearClothingItem(newitem.name, 0)
            avatar.avatar.tintClothingItem(newitem.name, lastcolor1, 0)
            avatar.avatar.tintClothingItemLayer(newitem.name, lastcolor2, 2)
            self.IMorphOneItem(kWeightKnob, newitem.name)
            matchingItem = avatar.avatar.getMatchingClothingItem(newitem.name)
            if (type(matchingItem) == type([])):
                avatar.avatar.wearClothingItem(matchingItem[0], 0)
                avatar.avatar.tintClothingItem(matchingItem[0], lastcolor1, 0)
                avatar.avatar.tintClothingItemLayer(matchingItem[0], lastcolor2, 2, 0)
        PtAtTimeCallback(self.key, 1, kTimerUpdateControls)


    def IRemoveWornSet(self):
        setToRemove = ''
        for item in WornList:
            if item.isClothingSet:
                setToRemove = item.clothingSet
        if (setToRemove == ''):
            return
        try:
            theSet = clothingSetContents[setToRemove]
        except:
            PtDebugPrint((('Non-existant set ' + setToRemove) + ' requested, not removing'))
            return
        PtDebugPrint(('Removing clothing set ' + setToRemove))
        avatar = PtGetLocalAvatar()
        typesToReplace = []
        for olditem in theSet:
            if (not (olditem.accessoryType == -1)):
                avatar.avatar.removeClothingItem(olditem.name)
            else:
                typesToReplace.append(olditem.type)
                if (olditem.type == kRightHandClothingItem):
                    typesToReplace.append(kLeftHandClothingItem)
                elif (olditem.type == kRightFootClothingItem):
                    typesToReplace.append(kLeftFootClothingItem)
        typesNeedingDefault = []
        for clothingType in typesToReplace:
            for i in range(len(DefaultClothing)):
                if (DefaultClothing[i].type == clothingType):
                    if DefaultClothing[i].isClothingSet:
                        typesNeedingDefault.append(clothingType)
                    else:
                        item = DefaultClothing[i]
                        color1 = DefaultColor1[i]
                        color2 = DefaultColor2[i]
                        avatar.avatar.wearClothingItem(item.name, 0)
                        avatar.avatar.tintClothingItem(item.name, color1, 0)
                        avatar.avatar.tintClothingItemLayer(item.name, color2, 2)
                        matchingItem = avatar.avatar.getMatchingClothingItem(item.name)
                        if (type(matchingItem) == type([])):
                            avatar.avatar.wearClothingItem(matchingItem[0], 0)
                            avatar.avatar.tintClothingItem(matchingItem[0], color1, 0)
                            avatar.avatar.tintClothingItemLayer(matchingItem[0], color2, 2, 0)
        if (len(typesNeedingDefault) > 0):
            for clothingType in typesNeedingDefault:
                PtWearDefaultClothingType(avatar.getKey(), clothingType)
        PtAtTimeCallback(self.key, 1, kTimerUpdateControls)


    def ISaveSeasonalToCloset(self):
        for item in WornList:
            if (item.seasonal and (not ItemInWardrobe(item))):
                PtDebugPrint((('Adding seasonal item ' + item.name) + ' to your closet since you are wearing it'))
                avatar = PtGetLocalAvatar()
                avatar.avatar.addWardrobeClothingItem(item.name, ptColor().white(), ptColor().white())


    def ILinkToCloset(self):
        linkmgr = ptNetLinkingMgr()
        ageLink = ptAgeLinkStruct()
        ageInfo = ageLink.getAgeInfo()
        temp = ptAgeInfoStruct()
        temp.copyFrom(ageInfo)
        ageInfo = temp
        ageInfo.setAgeFilename('Personal')
        spawnPoint = ageLink.getSpawnPoint()
        spawnPoint.setName('LinkInPointCloset')
        ageLink.setAgeInfo(ageInfo)
        ageLink.setSpawnPoint(spawnPoint)
        ageLink.setLinkingRules(PtLinkingRules.kOwnedBook)
        linkmgr.linkToAge(ageLink)


    def IInitFirst(self):
        global InAvatarCloset
        vault = ptVault()
        entry = vault.findChronicleEntry(kAvaCustaIsDone)
        InAvatarCloset = 0
        if (type(entry) != type(None)):
            InAvatarCloset = 1
        PtDebugPrint(('AvaCusta: InAvatarCloset is %d' % InAvatarCloset))
        entry = vault.findChronicleEntry('GiveYeeshaReward')
        if (type(entry) != type(None)):
            avatar = PtGetLocalAvatar()
            currentgender = avatar.avatar.getAvatarClothingGroup()
            if (currentgender == kFemaleClothingGroup):
                clothingName = '02_FTorso11_01'
            else:
                clothingName = '02_MTorso09_01'
            clothingList = avatar.avatar.getWardrobeClothingList()
            if (clothingName not in clothingList):
                print ('adding Yeesha reward clothing %s to wardrobe' % clothingName)
                avatar.avatar.addWardrobeClothingItem(clothingName, ptColor().white(), ptColor().black())
            else:
                print 'player already has Yeesha reward clothing, doing nothing'
            folder = vault.getChronicleFolder()
            if (type(folder) != type(None)):
                folder.removeNode(entry)


    def IInitAvaCusta(self):
        self.IUpdateAllControls()
        SetDefaultSettings()
        PtDisableAvatarCursorFade()
        AvCustGUI.dialog.show()
        PtDisableAvatarJump()
        self.ILocalizeStaticText()
        self.SetupCamera()


    def OnClothingUpdate(self):
        GetClothingWorn()


    def IGetHairColor(self):
        avatar = PtGetLocalAvatar()
        for item in WornList:
            if (item.type == kHairClothingItem):
                return avatar.avatar.getTintClothingItem(item.name, 1)
        return None


    def OnTimer(self, id):
        if (id == kCalibrationFadeOutID):
            PtHideDialog(kCalibrationDialogName)
            self.IInitAvaCusta()
            PtFadeIn(kCalibrationFadeInSeconds, 0)
            return
        if ((id == kTimerUpdateMorphs) and (not self.morphsLoaded)):
            self.numTries = (self.numTries + 1)
            if (self.numTries < 5):
                self.IUpdateAllControls()
                SetDefaultSettings()
        elif (id == kTimerUpdateControls):
            self.IUpdateAllControls()


    def IUpdateAllControls(self):
        avatar = PtGetLocalAvatar()
        namebox = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kNameTBID))
        namebox.show()
        editbox = ptGUIControlEditBox(AvCustGUI.dialog.getControlFromTag(kNameEBID))
        editbox.hide()
        localplayer = PtGetLocalPlayer()
        namebox.setString(localplayer.getPlayerName())
        panelRG = ptGUIControlRadioGroup(AvCustGUI.dialog.getControlFromTag(kPanelsRGID))
        clothing_panel = panelRG.getValue()
        zoomBtn = ptGUIControlCheckBox(AvCustGUI.dialog.getControlFromTag(kZoomButton))
        if (clothing_panel == 1):
            zoomBtn.show()
        else:
            zoomBtn.hide()
        Color1Map.textmap.clearToColor(ptColor(0, 0, 0, 0))
        Color1Map.textmap.flush()
        Color2Map.textmap.clearToColor(ptColor(0, 0, 0, 0))
        Color2Map.textmap.flush()
        SkinMap.textmap.clearToColor(ptColor(0, 0, 0, 0))
        SkinMap.textmap.flush()
        GetClothingWorn()
        self.IUpdateClothingListboxes(avatar)
        self.ISetWhatWearing(avatar)
        self.ISetStandardControls()


    def IUpdateClothingListboxes(self, avatar):
        global TheCloset
        listbox = ptGUIControlListBox(AvCustGUI.dialog.getControlFromTag(kAccessOptionsLB))
        listbox.hide()
        if (TheCloset == None):
            TheCloset = ClothingCloset()
        for listboxID in TheCloset.keys():
            group = TheCloset[listboxID]
            if (not (listboxID in listboxDict)):
                listboxDict[listboxID] = ScrollingListBox()
                listboxDict[listboxID].SetListboxID(listboxID)
            if (not ((listboxID + kAccessoryLBOffset) in listboxDict)):
                listboxDict[(listboxID + kAccessoryLBOffset)] = ScrollingListBox()
                listboxDict[(listboxID + kAccessoryLBOffset)].SetListboxID((listboxID + kAccessoryLBOffset))
            listboxDict[listboxID].SetClothingList(group.clothingItems)
            listboxDict[listboxID].UpdateScrollArrows()
            listboxDict[listboxID].UpdateListbox()
            if ((listboxID == kUpperBodyOptionsLB) or (listboxID == kLwrBodyOptionsLB)):
                targetMesh = listboxDict[listboxID].GetSelectedItem()
                texGroup = TheCloset.getTextureGroup(targetMesh.name)
                if (not texGroup):
                    listboxDict[(listboxID + kAccessoryLBOffset)].SetClothingList([])
                else:
                    listboxDict[(listboxID + kAccessoryLBOffset)].SetClothingList(texGroup.clothingItems)
                listboxDict[(listboxID + kAccessoryLBOffset)].UpdateScrollArrows()
                listboxDict[(listboxID + kAccessoryLBOffset)].UpdateListbox()
            else:
                listboxDict[(listboxID + kAccessoryLBOffset)].SetClothingList(group.accessories)
                listboxDict[(listboxID + kAccessoryLBOffset)].UpdateScrollArrows()
                listboxDict[(listboxID + kAccessoryLBOffset)].UpdateListbox()


    def ISetWhatWearing(self, avatar):
        for id in TheCloset.keys():
            listboxDict[id].SetWhatWearing()
            listboxDict[id].UpdateScrollArrows()
            listboxDict[id].UpdateListbox()
            if ((id == kUpperBodyOptionsLB) or (id == kLwrBodyOptionsLB)):
                targetMesh = listboxDict[id].GetSelectedItem()
                group = TheCloset[id]
                texGroup = TheCloset.getTextureGroup(targetMesh.name)
                if (not texGroup):
                    listboxDict[(id + kAccessoryLBOffset)].SetClothingList([])
                else:
                    listboxDict[(id + kAccessoryLBOffset)].SetClothingList(texGroup.clothingItems)
                listboxDict[(id + kAccessoryLBOffset)].SetWhatWearing()
                listboxDict[(id + kAccessoryLBOffset)].UpdateScrollArrows()
                listboxDict[(id + kAccessoryLBOffset)].UpdateListbox()
            else:
                listboxDict[(id + kAccessoryLBOffset)].SetWhatWearing()
                listboxDict[(id + kAccessoryLBOffset)].UpdateScrollArrows()
                listboxDict[(id + kAccessoryLBOffset)].UpdateListbox()


    def IColorShowingItem(self, controlID):
        panelRG = ptGUIControlRadioGroup(AvCustGUI.dialog.getControlFromTag(kPanelsRGID))
        clothing_panel = panelRG.getValue()
        foundItem = 0
        if ((clothing_panel >= 0) and (clothing_panel < len(CLxref))):
            clothing_type = CLxref[clothing_panel][0]
            wornItem = FindWornItem(clothing_type)
            if (type(wornItem) != type(None)):
                if ((controlID == kColor1ClickMap) or (controlID == kColor2ClickMap)):
                    if (controlID == kColor2ClickMap):
                        layer = 2
                        colormap = ptGUIControlClickMap(AvCustGUI.dialog.getControlFromTag(kColor2ClickMap)).getLastMouseUpPoint()
                        colorit = ColorMaterial.map.getPixelColor(colormap.getX(), colormap.getY())
                        self.IDrawCrosshair(kColor2ClickMap, colormap.getX(), colormap.getY())
                    else:
                        layer = 1
                        colormap = ptGUIControlClickMap(AvCustGUI.dialog.getControlFromTag(kColor1ClickMap)).getLastMouseUpPoint()
                        colorit = ColorMaterial.map.getPixelColor(colormap.getX(), colormap.getY())
                        self.IDrawCrosshair(kColor1ClickMap, colormap.getX(), colormap.getY())
                    avatar = PtGetLocalAvatar()
                    clothing_group = TheCloset[CLxref[clothing_panel][1]]
                    if (clothing_group.numberItems > 1):
                        matchingItem = avatar.avatar.getMatchingClothingItem(wornItem.name)
                        if (type(matchingItem) == type([])):
                            avatar.avatar.tintClothingItemLayer(matchingItem[0], colorit, layer, 0)
                    avatar.avatar.tintClothingItemLayer(wornItem.name, colorit, layer)
                    if ((clothing_type == kFaceClothingItem) and (layer == 2)):
                        for aitem in clothing_group.accessories:
                            if IsWearing(aitem):
                                avatar.avatar.tintClothingItem(aitem.name, colorit)
                elif (controlID == kSkinClickMap):
                    colormap = ptGUIControlClickMap(AvCustGUI.dialog.getControlFromTag(kSkinClickMap)).getLastMouseUpPoint()
                    colorskin = SkinMaterial.map.getPixelColor(colormap.getX(), colormap.getY())
                    self.IDrawCrosshair(kSkinClickMap, colormap.getX(), colormap.getY())
                    avatar = PtGetLocalAvatar()
                    avatar.avatar.tintSkin(colorskin)
                elif (controlID == kHairClickMap):
                    colormap = ptGUIControlClickMap(AvCustGUI.dialog.getControlFromTag(kHairClickMap)).getLastMouseUpPoint()
                    colorit = HairMaterial.map.getPixelColor(colormap.getX(), colormap.getY())
                    self.IDrawCrosshair(kHairClickMap, colormap.getX(), colormap.getY())
                    avatar = PtGetLocalAvatar()
                    for item in WornList:
                        if ((item.type == kHairClothingItem) or item.coloredAsHair):
                            avatar.avatar.tintClothingItemLayer(item.name, colorit, 1)


    def IMorphOneItem(self, knobID, itemName):
        if ((knobID < kMorphSliderOffset) or (knobID >= (kMorphSliderOffset + kNumberOfMorphs))):
            return
        morphKnob = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(knobID))
        morphVal = self.ISliderToMorph(morphKnob.getValue())
        avatar = PtGetLocalAvatar()
        item = TheCloset.getItemByName(itemName)
        if (item == None):
            return
        gender = avatar.avatar.getAvatarClothingGroup()
        if (gender == kFemaleClothingGroup):
            avatar.avatar.setMorph('FFace', (knobID - kMorphSliderOffset), morphVal)
        else:
            avatar.avatar.setMorph('MFace', (knobID - kMorphSliderOffset), morphVal)


    def IMorphItem(self, knobID):
        GetClothingWorn()
        if ((knobID < kMorphSliderOffset) or (knobID >= (kMorphSliderOffset + kNumberOfMorphs))):
            return
        morphKnob = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(knobID))
        morphVal = self.ISliderToMorph(morphKnob.getValue())
        avatar = PtGetLocalAvatar()
        gender = avatar.avatar.getAvatarClothingGroup()
        if (gender == kFemaleClothingGroup):
            avatar.avatar.setMorph('FFace', (knobID - kMorphSliderOffset), morphVal)
        else:
            avatar.avatar.setMorph('MFace', (knobID - kMorphSliderOffset), morphVal)


    def ITexMorphItem(self, knobID):
        if ((knobID <= kTexMorphSliderOffset) or (knobID > (kTexMorphSliderOffset + kNumberOfTexMorphs))):
            return
        morphKnob = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(knobID))
        morphVal = self.ISliderToTexMorph(morphKnob.getValue())
        avatar = PtGetLocalAvatar()
        if (knobID == kAgeTexMorph):
            avatar.avatar.setSkinBlend(4, morphVal)
        else:
            morphID1 = 0
            morphID2 = 0
            if (knobID == kEthnic1TexMorph):
                morphID1 = kEthnic2TexMorph
                morphID2 = kEthnic3TexMorph
            elif (knobID == kEthnic2TexMorph):
                morphID1 = kEthnic1TexMorph
                morphID2 = kEthnic3TexMorph
            else:
                morphID1 = kEthnic1TexMorph
                morphID2 = kEthnic2TexMorph
            morphKnob1 = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(morphID1))
            morphKnob2 = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(morphID2))
            morphVal1 = self.ISliderToTexMorph(morphKnob1.getValue())
            morphVal2 = self.ISliderToTexMorph(morphKnob2.getValue())
            total = ((morphVal + morphVal1) + morphVal2)
            if (total > 1.0):
                adjustment = ((total - 1.0) / 2.0)
                morphVal1 -= adjustment
                morphVal2 -= adjustment
                if (morphVal1 < 0.0):
                    morphVal2 += morphVal1
                    morphVal1 = 0.0
                if (morphVal2 < 0.0):
                    morphVal1 += morphVal2
                    morphVal2 = 0.0
            morphKnob1.setValue(self.ITexMorphToSlider(morphVal1))
            morphKnob2.setValue(self.ITexMorphToSlider(morphVal2))
            avatar.avatar.setSkinBlend(((knobID - kTexMorphSliderOffset) - 1), morphVal)
            avatar.avatar.setSkinBlend(((morphID1 - kTexMorphSliderOffset) - 1), morphVal1)
            avatar.avatar.setSkinBlend(((morphID2 - kTexMorphSliderOffset) - 1), morphVal2)


    def ISetStandardControls(self):
        if self.dirty:
            ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarResetID)).show()
        else:
            ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarResetID)).hide()
        if PtIsInternalRelease():
            ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarReadID)).show()
            ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarSaveID)).show()
        else:
            ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarReadID)).hide()
            ptGUIControlButton(AvCustGUI.dialog.getControlFromTag(kAvatarSaveID)).hide()
        foundItem = 0
        panelRG = ptGUIControlRadioGroup(AvCustGUI.dialog.getControlFromTag(kPanelsRGID))
        clothing_panel = panelRG.getValue()
        avatar = PtGetLocalAvatar()
        if ((clothing_panel >= 0) and (clothing_panel < len(CLxref))):
            clothing_type = CLxref[clothing_panel][0]
            wornitem = FindWornItem(clothing_type)
            if (type(wornitem) != type(None)):
                descbox = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kClothingDesc))
                descbox.setString(wornitem.description)
                colorbar1 = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName1))
                if (wornitem.colorlabel1 == ''):
                    self.IHideColorPicker(kColor1ClickMap)
                else:
                    self.IShowColorPicker(kColor1ClickMap)
                    colorbar1.setString(wornitem.colorlabel1)
                colorbar2 = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName2))
                if (wornitem.colorlabel2 == ''):
                    self.IHideColorPicker(kColor2ClickMap)
                else:
                    self.IShowColorPicker(kColor2ClickMap)
                    colorbar2.setString(wornitem.colorlabel2)
                if (clothing_type == kFaceClothingItem):
                    skin = avatar.avatar.getTintSkin()
                    self.IDrawPickerThingy(kSkinClickMap, skin)
                    self.IShowColorPicker(kSkinClickMap)
                if (clothing_type == kHairClothingItem):
                    self.IShowColorPicker(kHairClickMap)
                    hair = avatar.avatar.getTintClothingItem(wornitem.name, 1)
                    self.IDrawPickerThingy(kHairClickMap, hair)
                    color2 = avatar.avatar.getTintClothingItem(wornitem.name, 2)
                    self.IDrawPickerThingy(kColor2ClickMap, color2)
                else:
                    color1 = avatar.avatar.getTintClothingItem(wornitem.name)
                    self.IDrawPickerThingy(kColor1ClickMap, color1)
                    if (clothing_type == kFaceClothingItem):
                        color2 = ptColor(1, 1, 1, 1)
                        clothing_group = TheCloset[CLxref[clothing_panel][1]]
                        hasaccessory = 0
                        allowTint = 1
                        for aitem in clothing_group.accessories:
                            if IsWearing(aitem):
                                hasaccessory = 1
                                color2 = avatar.avatar.getTintClothingItem(aitem.name)
                                if (aitem.name in untintableHeadAcc):
                                    allowTint = 0
                        if (hasaccessory & allowTint):
                            self.IDrawPickerThingy(kColor2ClickMap, color2)
                        else:
                            self.IHideColorPicker(kColor2ClickMap)
                    else:
                        color2 = avatar.avatar.getTintClothingItem(wornitem.name, 2)
                        self.IDrawPickerThingy(kColor2ClickMap, color2)
        allMorphsLoaded = 1
        for morphID in range(kNumberOfMorphs):
            knobID = (morphID + kMorphSliderOffset)
            morphKnob = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(knobID))
            morphKnob.show()
            morphVal = 0
            gender = avatar.avatar.getAvatarClothingGroup()
            try:
                if (gender == kFemaleClothingGroup):
                    morphVal = avatar.avatar.getMorph('FFace', morphID)
                else:
                    morphVal = avatar.avatar.getMorph('MFace', morphID)
                morphKnob.setValue(self.IMorphToSlider(morphVal))
            except:
                PtDebugPrint((('Some error occurred while setting morph slider #' + str(morphID)) + ', morphs probably haven\'t loaded yet'))
                morphKnob.setValue(self.IMorphToSlider(0.0))
                allMorphsLoaded = 0
        for texMorphID in range(1, (kNumberOfTexMorphs + 1)):
            knobID = (texMorphID + kTexMorphSliderOffset)
            morphKnob = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(knobID))
            morphKnob.show()
            try:
                if (knobID == kAgeTexMorph):
                    morphVal = avatar.avatar.getSkinBlend(4)
                else:
                    morphVal = avatar.avatar.getSkinBlend((texMorphID - 1))
                morphKnob.setValue(self.ITexMorphToSlider(morphVal))
            except:
                PtDebugPrint((('Some error occurred while setting tex morph slider #' + str(texMorphID)) + ", probably haven't loaded yet"))
                allMorphsLoaded = 0
        self.morphsLoaded = allMorphsLoaded
        if (not self.morphsLoaded):
            PtAtTimeCallback(self.key, 1, kTimerUpdateMorphs)


    def IShowColorPicker(self, id):
        if (id == kColor1ClickMap):
            clickMap = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(kColor1ClickMap))
        elif (id == kColor2ClickMap):
            clickMap = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(kColor2ClickMap))
        elif (id == kHairClickMap):
            clickMap = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(kHairClickMap))
        else:
            clickMap = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(kSkinClickMap))
        clickMap.enable()
        clickMap.show()


    def IHideColorPicker(self, id):
        textBox = None
        if (id == kColor1ClickMap):
            textBox = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName1))
            clickMap = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(kColor1ClickMap))
            texMap = Color1Map.textmap
        elif (id == kColor2ClickMap):
            textBox = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName2))
            clickMap = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(kColor2ClickMap))
            texMap = Color2Map.textmap
        elif (id == kHairClickMap):
            textBox = ptGUIControlTextBox(AvCustGUI.dialog.getControlFromTag(kColorbarName1))
            clickMap = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(kHairClickMap))
            texMap = Color1Map.textmap
        else:
            clickMap = ptGUIControlValue(AvCustGUI.dialog.getControlFromTag(kSkinClickMap))
            texMap = SkinMap.textmap
        clickMap.disable()
        clickMap.hide()
        if (not (textBox == None)):
            textBox.setString('')
        texMap.clearToColor(ptColor(0, 0, 0, 0))
        texMap.flush()


    def IDrawPickerThingy(self, id, color):
        if (id == kColor1ClickMap):
            location = ColorMaterial.map.getColorLoc(color)
        elif (id == kColor2ClickMap):
            location = ColorMaterial.map.getColorLoc(color)
        elif (id == kHairClickMap):
            location = HairMaterial.map.getColorLoc(color)
        elif (id == kSkinClickMap):
            location = SkinMaterial.map.getColorLoc(color)
        else:
            return
        if (location == None):
            location = ptPoint3(0, 0, 0)
        self.IDrawCrosshair(id, location.getX(), location.getY())


    def IDrawCrosshair(self, id, relX, relY):
        if (id == kColor1ClickMap):
            texMap = Color1Map.textmap
            if (not ptGUIControl(AvCustGUI.dialog.getControlFromTag(kColor1ClickMap)).isVisible()):
                return
        elif (id == kColor2ClickMap):
            texMap = Color2Map.textmap
            if (not ptGUIControl(AvCustGUI.dialog.getControlFromTag(kColor2ClickMap)).isVisible()):
                return
        elif (id == kHairClickMap):
            texMap = Color1Map.textmap
            if (not ptGUIControl(AvCustGUI.dialog.getControlFromTag(kHairClickMap)).isVisible()):
                return
        elif (id == kSkinClickMap):
            texMap = SkinMap.textmap
        else:
            return
        width = texMap.getWidth()
        height = texMap.getHeight()
        x = int((relX * width))
        y = int((relY * height))
        texMap.clearToColor(ptColor(0, 0, 0, 0))
        self.IDrawClippedRectangle(texMap, (x - 8), (y - 2), 6, 5, width, height)
        self.IDrawClippedRectangle(texMap, (x + 3), (y - 2), 6, 5, width, height)
        self.IDrawClippedRectangle(texMap, (x - 2), (y - 8), 5, 6, width, height)
        self.IDrawClippedRectangle(texMap, (x - 2), (y + 3), 5, 6, width, height)
        texMap.flush()


    def IDrawClippedRectangle(self, texMap, x, y, width, height, texMapWidth, texMapHeight):
        black = ptColor(0, 0, 0, 1)
        white = ptColor(1, 1, 1, 1)
        x = min(x, (texMapWidth - 1))
        y = min(y, (texMapHeight - 1))
        left = max(x, 0)
        top = max(y, 0)
        right = min((x + width), (texMapWidth - 1))
        bottom = min((y + height), (texMapHeight - 1))
        right = max(right, 0)
        bottom = max(bottom, 0)
        texMap.fillRect(left, top, right, bottom, black)
        texMap.frameRect(left, top, right, bottom, white)


    def IMorphToSlider(self, morph):
        morph = (-(morph))
        slider = (morph + 1.0)
        slider *= 6.0
        return slider


    def ISliderToMorph(self, slider):
        morph = (slider / 6.0)
        morph -= 1.0
        morph = (-(morph))
        return morph


    def ITexMorphToSlider(self, texMorph):
        slider = (texMorph * 12.0)
        return slider


    def ISliderToTexMorph(self, slider):
        texMorph = (slider / 12.0)
        return texMorph



class ClothingItem:


    def __init__(self, clothing, colorType, tintSaturation, inCloset, inClosetColor1, inClosetColor2):
        self.colorType = colorType
        self.tintSaturation1 = tintSaturation
        self.tintSaturation2 = tintSaturation
        self.inCloset = inCloset
        self.inClosetColor1 = inClosetColor1
        self.inClosetColor2 = inClosetColor2
        self.tintValue1 = 1.0
        self.tintValue2 = 1.0
        self.name = ''
        self.type = 0
        self.description = ''
        self.thumbnail = 0
        self.colorlabel1 = 'Color 1'
        self.colorlabel2 = 'Color 2'
        self.accessories = []
        self.meshicon = 0
        self.logofor = ''
        self.groupwith = -1
        self.groupName = ''
        self.accessoryType = -1
        self.wornwith = []
        self.donotwear = 0
        self.coloredAsHair = 0
        self.lastcolorLayer1 = None
        self.lastcolorLayer2 = None
        self.nonStandardItem = 0
        self.singlePlayer = 1
        self.internalOnly = 0
        self.seasonal = 0
        self.seasonTime = []
        self.isClothingSet = 0
        self.clothingSet = ''
        try:
            self.name = clothing[0]
            self.type = clothing[1]
            try:
                if (clothing[2] != ''):
                    self.description = xLocalization.xACA.xClothesXRef[clothing[2]]
            except:
                self.description = clothing[2]
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
                    if (ls == 'colorlabel1'):
                        try:
                            if (rs != ''):
                                self.colorlabel1 = xLocalization.xACA.xClothesXRef[rs]
                            else:
                                self.colorlabel1 = ''
                        except KeyError:
                            self.colorlabel1 = rs
                    elif (ls == 'colorlabel2'):
                        try:
                            if (rs != ''):
                                self.colorlabel2 = xLocalization.xACA.xClothesXRef[rs]
                            else:
                                self.colorlabel2 = ''
                        except KeyError:
                            self.colorlabel2 = rs
                    elif (ls == 'saturationlayer1'):
                        self.tintSaturation1 = string.atof(rs)
                    elif (ls == 'saturationlayer2'):
                        self.tintSaturation2 = string.atof(rs)
                    elif (ls == 'valuelayer1'):
                        self.tintValue1 = string.atof(rs)
                    elif (ls == 'valuelayer2'):
                        self.tintValue2 = string.atof(rs)
                    elif (ls == 'clothingtype'):
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
                            PtDebugPrint(('AvaCusta: ERROR: Unknown ClothingType %s' % rs))
                    elif (ls == 'accessorytype'):
                        self.accessoryType = 0
                    elif (ls == 'accessory'):
                        self.accessoryType = 0
                    elif (ls == 'incloset'):
                        rs = string.lower(rs)
                        if (rs == 'yes'):
                            self.inCloset = 1
                        elif (rs == 'no'):
                            self.inCloset = 0
                        else:
                            PtDebugPrint(('AvaCusta: ERROR: Unknown inCloset type of %s on clothing item %s' % (rs, self.name)))
                    elif (ls == 'inclosetcolor1'):
                        rs = string.lower(rs)
                        if (rs == 'yes'):
                            self.inClosetColor1 = 1
                        elif (rs == 'no'):
                            self.inClosetColor1 = 0
                        else:
                            PtDebugPrint(('AvaCusta: ERROR: Unknown inClosetColor1 type of %s on clothing item %s' % (rs, self.name)))
                    elif (ls == 'inclosetcolor2'):
                        rs = string.lower(rs)
                        if (rs == 'yes'):
                            self.inClosetColor2 = 1
                        elif (rs == 'no'):
                            self.inClosetColor2 = 0
                        else:
                            PtDebugPrint(('AvaCusta: ERROR: Unknown inClosetColor2 type of %s on clothing item %s' % (rs, self.name)))
                    elif (ls == 'nonstandard'):
                        self.nonStandardItem = 1
                    elif (ls == 'internal'):
                        self.internalOnly = 1
                    elif (ls == 'wornwith'):
                        wearlist = rs.split(',')
                        for wearitem in wearlist:
                            self.wornwith.append(wearitem.strip())

                    elif (ls == 'donotwear'):
                        self.donotwear = 1
                    elif (ls == 'coloredashair'):
                        self.coloredAsHair = 1
                    elif (ls == 'groupicon'):
                        self.meshicon = 1
                    elif (ls == 'islogofor'):
                        self.logofor = rs
                    elif (ls == 'groupname'):
                        self.groupName = rs
                        if (not (self.groupName in clothingGroups)):
                            PtDebugPrint((('AvaCusta: Found clothing group ' + self.groupName) + ' adding it to our list of groups'))
                            clothingGroups.append(self.groupName)
                    elif (ls == 'singleplayer'):
                        self.singlePlayer = 1
                    elif (ls == 'needssort'):
                        pass
                    elif (ls == 'seasonal'):
                        self.seasonal = 1
                        try:
                            ranges = rs.split(',')
                            self.seasonTime = []
                            for dateRange in ranges:
                                dates = dateRange.split('-')
                                tempRange = []
                                if (len(dates) == 1):
                                    date = dates[0].split('/')
                                    date = [ int(item) for item in date ]
                                    if (len(date) > 2):
                                        if (date[2] < 2000):
                                            date[2] = (date[2] + 2000)
                                    else:
                                        date.append(0)
                                    tempRange.append(date)
                                else:
                                    startDate = dates[0].split('/')
                                    startDate = [ int(item) for item in startDate ]
                                    if (len(startDate) > 2):
                                        if (startDate[2] < 2000):
                                            startDate[2] = (startDate[2] + 2000)
                                    else:
                                        startDate.append(0)
                                    endDate = dates[1].split('/')
                                    endDate = [ int(item) for item in endDate ]
                                    if (len(endDate) > 2):
                                        if (endDate[2] < 2000):
                                            endDate[2] = (endDate[2] + 2000)
                                    else:
                                        endDate.append(0)
                                    if ((startDate[2] == 0) or (endDate[2] == 0)):
                                        startDate[2] = endDate[2] = 0
                                    if (startDate[0] == 0):
                                        startDate[0] = 1
                                    if (startDate[1] == 0):
                                        startDate[1] = 1
                                    if (endDate[0] == 0):
                                        endDate[0] = 1
                                    if (endDate[1] == 0):
                                        endDate[1] = 1
                                    while (not (startDate == endDate)):
                                        tempRange.append([ date for date in startDate ])
                                        if (startDate[1] >= 31):
                                            if (not (len(tempRange) == ((len(tempRange) / 2) * 2))):
                                                tempRange.append([ date for date in startDate ])
                                            if (startDate[0] >= 12):
                                                startDate[0] = 1
                                                startDate[1] = 1
                                                startDate[2] = (startDate[2] + 1)
                                            else:
                                                startDate[0] = (startDate[0] + 1)
                                                startDate[1] = 1
                                        elif ((startDate[0] == endDate[0]) and (startDate[2] == endDate[2])):
                                            startDate[1] = endDate[1]
                                        else:
                                            startDate[1] = 31
                                        if (startDate[2] > endDate[2]):
                                            startDate[2] = endDate[2]
                                    tempRange.append([ date for date in endDate ])
                                    if (not (len(tempRange) == ((len(tempRange) / 2) * 2))):
                                        tempRange.append([ date for date in endDate ])
                                for i in range(len(tempRange)):
                                    if (not (i == ((i / 2) * 2))):
                                        continue
                                    startMonth = tempRange[i][0]
                                    startDay = tempRange[i][1]
                                    startYear = tempRange[i][2]
                                    if ((i + 1) >= len(tempRange)):
                                        if (i == 0):
                                            monthRange = [startMonth, startMonth]
                                            dayRange = [startDay, startDay]
                                            yearRange = [startYear, startYear]
                                            self.seasonTime.append([monthRange, dayRange, yearRange])
                                    else:
                                        endMonth = tempRange[(i + 1)][0]
                                        endDay = tempRange[(i + 1)][1]
                                        endYear = tempRange[(i + 1)][2]
                                        monthRange = [startMonth, endMonth]
                                        dayRange = [startDay, endDay]
                                        yearRange = [startYear, endYear]
                                        self.seasonTime.append([monthRange, dayRange, yearRange])
                        except:
                            PtDebugPrint(((('AvaCusta: ERROR: Malformed date string ' + rs) + ' on clothing ') + self.name))
                            self.seasonal = 0
                    elif (ls == 'clothingset'):
                        self.isClothingSet = 1
                        self.clothingSet = rs
                        if (not ((self.clothingSet in clothingSets))):
                            PtDebugPrint((('AvaCusta: Found clothing set ' + self.clothingSet) + ' adding it to our list of sets'))
                            clothingSets.append(self.clothingSet)
                    elif (ls == 'free'): pass # keyword used in MOUL
                    elif (ls != ''):
                        PtDebugPrint(('AvaCusta: ERROR: Unknown keyword type (%s) on clothing %s' % (ls, self.name)))
                if ((self.name == '01_MAccNoGlasses') and (not (self.singlePlayer))):
                    self.singlePlayer = 1
                    PtDebugPrint('AvaCusta: ERROR: Hacking 01_MAccNoGlasses to be single player since the material insists it isn\'t')
        except (TypeError, LookupError):
            PtDebugPrint(('AvaCusta: some kind of error on clothing ' + str(clothing)))



class TextureGroup:


    def __init__(self, clothingType, meshName):
        self.clothingType = clothingType
        if (clothingType == kShirtClothingItem):
            self.listboxID = kUpperBodyAccLB
        else:
            self.listboxID = kLwrBodyAccLB
        clothinglist = GetAllWithSameGroup(meshName)
        self.clothingItems = []
        for newitem in clothinglist:
            if newitem.isClothingSet:
                if (newitem.clothingSet in clothingSetContents):
                    hasItem = 0
                    for tempItem in clothingSetContents[newitem.clothingSet]:
                        if (tempItem.name == newitem.name):
                            hasItem = 1
                    if (not hasItem):
                        PtDebugPrint(((('AvaCusta: item ' + newitem.name) + ' added to clothing set ') + newitem.clothingSet))
                        clothingSetContents[newitem.clothingSet].append(newitem)
                else:
                    PtDebugPrint((((('AvaCusta: adding clothing set ' + newitem.clothingSet) + ' and added item ') + newitem.name) + ' to it'))
                    clothingSetContents[newitem.clothingSet] = [newitem]
            if CanShowClothingItem(newitem):
                if newitem.meshicon:
                    if (newitem.groupName in clothingGroupIcons):
                        PtDebugPrint(((((('AvaCusta: icon ' + newitem.name) + ' replaced existing icon ') + clothingGroupIcons[newitem.groupName].name) + ' for group ') + newitem.groupName))
                    else:
                        PtDebugPrint(((('AvaCusta: icon ' + newitem.name) + ' set for group ') + newitem.groupName))
                    clothingGroupIcons[newitem.groupName] = newitem
                elif (newitem.groupName in clothingGroupContents):
                    hasItem = 0
                    for tempItem in clothingGroupContents[newitem.groupName]:
                        if (tempItem.name == newitem.name):
                            hasItem = 1
                            break
                    if (not hasItem):
                        PtDebugPrint(((('AvaCusta: item ' + newitem.name) + ' added to clothing group ') + newitem.groupName))
                        clothingGroupContents[newitem.groupName].append(newitem)
                else:
                    PtDebugPrint((((('AvaCusta: adding clothing group ' + newitem.groupName) + ' and added item ') + newitem.name) + ' to it'))
                    clothingGroupContents[newitem.groupName] = [newitem]
                if (not newitem.meshicon):
                    self.clothingItems.append(newitem)
        sortedList = []
        for item in self.clothingItems[:]:
            if (item.logofor == ''):
                sortedList.append(item)
                self.clothingItems.remove(item)
        while (len(self.clothingItems) > 0):
            startingLen = len(self.clothingItems)
            for item in self.clothingItems[:]:
                for i in range(len(sortedList)):
                    if (item.logofor == sortedList[i].name):
                        sortedList.insert((i + 1), item)
                        self.clothingItems.remove(item)
                        break
            if (startingLen == len(self.clothingItems)):
                for item in self.clothingItems:
                    sortedList.append(item)
                self.clothingItems = []
        self.clothingItems = sortedList


    def __getitem__(self, key):
        return self.clothingItems[key]


    def __getslice__(self, i, j):
        return self.clothingItems[i:j]


    def __len__(self):
        return len(self.clothingItems)


    def type(self):
        return self.clothingType



class ClothingGroup:


    def __init__(self, clothingType, listboxID, numberItems):
        self.clothingType = clothingType
        self.listboxID = listboxID
        self.numberItems = numberItems
        self.accessories = []
        avatar = PtGetLocalAvatar()
        clothinglist = avatar.avatar.getClosetClothingList(clothingType)
        self.clothingItems = []
        for item in clothinglist:
            (ctype, saturation, inCloset, inClosClr1, inClosClr2) = FindSaturationAndCloset(item[0], item[1])
            newitem = ClothingItem(item, ctype, saturation, inCloset, inClosClr1, inClosClr2)
            if newitem.isClothingSet:
                if (newitem.clothingSet in clothingSetContents):
                    hasItem = 0
                    for tempItem in clothingSetContents[newitem.clothingSet]:
                        if (tempItem.name == newitem.name):
                            hasItem = 1
                            break
                    if (not hasItem):
                        PtDebugPrint(((('AvaCusta: item ' + newitem.name) + ' added to clothing set ') + newitem.clothingSet))
                        clothingSetContents[newitem.clothingSet].append(newitem)
                else:
                    PtDebugPrint((((('AvaCusta: adding clothing set ' + newitem.clothingSet) + ' and added item ') + newitem.name) + ' to it'))
                    clothingSetContents[newitem.clothingSet] = [newitem]
            if CanShowClothingItem(newitem):
                if newitem.meshicon:
                    if (newitem.groupName in clothingGroupIcons):
                        PtDebugPrint(((((('AvaCusta: icon ' + newitem.name) + ' replaced existing icon ') + clothingGroupIcons[newitem.groupName].name) + ' for group ') + newitem.groupName))
                    else:
                        PtDebugPrint(((('AvaCusta: icon ' + newitem.name) + ' set for group ') + newitem.groupName))
                    clothingGroupIcons[newitem.groupName] = newitem
                elif (newitem.groupName in clothingGroupContents):
                    hasItem = 0
                    for tempItem in clothingGroupContents[newitem.groupName]:
                        if (tempItem.name == newitem.name):
                            hasItem = 1
                            break
                    if (not hasItem):
                        PtDebugPrint(((('AvaCusta: item ' + newitem.name) + ' added to clothing group ') + newitem.groupName))
                        clothingGroupContents[newitem.groupName].append(newitem)
                else:
                    PtDebugPrint((((('AvaCusta: adding clothing group ' + newitem.groupName) + ' and added item ') + newitem.name) + ' to it'))
                    clothingGroupContents[newitem.groupName] = [newitem]
                if (((listboxID == kUpperBodyOptionsLB) or (listboxID == kLwrBodyOptionsLB)) and (newitem.meshicon and GroupHasClothing(newitem))):
                    self.clothingItems.append(newitem)
                elif (not ((listboxID == kUpperBodyOptionsLB) or (listboxID == kLwrBodyOptionsLB))):
                    self.clothingItems.append(newitem)


    def __getitem__(self, key):
        return self.clothingItems[key]


    def __getslice__(self, i, j):
        return self.clothingItems[i:j]


    def __len__(self):
        return len(self.clothingItems)


    def type(self):
        return self.clothingType



class ClothingCloset:


    def __init__(self):
        self.clothingGroups = {}
        self.textureGroups = {}
        self.nameToGroup = {}
        for xref in CLxref:
            self.clothingGroups[xref[1]] = ClothingGroup(xref[0], xref[1], xref[4])
        avatar = PtGetLocalAvatar()
        acclist = avatar.avatar.getClosetClothingList(kAccessoryClothingItem)
        for accitem in acclist:
            accCI = ClothingItem(accitem, 0, 0.0, 1, 0, 0)
            if accCI.isClothingSet:
                if (accCI.clothingSet in clothingSetContents):
                    hasItem = 0
                    for tempItem in clothingSetContents[accCI.clothingSet]:
                        if (tempItem.name == accCI.name):
                            hasItem = 1
                    if (not hasItem):
                        PtDebugPrint(((('AvaCusta: item ' + accCI.name) + ' added to clothing set ') + accCI.clothingSet))
                        clothingSetContents[accCI.clothingSet].append(accCI)
                else:
                    PtDebugPrint((((('AvaCusta: adding clothing set ' + accCI.clothingSet) + ' and added item ') + accCI.name) + ' to it'))
                    clothingSetContents[accCI.clothingSet] = [accCI]
            if CanShowClothingItem(accCI):
                group = self.findGroup(accCI.groupwith)
                if (type(group) != type(None)):
                    if (not accCI.donotwear):
                        group.accessories.append(accCI)
                    else:
                        group.accessories.insert(0, accCI)
                else:
                    PtDebugPrint(('AvaCusta: no group set for accessory %s' % accCI.name))
        for group in self.clothingGroups.values():
            for clothingItem in group:
                if clothingItem.meshicon:
                    self.textureGroups[clothingItem.groupName] = TextureGroup(clothingItem.type, clothingItem.name)
                    self.nameToGroup[clothingItem.name] = clothingItem.groupName
                    for texItem in self.textureGroups[clothingItem.groupName]:
                        self.nameToGroup[texItem.name] = clothingItem.groupName


    def __getitem__(self, key):
        try:
            return self.clothingGroups[key]
        except LookupError:
            return None


    def __len__(self):
        return len(self.clothingGroups)


    def keys(self):
        return self.clothingGroups.keys()


    def findGroup(self, clothing_type):
        for group in self.clothingGroups.values():
            if (group.clothingType == clothing_type):
                return group
        return None


    def findClothingItem(self, finditem):
        for group in self.clothingGroups.values():
            for idx in range(len(group)):
                if (group[idx].name == finditem.name):
                    return (group, idx, 0)
            for idx in range(len(group.accessories)):
                if (group.accessories[idx].name == finditem.name):
                    return (group, idx, 1)
        return (None, -1, -1)


    def getItemByName(self, itemName):
        for group in self.clothingGroups.values():
            for idx in range(len(group)):
                if (group[idx].name == itemName):
                    return group[idx]
            for idx in range(len(group.accessories)):
                if (group.accessories[idx].name == itemName):
                    return group.accessories[idx]
        try:
            texGroup = self.textureGroups[self.nameToGroup[itemName]]
            for texItem in texGroup:
                if (texItem.name == itemName):
                    return texItem
        except:
            pass
        return None


    def getTextureGroup(self, itemName):
        try:
            texGroup = self.textureGroups[self.nameToGroup[itemName]]
            return texGroup
        except:
            return None



class ScrollingListBox:


    def __init__(self):
        self.offset = 0
        self.selection = 0
        self.columns = 0
        self.rows = 2
        self.clothingList = []
        self.listboxID = 0


    def IShowLeftArrow(self):
        if (self.offset > 0):
            return 1
        else:
            return 0


    def IShowRightArrow(self):
        if (self.offset < (self.columns - 4)):
            return 1
        else:
            return 0


    def SetOffset(self, offset):
        if ((offset >= 0) and (offset <= (self.columns - 4))):
            self.offset = offset


    def IncrementOffset(self):
        self.SetOffset((self.offset + 1))


    def DecrementOffset(self):
        self.SetOffset((self.offset - 1))


    def SelectItem(self, listboxIndex):
        selection = -1
        if ((listboxIndex >= 0) and (listboxIndex < 4)):
            selection = (listboxIndex + self.offset)
        elif ((self.rows == 2) and ((listboxIndex >= 4) and (listboxIndex < 8))):
            if (len(self.clothingList) <= 8):
                selection = (listboxIndex + self.offset)
            else:
                selection = (((listboxIndex + self.offset) - 4) + self.columns)
        if ((selection >= 0) and (selection < len(self.clothingList))):
            self.selection = selection
        PtDebugPrint(((((((('ScrollingListBox::SelectItem(): We just selected: ' + self.clothingList[self.selection].name) + ' listboxIndex=') + str(listboxIndex)) + ' offset=') + str(self.offset)) + ' selection=') + str(self.selection)))


    def SetWhatWearing(self):
        for wornitem in WornList:
            if ((self.listboxID == kUpperBodyOptionsLB) or (self.listboxID == kLwrBodyOptionsLB)):
                for idx in range(len(self.clothingList)):
                    if UsesSameGroup(self.clothingList[idx].name, wornitem.name):
                        self.selection = idx
                        return
                self.selection = -1
            else:
                for idx in range(len(self.clothingList)):
                    if (self.clothingList[idx].name == wornitem.name):
                        self.selection = idx
                        return
                self.selection = -1


    def GetSelectedItem(self):
        return self.clothingList[self.selection]


    def SetClothingList(self, clothingList):
        self.clothingList = clothingList
        if (self.rows == 1):
            self.columns = len(self.clothingList)
        else:
            self.columns = int(round((float(len(self.clothingList)) / 2.0)))
        if (((self.rows == 1) and (len(self.clothingList) <= 4)) or ((self.rows == 2) and (len(self.clothingList) <= 8))):
            self.offset = 0
        elif ((self.offset + 4) >= self.columns):
            self.offset = (self.columns - 4)
        self.selection = 0


    def SetListboxID(self, id):
        if ((id >= kHairOptionsLB) and (id <= kAccessOptionsLB)):
            self.listboxID = id
        elif ((id >= kHairAccLB) and (id <= kAccessAccLB)):
            self.listboxID = id
        if (id == kHeadAccLB):
            self.rows = 1
            self.columns = len(self.clothingList)
        else:
            self.rows = 2
            self.columns = int(round((float(len(self.clothingList)) / 2.0)))


    def GetListboxID(self):
        return self.listboxID


    def UpdateScrollArrows(self):
        if ((self.listboxID >= kHairAccLB) and (self.listboxID <= kAccessAccLB)):
            leftArrow = ptGUIControlButton(AvCustGUI.dialog.getControlFromTag((self.listboxID + kIDBtnLeftAccOffset)))
            rightArrow = ptGUIControlButton(AvCustGUI.dialog.getControlFromTag((self.listboxID + kIDBtnRightAccOffset)))
        else:
            if (self.listboxID == kHeadOptionsLB):
                return
            leftArrow = ptGUIControlButton(AvCustGUI.dialog.getControlFromTag((self.listboxID + kIDBtnLeftOptOffset)))
            rightArrow = ptGUIControlButton(AvCustGUI.dialog.getControlFromTag((self.listboxID + kIDBtnRightOptOffset)))
        if self.IShowLeftArrow():
            leftArrow.show()
        else:
            leftArrow.hide()
        if self.IShowRightArrow():
            rightArrow.show()
        else:
            rightArrow.hide()


    def UpdateListbox(self):
        listbox = ptGUIControlListBox(AvCustGUI.dialog.getControlFromTag(self.listboxID))
        listbox.clearAllElements()
        listbox.hide()
        listbox.disallowNoSelect()
        if ((self.listboxID == kUpperBodyAccLB) or (self.listboxID == kLwrBodyAccLB)):
            if (len(self.clothingList) == 1):
                return
        if ((self.listboxID >= kHairAccLB) and (self.listboxID <= kAccessAccLB)):
            if (len(self.clothingList) == 0):
                return
        listbox.show()
        listbox.enable()
        displayItems = []
        if ((self.rows == 1) and (len(self.clothingList) <= 4)):
            displayItems = self.clothingList
        elif ((self.rows == 2) and (len(self.clothingList) <= 8)):
            displayItems = self.clothingList
        else:
            for i in range(4):
                displayItems.append(self.clothingList[(i + self.offset)])
            if (self.rows == 2):
                for i in range(4):
                    try:
                        displayItems.append(self.clothingList[((i + self.offset) + self.columns)])
                    except:
                        pass
        for item in displayItems:
            if (type(item.thumbnail) != type(0)):
                listbox.addImageInBox(item.thumbnail, kCLBImageX, kCLBImageY, kCLBImageWidth, kCLBImageHeight, 1)
            else:
                listbox.addStringInBox(item.name, kCLBMinWidth, kCLBMinHeight)
        LBIndex = -1
        if (((self.rows == 1) and (len(self.clothingList) <= 4)) or ((self.rows == 2) and (len(self.clothingList) <= 8))):
            LBIndex = self.selection
        elif ((self.selection >= self.offset) and (self.selection <= (self.offset + 3))):
            LBIndex = (self.selection - self.offset)
        elif ((self.rows == 2) and ((self.selection >= (self.offset + self.columns)) and (self.selection <= ((self.offset + self.columns) + 3)))):
            LBIndex = (((self.selection - self.offset) - self.columns) + 4)
        if (LBIndex >= 0):
            listbox.setSelection(LBIndex)


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



