#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
from telebot import types
import telebot
import emoji
import inits
import time

import InlineBtn


HTPtext="""\tYou see a cookie button(🍪) below
press that button to give me cookie
the more cookie me get the more me like(❤️)
goodluck!"""
Starttext="""Hellooooo...
Me Cookie Monster and me here to eat cookies
type /howtoplay to get started!"""
HTDueltext="""A CookieDuel is a game played by two users.
You can start a duel by either inviting someone to a duel or accepting someones invitation, \
to invite someone to a duel enter the command /invite with the like amount that you want to duel on, for example:
/invite 100
Will make an invitation that you can send to someone or a group, after a user accepts the invitation the duel will start \
and the winner will get the amount of likes that was specified in the command(in this case 100""" + \
           emoji.emojize(emoji.demojize(u'❤')) + """) and the looser will get \
dislikes as much as the likes the winner got (100""" + emoji.emojize(emoji.demojize(u'💔')) + \
           """ for this example).\n""" + \
           "In the duel you have three options of cookies to offer cookie monster " + \
           "and he will choose one of the cookies that are given from the two users." + \
           "\nCookie Monster,\n" + \
    emoji.emojize("Prefers (" + emoji.demojize(u'🍪') + 'Banana Cookie' + emoji.demojize(u'🍌') + ") to (" +
                  emoji.demojize(u'🍪') + 'Chocolate Chip Cookie' + emoji.demojize(u'🍫') + ")\n") + \
    emoji.emojize(",Prefers (" + emoji.demojize(u'🍪') + 'Chocolate Chip Cookie' + emoji.demojize(u'🍫') + ") to (" +
                  emoji.demojize(u'🍪') + 'Vanilla Ice-Cream Cookie' + emoji.demojize(u'🍦') + ")\n") + \
    emoji.emojize("and Prefers (" + emoji.demojize(u'🍪') + 'Vanilla Ice-Cream Cookie' + emoji.demojize(u'🍦') + ") to (" +
                  emoji.demojize(u'🍪') + 'Banana Cookie' + emoji.demojize(u'🍌') + ")\n") + \
    "\nThe user, whose cookie has been chosen will get one point and the first user " + \
    "that gets three points will be the winner.\n" + \
    "good luck!"

HELPtext="""here is the list of commands:
/help - show list of commands
/top10 - see the top 10 rank by likes
/rank - see your rank
/showcookies - Show the cookie buttons below

/howtoduel - How to play a duel
/invite <like_amount> - Make an invitation to a CookieDuel
/abortduel - Cancel the duel that you're in"""


@inits.bot.message_handler(commands=['start'])
def send_welcome(message):
    inits.bot.sendMessage(chat_id=message.message.chat_id, text=Starttext)

