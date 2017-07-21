# -*- coding: utf-8 -*-



from inits import bot
from telebot import types
import sqlite3
import emoji
from Duel import Duel
from Duel import Duelmarkup
from Duel import Defaultmarkup



def generate_duel_code(id,time):
    return '#' + id[0:3] + time[0:3] + id[3:] + time[3:]

def init_inline_func(InvDuelCode):
    @bot.inline_handler(lambda query: query.query == InvDuelCode)
    def query_text(inline_query):
        try:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Accept", callback_data=InvDuelCode))
            tempAmnt=give_duel_amnt(InvDuelCode)
            if(give_duel_amnt(InvDuelCode) == -1):
                raise Exception("Looks like the duel is not in the file")
            r = types.InlineQueryResultArticle('1', 'Invite to CookieDuel',
                                               types.InputTextMessageContent("Hi,\nI Like to invite you to a CookieDuel\non "  + str(tempAmnt) + emoji.emojize(emoji.demojize(u'❤'))),
                                                                             reply_markup=markup)
            bot.answer_inline_query(inline_query.id, [r])
            print "Made a duel request with ID: " + InvDuelCode
        except Exception as e:
            print(e)

def store_duel(FirstId,Amnt,CallBId,SecondId=0):
    con = sqlite3.connect('duel.sqlite')
    cur = con.cursor()
    con.execute("PRAGMA ENCODING = 'utf8';")
    # print cur.execute("PRAGMA table_info(Duel);")
    # cur.execute("CREATE TABLE Duel(First_Id INT, amount INT, Second_Id INT)")
    try:
        cur.execute("INSERT INTO Duel VALUES (?, ?, ?, ?);",
                   (FirstId, Amnt, CallBId, SecondId))
        con.commit()
        print "stored!!!"
    except:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Duel(First_Id INT, amount INT,call_back_code TEXT, Second_Id INT);")
        cur.execute("INSERT INTO Duel VALUES (?, ?, ?, ?);",
                    (FirstId, Amnt, CallBId, SecondId))
        con.commit()
        print "failed!!!!!!!!"

    con.close()

def update_duel(CallBId,SecondId):
    if(is_in_duel(SecondId)):# second person is in Duel
        return 5
    con = sqlite3.connect('duel.sqlite')
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM Duel WHERE call_back_code=\"{0}\"".format(CallBId))
    except Exception:
        print "No table called Duel"
        print Exception
        return False
    con.execute("PRAGMA ENCODING = 'utf8';")
    con.text_factory = str
    row = cur.fetchone()
    if row!=None:
        if row[0]==SecondId:
            con.close()
            return 2
        elif is_in_duel(row[0]):# first person is in Duel
            con.close()
            return 4
        elif (give_duel_amnt(CallBId) > give_user_like(row[0])):# first person doesn't have enouph likes
            con.close()
            return 6
        else:
            if(give_duel_amnt(CallBId) <= give_user_like(SecondId)):
                cur.execute("UPDATE Duel SET Second_Id=? WHERE call_back_code=?", (SecondId, CallBId))
                con.close()
                return 1
            else:
                con.close()
                return 3
    else:
        con.close()
        return 0
    return 0

def give_duel_starter(call_back_data):
    con = sqlite3.connect('duel.sqlite')
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM Duel WHERE call_back_code=\"{0}\"".format(call_back_data))
    except Exception:
        print "No table called Duel"
        print Exception
        return ""
    con.execute("PRAGMA ENCODING = 'utf8';")
    con.text_factory = str
    row = cur.fetchone()
    if row != None:
        con.close()
        return row[0]
    else:
        con.close()
    return ""

def give_duel_amnt(call_back_data):
    con = sqlite3.connect('duel.sqlite')
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM Duel WHERE call_back_code=\"{0}\"".format(call_back_data))
    except Exception:
        print "No table called Duel"
        print Exception
        return -1
    con.execute("PRAGMA ENCODING = 'utf8';")
    con.text_factory = str
    row = cur.fetchone()
    if row != None:
        con.close()
        return row[1]

    con.close()
    return -1

def find_disp_name(user_Id):
    cn = sqlite3.connect("zthb.sqlite")
    cur = cn.cursor()
    cur.execute("SELECT * FROM cookie_giver")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    rows = cur.fetchall()
    output=""

    for row in rows:
        if(row[0]==user_Id):
            if(row[1]!=None):
                output = '@' + row[1]
            else:
                output = row[2] + ' ' + row[3]
            break
    cn.close()
    return output

