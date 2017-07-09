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

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("OMGGG!!!", callback_data="CALLB_DA"))
    markup.add(types.InlineKeyboardButton("Yahoo", url="http://www.yahoo.com"))
    bot.edit_message_text("EDITED!!!",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    #reply = "Yello!!!"
    #bot.reply_to(message, reply)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Google",callback_data="CALLB_DA"))
    markup.add(types.InlineKeyboardButton("Yahoo", url="http://www.yahoo.com"))
    bot.send_message(message.chat.id, "SAMPLE TEXT", disable_notification=True, reply_markup=markup)



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