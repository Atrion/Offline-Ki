# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaVaultConstants import *
xFolderIDToFolderName = {
    PtVaultStandardNodes.kUserDefinedNode: 'User Defined',
    PtVaultStandardNodes.kInboxFolder: 'Incoming',
    PtVaultStandardNodes.kBuddyListFolder: 'Buddies',
    PtVaultStandardNodes.kIgnoreListFolder: 'Ignore List',
    PtVaultStandardNodes.kPeopleIKnowAboutFolder: 'Recent',
    PtVaultStandardNodes.kChronicleFolder: 'Chronicle',
    PtVaultStandardNodes.kAvatarOutfitFolder: 'Closet',
    PtVaultStandardNodes.kAgeTypeJournalFolder: 'Age Journals',
    PtVaultStandardNodes.kSubAgesFolder: 'Sub Ages',
    PtVaultStandardNodes.kHoodMembersFolder: 'Neighbors',
    PtVaultStandardNodes.kAllPlayersFolder: 'All Players',
    PtVaultStandardNodes.kAgeMembersFolder: 'Age Players',
    PtVaultStandardNodes.kAgeJournalsFolder: 'Folder of Age journals',
    PtVaultStandardNodes.kCanVisitFolder: 'People Who Can Visit',
    PtVaultStandardNodes.kAgeOwnersFolder: 'Owners',
    PtVaultStandardNodes.kPublicAgesFolder: 'Public Neighborhoods',
    PtVaultStandardNodes.kAgesIOwnFolder: 'Ages I Own',
    PtVaultStandardNodes.kAgesICanVisitFolder: 'Ages I Can Visit',
    PtVaultStandardNodes.kAvatarClosetFolder: 'Avatar Closet'
}
xMayorOfNeighborhood = 'Mayor'
xMemberOfNeighborhood = 'Member'
xNeighborhoodPrivate = 'private'
xNeighborhoodPublic = 'public'
xDateTimeFormat = '%m/%d/%y  %H:%M'
xDateFormat = '%m/%d/%y'
xImagerMessage = 'From: %s\nSubject: %s\n\n%s'
xHoodWelcome = 'Welcome to %s For more info go to the classroom'
xDeleteNeighborhoodBook = 'Are you sure you want to delete this book, and lose your membership in this neighborhood?'
xDeleteBook = 'Are you sure you want to delete this book, and lose your progress in the age?'

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
    elif (localizedName == 'Great Zero'):
        localizedName = 'D\'ni-Rezeero'
    elif (not (localizedName.startswith('D\'ni'))):
        pass
    return localizedName

