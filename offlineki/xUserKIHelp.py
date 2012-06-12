# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2004-2011  The Offline KI contributors                      #
#    See the file AUTHORS for more info about the contributors (including      #
#    contact information)                                                      #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    Please see the file COPYING for the full GPLv3 license, or see            #
#    <http://www.gnu.org/licenses/>                                            #
#                                                                              #
#    Uru exception: In addition, this file may be used in combination with     #
#    (non-GPL) code within the context of Uru.                                 #
#                                                                              #
#==============================================================================#
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
import xxConfig

import re

helpBook = None # needs to be a global variable?!?

fontCaption = "font size=16 face=Arial"
fontText = "font size=12 face=Arial"
fontCommandText = "font size=10 face=Courier"

commandWidth = 59 # font size 12: max. 47 characters; size 10: max. 59 characters
commandIndent = 5

syntax = '''Each argument is enclosed by < and >. Arguments enclosed by <[ and ]> are optional. From a list of optional arguments, you can only skip the last ones, because the KI has to know which ones you skipped - don't skip one argument and use another one coming after it, that is not possible. You can also get the syntax description in-game by passing "help" as first and only argument.

A "color" is either specified by a simple name like "white" or by three values for the red, green and blue part, e.g. "0.5 0.9 0.1". The "player name" is the name of an avatar in the same or another age, but without spaces - use "me" to run the command on yourself. An "object name" is the name of a scene object or a player in the age you are in. Accordingly, a "list of players" or a "list of objects" is a space-separated list of items of the corresponding type, with the additional possibility to use "all" as shortcut for everyone in the current age except for yourself. For lists of objects, you can also specify a pre-defined object list of the current age - see "/list objectlists". If such a list is optional, it defaults to the objects you have under control in flymode. If flymode is disabled, it defaults to your own avatar.

Commands requiring story or admin access only work for some players online - the Shard administrator has to grant these additional privileges. Offline, everyone is an admin. Admin access always includes story access.'''

