#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string


def strip_punctuation(name):
    '''
    Strips any unauthorized punctuation from user input in the following steps:
    1. Makes unauthorized punctuation list of string.punctuation
    2. Removes any allowed punctuation from  unauthorized punctuation list.
    3. Creates translation map for removing any unauthorized punctuation.
    4. Returns translated string with removed unauthorized punctuation.
    '''
    punc_input = ''.join(name.split())
    punc_key = [punctuation for punctuation in string.punctuation]
    allowed_punc = [punc_key.remove(
        punc)for punc in punc_key if punc == '_' or punc == '-']
    translator = str.maketrans('', '', str(punc_key))
    return punc_input.translate(translator)
