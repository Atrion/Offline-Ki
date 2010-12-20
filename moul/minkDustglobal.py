# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaTypes import *
minkDayClusterGroups = []
minkNightClusterGroups = []

def minkShowDayClusters(show):
    print 'minkShowDayClusters'
    for clustergroup in minkDayClusterGroups:
        for cluster in clustergroup.value:
            cluster.setVisible(show)





def minkShowNightClusters(show):
    print 'minkShowNightClusters'
    for clustergroup in minkNightClusterGroups:
        for cluster in clustergroup.value:
            cluster.setVisible(show)

