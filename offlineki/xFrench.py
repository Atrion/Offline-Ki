# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaVaultConstants import *
xFolderIDToFolderName = {
    PtVaultStandardNodes.kUserDefinedNode: 'D\xe9fini par l\'utilisateur',
    PtVaultStandardNodes.kInboxFolder: 'Bo\xeete de r\xe9ception',
    PtVaultStandardNodes.kBuddyListFolder: 'Amis',
    PtVaultStandardNodes.kIgnoreListFolder: 'Liste \xe0 ignorer',
    PtVaultStandardNodes.kPeopleIKnowAboutFolder: 'R\xe9cents',
    PtVaultStandardNodes.kChronicleFolder: 'Chronique',
    PtVaultStandardNodes.kAvatarOutfitFolder: 'Armoire',
    PtVaultStandardNodes.kAgeTypeJournalFolder: 'Journaux d\'\xc2ges',
    PtVaultStandardNodes.kSubAgesFolder: 'Sous-\xc2ges',
    PtVaultStandardNodes.kHoodMembersFolder: 'Voisins',
    PtVaultStandardNodes.kAllPlayersFolder: 'Tous les joueurs',
    PtVaultStandardNodes.kAgeMembersFolder: 'Joueurs de l\'\xc2ge',
    PtVaultStandardNodes.kAgeJournalsFolder: 'Dossiers des journaux d\'\xc2ges',
    PtVaultStandardNodes.kCanVisitFolder: 'Visiteurs potentiels',
    PtVaultStandardNodes.kAgeOwnersFolder: 'Propri\xe9taires',
    PtVaultStandardNodes.kPublicAgesFolder: 'Quartiers publics',
    PtVaultStandardNodes.kAgesIOwnFolder: '\xc2ges poss\xe9d\xe9s',
    PtVaultStandardNodes.kAgesICanVisitFolder: '\xc2ges visitables',
    PtVaultStandardNodes.kAvatarClosetFolder: 'Armoire \xe0 avatar'
}
xMayorOfNeighborhood = 'Maire'
xMemberOfNeighborhood = 'Membre'
xNeighborhoodPrivate = 'priv\xe9'
xNeighborhoodPublic = 'public'
xDateTimeFormat = '%d/%m/%y  %H:%M'
xDateFormat = '%d/%m/%y'
xImagerMessage = 'De\xa0: %s\nObjet\xa0: %s\n\n%s'
xHoodWelcome = 'Bienvenue \xe0 %s. Pour plus d\'informations, rendez-vous dans la salle de classe'
xDeleteNeighborhoodBook = '\xcates-vous s\xfbr(e) de vouloir supprimer ce Livre et ainsi perdre votre inscription dans ce quartier ?'
xDeleteBook = '\xcates-vous s\xfbr(e) de vouloir supprimer ce Livre et ainsi annuler votre progression dans cet \xc2ge ?'
xNeighborhood = 'Quartier'
xTranslatedAgeNames = {
    'Ferry Terminal': 'Terminal de ferry',
    'Tokotah Alley': 'All\xe9e Tokotah',
    'Palace Alcove': 'Alc\xf4ve du palais',
    'Library Courtyard': 'Cour de la biblioth\xe8que',
    'Concert Hall Foyer': 'Hall de la salle de concert',
    'Eder Kemo': 'Eder Kemo',
    'Eder Gira': 'Eder Gira',
    'Gahreesen': 'Gahreesen',
    'Kadish': 'Kadish',
    'Nexus': 'Nexus',
    'Neighborhood': 'Quartier',
    'Relto': 'Relto',
    'Teledahn': 'Teledahn',
    'Bevin': 'Bevin',
    'Kirel': 'Kirel',
    'Rezeero Observation': 'D\'ni-Rezeero observation',
    'Rezeero': 'D\'ni-Rezeero',
    'Great Zero': 'D\'ni-Rezeero'
}
xPossesive = 'de'

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
        apostropheLoc = localizedName.rfind("'")
        if (apostropheLoc == -1):
            return localizedName
        if ((apostropheLoc + 3) >= len(localizedName)):
            return localizedName
        if (not (((localizedName[(apostropheLoc + 1)] == 's') and (localizedName[(apostropheLoc + 2)] == ' ')))):
            return localizedName
        userName = localizedName[:apostropheLoc]
        ageName = localizedName[(apostropheLoc + 3):]
        localizedName = ((((ageName + ' ') + xPossesive) + ' ') + userName)
    return localizedName

