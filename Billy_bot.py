import random
import bs4
import requests
import telebot
from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError
from telebot import types
from translate import Translator

translator = Translator(from_lang='en', to_lang='ru')
bot = telebot.TeleBot("Bot_token")


def get_weather(city_message):
    try:
        owm = OWM('OWM_token')
        observation = owm.weather_manager().weather_at_place(city_message.text)
        w = translator.translate(observation.weather.detailed_status)
        answer = f"В городе {city_message.text} сейчас {w} \n"
        bot.send_message(city_message.chat.id, answer)
    except NotFoundError:
        bot.send_message(city_message.chat.id, f'Сорян, сладкий, я не знаю такого города')


def get_anekdot():
    z = ''
    s = requests.get('http://anekdotme.ru/random')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    p = b.select('.anekdot_text')
    for x in p:
        s = (x.getText().strip())
        z = z + s + '\n\n'
    return s


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # bot.reply_to(message, "Я робот и я захвачу мир")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Какой у меня шанс на swallow cum сегодня?")
    item2 = types.KeyboardButton("Как дела, Билли?")
    item3 = types.KeyboardButton("Дай совет")
    item4 = types.KeyboardButton("Билли, подскажи погоду")
    item5 = types.KeyboardButton("Расскажи анекдот")

    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id,
                     "\n{0.first_name} приветствую тебя в нашем чате\n Я - <b>{1.first_name}</b> и я окружу тебя любовью".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def first_message(message):
    # if message.chat.type == 'private':
    if message.text == 'Какой у меня шанс на swallow cum сегодня?':
        swallow = random.randint(0, 100)
        if swallow == 100:
            bot.send_message(message.chat.id,
                             '\nБоже мой! Да у нас новый Boss of this gym, твой шанс ' + str(swallow) + '%')
        elif swallow == 69:
            bot.send_message(message.chat.id, '\nЦелых 😏 ' + str(swallow) + '% 👄💦🍆🤼‍♂️')
        elif swallow == 0:
            bot.send_message(message.chat.id, "\nI don't do anal с тобой, шанс 0%")
        elif swallow >= 70:
            bot.send_message(message.chat.id, '\nТы у нас сегодня везунчик! Твой шанс ' + str(swallow) + '%')
        elif swallow <= 30:
            bot.send_message(message.chat.id, '\nСегодня не твой день, дружок-пирожок, шанс ' + str(swallow) + '%((((')
        else:
            bot.send_message(message.chat.id, '\nРовно ' + str(swallow) + '%')

    elif message.text == "Расскажи анекдот" or message.text.lower()[:6] == "анекдо":
        bot.send_message(message.chat.id, get_anekdot())

    elif message.text.lower()[:7] == 'cмешной' or message.text.lower()[:7] == 'хороший':
        bot.send_message(message.chat.id, '\nСпасибо, Dungeon master')

    elif message.text.lower()[:7] == 'спасибо':
        bot.send_message(message.chat.id, '\nЯ твой fucking slave')

    elif message.text.lower() == message.text.lower()[:2] == 'ха' or message.text.lower()[:2] == 'ах':
        bot.send_message(message.chat.id, '\nСоласен, умора вообще')

    elif message.text.lower() == message.text.lower()[:6] == 'фигня' or message.text.lower()[:8] == 'не очень':
        bot.send_message(message.chat.id, '\nСорян, попробую еще((\n')
        bot.send_message(message.chat.id, get_anekdot())

    elif message.text.lower()[:15] == 'рад видеть тебя' or message.text.lower()[:6] == 'привет':
        bot.send_message(message.chat.id,
                         "\nПривет, {0.first_name}, какие люди! Let's celebrate and suck some dick!".format(
                             message.from_user, bot.get_me()))

    elif message.text.lower()[:14] == 'стреляй в меня':
        bot.send_message(message.chat.id,
                         '\nТы сам напросился {0.first_name}. Я достаю свой огромный ствол и...'.format(
                             message.from_user, bot.get_me()))
        shoot = random.randint(1, 6)
        if shoot == 6:
            bot.send_message(message.chat.id,
                             '\nБилли стреляет в {0.first_name} и убивает его'.format(message.from_user, bot.get_me()))
        else:
            bot.send_message(message.chat.id,
                             'Билли стреляет в {0.first_name}, но у него происходит осечка. {0.first_name} выживает'.
                             format(message.from_user, bot.get_me()))

    elif message.text.lower()[:8] == 'как дела':

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
        item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
        item3 = types.InlineKeyboardButton("Тяночку хочу(((", callback_data='tyan')

        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, "Oh, I'm fucking cumming, а ты сам как?", reply_markup=markup)
    elif message.text == 'Дай совет':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Сейчас идет дождь", callback_data='rain')
        item2 = types.InlineKeyboardButton("Сейчас солнечно", callback_data='shiny')

        markup.add(item1, item2)

        bot.send_message(message.chat.id, 'Какая сейчас погода?', reply_markup=markup)

    elif message.text == 'Билли, подскажи погоду':
        bot.send_message(message.chat.id, 'В каком городе ты хочешь узнать погоду?')
        bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(message.chat.id, 'Не понял тебя((')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Наверное ты suck some dick?')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Установил тебе майнер, проверяй))")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Oh, I'm fucking cumming, а ты сам как?", reply_markup=None)
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Тогда stick your finger and be happy')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Установил тебе майнер, проверяй))")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Oh, I'm fucking cumming, а ты сам как?", reply_markup=None)
            elif call.data == 'rain':
                bot.send_message(call.message.chat.id, 'Сиди дома и fisting is 300 bucks')
                bot.answer_callback_query(callback_query_id=call.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Какая сейчас погода?", reply_markup=None)
            elif call.data == 'shiny':
                bot.send_message(call.message.chat.id, "Иди на улицу и Oh shit i'm sorry")
                bot.answer_callback_query(callback_query_id=call.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Какая сейчас погода?", reply_markup=None)
            elif call.data == 'tyan':
                bot.send_message(call.message.chat.id,
                                 'Ты хочешь меня ♂FUCK♂-♂FUCK♂-♂FUCK♂ а я хочу ♂THREE HUNDRED BUCKS♂')
                bot.answer_callback_query(callback_query_id=call.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Oh, I'm fucking cumming, а ты сам как?", reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.infinity_polling()
