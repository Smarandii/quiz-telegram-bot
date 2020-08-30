from time import sleep
from telebot import TeleBot

import sendemail
from buttons import *
from models import User
from database import get_user
import content

bot = TeleBot(content.TOKEN)
h_menu = HelpMenu()
r_menu = ResultMenu()


def send_forms(user: User):
    try:
        form = user.get_form_message()
        # bot.send_message(content.client_id, text=form)
        sendemail.send_forms('olegsmarandi@gmail.com')
        sendemail.send_forms('treningi-biz@mail.ru')
    except Exception as er:
        bot.send_message(content.admin_id, text=er)


def journalist(call):
    # call.data = f"{sex}_q{N}a{N}"
    sex, answer = call.data.split('_')
    current_q = call.data[-3]
    next_q = sex + "_q" + str(int(current_q) + 1)

    if sex == 'start':
        bot.send_message(chat_id=call.message.chat.id,
                         text='Жми!',
                         reply_markup=START_TEST_BUTTON)

    elif current_q == '6' and sex == 'man':
        number_of_buttons = 2
        callback = [f'result_q7a{i}' for i in range(1, number_of_buttons + 1)]
        button_text = [content.man_answers[f'q{6}a{i}'] for i in range(1, number_of_buttons + 1)]
        question = content.man_questions[f'q{current_q}']

    elif current_q == '6' and sex == 'woman':
        number_of_buttons = 2
        callback = [f'result_q7a{i}' for i in range(1, number_of_buttons + 1)]
        button_text = [content.woman_answers[f'q{6}a{i}'] for i in range(1, number_of_buttons + 1)]
        question = content.woman_questions[f'q{current_q}']

    elif sex == 'man':
        number_of_buttons = content.number_of_answers_man[current_q]
        button_text = [content.man_answers[f'q{current_q}a{i}'] for i in range(1, number_of_buttons + 1)]
        question = content.man_questions[f'q{current_q}']
        callback = [next_q + f'a{i}' for i in range(1, number_of_buttons + 1)]

    elif sex == 'woman':
        number_of_buttons = content.number_of_answers_woman[current_q]
        button_text = [content.woman_answers[f'q{current_q}a{i}'] for i in range(1, number_of_buttons + 1)]
        question = content.woman_questions[f'q{current_q}']
        callback = [next_q + f'a{i}' for i in range(1, number_of_buttons + 1)]

    keyboard = keyboard_maker(number_of_buttons, button_text, callback)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=question, reply_markup=keyboard)
    return answer


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = User(telegram_id=message.chat.id, username=message.chat.username)
    if user.not_in_base():
        user.add_user_in_db()
    message = user.get_welcome_message()
    bot.send_message(chat_id=user.user_id, text=message, reply_markup=START_TEST_BUTTON)


@bot.message_handler(commands=['contacts'])
def send_contacts(message):
    user = User(telegram_id=message.chat.id, username=message.chat.username)
    if user.not_in_base():
        user.add_user_in_db()
    message = content.service_msg['contacts']
    bot.send_message(chat_id=user.user_id, text=message, reply_markup=CONTACTS_KEYBOARD)


@bot.message_handler(content_types=["text"])
def any_msg(message):
    user = User(telegram_id=message.chat.id, username=message.chat.username)
    if user.not_in_base():
        send_welcome(message)
    else:
        user = get_user(message.chat.id)
        if "@" in message.text:
            user.add_email(message.text)
            bot.send_message(chat_id=user.user_id, text=content.service_msg['email'] + message.text)
        elif "+7" in message.text or message.text.isdigit():
            user.add_phone_number(message.text)
            bot.send_message(chat_id=user.user_id, text=content.service_msg['number'] + message.text)
        else:
            user.add_name(message.text)
            bot.send_message(chat_id=user.user_id, text=content.service_msg['name'] + message.text)
        user.rewrite_user_info()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = get_user(telegram_id_need_to_be_found=call.message.chat.id)
    sex, answer = call.data.split('_')
    print(call.data, '----------------------------------------')
    if call.data == "start_test":
        keyboard_main = keyboard_maker(2, ["Мужчина", "Женщина"], ["man_q1aM", "woman_q1aW"],
                                       without_back_btn=True)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите ваш пол:", reply_markup=keyboard_main)

    elif "result_" in call.data:
        user.update_answer(answer)
        user.rewrite_user_info()
        bot.send_message(call.message.chat.id,
                         text=content.service_msg['result'],
                         reply_markup=GET_RESULT_BUTTON)

    elif 'get_result' == call.data:
        if not user.form_filled():
            bot.send_message(chat_id=user.user_id, text=content.service_msg['result'])
        if user.form_filled():
            message = user.get_result_from_answers()
            bot.send_message(chat_id=user.user_id, text=message)
            bot.send_message(chat_id=user.user_id, text=content.service_msg['contacts'], reply_markup=CONTACTS_KEYBOARD)
            if user.not_in_forms():
                user.add_user_in_forms()
                send_forms(user)

    else:
        journalist(call)
        user.add_sex(sex)
        user.update_answer(answer)
        user.rewrite_user_info()
        if user is None:
            print("Can't find that user")


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except ConnectionError as error:
            sleep(15)