commands = r"""=== Avatar appearance and animation commands ===

You can use all emotes from Uru:CC and MO:UL. The complete list is below.

*/afk <[afk-message]>
*/sit <[message]>
*/wave <[message]>
*/sneeze <[message]>
*/clap <[message]>
*/laugh <[message]>
*/lol <[message]>
*/rotfl <[message]>
*/dance <[message]>
*/yes <[message]>
*/no <[message]>
*/yawn <[message]>
*/cheer <[message]>
*/thanks <[message]>
*/thx <[message]>
*/cry <[message]>
*/cries <[message]>
*/dontknow <[message]>
*/shrug <[message]>
*/dunno <[message]>
*/point <[message]>
*/amazed <[message]>
*/askquestion <[message]>
*/beckonbig <[message]>
*/beckonsmall <[message]>
*/blowkiss <[message]>
*/bow <[message]>
*/callme <[message]>
*/cower <[message]>
*/crazy <[message]>
*/cringe <[message]>
*/crossarms <[message]>
*/doh <[message]>
*/flinch <[message]>
*/groan <[message]>
*/kneel <[message]>
*/leanleft <[message]>
*/leanright <[message]>
*/lookaround <[message]>
*/okay <[message]>
*/overhere <[message]>
*/peer <[message]>
*/salute <[message]>
*/scratchhead <[message]>
*/shakefist <[message]>
*/shoo <[message]>
*/slouchsad <[message]>
*/stop <[message]>
*/talkhand <[message]>
*/tapfoot <[message]>
*/taunt <[message]>
*/thumbsdown <[message]>
*/thumbsdown2 <[message]>
*/thumbsup <[message]>
*/thumbsup2 <[message]>
*/wavebye <[message]>
*/wavelow <[message]>
*/winded <[message]>
*/dance2 <[message]>
*/hug
*/unhug
*/glow (locked in some ages if you don't have at least story access)
*/noglow (locked in some ages if you don't have at least story access)
*/lite <w|r|g|b> (locked in some ages if you don't have at least story access)
*/nolite (locked in some ages if you don't have at least story access)
*/suitup
*/removeki: Remove the KI from your avatar (but keep it enabled in the GU). You can get it back using the dispenser in Gahreesen.
*/removereltobook: Remove the Relto book from your avatar (but keep it enabled in the GU). You can get it back using the dispenser in Gahreesen.
*/haircolor <color>: Change the color of your hair
*/skincolor <color: Change the color of - guess what?
*/eyecolor <color>: Does what you think it does.

=== Chat commands ===

*/p <nickname> <message>: Directly send a private message to someone.
*/shout <message>
*/neighbors <message>
*/buddies <message>
*/reply: Send a private message to the person who sent you the last message.
*/startlog
*/stoplog
*/clearchat
*/addbuddy
*/removebuddy
*/ignore
*/unignore
*/me
*/my

=== Avatar warp and cheat commands ===

*/respawn or /sav or /a: Immediately move to the point you arrived at in the current age - useful if you want to avoid leaving to Relto.
*/goto <place> (locked in some ages if you don't have at least story access): Warp yourself to a predefined location in the current age. Type "/goto list" or "/goto listall" to see where you can go.
*/spawn (locked in some ages if you don't have at least story access): Warp yourself to the next spawn-point.
*/jump <height> (locked in some ages if you don't have at least story access)
*/float <[list of objects]> (locked in some ages if you don't have at least story access, the list of objects can only be used by admins): Turn off gravitation for you/the given objects. Also prevents avatars from moving!
*/nofloat <[list of objects]> (locked in some ages if you don't have at least story access, the list of objects can only be used by admins): Undo the effect of /float.
*/call <[Urwin|Monkey]> (works only in Negilahn and Payiferen): Make him appear right now!
*/rotsphere (works only in the MOUL version of Ahnonay): Rotate the spheres by one step.
*'''/reltostars''' (works only in Relto): Change the way your Relto looks in an amazing way. Looks especially great in combination with "/struct trees"!
*/noreltostars (works only in Relto): Undo the changes of "/reltostars".
*/getfissure <fissure stage (1-4)> (works only in Relto): Enable the given fissure state in your Relto.
*/bahro <name> (requires admin access): Call a Bahro. Possible names in the city: 1-6, ferry, palace, library; in the hood: shouter.
*/getzandoni (requires admin access): Enable the Zandoni in the Cleft.
*/getgzmarker (requires admin access): Collect all GZ markers (works only for callibration missions).
*/getjourneys (requires admin access): Collect all journey cloths.
*/growtree (requires admin access): Grow your Relto tree.
*/shrinktree (requires admin access): Srhink your Relto tree.
*/getyeeshapages (requires admin access): Collect all Yeesha pages.
*/getsparklies (requires admin access): Collect all Sparklies.
*/getfirstweek (requires admin access): Enable the first-week clothing in the closet.

=== Admin, age developer and control commands ===

*'''/fogcolor''' <color> or /fcol <color> (locked in some ages if you don't have at least story access): Change the color of the fog in this age (you may have to enable fog first, using /fogdensity).
*'''/fogdensity''' <start> <end> <density> or /fdens <start> <end> <density> (locked in some ages if you don't have at least story access): Specify the fog density gradient. The fog density will grow linear from 0 at the start distance to the full density at the end distance.
*/link <age filename> [<list of players>]: Link you or someone else directly to the given age (requires story access, admin access if other players should be linked)
*/linksp <age filename> <spawn point name> [<list of players>] (requires story access, admin access if other players should be linked): Like /link, but uses a specific spawn-point instead of the default one.
*/linkto <player> (requires admin access): Link yourself to the given player.
*/linkhere [<list of players>] (requires admin access): Link the given players to yourself.
*'''/autolink''' <age filename|disable> (requires admin access): Immediately link you to the given age when Uru starts - useful for age development and testing.
*/set <option name> <new value> (type "/set list" or "/set listall" to see possible options, requires admin access)
*/listsdl <[filter]> (requires admin access)
*/setsdl <varname> <value> (requires admin access): Change the given SDL value (works only for integers).
*/getsdl <varname> (requires admin access): Print the current value of the given SDL variable.
*/setpsnlsdl <varname> <value> (integer SDL values only! Requires admin access)
*/getpsnlsdl <varname> (integer SDL values only! Requires admin access)
*/console <uru console command> (requires admin access): Run Uru console commands, like those possible in fni files.
*/consolenet <uru console command> (requires admin access and works only online): Run Uru console commands for everyone in the current age.
*/loadpage <page name> (requires admin access): Load the given PRP page. Behaviour is undefined if several ages contain a page with that name.
*'''/anim''' <name of animation> <[list of players]> (requires admin access): Runs an animation on you or the given avatars. Type "/anim list" to see the pre-defined animations, but you can also directly call an animation by its name, for example "MaleBow".
*/avatar <new avatar type> (requires admin access): Change your avatar to, for example, "Yeesha" or "DrWatson" ("/avatar list" gives you a list of possible avatars).
*/name <new avatar name> (requires admin access)
*/exec <python-command> (requires admin access): Run the given python command.
*/getchron <chronicle ename> (requires admin access)
*/getversion <player name> (requires admin access)
*/about <object name> (requires admin access)
*/struct <name of a struct> <[struct mode]> (requires admin access): Build something awesome in the current age, also see "/list struct".
*/printstruct <list of objects> (requires admin access)
*/tour <tour name> <[camera name]> <[interval]> (requires admin access): Start a camera tour (see "/list tours" for a list).
*/tourstop (requires admin access): Stop the current camera tour.
*/observe <[object]> <[camera name]> <[offset for camera behind avatar]> <[camera height offset]> <[target height offset]> (requires admin access): Set up the camera behind the given object.
*/entercam <camera name> <[list of players]> (requires admin access): Let the given players view through the camera.
*/leavecam <camera name> <[list of players]> (requires admin access): The players stop viewing through the camera.
*/printcam <[camera name]> (requires admin access)

=== Flymode (requires admin access) ===

*/flymode <[list of objects]>
*/noflymode
*/xyz <relative x coordinate> <relative y coordinate> <relative z coordinate> <[list of objects]>
*/x <relative x coordinate> <[list of objects]>
*/y <relative y coordinate> <[list of objects]>
*/z <relative z coordinate> <[list of objects]>
*/hide <[list of objects]>
*/show <[list of objects]>
*/ghost <[list of objects]>
*/unghost <[list of objects]>
*/normalize <[list of objects]>
*/repos <[list of objects]>
*/location <[list of objects]>
*/warp <x coordinate> <y coordinate> <z coordinate> <[list of objects]>|<warp location> <[list of objects]>|<target object> <[list of objects]>
*/scale <scale factor> <[list of objects]>|<scale x> <scale y> <scale z> <[list of objects]>
*/rot <angle> <[axis (x|y|z)]> <[list of objects]>
*/attach <parent object> <list of child objects> (works only offline)
*/detach <parent object> <list of child objects> (works only offline)
*Esc key: Toggles flymode for the avatar
*Up arrow: Move forward
*Back arrow: Move backward
*Left arrow: Rotate left
*Right arrow: Rotate right
*Comma: Move left / Rotate counter-clockwise / Rotate backward (depending on strafe key mode which is set by F9)
*Period: Move right / Rotate clockwise / Rotate forward (depending on strafe key mode which is set by F9)
*Num-pad "-": Move up
*Num-pad "+": Move down
*Space: Move up/down alternatingly
*Shift: Move/rotate faster
*Caps lock: Accelerate move/rotation when key is hold
*Insert: Reduce linear speed
*Scroll lock: Reduce rotational speed
*F9: Toggle between Strafe, X rotation, and Y Rotation modes for strafing keys
*F10: Reset avatar's X, Y and Z axes
*F11: Reset linear and rotational speed and position recalculation rate
*F12: Increase position recalculation rate

=== Other commands ===

*/hood
*/nexus
*'''/stopcam''': Fix the camera in the current position. You can still move the avatar. This makes for some interesting pictures!
*/gocam: Let the camera move like normal again.
*/loadcolumns <filename> (works only in Jalak)
*/savecolumns <filename> (works only in Jalak)
*/export
*/import <filename> (works only offline)
*/kiusage: Show how many images, marker missions etc. are available, and how many you used up.
*/info
*/savecolumns <[filename]>
*/loadcolumns <[filename]>
*/loadscript <filename>: Load a command script.
*/loopstart <interval> <command>|<interval> <count> <command> (requires admin access): Run the command every <interval> seconds.
*/loopstop (requires admin access): Stop th currently running loop.
*/m <command 1> & <command 2> & ... & <command n> (requires admin access): Run all commands sequentially (useful to have several commands in a loop, for example).
*/checkaccess: Print your current access level.
*/enablefp: Re-enable the first-person camera (which is disabled, for example, if you improperly leave a swim region).
*/clearcam: Clear the camera stack to repair a messed-up camera (the result will be less messed-up... hopefully).
*/copy: Copy the content of the chat area to the clipboard.
*/quit
*/hideki <hide time>: Entirely hide the KI for some seconds.
*/textcolor <color>
*/ping <[player name]> (works only online)
*/createmarkerfolder
*/toggleoffline (requires story access and works only online)
*/help: Shot a book explaining all commands.
*/list <list to show>

=== Global shortcuts ===

*F1: 1st/3rd person
*F2: Open KI
*F3: Relto book
*F4:  Settings
*F5:  Take picture
*F6: Create text note
*F7: Add marker
*F8: Create new marker mission
*Ctrl+1: /wave
*Ctrl+2: /laugh
*Ctrl+3: /clap
*Ctrl+4: /dance
*Ctrl+5: Chat/talk gesture
*Ctrl+6: /sneeze
*Ctrl+7: /sit
*Shift+Ctrl: paste from clipboard (focus must be in chat line)
*Ctrl+Pause or Ctrl+Num: Run next command of file loaded using /loadscript (key may depend on keyboard layout)

=== Server-side commands (work only online) ===

(you can also use /% as prefix if you can not enter the ! character)

* /!ping
* /!resetage"""

