#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import unicodedata

#pour découper la phrase en mots.
def analyse(sentence):
    sentence1=unicodedata.normalize('NFD',sentence).encode('ascii','ignore')
    sentence2=sentence1.decode('utf-8')
    sentence_words = nltk.word_tokenize(sentence2)
    return sentence_words[0]
