#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

#le nombre de jours entre aujourd'hui et samedi prochain.
def date_week():
    d=datetime.datetime.today()
    dd=d.weekday()
    if dd==0:
        ddd=4
    elif dd==1:
        ddd=3
    elif dd==2:
        ddd=2
    elif dd==3:
        ddd=1
    elif dd==4:
        ddd=0
    elif dd==5:
        ddd=6
    else:
        ddd=5
    return ddd
