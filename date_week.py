#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

def date_week():
    d=datetime.datetime.today()
    dd=d.weekday()
    if dd==0:
        ddd=5
    elif dd==1:
        ddd=4
    elif dd==2:
        ddd=3
    elif dd==3:
        ddd=2
    elif dd==4:
        ddd=1
    elif dd==5:
        ddd=0
    else:
        ddd=6
    return ddd