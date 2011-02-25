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
fSunrise = ptAttribFloat(1, 'Percent the sun rises', 0.0, (0.0,
 1.0))
fSunset = ptAttribFloat(2, 'Percent the sun sets', 0.5, (0.0,
 1.0))
SDLBatteryCharge = ptAttribString(3, 'SDL: Battery Charge')
SDLBatteryCapacity = ptAttribString(4, 'SDL: Battery Capacity')
SDLBatteryLastUpdated = ptAttribString(5, 'SDL: Battery Last Updated')
SDLPodLights = ptAttribString(6, 'SDL: Pod Lights')
SDLSpeaker01 = ptAttribString(7, 'SDL: Speaker01')
SDLSpeaker02 = ptAttribString(8, 'SDL: Speaker02')
SDLSpeaker03 = ptAttribString(9, 'SDL: Speaker03')
SDLSpeaker04 = ptAttribString(10, 'SDL: Speaker04')
SDLSpotlight01 = ptAttribString(11, 'SDL: Spotlight01')
SDLSpotlight02 = ptAttribString(12, 'SDL: Spotlight02')
SDLSpotlight03 = ptAttribString(13, 'SDL: Spotlight03')
actSpeaker01 = ptAttribActivator(14, 'Act: Speaker01')
actSpeaker02 = ptAttribActivator(15, 'Act: Speaker02')
actSpeaker03 = ptAttribActivator(16, 'Act: Speaker03')
actSpeaker04 = ptAttribActivator(17, 'Act: Speaker04')
actSpotlight01 = ptAttribActivator(18, 'Act: Spotlight01')
actSpotlight02 = ptAttribActivator(19, 'Act: Spotlight02')
actSpotlight03 = ptAttribActivator(20, 'Act: Spotlight03')
actPodLights = ptAttribActivator(21, 'Act: Pod Lights')
behSpeaker01 = ptAttribResponder(22, 'Beh: Speaker01')
behSpeaker02 = ptAttribResponder(23, 'Beh: Speaker02')
behSpeaker03 = ptAttribResponder(24, 'Beh: Speaker03')
behSpeaker04 = ptAttribResponder(25, 'Beh: Speaker04')
behSpotlight01 = ptAttribResponder(26, 'Beh: Spotlight01')
behSpotlight02 = ptAttribResponder(27, 'Beh: Spotlight02')
behSpotlight03 = ptAttribResponder(28, 'Beh: Spotlight03')
behPodLights = ptAttribResponder(29, 'Beh: Pod Lights', ['1',
 '0'])
respSpeaker01 = ptAttribResponder(30, 'Resp: Speaker01', ['1',
 '0'], netForce=1)
respSpeaker02 = ptAttribResponder(31, 'Resp: Speaker02', ['1',
 '0'], netForce=1)
respSpeaker03 = ptAttribResponder(32, 'Resp: Speaker03', ['1',
 '0'], netForce=1)
respSpeaker04 = ptAttribResponder(33, 'Resp: Speaker04', ['1',
 '0'], netForce=1)
respPodLights = ptAttribResponder(37, 'Resp: Pod Lights', ['1',
 '0'], netForce=1)
