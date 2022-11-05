import random
import logging
import requests
from telebot import types, TeleBot
from bs4 import BeautifulSoup
from config import OWM_TOKEN, BOT_TOKEN
from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError
from translate import Translator
from phrases import phrases

logging.basicConfig(level=logging.INFO)
translator = Translator(from_lang="en", to_lang="ru")
bot = TeleBot(BOT_TOKEN)


def get_weather(city_message):
    """Function for getting weather forecast"""
    try:
        owm = OWM(OWM_TOKEN)
        observation = owm.weather_manager().weather_at_place(city_message.text)
        weather = translator.translate(observation.weather.detailed_status)
        answer = f"В городе {city_message.text} сейчас {weather} \n"
        logging.info(f"Билли сказал какая погода в городе {city_message.text}")
        bot.send_message(city_message.chat.id, answer)
    except NotFoundError:
        bot.send_message(city_message.chat.id, random.choice(phrases["wrong_city"]))


def get_joke():
    """Function for getting a random joke"""
    s = requests.get("http://anekdotme.ru/random")
    b = BeautifulSoup(s.text, "html.parser")
    p = b.select(".anekdot_text")
    for x in p:
        s = (x.getText().strip())
    return s


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    # bot.reply_to(message, "")
    item1 = types.KeyboardButton("Какой у меня шанс на swallow cum сегодня?")
    item2 = types.KeyboardButton("Как дела, Билли?")
    item3 = types.KeyboardButton("Дай совет")
    item4 = types.KeyboardButton("Билли, подскажи погоду")
    item5 = types.KeyboardButton("Расскажи анекдот")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id,
                     "\nПриветствую тебя в нашем чате\n Я - <b>{1.first_name}</b> и я окружу тебя любовью"
                     .format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def message_function(message):
    user_message = message.text.lower()
    user_message = [c for c in user_message if c in "абвгдеёжзийклмнопрстуфхцчшщъьэюя abcdefghijklmnopqrstuvwxyz"]
    user_message = "".join(user_message)

    if user_message == "какой у меня шанс на swallow cum сегодня":
        swallow = random.randint(0, 100)
        if swallow == 100:
            bot.send_message(message.chat.id, f"\nБоже мой! Да у нас новый Boss of this gym, твой шанс {str(swallow)}%")
        elif swallow == 69:
            bot.send_message(message.chat.id, f"\nЦелых 😏 {str(swallow)} % 👄💦🍆🤼‍♂️")
        elif swallow == 0:
            bot.send_message(message.chat.id, "\nI don't do anal с тобой, шанс 0%")
        elif swallow >= 70:
            bot.send_message(message.chat.id, f"\nТы у нас сегодня везунчик! Твой шанс {str(swallow)}%")
        elif swallow <= 30:
            bot.send_message(message.chat.id, f"\nСегодня не твой день, дружок-пирожок, шанс {str(swallow)}%((((")
        else:
            bot.send_message(message.chat.id, f"\nРовно {str(swallow)}%")

    elif user_message[:13] == "расскажи анек" or user_message[:6] == "анекдо":
        bot.send_message(message.chat.id, get_joke())
        logging.info("Билли рассказал анекдот")

    elif user_message[:5] == "фигня" or user_message[:5] == "не оч":
        bot.send_message(message.chat.id, f"\n{random.choice(phrases['other_joke'])}\n")
        bot.send_message(message.chat.id, get_joke())
        logging.info("Билли рассказал анекдот")

    elif user_message[:6] == "смешно" or user_message[:7] == "хороший":
        bot.send_message(message.chat.id, "\n" + random.choice(phrases["good_joke"]))

    elif user_message[:7] == "спасибо":
        bot.send_message(message.chat.id, "\n" + random.choice(phrases["thanks"]))

    elif user_message[:2] == "ха" or user_message[:2] == "ах":
        bot.send_message(message.chat.id, "\n" + random.choice(phrases["hahaha"]))

    elif user_message[:15] == "рад видеть тебя" or user_message[:6] == "привет":
        bot.send_message(message.chat.id,
                         "\nПривет, {0.first_name}, какие люди! Let's celebrate and suck some dick!".format(
                             message.from_user, bot.get_me()))

    elif user_message[:6] == "пока" or user_message[:6] == "прощай":
        bot.send_message(message.chat.id, random.choice(phrases["goodbye"]))

    elif user_message[:7] == "стреляй":
        bot.send_message(message.chat.id,
                         "\nТы сам напросился {0.first_name}. Я достаю свой огромный ствол и...".format(
                             message.from_user, bot.get_me()))
        shoot = random.randint(1, 6)
        if shoot == 6:
            bot.send_message(message.chat.id, "\nБилли стреляет в {0.first_name} и убивает его"
                             .format(message.from_user, bot.get_me()))
        else:
            bot.send_message(message.chat.id,
                             "Билли стреляет в {0.first_name}, но у него происходит осечка. {0.first_name} выживает".
                             format(message.from_user, bot.get_me()))

    elif user_message[:8] == "как дела":
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Хорошо", callback_data="good")
        item2 = types.InlineKeyboardButton("Не очень", callback_data="bad")
        item3 = types.InlineKeyboardButton("Тяночку хочу(((", callback_data="tyan")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, random.choice(phrases["billy_mood"]), reply_markup=markup)

    elif user_message[:9] == 'дай совет':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Сейчас идет дождь", callback_data="rain")
        item2 = types.InlineKeyboardButton("Сейчас солнечно", callback_data="shiny")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Какая сейчас погода?", reply_markup=markup)

    elif user_message == "билли подскажи погоду" or user_message[:6] == "погода":
        bot.send_message(message.chat.id, "В каком городе ты хочешь узнать погоду?")
        bot.register_next_step_handler(message, get_weather)

    else:
        plug = random.choice(phrases["plug_phrases"])
        bot.send_message(message.chat.id, plug)

    logging.info("Билли ответил на сообщение")


@bot.callback_query_handler(func=lambda call: True)
def callback_func(call):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Oh, I'm fucking cumming, а ты сам как?", reply_markup=None)
        if call.message:
            if call.data == "good":
                bot.send_message(call.message.chat.id, random.choice(phrases["good"]))
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Установил тебе майнер, проверяй))")
            elif call.data == "bad":
                bot.send_message(call.message.chat.id, random.choice(phrases["bad"]))
            elif call.data == "tyan":
                bot.send_message(call.message.chat.id, random.choice(phrases["tyan"]))
            elif call.data == "rain":
                bot.send_message(call.message.chat.id, random.choice(phrases["rainy"]))
            elif call.data == "shiny":
                bot.send_message(call.message.chat.id, random.choice(phrases["shiny"]))

        bot.answer_callback_query(callback_query_id=call.id)
        logging.info("Билли ответил на сообщение")

    except Exception as e:
        print(repr(e))


bot.infinity_polling()
