#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################
#les packages et les framework
import os.path
import sys
import config
import json
import fbweb

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
    try:
        if intention=="gallery":
            fbweb.get_gallery(config.HID,"it_IT",config.H_Access_Token)
            return ([speech]+[intention])
        else:
            return ([speech]+[intention])
    except:
        print (speech,intention)
        return ([speech]+[intention])
