#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import config
import unicodedata

def nights_test(sentence):
    sentence1=unicodedata.normalize('NFD',sentence).encode('ascii','ignore')
    sentence2=sentence1.decode('utf-8')
    sentence_words = nltk.word_tokenize(sentence2)
    ln=len(sentence_words)
    for mot in range (0,ln):
        if sentence_words[mot]=="nuits" or sentence_words[mot] =="nuit":
            res=sentence_words[mot-1]
    return res

def personnes_test(sentence):
    sentence1=unicodedata.normalize('NFD',sentence).encode('ascii','ignore')
    sentence2=sentence1.decode('utf-8')
    sentence_words = nltk.word_tokenize(sentence2)
    ln=len(sentence_words)
    for mot in range (0,ln):
        if sentence_words[mot]=="personne" or sentence_words[mot] =="personnes":
            res=sentence_words[mot-1]
    return res
