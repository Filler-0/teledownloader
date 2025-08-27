from configparser import ConfigParser
import telebot
import yt_dlp
import os


URLS = ['https://www.youtube.com/watch?v=pvy9km7g6fw']


CONFIG = ConfigParser()
try:
    CONFIG.read('config.ini')
    TELEGRAM_TOKEN = CONFIG['TELEGRAM']['token']
    SECURE_ID = int(CONFIG['TELEGRAM']['my_chat'])
except:
    pass


bot = telebot.TeleBot(TELEGRAM_TOKEN)


class DownLogger:
    def __init__(self, id, message_id):
        self.chat_id = id
        self.message_id = message_id

    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        bot.edit_message_text(msg, self.chat_id, self.message_id)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download(url, mode, id, message_id=0):
    ydl_opts = {
        'logger': DownLogger(id, message_id),
        'format': 'bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


@bot.message_handler(chat_id=[SECURE_ID], commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Send link to start downloading")


@bot.message_handler(chat_id=[SECURE_ID])
def url_handler(message):

    mes_id = bot.send_message(message.chat.id, "Got the link").message_id

    try:
        download(message.text, "mp3", message.chat.id, mes_id)
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