# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#    See the file AUTHORS for more info about the contributors.                #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                      #
#                                                                              #
#    You may re-use the code in this file within the context of Uru.           #
#                                                                              #
#==============================================================================#
class ClimbAction:
    """Possible actions when climbing
This does not mean only climbing, but might also be used by regions, that's why they can all be added (except climb)."""
    def __init__(self):
        pass

    probe    = 0
    mount    = 1
    dismount = 2
    fallOff  = 4
    release  = 8
    idle     = 16


class ClimbDirection:
    """Possible directions when climbing (x, y, -x, -y)
Also used by regions, that's why it can be added again."""
    def __init__(self):
        pass

    up		= 1
    down	= 2
    left	= 4
    right   = 8