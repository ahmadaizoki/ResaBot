#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################
#les packages et les framework
import os.path
import sys
import config
import json
import date as dd
import date_week
import time
import datetime
from random import randint
import analys
import date_test
import date_jour_semaine
import analyse_phrase
import analyse_dans

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
        resolvedQuery=res['result']['resolvedQuery']
        date=date.lower()
        if date!="":
            mot=analyse_phrase.analyse(date)
        else:
            mot=""
        if date in config.date0:
            date=dd.time_calc(0)
        elif date in config.date1:
            date=dd.time_calc(1)
        elif date in config.date2:
            date=dd.time_calc(2)
        elif date in config.date_week_end:
            ddd=date_week.date_week()
            date=dd.time_calc(ddd)
        elif date in config.prochain:
            date1=str(date)
            res=date_jour_semaine.jour_prochain(date1)
            date=dd.time_calc(res)
        elif date in config.prochain1:
            date1=str(date)
            res=date_jour_semaine.jour_prochain(date1)
            date=dd.time_calc(res)
        elif date in config.prochain2:
            date1=str(date)
            res=date_jour_semaine.jour_prochain(date1)
            date=dd.time_calc(res)
        elif mot=="dans":
            date=analyse_dans.analyse_sentence(date)
        elif date in config.date_noel:
            time_loc=time.localtime()
            tm_mon=time_loc.tm_mon
            tm_mday=time_loc.tm_mday
            tm_year=time_loc.tm_year
            if tm_mon==12 and tm_mday>25:
                d=datetime.date(tm_year+1,12,25)
                date=str(d)
            else:
                d=datetime.date(tm_year,12,25)
                date=str(d)
        elif date in config.date_valentin:
            time_loc=time.localtime()
            tm_mon=time_loc.tm_mon
            tm_mday=time_loc.tm_mday
            tm_year=time_loc.tm_year
            if tm_mon>=2 and tm_mday>14:
                d=datetime.date(tm_year+1,2,14)
                date=str(d)
            else:
                d=datetime.date(tm_year,2,14)
                date=str(d)
        else:
            try:
                date1=str(date)
                date=analys.analyse_date(date1)
            except:
                try:
                    date=date_test.test(date)
                except:
                    date=res['result']['parameters']['date']
        if date!="" and nights!="" and adults!="":
            message_text="l'original nombre de personnes "+str(adults)+" et nombre de nuits "+str(nights)+" et la date "+str(date)
            print (message_text)
            api_message(message_text,user_id)
            print ("ahmad")
        print ([speech]+[intention]+[date]+[nights]+[adults])
        return ([speech]+[intention]+[date]+[nights]+[adults]+[resolvedQuery])
    elif intention=="nouvelle_date" or intention=="nombre_nuits" or intention=="nombre_personnes" or intention=="Moins_cher" or intention=="offre_spe" :
        try:
            date=res['result']['contexts'][0]['parameters']['date']
            nights=res['result']['contexts'][0]['parameters']['nbnight']
            adults=res['result']['contexts'][0]['parameters']['nbpax']
            date=date.lower()
            if date!="":
                mot=analyse_phrase.analyse(date)
            else:
                mot=""
            if date in config.date0:
                date=dd.time_calc(0)
            elif date in config.date1:
                date=dd.time_calc(1)
            elif date in config.date2:
                date=dd.time_calc(2)
            elif date in config.date_week_end:
                ddd=date_week.date_week()
                date=dd.time_calc(ddd)
            elif date in config.prochain:
                date1=str(date)
                res=date_jour_semaine.jour_prochain(date1)
                date=dd.time_calc(res)
            elif date in config.prochain1:
                date1=str(date)
                res=date_jour_semaine.jour_prochain(date1)
                date=dd.time_calc(res)
            elif date in config.prochain2:
                date1=str(date)
                res=date_jour_semaine.jour_prochain(date1)
                date=dd.time_calc(res)
            elif mot=="dans":
                date=analyse_dans.analyse_sentence(date)
            elif date in config.date_noel:
                time_loc=time.localtime()
                tm_mon=time_loc.tm_mon
                tm_mday=time_loc.tm_mday
                tm_year=time_loc.tm_year
                if tm_mon==12 and tm_mday>25:
                    d=datetime.date(tm_year+1,12,25)
                    date=str(d)
                else:
                    d=datetime.date(tm_year,12,25)
                    date=str(d)
            elif date in config.date_valentin:
                time_loc=time.localtime()
                tm_mon=time_loc.tm_mon
                tm_mday=time_loc.tm_mday
                tm_year=time_loc.tm_year
                if tm_mon>=2 and tm_mday>14:
                    d=datetime.date(tm_year+1,2,14)
                    date=str(d)
                else:
                    d=datetime.date(tm_year,2,14)
                    date=str(d)
            else:
                try:
                    date1=str(date)
                    date=analys.analyse_date(date1)
                except:
                    try:
                        date=date_test.test(date)
                    except:
                        date=res['result']['parameters']['date']
            print ([speech]+[intention]+[date]+[nights]+[adults])
            return ([speech]+[intention]+[date]+[nights]+[adults])
        except:
            return ([speech]+[intention])
    elif intention=="Changement_avis":
        try:
            date=res['result']['contexts'][0]['parameters']['ddate']
            nights=res['result']['contexts'][0]['parameters']['nnnight']
            adults=res['result']['contexts'][0]['parameters']['nnpax']
            date=date.lower()
            if date!="":
                mot=analyse_phrase.analyse(date)
            else:
                mot=""
            if date in config.date0:
                date=dd.time_calc(0)
            elif date in config.date1:
                date=dd.time_calc(1)
            elif date in config.date2:
                date=dd.time_calc(2)
            elif date in config.date_week_end:
                ddd=date_week.date_week()
                date=dd.time_calc(ddd)
            elif date in config.prochain:
                date1=str(date)
                res=date_jour_semaine.jour_prochain(date1)
                date=dd.time_calc(res)
            elif date in config.prochain1:
                date1=str(date)
                res=date_jour_semaine.jour_prochain(date1)
                date=dd.time_calc(res)
            elif date in config.prochain2:
                date1=str(date)
                res=date_jour_semaine.jour_prochain(date1)
                date=dd.time_calc(res)
            elif mot=="dans":
                date=analyse_dans.analyse_sentence(date)
            elif date in config.date_noel:
                time_loc=time.localtime()
                tm_mon=time_loc.tm_mon
                tm_mday=time_loc.tm_mday
                tm_year=time_loc.tm_year
                if tm_mon==12 and tm_mday>25:
                    d=datetime.date(tm_year+1,12,25)
                    date=str(d)
                else:
                    d=datetime.date(tm_year,12,25)
                    date=str(d)
            elif date in config.date_valentin:
                time_loc=time.localtime()
                tm_mon=time_loc.tm_mon
                tm_mday=time_loc.tm_mday
                tm_year=time_loc.tm_year
                if tm_mon>=2 and tm_mday>14:
                    d=datetime.date(tm_year+1,2,14)
                    date=str(d)
                else:
                    d=datetime.date(tm_year,2,14)
                    date=str(d)
            else:
                try:
                    date1=str(date)
                    date=analys.analyse_date(date1)
                except:
                    try:
                        date=date_test.test(date)
                    except:
                        date=res['result']['parameters']['date']
            print ([speech]+[intention]+[date]+[nights]+[adults])
            return ([speech]+[intention]+[date]+[nights]+[adults])
        except:
            return ([speech]+[intention])
    elif intention=="insultes_action" or intention=="danser" or intention=="r_n" or intention=="r_p":
        ln=len(res['result']['fulfillment']['messages'])
        i=randint(0,ln-1)
        speech=res['result']['fulfillment']['messages'][i]['imageUrl']
        return ([speech]+[intention])
    elif intention=="r_i":
        ln=len(res['result']['fulfillment']['messages'])
        i=randint(0,ln-1)
        speech=res['result']['fulfillment']['messages'][i]['imageUrl']
        chaine=res['result']['parameters']['chaine']
        return ([speech]+[intention]+[chaine])
    else:
        return ([speech]+[intention])
