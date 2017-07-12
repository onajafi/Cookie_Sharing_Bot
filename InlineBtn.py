import telebot
import inits
from telebot import types

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
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data == "inline":
        print(call)
    print "call back is called!!!"
    print "with the data: " + str(call.data)
    print call
    print "and by the user: " + call.from_user.username + ' ' + call.from_user.first_name + ' ' + call.from_user.last_name

    # markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton("OMGGG!!!", callback_data="Done"))
    # markup.add(types.InlineKeyboardButton("Yahoo", url="http://www.yahoo.com"))
    # bot.edit_message_text("EDITED!!!",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    #reply = "Yello!!!"
    #bot.reply_to(message, reply)
    markup = types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton('Share', switch_inline_query='ccy'));
    markup.add(types.InlineKeyboardButton("Google",switch_inline_query='ccy'))
    markup.add(types.InlineKeyboardButton("Yahoo", url="http://www.yahoo.com"))
    bot.send_message(message.chat.id, "SAMPLE TEXT", disable_notification=True, reply_markup=markup)
    print message.text

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    print "got " + inline_query.data

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    print "hehehe"
    try:
        print "imhere"
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


# @bot.inline_handler(lambda query: len(query.query) is 0)
# def default_query(inline_query):
#     try:
#         r = types.InlineQueryResultArticle('1', 'default', types.InputTextMessageContent('default'))
#         bot.answer_inline_query(inline_query.id, [r])
#     except Exception as e:
#         print(e)
#
#     def test_send_message_with_inlinemarkup(self):
#         text = 'CI Test Message'
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton("Google", url="http://www.google.com"))
#         markup.add(types.InlineKeyboardButton("Yahoo", url="http://www.yahoo.com"))
#         ret_msg = bot.send_message(CHAT_ID, text, disable_notification=True, reply_markup=markup)
#         assert ret_msg.message_id

bot.polling()