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
import Plasma
import xLocalization
import xInvite
xChatExtendedChat = {
    xLocalization.xKI.xSitCmd: Plasma.PtAvatarSitOnGround,
    #xLocalization.xKI.xAfkCmd: Plasma.PtAvatarEnterAFK,
    #xLocalization.xKI.xInviteCmd: xInvite.CreateInvitation,
    #xLocalization.xKI.xUninviteCmd: xInvite.DeleteInvitation,
    #xLocalization.xKI.xAcceptCmd: xInvite.AcceptInvitation,
    #xLocalization.xKI.xShowInvitesCmd: xInvite.ShowInvitations
}
xChatEmoteXlate = {
    xLocalization.xKI.xWaveCmd: ('Wave', xLocalization.xKI.xWaveString),
    xLocalization.xKI.xSneezeCmd: ('Sneeze', xLocalization.xKI.xSneezeString),
    xLocalization.xKI.xClapCmd: ('Clap', xLocalization.xKI.xClapString),
    xLocalization.xKI.xLaughCmd: ('Laugh', xLocalization.xKI.xLaughString),
    xLocalization.xKI.xLOLCmd: ('Laugh', xLocalization.xKI.xLOLString),
    xLocalization.xKI.xROTFLCmd: ('Laugh', xLocalization.xKI.xROTFLString),
    xLocalization.xKI.xDanceCmd: ('Dance', xLocalization.xKI.xDanceString),
    xLocalization.xKI.xYesCmd: ('Agree', xLocalization.xKI.xYesString),
    xLocalization.xKI.xNoCmd: ('ShakeHead', xLocalization.xKI.xNoString),
    xLocalization.xKI.xYawnCmd: ('Yawn', xLocalization.xKI.xYawnString),
    xLocalization.xKI.xCheerCmd: ('Cheer', xLocalization.xKI.xCheerString),
    xLocalization.xKI.xThanksCmd: ('Thank', xLocalization.xKI.xThanksString),
    xLocalization.xKI.xThxCmd: ('Thank', xLocalization.xKI.xThxString),
    xLocalization.xKI.xCryCmd: ('Cry', xLocalization.xKI.xCryString),
    xLocalization.xKI.xCriesCmd: ('Cry', xLocalization.xKI.xCriesString),
    xLocalization.xKI.xDontKnowCmd: ('Shrug', xLocalization.xKI.xDontKnowString),
    xLocalization.xKI.xShrugCmd: ('Shrug', xLocalization.xKI.xShrugString),
    xLocalization.xKI.xDunnoCmd: ('Shrug', xLocalization.xKI.xDunnoString),
    xLocalization.xKI.xPointCmd: ('Point', xLocalization.xKI.xPointString)
    , # MOUL emotes
    "amazed": ("Amazed", "%s is amazed!"),
    "askquestion": ("AskQuestion", "%s wants to ask a question..."),
    "beckonbig": ("BeckonBig", "%s beckons you"),
    "beckonsmall": ("BeckonSmall", "%s beckons you"),
    "blowkiss": ("BlowKiss", "%s blows you a kiss"), # doesn't have an animation
    "bow": ("Bow", "%s bows"),
    "callme": ("CallMe", "%s wants you to call"),
    "cower": ("Cower", "%s cowers"),
    "crazy": ("Crazy", "%s tries to be funny"),
    "cringe": ("Cringe", "%s cringes"),
    "crossarms": ("CrossArms", "%s is waiting..."),
    "doh": ("Doh", "%s says DOH!"),
    "flinch": ("Flinch", "%s flinches"),
    "groan": ("Groan", "%s groans"),
    "kneel": ("Kneel", "%s kneels down..."),
    "leanleft": ("LeanLeft", "%s leans left"),
    "leanright": ("LeanRight", "%s leans right"),
    "lookaround": ("LookAround", "%s looks around for a bit"),
    "okay": ("Okay", "%s says okay"),
    "overhere": ("OverHere", "%s wants you to come over"),
    "peer": ("Peer", "%s is checking something out"),
    "salute": ("Salute", "%s salutes"),
    "scratchhead": ("ScratchHead", "%s is a bit puzzled..."),
    "shakefist": ("ShakeFist", "%s is a bit upset..."),
    "shoo": ("Shoo", "%s wants some space!"),
    "slouchsad": ("SlouchSad", "%s is sorta bummed..."),
    "stop": ("Stop", "%s says stop!"),
    "talkhand": ("TalkHand", "%s says, \"talk to the hand...\""),
    "tapfoot": ("TapFoot", "%s taps %s foot"),
    "taunt": ("Taunt", "%s taunts you"),
    "thumbsdown": ("ThumbsDown", "Thumbs down from %s"),
    "thumbsdown2": ("ThumbsDown2", "BIG thumbs down from %s"),
    "thumbsup": ("ThumbsUp", "Thumbs up from %s"),
    "thumbsup2": ("ThumbsUp2", "BIG thumbs up from %s"),
    "wavebye": ("Wave", "%s waves goodbye"),
    "wavelow": ("WaveLow", "%s says hey"),
    "winded": ("Winded", "%s needs a moment to breathe!"),
    "dance2": ("DanceMOUL", "%s does a dance"),
}
xChatSpecialHandledCommands = [
    xLocalization.xKI.xChatAllAgeCommand,
    xLocalization.xKI.xChatReplyCommand,
    xLocalization.xKI.xChatPrivateCommand,
    xLocalization.xKI.xChatNeighborsCommand,
    xLocalization.xKI.xChatBuddiesCommand
]

