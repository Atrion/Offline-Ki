# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import xEnum
import xRandom
from xPsnlVaultSDL import *
import copy
respTeledahnWedge = ptAttribResponder(1, 'Tldn wedge resp')
respGarrisonWedge = ptAttribResponder(2, 'Grsn wedge resp')
respGardenWedge = ptAttribResponder(3, 'Grdn wedge resp')
respKadishWedge = ptAttribResponder(4, 'Kdsh wedge resp')
soTeledahnPoleCollider = ptAttribSceneobject(5, 'Tldn pole collider')
soGarrisonPoleCollider = ptAttribSceneobject(6, 'Grsn pole collider')
soGardenPoleCollider = ptAttribSceneobject(7, 'Grdn pole collider')
soKadishPoleCollider = ptAttribSceneobject(8, 'Kdsh pole collider')
respTeledahnPoleRemove = ptAttribResponder(9, 'Tldn remove pole resp', ['Remove', 'PutBack'])
respGarrisonPoleRemove = ptAttribResponder(10, 'Grsn remove pole resp', ['Remove', 'PutBack'])
respGardenPoleRemove = ptAttribResponder(11, 'Grdn remove pole resp', ['Remove', 'PutBack'])
respKadishPoleRemove = ptAttribResponder(12, 'Kdsh remove pole resp', ['Remove', 'PutBack'])
respTeledahnJCDisable = ptAttribResponder(13, 'Tldn JC disable resp')
respGarrisonJCDisable = ptAttribResponder(14, 'Grsn JC disable resp')
respGardenJCDisable = ptAttribResponder(15, 'Grdn JC disable resp')
respKadishJCDisable = ptAttribResponder(16, 'Kdsh JC disable resp')
clickTeledahnJC = ptAttribActivator(17, 'Tldn JC clickable')
clickGarrisonJC = ptAttribActivator(18, 'Grsn JC clickable')
clickGardenJC = ptAttribActivator(19, 'Grdn JC clickable')
clickKadishJC = ptAttribActivator(20, 'Kdsh JC clickable')
respTeledahnSolutionSymbols = ptAttribResponder(21, 'Tldn solution symbols', ['0', '1', '2', '3', '4', '5', '6'])
respGarrisonSolutionSymbols = ptAttribResponder(22, 'Grsn solution symbols', ['0', '1', '2', '3', '4', '5', '6'])
respGardenSolutionSymbols = ptAttribResponder(23, 'Grdn solution symbols', ['0', '1', '2', '3', '4', '5', '6'])
respKadishSolutionSymbols = ptAttribResponder(24, 'Kdsh solution symbols', ['0', '1', '2', '3', '4', '5', '6'])
clickTeledahnYS = ptAttribActivator(25, 'Tldn YS clickable')
clickGarrisonYS = ptAttribActivator(26, 'Grsn YS clickable')
clickGardenYS = ptAttribActivator(27, 'Grdn YS clickable')
clickKadishYS = ptAttribActivator(28, 'Kdsh YS clickable')
respTeledahnYS = ptAttribResponder(29, 'Tldn yeesha speech')
respGarrisonYS = ptAttribResponder(30, 'Grsn yeesha speech')
respGardenYS = ptAttribResponder(31, 'Grdn yeesha speech')
respKadishYS = ptAttribResponder(32, 'Kdsh yeesha speech')
respTeledahnJCOneShot = ptAttribResponder(33, 'Tldn JC one shot resp')
respGarrisonJCOneShot = ptAttribResponder(34, 'Grsn JC one shot resp')
respGardenJCOneShot = ptAttribResponder(35, 'Grdn JC one shot resp')
respKadishJCOneShot = ptAttribResponder(36, 'Kdsh JC one shot resp')
respTeledahnYSOneShot = ptAttribResponder(37, 'Tldn YS one shot resp', ['trigger', 'glowstart', 'glowend'])
respGarrisonYSOneShot = ptAttribResponder(38, 'Grsn YS one shot resp', ['trigger', 'glowstart', 'glowend'])
respGardenYSOneShot = ptAttribResponder(39, 'Grdn YS one shot resp', ['trigger', 'glowstart', 'glowend'])
respKadishYSOneShot = ptAttribResponder(40, 'Kdsh YS one shot resp', ['trigger', 'glowstart', 'glowend'])
respSequentialYS = ptAttribResponder(41, 'Sequential yeesha speeches', ['1a', '1b', '2a', '2b', '3a', '3b', '4a', '4b'])
rgnLinkOut = ptAttribActivator(42, 'Link out region')
respLinkOut = ptAttribResponder(43, 'Link out responder', ['starfield', 'cavern'])
respStarCavern = ptAttribResponder(44, 'Starfield/cavern vis', ['StarVis', 'CavernVis'])
respKillSpeeches = ptAttribResponder(45, 'Kill yeesha speeches', ['a', 'age', 'b'])
respBahroScream = ptAttribResponder(46, 'Bahro scream')
rgnCaveJump = ptAttribActivator(47, 'Cave jump region')
kWriteTimestamps = 8

