#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys
import config
import json
import requests

def get_offers(output,property,orderBy,locale,currency,_authcode):
    res=requests.get("https://websdk.fastbooking-services.com/offers/?output="+output+"&property="+property+"&orderBy="+orderBy+"&locale="+locale+"&currency="+currency+"&_authCode="+_authcode)
    print (res.json())

def get_gallery(property,locale,_authcode):
    res=requests.get("https://websdk.fastbooking-services.com/gallery/?property="+property+"&locale="+locale+"&_authCode="+_authcode)
    resulta=res.json()
    ln=len(resulta["data"])
    ulr=[]
    alt=[]
    for i in range(0,ln):
        url=url+[resulta["data"][i]["full"]["url"]]
        alt=alt+[resulta["data"][i]["full"]["alt"]]
    print (url,alt)
    print (ln)
