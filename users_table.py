  # -*- coding: utf-8 -*-
import psycopg2
import config
from datetime import datetime, timezone
from pytz import utc

try:
    conn=psycopg2.connect(config.db_url)
except:
    print ("echec de connexion")
rows=[]
cur=conn.cursor()

def users(user_id,timestamp):
    try:
        cur.execute("""SELECT * FROM users WHERE userid=%(user_id)s""",{"user_id":user_id})
        rows=cur.fetchall()
    except:
        print ("erreur connexion")
    if rows!=[]:
        if rows[0][1]==user_id and rows[0][2]!=timestamp:
            try:
                cur.execute("""UPDATE users SET timestamp=%(timestamp)s WHERE userid=%(user_id)s""",{"timestamp":timestamp,"user_id":user_id})
                conn.commit()
            except:
                print ("erreur connexion")
    else:
        try:
            cur.execute("""INSERT INTO users (userid,timestamp) VALUES (%(user_id)s,%(timestamp)s)""",{"user_id":user_id,"timestamp":timestamp})
            conn.commit()
        except:
            print ("erreur connexion")

def get_users_timestamp(user_id):
    try:
        cur.execute("""SELECT timestamp FROM users WHERE userid=%(user_id)s""",{"user_id":user_id})
        rows=cur.fetchall()
    except:
        print ("erreur connexion")
    if rows!=[]:
        timestamp=int(rows[0][0])/1000
        timestamp=datetime.fromtimestamp(float(timestamp),timezone.utc)
        ltime=timestamp.astimezone()
        timestamp=ltime.strftime('%Y-%m-%d-%H')
        tstamp=timestamp.split('-')
        if int(tstamp[0])>2017:
            return True
        elif int(tstamp[1])>7:
            return True
        elif int(tstamp[2])>10:
            return True
        elif int(tstamp[3])>7:
            return True
        else:
            return False
        print (tstamp)
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
