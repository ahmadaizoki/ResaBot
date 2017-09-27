#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

#calculer la date des phrases de type (lundi prochain) par exemple.
def jour_prochain(sentence):
    d=datetime.datetime.today()
    dd=d.weekday()
    if sentence=="lundi prochain" or sentence=="prochain lundi" or sentence=="pour lundi prochain" or sentence=="pour prochain lundi" or sentence=="lundi":
        if dd==0:
            res=7
        else:
            res=(7-dd+0)%7
    elif sentence=="mardi prochain" or sentence=="prochain mardi" or sentence=="pour mardi prochain" or sentence=="pour prochain mardi" or sentence=="mardi":
        if dd==1:
            res=7
        else:
            res=(7-dd+1)%7
    elif sentence=="mercredi prochain" or sentence=="prochain mercredi" or sentence=="pour mercredi prochain" or sentence=="pour prochain mercredi" or sentence=="mercredi":
        if dd==2:
            res=7
        else:
            res=(7-dd+2)%7
    elif sentence=="jeudi prochain" or sentence=="prochain jeudi"or sentence=="pour jeudi prochain" or sentence=="pour prochain jeudi" or sentence=="jeudi":
        if dd==3:
            res=7
        else:
            res=(7-dd+3)%7
    elif sentence=="vendredi prochain" or sentence=="prochain vendredi" or sentence=="pour vendredi prochain" or sentence=="pour prochain vendredi" or sentence=="vendredi":
        if dd==4:
            res=7
        else:
            res=(7-dd+4)%7
    elif sentence=="samedi prochain" or sentence=="prochain samedi" or sentence=="pour samedi prochain" or sentence=="pour prochain samedi" or sentence=="samedi":
        if dd==5:
            res=7
        else:
            res=(7-dd+5)%7
    elif sentence=="dimanche prochain" or sentence=="prochain dimanche" or sentence=="pour dimanche prochain" or sentence=="pour prochain dimanche" or sentence=="dimanche":
        if dd==6:
            res=7
        else:
            res=(7-dd+6)%7
    elif sentence=="lundi en 8" or sentence=="lundi en huit" or sentence=="pour lundi en 8" or sentence=="pour lundi en huit":
        if dd==0:
            res=14
        else:
            res=(7-dd+0)%7+7
    elif sentence=="mardi en 8" or sentence=="mardi en huit" or sentence=="pour mardi en 8" or sentence=="pour mardi en huit":
        if dd==1:
            res=14
        else:
            res=(7-dd+1)%7+7
    elif sentence=="mercredi en 8" or sentence=="mercredi en huit" or sentence=="pour mercredi en 8" or sentence=="pour mercredi en huit":
        if dd==2:
            res=14
        else:
            res=(7-dd+2)%7+7
    elif sentence=="jeudi en 8" or sentence=="jeudi en huit" or sentence=="pour jeudi en 8" or sentence=="pour jeudi en huit":
        if dd==3:
            res=14
        else:
            res=(7-dd+3)%7+7
    elif sentence=="vendredi en 8" or sentence=="vendredi en huit" or sentence=="pour vendredi en 8" or sentence=="pour vendredi en huit":
        if dd==4:
            res=14
        else:
            res=(7-dd+4)%7+7
    elif sentence=="samedi en 8" or sentence=="samedi en huit" or sentence=="pour samedi en 8" or sentence=="pour samedi en huit":
        if dd==5:
            res=14
        else:
            res=(7-dd+5)%7+7
    elif sentence=="dimanche en 8" or sentence=="dimanche en huit" or sentence=="pour dimanche en 8" or sentence=="pour dimanche en huit":
        if dd==6:
            res=14
        else:
            res=(7-dd+6)%7+7
    return res
