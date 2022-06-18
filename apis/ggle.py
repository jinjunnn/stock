# Google 库

# import telebot

# api_key = '5326945934:AAG0AYlJvGI40v9dpFHcvN64gliDDzkqGQI'
# bot = telebot.TeleBot(api_key, parse_mode=None) 

# @bot.message_handler(commands=['start','help'])

# def handle_start_help(message):
#     print(message.chat.id)
#     bot.reply_to(message,'what up')
    
# # bot.polling()
# s = pd.Series(data=[3,2,3,4,5],index=['ts_code', 'cci_12', 'cci_9', 'cci_20', 'date'])

# # 2013737722  这个是我的TELEGRAM ID

# def send_word(_id,_message):
#     bot.send_message(_id, _message)


# google
def send_message_to_tg(message):
    #google请求函数
    url = 'https://asia-east1-jinjunnnnn.cloudfunctions.net/tg'
    # message = {'uid':2013737722,'message':'成功'}
    # message的类型是dict
    result = requests.post(url=url,data=message)
    print(result.content)