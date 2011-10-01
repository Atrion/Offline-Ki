# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2004-2011  The Offline KI contributors                      #
#    See the file AUTHORS for more info about the contributors                 #
#                                                                              #
#    This program is free software; you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation; either version 2 of the License, or         #
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with this program; if not, write to the Free Software               #
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA #
#                                                                              #
#    Please see the file COPYING for the full GPLv2 license.                   #
#                                                                              #
#    Uru exception: In addition, this file may be used in combination with     #
#    (non-GPL) code within the context of Uru.                                 #
#                                                                              #
#==============================================================================#
from Plasma import *
from PlasmaTypes import *
kChronicleUserAgeType = 4

def ISetBaseChron():
    vault = ptVault()
    entry = vault.findChronicleEntry('UserAges')
    if (type(entry) == type(None)):
        PtDebugPrint('ISetBaseChron: Create UserAges base chronicle')
        vault.addChronicleEntry('UserAges', kChronicleUserAgeType, '')
        return 1
    PtDebugPrint('ISetBaseChron: UserAges base chronicle found, do nothing...')
    return 0



def ISetSubChron(ageName):
    if (not ageName):
        return 
    ourChild = None
    vault = ptVault()
    entry = vault.findChronicleEntry('UserAges')
    if (type(entry) == type(None)):
        PtDebugPrint('DEBUG: No UserAges chronicle')
        return 
    chronRefList = entry.getChildNodeRefList()
    for subChron in chronRefList:
        theChild = subChron.getChild()
        theChild = theChild.upcastToChronicleNode()
        if (theChild.chronicleGetName() == ageName):
            ourChild = theChild
            break

    if (type(ourChild) == type(None)):
        PtDebugPrint(('ISetSubChron: Create subchronicle %s' % ageName))
        newNode = ptVaultChronicleNode(0)
        newNode.chronicleSetName(ageName)
        newNode.chronicleSetType(kChronicleUserAgeType)
        newNode.chronicleSetValue('')
        entry.addNode(newNode)



def IWriteAgeChron(ageName, chronName, chronVal):
    chronVal = str(chronVal)
    ourChild = None
    vault = ptVault()
    entry = vault.findChronicleEntry('UserAges')
    if (type(entry) == type(None)):
        PtDebugPrint('DEBUG: No UserAges chronicle')
        return 
    chronRefList = entry.getChildNodeRefList()
    for ageChron in chronRefList:
        theChild = ageChron.getChild()
        theChild = theChild.upcastToChronicleNode()
        if (theChild.chronicleGetName() == ageName):
            PtDebugPrint(('IWriteAgeChron: %s chronicle found' % ageName))
            chronRefList2 = theChild.getChildNodeRefList()
            for ageChron2 in chronRefList2:
                theChild2 = ageChron2.getChild()
                theChild2 = theChild2.upcastToChronicleNode()
                if (theChild2.chronicleGetName() == chronName):
                    ourChild = theChild2
                    break

            if (type(ourChild) == type(None)):
                PtDebugPrint(('IWriteAgeChron: Create chronicle %s, value=%s' % (chronName,
                 chronVal)))
                newNode = ptVaultChronicleNode(0)
                newNode.chronicleSetName(chronName)
                newNode.chronicleSetType(kChronicleUserAgeType)
                newNode.chronicleSetValue(chronVal)
                theChild.addNode(newNode)
            else:
                if (ourChild.chronicleGetValue() == chronVal):
                    PtDebugPrint('IWriteAgeChron: Chronicle value already correct, do nothing')
                    return 
                PtDebugPrint(('IWriteAgeChron: Change chronicle %s value to %s' % (chronName,
                 chronVal)))
                ourChild.chronicleSetValue(chronVal)
                ourChild.save()




def IReadAgeChron(ageName, chronName):
    vault = ptVault()
    entry = vault.findChronicleEntry('UserAges')
    if (type(entry) == type(None)):
        PtDebugPrint('DEBUG: No UserAges chronicle')
        return 0
    chronRefList = entry.getChildNodeRefList()
    for ageChron in chronRefList:
        theChild = ageChron.getChild()
        theChild = theChild.upcastToChronicleNode()
        if (theChild.chronicleGetName() == ageName):
            PtDebugPrint(('IReadAgeChron: %s chronicle found' % ageName))
            chronRefList2 = theChild.getChildNodeRefList()
            for ageChron2 in chronRefList2:
                theChild2 = ageChron2.getChild()
                theChild2 = theChild2.upcastToChronicleNode()
                if (theChild2.chronicleGetName() == chronName):
                    chronVal = theChild2.chronicleGetValue()
                    PtDebugPrint(('IReadAgeChron: %s chronicle found, value=%s' % (chronName,
                     chronVal)))
                    return chronVal


    PtDebugPrint(('IReadAgeChron: Chronicle %s missing' % chronName))
    return 0
