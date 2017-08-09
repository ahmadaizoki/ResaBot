#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import config

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = config.api_client_token


def api_message(text,user_id):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'fr'  # optional, default value equal 'en'

    request.session_id = user_id

    request.query = text

    response = request.getresponse()
    res=response.read()

    print (res['id'])
    return res['id']
