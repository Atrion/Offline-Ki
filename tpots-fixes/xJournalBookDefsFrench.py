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
import xDummyJournalEnglish
import xSharperJournalFrench
import xClassStructureJournalFrench
import xPregnancyJournalFrench
import xMaturityJournalFrench
import xMarriageJournalFrench
import xKingShomatJournalFrench
import xKingAileshJournalFrench
import xKingNaygenJournalFrench
import xKingAsemlefJournalFrench
import xKingRinerefJournalFrench
import xKingDemathJournalFrench
import xKingMeemenJournalFrench
import xKingKerathJournalFrench
import xYeeshaJournalFrench
import xUruCreditsJournalFrench
import xExp1CreditsJournalFrench
import xExp2CreditsJournalFrench
import xGahreesenInfoJournalFrench
import xShomatStoryJournalFrench
import xKIJournalFrench
import xGZHelpJournalFrench
import xNegilahnJournalFrench
import xPoetry1JournalEnglish
import xKingMararonJournalFrench
import xKingYableshanJournalFrench
import xGrsnWallHelpJournalFrench
import xKingRikoothJournalFrench
import xKingJaronJournalFrench
import xKingLanarenJournalFrench
import xKingAdeshJournalFrench
import xKingEmenJournalFrench
import xKingJiJournalFrench
import xKingLoshemaneshJournalFrench
import xKingIshekJournalFrench
import xKingLemashalJournalFrench
import xKingKedriJournalFrench
import xKingTiamelJournalFrench
import xKingTejaraJournalFrench
import xKingRakeriJournalFrench
import xKingNeedrahJournalFrench
import xKingHinashJournalFrench
import xKingHemelinJournalFrench
import xKingBehnashirenJournalFrench
import xKingGanJournalFrench
import xKingMeertaJournalFrench
import xKingSolathJournalFrench
import xKingAhlsendarJournalFrench
import xKingKoreenJournalFrench
import xKingJakreenJournalFrench
import xKingVeeshaJournalFrench
import xMeertaStoryJournalFrench
import xKedriStoryJournalFrench
import xMeemenStoryJournalFrench
import xSharper2JournalFrench
import xWatsonJournalFrench
import xPhilJournalFrench
import xYeesha2JournalFrench
import xWatcherPubInfoJournalFrench
import xWords1JournalFrench
import xWords2JournalFrench
import xWords3JournalFrench
import xWords4JournalFrench
import xWords5JournalFrench
import xWordsIntroJournalFrench
xPlayerJournalSource = '<cover src=\"xEditableJournalCover*1#0.hsm\"><font size=20 face=Sharper><margin left=62 right=62 top=48><editable>If you can read this, the book isn\'t working right!'
xPlayerJournalTitle = 'F: %s\'s Journal'
xPlayerJournalXScale = 0.90000000000000002
xPlayerJournalYScale = 1.0
xJournalBooks = {
    'Dummy': (1.0, 1.0, xDummyJournalEnglish),
    'Sharper': (1.0, 1.0, xSharperJournalFrench, 'bkNotebook'),
    'ClassStructure': (1.0, 1.0, xClassStructureJournalFrench, 'bkNotebook'),
    'Pregnancy': (1.0, 1.0, xPregnancyJournalFrench, 'bkNotebook'),
    'Maturity': (1.0, 1.0, xMaturityJournalFrench, 'bkNotebook'),
    'Marriage': (1.0, 1.0, xMarriageJournalFrench, 'bkNotebook'),
    'KingShomat': (1.0, 1.0, xKingShomatJournalFrench, 'bkNotebook'),
    'KingAilesh': (1.0, 1.0, xKingAileshJournalFrench, 'bkNotebook'),
    'KingNaygen': (1.0, 1.0, xKingNaygenJournalFrench, 'bkNotebook'),
    'KingAsemlef': (1.0, 1.0, xKingAsemlefJournalFrench, 'bkNotebook'),
    'KingRineref': (1.0, 1.0, xKingRinerefJournalFrench, 'bkNotebook'),
    'KingDemath': (1.0, 1.0, xKingDemathJournalFrench, 'bkNotebook'),
    'KingMeemen': (1.0, 1.0, xKingMeemenJournalFrench, 'bkNotebook'),
    'KingKerath': (1.0, 1.0, xKingKerathJournalFrench, 'bkNotebook'),
    'Yeesha': (1.0, 1.0, xYeeshaJournalFrench),
    'UruCredits': (1.0, 1.0, xUruCreditsJournalFrench),
    'Exp1Credits': (1.0, 1.0, xExp1CreditsJournalFrench),
    'Exp2Credits': (1.0, 1.0, xExp2CreditsJournalFrench),
    'GahreesenInfo': (1.0, 1.0, xGahreesenInfoJournalFrench, 'bkNotebook'),
    'ShomatStory': (1.0, 1.0, xShomatStoryJournalFrench, 'bkNotebook'),
    'KI': (1.0, 1.0, xKIJournalFrench, 'bkNotebook'),
    'GZHelp': (1.0, 1.0, xGZHelpJournalFrench, 'bkNotebook'),
    'Negilahn': (1.0, 1.0, xNegilahnJournalFrench, 'bkNotebook'),
    'Poetry1': (1.0, 0.90000000000000002, xPoetry1JournalEnglish),
    'KingMararon': (1.0, 0.90000000000000002, xKingMararonJournalFrench),
    'KingYableshan': (1.0, 0.90000000000000002, xKingYableshanJournalFrench),
    'GrsnWallHelp': (1.0, 1.0, xGrsnWallHelpJournalFrench, 'bkNotebook'),
    'KingRikooth': (1.0, 0.90000000000000002, xKingRikoothJournalFrench),
    'KingJaron': (1.0, 0.90000000000000002, xKingJaronJournalFrench),
    'KingLanaren': (1.0, 0.90000000000000002, xKingLanarenJournalFrench),
    'KingAdesh': (1.0, 1.0, xKingAdeshJournalFrench),
    'KingEmen': (1.0, 0.90000000000000002, xKingEmenJournalFrench),
    'KingJi': (1.0, 0.90000000000000002, xKingJiJournalFrench),
    'KingLoshemanesh': (1.0, 0.90000000000000002, xKingLoshemaneshJournalFrench),
    'KingIshek': (1.0, 1.0, xKingIshekJournalFrench),
    'KingLemashal': (1.0, 0.90000000000000002, xKingLemashalJournalFrench),
    'KingKedri': (1.0, 0.90000000000000002, xKingKedriJournalFrench),
    'KingTiamel': (1.0, 0.90000000000000002, xKingTiamelJournalFrench),
    'KingTejara': (1.0, 0.90000000000000002, xKingTejaraJournalFrench),
    'KingRakeri': (1.0, 0.90000000000000002, xKingRakeriJournalFrench),
    'KingNeedrah': (1.0, 0.90000000000000002, xKingNeedrahJournalFrench),
    'KingHinash': (1.0, 0.90000000000000002, xKingHinashJournalFrench),
    'KingHemelin': (1.0, 0.90000000000000002, xKingHemelinJournalFrench),
    'KingBehnashiren': (1.0, 0.90000000000000002, xKingBehnashirenJournalFrench),
    'KingGan': (1.0, 0.90000000000000002, xKingGanJournalFrench),
    'KingMeerta': (1.0, 0.90000000000000002, xKingMeertaJournalFrench),
    'KingSolath': (1.0, 0.90000000000000002, xKingSolathJournalFrench),
    'KingAhlsendar': (1.0, 0.90000000000000002, xKingAhlsendarJournalFrench),
    'KingKoreen': (1.0, 0.90000000000000002, xKingKoreenJournalFrench),
    'KingJakreen': (1.0, 0.90000000000000002, xKingJakreenJournalFrench),
    'KingVeesha': (1.0, 0.90000000000000002, xKingVeeshaJournalFrench),
    'MeertaStory': (1.0, 1.0, xMeertaStoryJournalFrench, 'bkNotebook'),
    'KedriStory': (1.0, 1.0, xKedriStoryJournalFrench, 'bkNotebook'),
    'MeemenStory': (1.0, 1.0, xMeemenStoryJournalFrench, 'bkNotebook'),
    'Sharper2': (1.0, 1.0, xSharper2JournalFrench, 'bkNotebook'),
    'Watson': (1.0, 0.90000000000000002, xWatsonJournalFrench),
    'Phil': (1.0, 0.90000000000000002, xPhilJournalFrench, 'bkNotebook'),
    'Yeesha2': (1.0, 1.0, xYeesha2JournalFrench),
    'WatcherPubInfo': (1.0, 1.0, xWatcherPubInfoJournalFrench),
    'Words1': (1.0, 1.0, xWords1JournalFrench),
    'Words2': (1.0, 1.0, xWords2JournalFrench),
    'Words3': (1.0, 1.0, xWords3JournalFrench),
    'Words4': (1.0, 1.0, xWords4JournalFrench),
    'Words5': (1.0, 1.0, xWords5JournalFrench),
    'WordsIntro': (1.0, 1.0, xWordsIntroJournalFrench)
}


