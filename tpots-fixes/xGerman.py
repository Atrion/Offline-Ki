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
from PlasmaVaultConstants import *
xFolderIDToFolderName = {
    PtVaultStandardNodes.kUserDefinedNode: 'Benutzerdefiniert',
    PtVaultStandardNodes.kInboxFolder: 'Eingang',
    PtVaultStandardNodes.kBuddyListFolder: 'Freunde',
    PtVaultStandardNodes.kIgnoreListFolder: 'Ignorieren-Liste ',
    PtVaultStandardNodes.kPeopleIKnowAboutFolder: 'Bekannte',
    PtVaultStandardNodes.kChronicleFolder: 'Chronik',
    PtVaultStandardNodes.kAvatarOutfitFolder: 'Schrank',
    PtVaultStandardNodes.kAgeTypeJournalFolder: 'Welten- Journale',
    PtVaultStandardNodes.kSubAgesFolder: 'Unterwelten',
    PtVaultStandardNodes.kHoodMembersFolder: 'Nachbarn',
    PtVaultStandardNodes.kAllPlayersFolder: 'Alle Spieler',
    PtVaultStandardNodes.kAgeMembersFolder: 'Spieler dieser Welt',
    PtVaultStandardNodes.kAgeJournalsFolder: 'Ordner der Welten-Journale',
    PtVaultStandardNodes.kCanVisitFolder: 'Besucher',
    PtVaultStandardNodes.kAgeOwnersFolder: 'Besitzer',
    PtVaultStandardNodes.kPublicAgesFolder: '\xd6ffentliche Nachbarschaften',
    PtVaultStandardNodes.kAgesIOwnFolder: 'Meine Welten',
    PtVaultStandardNodes.kAgesICanVisitFolder: 'Welten, die ich besuchen kann',
    PtVaultStandardNodes.kAvatarClosetFolder: 'Avatar-Schrank'
}
xMayorOfNeighborhood = 'Verwalter'
xMemberOfNeighborhood = 'Mitglied'
xNeighborhoodPrivate = 'Privat'
xNeighborhoodPublic = '\xd6ffentlich'
xDateTimeFormat = '%d/%m/%y  %H:%M'
xDateFormat = '%d/%m/%y'
xImagerMessage = 'Von: %s\nBetreff: %s\n\n%s'
xHoodWelcome = 'Willkommen in %s - Weitere Infos erhalten Sie im Klassenraum'
xDeleteNeighborhoodBook = 'Wollen Sie das Buch wirklich l\xf6schen? Dabei geht Ihr Mitgliedschaft in dieser Gemeinde verloren.'
xDeleteBook = 'Wollen Sie das Buch wirklich l\xf6schen? Dabei geht Ihr Fortschritt in dieser Welt verloren.'
xNeighborhood = 'Gemeinde'
xTranslatedAgeNames = {
    'Ferry Terminal': 'F\xe4hren-Terminal',
    'Tokotah Alley': 'Tokotah-Stra\xdfe',
    'Palace Alcove': 'Palast-Alkove',
    'Library Courtyard': 'Bibliothekshof',
    'Concert Hall Foyer': 'Konzerthallen-Foyer',
    'Eder Kemo': 'Eder Kemo',
    'Eder Gira': 'Eder Gira',
    'Gahreesen': 'Gahreesen',
    'Kadish': 'Kadish',
    'Nexus': 'Nexus',
    'Neighborhood': 'Gemeinde',
    'Relto': 'Relto',
    'Teledahn': 'Teledahn',
    'Bevin': 'Bevin',
    'Kirel': 'Kirel',
    'Rezeero Observation': 'D\'ni-Rezeero Beobachtung',
    'Rezeero': 'D\'ni-Rezeero',
    'Great Zero': 'D\'ni-Rezeero'
}
xPossesive = 's'

def LocalizeAgeName(displayName):
    localizedName = displayName.strip()
    if (localizedName == 'D\'ni-Rudenna'):
        try:
            sdl = xPsnlVaultSDL()
            if ((sdl['TeledahnPoleState'][0] > 5) or ((sdl['KadishPoleState'][0] > 5) or ((sdl['GardenPoleState'][0] > 5) or (sdl['GarrisonPoleState'][0] > 5)))):
                localizedName = 'D\'ni-Rudenna'
            else:
                localizedName = '???'
        except:
            localizedName = '???'
    elif (localizedName == 'Ae\'gura'):
        localizedName = 'D\'ni-Ae\'gura'
    elif (localizedName == 'GreatZero'):
        localizedName = 'D\'ni-Rezeero'
    elif (not (localizedName.startswith('D\'ni'))):
        if (localizedName[(len(localizedName) - 12):] == 'Neighborhood'):
            localizedName = (localizedName[:(len(localizedName) - 12)] + xNeighborhood)
            return localizedName
        try:
            localizedName = xTranslatedAgeNames[localizedName]
            return localizedName
        except:
            pass
        apostropheLoc = localizedName.rfind('\'')
        if (apostropheLoc == -1):
            return localizedName
        if ((apostropheLoc + 3) >= len(localizedName)):
            return localizedName
        if (not (((localizedName[(apostropheLoc + 1)] == 's') and (localizedName[(apostropheLoc + 2)] == ' ')))):
            return localizedName
        userName = localizedName[:apostropheLoc]
        ageName = localizedName[(apostropheLoc + 3):]
        localizedName = userName + xPossesive + ' ' + ageName
    return localizedName

