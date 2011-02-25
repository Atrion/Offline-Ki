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
import math
FogMode = ptAttribDropDownList(1, 'Fog Mode', ('Linear', 'Exponential', 'Exponential2'))
Dimensions = ptAttribDropDownList(2, 'Compute Dimensions', ('XYZ', 'XY', 'Z'))
FogStyle = ptAttribDropDownList(3, 'Fog Style', ('Linear', 'Radial'))
RefreshRate = ptAttribFloat(4, 'Refresh Rate', 1.0, (0.0, 10.0))
PointA_Obj = ptAttribSceneobject(5, 'Point A Obj')
PointA_RGB = ptAttribString(6, 'Point A: Red,Green,Blue')
PointA_Start = ptAttribInt(7, 'Point A: Start Dist', 0, (-10000, 1000000))
PointA_End = ptAttribInt(8, 'Point A: End Dist', 0, (-10000, 1000000))
PointA_Density = ptAttribInt(9, 'Point A: Density', 0, (0, 10))
PointB_Obj = ptAttribSceneobject(10, 'Point B Obj')
PointB_RGB = ptAttribString(11, 'Point B: Red,Green,Blue')
PointB_Start = ptAttribInt(12, 'Point B: Start Dist', 0, (-10000, 1000000))
PointB_End = ptAttribInt(13, 'Point B: End Dist', 0, (-10000, 1000000))
PointB_Density = ptAttribInt(14, 'Point B: Density', 0, (0, 10))
OnlyInRegion = ptAttribBoolean(15, 'Only Operate In Region?', default=false)
Region = ptAttribActivator(16, 'Region Sensor')
Enabled = 0
class xFogDistTweener(ptMultiModifier,):


    def __init__(self):
        ptMultiModifier.__init__(self)
        self.id = 5347
        version = 1
        self.version = version
        print '__init__xFogDistTweener v.',
        print version
        self.PointA_RGBList = []
        self.PointB_RGBList = []



    def OnFirstUpdate(self):
        self.PointA_RGBList = PointA_RGB.value.split(',')
        self.PointA_RGBList[0] = float(self.PointA_RGBList[0])
        self.PointA_RGBList[1] = float(self.PointA_RGBList[1])
        self.PointA_RGBList[2] = float(self.PointA_RGBList[2])
        self.PointB_RGBList = PointB_RGB.value.split(',')
        self.PointB_RGBList[0] = float(self.PointB_RGBList[0])
        self.PointB_RGBList[1] = float(self.PointB_RGBList[1])
        self.PointB_RGBList[2] = float(self.PointB_RGBList[2])
        print ('xFogDistTweener.OnFirstUpdate: PointA_RGB=(%s,%s,%s), PointB_RGB=(%s,%s,%s)' % (self.PointA_RGBList[0],
         self.PointA_RGBList[1],
         self.PointA_RGBList[2],
         self.PointB_RGBList[0],
         self.PointB_RGBList[1],
         self.PointB_RGBList[2]))
        print ('xFogDistTweener.OnFirstUpdate: PointA_SED=(%s,%s,%s), PointB_SED=(%s,%s,%s)' % (PointA_Start.value,
         PointA_End.value,
         PointA_Density.value,
         PointB_Start.value,
         PointB_End.value,
         PointB_Density.value))
        if (not OnlyInRegion.value):
            PtAtTimeCallback(self.key, 0, 1)



    def OnNotify(self, state, id, events):
        global Enabled
        print ('xFogDistTweener.OnNotify: state=%s id=%d events=' % (state,
         id)),
        print events
        if ((id == Region.id) and (OnlyInRegion.value and (PtFindAvatar(events) == PtGetLocalAvatar()))):
            print 'xFogDistTweener.OnNotify: Region with fog settings triggered'
            if (events[0][1] == 1):
                print 'xFogDistTweener.OnNotify: Entered'
                Enabled = 1
                PtAtTimeCallback(self.key, 0, 1)
            elif (events[0][1] == 0):
                print 'xFogDistTweener.OnNotify: Exited'
                PtClearTimerCallbacks(self.key)
                Enabled = 0



    def OnTimer(self, id):
        if (Enabled or (not OnlyInRegion.value)):
            self.UpdateFog()
            PtAtTimeCallback(self.key, RefreshRate.value, 1)



    def UpdateFog(self):
        TweenPct = self.CalculateDistanceBetweenPoints()
        try:
            self.PointA_RGBList[0]
        except:
            self.PointA_RGBList = PointA_RGB.value.split(',')
            self.PointA_RGBList[0] = float(self.PointA_RGBList[0])
            self.PointA_RGBList[1] = float(self.PointA_RGBList[1])
            self.PointA_RGBList[2] = float(self.PointA_RGBList[2])
            self.PointB_RGBList = PointB_RGB.value.split(',')
            self.PointB_RGBList[0] = float(self.PointB_RGBList[0])
            self.PointB_RGBList[1] = float(self.PointB_RGBList[1])
            self.PointB_RGBList[2] = float(self.PointB_RGBList[2])
        NewR = (self.PointA_RGBList[0] + ((self.PointB_RGBList[0] - self.PointA_RGBList[0]) * TweenPct))
        NewG = (self.PointA_RGBList[1] + ((self.PointB_RGBList[1] - self.PointA_RGBList[1]) * TweenPct))
        NewB = (self.PointA_RGBList[2] + ((self.PointB_RGBList[2] - self.PointA_RGBList[2]) * TweenPct))
        NewS = (PointA_Start.value + ((PointB_Start.value - PointA_Start.value) * TweenPct))
        NewE = (PointA_End.value + ((PointB_End.value - PointA_End.value) * TweenPct))
        NewD = (PointA_Density.value + ((PointB_Density.value - PointA_Density.value) * TweenPct))
        newfogcolor = ptColor(red=NewR, green=NewG, blue=NewB)
        PtFogSetDefColor(newfogcolor)
        if (FogMode.value == 'Linear'):
            PtFogSetDefLinear(NewS, NewE, NewD)
        elif (FogMode.value == 'Exponential'):
            PtFogSetDefExp(NewE, NewD)
        elif (FogMode.value == 'Exponential2'):
            PtFogSetDefExp2(NewE, NewD)
        else:
            print 'xFogDistTweener.UpdateFog: What type of Fog?'



    def CalculateDistanceBetweenPoints(self):
        objAvatar = PtGetLocalAvatar()
        AvatarPos = objAvatar.position()
        PointAPos = PointA_Obj.value.position()
        PointBPos = PointB_Obj.value.position()
        Temp_A = 0
        Temp_B = 0
        Temp_Avatar = 0
        Distance = 0
        if (Dimensions.value == 'XYZ'):
            Temp_A = PointAPos
            Temp_B = PointBPos
            Temp_Avatar = AvatarPos
        elif (Dimensions.value == 'XY'):
            Temp_A = ptPoint3(PointAPos.getX(), PointAPos.getY(), 0)
            Temp_B = ptPoint3(PointBPos.getX(), PointBPos.getY(), 0)
            Temp_Avatar = ptPoint3(AvatarPos.getX(), AvatarPos.getY(), 0)
        elif (Dimensions.value == 'Z'):
            Temp_A = ptPoint3(0, 0, PointAPos.getZ())
            Temp_B = ptPoint3(0, 0, PointBPos.getZ())
            Temp_Avatar = ptPoint3(0, 0, AvatarPos.getZ())
        else:
            print 'xFogDistTweener.CalculateDistanceBetweenPoints: Danger! No Dimension Specified!'
        if (FogStyle.value == 'Linear'):
            P1_X = float(Temp_A.getX())
            P1_Y = float(Temp_A.getY())
            P1_Z = float(Temp_A.getZ())
            P2_X = float(Temp_B.getX())
            P2_Y = float(Temp_B.getY())
            P2_Z = float(Temp_B.getZ())
            A_X = float(Temp_Avatar.getX())
            A_Y = float(Temp_Avatar.getY())
            A_Z = float(Temp_Avatar.getZ())
            Pn_X = (P2_X - P1_X)
            Pn_Y = (P2_Y - P1_Y)
            Pn_Z = (P2_Z - P1_Z)
            Magnitutde_Pn = math.sqrt((((Pn_X * Pn_X) + (Pn_Y * Pn_Y)) + (Pn_Z * Pn_Z)))
            Normalized_PnX = (Pn_X / Magnitutde_Pn)
            Normalized_PnY = (Pn_Y / Magnitutde_Pn)
            Normalized_PnZ = (Pn_Z / Magnitutde_Pn)
            Pm_X = (A_X - P1_X)
            Pm_Y = (A_Y - P1_Y)
            Pm_Z = (A_Z - P1_Z)
            Distance = (((Normalized_PnX * Pm_X) + (Normalized_PnY * Pm_Y)) + (Normalized_PnZ * Pm_Z))
        elif (FogStyle.value == 'Radial'):
            Distance = Temp_A.distance(Temp_Avatar)
        else:
            print 'xFogDistTweener.CalculateDistanceBetweenPoints: Danger! No Fog Style Specified!'
            Distance = 0
        totalDist = Temp_A.distance(Temp_B)
        if (Distance < 0.0):
            Distance = 0.0
        elif (Distance > totalDist):
            Distance = totalDist
        return (Distance / totalDist)


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



