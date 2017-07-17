#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3
# from telegram.ext import Updater
# from telegram.ext import CommandHandler
# from telegram.ext import MessageHandler, Filters
from datetime import datetime
from datetime import timedelta
from telebot import types
import telebot
import logging
import emoji
import inits

import InlineBtn


HTPtext="""\tYou see a cookie button(🍪) below
press that button to give me cookie
the more cookie me get the more me like(❤️)
goodluck!"""
Starttext="""Hellooooo...
Me Cookie Monster and me here to eat cookies
type /howtoplay to get started!"""

@inits.bot.message_handler(commands=['start'])
def send_welcome(message):
    inits.bot.sendMessage(chat_id=message.message.chat_id, text=Starttext)

# def start(bot, update):
#     bot.sendMessage(chat_id=update.message.chat_id, text=Starttext)

#bot1 = telebot.TeleBot(inits.bot_address)
#tb = telebot.TeleBot('384344173:AAFvWbjW5jHO2yh_wvO3v5ysvXqFqefsSFg')

@inits.bot.message_handler(commands=['howtoplay'])
def HowToPlay(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtna = types.KeyboardButton('🍪')
    markup.row(itembtna)
    inits.bot.send_message(message.chat.id, HTPtext, reply_markup=markup)

# def HowToPlay(bot,update):
#     TestCom(bot,update)
#     #bot.sendMessage(chat_id=update.message.chat_id, text=HTPtext)
#
# def TestCom(bot,update):
#     markup = types.ReplyKeyboardMarkup(row_width=1)
#     itembtna = types.KeyboardButton('🍪')
#     markup.row(itembtna)
#     inits.bot.send_message(update.message.chat_id,HTPtext, reply_markup=markup)

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



# def unknown(bot, update):
#     bot.sendMessage(chat_id=update.message.chat_id, text="Me not get that?!?!")


# updater = Updater(token=inits.bot_address)
#updater = Updater(token='432998260:AAHw2zyD4zx79WHpcbAVjAc8cYLz_PIfRuM')
#updater = Updater(token='384344173:AAFvWbjW5jHO2yh_wvO3v5ysvXqFqefsSFg')

# dispatcher = updater.dispatcher

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# howtoplay_handler = CommandHandler('howtoplay', HowToPlay)
# dispatcher.add_handler(howtoplay_handler)

# seeRankTop10_handler = CommandHandler('top10', seeRankTop10)
# dispatcher.add_handler(seeRankTop10_handler)
#
# seeMeRank_handler = CommandHandler('rank', seeRank)
# dispatcher.add_handler(seeMeRank_handler)

# TestCom_handler = CommandHandler('test', TestCom)
# dispatcher.add_handler(TestCom_handler)
#
#
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)

# cm_handler = MessageHandler([Filters.text], getCm)
# dispatcher.add_handler(cm_handler)

# unknown_handler = MessageHandler([Filters.command], unknown)
# dispatcher.add_handler(unknown_handler)


# updater.start_polling()
print 'step1'
#test_announce()
# updater.idle()
inits.bot.polling()
print 'step2'
# updater.stop()
print 'step3'