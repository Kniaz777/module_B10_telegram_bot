import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту в формате: \n <Название валюты с маленькой буквы> \
<В какую валюту перевести> \
<Количество переводимой валюты> \
Показать список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка ввода\n{e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Выполнение команды не возможно\n{e}')

    else:
        text = f'Цена {amount}, {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
