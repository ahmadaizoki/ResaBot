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
