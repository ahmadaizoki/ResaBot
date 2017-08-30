  # -*- coding: utf-8 -*-
import psycopg2
import config

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
        return rows[0][0]
    else:
        return ""
