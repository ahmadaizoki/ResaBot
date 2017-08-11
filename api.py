#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################
#les packages et les framework
import os.path
import sys
import config
import json

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
        print ([speech]+[intention]+[date]+[nights]+[adults])
        return ([speech]+[intention]+[date]+[nights]+[adults])
    else:
        print (speech,intention)
        return ([speech]+[intention])
