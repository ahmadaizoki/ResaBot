#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################
#les packages et les framework
import os.path
import sys
import config
import json
import date as dd
import date_week

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

################################################
#la connexion avec API.AI
CLIENT_ACCESS_TOKEN = config.api_client_token #CLIENT_ACCESS_TOKEN de API.AI
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

###############################################
#detecter l'intention de API.AI
def api_message(text,user_id):
    request = ai.text_request()
    request.lang = 'fr'
    request.session_id = user_id
    request.query = text
    response = request.getresponse()
    resau=response.read().decode('utf-8')
    res=json.loads(resau)
    speech=res['result']['fulfillment']['speech']
    intention=res['result']['action']
    if intention=="h_dispo":
        date=res['result']['parameters']['date']
        nights=res['result']['parameters']['nbnight']
        adults=res['result']['parameters']['nbpax']
        if date in config.date0:
            date=dd.time_calc(0)
        elif date in config.date1:
            date=dd.time_calc(1)
        elif date in config.date2:
            date=dd.time_calc(2)
        #elif date in date_week_end:
        #    ddd=date_week.date_week()
        #    date=dd.time_calc(ddd)
        else:
            date=res['result']['parameters']['date']
        print ([speech]+[intention]+[date]+[nights]+[adults])
        return ([speech]+[intention]+[date]+[nights]+[adults])
    else:
        print (speech,intention)
        return ([speech]+[intention])
