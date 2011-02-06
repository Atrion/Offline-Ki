# -*- coding: utf-8 -*-
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



