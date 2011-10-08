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
import xSharperJournalGerman
import xClassStructureJournalGerman
import xPregnancyJournalGerman
import xMaturityJournalGerman
import xMarriageJournalGerman
import xKingShomatJournalGerman
import xKingAileshJournalGerman
import xKingNaygenJournalGerman
import xKingAsemlefJournalGerman
import xKingRinerefJournalGerman
import xKingDemathJournalGerman
import xKingMeemenJournalGerman
import xKingKerathJournalGerman
import xYeeshaJournalGerman
import xUruCreditsJournalGerman
import xExp1CreditsJournalGerman
import xExp2CreditsJournalGerman
import xGahreesenInfoJournalGerman
import xShomatStoryJournalGerman
import xKIJournalGerman
import xGZHelpJournalGerman
import xNegilahnJournalGerman
import xPoetry1JournalEnglish
import xKingMararonJournalGerman
import xKingYableshanJournalGerman
import xGrsnWallHelpJournalGerman
import xKingRikoothJournalGerman
import xKingJaronJournalGerman
import xKingLanarenJournalGerman
import xKingAdeshJournalGerman
import xKingEmenJournalGerman
import xKingJiJournalGerman
import xKingLoshemaneshJournalGerman
import xKingIshekJournalGerman
import xKingLemashalJournalGerman
import xKingKedriJournalGerman
import xKingTiamelJournalGerman
import xKingTejaraJournalGerman
import xKingRakeriJournalGerman
import xKingNeedrahJournalGerman
import xKingHinashJournalGerman
import xKingHemelinJournalGerman
import xKingBehnashirenJournalGerman
import xKingGanJournalGerman
import xKingMeertaJournalGerman
import xKingSolathJournalGerman
import xKingAhlsendarJournalGerman
import xKingKoreenJournalGerman
import xKingJakreenJournalGerman
import xKingVeeshaJournalGerman
import xMeertaStoryJournalGerman
import xKedriStoryJournalGerman
import xMeemenStoryJournalGerman
import xSharper2JournalGerman
import xWatsonJournalGerman
import xPhilJournalGerman
import xYeesha2JournalGerman
import xWatcherPubInfoJournalGerman
import xWords1JournalGerman
import xWords2JournalGerman
import xWords3JournalGerman
import xWords4JournalGerman
import xWords5JournalGerman
import xWordsIntroJournalGerman
xPlayerJournalSource = '<cover src=\"xEditableJournalCover*1#0.hsm\"><font size=20 face=Sharper><margin left=62 right=62 top=48><editable>If you can read this, the book isn\'t working right!'
xPlayerJournalTitle = 'G: %s\'s Journal'
xPlayerJournalXScale = 0.90000000000000002
xPlayerJournalYScale = 1.0
xJournalBooks = {
    'Dummy': (1.0, 1.0, xDummyJournalEnglish),
    'Sharper': (1.0, 1.0, xSharperJournalGerman, 'bkNotebook'),
    'ClassStructure': (1.0, 1.0, xClassStructureJournalGerman, 'bkNotebook'),
    'Pregnancy': (1.0, 1.0, xPregnancyJournalGerman, 'bkNotebook'),
    'Maturity': (1.0, 1.0, xMaturityJournalGerman, 'bkNotebook'),
    'Marriage': (1.0, 1.0, xMarriageJournalGerman, 'bkNotebook'),
    'KingShomat': (1.0, 1.0, xKingShomatJournalGerman, 'bkNotebook'),
    'KingAilesh': (1.0, 1.0, xKingAileshJournalGerman, 'bkNotebook'),
    'KingNaygen': (1.0, 1.0, xKingNaygenJournalGerman, 'bkNotebook'),
    'KingAsemlef': (1.0, 1.0, xKingAsemlefJournalGerman, 'bkNotebook'),
    'KingRineref': (1.0, 1.0, xKingRinerefJournalGerman, 'bkNotebook'),
    'KingDemath': (1.0, 1.0, xKingDemathJournalGerman, 'bkNotebook'),
    'KingMeemen': (1.0, 1.0, xKingMeemenJournalGerman, 'bkNotebook'),
    'KingKerath': (1.0, 1.0, xKingKerathJournalGerman, 'bkNotebook'),
    'Yeesha': (1.0, 1.0, xYeeshaJournalGerman),
    'UruCredits': (1.0, 1.0, xUruCreditsJournalGerman),
    'Exp1Credits': (1.0, 1.0, xExp1CreditsJournalGerman),
    'Exp2Credits': (1.0, 1.0, xExp2CreditsJournalGerman),
    'GahreesenInfo': (1.0, 1.0, xGahreesenInfoJournalGerman, 'bkNotebook'),
    'ShomatStory': (1.0, 1.0, xShomatStoryJournalGerman, 'bkNotebook'),
    'KI': (1.0, 1.0, xKIJournalGerman, 'bkNotebook'),
    'GZHelp': (1.0, 1.0, xGZHelpJournalGerman, 'bkNotebook'),
    'Negilahn': (1.0, 1.0, xNegilahnJournalGerman, 'bkNotebook'),
    'Poetry1': (1.0, 0.90000000000000002, xPoetry1JournalEnglish),
    'KingMararon': (1.0, 0.90000000000000002, xKingMararonJournalGerman),
    'KingYableshan': (1.0, 0.90000000000000002, xKingYableshanJournalGerman),
    'GrsnWallHelp': (1.0, 1.0, xGrsnWallHelpJournalGerman),
    'KingRikooth': (1.0, 0.90000000000000002, xKingRikoothJournalGerman),
    'KingJaron': (1.0, 0.90000000000000002, xKingJaronJournalGerman),
    'KingLanaren': (1.0, 0.90000000000000002, xKingLanarenJournalGerman),
    'KingAdesh': (1.0, 1.0, xKingAdeshJournalGerman),
    'KingEmen': (1.0, 0.90000000000000002, xKingEmenJournalGerman),
    'KingJi': (1.0, 0.90000000000000002, xKingJiJournalGerman),
    'KingLoshemanesh': (1.0, 0.90000000000000002, xKingLoshemaneshJournalGerman),
    'KingIshek': (1.0, 1.0, xKingIshekJournalGerman),
    'KingLemashal': (1.0, 0.90000000000000002, xKingLemashalJournalGerman),
    'KingKedri': (1.0, 0.90000000000000002, xKingKedriJournalGerman),
    'KingTiamel': (1.0, 0.90000000000000002, xKingTiamelJournalGerman),
    'KingTejara': (1.0, 0.90000000000000002, xKingTejaraJournalGerman),
    'KingRakeri': (1.0, 0.90000000000000002, xKingRakeriJournalGerman),
    'KingNeedrah': (1.0, 0.90000000000000002, xKingNeedrahJournalGerman),
    'KingHinash': (1.0, 0.90000000000000002, xKingHinashJournalGerman),
    'KingHemelin': (1.0, 0.90000000000000002, xKingHemelinJournalGerman),
    'KingBehnashiren': (1.0, 0.90000000000000002, xKingBehnashirenJournalGerman),
    'KingGan': (1.0, 0.90000000000000002, xKingGanJournalGerman),
    'KingMeerta': (1.0, 0.90000000000000002, xKingMeertaJournalGerman),
    'KingSolath': (1.0, 0.90000000000000002, xKingSolathJournalGerman),
    'KingAhlsendar': (1.0, 0.90000000000000002, xKingAhlsendarJournalGerman),
    'KingKoreen': (1.0, 0.90000000000000002, xKingKoreenJournalGerman),
    'KingJakreen': (1.0, 0.90000000000000002, xKingJakreenJournalGerman),
    'KingVeesha': (1.0, 0.90000000000000002, xKingVeeshaJournalGerman),
    'MeertaStory': (1.0, 1.0, xMeertaStoryJournalGerman, 'bkNotebook'),
    'KedriStory': (1.0, 1.0, xKedriStoryJournalGerman, 'bkNotebook'),
    'MeemenStory': (1.0, 1.0, xMeemenStoryJournalGerman, 'bkNotebook'),
    'Sharper2': (1.0, 1.0, xSharper2JournalGerman, 'bkNotebook'),
    'Watson': (1.0, 0.90000000000000002, xWatsonJournalGerman),
    'Phil': (1.0, 0.90000000000000002, xPhilJournalGerman, 'bkNotebook'),
    'Yeesha2': (1.0, 1.0, xYeesha2JournalGerman),
    'WatcherPubInfo': (1.0, 1.0, xWatcherPubInfoJournalGerman),
    'Words1': (1.0, 1.0, xWords1JournalGerman),
    'Words2': (1.0, 1.0, xWords2JournalGerman),
    'Words3': (1.0, 1.0, xWords3JournalGerman),
    'Words4': (1.0, 1.0, xWords4JournalGerman),
    'Words5': (1.0, 1.0, xWords5JournalGerman),
    'WordsIntro': (1.0, 1.0, xWordsIntroJournalGerman)
}