# Helper function
def breakLine(line, firstBreak = True):
    # adds linebreaks so that each line does not exceed the maximum width. If possible, breaks at a space between words.
    width = commandWidth
    if not firstBreak: width = width-commandIndent
    if len(line) <= width: return line
    skip = 0
    i = width
    while i >= 0 and line[i] != ' ': i = i-1
    if i <= 0: i = width # have at least one character per line
    else: skip = 1 # skip the space that we are separating at
    return line[:i] + '\n' + ' '*commandIndent + breakLine(line[i+skip:], False)

def formatLine(match):
    return '\n' + breakLine(match.group(1))

def formatCommands(commands):
    # format lines
    commands = re.sub("\\n\\*([^\\n]+)", formatLine, commands)
    # format captions
    commands = re.sub("=== ([^\\n]+) ===", "<pb><%s>\\1<%s>" % (fontCaption, fontCommandText), commands)
    # format bold text (we can't make it bold, so just remove the boldness markers)
    commands = re.sub("'''([^\\n]+)'''", "\\1", commands)
    # done formatting
    return commands

# Main function
def OnCommand(ki, arg, cmnd, args, playerList, KIContent, silent):
    if (cmnd == 'help'):
        # Build help Text
        helpText = "<%s>Offline KI Help System: Syntax\n" % fontCaption
        helpText += "<%s>\n%s" % (fontText, syntax)
        helpText += formatCommands(commands)
        # show it
        global helpBook
        ki.IminiPutAwayKI()
        helpBook = ptBook(helpText, ki.key)
        helpBook.show(1)
        PtToggleAvatarClickability(0) # as we pass "ki.key" above, this is re-enabled in xKI, OnNotify
        return True
    if (cmnd == 'list'):
        (valid, listName) = xUserKI.GetArg(ki, cmnd, args, 'list to show',
            lambda args: len(args) == 1, lambda args: args[0])
        if not valid: return True
        try:
            import xUserKIData
        except:
            ki.IDoErrorChatMessage('The Offline KI data module is missing, so there are no %s available' % listName)
            return True
        # now show the list
        age = PtGetAgeName()
        lists = { 'warppoints': xUserKIData.WarpPoints,
            'tours': xUserKIData.CameraTours,
            'cameras': xUserKIData.CameraShortcuts,
            'objectlists': xUserKIData.ObjectLists,
            'structs': xUserKIData.StructLists }
        if listName in lists:
            if not silent:
                if age in lists[listName]:
                    ki.IAddRTChat(None, 'There are the following %s in this age: %s' % (listName, xUserKI.JoinList(lists[listName][age])), 0)
                else:
                    ki.IAddRTChat(None, 'There are no %s in this age' % listName, 0)
        else:
            ki.IDoErrorChatMessage('Choose one of the following lists to show: %s' % xUserKI.JoinList(lists))
        return True
    return False
