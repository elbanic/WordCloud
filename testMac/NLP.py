__author__ = 'ejjeong'

import nltk
from konlpy.tag import Twitter
from nltk import regexp_tokenize

class NLP:

    def __init__(self):
        return

    def generateWCData(self, str):
        pattern = r'''(?x) ([A-Z]\.)+ | \w+(-\w+)* | \$?\d+(\.\d+)?%? | \.\.\. | [][.,;"'?():-_`]'''
        tokens_en = regexp_tokenize(str, pattern)
        en = nltk.Text(tokens_en)
        data = en.vocab()
        '''
        t = Twitter()
        tokens_ko = t.morphs(text)
        ko = nltk.Text(tokens_ko, text)
        print(ko.vocab())
        data = ko.vocab().items()
        print(data)
        print(type(data))
        '''
        return data

