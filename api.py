#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

CLIENT_ACCESS_TOKEN = config.api_client_token
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)


def api_message(text,user_id):
    request = ai.text_request()

    request.lang = 'fr'  # optional, default value equal 'en'

    request.session_id = user_id

    request.query = text

    response = request.getresponse()
    resau=response.read().decode('utf-8')
    res=json.loads(resau)
    #res=resau.decode('utf8').replace("'",'"')

    #data=json.loads(res)
    #s=json.dumps(data,indent=4,sort_keys=True)

    print (res['result']['fulfillment'])
    return "ok"
