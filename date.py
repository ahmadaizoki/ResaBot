#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime

def time_calc(day):
    time_loc=time.localtime()
    tm_year=time_loc.tm_year
    tm_mon=time_loc.tm_mon
    tm_mday=time_loc.tm_mday+day
    if (tm_mon in [1,3,5,7,8,10,12]):
        if tm_mday>31:
            tm_mday=tm_mday%31
            tm_mon=tm_mon+1
        else:
            tm_mday=tm_mday
    elif tm_mon==2:
        if tm_year%4==0:
            if tm_mday>29:
                tm_mday=tm_mday%29
                tm_mon=tm_mon+1
            else:
                tm_mday=tm_mday
        else:
            if tm_mday>28:
                tm_mday=tm_mday%28
                tm_mon=tm_mon+1
            else:
                tm_mday=tm_mday
    else:
        if tm_mday>30:
            tm_mday=tm_mday%30
            tm_mon=tm_mon+1
        else:
            tm_mday=tm_mday
    if tm_mon>12:
        tm_mon=tm_mon%12
        tm_year=tm_year+1
    else:
        tm_mon=tm_mon
    date=datetime.date(tm_year,tm_mon,tm_mday)
    return str(date)
