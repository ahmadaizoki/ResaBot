#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import calendar
import config
import datetime
import unicodedata
import time
import os
import sys

def analyse_date(sentence):
    sentence1=unicodedata.normalize('NFD',sentence).encode('ascii','ignore')
    sentence2=sentence1.decode('utf-8')
    sentence_words = nltk.word_tokenize(sentence2)
    print (sentence_words)
    time_loc=time.localtime()
    tm_year=time_loc.tm_year
    for mot1 in sentence_words:
        if mot1=="premier":
            i=1
            break
        elif mot1=="deuxieme":
            i=2
            break
        elif mot1=="troisieme":
            i=3
            break
        elif mot1=="quatrieme":
            i=4
            break
        elif mot1=="cinquieme":
            i=5
            break
    for mot2 in sentence_words:
        if mot2=="janvier":
            m=1
            break
        elif mot2=="fevrier":
            m=2
            break
        elif mot2=="mars":
            m=3
            break
        elif mot2=="avril":
            m=4
            break
        elif mot2=="mai":
            m=5
            break
        elif mot2=="juin":
            m=6
            break
        elif mot2=="juillet":
            m=7
            break
        elif mot2=="aout":
            m=8
            break
        elif mot2=="septembre":
            m=9
            break
        elif mot2=="octobre":
            m=10
            break
        elif mot2=="novembre":
            m=11
            break
        elif mot2=="decembre":
            m=12
            break
    cal=calendar.monthcalendar(tm_year,m)
    re=0
    for mot3 in sentence_words:
        for j in range(0,len(cal)):
            if mot3=="lundi":
                if cal[j][calendar.MONDAY]:
                    day=cal[j][calendar.MONDAY]
                    re=re+1
                else:
                    re=re
                if re==i:
                    break
            elif mot3=="mardi":
                if cal[j][calendar.TUESDAY]:
                    day=cal[j][calendar.TUESDAY]
                    re=re+1
                else:
                    re=re
                if re==i:
                    break
            elif mot3=="mercredi":
                if cal[j][calendar.WEDNESDAY]:
                    day=cal[j][calendar.WEDNESDAY]
                    re=re+1
                else:
                    re=re
                if re==i:
                    break
            elif mot3=="jeudi":
                if cal[j][calendar.THURSDAY]:
                    day=cal[j][calendar.THURSDAY]
                    re=re+1
                else:
                    re=re
                if re==i:
                    break
            elif mot3=="vendredi":
                if cal[j][calendar.FRIDAY]:
                    day=cal[j][calendar.FRIDAY]
                    re=re+1
                else:
                    re=re
                if re==i:
                    break
            elif mot3=="samedi" or mot3=="week-end" or mot3=="weekend":
                if cal[j][calendar.SATURDAY]:
                    day=cal[j][calendar.SATURDAY]
                    re=re+1
                else:
                    re=re
                if re==i:
                    break
            elif mot3=="dimanche":
                if cal[j][calendar.SUNDAY]:
                    day=cal[j][calendar.SUNDAY]
                    re=re+1
                else:
                    re=re
                if re==i:
                    break
    date=datetime.date(tm_year,m,day)
    return str(date)
