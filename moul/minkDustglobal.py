# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#    See the file AUTHORS for more info about the contributors.                #
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

