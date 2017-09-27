  # -*- coding: utf-8 -*-
import time
import datetime
import date

#calculerla date pour (aujourd'hui ,aujourd'hui+7,aujourd'hui+14,aujourd'hui-7,aujourd'hui_14).
def date_offre(date):
    dd=date.split('-')
    year=int(dd[0])
    month=int(dd[1])
    day=int(dd[2])
    date0=date
    day7=day+7
    day14=day+14
    day_7=day-7
    day_14=day-14
    if (month in [1,3,5,7,8,10,12]):
        if day7>31:
            day7=day7%31
            mon7=month+1
        else:
            day7=day7
            mon7=month
        if day14>31:
            day14=day14%31
            mon14=month+1
        else:
            day14=day14
            mon14=month
    elif month==2:
        if year%4==0:
            if day7>29:
                day7=day7%29
                mon7=month+1
            else:
                day7=day7
                mon7=month
            if day14>29:
                day14=day14%29
                mon14=month+1
            else:
                day14=day14
                mon14=month
        else:
            if day7>28:
                day7=day7%28
                mon7=month+1
            else:
                day7=day7
                mon7=month
            if day14>28:
                day14=day14%28
                mon14=month+1
            else:
                day14=day14
                mon14=month
    else:
        if day7>30:
            day7=day7%30
            mon7=month+1
        else:
            day7=day7
            mon7=month
        if day14>30:
            day14=day14%30
            mon14=month+1
        else:
            day14=day14
            mon14=month
    if mon7>12:
        mon7=mon7%12
        year7=year+1
    else:
        mon7=mon7
        year7=year
    if mon14>12:
        mon14=mon14%12
        year14=year+1
    else:
        mon14=mon14
        year14=year
    if day_7>0:
        day_7=day_7
        mon_7=month
        year_7=year
    else:
        if month==3:
            if year%4==0:
                day_7=29+day_7
                mon_7=month-1
            else:
                day_7=28+day_7
                mon_7=month-1
        elif (month in [5,7,10,12]):
            day_7=30+day_7
            mon_7=month-1
        else:
            day_7=31+day_7
            mon_7=month-1
    if day_14>0:
        day_14=day_14
        mon_14=month
        year_14=year
    else:
        if month==3:
            if year%4==0:
                day_14=29+day_14
                mon_14=month-1
            else:
                day_14=28+day_14
                mon_14=month-1
        elif (month in [5,7,10,12]):
            day_14=30+day_14
            mon_14=month-1
        else:
            day_14=31+day_14
            mon_14=month-1
    if mon_7==0:
        mon_7=1
        year_7=year-1
    else:
        mon_7=mon_7
        year_7=year
    if mon_14==0:
        mon_14=1
        year_14=year-1
    else:
        mon_14=mon_14
        year_14=year
    date7=datetime.date(year7,mon7,day7)
    date14=datetime.date(year14,mon14,day14)
    date_7=datetime.date(year_7,mon_7,day_7)
    date_14=datetime.date(year_14,mon_14,day_14)
    date_off=[date0,str(date7),str(date14),str(date_7),str(date_14)]
    return (date_off)
