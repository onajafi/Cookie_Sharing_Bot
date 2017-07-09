#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime
from datetime import timedelta
from telebot import types
import telebot
import logging
import emoji
import inits


HTPtext="""\tYou see a cookie button(🍪) below
press that button to give me cookie
the more cookie me get the more me like(❤️)
goodluck!"""
Starttext="""Hellooooo...
Me Cookie Monster and me here to eat cookies
type /howtoplay to get started!"""

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=Starttext)


tb = telebot.TeleBot(inits.bot_address)
#tb = telebot.TeleBot('384344173:AAFvWbjW5jHO2yh_wvO3v5ysvXqFqefsSFg')

def HowToPlay(bot,update):
    TestCom(bot,update)
    #bot.sendMessage(chat_id=update.message.chat_id, text=HTPtext)

def TestCom(bot,update):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtna = types.KeyboardButton('🍪')
    markup.row(itembtna)
    tb.send_message(update.message.chat_id,HTPtext, reply_markup=markup)

last_time={}

def getCm(bot, update):
    userInfo = update.message.chat
    userId = userInfo['id']

    if(last_time.has_key(userId) and (update.message.date-last_time[userId]) < timedelta(0,0,0,1,0,0)):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Hey let me finish last cookie...")
        print 'multiple calls from getCm'
        return

    userMessage = update.message.text

    userName = userInfo['username']
    userFirstName = userInfo['first_name']
    userLastName = userInfo['last_name']
    last_time[userId]=update.message.date;


    print update.message.date

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
            bot.sendMessage(chat_id=update.message.chat_id, text="Me got it!!!\nOHM NOM NOM NOM")
            bot.sendMessage(chat_id=update.message.chat_id, text="Now me {0}❤ you".format(userLikes))
        else:
            userLikes = 1
            cn.execute(
                "CREATE TABLE IF NOT EXISTS cookie_giver(u_id MEDIUMINT, u_name VARCHAR(100), u_first_name VARCHAR(100), u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME,u_likes MEDIUMINT);")
            cn.execute("INSERT INTO cookie_giver VALUES (?, ?, ?, ?, ?, ?,?);",
                       (userId, userName, userFirstName, userLastName, userMessage, datetime.now(), userLikes))
            cn.commit()
            bot.sendMessage(chat_id=update.message.chat_id, text="You give me your first cookie!!!\nThanks!!!\nOHM NOM NOM NOM")
            bot.sendMessage(chat_id=update.message.chat_id, text="Now me {0}❤ you".format(userLikes))
        cn.close();
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Me not get any cookies :(")
    
    ##########################################
    # cn = sqlite3.connect("zthb.sqlite")
    # cn.execute("PRAGMA ENCODING = 'utf8';")
    # cn.text_factory = str
    # cn.execute("CREATE TABLE IF NOT EXISTS user_comment(u_id MEDIUMINT, u_name VARCHAR(100), u_first_name VARCHAR(100), u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME);")
    # cn.execute("INSERT INTO user_comment VALUES (?, ?, ?, ?, ?, ?);", (userId, userName, userFirstName, userLastName, userMessage, datetime.now()))
    # cn.commit()
    # cn.close()
    ##########################################
    
    print(userInfo['username'])
    print "done"

def seeRankTop10(bot,update):
    if (last_time.has_key(update.message.chat['id']) and (update.message.date - last_time[update.message.chat['id']]) < timedelta(0, 0, 0, 1, 0, 0)):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Hey let me finish last cookie...")
        print 'multiple calls from seeRankTop10'
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
    cn.close();
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=output)

def seeRank(bot,update):
    if (last_time.has_key(update.message.chat['id']) and (update.message.date - last_time[update.message.chat['id']]) < timedelta(0, 0, 0, 1, 0, 0)):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Hey let me finish last cookie...")
        print 'multiple calls from seeRank'
        return

    UserID=update.message.chat["id"]
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
        if UserID==u_id:
            output="Your rank is "+str(x)+" with "+str(max)+emoji.emojize(emoji.demojize(u'❤'))
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=output)
            cn.close();
            return


    cn.close();
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Sorry your rank is above 100 :(")


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Me not get that?!?!")

# announce_message="""Hey everybody,
# Thanks for joining Cookie Monster's friend zone.
# There are a few updates that have been applied to the bot:
# - Some bugs related to the lack of process has been fixed (but still needs some work)
# - The /top10 command shows all top 10 users even without IDs
# - Cookie Monster is a little busy eating all the cookies from you guys so it takes a little time for him to finish the previous cookies :d
#
# enjoy feeding
# .B"""

# def test_announce():
#     cn = sqlite3.connect("zthb.sqlite")
#     cur = cn.cursor()
#     cur.execute("SELECT * FROM cookie_giver")
#     cn.execute("PRAGMA ENCODING = 'utf8';")
#     cn.text_factory = str
#     rows = cur.fetchall()
#     templib = []
#     for row in rows:
#         if (row[0] not in templib):
#             templib.append(row[0])
#             if(row[1]=="Dot_Blue"):
#                 tb.send_message(chat_id=row[0], text=announce_message)
#
#     cn.close();

updater = Updater(token=inits.bot_address)
#updater = Updater(token='432998260:AAHw2zyD4zx79WHpcbAVjAc8cYLz_PIfRuM')
#updater = Updater(token='384344173:AAFvWbjW5jHO2yh_wvO3v5ysvXqFqefsSFg')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

howtoplay_handler = CommandHandler('howtoplay', HowToPlay)
dispatcher.add_handler(howtoplay_handler)

seeRankTop10_handler = CommandHandler('top10', seeRankTop10)
dispatcher.add_handler(seeRankTop10_handler)

seeMeRank_handler = CommandHandler('rank', seeRank)
dispatcher.add_handler(seeMeRank_handler)

TestCom_handler = CommandHandler('test', TestCom)
dispatcher.add_handler(TestCom_handler)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

cm_handler = MessageHandler([Filters.text], getCm)
dispatcher.add_handler(cm_handler)

unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
print 'step1'
#test_announce()
updater.idle()

print 'step2'
updater.stop()
print 'step3'