boolEmergencyPower = ptAttribBoolean(38, 'Emergency Power Only')
respPodLightsTripped = ptAttribResponder(39, 'Resp: Power Tripped', netForce=1)
kTimeIncrement = 10
CurrentTime = 0
Avvie = None
kPowerOnDrain = 6.5999999999999996
kMicrophoneOnDrain = 4.0
kSpotlightOnDrain = 8.0
kSunRechargeRate = 6.5999999999999996
BatteryCharge = 100
BatteryCapacity = 100
kDayLengthInSeconds = 56585
class xPodBattery(ptResponder,):


    def __init__(self):
        ptResponder.__init__(self)
        self.id = 5242
        version = 5
        self.version = version
        print '__init__xPodBattery v.',
        print version



    def OnServerInitComplete(self):
        try:
            ageSDL = PtGetAgeSDL()
        except:
            print 'xPodBattery:\tERROR---Cannot find the Negilahn Age SDL'
            ageSDL[SDLBatteryCharge.value] = (100,)
            ageSDL[SDLBatteryCapacity.value] = (100,)
            ageSDL[SDLBatteryLastUpdated.value] = (0,)
            ageSDL[SDLPodLights.value] = (0,)
            ageSDL[SDLSpeaker01.value] = (0,)
            ageSDL[SDLSpeaker02.value] = (0,)
            ageSDL[SDLSpeaker03.value] = (0,)
            ageSDL[SDLSpeaker04.value] = (0,)
            ageSDL[SDLSpotlight01.value] = (0,)
            ageSDL[SDLSpotlight02.value] = (0,)
            ageSDL[SDLSpotlight03.value] = (0,)
        ageSDL.sendToClients(SDLBatteryCharge.value)
        ageSDL.sendToClients(SDLBatteryCapacity.value)
        ageSDL.sendToClients(SDLPodLights.value)
        ageSDL.sendToClients(SDLSpeaker01.value)
        ageSDL.sendToClients(SDLSpeaker02.value)
        ageSDL.sendToClients(SDLSpeaker03.value)
        ageSDL.sendToClients(SDLSpeaker04.value)
        ageSDL.sendToClients(SDLSpotlight01.value)
        ageSDL.sendToClients(SDLSpotlight02.value)
        ageSDL.sendToClients(SDLSpotlight03.value)
        ageSDL.setFlags(SDLBatteryCharge.value, 1, 1)
        ageSDL.setFlags(SDLBatteryCapacity.value, 1, 1)
        ageSDL.setFlags(SDLPodLights.value, 1, 1)
        ageSDL.setFlags(SDLSpeaker01.value, 1, 1)
        ageSDL.setFlags(SDLSpeaker02.value, 1, 1)
        ageSDL.setFlags(SDLSpeaker03.value, 1, 1)
        ageSDL.setFlags(SDLSpeaker04.value, 1, 1)
        ageSDL.setFlags(SDLSpotlight01.value, 1, 1)
        ageSDL.setFlags(SDLSpotlight02.value, 1, 1)
        ageSDL.setFlags(SDLSpotlight03.value, 1, 1)
        ageSDL.setNotify(self.key, SDLBatteryCharge.value, 0.0)
        ageSDL.setNotify(self.key, SDLBatteryCapacity.value, 0.0)
        ageSDL.setNotify(self.key, SDLPodLights.value, 0.0)
        ageSDL.setNotify(self.key, SDLSpeaker01.value, 0.0)
        ageSDL.setNotify(self.key, SDLSpeaker02.value, 0.0)
        ageSDL.setNotify(self.key, SDLSpeaker03.value, 0.0)
        ageSDL.setNotify(self.key, SDLSpeaker04.value, 0.0)
        ageSDL.setNotify(self.key, SDLSpotlight01.value, 0.0)
        ageSDL.setNotify(self.key, SDLSpotlight02.value, 0.0)
        ageSDL.setNotify(self.key, SDLSpotlight03.value, 0.0)
        AgeTimeOfDayPercent = PtGetAgeTimeOfDayPercent()
        BatteryCharge = ageSDL[SDLBatteryCharge.value][0]
        BatteryCapacity = ageSDL[SDLBatteryCapacity.value][0]
        BatteryLastUpdated = ageSDL[SDLBatteryLastUpdated.value][0]
        if ageSDL[SDLPodLights.value][0]:
            respPodLights.run(self.key, state='1', fastforward=1)
            behPodLights.run(self.key, state='1', fastforward=1)
        if ageSDL[SDLSpeaker01.value][0]:
            respSpeaker01.run(self.key, state='1', fastforward=1)
        if ageSDL[SDLSpeaker02.value][0]:
            respSpeaker02.run(self.key, state='1', fastforward=1)
        if ageSDL[SDLSpeaker03.value][0]:
            respSpeaker03.run(self.key, state='1', fastforward=1)
        if ageSDL[SDLSpeaker04.value][0]:
            respSpeaker04.run(self.key, state='1', fastforward=1)
        print ('xPodBattery: The Pod Battery has %s of a possible %s units.' % (BatteryCharge,
         BatteryCapacity))
        CurrentTime = PtGetDniTime()
        if (len(PtGetPlayerList()) == 0):
            if (BatteryLastUpdated == 0):
                ageSDL[SDLBatteryLastUpdated.value] = (CurrentTime,)
                print 'xPodBattery: This is your first time here. The Battery has never been updated.'
            else:
                self.SimulateDrainDuringVacancy(CurrentTime, BatteryLastUpdated, BatteryCharge)
        PtAtTimeCallback(self.key, kTimeIncrement, 1)



    def SimulateDrainDuringVacancy(self, CurrentTime, BatteryLastUpdated, BatteryCharge):
        TimeSinceUpdate = (CurrentTime - BatteryLastUpdated)
        WholeDaysVacated = int((TimeSinceUpdate / kDayLengthInSeconds))
        FractionalDaysVacated = (TimeSinceUpdate % kDayLengthInSeconds)
        AgeTimeOfDayPercent = PtGetAgeTimeOfDayPercent()
        CurrentAgeTimeOfDay = (AgeTimeOfDayPercent * kDayLengthInSeconds)
        UnoccupiedDaylightSeconds = 0
        print 'xPodBattery.SimulateDrainDuringVacancy:'
        print ('\tCurrentTime: %d' % CurrentTime)
        print ('\tBatteryLastUpdated: %d' % BatteryLastUpdated)
        print ('\tTimeSinceUpdate: %d' % TimeSinceUpdate)
        print ('\tWholeDaysVacated: %d' % WholeDaysVacated)
        print ('\tFractionalDaysVacated: %d' % FractionalDaysVacated)
        print ('\tAgeTimeOfDayPercent: %.2f%%' % (AgeTimeOfDayPercent * 100))
        print ('\tCurrentAgeTimeOfDay: %.2f of %d' % (CurrentAgeTimeOfDay,
         kDayLengthInSeconds))
        if (FractionalDaysVacated > CurrentAgeTimeOfDay):
            TimeOfDayVacated = (kDayLengthInSeconds - (FractionalDaysVacated - CurrentAgeTimeOfDay))
            print '\tThe pod was vacated at a time of day later than it is now.'
            if (TimeOfDayVacated < (kDayLengthInSeconds * fSunset.value)):
                UnoccupiedDaylightSeconds = ((kDayLengthInSeconds * fSunset.value) - (TimeOfDayVacated - CurrentAgeTimeOfDay))
            elif (CurrentAgeTimeOfDay < (kDayLengthInSeconds * fSunset.value)):
                UnoccupiedDaylightSeconds = CurrentAgeTimeOfDay
            else:
                UnoccupiedDaylightSeconds = (kDayLengthInSeconds * fSunset.value)
        elif (FractionalDaysVacated < CurrentAgeTimeOfDay):
            TimeOfDayVacated = (CurrentAgeTimeOfDay - FractionalDaysVacated)
            print '\tThe Pod was vacated at a time of day earlier than it is now.'
            if (TimeOfDayVacated < (kDayLengthInSeconds * fSunset.value)):
                if (CurrentAgeTimeOfDay <= (kDayLengthInSeconds * fSunset.value)):
                    UnoccupiedDaylightSeconds = FractionalDaysVacated
                else:
                    UnoccupiedDaylightSeconds = ((kDayLengthInSeconds * fSunset.value) - TimeOfDayVacated)
        else:
            TimeOfDayVacated = CurrentAgeTimeOfDay
            print '\tThe Pod was vacated at this exact time.'
        UnoccupiedDaylightSeconds += (WholeDaysVacated * kDayLengthInSeconds)
        print ('\tTimeOfDayVacated: %.2f of %d' % (TimeOfDayVacated,
         kDayLengthInSeconds))
        print ('\tUnoccupiedDaylightSeconds: %.2f' % UnoccupiedDaylightSeconds)
        print 'xPodBattery.SimulateDrainDuringVacancy: The following gadgets were left on while the Pod was vacant:'
        self.CalculateCostPerCycle()
        print ('xPodBattery.SimulateDrainDuringVacancy: SimulateDrainDuringVacancy: CostThisCycle: %.4f' % CostThisCycle)
        CumulativeRecharge = ((UnoccupiedDaylightSeconds / 3600.0) * kSunRechargeRate)
        CumulativeDrain = ((TimeSinceUpdate / 10.0) * CostThisCycle)
        print ('\tCumulativeRecharge: %.2f' % CumulativeRecharge)
        print ('\tCumulativeDrain: %.2f' % CumulativeDrain)
        BatteryCharge += (CumulativeRecharge - CumulativeDrain)
        self.UpdateBatteryChargeSDL(BatteryCharge)



    def CalculateCostPerCycle(self):
        global CostThisCycle
        ageSDL = PtGetAgeSDL()
        CostThisCycle = 0
        boolPodLights = ageSDL[SDLPodLights.value][0]
        boolSpeaker01 = ageSDL[SDLSpeaker01.value][0]
        boolSpeaker02 = ageSDL[SDLSpeaker02.value][0]
        boolSpeaker03 = ageSDL[SDLSpeaker03.value][0]
        boolSpeaker04 = ageSDL[SDLSpeaker04.value][0]
        boolSpotlight01 = ageSDL[SDLSpotlight01.value][0]
        boolSpotlight02 = ageSDL[SDLSpotlight02.value][0]
        boolSpotlight03 = ageSDL[SDLSpotlight03.value][0]
        if (boolPodLights and (not boolEmergencyPower.value)):
            print '\tPodLights'
            CostThisCycle += (kPowerOnDrain * (kTimeIncrement / 3600.0))
        if (boolSpeaker01 and (not boolEmergencyPower.value)):
            print '\tSpeaker01'
            CostThisCycle += (kMicrophoneOnDrain * (kTimeIncrement / 3600.0))
        if (boolSpeaker02 and (not boolEmergencyPower.value)):
            print '\tSpeaker02'
            CostThisCycle += (kMicrophoneOnDrain * (kTimeIncrement / 3600.0))
        if (boolSpeaker03 and (not boolEmergencyPower.value)):
            print '\tSpeaker03'
            CostThisCycle += (kMicrophoneOnDrain * (kTimeIncrement / 3600.0))
        if (boolSpeaker04 and (not boolEmergencyPower.value)):
            print '\tSpeaker04'
            CostThisCycle += (kMicrophoneOnDrain * (kTimeIncrement / 3600.0))
        if (boolSpotlight01 and (not boolEmergencyPower.value)):
            print '\tSpotlight01'
            CostThisCycle += (kSpotlightOnDrain * (kTimeIncrement / 3600.0))
        if (boolSpotlight02 and (not boolEmergencyPower.value)):
            print '\tSpotlight02'
            CostThisCycle += (kSpotlightOnDrain * (kTimeIncrement / 3600.0))
        if (boolSpotlight03 and (not boolEmergencyPower.value)):
            print '\tSpotlight03'
            CostThisCycle += (kSpotlightOnDrain * (kTimeIncrement / 3600.0))



    def CalculatePowerDrain(self):
        print 'xPodBattery.CalculatePowerDrain: The following gadgets are currently turned on:'
        self.CalculateCostPerCycle()
        print ('xPodBattery.CalculatePowerDrain: Over the last %s seconds, you drained the battery %.4f units.' % (kTimeIncrement,
         CostThisCycle))
        RechargeFromSun = 0
        ageSDL = PtGetAgeSDL()
        BatteryCharge = ageSDL[SDLBatteryCharge.value][0]
        BatteryCharge -= CostThisCycle
        AgeTimeOfDayPercent = PtGetAgeTimeOfDayPercent()
        if ((AgeTimeOfDayPercent >= fSunrise.value) and (AgeTimeOfDayPercent <= fSunset.value)):
            RechargeFromSun = (kSunRechargeRate * (kTimeIncrement / 3600.0))
            print ('xPodBattery.CalculatePowerDrain: The time is %.1f%% through the daytime, adding %.4f units to the battery.' % (((AgeTimeOfDayPercent * 2) * 100),
             RechargeFromSun))
            BatteryCharge += RechargeFromSun
        if ((CostThisCycle - RechargeFromSun) > 0):
            EstimatedTimeLeft = (BatteryCharge / (CostThisCycle * kTimeIncrement))
            print ("xPodBattery.CalculatePowerDrain: At this rate, you'll run out of power in %.2f minutes." % EstimatedTimeLeft)
        self.UpdateBatteryChargeSDL(BatteryCharge)



    def UpdateBatteryChargeSDL(self, BatteryCharge):
        ageSDL = PtGetAgeSDL()
        if (BatteryCharge <= 0):
            BatteryCharge = 0
            ageSDL[SDLPodLights.value] = (0,)
        elif (BatteryCharge > BatteryCapacity):
            BatteryCharge = BatteryCapacity
        ageSDL[SDLBatteryCharge.value] = (BatteryCharge,)
        print ('xPodBattery.UpdateBatteryChargeSDL: The Pod Battery now has %.4f units.' % BatteryCharge)
        CurrentTime = PtGetDniTime()
        ageSDL[SDLBatteryLastUpdated.value] = (CurrentTime,)



    def OnTimer(self, timer):
        if (timer == 1):
            if self.sceneobject.isLocallyOwned():
                self.CalculatePowerDrain()
            PtAtTimeCallback(self.key, kTimeIncrement, 1)



    def OnNotify(self, state, id, events):
        global Avvie
        ageSDL = PtGetAgeSDL()
        print ('xPodBattery.OnNotify: state=%s id=%d events=' % (state,
         id)),
        print events
        if ((id == actPodLights.id) and state):
            Avvie = PtFindAvatar(events)
            newVal = int((not ageSDL[SDLPodLights.value][0]))
            behPodLights.run(self.key, state=str(newVal), avatar=Avvie)
        elif ((id == actSpeaker01.id) and state):
            Avvie = PtFindAvatar(events)
            behSpeaker01.run(self.key, avatar=Avvie)
        elif ((id == actSpeaker02.id) and state):
            Avvie = PtFindAvatar(events)
            behSpeaker02.run(self.key, avatar=Avvie)
        elif ((id == actSpeaker03.id) and state):
            Avvie = PtFindAvatar(events)
            behSpeaker03.run(self.key, avatar=Avvie)
        elif ((id == actSpeaker04.id) and state):
            Avvie = PtFindAvatar(events)
            behSpeaker04.run(self.key, avatar=Avvie)
        elif ((id == actSpotlight01.id) and state):
            Avvie = PtFindAvatar(events)
            behSpotlight01.run(self.key, avatar=Avvie)
        elif ((id == actSpotlight02.id) and state):
            Avvie = PtFindAvatar(events)
            behSpotlight02.run(self.key, avatar=Avvie)
        elif ((id == actSpotlight03.id) and state):
            Avvie = PtFindAvatar(events)
            behSpotlight03.run(self.key, avatar=Avvie)
        elif self.sceneobject.isLocallyOwned():
            if (id == behPodLights.id):
                newVal = int((not ageSDL[SDLPodLights.value][0]))
                ageSDL[SDLPodLights.value] = (newVal,)
            elif (id == behSpeaker01.id):
                if ageSDL[SDLPodLights.value][0]:
                    newVal = int((not ageSDL[SDLSpeaker01.value][0]))
                    ageSDL[SDLSpeaker01.value] = (newVal,)
            elif (id == behSpeaker02.id):
                if ageSDL[SDLPodLights.value][0]:
                    newVal = int((not ageSDL[SDLSpeaker02.value][0]))
                    ageSDL[SDLSpeaker02.value] = (newVal,)
            elif (id == behSpeaker03.id):
                if ageSDL[SDLPodLights.value][0]:
                    newVal = int((not ageSDL[SDLSpeaker03.value][0]))
                    ageSDL[SDLSpeaker03.value] = (newVal,)
            elif (id == behSpeaker04.id):
                if ageSDL[SDLPodLights.value][0]:
                    newVal = int((not ageSDL[SDLSpeaker04.value][0]))
                    ageSDL[SDLSpeaker04.value] = (newVal,)
            elif (id == behSpotlight01.id):
                if ageSDL[SDLPodLights.value][0]:
                    newVal = int((not ageSDL[SDLSpotlight01.value][0]))
                    ageSDL[SDLSpotlight01.value] = (newVal,)
            elif (id == behSpotlight02.id):
                if ageSDL[SDLPodLights.value][0]:
                    newVal = int((not ageSDL[SDLSpotlight02.value][0]))
                    ageSDL[SDLSpotlight02.value] = (newVal,)
            elif (id == behSpotlight03.id):
                if ageSDL[SDLPodLights.value][0]:
                    newVal = int((not ageSDL[SDLSpotlight03.value][0]))
                    ageSDL[SDLSpotlight03.value] = (newVal,)



    def OnSDLNotify(self, VARname, SDLname, playerID, tag):
        ageSDL = PtGetAgeSDL()
        print ('xPodBattery.OnSDLNotify(): VARname:%s, SDLname:%s, tag:%s, value:%s, playerID:%d' % (VARname,
         SDLname,
         tag,
         ageSDL[VARname][0],
         playerID))
        if self.sceneobject.isLocallyOwned():
            if (VARname == SDLPodLights.value):
                respPodLights.run(self.key, state=str(ageSDL[SDLPodLights.value][0]))
                if (not ageSDL[SDLPodLights.value][0]):
                    print 'xPodBattery.OnSDLNotify(): Tripping all SDLs to negative'
                    respPodLightsTripped.run(self.key)
                    ageSDL[SDLSpeaker01.value] = (0,)
                    ageSDL[SDLSpeaker02.value] = (0,)
                    ageSDL[SDLSpeaker03.value] = (0,)
                    ageSDL[SDLSpeaker04.value] = (0,)
                    ageSDL[SDLSpotlight01.value] = (0,)
                    ageSDL[SDLSpotlight02.value] = (0,)
                    ageSDL[SDLSpotlight03.value] = (0,)
            elif (VARname == SDLSpeaker01.value):
                respSpeaker01.run(self.key, state=str(ageSDL[SDLSpeaker01.value][0]))
            elif (VARname == SDLSpeaker02.value):
                respSpeaker02.run(self.key, state=str(ageSDL[SDLSpeaker02.value][0]))
            elif (VARname == SDLSpeaker03.value):
                respSpeaker03.run(self.key, state=str(ageSDL[SDLSpeaker03.value][0]))
            elif (VARname == SDLSpeaker04.value):
                respSpeaker04.run(self.key, state=str(ageSDL[SDLSpeaker04.value][0]))


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



