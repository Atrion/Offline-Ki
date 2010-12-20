# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
import PlasmaControlKeys
import xLocalization
stationName = ptAttribString(1, 'station name', 'foggy bottom')
linkpointName = ptAttribString(2, 'linkpoint object name', 'foo')
actClick = ptAttribActivator(3, 'Actvtr: click me')
respClick = ptAttribResponder(4, 'Rspndr: sans ki', netForce=1)
respClickGlow = ptAttribResponder(5, 'Rspndr: with ki', netForce=1)

class islmRegisterNexusLink(ptModifier):


    def __init__(self):
        ptModifier.__init__(self)
        self.id = 5019
        version = 2
        self.version = version
        PtDebugPrint(('__init__islmRegisterNexusLink v.%d.2' % version))


# KveerMOUL workaround BEGIN
    def IGetAgeLinkNode(self, ageFilename):
        vault = ptVault()
        folder = vault.getAgesIOwnFolder()
        contents = folder.getChildNodeRefList()
        for content in contents:
            link = content.getChild()
            link = link.upcastToAgeLinkNode()
            if (type(link) != type(None)):
                info = link.getAgeInfo()
            if (not info):
                continue
            ageName = info.getAgeFilename()
            if (ageName == ageFilename):
                return link

        return None
# KveerMOUL workaround END


    def OnNotify(self, state, id, events):
        if (not (state)):
            return
        if (id == actClick.id):
            if (not (PtWasLocallyNotified(self.key))):
                return
            kiLevel = PtDetermineKILevel()
            PtDebugPrint(('islmRegisterNexusLink.OnNotify:\tplayer ki level is %d' % kiLevel))
            if (kiLevel < kNormalKI):
                respClick.run(self.key, events=events)
                return
            respClickGlow.run(self.key, events=events)
            PtDebugPrint(('islmRegisterNexusLink.OnNotify:\tregistering MTStation %s,%s' % (stationName.value, linkpointName.value)))
            vault = ptVault()
# KveerMOUL workaround BEGIN
            if (stationName.value == 'Kveer'):
                ageLink = self.IGetAgeLinkNode('KveerMOUL')
                if (ageLink != None):
                    spoints = ageLink.getSpawnPoints()
                    foundIt = 0
                    for sp in spoints[:]:
                        if sp.getName() == 'LinkInPointKveerDummy' and sp.getTitle() == stationName.value:
                            foundIt = 1
                            break
                    if not foundIt:
                        PtAtTimeCallback(self.key, 4, 1)
                    newSP = ptSpawnPointInfo(stationName.value, 'LinkInPointKveerDummy')
                    ageLink.addSpawnPoint(newSP)
                    ageLink.save()
                return
# KveerMOUL workaround END
            cityLink = vault.getLinkToCity()
            if (type(cityLink) != type(None)):
                if (not (cityLink.hasSpawnPoint(linkpointName.value))):
                    PtAtTimeCallback(self.key, 4, 1)
            vault.registerMTStation(stationName.value, linkpointName.value)


    def OnTimer(self, id):
        PtSendKIMessage(kKILocalChatStatusMsg, xLocalization.xKI.xKIStatusNexusLinkAdded)


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



