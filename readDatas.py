import sqlite3 as lite
import sys
from datetime import datetime

#con = lite.connect('zthb.sqlite')

# with con:
#     cur = con.cursor()
#
#     cur.execute("UPDATE user_comment SET u_comment=? WHERE u_comment=?", ("__DOLLFACE__","OMG"))
#     con.commit()
#
#     print "Number of rows updated: %d" % cur.rowcount

# with con:
#     cur = con.cursor()
#     cur.execute("SELECT * FROM user_comment")
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print row

# def test1():
#     cn = lite.connect("zthb.sqlite")
#     cn.execute("PRAGMA ENCODING = 'utf8';")
#     cn.text_factory = str
#     cn.execute("CREATE TABLE IF NOT EXISTS cookie_giver(u_id MEDIUMINT, u_name VARCHAR(100), u_first_name VARCHAR(100), u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME,u_likes MEDIUMINT);")
#     cn.execute("INSERT INTO cookie_giver VALUES (?, ?, ?, ?, ?, ?,?);", (userId, userName, userFirstName, userLastName, userMessage, datetime.now(),userLikes))
#     cn.commit()
#     cn.close()

def test2():
    userId=123
    userName='Tester'
    userFirstName='POP'
    userLastName='COMPUTER'
    userMessage='THE MSG'

    cn = lite.connect("zthb.sqlite")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    cn.execute("CREATE TABLE IF NOT EXISTS user_comment(u_id MEDIUMINT, u_name VARCHAR(100), u_first_name VARCHAR(100), u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME);")
    cn.execute("INSERT INTO user_comment VALUES (?, ?, ?, ?, ?, ?);",(userId, userName, userFirstName, userLastName, userMessage, datetime.now()))
    cn.commit()
    cn.close()

def readDATA():
    con = lite.connect('zthb.sqlite')
    cur = con.cursor()
    cur.execute("SELECT * FROM cookie_giver")
    rows = cur.fetchall()

    for row in rows:
        print row



def fetchingDATA():
    userId = 124
    userName = 'Tester'
    userFirstName = 'POP'
    userLastName = 'COMPUTER'
    userMessage = 'THE MSG'

    cn = lite.connect("zthb.sqlite")
    cur = cn.cursor()
    cur.execute("SELECT * FROM cookie_giver WHERE u_id={0}".format(userId))
    cn.execute("PRAGMA ENCODING = 'utf8';")
    #cur.row_factory = lite.Row
    cn.text_factory = str
    row = cur.fetchone()
    if row != None:
        userLikes=row[6]+1
        cur.execute("UPDATE cookie_giver SET u_likes=? WHERE u_id=?", (userLikes, userId))
        cn.commit()
    else:
        userLikes=1
        cn.execute("CREATE TABLE IF NOT EXISTS cookie_giver(u_id MEDIUMINT, u_name VARCHAR(100), u_first_name VARCHAR(100), u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME,u_likes MEDIUMINT);")
        cn.execute("INSERT INTO cookie_giver VALUES (?, ?, ?, ?, ?, ?,?);", (userId, userName, userFirstName, userLastName, userMessage, datetime.now(),userLikes))
        cn.commit()
    cn.close();




#test2()
readDATA()
fetchingDATA()
readDATA()