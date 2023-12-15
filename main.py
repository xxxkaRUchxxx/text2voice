import telebot
import key

bot = telebot.TeleBot(key.tg_token, parse_mode='html')


@bot.message_handler(commands=['start'])
def start_mes(message):
    pass