@inits.bot.message_handler(commands=['howtoplay'])
def HowToPlay(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtna = types.KeyboardButton('🍪')
    markup.row(itembtna)
    inits.bot.send_message(message.chat.id, HTPtext, reply_markup=markup)

last_time={}
@inits.bot.message_handler(commands=['top10'])
def seeRankTop10(message):

    userId = message.from_user.id

    if (last_time.has_key(userId) and (message.date - last_time[userId]) < 1):
        inits.bot.send_message(message.chat.id,
                               "Hey let me finish last cookie...")
        print 'multiple calls from getCm'
        return

    cn = sqlite3.connect("zthb.sqlite")
    cur = cn.cursor()
    cur.execute("SELECT * FROM cookie_giver")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    rows = cur.fetchall()
    templib=[]

    output=""
    max=0
    for x in range(1, 11):
        try:
            max = 0
            for row in rows:
                if(max<row[6] and not (row[0] in templib)):
                    max=row[6]
                    try:
                        u_prtname='@'+row[1]
                        u_id = row[0]
                    except:
                        u_prtname=row[2]+' '+row[3]
                        u_id = row[0]
            if max==0:
                break
            templib.append(u_id)
            output=output+str(x)+"-"+u_prtname+" with "+str(max)+emoji.emojize(emoji.demojize(u'❤'))+"\n"
        except:
            continue
    cn.close()
    inits.bot.send_message(message.chat.id,
                           output)

@inits.bot.message_handler(commands=['howtoduel'])
def helpDuel(message):
    inits.bot.send_message(message.from_user.id,HTDueltext)

@inits.bot.message_handler(commands=['help'])
def helpDuel(message):
    inits.bot.send_message(message.from_user.id,HELPtext)

@inits.bot.message_handler(commands=['rank'])
def seeRank(message):

    userId = message.from_user.id

    if (last_time.has_key(userId) and (message.date - last_time[userId]) < 1):
        inits.bot.send_message(message.chat.id,
                               "Hey let me finish last cookie...")
        print 'multiple calls from getCm'
        return


    cn = sqlite3.connect("zthb.sqlite")
    cur = cn.cursor()
    cur.execute("SELECT * FROM cookie_giver")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    rows = cur.fetchall()
    templib=[]
    output=""
    max=0
    for x in range(1, 100):
        max = 0
        for row in rows:
            if(max<row[6] and not (row[0] in templib)):
                max=row[6]
                u_id=row[0]
        if max==0:
            break
        templib.append(u_id)
        if userId==u_id:
            output="Your rank is "+str(x)+" with "+str(max)+emoji.emojize(emoji.demojize(u'❤'))
            inits.bot.send_message(message.chat.id,
                                   output)
            cn.close()
            return

    cn.close()
    inits.bot.send_message(message.message.chat_id,
                           "Sorry your rank is above 100 :(")

@inits.bot.message_handler(content_types=['text'])
def getCm(message):

    userId = message.from_user.id

    if(last_time.has_key(userId) and (message.date-last_time[userId]) < 1):
        inits.bot.send_message(message.chat.id,
                               "Hey let me finish last cookie...")
        print 'multiple calls from getCm'
        return

    userMessage = message.text
    print message
    userName = message.from_user.username
    userFirstName = message.from_user.first_name
    userLastName = message.from_user.last_name
    last_time[userId] = message.date


    # print message.date

    if emoji.demojize(unicode(userMessage))==emoji.demojize(u'🍪'):
        cn = sqlite3.connect("zthb.sqlite")
        cur = cn.cursor()
        cur.execute("SELECT * FROM cookie_giver WHERE u_id={0}".format(userId))
        cn.execute("PRAGMA ENCODING = 'utf8';")
        # cur.row_factory = lite.Row
        cn.text_factory = str
        row = cur.fetchone()
        if row != None:
            userLikes = row[6] + 1
            cur.execute("UPDATE cookie_giver SET u_likes=? WHERE u_id=?", (userLikes, userId))
            cn.commit()
            inits.bot.send_message(message.chat.id, "Me got it!!!\nOHM NOM NOM NOM")
            inits.bot.send_message(message.chat.id, "Now me {0}❤ you".format(userLikes))
        else:
            userLikes = 1
            cn.execute(
                "CREATE TABLE IF NOT EXISTS cookie_giver(u_id MEDIUMINT, u_name VARCHAR(100), u_first_name VARCHAR(100), u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME,u_likes MEDIUMINT);")
            cn.execute("INSERT INTO cookie_giver VALUES (?, ?, ?, ?, ?, ?,?);",
                       (userId, userName, userFirstName, userLastName, userMessage, datetime.now(), userLikes))
            cn.commit()
            inits.bot.send_message(message.chat.id, "You give me your first cookie!!!\nThanks!!!\nOHM NOM NOM NOM")
            inits.bot.send_message(message.chat.id, "Now me {0}❤ you".format(userLikes))
        cn.close()
    elif (InlineBtn.get_Duel_MSG(message)):
        pass
    else:
        inits.bot.send_message(message.chat.id,
                        "Me not get any cookies :(")

    print(message.from_user.username)
    print "done"



print 'step1'

while(1):
    try:
        inits.bot.polling()
    except:
        time.sleep(5)
        print "An error in polling()"

print 'step2'