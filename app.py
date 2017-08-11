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
                        template=[]
                        if ln>10:
                            for i in range (0,10):
                                template=template+[Template.GenericElement("Gallery",
                                item_url=url[i],
                                image_url=url[i],
                                subtitle=alt[i])]
                        else:
                            for i in range (0,ln):
                                template=template+[Template.GenericElement("Gallery",
                                item_url=url[i],
                                image_url=url[i],
                                subtitle=alt[i])]
                        page.send(user_id,Template.Generic(template))
                    elif intention=="offres":
                        url=fbweb.get_offers("json",conf.HID,"totalPrice","en_GB","EUR",conf.H_Access_Token)[0]
                        title=fbweb.get_offers("json",conf.HID,"totalPrice","en_GB","EUR",conf.H_Access_Token)[1]
                        q_from=fbweb.get_offers("json",conf.HID,"totalPrice","en_GB","EUR",conf.H_Access_Token)[2]
                        q_to=fbweb.get_offers("json",conf.HID,"totalPrice","en_GB","EUR",conf.H_Access_Token)[3]
                        q_price=fbweb.get_offers("json",conf.HID,"totalPrice","en_GB","EUR",conf.H_Access_Token)[4]
                        q_currency=fbweb.get_offers("json",conf.HID,"totalPrice","en_GB","EUR",conf.H_Access_Token)[5]
                        q_BookLink=fbweb.get_offers("json",conf.HID,"totalPrice","en_GB","EUR",conf.H_Access_Token)[6]
                        ln=len(url)
                        template=[]
                        if ln>10:
                            for i in range (0,10):
                                template=template+[Template.GenericElement(title[i],
                                item_url=url[i],
                                image_url=url[i],
                                subtitle="DU "+q_from[i]+" au "+q_to[i],
                                #text="Reserver a partir de "+q_price[i]+" "+q_currency[i],
                                buttons=[
                                Template.ButtonWeb("Reserver",q_BookLink[i])
                                ])]
                        else:
                            for i in range (0,ln):
                                template=template+[Template.GenericElement(title[i],
                                item_url=url[i],
                                image_url=url[i],
                                subtitle="DU "+q_from[i]+" au "+q_to[i]+"\n"+"Reserver a partir de "+str(q_price[i])+" "+q_currency[i],
                                #subtitle="DU "+q_from[i]+" au "+q_to[i]+"               Reserver a partir de "+str(q_price[i])+" "+q_currency[i],
                                #text="Reserver a partir de "+q_price[i]+" "+q_currency[i],
                                buttons=[
                                Template.ButtonWeb("Reserver",q_BookLink[i])
                                ])]
                        page.send(user_id,Template.Generic(template))
                    else:
                        client.send_text(user_id,speech)
                except:
                    client.send_text(user_id,conf.message_data_null)

    return "Ok"

########################################################################
if __name__ == '__main__':
    app.run()
