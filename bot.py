import telebot

from config import TOKEN, keys
from extensions import Convertor, ConvertionException

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате: \
"название валюты" "в какую валюту перевести" "сколько валюты хотите перевести". \
 \nСписок доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные Валюты \n______________________'
    for k in keys.keys():
        text = '\n'.join((text, k))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Не верное количество аргументов.')

        base, quote, amount = value
        text = Convertor.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ощибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:

        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)