import telebot
import inits
from telebot import types
import sqlite3

bot = telebot.TeleBot(inits.bot_address)

# @bot.inline_handler(func=lambda query: True)
# def inline(query):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     btn = telebot.types.InlineKeyboardButton(text="Button text", callback_data="inline")
#     keyboard.add(btn)
#     r = telebot.types.InlineQueryResultArticle(
#         id="1",
#         title="Title",
#         input_message_content=telebot.types.InputTextMessageContent(message_text="Test"),
#         reply_markup=keyboard
#     )
#     bot.answer_inline_query(query.id, [r], cache_time=10)
#
def generate_duel_code(id,time):
    return '#' + id[0:3] + time[0:3] + id[3:] + time[3:]

def init_inline_func(InvDuelCode):
    @bot.inline_handler(lambda query: query.query == InvDuelCode)
    def query_text(inline_query):
        try:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Challenge accepted", callback_data=InvDuelCode))
            r = types.InlineQueryResultArticle('1', 'Invite to CookieDuel',
                                               types.InputTextMessageContent("Hi,\nI Like to invite you to a CookieDuel"),
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
        else:
            cur.execute("UPDATE Duel SET Second_Id=? WHERE call_back_code=?", (SecondId, CallBId))
            con.close()
            return 1
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


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data == "12341234":
        print "YYYYYYEEEEEEEEEEYYYYYYYYY"
    elif call.data == "Hit_It":
        print call
        print call.message
        print call.from_user.id
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
                bot.send_message(user_Id,"You are now in a cookie duel with " + name_First_Id)
                bot.send_message(First_Id, "You are now in a cookie duel with " + name_user_Id)

        elif result==2:
            print "Sorry, you can't duel with your self :)"
        else:
            print "Sorry, your not able to duel, I think you don't have enough likes :)"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    #reply = "Yello!!!"
    #bot.reply_to(message, reply)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Google", switch_inline_query="LetsRock"))
    markup.add(types.InlineKeyboardButton("Yahoo", callback_data="12341234"))
    bot.send_message(message.chat.id, "SAMPLE TEXT", disable_notification=True, reply_markup=markup)

    print message.text

@bot.message_handler(commands=['invite'])
def send_welcome(message):
    InvDuelCode=generate_duel_code(str(message.from_user.id),str(message.date))

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("invite",switch_inline_query=InvDuelCode ))
    bot.send_message(message.chat.id, "Hi,\nI Like to invite you to a CookieDuel", reply_markup=markup)

    init_inline_func(InvDuelCode)
    store_duel(message.from_user.id,message.date,InvDuelCode)




#print generate_duel_code("12343345","773457")
# store_duel(10,10,"hello")
# print update_duel("hello",134)

bot.polling()
# while(1):
#     try:
#         bot.polling()
#     except:
#         print "Little crash..."
#