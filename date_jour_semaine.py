#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

def jour_prochain(sentence):
    d=datetime.datetime.today()
    dd=d.weekday()
    if sentence=="lundi prochain" or sentence=="prochain lundi":
        if dd==0:
            res=7
        else:
            res=(7-dd+0)%7
    elif sentence=="mardi prochain" or sentence=="prochain mardi":
        if dd==1:
            res=7
        else:
            res=(7-dd+1)%7
    elif sentence=="mercredi prochain" or sentence=="prochain mercredi":
        if dd==2:
            res=7
        else:
            res=(7-dd+2)%7
    elif sentence=="jeudi prochain" or sentence=="prochain jeudi":
        if dd==3:
            res=7
        else:
            res=(7-dd+3)%7
    elif sentence=="vendredi prochain" or sentence=="prochain vendredi":
        if dd==4:
            res=7
        else:
            res=(7-dd+4)%7
    elif sentence=="samedi prochain" or sentence=="prochain samedi":
        if dd==5:
            res=7
        else:
            res=(7-dd+5)%7
    elif sentence=="dimanche prochain" or sentence=="prochain dimanche":
        if dd==6:
            res=7
        else:
            res=(7-dd+6)%7
    return res
