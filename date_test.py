#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime

#tester si la date est française ou anglaise puis le mettre dans le type anglaise.
def test(date):
    date=date_split(date)
    try:
        time.strptime(date,'%Y-%m-%d')
        date=date
    except:
        try:
            time.strptime(date,'%d-%m-%Y')
            d=date.split("-")
            date=str(d[2])+"-"+str(d[1])+"-"+str(d[0])
            date=datetime.date(int(d[2]),int(d[1]),int(d[0]))
        except:
            date=date
    return str(date)
#remplacer les / dans la date par -
def date_split(date):
    try:
        d=date.split("/")
        date=d[0]+"-"+d[1]+"-"+d[2]
    except:
        date=date
    return str(date)
