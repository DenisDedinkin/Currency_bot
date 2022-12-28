import telebot
import requests
import json
from config import TOKEN, keys




bot = telebot.TeleBot(TOKEN)




# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате: \
"название валюты" "в какую валюту перевести" "сколько валюты хотите перевести". \
 \nСписок доступных валют: /values'
    bot.reply_to(message, text)


# Обрабатывается все документы и аудиозаписи
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные Валюты \n______________________'
    for k in keys.keys():
        text = '\n'.join((text, k))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    base, quote, amount = message.text.split(' ')
    r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}")
    total_quote = json.loads(r.content)[keys[quote]]
    text = f"Цена {amount} {base} в {quote} - {total_quote}"
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)