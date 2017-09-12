#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
import psycopg2
import config

try:
    conn=psycopg2.connect(config.db_url)
except:
    print ("echec de connexion")
rows=[]
cur=conn.cursor()

def offre(dateIn,dateOut,nights):
    dateIN=dateIn.split('-')
    dateOUT=dateOut.split('-')
    duree=datetime(int(dateIN[0]),int(dateIN[1]),int(dateIN[2]))-datetime.now()
    ansIN=datetime(int(dateIN[0]),int(dateIN[1]),int(dateIN[2]))
    dayIN=ansIN.strftime('%A').lower()
    ansOUT=datetime(int(dateOUT[0]),int(dateOUT[1]),int(dateOUT[2]))
    dayOUT=ansOUT.strftime('%A').lower()
    if dayIN=="monday":
        dayIN="lundi"
    elif dayIN=="tuesday":
        dayIN="mardi"
    elif dayIN=="wednesday":
        dayIN="mercredi"
    elif dayIN=="thursday":
        dayIN="jeudi"
    elif dayIN=="friday":
        dayIN="vendredi"
    elif dayIN=="saturday":
        dayIN="samedi"
    elif dayIN=="sunday":
        dayIN="dimanche"
    else:
        return (["",nom_offre])
    if dayOUT=="monday":
        dayOUT="lundi"
    elif dayOUT=="tuesday":
        dayOUT="mardi"
    elif dayOUT=="wednesday":
        dayOUT="mercredi"
    elif dayOUT=="thursday":
        dayOUT="jeudi"
    elif dayOUT=="friday":
        dayOUT="vendredi"
    elif dayOUT=="saturday":
        dayOUT="samedi"
    elif dayOUT=="sunday":
        dayOUT="dimanche"
    else:
        return (["",nom_offre])
    print (dayIN,dayOUT)
    dayIN=str(dayIN)
    try:
        cur.execute("""SELECT * FROM offre WHERE dayn=%(dayIN)s AND dayt=%(dayOUT)s""",{"dayIN":dayIN,"dayOUT":dayOUT})
        rows=cur.fetchall()
    except:
        print ("erreur connexion")
    if rows==[]:
        try:
            cur.execute("""SELECT * FROM offre WHERE dayt=%(dayOUT)s""",{"dayOUT":dayOUT})
            rows=cur.fetchall()
        except:
            print ("erreur connexion")
    if rows==[]:
        try:
            cur.execute("""SELECT * FROM offre WHERE dayn=%(dayIN)s """,{"dayIN":dayIN})
            rows=cur.fetchall()
        except:
            print ("erreur connexion")
    try:
        nbDays=rows[0][1]
        nbNMax=rows[0][2]
        nbNMin=rows[0][3]
        dayIn=rows[0][4]
        dayOut=rows[0][5]
        nom_offre=rows[0][6]
    except:
        nbDays=""
        nbNMax=""
        nbNMin=""
        dayIn=""
        dayOut=""
        nom_offre=""
        print ("erreur de connexion")
        return ""
    nights=int (nights)
    if duree.days>=nbDays:
        if nbNMax>=nights and nights>=nbNMin:
            return nom_offre
    else:
        return ""
