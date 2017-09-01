  # -*- coding: utf-8 -*-
import psycopg2
import config
from datetime import datetime, timezone
from pytz import utc
import time

try:
    conn=psycopg2.connect(config.db_url)
except:
    print ("echec de connexion")
rows=[]
cur=conn.cursor()

def users(user_id,timestamp,message):
    try:
        cur.execute("""SELECT * FROM users WHERE userid=%(user_id)s""",{"user_id":user_id})
        rows=cur.fetchall()
    except:
        print ("erreur connexion")
    if rows!=[]:
        if rows[0][1]==user_id and rows[0][2]!=timestamp:
            try:
                cur.execute("""UPDATE users SET timestamp=%(timestamp)s,message=%(message)s WHERE userid=%(user_id)s""",{"timestamp":timestamp,"user_id":user_id,"message":message})
                conn.commit()
            except:
                print ("erreur connexion")
    else:
        try:
            cur.execute("""INSERT INTO users (userid,timestamp,message) VALUES (%(user_id)s,%(timestamp)s,%(message)s)""",{"user_id":user_id,"timestamp":timestamp,"message":message})
            conn.commit()
        except:
            print ("erreur connexion")

def get_users_timestamp(user_id):
    time_loc=time.localtime()
    tm_year=time_loc.tm_year
    tm_mon=time_loc.tm_mon
    tm_mday=time_loc.tm_mday
    tm_min=time_loc.tm_min
    try:
        cur.execute("""SELECT timestamp FROM users WHERE userid=%(user_id)s""",{"user_id":user_id})
        rows=cur.fetchall()
    except:
        print ("erreur connexion")
    if rows!=[]:
        timestamp=int(rows[0][0])/1000
        timestamp=datetime.fromtimestamp(float(timestamp),timezone.utc)
        ltime=timestamp.astimezone()
        timestamp=ltime.strftime('%Y-%m-%d-%H-%M')
        print (timestamp)
        print (time_loc)
        tstamp=timestamp.split('-')
        if tm_year>int(tstamp[0]):
            if tm_mon-int(tstamp[1])>3 or int(tstamp[1])-tm_mon>3:
                return True
        elif tm_mon-int(tstamp[1])>3:
            return True
        elif tm_min-int(tstamp[4])>2:
            return True
        else:
            return False
    else:
        return False

def get_users_id():
    try:
        cur.execute("""SELECT userid FROM users""")
        rows=cur.fetchall()
    except:
        print ("erreur connexion")
    ln=len(rows)
    r=[]
    for i in range (0,ln):
         r=r+[rows[i][0]]
    return r

def last_message(user_id):
    try:
        cur.execute("""SELECT message FROM users WHERE userid=%(user_id)s""",{"user_id":user_id})
        rows=cur.fetchall()
    except:
        print ("erreur connexion")
    if rows!=[]:
        return (rows[0][0])
    else:
        return ""
