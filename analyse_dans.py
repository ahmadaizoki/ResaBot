#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import unicodedata
import os
import sys
import date as dd
import time
import datetime

def analyse_sentence(sentence):
    sentence1=unicodedata.normalize('NFD',sentence).encode('ascii','ignore')
    sentence2=sentence1.decode('utf-8')
    sentence_words = nltk.word_tokenize(sentence2)
    for mot1 in sentence_words:
        if mot1=="un" or mot1=="1":
            day=1
        elif mot1=="deux" or mot1=="2":
            day=2
        elif mot1=="trois" or mot1=="3":
            day=3
        elif mot1=="quatre" or mot1=="4":
            day=4
        elif mot1=="cinq" or mot1=="5":
            day=5
        elif mot1=="six" or mot1=="6":
            day=6
        elif mot1=="sept" or mot1=="7":
            day=7
        elif mot1=="huit" or mot1=="8":
            day=8
        elif mot1=="neuf" or mot1=="9":
            day=9
        elif mot1=="dix" or mot1=="10":
            day=10
        elif mot1=="onze" or mot1=="11":
            day=11
        elif mot1=="douze" or mot1=="12":
            day=12
        elif mot1=="treize" or mot1=="13":
            day=13
        elif mot1=="quatorze" or mot1=="14":
            day=14
        elif mot1=="quinze" or mot1=="15":
            day=15
        elif mot1=="seize" or mot1=="16":
            day=16
        elif mot1=="dix-sept" or mot1=="17":
            day=17
        elif mot1=="dix-huit" or mot1=="18":
            day=18
        elif mot1=="dix-neuf" or mot1=="19":
            day=19
        elif mot1=="vingt" or mot1=="20":
            day=20
    for mot2 in sentence_words:
        if mot2=="jour" or mot2=="jours":
            res=dd.time_calc(day)
        elif mot2=="mois":
            time_loc=time.localtime()
            tm_year=time_loc.tm_year
            tm_mon=time_loc.tm_mon+day
            tm_mday=time_loc.tm_mday
            if tm_mon>12:
                tm_mon=tm_mon%12
                tm_year=tm_year+1
            else:
                tm_mon=tm_mon
            try:
                res=datetime.date(tm_year,tm_mon,tm_mday)
            except:
                res=datetime(tm_year,tm_mon,30)
    return res
