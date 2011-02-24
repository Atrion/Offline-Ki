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
kYeeshaBookShareID = 0
kYeeshaBookLinkID = 1
kYeeshaPageStartID = 3
YeeshaBookSizeWidth = 0.75
YeeshaBookSizeHeight = 1.0
xYeeshaBookBase = '<font size=10><cover src=\"xYeeshaBookCover*1#0.hsm\"><img src=\"xYeeshaBookBorder*1#0.hsm\" pos=0,0 blend=alpha><img src=\"xYeeshaBookShare_eng*801#0.hsm\" pos=180,375 blend=alpha link=0><pb><img src=\"xYeeshaBookLinkPanel*1#0.hsm\" align=center link=1 blend=alpha><img src=\"xYeeshaBookStampSquare*1#0.hsm\" pos=140,255 resize=no blend=alpha>'
xYeeshaBookNoShare = '<font size=10><cover src=\"xYeeshaBookCover*1#0.hsm\"><img src=\"xYeeshaBookBorder*1#0.hsm\" pos=0,0 blend=alpha><pb><img src=\"xYeeshaBookLinkPanel*1#0.hsm\" align=center link=1 blend=alpha><img src=\"xYeeshaBookStampSquare*1#0.hsm\" pos=140,255 resize=no blend=alpha>'
xYeeshaBookBroke = '<font size=10><cover src=\"xYeeshaBookCover*1#0.hsm\"><img src=\"xYeeshaBookBorder*1#0.hsm\" pos=0,0 blend=alpha><pb><img src=\"xLinkPanelBlackVoid*1#0.hsm\" align=center link=1 blend=alpha><img src=\"xYeeshaBookStampSquare*1#0.hsm\" pos=140,255 resize=no blend=alpha>'
xYeeshaPage1 = ('YeeshaPage1', '<pb><pb><img src=\"xYeeshaPageAlphaSketch01*1#0.hsm\" align=center check=00ff18,00800c,%d link=3>')
xYeeshaPage2 = ('YeeshaPage2', '<pb><pb><img src=\"xYeeshaPageAlphaSketch02*1#0.hsm\" align=center check=00ff18,00800c,%d link=4>')
xYeeshaPage3 = ('YeeshaPage3', '<pb><pb><img src=\"xYeeshaPageAlphaSketch03*1#0.hsm\" align=center check=00ff18,00800c,%d link=5>')
xYeeshaPage4 = ('YeeshaPage4', '<pb><pb><img src=\"xYeeshaPageAlphaSketch04*1#0.hsm\" align=center check=00ff18,00800c,%d link=6>')
xYeeshaPage5 = ('YeeshaPage5', '<pb><pb><img src=\"xYeeshaPageAlphaSketch07*1#0.hsm\" align=center check=00ff18,00800c,%d link=7>')
xYeeshaPage6 = ('YeeshaPage6', '<pb><pb><img src=\"xYeeshaPageAlphaSketch06*1#0.hsm\" align=center check=00ff18,00800c,%d link=8>')
xYeeshaPage7 = ('YeeshaPage7', '<pb><pb><img src=\"xYeeshaPageAlphaSketch05*1#0.hsm\" align=center check=00ff18,00800c,%d link=9>')
xYeeshaPage8 = ('YeeshaPage8', '<pb><pb><img src=\"xYeeshaPageAlphaSketch12*1#0.hsm\" align=center check=00ff18,00800c,%d link=10>')
xYeeshaPage9 = ('YeeshaPage9', '<pb><pb><img src=\"xYeeshaPageAlphaSketch09*1#0.hsm\" align=center check=00ff18,00800c,%d link=11>')
xYeeshaPage10 = ('YeeshaPage10', '<pb><pb><img src=\"xYeeshaPageAlphaSketch10*1#0.hsm\" align=center check=00ff18,00800c,%d link=12>')
xYeeshaPage12 = ('YeeshaPage12', '<pb><pb><img src=\"xYeeshaPageAlphaSketch08*1#0.hsm\" align=center check=00ff18,00800c,%d link=13>')
xYeeshaPage13 = ('YeeshaPage13', '<pb><pb><img src=\"xYeeshaPageAlphaSketch13*1#0.hsm\" align=center check=00ff18,00800c,%d link=14>')
xYeeshaPage14 = ('YeeshaPage14', '<pb><pb><img src=\"xYeeshaPageAlphaSketchFireplace*1#0.hsm\" align=center check=00ff18,00800c,%d link=15>')
xYeeshaPage15 = ('YeeshaPage15', '<pb><pb><img src=\"xYeeshaPageAlphaSketchClock*1#0.hsm\" align=center check=00ff18,00800c,%d link=16>')
xYeeshaPage16 = ('YeeshaPage16', '<pb><pb><img src=\"xYeeshaPageAlphaSketchFiremarbles*1#0.hsm\" align=center check=00ff18,00800c,%d link=17>')
xYeeshaPage17 = ('YeeshaPage17', '<pb><pb><img src=\"xYeeshaPageAlphaSketchLushRelto*1#0.hsm\" align=center check=00ff18,00800c,%d link=18>')
xYeeshaPage18 = ('YeeshaPage18', '<pb><pb><img src=\"xYeeshaPageAlphaSketch15*1#0.hsm\" align=center check=00ff18,00800c,%d link=19>')
xYeeshaPage19 = ('YeeshaPage19', '<pb><pb><img src=\"xYeeshaPageAlphaSketchBirds*1#0.hsm\" align=center check=00ff18,00800c,%d link=20>')
xYeeshaPage21 = ('YeeshaPage21', '<pb><pb><img src=\"xYeeshaPageAlphaSketchLeaf*1#0.hsm\" align=center check=00ff18,00800c,%d link=21>')
xYeeshaPage22 = ('YeeshaPage22', '<pb><pb><img src=\"xYeeshaPageAlphaSketchGrass*1#0.hsm\" align=center check=00ff18,00800c,%d link=22>')
xYeeshaPage23 = ('YeeshaPage23', '<pb><pb><img src=\"xYeeshaPageAlphaSketchErcaPlant*1#0.hsm\" align=center check=00ff18,00800c,%d link=23>')
xYeeshaPage24 = ('YeeshaPage24', '<pb><pb><img src=\"xYeeshaPageAlphaSketchStorm*1#0.hsm\" align=center check=00ff18,00800c,%d link=24>')
xYeeshaPage25 = ('YeeshaPage25', '<pb><pb><img src=\"xYeeshaPageAlphaSketch14*1#0.hsm\" align=center check=00ff18,00800c,%d link=25>')
xYeeshaPage26 = ('YeeshaPage26', '<pb><pb><img src=\"xYeeshaPageAlphaSketchCalendar*1#0.hsm\" align=center check=00ff18,00800c,%d link=26>')
xYeeshaPages = [
    xYeeshaPage1,
    xYeeshaPage2,
    xYeeshaPage3,
    xYeeshaPage4,
    xYeeshaPage5,
    xYeeshaPage6,
    xYeeshaPage7,
    xYeeshaPage8,
    xYeeshaPage9,
    xYeeshaPage10,
    # Page 11 is "Zandi's junk"
    xYeeshaPage12,
    xYeeshaPage13,
    xYeeshaPage14,
    xYeeshaPage15,
    xYeeshaPage16,
    xYeeshaPage17,
    xYeeshaPage18,
    xYeeshaPage19,
    # Page 20 is "second bookcase"
    xYeeshaPage21,
    xYeeshaPage22,
    xYeeshaPage23,
    xYeeshaPage24,
    xYeeshaPage25,
    xYeeshaPage26
]
BookStart1 = '<font size=10>%s'
DRCStampHolder = '%s'
NoDRCStamp = ''
DRCStamp1 = '<img src=\"xDRCBookRubberStamp*1#0.hsm\" '
DRCPos1 = 'pos=125,120 blend=alpha>'
DRCStamp2 = '<img src=\"xDRCBookRubberStamp2*1#0.hsm\" '
DRCPos2 = 'pos=190,60 blend=alpha>'
DRCPos3 = 'pos=220,240 blend=alpha>'
YeeshaStamp = '<img src=\"xYeeshaBookStampVSquish*1#0.hsm\" pos=140,255 resize=no blend=alpha>'
kBookMarkID = 0
JCBookMark = ('<img src=\"xBookJourneyClothBookmark*1#0.hsm\" pos=120,0 resize=yes blend=alpha link=%d><pb><pb>' % kBookMarkID)
SCBookMark = ('<img src=\"xBookSaveClothBookmark*1#0.hsm\" pos=120,0 resize=yes blend=alpha link=%d><pb><pb>' % kBookMarkID)
kShareBookLinkID = 1
NoShare = '<pb>'
ShareHolder = '%s<pb>'
ShareBook = ('<img src=\"xYeeshaBookShare_eng*801#0.hsm\" pos=180,375 blend=alpha link=%d>' % kShareBookLinkID)
BahroShare = ('<img src=\"xBahroShare*1#0.hsm\" pos=0,0 blend=alpha link=%d>' % kShareBookLinkID)
BahroNoShare = ''
LinkStart = '<img src=\"'
TransLinkStart = '<img opacity=0.7 src=\"'
kFirstLinkPanelID = 100
LinkEnd = ('*1#0.hsm\" align=center link=%d blend=alpha>' % kFirstLinkPanelID)
LinkEndPage = '*1#0.hsm\" align=center link=%d blend=alpha>'
LinkEndNoLink = '*1#0.hsm\" align=center blend=alpha>'
MovieLinkStart = '<movie src=\"avi\\'
MovieLinkEnd = ('.bik\" align=center link=%d resize=yes>' % kFirstLinkPanelID)
PageStart = '<pb>'
xAgeLinkingBooks = {
    'Neighborhood': (0, 1.0, 1.0, (DRCStamp2 + DRCPos1), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelBevinDefault') + LinkEnd)),
    'EderKemo': (1, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + ShareHolder) + LinkStart) + 'xLinkPanelGardenDefault') + LinkEnd)),
    'BaronCityOffice': (0, 1.0, 1.0, (DRCStamp2 + DRCPos1), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelBaronCityOffice') + LinkEnd)),
    'tldnUpperShroom': (1, 1.0, 1.0, (DRCStamp1 + DRCPos2), (((((BookStart1 + DRCStampHolder) + ShareHolder) + LinkStart) + 'xLinkPanelUpperShroom') + LinkEnd)),
    'Garrison': (0, 1.0, 1.0, (DRCStamp2 + DRCPos3), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelGarrisonDefault') + LinkEnd)),
    'grsnNexus': (0, 1.0, 1.0, (DRCStamp2 + DRCPos3), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelGarrisonNexus') + LinkEnd)),
    'Nexus': (0, 1.0, 1.0, (DRCStamp2 + DRCPos3), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelNexusDefault') + LinkEnd)),
    'Teledahn': (0, 1.0, 1.0, (DRCStamp2 + DRCPos1), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelTeledahnDefault') + LinkEnd)),
    'grtzGrtZeroLinkRm': 'xLinkPanelGrtZeroLinkRm',
    'islmConcertHallFoyer': 'xLinkPanelConcertHallFoyer',
    'islmDakotahRoof': 'xLinkPanelDokotahRoof',
    'islmDakotahAlley': 'xLinkPanelDakotahAlley',
    'islmFerryTerminal': 'xLinkPanelFerryTerminal',
    'islmLibraryCourtyard': 'xLinkPanelLibraryCourtyard',
    'islmPalaceAlcove': 'xLinkPanelPalaceAlcove',
    'islmPalaceBalcony02': 'xLinkPanelPalaceBalc02',
    'islmPalaceBalcony03': 'xLinkPanelPalaceBalc03',
    'KadishGallery': (0, 1.0, 1.0, (DRCStamp2 + DRCPos1), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelKadishGallery') + LinkEnd)),
    'KadishFromGallery': (1, 1.0, 1.0, (DRCStamp2 + DRCPos1), (((((BookStart1 + DRCStampHolder) + ShareHolder) + LinkStart) + 'xLinkPanelKadishFromGallery') + LinkEnd)),
    'Kadish': (0, 1.0, 1.0, (DRCStamp1 + DRCPos2), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelKadishDefault') + LinkEnd)),
    'kdshGlowRmBalcony': 'xLinkPanelKadishGlowBalc',
    'kverKveer': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelKveer') + LinkEnd)),
    'dsntShaftFall': 'xLinkPanelDescentShaftFall',
    'ercaSilo': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelErcanaSilo') + LinkEnd)),
    'ercaPelletRoom': (0,  1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelErcanaPelletRoom') + LinkEnd)), # sharing the book in Restoration Guild does not work
    'Myst': (0, 1.0, 1.0, (DRCStamp2 + DRCPos1), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelMystLibrary') + LinkEnd)),
    'YeeshaVault': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelYeeshaVault') + LinkEnd)),
    'Gira': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelGiraDefault') + LinkEnd)),
    'GiraFromKemo': (1, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + ShareHolder) + LinkStart) + 'xLinkPanelGiraFromKemo') + LinkEnd)),
    'nb01BevinBalcony01': 'xLinkPanelBevinBalc01',
    'nb01BevinBalcony02': 'xLinkPanelBevinBalc02',
    'grsnPrison': 'xLinkPanelGarrisonPrison',
    'tldnChoppedShroom': 'xLinkPanelTeledahnChopShroom',
    'tldnLagoonDock': 'xLinkPanelTeledahnDock',
    'Garden': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelGardenDefault') + LinkEnd)),
    'Spyroom': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelSpyRoom') + LinkEnd)),
    'Cleft': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelCleftDesert') + LinkEnd)),
    'CleftWithTomahna': (0, 1.0, 1.0, NoDRCStamp, ((((((((BookStart1 + DRCStampHolder) + LinkStart) + 'xLinkPanelTomahnaDesert') + LinkEndPage) + PageStart) + LinkStart) + 'xLinkPanelCleftDesert') + LinkEndPage)),
    'TomahnaFromCleft': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelTomahnaDesert') + LinkEnd)),
    'grsnTeamRmPurple': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelCleftDesert') + LinkEnd)),
    'grsnTeamRmYellow': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelCleftDesert') + LinkEnd)),
    'Ahnonay': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelAhnonayTemple') + LinkEnd)),
    'AhnySphere01': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelAhnonayVortex') + LinkEnd)),
    'AhnonayVortex': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelAhnonayVortex') + LinkEnd)),
    'Ercana': (0, 1.0, 1.0, (DRCStamp2 + DRCPos1), (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelErcanaDefault') + LinkEnd)), # sharing the book in Restoration Guild does not work
    'RestorationGuild': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + NoShare) + LinkStart) + 'xLinkPanelWatchersPub') + LinkEnd)),
    'BahroCaveUpper': 'xLinkPanelBahroCaveUpper',
    'BahroCaveLower': 'xLinkPanelBahroCaveLower',
    'NotPossible': (0, 1.0, 1.0, NoDRCStamp, (((((BookStart1 + DRCStampHolder) + 'You obviously cheated, this link is not possible:') + LinkStart) + 'xLinkPanelBlackVoid') + LinkEndNoLink)),
    'Personal02': (0, 0.75, 1.0, NoDRCStamp, (('<font size=10><cover src=\"xYeeshaBookCover*1#0.hsm\">%s%s<img src=\"xYeeshaBookBorder*1#0.hsm\" pos=0,0 blend=alpha><pb><img src=\"xLinkPanelPhilsRelto*1#0.hsm\" align=center link=' + str(kFirstLinkPanelID)) + ' blend=alpha><img src=\"xYeeshaBookStampSquare*1#0.hsm\" pos=140,255 resize=no blend=alpha>'))
    , # new entries
    'KirelMOUL': (0, 1.0, 1.0, NoDRCStamp, BookStart1 + DRCStampHolder + NoShare +  LinkStart + 'xLinkPanelKirel' + LinkEnd + YeeshaStamp),
    'Great Tree': 'xLinkPanelCityGreatTree',
    'dsntMystV': 'xLinkPanelDescentMystV',
    'KveerMOUL': 'xLinkPanelKveerGreatHall',
    'Negilahn': 'xLinkPanelNegilahnDefault',
    'Dereno': 'xLinkPanelDerenoDefault',
    'Payiferen': 'xLinkPanelPayiferenDefault',
    'Tetsonot': 'xLinkPanelTetsonotDefault',
    'Todelmer': 'xLinkPanelTodelmerPod',
    'Jalak': 'xLinkPanelJalakDefault',
    'Minkata': 'xLinkPanelMinkataDefault',
    'DireboVideo': (0, 1.0, 1.0, NoDRCStamp, BookStart1 + DRCStampHolder + NoShare + MovieLinkStart + 'direboWithAlpha' + MovieLinkEnd),
    'Direbo': 'xLinkPanelDirebo',
    'MystMystV': (0, 1.0, 1.0, NoDRCStamp, BookStart1 + DRCStampHolder + NoShare +  LinkStart + 'xLinkPanelMystIsland' + LinkEnd),
    'MystMystVVideo': (0, 1.0, 1.0, NoDRCStamp, BookStart1 + DRCStampHolder + NoShare + MovieLinkStart + 'mystWithAlpha' + MovieLinkEnd),
    'AhnonayMOUL': (0, 1.0, 1.0, NoDRCStamp, BookStart1 + DRCStampHolder + NoShare +  LinkStart + 'xLinkPanelAhnonayVortex' + LinkEnd + YeeshaStamp),
}
xLinkDestinations = {
    'Neighborhood': ('Neighborhood', 'LinkInPointDefault'),
    'EderKemo': ('Garden', 'LinkInPointDefault'),
    'BaronCityOffice': ('BaronCityOffice', 'LinkInPointDefault'),
    'tldnUpperShroom': ('Teledahn', 'LinkInPointUpperRoom'),
    'Garrison': ('Garrison', 'LinkInPointDefault'),
    'grsnNexus': ('GarrisonNexus', 'LinkInPointGrsnNexus'),
    'Nexus': ('Nexus', 'LinkInPointDefault'),
    'Teledahn': ('Teledahn', 'LinkInPointDefault'),
    'islmDakotahRoof': ('city', 'DakotahRoofPlayerStart'),
    'islmPalaceBalcony02': ('city', 'PalaceBalcony02PlayerStart'),
    'islmPalaceBalcony03': ('city', 'PalaceBalcony03PlayerStart'),
    'KadishGallery': ('city', 'LinkInPointKadishGallery'),
    'KadishFromGallery': ('Kadish', 'LinkInPointFromGallery'),
    'Kadish': ('Kadish', 'LinkInPointDefault'),
    'kdshGlowRmBalcony': ('Kadish', 'LinkInPointGlowRmBalcony'),
    'kverKveer': ('Kveer', 'LinkInPointDefault'),
    'dsntShaftFall': ('Descent', 'LinkInPointShaftFall'),
    'ercaSilo': ('ErcanaCitySilo', 'LinkInPointErcanaSilo'),
    'ercaPelletRoom': ('Ercana', 'LinkInPointPelletRoom'),
    'MystLibrary': ('', ''),
    'YeeshaVault': ('', ''),
    'Gira': ('Gira', 'LinkInPointDefault'),
    'GiraFromKemo': ('Gira', 'LinkInPointFromKemo'),
    'nb01BevinBalcony01': ('Neighborhood', 'LinkInPointBevinBalcony01'),
    'nb01BevinBalcony02': ('Neighborhood', 'LinkInPointBevinBalcony02'),
    'grsnPrison': ('Garrison', 'LinkInPointPrison'),
    'tldnChoppedShroom': ('Teledahn', 'StumpStartPoint'),
    'tldnLagoonDock': ('Teledahn', 'DockStartPoint'),
    'Garden': ('Garden', 'LinkInPointDefault'),
    'Cleft': ('Cleft', 'LinkInPointDefault'),
    'CleftWithTomahna': ('', ''),
    'TomahnaFromCleft': ('', ''),
    'grsnTeamRmPurple': ('Garrison', ''),
    'grsnTeamRmYellow': ('Garrison', ''),
    'Negilahn': ('Negilahn', 'LinkInPointDefault'),
    'Todelmer': ('Todelmer', 'LinkInTdlmKeep'), # changed to match the actual age
    'Ercana': ('Ercana', 'LinkInPointDefault'),
    'Ahnonay': ('Ahnonay', 'LinkInPointDefault'),
    'AhnySphere01': ('AhnySphere01', 'LinkInPointDefault', 'SaveClothPoint1', 'SaveClothPoint2', 'SaveClothPoint3', 'SaveClothPoint4', 'SaveClothPoint5', 'SaveClothPoint6'),
    'AhnySphere02': ('AhnySphere02', 'LinkInPointDefault', 'SaveClothPoint7', 'SaveClothPoint8', 'SaveClothPoint9', 'SaveClothPoint10', 'SaveClothPoint11', 'SaveClothPoint12'),
    'AhnySphere03': ('AhnySphere03', 'LinkInPointDefault', 'SaveClothPoint13', 'SaveClothPoint14', 'SaveClothPoint15', 'SaveClothPoint16', 'SaveClothPoint17', 'SaveClothPoint18'),
    'AhnySphere04': ('AhnySphere04', 'LinkInPointDefault', 'SaveClothPoint19', 'SaveClothPoint20', 'SaveClothPoint21', 'SaveClothPoint22', 'SaveClothPoint23', 'SaveClothPoint24', 'SaveClothPoint25', 'SaveClothPoint26', 'SaveClothPoint27'),
    'BahroCaveUpper': ('BahroCave', 'LinkInPointDefault'),
    'BahroCaveLower': ('BahroCave', 'LinkInPointLower')
}
xLinkingPages = {
    'nb01BevinBalcony01': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelBevinBalc01') + LinkEndPage),
    'nb01BevinBalcony02': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelBevinBalc02') + LinkEndPage),
    'grsnPrison': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelGarrisonPrison') + LinkEndPage),
    'tldnChoppedShroom': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelTeledahnChopShroom') + LinkEndPage),
    'tldnLagoonDock': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelTeledahnDock') + LinkEndPage),
    'kdshGlowRmBalcony': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelKadishGlowBalc') + LinkEndPage),
    'islmPalaceBalcony02': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelPalaceBalc02') + LinkEndPage),
    'islmPalaceBalcony03': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelPalaceBalc03') + LinkEndPage),
    'islmDakotahRoof': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelDokotahRoof') + LinkEndPage),
    'KadishGallery': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelKadishGallery') + LinkEndPage),
    'BaronCityOffice': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelBaronCityOffice') + LinkEndPage),
    'dsntShaftFall': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelDescentShaftFall') + LinkEndPage),
    'BahroCaveUpper': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelBahroCaveUpper') + LinkEndPage),
    'BahroCaveLower': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelBahroCaveLower') + LinkEndPage),
    'grtzGrtZeroLinkRm': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelGrtZeroLinkRm') + LinkEndPage),
    'islmConcertHallFoyer': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelConcertHallFoyer') + LinkEndPage),
    'islmDakotahAlley': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelDakotahAlley') + LinkEndPage),
    'islmFerryTerminal': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelFerryTerminal') + LinkEndPage),
    'islmLibraryCourtyard': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelLibraryCourtyard') + LinkEndPage),
    'islmPalaceAlcove': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelPalaceAlcove') + LinkEndPage),
    'Spyroom': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelSpyRoom') + LinkEndPage),
    'kverKveer': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelKveer') + LinkEndPage),
    'YeeshaVault': ((((PageStart + NoShare) + LinkStart) + 'xLinkPanelYeeshaVault') + LinkEndPage)
    , # new entries
    'Negilahn': PageStart + NoShare + LinkStart + 'xLinkPanelNegilahnDefault' + LinkEndPage,
    'Dereno': PageStart + NoShare + LinkStart + 'xLinkPanelDerenoDefault' + LinkEndPage,
    'Payiferen': PageStart + NoShare + LinkStart + 'xLinkPanelPayiferenDefault' + LinkEndPage,
    'Tetsonot': PageStart + NoShare + LinkStart + 'xLinkPanelTetsonotDefault' + LinkEndPage,
    'Todelmer': PageStart + NoShare + LinkStart + 'xLinkPanelTodelmerPod' + LinkEndPage,
    'Great Tree': PageStart + NoShare + LinkStart + 'xLinkPanelCityGreatTree' + LinkEndPage,
    'dsntMystV': PageStart + NoShare + LinkStart + 'xLinkPanelDescentMystV' + LinkEndPage,
    'KveerMOUL': PageStart + NoShare + LinkStart + 'xLinkPanelKveerGreatHall' + LinkEndPage
}
CityBookLinks = [
    'islmPalaceBalcony02',
    'islmPalaceBalcony03',
    'islmDakotahRoof',
    'KadishGallery',
    'BaronCityOffice',
    'dsntShaftFall',
    'grtzGrtZeroLinkRm',
    # 'islmPalaceAlcove', # prevent links from Kirel to city to show up in Relto
    # 'islmLibraryCourtyard',
    # 'islmConcertHallFoyer',
    # 'islmDakotahAlley',
    'Spyroom',
    'kverKveer'
    , # new entries
    'Great Tree',
    'KveerMOUL',
    'dsntMystV'
]
# new arrays
PodAges = {
    'Negilahn': ['Default'],
    'Dereno': ['Default'],
    'Payiferen': ['Default'],
    'Tetsonot': ['Default'],
    'Todelmer': ['tdlmPod']
}
