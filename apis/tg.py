import telebot

api_key = '5326945934:AAG0AYlJvGI40v9dpFHcvN64gliDDzkqGQI'
bot = telebot.TeleBot(api_key, parse_mode=None) 

# @bot.message_handler(commands=['start','help'])

# def handle_start_help(message):
#     print(message.chat.id)
#     bot.reply_to(message,'what up')
    
# bot.polling()

# 2013737722  这个是我的TELEGRAM ID

def handle_messages(messages):
    for message in messages:
    # Do something with the message
        bot.reply_to(message, 'Hi')

# bot.set_update_listener(handle_messages)
# bot.infinity_polling()