class bhroBahroYeeshaCave(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5315
        self.version = 5
        PtDebugPrint(('__init__bhroBahroYeeshaCave v. %d' % self.version))
        self.ageFrom = ''
        self.AgePlaying = ''
        self.SpeechRespReset = 1
        self.IsStarfield = 1


    def OnFirstUpdate(self):
        PtDebugPrint('DEBUG: bhroBahroYeeshaCave.OnFirstUpdate():\tEverything ok so far')
        xRandom.seed()
        xRandom.setmaxseries(1)
        self.currentYS = 'zz'
        PtSendKIMessage(kDisableYeeshaBook, 0)
        vault = ptVault()
        entry = vault.findChronicleEntry('BahroCave')
        if (type(entry) == type(None)):
            PtDebugPrint('DEBUG: bhroBahroYeeshaCave.OnFirstUpdate: Did not find BahroCave chronicle...creating')
            vault.addChronicleEntry('BahroCave', 0, '0')
        self.varMap = {
            'YeeshaSymbolTouched': 0,
            'SolutionSymbol': 1,
            'YeeshaSpeech': 2
        }
        self.ageDict = {
            'Teledahn': {
                'State': 0,
                'WedgeAnim': respTeledahnWedge,
                'PoleCollider': soTeledahnPoleCollider,
                'JCDisable': respTeledahnJCDisable,
                'JCClickable': clickTeledahnJC,
                'SolutionSymbols': respTeledahnSolutionSymbols,
                'YSClickable': clickTeledahnYS,
                'YeeshaSpeech': respTeledahnYS,
                'PoleRemove': respTeledahnPoleRemove,
                'OneShotYS': respTeledahnYSOneShot,
                'OneShotJC': respTeledahnJCOneShot,
                'ID': 0
            },
            'Garrison': {
                'State': 0,
                'WedgeAnim': respGarrisonWedge,
                'PoleCollider': soGarrisonPoleCollider,
                'JCDisable': respGarrisonJCDisable,
                'JCClickable': clickGarrisonJC,
                'SolutionSymbols': respGarrisonSolutionSymbols,
                'YSClickable': clickGarrisonYS,
                'YeeshaSpeech': respGarrisonYS,
                'PoleRemove': respGarrisonPoleRemove,
                'OneShotYS': respGarrisonYSOneShot,
                'OneShotJC': respGarrisonJCOneShot,
                'ID': 1
            },
            'Garden': {
                'State': 0,
                'WedgeAnim': respGardenWedge,
                'PoleCollider': soGardenPoleCollider,
                'JCDisable': respGardenJCDisable,
                'JCClickable': clickGardenJC,
                'SolutionSymbols': respGardenSolutionSymbols,
                'YSClickable': clickGardenYS,
                'YeeshaSpeech': respGardenYS,
                'PoleRemove': respGardenPoleRemove,
                'OneShotYS': respGardenYSOneShot,
                'OneShotJC': respGardenJCOneShot,
                'ID': 2
            },
            'Kadish': {
                'State': 0,
                'WedgeAnim': respKadishWedge,
                'PoleCollider': soKadishPoleCollider,
                'JCDisable': respKadishJCDisable,
                'JCClickable': clickKadishJC,
                'SolutionSymbols': respKadishSolutionSymbols,
                'YSClickable': clickKadishYS,
                'YeeshaSpeech': respKadishYS,
                'PoleRemove': respKadishPoleRemove,
                'OneShotYS': respKadishYSOneShot,
                'OneShotJC': respKadishJCOneShot,
                'ID': 3
            }
        }


    def OnServerInitComplete(self):
        self.ageFrom = PtGetPrevAgeName()
        if (self.ageFrom == ''):
            self.ageFrom = 'Garrison'
        PtDebugPrint(('DEBUG: bhroBahroYeeshaCave.OnServerInitComplete():\tCame from: %s' % self.ageFrom))
        if (not (self.CheckForSolution())):
            PtDebugPrint('No solution found, attempting to create')
            self.CreateSolution()
        self.UpdatePoleStates()
        self.UpdateToState2()
        autostart = 0
        self.UseYeeshaSpeech = self.GetAgeVariable(self.ageFrom, 'YeeshaSpeech')
        if (int(self.UseYeeshaSpeech) == 0):
            serieslen = self.GetNumYSSet()
            self.UseYeeshaSpeech = (serieslen + 1)
            if (self.GetAutoStartLevel() < self.UseYeeshaSpeech):
                autostart = 1
                self.IncrementAutoStartLevel()
        journeyComplete = 0
        sdl = xPsnlVaultSDL()
        if sdl['CleftVisited'][0]:
            journeyComplete = 1
        starCavernRun = 0
        agelist = ['Teledahn', 'Garrison', 'Garden', 'Kadish']
        for age in agelist:
            currentState = self.ageDict[age]['State']
            PtDebugPrint(('Current state: %d' % currentState))
            if ((age != self.ageFrom) and (currentState < 8)):
                self.ageDict[age]['WedgeAnim'].run(self.key, fastforward=1)
            if ((not (starCavernRun)) and (currentState > 5)):
                respStarCavern.run(self.key, state='CavernVis', fastforward=1)
                starCavernRun = 1
                self.IsStarfield = 0
            if (currentState in (4, 6, 9)):
                tid = (90 + self.ageDict[age]['ID'])
                PtAtTimeCallback(self.key, 0.10000000000000001, tid)
            if ((currentState == 4) or ((currentState > 6) and (not (journeyComplete)))):
                self.ageDict[age]['JCDisable'].run(self.key, fastforward=1)
            val = self.GetAgeVariable(age, 'SolutionSymbol')
            self.ageDict[age]['SolutionSymbols'].run(self.key, state=val, fastforward=1)
        if (not (starCavernRun)):
            respStarCavern.run(self.key, state='StarVis', fastforward=1)
        if autostart:
            PtAtTimeCallback(self.key, 3, 1)


    def OnNotify(self, state, id, events):
        PtDebugPrint(('DEBUG: bhroBahroYeeshaCave.OnNotify():\tid = %d' % id))
        if (not (state)):
            return
        if (id == clickTeledahnJC.id):
            self.JCClickHandle('Teledahn')
        elif (id == clickGarrisonJC.id):
            self.JCClickHandle('Garrison')
        elif (id == clickGardenJC.id):
            self.JCClickHandle('Garden')
        elif (id == clickKadishJC.id):
            self.JCClickHandle('Kadish')
        if (id == clickTeledahnYS.id):
            self.YSClickHandle('Teledahn')
        elif (id == clickGarrisonYS.id):
            self.YSClickHandle('Garrison')
        elif (id == clickGardenYS.id):
            self.YSClickHandle('Garden')
        elif (id == clickKadishYS.id):
            self.YSClickHandle('Kadish')
        elif (id == respTeledahnJCOneShot.id):
            self.PostJCOneShot('Teledahn')
        elif (id == respGarrisonJCOneShot.id):
            self.PostJCOneShot('Garrison')
        elif (id == respGardenJCOneShot.id):
            self.PostJCOneShot('Garden')
        elif (id == respKadishJCOneShot.id):
            self.PostJCOneShot('Kadish')
        elif (id == respTeledahnYSOneShot.id):
            self.PostYSOneShot('Teledahn')
        elif (id == respGarrisonYSOneShot.id):
            self.PostYSOneShot('Garrison')
        elif (id == respGardenYSOneShot.id):
            self.PostYSOneShot('Garden')
        elif (id == respKadishYSOneShot.id):
            self.PostYSOneShot('Kadish')
        elif (id == respTeledahnYS.id):
            self.SpeechRespReset = 1
            self.PlayYeeshaSpeech('Teledahn')
        elif (id == respGarrisonYS.id):
            self.SpeechRespReset = 1
            self.PlayYeeshaSpeech('Garrison')
        elif (id == respGardenYS.id):
            self.SpeechRespReset = 1
            self.PlayYeeshaSpeech('Garden')
        elif (id == respKadishYS.id):
            self.SpeechRespReset = 1
            self.PlayYeeshaSpeech('Kadish')
        elif (id == respSequentialYS.id):
            self.SpeechRespReset = 1
            self.PlayYeeshaSpeech(self.ageFrom)
        elif (id == rgnLinkOut.id):
            self.LinkOut()
        elif (id == respTeledahnPoleRemove.id):
            self.PostPoleRemove('Teledahn')
        elif (id == respGarrisonPoleRemove.id):
            self.PostPoleRemove('Garrison')
        elif (id == respGardenPoleRemove.id):
            self.PostPoleRemove('Garden')
        elif (id == respKadishPoleRemove.id):
            self.PostPoleRemove('Kadish')
        elif (id == rgnCaveJump.id):
            cam = ptCamera()
            cam.undoFirstPerson()
            cam.disableFirstPersonOverride()
            print 'undid first person and disabled override'


    def OnTimer(self, id):
        PtDebugPrint(('DEBUG: bhroBahroYeeshaCave.OnTimer():\tid = %d' % id))
        if (id == 1):
            self.PostYSOneShot(self.ageFrom, 1)
        elif (id == 2):
            cam = ptCamera()
            cam.enableFirstPersonOverride()
        elif (id >= 90):
            for pole in ['Teledahn', 'Garden', 'Garrison', 'Kadish']:
                if (self.ageDict[pole]['ID'] == (id - 90)):
                    self.DisablePole(pole, 1)


    def UpdatePoleStates(self):
        psnlSDL = xPsnlVaultSDL()
        sdllist = psnlSDL.BatchGet(['TeledahnPoleState', 'GardenPoleState', 'GarrisonPoleState', 'KadishPoleState'])
        for var in ['Teledahn', 'Garrison', 'Garden', 'Kadish']:
            self.ageDict[var]['State'] = sdllist[(var + 'PoleState')]


    def SetState(self, age, state):
        if (type(state) == type(0)):
            psnlSDL = xPsnlVaultSDL()
            psnlSDL[(age + 'PoleState')] = (state,)


    def GetAgeNode(self, age):
        vault = ptVault()
        chron = vault.findChronicleEntry('BahroCave')
        ageChronRefList = chron.getChildNodeRefList()
        for ageChron in ageChronRefList:
            ageChild = ageChron.getChild()
            ageChild = ageChild.upcastToChronicleNode()
            if (ageChild.chronicleGetName() == age):
                return ageChild
        return None


    def GetAgeVariable(self, age, variable):
        node = self.GetAgeNode(age)
        if (node != None):
            varlist = node.chronicleGetValue().split(',')
            return varlist[self.varMap[variable]]
        else:
            return None


    def SetAgeVariable(self, age, variable, value):
        node = self.GetAgeNode(age)
        if (node != None):
            varlist = node.chronicleGetValue().split(',')
            while (len(varlist) < len(self.varMap)):
                varlist.append('0')
            varlist[self.varMap[variable]] = str(value)
            varstr = ''
            for var in range((len(varlist) - 1)):
                varstr += (varlist[var] + ',')
            varstr += varlist[-1]
            node.chronicleSetValue(varstr)
            node.save()
        else:
            raise 'Could not find chronicle variable to set'


    def AreListsEquiv(self, list1, list2):
        if ((list1[0] in list2) and (len(list1) == len(list2))):
            list2Copy = copy.copy(list2)
            while (list2Copy[0] != list1[0]):
                list2Copy.append(list2Copy.pop(0))
            for i in range(4):
                if (list2Copy[i] != list1[i]):
                    return false
            return true
        return false


    def CheckForSolution(self):
        var = self.GetAgeVariable('Teledahn', 'SolutionSymbol')
        if (var != None):
            return 1
        else:
            return 0


    def CreateSolution(self):
        solutionlist = [3, 2, 5, 0]
        cleftSolList = [3, 2, 5, 0]
        while self.AreListsEquiv(solutionlist, cleftSolList):
            solutionlist = []
            while (len(solutionlist) < 4):
                newint = xRandom.randint(0, 6)
                if (not ((newint in solutionlist))):
                    solutionlist.append(newint)
        vault = ptVault()
        entry = vault.findChronicleEntry('BahroCave')
        if (entry != None):
            agelist = ['Teledahn', 'Garrison', 'Garden', 'Kadish']
            for v in range(len(agelist)):
                newnode = ptVaultChronicleNode(0)
                newnode.chronicleSetName(agelist[v])
                newnode.chronicleSetValue((('0,' + str(solutionlist[v])) + ',0'))
                entry.addNode(newnode)


    def DisablePole(self, age, fforward = 0):
        self.ageDict[age]['PoleRemove'].run(self.key, state='Remove', fastforward=fforward)
        self.ageDict[age]['PoleCollider'].value.physics.suppress(1)
        if (not fforward):
            self.DoWedge()


    def EnablePole(self, age, fforward = 0):
        self.ageDict[age]['PoleRemove'].run(self.key, state='PutBack', fastforward=fforward)
        self.ageDict[age]['PoleCollider'].value.physics.suppress(0)


    def JCClickHandle(self, age):
        cam = ptCamera()
        cam.undoFirstPerson()
        cam.disableFirstPersonOverride()
        PtAtTimeCallback(self.key, 5, 2)
        avatar = PtGetLocalAvatar()
        self.ageDict[age]['OneShotJC'].run(self.key, avatar=avatar)


    def YSClickHandle(self, age):
        avatar = PtGetLocalAvatar()
        self.ageDict[age]['OneShotYS'].run(self.key, avatar=avatar, state='trigger')


    def PostPoleRemove(self, age):
        self.ageDict[age]['JCClickable'].enable()


    def PostJCOneShot(self, age):
        self.UpdatePoleStates()
        state = self.ageDict[age]['State']
        PtDebugPrint(('Current %s state: %d' % (age, state)))
        self.ageDict[age]['JCClickable'].disable()
        if (state == 2):
            self.DisablePole(age)
            self.SetState(age, 3)
        elif (state == 3):
            self.EnablePole(age)
            self.SetState(age, 2)
        elif (state == 6):
            self.EnablePole(age)
            self.SetState(age, 7)
        elif (state == 7):
            self.DisablePole(age)
            self.SetState(age, 6)
        elif (state == 8):
            polesInPsnl = 1
            for tage in ['Teledahn', 'Garrison', 'Garden', 'Kadish']:
                if (self.ageDict[tage]['State'] == 9):
                    polesInPsnl += 1
            if (polesInPsnl == 1):
                print 'Playing Bahro Cave bahro scream'
                respBahroScream.run(self.key)
            self.DisablePole(age)
            self.SetState(age, 9)
        elif (state == 9):
            self.EnablePole(age)
            self.SetState(age, 8)


    def PostYSOneShot(self, age, autotriggered = 0):
        if (self.AgePlaying != age):
            self.ageDict[age]['OneShotYS'].run(self.key, state='glowstart')
        prevage = self.AgePlaying
        self.AgePlaying = age
        if (self.currentYS != 'zz'):
            PtDebugPrint(('Killing speech %s' % self.currentYS))
            respKillSpeeches.run(self.key, state=self.currentYS)
            self.currentYS = 'zz'
            self.ageDict[prevage]['OneShotYS'].run(self.key, state='glowend')
            if (prevage == age):
                self.AgePlaying = ''
                return
        if ((not (int(self.GetAgeVariable(age, 'YeeshaSymbolTouched')))) and (not (autotriggered))):
            PtDebugPrint('DEBUG: bhroBahroYeeshaCave.PostYSOneShot:\tFirst time touching the symbol')
            self.SetAgeVariable(age, 'YeeshaSymbolTouched', 1)
        self.PlayYeeshaSpeech(age)


    def PlayYeeshaSpeech(self, age):
        if ((not (self.SpeechRespReset)) or (self.AgePlaying == '')):
            return
        if (age != self.AgePlaying):
            age = self.AgePlaying
        speech = self.GetAgeVariable(age, 'YeeshaSpeech')
        if (int(speech) == 0):
            speech = str(self.UseYeeshaSpeech)
        if (self.currentYS == 'a'):
            self.currentYS = 'age'
        elif (self.currentYS == 'age'):
            self.currentYS = 'b'
        elif (self.currentYS == 'b'):
            self.currentYS = 'zz'
            self.AgePlaying = ''
        else:
            self.currentYS = 'a'
        if (self.currentYS == 'age'):
            self.ageDict[age]['YeeshaSpeech'].run(self.key)
            self.SpeechRespReset = 0
        elif (self.currentYS != 'zz'):
            respSequentialYS.run(self.key, state=(speech + self.currentYS))
            self.SpeechRespReset = 0
        else:
            self.ageDict[age]['OneShotYS'].run(self.key, state='glowend')


    def GetNumYSSet(self):
        num = 0
        for age in ['Teledahn', 'Garrison', 'Garden', 'Kadish']:
            if int(self.GetAgeVariable(age, 'YeeshaSpeech')):
                num += 1
        return num


    def LinkOut(self):
        polesInPsnl = 0
        updateAgeList = []
        psnlSDL = xPsnlVaultSDL()
        for age in ['Teledahn', 'Garrison', 'Garden', 'Kadish']:
            agevar = (age + 'PoleState')
            sdlval = psnlSDL[agevar][0]
            if ((sdlval == 4) and (age != self.ageFrom)):
                polesInPsnl += 1
                updateAgeList.append((agevar, (5,)))
            elif ((sdlval == 3) and (age == self.ageFrom)):
                if (int(self.GetAgeVariable(self.ageFrom, 'YeeshaSpeech')) == 0):
                    self.SetAgeVariable(self.ageFrom, 'YeeshaSpeech', self.UseYeeshaSpeech)
        if ((polesInPsnl == 3) and (psnlSDL[(self.ageFrom + 'PoleState')][0] == 3)):
            psnlSDL.BatchSet(updateAgeList)
        if self.IsStarfield:
            respLinkOut.run(self.key, state='starfield')
        else:
            respLinkOut.run(self.key, state='cavern')


    def DoWedge(self):
        psnlSDL = xPsnlVaultSDL()
        if (self.ageFrom == 'Garrison'):
            sdlName = 'psnlBahroWedge01'
        elif (self.ageFrom == 'Garden'):
            sdlName = 'psnlBahroWedge02'
        elif (self.ageFrom == 'Kadish'):
            sdlName = 'psnlBahroWedge03'
        elif (self.ageFrom == 'Teledahn'):
            sdlName = 'psnlBahroWedge04'
        else:
            print "bhroBahroYeeshaCave.DoWedge():  ERROR.  Didn't recognize previous age name, no wedge will be set"
            return
        sdlVal = psnlSDL[sdlName][0]
        if (not sdlVal):
            print ('bhroBahroYeeshaCave.DoWedge():  previous age was %s, turning wedge SDL of %s to On' % (self.ageFrom, sdlName))
            psnlSDL[sdlName] = (1,)


    def SetCurrentState(self, age, state):
        ageSDL = xPsnlVaultSDL()
        ageSDL[(age + 'PoleState')] = (state,)


    def UpdateToState2(self):
        vault = ptVault()
        myAges = vault.getAgesIOwnFolder()
        myAges = myAges.getChildNodeRefList()
        for ageInfo in myAges:
            link = ageInfo.getChild()
            link = link.upcastToAgeLinkNode()
            info = link.getAgeInfo()
            if (not (info)):
                continue
            ageName = info.getAgeFilename()
            spawnPoints = link.getSpawnPoints()
            if (ageName == 'Gira'):
                ageName = 'Garden'
            if ((ageName == 'Teledahn') or ((ageName == 'Garrison') or ((ageName == 'Garden') or (ageName == 'Kadish')))):
                for spawnPoint in spawnPoints:
                    if (spawnPoint.getName() == 'LinkInPointDefault'):
                        if (self.ageDict[ageName]['State'] == 1):
                            self.SetCurrentState(ageName, 2)
                        break
        self.UpdatePoleStates()


    def GetAutoStartLevel(self):
        vault = ptVault()
        bc = vault.findChronicleEntry('BahroCave')
        if (type(bc) != type(None)):
            val = bc.chronicleGetValue()
            if (val == ''):
                return 0
            else:
                return int(val)
        else:
            return 0


    def IncrementAutoStartLevel(self):
        vault = ptVault()
        bc = vault.findChronicleEntry('BahroCave')
        if (type(bc) != type(None)):
            val = bc.chronicleGetValue()
            if (val == ''):
                val = 0
            else:
                val = int(val)
            bc.chronicleSetValue(str((val + 1)))
            bc.save()


    def OnBackdoorMsg(self, target, param):
        if (target == 'kill'):
            respKillSpeeches.run(self.key, state=param)
            self.currentYS = 'b'
        elif (target == 'wedgetoggle'):
            vault = ptVault()
            myAges = vault.getAgesIOwnFolder()
            myAges = myAges.getChildNodeRefList()
            for ageInfo in myAges:
                link = ageInfo.getChild()
                link = link.upcastToAgeLinkNode()
                info = link.getAgeInfo()
                if (not info):
                    continue
                ageName = info.getAgeFilename()
            if (ageName == 'Personal'):
                psnlSDL = xPsnlVaultSDL(1)
            else:
                psnlSDL = xPsnlVaultSDL(0)
            if (param == 'Garrison'):
                sdlName = 'psnlBahroWedge01'
            elif ((param == 'Garden') or (param == 'Gira')):
                param = 'Garden'
                sdlName = 'psnlBahroWedge02'
            elif (param == 'Kadish'):
                sdlName = 'psnlBahroWedge03'
            elif (param == 'Teledahn'):
                sdlName = 'psnlBahroWedge04'
            else:
                print 'bhroBahroYeeshaCave.OnBackdoorMsg():  ERROR.  Incorrect age specified, no wedge will be set'
                return 
            sdlVal = psnlSDL[sdlName][0]
            if sdlVal:
                print ('bhroBahroYeeshaCave.OnBackdoorMsg():  previous age was %s, turning wedge SDL of %s to OFF' % (param,
                 sdlName))
                psnlSDL[sdlName] = (0,)
            else:
                print ('bhroBahroYeeshaCave.OnBackdoorMsg():  previous age was %s, turning wedge SDL of %s to ON' % (param,
                 sdlName))
                psnlSDL[sdlName] = (1,)
        elif (target == 'pole'):
            paramlist = param.split('|')
            if (paramlist[0] == 'restore'):
                for pole in ['Teledahn', 'Garden', 'Garrison', 'Kadish']:
                    self.EnablePole(pole, 0)
            elif (paramlist[0] == 'remove'):
                if ((len(paramlist) > 1) and (paramlist[1] == 'fast')):
                    ff = 1
                else:
                    ff = 0
                print 'using ff:',
                print ff
                for pole in ['Teledahn', 'Garden', 'Garrison', 'Kadish']:
                    self.DisablePole(pole, ff)


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



