# -*- coding: utf-8 -*-
import sys
import traceback
import json
import base64
import requests
import string
from imp import reload
import api
import fbweb
from fbmq import Attachment, Template, QuickReply, Page

reload(sys)


from flask import Flask, request
import config as conf
page = Page(conf.fb_access_token)

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
                try:
                    user_id="{sender[id]}".format(**message)
                    text="{message[text]}".format(**message)
                    res=api.api_message(text,user_id)
                    speech=res[0]
                    intention=res[1]
                    if intention=="gallery":
                        url=fbweb.get_gallery(conf.HID,"it_IT",conf.H_Access_Token)[0]
                        alt=fbweb.get_gallery(conf.HID,"it_IT",conf.H_Access_Token)[1]
                        ln=len(url)
                        print (url)
                        print (alt)
                        #template=Template.Generic([])
                        for i in range (0,ln):
                            Template.Generic([
                                Template.GenericElement("Gallery",
                                  item_url=url[i],
                                  image_url=url[i],
                                  subtitle=alt[i]
                                )
                            ])
                        page.send(user_id,Template.Generic)
                        #client.send_text(user_id,"speech")
                    else:
                        client.send_text(user_id,speech)
                except:
                    client.send_text(user_id,conf.message_data_null)

    return "Ok"

########################################################################
if __name__ == '__main__':
    app.run()
