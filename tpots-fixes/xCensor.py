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
from ptWordFilter import *
import xLocalization
SpecialPunctuation = '#$%&*+-@_|~'
SentenceFilters = xLocalization.xCensor.xSentenceFilters

def xCensor(sentence, censorLevel):
    return sentence


def xWhatRating(sentence):
    rated = xRatedG
    for sfilter in SentenceFilters:
        thisRating = sfilter.test(sentence)
        if (thisRating > rated):
            rated = thisRating
    return rated