def give_user_like(userId):
    cn = sqlite3.connect("zthb.sqlite")
    cur = cn.cursor()
    cur.execute("SELECT * FROM cookie_giver WHERE u_id={0}".format(userId))
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    row = cur.fetchone()
    cn.close()
    return row[6]

def add_likes(userId,Like_Amnt):
    cn = sqlite3.connect("zthb.sqlite")
    cur = cn.cursor()
    cur.execute("SELECT * FROM cookie_giver WHERE u_id={0}".format(userId))
    cn.execute("PRAGMA ENCODING = 'utf8';")
    # cur.row_factory = lite.Row
    cn.text_factory = str
    row = cur.fetchone()
    if row != None:
        userLikes = row[6] + Like_Amnt
        cur.execute("UPDATE cookie_giver SET u_likes=? WHERE u_id=?", (userLikes, userId))
        cn.commit()
        bot.send_message(userId, "Now me {0}❤ you".format(userLikes))
    cn.close()

Duel_list=[]

def finish_duel(Duel_ele):
    WinID = Duel_ele.winner()[0]
    LoseID = Duel_ele.looser()[0]

    add_likes(WinID,Duel_ele.Amnt)
    add_likes(LoseID,-Duel_ele.Amnt)

    Duel_list.remove(Duel_ele)

def is_in_duel(UsrId):
    for Duel_ele in Duel_list:
        if(Duel_ele.F_Id == UsrId or Duel_ele.S_Id == UsrId):
            return True
    return False

def get_duel_move(UsrId,moveNum):
    for Duel_ele in Duel_list:
        if(Duel_ele.F_Id == UsrId or Duel_ele.S_Id == UsrId):
            if(Duel_ele.F_Id == UsrId):
                if(Duel_ele.F_temp_Move == 0):
                    bot.send_message(Duel_ele.S_Id, find_disp_name(UsrId) + " has made its move")
                else:
                    bot.send_message(Duel_ele.S_Id, find_disp_name(UsrId) + " has changed its move")
                    bot.send_message(Duel_ele.F_Id, "You have changed your move")
            else:
                if (Duel_ele.S_temp_Move == 0):
                    bot.send_message(Duel_ele.F_Id, find_disp_name(UsrId) + " has made its move")
                else:
                    bot.send_message(Duel_ele.F_Id, find_disp_name(UsrId) + " has changed its move")
                    bot.send_message(Duel_ele.S_Id, "You have changed your move")


            print "PART1"
            Duel_ele.solo_move(UsrId,moveNum)
            if(Duel_ele.Ready_to_move()):
                resMSG=Duel_ele.compute_solo_moves()

                CM_MSG=Duel_ele.CookieM_MSG
                bot.send_message(Duel_ele.F_Id, CM_MSG)
                bot.send_message(Duel_ele.S_Id, CM_MSG)

                bot.send_message(Duel_ele.F_Id, resMSG)
                bot.send_message(Duel_ele.S_Id, resMSG)

                if(Duel_ele.winner() != None):
                    winMSG= "Results:"\
                            + "\n- " + Duel_ele.winner()[1] + " will get " + str(Duel_ele.Amnt) + emoji.emojize(emoji.demojize(u'❤')) \
                            + "\n- " + Duel_ele.looser()[1] + " will get " + str(Duel_ele.Amnt) + emoji.emojize(emoji.demojize(u'💔'))
                    bot.send_message(Duel_ele.F_Id, winMSG, reply_markup=Defaultmarkup)
                    bot.send_message(Duel_ele.S_Id, winMSG, reply_markup=Defaultmarkup)
                    finish_duel(Duel_ele)
            return


