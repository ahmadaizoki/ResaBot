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
import offre
import users_table
from datetime import date
import offre_weekend

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

#vérifier les access à la page.
@app.route('/webhook', methods=["GET"])
def fb_webhook():
    verification_code = conf.fb_verifing_token
    verify_token = request.args.get('hub.verify_token')
    if verification_code == verify_token:
        return request.args.get('hub.challenge')

#le webhook pour recevoir les message de facebook messenger.
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
                    timestamp="{timestamp}".format(**message)
                    users_table.users(user_id,timestamp)
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
                    elif intention=="h_dispo":
                        try:
                            date=res[2]
                            nights=res[3]
                            adults=res[4]
                            if adults=="":
                                resolvedQuery=res[5]
                                if resolvedQuery!="Plus de personnes":
                                    try:
                                        quick_replies=[
                                        QuickReply(title="1",payload="PICK_P1"),
                                        QuickReply(title="2",payload="PICK_P2"),
                                        QuickReply(title="3",payload="PICK_P3"),
                                        QuickReply(title="Plus de personnes",payload="PICK_P5")
                                        ]
                                        page.send(user_id,"Choisi le nombre de personnes:",quick_replies=quick_replies,metadata="DEVELOPER_DEFINED_METADATA")
                                    except:
                                        client.send_text(user_id,speech)
                                else:
                                    client.send_text(user_id,speech)
                            elif nights=="":
                                resolvedQuery=res[5]
                                if resolvedQuery!="Plus de nuits":
                                    try:
                                        quick_replies=[
                                        QuickReply(title="1",payload="PICK_N1"),
                                        QuickReply(title="2",payload="PICK_N2"),
                                        QuickReply(title="3",payload="PICK_N3"),
                                        QuickReply(title="4",payload="PICK_N4"),
                                        QuickReply(title="Plus de nuits",payload="PICK_N5")
                                        ]
                                        page.send(user_id,"Choisi le nombre de nuits:",quick_replies=quick_replies,metadata="DEVELOPER_DEFINED_METADATA")
                                    except:
                                        client.send_text(user_id,speech)
                                else:
                                    client.send_text(user_id,speech)
                            else:
                                try:
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
                                    try:
                                        res_offre=offre.offre(str(q_from),str(q_to),int(q_nights))
                                        res_offre_of=res_offre
                                        if res_offre_of!="":
                                            message_offre="J'ai trouvé une offre ("+res_offre_of+") juste pour toi ;) Tu veux que je te l'affiche?"
                                            quick_replies=[
                                            QuickReply(title="Oui",payload="PICK_OFFR"),
                                            QuickReply(title="Non",payload="PICK_OFFR")
                                            ]
                                            page.send(user_id,message_offre,quick_replies=quick_replies,metadata="DEVELOPER_DEFINED_METADATA")
                                    except:
                                        print ("erreur offre")
                                except:
                                    client.send_text(user_id,speech)
                        except:
                            client.send_text(user_id,speech)
                    elif intention=="offre_spe":
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
                            res_offre=offre.offre(str(q_from),str(q_to),int(q_nights))
                            res_offre_of=res_offre
                            if res_offre_of=="offre 2":
                                offre_week=offre_weekend.offre_we(q_from,q_to,str(q_nights),str(q_adults))
                                if offre_week!="":
                                    if len(offre_week)==8:
                                        q_from_of=offre_week[0]
                                        q_to_of=offre_week[1]
                                        q_nights_of=offre_week[2]
                                        q_adults_of=offre_week[3]
                                        q_price_of=offre_week[4]
                                        q_currency_of=offre_week[5]
                                        q_BookLink_of=offre_week[6]
                                        q_room_of=offre_week[7]
                                        photo_of=photo_room.photo(q_room_of)
                                        template_of=[Template.GenericElement(res_offre_of,
                                        item_url=photo_of,
                                        image_url=photo_of,
                                        subtitle="Pour "+str(q_nights_of)+" nuits et "+str(q_adults_of)+" personne(s)"+"\n"+"Du "+q_from_of+" au "+q_to_of+" à partir de "+str(q_price_of)+" "+q_currency_of,
                                        buttons=[
                                        Template.ButtonWeb("Réserver",q_BookLink_of),
                                        Template.ButtonPostBack("Plus de chambres","CHAMBRE_PAYLOAD,"+str(q_from)+","+str(q_nights)+","+str(q_adults))
                                        ])]
                                        page.send(user_id,Template.Generic(template_of))
                                else:
                                    client.send_text(user_id,speech)
                        except:
                            client.send_text(user_id,speech)

                    elif intention=="nouvelle_date" or intention=="nombre_personnes" or intention=="nombre_nuits" or intention=="Changement_avis":

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
                            try:
                                res_offre=offre.offre(str(q_from),str(q_to),int(q_nights))
                                res_offre_of=res_offre
                                if res_offre_of!="":
                                    message_offre="J'ai trouvé une offre ("+res_offre_of+") juste pour toi ;) Tu veux que je te l'affiche?"
                                    quick_replies=[
                                    QuickReply(title="Oui",payload="PICK_OFFR"),
                                    QuickReply(title="Non",payload="PICK_OFFR")
                                    ]
                                    page.send(user_id,message_offre,quick_replies=quick_replies,metadata="DEVELOPER_DEFINED_METADATA")
                            except:
                                print ("erreur offre")
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
                        page.send(user_id,"Bonjour "+user_first_name+"! Voilà une petite liste de ce que je peux faire pour toi :)",quick_replies=quick_replies,metadata="DEVELOPER_DEFINED_METADATA")
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

