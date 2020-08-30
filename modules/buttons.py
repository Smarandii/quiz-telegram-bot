from telebot import types


def one_button_keyboard(text, callback_line, url=None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text=text, callback_data=callback_line, url=url)
    keyboard.add(button)
    return keyboard


def keyboard_maker(number_of_buttons: int,
                   text_for_each_button: list,
                   callback_data: list,
                   url_for_each_button: list = None,
                   without_back_btn: bool = False):
    if url_for_each_button is None:
        url_for_each_button = [None, None, None, None]
    keyboard = types.InlineKeyboardMarkup()
    if number_of_buttons > 1:
        butt1 = types.InlineKeyboardButton(text=text_for_each_button[0],
                                           callback_data=callback_data[0],
                                           url=url_for_each_button[0])
        keyboard.add(butt1)
    if number_of_buttons >= 2:
        butt2 = types.InlineKeyboardButton(text=text_for_each_button[1],
                                           callback_data=callback_data[1],
                                           url=url_for_each_button[1])
        keyboard.add(butt2)
    if number_of_buttons >= 3:
        butt3 = types.InlineKeyboardButton(text=text_for_each_button[2],
                                           callback_data=callback_data[2],
                                           url=url_for_each_button[2])
        keyboard.add(butt3)
    if number_of_buttons >= 4:
        butt4 = types.InlineKeyboardButton(text=text_for_each_button[3],
                                           callback_data=callback_data[3],
                                           url=url_for_each_button[3])
        keyboard.add(butt4)
    if not without_back_btn:
        backbutton = types.InlineKeyboardButton(text="Начать сначала", callback_data="start_test")
        keyboard.add(backbutton)
    return keyboard


class HelpMenu:
    MENU_CONTENT = {'start': 'СТАРТ!'}

    def __init__(self):
        pass

    def get_buttons(self):
        markup = types.ReplyKeyboardMarkup()
        start_button = types.KeyboardButton(self.MENU_CONTENT['start'])
        markup.row(start_button)
        return markup


class ResultMenu:
    MENU_CONTENT = {'result': 'Получить результат',
                    'close': ''}

    def __init__(self):
        pass

    def get_buttons(self):
        markup = types.ReplyKeyboardMarkup()
        result_button = types.KeyboardButton(self.MENU_CONTENT['result'])
        markup.row(result_button)
        return markup


START_TEST_BUTTON = one_button_keyboard('Пройти тест', 'start_test')
GET_RESULT_BUTTON = one_button_keyboard('Получить результат', 'get_result')
CONTACTS_KEYBOARD = keyboard_maker(3,
                                   ['Инстаграм Организаторов', 'Инстарам Проекта', 'Наш сайт'],
                                   ['None', 'None', 'None', 'None'],
                                   url_for_each_button=['',
                                                        '',
                                                        '',
                                                        ''],
                                   without_back_btn=True)
