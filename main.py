from configparser import ConfigParser
import telebot
import os
import time


CONFIG = ConfigParser()
try:
    CONFIG.read('config.ini')
    TELEGRAM_TOKEN = CONFIG['TELEGRAM']['token']
    SECURE_ID = int(CONFIG['TELEGRAM']['my_chat'])
except:
    pass


bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(chat_id=[SECURE_ID], commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Send link to start downloading")


@bot.message_handler(chat_id=[SECURE_ID])
def url_handler(message):

    mes_id = bot.send_message(message.chat.id, "Got the link").message_id

    try:
        os.popen(f'yt-dlp {message.text} -t mp3 --cookies cookies.txt > output.txt')
        time.sleep(1)
        new = ''
        while 'Deleting' not in new:
            last = new
            new = open('output.txt', 'r').readlines()[-1]
            if last != new:
                bot.edit_message_text(new.strip(), message.chat.id, mes_id)
        bot.edit_message_text("Sending file...", message.chat.id, mes_id)
        filename = list(filter(lambda x: '.mp3' in x, os.listdir()))[0]

        with open(filename, 'rb') as f:
            bot.send_audio(message.chat.id, f)
        
        os.remove(filename)
        
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, "????")


bot.add_custom_filter(telebot.custom_filters.ChatFilter())
bot.infinity_polling()