#gérer les postbacks
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
        payload=event["postback"]["payload"]
        print (payload)
    if payload[0]=="CHAMBRE_PAYLOAD":
        try:
            page.send(user_id,Template.Generic(template))
        except:
            page.send(user_id.conf.message_data_null)
    elif payload=="START_PAYLOAD":
        page.send(user_id,"Bienvenue "+user+"!")
    elif payload=="PHOTO_PAYLOAD":
        try:
            gallery=fbweb.get_gallery(conf.HID,"it_IT",conf.H_Access_Token)
            url=gallery[0]
            alt=gallery[1]
            ln=len(url)
            template=[]
            if ln>19:
                for j in range (9,17):
                    template=template+[Template.GenericElement("Gallery",
                    item_url=url[j],
                    image_url=url[j],
                    subtitle=alt[j])]
                template=template+[Template.GenericElement("Gallery",
                subtitle="Pour voir plus de photos",
                buttons=[
                Template.ButtonPostBack("Plus de photos","PHOTO_PAYLOAD1")
                ])]
            else:
                for i in range (9,ln):
                    template=template+[Template.GenericElement("Gallery",
                    item_url=url[i],
                    image_url=url[i],
                    subtitle=alt[i])]
            page.send(user_id,Template.Generic(template))
        except:
            page.send(user_id.conf.message_data_null)
    elif payload=="PHOTO_PAYLOAD1":
        try:
            gallery=fbweb.get_gallery(conf.HID,"it_IT",conf.H_Access_Token)
            url=gallery[0]
            alt=gallery[1]
            ln=len(url)
            template=[]
            if ln>28:
                for j in range (17,26):
                    template=template+[Template.GenericElement("Gallery",
                    item_url=url[j],
                    image_url=url[j],
                    subtitle=alt[j])]
                template=template+[Template.GenericElement("Gallery",
                subtitle="Pour voir plus de photos",
                buttons=[
                Template.ButtonPostBack("Plus de photos","PHOTO_PAYLOAD2")
                ])]
            else:
                for i in range (17,ln):
                    template=template+[Template.GenericElement("Gallery",
                    item_url=url[i],
                    image_url=url[i],
                    subtitle=alt[i])]
            page.send(user_id,Template.Generic(template))
        except:
            page.send(user_id.conf.message_data_null)
    elif payload=="PHOTO_PAYLOAD2":
        try:
            gallery=fbweb.get_gallery(conf.HID,"it_IT",conf.H_Access_Token)
            url=gallery[0]
            alt=gallery[1]
            ln=len(url)
            template=[]
            if ln>37:
                for j in range (26,36):
                    template=template+[Template.GenericElement("Gallery",
                    item_url=url[j],
                    image_url=url[j],
                    subtitle=alt[j])]
            else:
                for i in range (26,ln):
                    template=template+[Template.GenericElement("Gallery",
                    item_url=url[i],
                    image_url=url[i],
                    subtitle=alt[i])]
            page.send(user_id,Template.Generic(template))
        except:
            page.send(user_id.conf.message_data_null)

########################################################################
if __name__ == '__main__':
    app.run()
