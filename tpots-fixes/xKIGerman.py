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
from PlasmaConstants import *
xInviteVisitTitle = 'Einladung %s zu besuchen'
xInviteVisitBody = 'Sie sind herzlich eingeladen, die Welt %s zu besuchen, indem sie sich zur MT Nexus-Station begeben ...\n\nGru\xdf,\n%s (Eigent\xfcmer)\n'
xRevokeVisitorTitle = 'Einladung an %s zur\xfcckgezogen'
xRevokeVisitorBody = 'Ihre Besucherrechte f\xfcr die Welt %s gelten nicht mehr.\n\n<Tut mir leid.>\n\nGru\xdf,\n%s (Eigent\xfcmer)'
xKIConfiguration = 'KI-Einstellungen'
xVolumeConfiguration = 'Lautst\xe4rke-Einstellungen'
xOwnerConfiguration = '%s Einstellungen'
xOwnerVistors = '%s Besucher'
xOwnerCoOwners = '%s Eigent\xfcmer'
xDevicesFolderName = 'Ger\xe4te'
xLeaveGameMessageNormal = 'Uru wirklich verlassen?'
xLeaveGameMessageNano = xLeaveGameMessageNormal
xLeaveGameMessageMicro = xLeaveGameMessageNormal
xSendToErrorMessage1 = 'Senden nicht m\xf6glich'
xSendToErrorMessage2 = 'Spieler nicht gefunden'
xSendToErrorMessage3 = 'Unbekannte Spielerart'
xSendToErrorMessage4 = 'Ung\xfcltiges Journalelement'
xSendToErrorMessage5 = 'Darf nur Text enthalten'
xCommandErrorMessage1 = '\'%s\' nicht m\xf6glich - unbekannter Befehl'
xKITimeBroke = '<Verbindung gest\xf6rt>'
xDeletePictureAsk = '\"%s\" wirklich l\xf6schen?'
xDeleteJournalAsk = '\"%s\" wirklich l\xf6schen?'
xDeletePlayerAsk = '\"%s\" wirklich aus Ordner \"%s\" l\xf6schen?'
xKIFullImagesError = 'Ihre KI kann keine weiteren Bilder im Journal speichern. Sie ist augelastet.'
xKIFullNotesError = 'Ihre KI kann keine weiteren Textnotizen im Journal speichern. Sie ist ausgelastet.'
xKIFullMarkersError = 'Ihre KI kann keine weiteren Marker im Journal speichern. Sie ist augelastet.'
xCCRConversationStarted = '(Konversation begonnen)'
xCCRConversationEnded = '(Konversation beendet)'
xCCRNoCCRInContact = '(Kein Kontakt mit Kundenbetreuung, Nachricht nicht gesendet)'
xCCRPetitionSent = '(%s gesendet) %s'
xChatNoOneToReply = '(Es gibt niemand, dem man antworten k\xf6nnte.)'
xChatLeftTheAge = '(%s hat die Welt verlassen)'
xChatLeftTheGame = '(%s hat das Spiel verlassen)'
xChatWentOffline = '(%s ist offline und nicht f\xfcr einen Chat verf\xfcgbar.)'
xChatCannotFindBuddy = '(\'%s\' in keiner Spielerliste gefunden.)'
xChatBroadcastMsgRecvd = ''
xChatPrivateMsgRecvd = 'Von '
xChatInterAgeMsgRecvd = 'Von '
xChatInterAgePlayerRecvd = '%s in %s'
xChatBroadcastSendTo = ''
xChatPrivateSendTo = 'An '
xChatInterAgeSendTo = 'An '
xChatTOPrompt = 'AN:'
xChatAllAgeCommand = '/schreien'
xChatClearAll = '/chatl\xf6schen'
xChatPrivateCommand = '/p'
xChatNeighborsCommand = '/nachbarn'
xChatBuddiesCommand = '/freunde'
xChatNoOneListening = '(Sie sind zu weit weg. Vielleicht sollten Sie schreien.)'
xChatInterAgeNotAvailable = '(Welten-Umschalter nicht verf\xfcgbar)'
xChatReplyCommand = '/antworten'
xChatStartLogCommand = '/protokollan'
xChatStopLogCommand = '/protokollaus'
xChatLogStarted = 'Chat.log aktiviert...'
xChatLogStopped = '...Chat.log gestoppt.'
xChatPetitionCommands = {
    '/petition': PtCCRPetitionType.kGeneralHelp,
    '/hilfe': PtCCRPetitionType.kGeneralHelp,
    '/bug': PtCCRPetitionType.kBug,
    '/feedback': PtCCRPetitionType.kFeedback,
    '/exploit': PtCCRPetitionType.kExploit,
    '/bel\xe4stigung': PtCCRPetitionType.kHarass,
    '/spielproblem': PtCCRPetitionType.kStuck,
    '/technisch': PtCCRPetitionType.kTechnical
}
xChatCCRPetitionTitle = 'Chat-Petition'
xChatCCRCommand = '/ccr'
xChatCCRMsgRecvd = 'Von Kundenbetreuung:'
xChatCCRSendTo = 'An Kundenbetreuung:'
xChatErrorMsgRecvd = 'Fehler:'
xChatCCRFromPlayer = 'Von %d an Kundenbetreuung:'
xChatWeeBeeAFK = ' (Ich bin an der Oberfl\xe4che, komme gleich zur\xfcck)'
xCCRHelpPopupMenu = [
    ('Bug-Report', PtCCRPetitionType.kBug),
    ('Feedback und Vorschl\xe4ge', PtCCRPetitionType.kFeedback),
    ('Ausnutzen von Programmfehlern und Schummeln', PtCCRPetitionType.kExploit),
    ('Bel\xe4stigung und andere Benehmensfragen', PtCCRPetitionType.kHarass),
    ('Probleme mit der Spiell\xf6sung', PtCCRPetitionType.kStuck),
    ('Technische Probleme', PtCCRPetitionType.kTechnical),
    ('Allgemeine Hilfe', PtCCRPetitionType.kGeneralHelp)
]
xCCRHelpPopupDefault = 6
xOfferLinkToMessage = 'Euch wurde eine Verbindung nach \"%s\" angeboten. Wollt Ihr sie benutzen?'
xAgeOwnedStatusLine = '%d Eigent\xfcmer%s mit %d Besucher%s.'
xPorPAgeOwnedStatusLine = '%d Eigent\xfcmer%s mit %d Besucher%s. Und ist %s.'
xNeighborhoodBottomLine = '%s von %s'
xNeighborhoodNone = 'Keine Mitgliedschaft in einer Nachbarschaft'
xNeighborhoodNoName = '<kein Name>'
xNeighborhoodMakePorP = 'Als %s markieren'
xPlayerInCleft = 'Ist online und hat sich in der Spalte verirrt.'
xPlayerInCloset = 'Ist online und wechselt die Kleidung.'
xPlayerInAge = 'Ist online und erforscht die Welt %s.'
xPlayerOffline = 'Ist offline.'
xJournalInitialMessage = '<Text eingeben>'
xJournalInitialTitle = '<Titel eingeben>'
xImageInitialTitle = '<Kommentar eingeben>'
xFolderVisLists = 'Welt-Besucherliste:'
xFolderOwnLists = 'Welt-Eigent\xfcmerliste:'
xMarkerFolderPopupMenu = [('1 Min.', 60), ('2 Min.', 120), ('5 Min.', 300), ('10 Min.', 600)]
xChatMarkerTOAllTeams = 'An: Alle Teams >'
xChatMarkerTOGreenTeam = 'AN: Gr\xfcnes Team >'
xChatMarkerTORedTeam = 'AN: Rotes Team >'
xChatMarkerAllTeams = 'Alle Teams'
xChatMarkerGreenTeam = 'Gr\xfcnes Team'
xChatMarkerRedTeam = 'Rotes Team'
xMarkerGamePrematureEnding = 'Der Spielleiter hat das Spiel beendet!'
xMarkerGameCaptureGame = 'Erobern-Spiel'
xMarkerGameHoldGame = 'Halten-Spiel'
xMarkerGameQuestGame = 'Aufgaben-Spiel'
xMarkerGameBegins = 'Das Spiel beginnt!'
xMarkerGameGreenTeamWins = 'Das gr\xfcne Team gewinnt! %d zu %d'
xMarkerGameTieGame = 'Unentschieden: %d zu %d'
xMarkerGameRedTeamWins = 'Das rote Team gewinnt! %d zu %d'
xMarkerGameEnded = 'Spielende... %s'
xMarkerGameResults = 'Ergebnis:'
xMarkerGameNoMarkers = 'Keine Marker'
xMarkerGameOneMarker = 'Ein Marker'
xMarkerGameNMarkers = '%d Marker'
xMarkerGameCaptured = 'erobert'
xMarkerGameFoundMarker = 'Marker gefunden \'%s\'.'
xMarkerGameLastMarker = 'Und das war der letzte Marker.'
xMarkerGameOneMoreLeft = 'Nur noch EIN Marker!'
xMarkerGameCaptures = '%s erobert \'%s\'. %s'
xMarkerGameEditButton = 'Spiel bearbeiten'
xMarkerGamePlayButton = 'Spiel beginnen'
xMarkerGameDoneEditButton = 'Bearbeiten beenden'
xMarkerGameAddMarkerButton = 'Marker hinzuf\xfcgen'
xMarkerGameMarkerListButton = 'Markerliste'
xMarkerGameRemoveMarkerButton = 'Marker entfernen'
xMarkerGameGoBackButton = 'Zur\xfcck'
xMarkerGameInviteButton = 'Spieler einladen'
xMarkerGameStartGameButton = 'Spiel starten'
xMarkerGameEndGameButton = 'Spiel beenden'
xMarkerGameStopPlayingButton = 'Spiel abbrechen'
xMarkerGameResetGameButton = 'Spiel zur\xfccksetzen'
xMarkerGameStatusNoMarkers = 'Es gibt keine Marker'
xMarkerGameStatusOneMarker = 'Es gibt einen Marker'
xMarkerGameStatusNMarkers = 'Es gibt %s Marker'
xMarkerGameStatusIn = ' in %s'
xMarkerGameStatusAllFound = 'Alle Aufgaben-Marker wurden gefunden.'
xMarkerGameStatusNotAllFound = 'Nicht alle Aufgaben-Marker wurden gefunden.'
xWaitingForStartText = 'Warte auf Start'
xTimeRemainingText = 'Verbleibende Zeit: %01d:%02d'
xMarkerGameMarkersRemaining = 'Verbleibende Marker: %d'
xMarkerGameMarkersUnclaimed = 'Freie Marker: %d'
xMarkerGameGreenTeamScore = 'Gr\xfcnes Team(%d)'
xMarkerGameRedTeamScore = 'Rotes Team(%d)'
xMarkerGameNameCapture = 'Erobern'
xMarkerGameInstructCapNoMarker = 'Da es in diesen Spiel keine Marker gibt, haben alle gewonnen oder verloren!'
xMarkerGameInstructCapOneMarker = 'Das Team, das den einzelnen Marker erobert ehe %d Minute%s um sind, gewinnt!'
xMarkerGameInstructCapNMarkers = 'Das Team, das in %d Minute%s die meisten Marker erobert, gewinnt!'
xMarkerGameNameHold = 'Halten'
xMarkerGameInstructHoldNoMarker = 'Da es in diesen Spiel keine Marker gibt, haben alle gewonnen oder verloren!'
xMarkerGameInstructHoldNMarkers = 'Das Team, das nach %d Minute%s die meisten Marker erobert hat und h\xe4lt, gewinnt!'
xMarkerGameNameQuest = 'Aufgabe'
xMarkerGameInstructQuest = 'Einladung nicht m\xf6glich - dies ist ein Einzelspieler-Spiel'
xMarkerGameNameUnknown = 'Unbekannte Art'
xMarkerGameQTitle = 'Marker-Spiel von %s anschlie\xdfen'
xMarkerGameQMessage = '    %s hat Sie zu einer Runde \'%s\' eingeladen.\n    %s\n\nWollen Sie mitspielen?'
xMarkerGameInviteRecvd = 'Einladung zu einem Spiel erhalten. Sehen Sie Ihre Nachrichten durch.'
xYesNoYESbutton = 'Ja'
xYesNoOKbutton = 'Ok'
xYesNoAcceptButton = 'Annehmen'
xYesNoDeclineButton = 'Ablehnen'
xYesNoQuitbutton = 'Ja'
xYesNoNoButton = 'Nein'
xOptMenuKeyMap = 'Tastatur'
xOptMenuGameSettings = 'Spieleinstellungen'
xOptMenuURULive = 'URU Live'
xOptMenuHelp = 'Hilfe'
xOptMenuCredits = 'URU Credits'
xOptMenuQuit = 'URU verlassen'
xOptMenuOk = 'Spiel fortsetzen'
xOptMenuCancel = 'Abbrechen'
xMoveForward = 'Vorw\xe4rts'
xMoveBackward = 'R\xfcckw\xe4rts'
xRotateLeft = 'Nach links drehen'
xRotateRight = 'Nach rechts drehen'
xJump = 'Springen'
xExitMode = 'Modus verlassen'
xPushToTalk = 'Dr\xfccken zum Sprechen'
xOKDialogDict = {
    '': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#01',
    'TERMINATED: Server LogOff. Reason: Logged In Elsewhere': 'Ihre Verbindung wurde getrennt, da Ihr Konto bereits benutzt wird.\n#02',
    'TERMINATED: Server LogOff. Reason: Timed Out': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#03',
    'TERMINATED: Server LogOff. Reason: Not Authenticated': 'Bei der Verbindungsherstellung ist ein Problem aufgetreten. Bitte \xfcberpr\xfcfen Sie Kontonamen und Passwort und versuchen Sie es erneut.\n#04',
    'TERMINATED: Server LogOff. Reason: Kicked Off': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#05',
    'TERMINATED: Server LogOff. Reason: Unknown Reason': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#06',
    'TERMINATED: Server LogOff. Reason: CCRs must use a protected lobby': 'Ihre Verbindung wurde getrennt, da Kundenbetreuer eine gesch\xfctzte Lobby verwenden m\xfcssen.\n#07',
    'TERMINATED: Server LogOff. Reason: CCRs must have internal client code': ' Ihre Verbindung wurde getrennt, da Kundenbetreuer einen internen Kundencode verwenden m\xfcssen.\n#08',
    'TERMINATED: Server LogOff. Reason: UNKNOWN REASON CODE': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut..\n#09',
    'SERVER SILENCE': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#10',
    'BAD VERSION': 'Dies ist eine alte Uru-Version. Bitte aktualisieren Sie Ihre Version.\n#11',
    'Player Disabled': 'Der von Ihnen gew\xe4hlte charakter ist ung\xfcltig. Bitte wenden Sie sich an den Kundendienst.\n#12',
    'CAN\'T FIND AGE': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#13',
    'AUTH RESPONSE FAILED': 'Bei der Verbindungsherstellung ist ein Problem aufgetreten. Bitte \xfcberpr\xfcfen Sie Kontonamen und Passwort und versuchen Sie es erneut.\n#14',
    'AUTH TIMEOUT': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#15',
    'SDL Desc Problem': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#16',
    'Unspecified error': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#17',
    'Failed to send msg': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#18',
    'Authentication timed out': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#19',
    'Peer timed out': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#20',
    'Server silence': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#21',
    'Protocol version mismatch': 'Dies ist eine alte Uru-Version. Bitte aktualisieren Sie Ihre Version.\n#22',
    'Auth failed': 'Bei der Verbindungsherstellung ist ein Problem aufgetreten. Bitte \xfcberpr\xfcfen Sie Kontonamen und Passwort und versuchen Sie es erneut.\n#23',
    'Failed to create player': 'Bei der Erstellung Ihres Spielers ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut.\n#24',
    'Invalid error code': 'Es scheint ein Problem mit der Verbindung vorzuliegen. Bitte versuchen Sie es erneut.\n#25',
    'linking banned': 'Ihre Buch-Verbindungen wurden deaktiviert\n#26',
    'linking restored': 'Ihre Buch-Verbindungen wurden wiederhergestellt\n#27',
    'silenced': 'Ihre Chat-Funktion wurde deaktiviert\n#28',
    'unsilenced': 'Ihre Chat-Funktion wurde wiederhergestellt\n#29'
}
xInviteKeyAdded = 'Einladnugsschl\xfcssel hinzugef\xfcgt: %s'
xMaxInvites = 'Maximale Zahl von Einladungen erreicht'
xMissingInviteFolder = 'Einladungsordner nicht vorhanden'
xInviteUsage = 'Syntax: /einladung <Einladungsschl\xfcssel>'
xInviteAccepted = 'Einladung von Freund: %s mit Schl\xfcssel: %s akzeptieren?'
xAcceptUsage = 'Syntax: /annehmen <Name des Freundes> <Schl\xfcssel>'
xCouldNotCast = 'Listenelement konnte nicht verarbeitet werden'
xKeys = 'Schl\xfcssel: '
xRemoveNodeFailed = 'Entfernen von Node gescheitert'
xInviteNotFound = 'Einladung nicht gefunden'
xUninviteUsage = 'Syntax: /einladungl\xf6schen <Einladungsschl\xfcssel>'
xDeletedInvitation = 'Gel\xf6schte Einladung: '
xSitCmd = 'sit'
xAfkCmd = 'afk'
xInviteCmd = 'einladung'
xUninviteCmd = 'einladungl\xf6schen'
xAcceptCmd = 'annehmen'
xShowInvitesCmd = 'einladungsliste'
xWaveCmd = 'winken'
xWaveString = '%s winkt'
xSneezeCmd = 'niesen'
xSneezeString = '%s niest'
xClapCmd = 'klatschen'
xClapString = '%s klatscht'
xLaughCmd = 'lachen'
xLaughString = '%s lacht'
xLOLCmd = 'lol'
xLOLString = '%s beginnt laut zu lachen'
xROTFLCmd = 'rotfl'
xROTFLString = '%s lacht schallend'
xDanceCmd = 'tanzen'
xDanceString = '%s tanzt'
xYesCmd = 'ja'
xYesString = '%s nickt'
xNoCmd = 'nein'
xNoString = '%s sch\xfcttelt den Kopf'
xYawnCmd = 'g\xe4hnen'
xYawnString = '%s g\xe4hnt'
xCheerCmd = 'jubeln'
xCheerString = '%s jubelt'
xThanksCmd = 'vielendank'
xThanksString = '%s dankt Ihnen herzlich!'
xThxCmd = 'danke'
xThxString = '%s dankt Ihnen'
xCryCmd = 'traurig'
xCryString = '<schn\xfcff> %s ist traurig'
xCriesCmd = 'weinen'
xCriesString = '%s weint'
xDontKnowCmd = 'ratlos'
xDontKnowString = '%s zuckt mit den Schultern'
xShrugCmd = 'schulternzucken'
xShrugString = '%s zuckt mit den Schultern'
xDunnoCmd = 'wei\xdfnicht'
xDunnoString = '%s zuckt mit den Schultern'
xPointCmd = 'punkte'
xPointString = '%s points'
xKISettingsFontSizeText = 'Schriftgr\xf6\xdfe:'
xKISettingChatFadeTimeText = 'Chatblende:'
xKISettingsOnlyBuddiesText = 'Nur private und KI-Nachrichten von Freunden annehmen'
xKIDescriptionText = 'Beschreibung:'
xMarkerGameOwnerTitle = 'BESITZER:'
xMarkerGameTimeText = 'Spielzeit:'
xCCRAwayText = 'KB derzeit nicht verf\xfcgbar'
xCCRPetitionTypeText = 'Petitionsart:'
xCCRSubjectText = 'Betreff:'
xCCRCommentText = 'Kommentar:'
xCCRSubmitBtnText = 'Senden'
xCCRCancelBtnText = 'Abbruch'
xKIStatusNexusLinkAdded = 'Ein Link wurde zu Ihrer KI zugef\xfcgt.'
xPlayerEnterID = 'G:Enter player ID or name:'
xPlayerNumberOnly = 'G:Please enter a player ID or current Age player name.'
xPlayerNotYourself = 'G:Can\'t be yourself.'
xCreateBuddyTitle = '<G:add buddy by ID or name if in Age>'
xChatAddBuddyCmd = '/addbuddy'
xChatRemoveBuddyCmd = '/removebuddy'
xChatIgnoreCmd = '/ignore'
xChatUnIgnoreCmd = '/unignore'
xPlayerAlreadyAdded = 'G:Player has already been added.'
xPlayerNotFound = 'G:Player not found.'
xPlayerAdded = 'G:Player added.'
xPlayerRemoved = 'G:Player removed.'
xCannotDeleteImage = 'G:Cannot delete the picture as it may be in use.'