@bot.message_handler(commands=['abortduel'])
def abort_duel(message):
    UsrId=message.from_user.id

    for Duel_ele in Duel_list:
        if(Duel_ele.F_Id == UsrId or Duel_ele.S_Id == UsrId):
            bot.send_message(Duel_ele.F_Id, "The Duel has been aborted by " + find_disp_name(UsrId), reply_markup=Defaultmarkup)
            bot.send_message(Duel_ele.S_Id, "The Duel has been aborted by " + find_disp_name(UsrId), reply_markup=Defaultmarkup)
            Duel_list.remove(Duel_ele)
            return True

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):

    rec_data=call.data
    user_Id=call.from_user.id
    print call

    if rec_data[0]=='#':
        result=update_duel(rec_data,user_Id)
        if result==1:
            print "We have a duel!!!"
            First_Id=give_duel_starter(rec_data)
            name_First_Id=find_disp_name(First_Id)
            name_user_Id=find_disp_name(user_Id)
            if(name_user_Id==""):
                bot.send_message(First_Id, "An unknown user(" + call.from_user.first_name + " " + call.from_user.last_name + ") wants to duel with you.\nTell him or her to start the bot")
            else:
                temp=give_duel_amnt(rec_data)
                if(temp == -1):
                    bot.send_message(user_Id, "Sorry can't start this Duel please try another or make a new one")
                Duel_list.append(Duel(First_Id,user_Id,temp,name_First_Id,name_user_Id))
                bot.send_message(user_Id,"You are now in a CookieDuel with " + name_First_Id, reply_markup=Duelmarkup)
                bot.send_message(First_Id, "You are now in a CookieDuel with " + name_user_Id, reply_markup=Duelmarkup)

        elif result==2:
            bot.send_message(user_Id,"Sorry, you can't duel with your self :))")
            print "Sorry, you can't duel with your self :))"
        elif result==3:
            bot.send_message(user_Id, "Sorry, your not able to duel, Looks like you don't have enough likes :)" +
                             "\nyou currently have " + str(give_user_like(user_Id)) + emoji.emojize(emoji.demojize(u'❤')))
            print "Sorry, your not able to duel, I think you don't have enough likes :)"
        elif result==4:# first user is in a duel
            bot.send_message(user_Id, "Sorry, The user that you want to duel with, is already in a Duel" +
                             "\nTry to tell him or her to finish the Duel or /abort it\nyou can also start a duel with /invite")
            print "user came a little late"
        elif result==5:# seconed user is in a duel
            bot.send_message(user_Id, "Sorry, you're already in a duel")
            print "already in duel"
        elif result==6:
            bot.send_message(user_Id, "Sorry, the user that you want to duel with, doesn't have enough likes")
            print "First user is poor now"
        else:
            bot.send_message(user_Id, "Sorry can't start this Duel please try another or make a new one")
            print "error in duel starting..."

@bot.message_handler(commands=['showcookies'])
def show_markup(call):
    if(is_in_duel(call.from_user.id)):
        markup=Duelmarkup
    else:
        markup=Defaultmarkup
    bot.send_message(call.from_user.id,"Here is the menu",reply_markup=markup)

@bot.message_handler(commands=['invite'])
def send_welcome(message):
    InvDuelCode=generate_duel_code(str(message.from_user.id),str(message.date))

    #find the amount of likes:
    tempstr=message.text.split()
    try:
        StrAmnt=tempstr[1]
        Amnt=int(StrAmnt)
        if(Amnt<=0):
            raise Exception
        if(give_user_like(message.from_user.id) < Amnt):
            raise IOError("User doesn't have the enough likes")
    except IOError as valerr:
        print valerr
        bot.send_message(message.chat.id, "Sorry you don't have enough likes!")
        return
    except:
        bot.send_message(message.chat.id, "Please enter an amount in number")
        return

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("invite someone",switch_inline_query=InvDuelCode ))
    bot.send_message(message.chat.id, "Hi,\nI Like to invite you to a CookieDuel\non " + str(Amnt) + emoji.emojize(emoji.demojize(u'❤')), reply_markup=markup)

    init_inline_func(InvDuelCode)
    store_duel(message.from_user.id,Amnt,InvDuelCode)

def get_Duel_MSG(message):
    print message.text
    if(not is_in_duel(message.from_user.id)):
        return False
    if (message.text == emoji.emojize(emoji.demojize(u'🍪') + 'Banana Cookie' + emoji.demojize(u'🍌'))):
        print "Got M1"
        get_duel_move(message.from_user.id,1)
        return True
    elif (message.text == emoji.emojize(emoji.demojize(u'🍪') + 'Chocolate Chip Cookie' + emoji.demojize(u'🍫'))):
        print "Got M2"
        get_duel_move(message.from_user.id,2)
        return True
    elif (message.text == emoji.emojize(emoji.demojize(u'🍪') + 'Vanilla Ice-Cream Cookie' + emoji.demojize(u'🍦'))):
        print "Got M3"
        get_duel_move(message.from_user.id,3)
        return True
    return False

#print generate_duel_code("12343345","773457")
# store_duel(10,10,"hello")
# print update_duel("hello",134)

# bot.polling()
# while(1):
#     try:
#         bot.polling()
#     except:
#         print "Little crash..."
#