# -*- coding: utf-8 -*-
from Plasma import *
from PlasmaNetConstants import *
from NegilahnJournal import *
from JalakJournal import *
from MinkataJournal import *
PageStart = '<pb>'
ImgStart = '<img src="'
TransImgStart = '<img opacity=0.7 src="'
ImgEnd = '" align=center link=%d blend=alpha>'
ImgEndNoLink = '" align=center blend=alpha>'
AlignCenter = '<p align=center>'
AlignLeft = '<p align=left>'
AlignRight = '<p align=right>'
YeeshaStamp = '<img src="xYeeshaBookStampVSquish*1#0.hsm" pos=140,255 resize=no blend=alpha>'
plyrName = PtGetLocalPlayer().getPlayerName()
AgeBooks = {
    'M-NegilahnBook': ('', '', 1, 0, 'BkBook', 1.0, 1.0),
    'M-DerenoBook': ('', '', 1, 0, 'BkBook', 1.0, 1.0),
    'M-PayiferenBook': ('', '', 1,0, 'BkBook', 1.0, 1.0),
    'M-TetsonotBook': ('', '', 1, 0, 'BkBook', 1.0, 1.0),
    'jrnlNegilahn': ('<cover src="xnegilahninfojournalc"><margin right=32 left=32>', '', 0, 0, 'bkNotebook', 1.0, 1.0),
    'LIBMinkataBook': ('', '', 1, 0, 'BkBook', 1.0, 1.0),
    'LIBJalakBook': ('', '', 1, 0, 'BkBook', 1.0, 1.0),
    'DniLinkingBookToDelin': ('', '', 1, 0, 'BkBook', 1.0, 1.0),
    'DniLinkingBookToGZ': ('', '', 1, 0, 'BkBook', 1.0, 1.0),
    'EderTsogalLinkBook': ('', '', 1, 0, 'BkBook', 1.0, 1.0),
    'BahroRockBook': ('', '', 1, 0, 'bkBahroRockBook', 1.0, 1.0),
    'jrnlJalak': ('<cover src="JalakJournalCover.PNG"><margin right=32 left=32>', '', 0, 0, 'BkBook', 1.0, 1.0),
    'jrnlMinkata': ('<cover src="minkQuestJournal*1#0.hsm"><margin right=32 left=32>', '<img src="minkJournalPage*1#0.hsm" pos=0,0>', 0, 0, 'BkBook', 1.0, 1.0),
    'BahroBookKadish': ('', '', 1, 0, 'bkBahroRockBook', 1.0, 1.0),
    'BahroBookDescent': ('', '', 1, 0, 'bkBahroRockBook', 1.0, 1.0),
    'BahroStoneKveer': ('', '', 1, 0, 'bkBahroRockBook', 1.0, 1.0),
    'MT-LinkingBook': ('', '', 1, 0, 'bkBook', 1.0, 1.0),
    'NbhoodLinkingBook': ('', '', 1, 0, 'bkbook', 1.0, 1.0),
    'M-TodelmerBook': ('', '', 1, 0, 'bkBook', 1.0, 1.0),
    'LIBReleeshanBook': ('', '', 1, 0, 'bkBook', 1.0, 1.0),
    'GuildRockBook': ('', '', 1, 0, 'bkBahroRockBook', 1.0, 1.0),
    'SeretRockBook': ('', '', 1, 0, 'bkBahroRockBook', 1.0, 1.0),
}
BookPages = {
    'M-NegilahnBook': PageStart + ImgStart + 'xlinkpanelnegilahndefault*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'M-DerenoBook': PageStart + ImgStart + 'xlinkpanelderenodefault*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'M-PayiferenBook': PageStart + ImgStart + 'xlinkpanelpayiferendefault*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'M-TetsonotBook': PageStart + ImgStart + 'xlinkpaneltetsonotdefault*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'NegilahnJournal': PageStart + xNegilahnContents,
    'LIBMinkataBook': PageStart + ImgStart + 'xlinkpanelminkatadefault*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'LIBJalakBook': PageStart + ImgStart + 'xlinkpaneljalakdefault*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'DniLinkingBookToDelin': PageStart + ImgStart + 'xlinkpanelederdelindefault*1#0.hsm' + ImgEnd + AlignCenter,
    'BahroRockBook': PageStart + TransImgStart + 'xlinkpanelcitygreattree*1#0.hsm' + ImgEnd + AlignCenter,
    'DniLinkingBookToGZ': PageStart + ImgStart + 'xlinkpanelgrtzerolinkrm*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'EderTsogalLinkBook': PageStart + ImgStart + 'xlinkpaneltsogarden*1#0.hsm' + ImgEnd + AlignCenter,
    'JalakJournal': PageStart + xJalakContents,
    'MinkataJournal': PageStart + xMinkataContents,
    'BahroBookDescent': PageStart + TransImgStart + 'xlinkpaneldescentshaftfall*1#0.hsm' + ImgEnd + AlignCenter,
    'BahroBookKadish': PageStart + TransImgStart + 'xlinkpanelkadishglowbalc*1#0.hsm' + ImgEnd + AlignCenter,
    'BahroStoneKveer': PageStart + TransImgStart + 'xlinkpanelkveergreathall*1#0.hsm' + ImgEnd + AlignCenter,
    'MT-LinkingBook': PageStart + ImgStart + 'xlinkpanelnexusdefault*1#0.hsm' + ImgEnd + AlignCenter,
    'NbhoodLinkingBook': PageStart + ImgStart + 'xlinkpanelbevindefault*1#0.hsm' + ImgEnd + AlignCenter,
    'M-TodelmerBook': PageStart + ImgStart + 'xlinkpaneltodelmerpod*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'LIBReleeshanBook': PageStart + ImgStart + 'xlinkpanelreleeshandefault*1#0.hsm' + ImgEnd + AlignCenter + YeeshaStamp,
    'GuildRockBook': PageStart + TransImgStart + 'xlinkpanelkirel*1#0.hsm' + ImgEnd + AlignCenter,
    'SeretRockBook': PageStart + TransImgStart + 'xislmkaeseretlink-1-0' + ImgEnd + AlignCenter,
}
LinkDestinations = {
    'M-NegilahnBook': ('Negilahn', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'M-DerenoBook': ('Dereno', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'M-PayiferenBook': ('Payiferen', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'M-TetsonotBook': ('Tetsonot', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'NegilahnJournal': (None, None, None, None),
    'LIBMinkataBook': ('Minkata', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'LIBJalakBook': ('Jalak', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'BahroRockBook': ('city', 'LinkInPointGreatTree', 'Great Tree', PtLinkingRules.kOriginalBook),
    'DniLinkingBookToDelin': ('EderDelin', 'LinkInPointDefault', None, PtLinkingRules.kBasicLink),
    'DniLinkingBookToGZ': ('GreatZero', 'LinkInPointDefault', 'grtzGrtZeroLinkRm', PtLinkingRules.kOriginalBook),
    'EderTsogalLinkBook': ('EderTsogal', 'LinkInPointDefault', None, PtLinkingRules.kBasicLink),
    'BahroBookDescent': ('Descent', 'LinkInPointShaftFall', 'dsntShaftFall', PtLinkingRules.kOriginalBook),
    'BahroBookKadish': ('Kadish', 'LinkInPointGlowRmBalcony', 'kdshGlowRmBalcony', PtLinkingRules.kOriginalBook),
    'BahroStoneKveer': ('KveerMOUL', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'JalakJournal': (None, None, None, None),
    'MinkataJournal': (None, None, None, None),
    'MT-LinkingBook': ('Nexus', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'NbhoodLinkingBook': ('Neighborhood', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
    'M-TodelmerBook': ('Todelmer', 'EsherWarpRing', 'Todelmer Pod', PtLinkingRules.kOriginalBook),
    'LIBReleeshanBook': ('KveerMystV', 'WarpEsherRlsn', 'Releeshan', PtLinkingRules.kBasicLink),
    'GuildRockBook': ('KirelMOUL', 'kirelPerf-SpawnPointBevin02', None, PtLinkingRules.kOriginalBook),
    'SeretRockBook': ('NeighborhoodMOUL', 'LinkInPointDefault', None, PtLinkingRules.kOriginalBook),
}
