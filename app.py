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
from fbmq import Template, Page

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
                    print (text)
                    res=api.api_message(text,user_id)
                    speech=res[0]
                    intention=res[1]
                    if intention=="gallery":
                        try:
                            gallery=fbweb.get_gallery(conf.HID,"it_IT",conf.H_Access_Token)
                            url=gallery[0]
                            alt=gallery[1]
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
                        except:
                            client.send_text(user_id,conf.message_pas_photos)
                    elif intention=="offres":
                        try:
                            offres=fbweb.get_offers("json",conf.HID,"totalPrice","en_GB","EUR",conf.H_Access_Token)
                            url=offres[0]
                            title=offres[1]
                            q_from=offres[2]
                            q_to=offres[3]
                            q_price=offres[4]
                            q_currency=offres[5]
                            q_BookLink=offres[6]
                            ln=len(url)
                            template=[]
                            if ln>10:
                                for i in range (0,10):
                                    template=template+[Template.GenericElement(title[i],
                                    item_url=url[i],
                                    image_url=url[i],
                                    subtitle="DU "+q_from[i]+" au "+q_to[i]+"\n"+"Réserver à partir de "+str(q_price[i])+" "+q_currency[i],
                                    buttons=[
                                    Template.ButtonWeb("Réserver",q_BookLink[i])
                                    ])]
                            else:
                                for i in range (0,ln):
                                    template=template+[Template.GenericElement(title[i],
                                    item_url=url[i],
                                    image_url=url[i],
                                    subtitle="DU "+q_from[i]+" au "+q_to[i]+"\n"+"Réserver à partir de "+str(q_price[i])+" "+q_currency[i],
                                    buttons=[
                                    Template.ButtonWeb("Réserver",q_BookLink[i])
                                    ])]
                            page.send(user_id,Template.Generic(template))
                        except:
                            client.send_text(user_id,conf.message_pas_offres)
                    elif intention=="h_dispo":
                        try:
                            date=res[2]
                            nights=res[3]
                            adults=res[4]
                            h_dispo=fbweb.get_quotation(date,"",nights,adults,conf.HID,"json","",conf.H_Access_Token)
                            q_from=h_dispo[0]
                            q_to=h_dispo[1]
                            q_nights=h_dispo[2]
                            q_adults=h_dispo[3]
                            q_price=h_dispo[4]
                            q_currency=h_dispo[5]
                            q_BookLink=h_dispo[6]
                            q_room=h_dispo[7]
                            template=[Template.GenericElement(q_room,
                            subtitle="Pour "+str(q_nights)+" nuits et "+str(q_adults)+" personne(s)"+"\n"+"Du "+q_from+" au "+q_to+" à partir de "+str(q_price)+" "+q_currency+" par chambre",
                            buttons=[
                            Template.ButtonWeb("Réserver",q_BookLink),
                            Template.ButtonPostBack("Plus de chambres","CHAMBRE_PAYLOAD"+str(date)+str(nights)+str(adults))#more_room(user_id,date,"",nights,adults,conf.HID,"json","",conf.H_Access_Token))
                            ])]
                            page.send(user_id,Template.Generic(template))
                        except:
                            client.send_text(user_id,speech)
                    elif intention=="insultes_action":
                        client.send_image(user_id,speech)
                    else:
                        client.send_text(user_id,speech)
                except:
                    client.send_text(user_id,conf.message_data_null)
            elif message.get('postback'):
                received_postback(message)

    return "Ok"

def received_postback(event):
    user_id=event["sender"]["id"]
    payload=event["postback"]["payload"]
    if payload=="CHAMBRE_PAYLOAD":
        print (event)
        print (payload)
        page.send(user_id,"okkk!")
########################################################################
if __name__ == '__main__':
    app.run()
