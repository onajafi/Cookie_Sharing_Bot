#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
from datetime import timedelta
from telebot import types
import telebot
import logging
import emoji
import inits


tb = telebot.TeleBot(inits.bot_address)

announce_message="""Hey everybody,
We have updated the bot by adding a challenging feature!
You are now able to invite friends to a Cookie Duel, press /howtoduel for more informations.
Type /help to see the new commands.
and type /showcookies to see the reply buttons.

enjoy feeding
.B"""

def announce_to_all():
    cn = sqlite3.connect("zthb.sqlite")
    cur = cn.cursor()
    cur.execute("SELECT * FROM cookie_giver")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    rows = cur.fetchall()
    templib = []
    for row in rows:
        try:
            if (row[0] not in templib):
                templib.append(row[0])
                if(True):
                    tb.send_message(chat_id=row[0], text=announce_message)
                    print "sent for " + row[1]
        except:
            pass
    cn.close()



announce_to_all()

