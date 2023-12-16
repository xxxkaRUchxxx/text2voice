import telebot
import key
import text
import func


bot = telebot.TeleBot(key.tg_token, parse_mode='html')


@bot.message_handler(commands=['start'])
def start_mes(message):
    if message.text == '/start':
        data = func.first_join(message)
        bot.send_message(message.chat.id, text.start.format(message.from_user.first_name, data[0], data[1]))





bot.polling(none_stop=True)