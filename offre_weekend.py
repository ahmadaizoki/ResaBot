#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
import config
import requests
import json
import psycopg2

try:
    conn=psycopg2.connect(config.db_url)
except:
    print ("echec de connexion")
rows=[]
cur=conn.cursor()
try:
    cur.execute("""SELECT * FROM offre WHERE id=2""")
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
    rate=rows[0][7]
except:
    nbDays=""
    nbNMax=""
    nbNMin=""
    dayIn=""
    dayOut=""
    nom_offre=""
    print ("erreur de connexion")

#gérer la deuxième offre.
def offre_we(dateIn,dateOut,nights,adults):
    res_in=requests.get("https://websdk.fastbooking-services.com/quotation/?arrivalDate="+dateIn+"&rate="+""+"&nights="+nights+"&adults="+adults+"&property="+config.HID+"&output="+"json"+"&accessCode="+""+"&_authCode="+config.H_Access_Token)
    res_in=res_in.json()
    price_in=res_in["data"][0]["totalPrice"]
    means_in=int(price_in)/int(nights)
    rate_in=res_in["data"][0]["rate"]
    res_out=requests.get("https://websdk.fastbooking-services.com/quotation/?arrivalDate="+dateOut+"&rate="+""+"&nights="+"2"+"&adults="+adults+"&property="+config.HID+"&output="+"json"+"&accessCode="+""+"&_authCode="+config.H_Access_Token)
    res_out=res_out.json()
    price_out=res_out["data"][0]["totalPrice"]
    means_out=int(price_out)/2
    rate_out=res_out["data"][0]["rate"]
    if (means_out/means_in)>rate:
        if rate_out==rate_in:
            nights=str(int(nights)+2)
            res=requests.get("https://websdk.fastbooking-services.com/quotation/?arrivalDate="+dateIn+"&rate="+""+"&nights="+nights+"&adults="+adults+"&property="+config.HID+"&output="+"json"+"&accessCode="+""+"&_authCode="+config.H_Access_Token)
            resulta=res.json()
            q_from=resulta["data"][0]["bookingParams"]["from"]
            q_to=resulta["data"][0]["bookingParams"]["to"]
            q_nights=resulta["data"][0]["nights"]
            q_adults=resulta["data"][0]["adults"]
            q_price=resulta["data"][0]["totalPrice"]
            q_currency=resulta["data"][0]["currency"]
            q_BookLink=resulta["data"][0]["plainBookLink"]
            q_room=resulta["data"][0]["room"]
            return (q_from,q_to,q_nights,q_adults,q_price,q_currency,q_BookLink,q_room)
        else:
            res_in=res_in
            q_from_in=res_in["data"][0]["bookingParams"]["from"]
            q_to_in=res_in["data"][0]["bookingParams"]["to"]
            q_nights_in=res_in["data"][0]["nights"]
            q_adults_in=res_in["data"][0]["adults"]
            q_price_in=res_in["data"][0]["totalPrice"]
            q_currency_in=res_in["data"][0]["currency"]
            q_BookLink_in=res_in["data"][0]["plainBookLink"]
            q_room_in=res_in["data"][0]["room"]
            res_out=res_out
            q_from_out=res_out["data"][0]["bookingParams"]["from"]
            q_to_out=res_out["data"][0]["bookingParams"]["to"]
            q_nights_out=res_out["data"][0]["nights"]
            q_adults_out=res_out["data"][0]["adults"]
            q_price_out=res_out["data"][0]["totalPrice"]
            q_currency_out=res_out["data"][0]["currency"]
            q_BookLink_out=res_out["data"][0]["plainBookLink"]
            q_room_out=res_out["data"][0]["room"]
            return (q_from_in,q_to_in,q_nights_in,q_adults_in,q_price_in,q_currency_in,q_BookLink_in,q_room_in,q_from_out,q_to_out,q_nights_out,q_adults_out,q_price_out,q_currency_out,q_BookLink_out,q_room_out)
    else:
        return ""
