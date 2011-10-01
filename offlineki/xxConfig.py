# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2004-2011  The Offline KI contributors                      #
#    See the file AUTHORS for more info about the contributors (including      #
#    contact information)                                                      #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    Please see the file COPYING for the full GPLv3 license, or see            #
#    <http://www.gnu.org/licenses/>                                            #
#                                                                              #
#    Uru exception: In addition, this file may be used in combination with     #
#    (non-GPL) code within the context of Uru.                                 #
#                                                                              #
#==============================================================================#
from Plasma import *

accessLevel = 40 # disabled account
shardIdentifier = ''

# some functions to decide
def isOnline(): return not PtIsSinglePlayerMode()
def isOffline(): return PtIsSinglePlayerMode()
def hasStoryLevel(): return accessLevel <= 10
def hasAdminLevel(): return accessLevel <= 7

# configuration for the dynamic loading of pages
AutoPages = {
    # Drizzle
    'city': ['islmBahroShoutFerry', 'islmBahroShoutLibrary', 'islmBahroShoutPalace', 'islmLakeLightMeter', 'guildhallDustAdditions', 'KadishGalleryDustAdditions'],
    'Neighborhood': 'nb01BahroPedestalShout',
    'Ercana': 'ercaDustAdditions',
    'Personal': 'psnlDustAdditions',
    'AhnySphere02': 'ahny2DustAdditions',
    'Cleft': ['clftDustAdditions', 'clftDustAdditions2'],
    'Descent': 'dsntDustAdditions',
    'Garrison': ['grsnDustAdditions', 'grsnDustAdditions2'],
    'Gira': 'giraDustAdditions',
    'GreatZero': 'grtzDustAdditions',
    'Kadish': 'kdshDustAdditions',
    'Myst': 'mystDustAdditions',
    'Personal02': 'philDustAdditions',
    'Teledahn': 'tldnDustAdditions',
    # Race's additions
    'DescentMystV': 'dsntFootRgns',
    'Direbo': 'drboAdditions',
    'KveerMystV': 'kverFootRgns',
    'MystMystV': 'mystFootRgns',
    'Todelmer': 'tdlmFootRgns',
    'Tahgira': 'thgrFootRgns',
    'Siralehn': 'srlnFootRgns',
    'Laki': 'lakiFootRgns',
    'MarshScene': 'mrshFootRgns',
    'MountainScene': 'mntnFootRgns',
    'Payiferen': 'payiWalkable',
    'Negilahn': 'negiWalkable',
}

CollectMarkersUU = False
InviteAges = [
    'Cleft',
    'Personal',
    'Gira',
    'Garrison',
    'Garden',
    'Teledahn',
    'Kadish',
    'Ercana',
    'Minkata',
    'Jalak'
]
PrivateAges = InviteAges + [
    'AvatarCustomization',
    # 'Nexus', # don't show this age as instanced (it only has an age owner set if you link there with the AdminKI)
    # 'BahroCave', # don't show this age as instanced
    # 'BahroCave02', # don't show this age as instanced
    # 'LiveBahroCaves', # don't show this age as instanced
    # 'DniCityX2Finale', # don't show this age as instanced
 ]
AgeNameReplace = { # some age names or parts of them (for instancing) that are set incorrectly in the linking responders
    'ErcanaCitySilo': "D'ni-Ashem'en",
    'Ercana': "Er'cana",
    'Kveer': "K'veer",
    'BahroCave02': "D'ni-Rudenna"
}
LockedAges = [
    'Sonavio', # age writer (boblishman) requested it
    'Kahntinoy', # age writer (wodan) requested it
    'Fenabarel', # age writer (Rich, wodan) requested it
    'oolbahnneea', # age writer (wodan) requested it
    'Ashream', # age writer (wodan) requested it
    'Adrael', # age write (D'Lanor) requested it
]
