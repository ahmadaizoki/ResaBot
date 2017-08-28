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
from fbmq import Template, Page, QuickReply
import photo_room

reload(sys)


from flask import Flask, request
import config as conf
page = Page(conf.fb_access_token)

app = Flask(__name__)

USER_SEQ={}
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
                    recipient="{recipient[id]}".format(**message)
                    user_profile=page.get_user_profile(user_id)
                    user_first_name=user_profile["first_name"]
                    user_last_name=user_profile["last_name"]
                    user_first_name_l=user_first_name.lower()
                    user_last_name_l=user_last_name.lower()
                    user=user_first_name+" "+user_last_name
                    user_l=user_first_name_l+" "+user_last_name_l
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
                                for i in range (0,9):
                                    template=template+[Template.GenericElement("Gallery",
                                    item_url=url[i],
                                    image_url=url[i],
                                    subtitle=alt[i])]
                                template=template+[Template.GenericElement("Gallery",
                                subtitle="Pour voir plus de photos",
                                buttons=[
                                Template.ButtonPostBack("Plus de photos","PHOTO_PAYLOAD")
                                ])]
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
                    elif intention=="h_dispo" or intention=="nouvelle_date" or intention=="nombre_personnes" or intention=="nombre_nuits":
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
                            photo=photo_room.photo(q_room)
                            template=[Template.GenericElement("Une "+q_room,
                            item_url=photo,
                            image_url=photo,
                            subtitle="Pour "+str(q_nights)+" nuits et "+str(q_adults)+" personne(s)"+"\n"+"Du "+q_from+" au "+q_to+" à partir de "+str(q_price)+" "+q_currency,
                            buttons=[
                            Template.ButtonWeb("Réserver",q_BookLink),
                            Template.ButtonPostBack("Plus de chambres","CHAMBRE_PAYLOAD,"+str(date)+","+str(nights)+","+str(adults))
                            ])]
                            page.send(user_id,Template.Generic(template))
                        except:
                            client.send_text(user_id,speech)
                    elif intention=="Moins_cher":
                        try:
                            date=res[2]
                            nights=res[3]
                            adults=res[4]
                            h_dispo=fbweb.moins_cher(date,"",nights,adults,conf.HID,"json","",conf.H_Access_Token)
                            q_from=h_dispo[0]
                            q_to=h_dispo[1]
                            q_nights=h_dispo[2]
                            q_adults=h_dispo[3]
                            q_price=h_dispo[4]
                            q_currency=h_dispo[5]
                            q_BookLink=h_dispo[6]
                            q_room=h_dispo[7]
                            photo=photo_room.photo(q_room)
                            template=[Template.GenericElement("Une "+q_room,
                            item_url=photo,
                            image_url=photo,
                            subtitle="Pour "+str(q_nights)+" nuits et "+str(q_adults)+" personne(s)"+"\n"+"Du "+q_from+" au "+q_to+" à partir de "+str(q_price)+" "+q_currency,
                            buttons=[
                            Template.ButtonWeb("Réserver",q_BookLink)
                            ])]
                            page.send(user_id,Template.Generic(template))
                        except:
                            client.send_text(user_id,speech)
                    elif intention=="insultes_action" or intention=="danser" or intention=="r_n" or intention=="r_p":
                        client.send_image(user_id,speech)
                    elif intention=="r_i":
                        chaine=res[2]
                        if chaine==user_first_name or chaine==user_last_name or chaine==user or chaine==user_first_name_l or chaine==user_last_name_l or chaine==user_l:
                            client.send_text(user_id,"C'est toi! :) Tu crois que j'ai pas les pouvoirs de te connaitre")
                        else:
                            client.send_image(user_id,speech)
                    elif intention=="smalltalk.greetings.hello":
                        quick_replies=[
                        QuickReply(title="Photos",payload="PICK_PHOTOS"),
                        QuickReply(title="Offres",payload="PICK_OFFRES"),
                        QuickReply(title="Réserver une chambre",payload="PICK_RESERVATION")
                        ]
                        page.send(user_id,"Bonjour! Voilà une petite liste de ce que je peux faire pour toi :)",quick_replies=quick_replies,metadata="DEVELOPER_DEFINED_METADATA")
                    elif intention=="s_f":
                        quick_replies=[
                        QuickReply(title="Photos",payload="PICK_PHOTOS"),
                        QuickReply(title="Offres",payload="PICK_OFFRES"),
                        QuickReply(title="Réserver une chambre",payload="PICK_RESERVATION")
                        ]
                        page.send(user_id,"Voilà une petite liste de ce que je peux faire pour toi :)",quick_replies=quick_replies,metadata="DEVELOPER_DEFINED_METADATA")
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
    user_profile=page.get_user_profile(user_id)
    user=user_profile["first_name"]
    try:
        payload=payload.split(',')
        h_dispo=fbweb.get_quotation_room(payload[1],"",payload[2],payload[3],conf.HID,"json","",conf.H_Access_Token)
        q_from=h_dispo[0]
        q_to=h_dispo[1]
        q_nights=h_dispo[2]
        q_adults=h_dispo[3]
        q_price=h_dispo[4]
        q_currency=h_dispo[5]
        q_BookLink=h_dispo[6]
        q_room=h_dispo[7]
        ln=len(q_from)
        template=[]
        if ln >10:
            for i in range(0,10):
                photo=photo_room.photo(q_room[i])
                template=template+[Template.GenericElement("Une "+q_room[i],
                item_url=photo,
                image_url=photo,
                subtitle="Pour "+str(q_nights[i])+" nuit(s) et "+str(q_adults[i])+" personne(s)"+"\n"+"Du "+q_from[i]+" au "+q_to[i]+" à partir de "+str(q_price[i])+" "+q_currency[i],
                buttons=[
                Template.ButtonWeb("Réserver",q_BookLink[i])
                ])]
        else:
            for i in range (0,ln):
                photo=photo_room.photo(q_room[i])
                template=template+[Template.GenericElement("Une "+q_room[i],
                item_url=photo,
                image_url=photo,
                subtitle="Pour "+str(q_nights[i])+" nuit(s) et "+str(q_adults[i])+" personne(s)"+"\n"+"Du "+q_from[i]+" au "+q_to[i]+" à partir de "+str(q_price[i])+" "+q_currency[i],
                buttons=[
                Template.ButtonWeb("Réserver",q_BookLink[i])
                ])]
    except:
        try:
            if payload=="PHOTO_PAYLOAD":
                me="ok"
        except:
            page.send(user_id,"Bienvenue "+user+"!")
    if payload[0]=="CHAMBRE_PAYLOAD":
        try:
            page.send(user_id,Template.Generic(template))
        except:
            page.send(user_id.conf.message_data_null)
    elif payload=="PHOTO_PAYLOAD":
        page.send(user_id,me)
########################################################################
if __name__ == '__main__':
    app.run()
