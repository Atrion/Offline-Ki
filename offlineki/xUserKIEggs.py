# -*- coding: utf-8 -*-
import string
import os
from Plasma import *
from PlasmaTypes import *
from PlasmaKITypes import *
from PlasmaVaultConstants import *
from PlasmaNetConstants import *
from xPsnlVaultSDL import *
import xLinkMgr
import xUserKI

# Main function - copied from MOUL KI
def OnCommand(ki, arg, cmnd, args, playerList, KIContent, silent):
    if (cmnd == 'look' and arg.lower() == 'in pocket'):
        if ki.getgFeather():
            if (ki.getgFeather() == 1):
                ki.IAddRTChat(None, 'You see a feather!', 0)
            else:
                pfeathers = ki.getgFeather()
                if (pfeathers > 7):
                    pfeathers = 7
                pOut = ('You see %d plain feathers' % pfeathers)
                if (ki.getgFeather() > 7):
                    pOut += " and a 'Red' feather"
                if (ki.getgFeather() > 8):
                    pOut += " and a 'Blue' feather"
                if (ki.getgFeather() > 9):
                    pOut += " and a 'Black' feather"
                if (ki.getgFeather() > 10):
                    pOut += " and a 'Silver' feather"
                if (ki.getgFeather() > 11):
                    pOut += " and a 'Duck' feather"
                if (ki.getgFeather() > 12):
                    pOut += " and a large 'Rukh' feather (sticking out of your pocket)"
                pOut += '.'
                ki.IAddRTChat(None, pOut, 0)
        else:
            ki.IAddRTChat(None, 'There is nothing there but lint.', 0)
        return True
    if (cmnd == 'look'):
        plist = ki.IRemoveCCRPlayers(ki.IGetPlayersInChatDistance(minPlayers=-1))
        people = 'nobody in particular'
        if (len(plist) > 0):
            people = ''
            for p in plist:
                people += (p.getPlayerName() + ', ')
            people = people[:-2]
        loc = ki.IGetAgeFileName()
        see = ''
        exits = 'North and West'
        if (loc == 'city'):
            see = '  You see the remnants of a great civilization, ready to be rebuilt. Where are the flying monkeys?\n'
            exits = 'North, West and South'
        elif (loc == 'Personal'):
            see = '  You see a small hut... looks deserted.\n'
            exits = '... well, there are no exits'
        elif (loc == 'Teledahn'):
            see = "  You see 'shrooms everywhere! Big ones, small ones. Are they edible?\n"
            exits = 'East'
        elif (loc == 'Nexus'):
            see = '  You see a jukebox like machine.\n'
            exits = '... well, there are no exits'
        elif (loc == 'Garden'):
            see = '  You see bugs.   BUGS! I hate bugs.\n'
            exits = 'North and South'
        elif (loc == 'EderTsogal'):
            see = '  You see grass, water and things floating in the air (not feathers).\n'
            exits = "North. But you'll have to climb or fly to get there"
        elif (loc == 'Dereno'):
            see = '  Ah, Dah-Ree-Toe. You see... well, if someone would clean those stupid windows you could see a *lot*. Have I been here before? Maybe all pods just look the same.\n'
            exits = 'South, West and East but they are all blocked'
        elif (loc == 'BahroCave'):
            see = '  You see a darkly lit cavern. Strange images on the wall next to you, flickering in the subdued light.\nBe afraid. Be very afraid!\n'
            exits = 'North, West and East... but they are blocked by a large hole in the floor'
        elif (loc == 'Minkata'):
            see = '  You see sand and dust in all directions. Above you there is a filtered sun or two... or more.\nSomewhere there is a horse with no name.\n'
            exits = 'East. Nine days away'
        elif (loc == 'Cleft'):
            see = '  You see sand for as far as the eye can see. Gonna need a vehicle of some sort.\n'
            exits = "... well, I don't know. Maybe you can ask the old man (if he ever stops listening to that music!)"
            people = "an old man. Ok, maybe he's not standing. BTW, wasn't he on M*A*S*H?"
        ki.IAddRTChat(None, ('%s:\n%s  Standing near you is %s.\n  There are exits to the %s.' % (ki.IGetAgeDisplayName(), see, people, exits)), 0)
        return True
    if (cmnd == 'go'):
        ki.IAddRTChat(None, 'Put one foot in front of the other and eventually you will get there.', 0)
        return True
    if (cmnd == 'get' and arg.lower() in ['feather', 'feathers']):
        loc = ki.IGetAgeFileName()
        if (loc == 'Gira'):
            if (ki.getgFeather() < 7):
                ki.IAddRTChat(None, "You pick up a plain feather and put it in your pocket. I know you didn't see yourself do that... trust me, you have a feather in your pocket.", 0)
                #xKI.gFeather += 1
                ki.setgFeather(ki.getgFeather()+1)
                vault = ptVault()
                entry = vault.findChronicleEntry('feather')
                if (type(entry) == type(None)):
                    vault.addChronicleEntry('feather', 1, ('%d' % ki.getgFeather()))
                else:
                    entry.chronicleSetValue(('%d' % ki.getgFeather()))
                    entry.save()
            else:
                ki.IAddRTChat(None, 'You can only carry seven plain feathers.', 0)
        elif (loc == 'EderDelin'):
            if (ki.getgFeather() == 7):
                ki.IAddRTChat(None, "You search... and find the 'Red' feather and put it in your pocket.", 0)
                #xKI.gFeather += 1
                ki.setgFeather(ki.getgFeather()+1)
                vault = ptVault()
                entry = vault.findChronicleEntry('feather')
                if (type(entry) == type(None)):
                    vault.addChronicleEntry('feather', 1, ('%d' % ki.getgFeather()))
                else:
                    entry.chronicleSetValue(('%d' % ki.getgFeather()))
                    entry.save()
            elif (ki.getgFeather() > 7):
                ki.IAddRTChat(None, 'You search... but find no other feathers.', 0)
            else:
                ki.IAddRTChat(None, 'You search... but then suddenly stop when you realize that you are missing seven plain feathers.', 0)
        elif (loc == 'Dereno'):
            if (ki.getgFeather() == 8):
                ki.IAddRTChat(None, "You search... and find the 'Blue' feather and put it in your pocket.", 0)
                #xKI.gFeather += 1
                ki.setgFeather(ki.getgFeather()+1)
                vault = ptVault()
                entry = vault.findChronicleEntry('feather')
                if (type(entry) == type(None)):
                    vault.addChronicleEntry('feather', 1, ('%d' % ki.getgFeather()))
                else:
                    entry.chronicleSetValue(('%d' % ki.getgFeather()))
                    entry.save()
            elif (ki.getgFeather() > 8):
                ki.IAddRTChat(None, 'You search... but find no other feathers.', 0)
            else:
                ki.IAddRTChat(None, "You search... but then suddenly stop when you realize that you are missing the 'Red' feather.", 0)
        elif (loc == 'Payiferen'):
            if (ki.getgFeather() == 9):
                ki.IAddRTChat(None, "You search... and find the 'Black' feather and put it in your pocket.", 0)
                #xKI.gFeather += 1
                ki.setgFeather(ki.getgFeather()+1)
                vault = ptVault()
                entry = vault.findChronicleEntry('feather')
                if (type(entry) == type(None)):
                    vault.addChronicleEntry('feather', 1, ('%d' % ki.getgFeather()))
                else:
                    entry.chronicleSetValue(('%d' % ki.getgFeather()))
                    entry.save()
            elif (ki.getgFeather() > 9):
                ki.IAddRTChat(None, 'You search... but find no other feathers.', 0)
            else:
                ki.IAddRTChat(None, "You search... but then suddenly stop when you realize that you are missing the 'Blue' feather.", 0)
        elif (loc == 'Ercana'):
            if (ki.getgFeather() == 10):
                ki.IAddRTChat(None, "You search... and find the 'Silver' feather and put it in your pocket.", 0)
                #xKI.gFeather += 1
                ki.setgFeather(ki.getgFeather()+1)
                vault = ptVault()
                entry = vault.findChronicleEntry('feather')
                if (type(entry) == type(None)):
                    vault.addChronicleEntry('feather', 1, ('%d' % ki.getgFeather()))
                else:
                    entry.chronicleSetValue(('%d' % ki.getgFeather()))
                    entry.save()
            elif (ki.getgFeather() > 10):
                ki.IAddRTChat(None, 'You search... but find no other feathers.', 0)
            else:
                ki.IAddRTChat(None, "You search... but then suddenly stop when you realize that you are missing the 'Black' feather.", 0)
        elif (loc == 'Jalak'):
            if (ki.getgFeather() == 11):
                ki.IAddRTChat(None, "You search... and find the 'Duck' feather and put it in your pocket.", 0)
                #xKI.gFeather += 1
                ki.setgFeather(ki.getgFeather()+1)
                vault = ptVault()
                entry = vault.findChronicleEntry('feather')
                if (type(entry) == type(None)):
                    vault.addChronicleEntry('feather', 1, ('%d' % ki.getgFeather()))
                else:
                    entry.chronicleSetValue(('%d' % ki.getgFeather()))
                    entry.save()
            elif (ki.getgFeather() > 11):
                ki.IAddRTChat(None, 'You search... but find no other feathers.', 0)
            else:
                ki.IAddRTChat(None, "You search... but then suddenly stop when you realize that you are missing the 'Silver' feather.", 0)
        elif (loc == 'Ahnonay'):
            if (ki.getgFeather() == 12):
                ki.IAddRTChat(None, "You search... and find a large 'Rukh' feather (how could you have missed it?) and put it in your pocket.", 0)
                #xKI.gFeather += 1
                ki.setgFeather(ki.getgFeather()+1)
                vault = ptVault()
                entry = vault.findChronicleEntry('feather')
                if (type(entry) == type(None)):
                    vault.addChronicleEntry('feather', 1, ('%d' % ki.getgFeather()))
                else:
                    entry.chronicleSetValue(('%d' % ki.getgFeather()))
                    entry.save()
            elif (ki.getgFeather() > 12):
                ki.IAddRTChat(None, 'You search... but find no other feathers.', 0)
            else:
                ki.IAddRTChat(None, "You search... but then suddenly stop when you realize that you are missing the 'Duck' feather.", 0)
        else:
            ki.IAddRTChat(None, 'There are no feathers here.', 0)
        return True
    if (cmnd == 'get'):
        if (len(arg) and arg[-1:] == 's'):
            v = 'are'
        else:
            v = 'is'
        ki.IAddRTChat(None, 'The %s %s too heavy to lift. Maybe you should stick to feathers.' % (arg, v), 0)
        return True
    if cmnd == 'fly':
        ki.IAddRTChat(None, 'You close your eyes, you feel light headed and the ground slips away from your feet... Then you open your eyes and WAKE UP! (Ha, you can only dream about flying.)', 0)
        return True
    return False
