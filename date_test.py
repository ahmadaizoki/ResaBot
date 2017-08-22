#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime

def test(date):
    date=str(date)
    try:
        time.strptime(date,'%Y-%m-%d')
        date=date
    except:
        try:
            time.strptime(date,'%d-%m-%Y')
            d=date.split("-")
            date=str(d[2])+"-"+str(d[1])+"-"+str(d[0])
            date=datetime.date(int(d[2]),int(d[1]),int(d[0]))
            print (date)
            print (d[0])
        except:
            date=date
    print (date)
    return str(date)

test("10-10-2017")
