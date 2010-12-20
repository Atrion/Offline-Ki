# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
import xLinkMgr

def dustlink(agename, spawnpoint):
    xLinkMgr.LinkToAge(agename, spawnpoint)


def fakelink(agename, spawnpoint):
    print ('fakelink to %s in %s' % (spawnpoint, agename))
    avatar = PtGetLocalAvatar()
    sp = PtFindSceneobject(spawnpoint, agename)
    PtFakeLinkAvatarToObject(avatar.getKey(), sp.getKey())

