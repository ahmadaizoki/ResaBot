#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys
import config
import json
import requests

def get_offers(output,property,orderBy,locale,currency,_authcode):
    res=requests.get("https://websdk.fastbooking-services.com/offers/?output="+output+"&property="+property+"&orderBy="+orderBy+"&locale="+locale+"&currency="+currency+"&_authCode="+_authcode)
    resulta=res.json()
    ln=len(resulta["data"]["rates"])
    url=[]
    title=[]
    q_from=[]
    q_to=[]
    q_price=[]
    q_currency=[]
    q_BookLink=[]
    for i in range (0,ln):
        url=url+[resulta["data"]["rates"][i]["rate"]["image"]["url"]]
        title=title+[resulta["data"]["rates"][i]["rate"]["title"]]
        q_from=q_from+[resulta["data"]["rates"][i]["quotation"]["bookingParams"]["from"]]
        q_to=q_to+[resulta["data"]["rates"][i]["quotation"]["bookingParams"]["to"]]
        q_price=q_price+[resulta["data"]["rates"][i]["quotation"]["totalPrice"]]
        q_currency=q_currency+[resulta["data"]["rates"][i]["quotation"]["currency"]]
        q_BookLink=q_BookLink+[resulta["data"]["rates"][i]["quotation"]["plainBookLink"]]
    return (url,title,q_from,q_to,q_price,q_currency,q_BookLink)

def get_gallery(property,locale,_authcode):
    res=requests.get("https://websdk.fastbooking-services.com/gallery/?property="+property+"&locale="+locale+"&_authCode="+_authcode)
    resulta=res.json()
    ln=len(resulta["data"])
    url=[]
    alt=[]
    for i in range(0,ln):
        url=url+[resulta["data"][i]["full"]["url"]]
        alt=alt+[resulta["data"][i]["full"]["alt"]]
    return (url,alt)

def get_quotation(arrivalDate,rate,nights,adults,property,output,accessCode,_authCode):
    res=requests.get("https://websdk.fastbooking-services.com/quotation/?arrivalDate="+arrivalDate+"&rate="+rate+"&nights="+nights+"&adults="+adults+"&property="+property+"&output="+output+"&accessCode="+accessCode+"&_authCode="+_authCode)
    resulta=res.json()
    print (resulta)

get_quotation("2017-10-28","Offerta1","2","2","itven27534","json","private-rate-code","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOiJeLiokIiwicHJvcGVydGllcyI6Il5pdHZlbjI3NTM0JCIsImdyb3VwcyI6Il4kIiwiZm9yIjoiZ2VuLXVzZXIiLCJpYXQiOjE1MDE4NTI3NzAsImp0aSI6IjYzODIxYWEyLTRmZDgtNGMzMS1hMDRjLTUyMzM4OTc5ZDUwMyJ9.QWO340YC4jjBXZT2wcW9ThtCg-mJf9EF_FHZPiDEgjA")
