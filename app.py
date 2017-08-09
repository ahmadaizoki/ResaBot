# -*- coding: utf-8 -*-
import sys
import traceback
import json
import base64
import requests
import string
from imp import reload
import api

reload(sys)


from flask import Flask, request
import config as conf

app = Flask(__name__)


#########################################################################
#facebook bot

from pymessager.message import Messager
client=Messager(conf.fb_access_token)

@app.route('/webhook', methods=["GET"])
def fb_webhook():
    verification_code = conf.fb_verifing_token
    verify_token = request.args.get('hub.verify_token')
    if verification_code == verify_token:
        return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        for message in entry['messaging']:
            if message.get('message'):
                user_id="{sender[id]}".format(**message)
                text="{message[text]}".format(**message)
                res=api.api_message(text,user_id)
                client.send_text(user_id,res)

    return "Ok"

########################################################################
if __name__ == '__main__':
    app.run()
