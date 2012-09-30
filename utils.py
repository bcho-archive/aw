#coding: utf-8

from string import expandtabs


TAB_WIDTH = 4

    
def real_len(l, tw=TAB_WIDTH):
    '''Calculate the real length of a word with a tab
    :param l: length of the word
    :param tw: tab width'''
    return tw - l % tw + l


def expand(s, width, tw=TAB_WIDTH):
    '''Expand the tab'''
    #: use aleast one tab
    if width == len(s):
        tab = '\t'
    else:
        tab = '\t' * (1 + (width - real_len(len(s), tw)) / tw)
    return expandtabs('\t%s%s' % (s, tab), tw)
