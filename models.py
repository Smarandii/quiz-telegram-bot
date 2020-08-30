from content import *


def sort_base_by_number(data_base):
    data_base = sorted(data_base)
    return data_base


class User:
    def __init__(self, telegram_id, username, number=None, name=None, sex=None, email=None,
                 phone_number=None, answers=None):
        self.base_file = "users.csv"
        self.forms_file = 'forms.csv'
        self.user_id = telegram_id
        self.username = username
        self.name = name
        self.sex = sex
        self.phone_number = phone_number
        self.email = email
        self.score = 0
        if number is None:
            self.number = int(self._get_last_number_in_base()) + 1
        else:
            self.number = number
        if answers is None:
            self.answers = {
                            'q1': "-",
                            'q2': "-",
                            'q3': "-",
                            'q4': "-",
                            'q5': "-",
                            'q6': "-",
                            'q7': "-",
                            }
        else:
            self.answers = answers
            print(answers)
            self.answers = self.str_answer_to_dict()

    def __str__(self):
        return f"{self.number},{self.user_id},{self.name},{self.sex},{self.username}," \
                             f"{self.phone_number},{self.email},{self.get_str_answers()}\n"

    def add_phone_number(self, number: str):
        self.phone_number = number

    def add_email(self, email: str):
        self.email = email

    def change_base_file(self, filename: str):
        self.base_file = filename

    def add_sex(self, sex: str):
        self.sex = sex

    def add_name(self, name: str):
        self.name = name

    def update_answer(self, pair):
        question = pair[0:2]
        answer = pair[-1]
        self.answers[question] = answer

    def get_str_answers(self):
        string = ''
        for question in self.answers:
            string += question + ":" + self.answers[question] + " "
        return string

    def get_answers_for_form(self) -> str:
        answers = self._get_str_answers_for_form()
        answers = answers.split(" ")
        answers_separated_with_comma = ''
        for answer in answers:
            if answer != '':
                try:
                    if self.sex == 'woman':
                        answers_separated_with_comma += woman_answers[answer].replace(',', '') + ","
                    if self.sex == 'man':
                        answers_separated_with_comma += man_answers[answer].replace(',', '') + ","
                except ValueError or KeyError as er:
                    print(er)
                    continue
        return answers_separated_with_comma[0:-1:]

    def str_answer_to_dict(self):
        # str = 'q1:- q2:1 q3:- q4:- q5:- q6:-'
        answers = self.answers
        tmp_list = answers.split(" ")
        tmp_list.pop(-1)
        print(tmp_list)
        dict_answers = {i.split(":")[0]: i.split(":")[1] for i in tmp_list}
        print(dict_answers)
        return dict_answers

    def show_telegram_id(self):
        return f"{self.user_id}"

    def _get_last_number_in_base(self):
        with open(self.base_file, 'r') as file:
            for user_line in file:
                number, telegram_id, name, sex, username, phone_number, email, answers = user_line.split(',')
        return number

    def add_user_in_db(self):
        with open(self.base_file, 'a') as file:
            data_base_line = f"{self.number},{self.user_id},{self.name},{self.sex},{self.username}," \
                             f"{self.phone_number},{self.email},{self.get_str_answers()}\n"
            file.write(data_base_line)

    def add_user_in_forms(self):
        with open(self.forms_file, 'a') as file:
            forms_line = f"{self.name},{self.sex},{self.username}," \
                             f"{self.phone_number},{self.email},{self.get_answers_for_form()}\n"
            print(forms_line)
            file.write(forms_line)

    def not_in_base(self):
        with open(self.base_file, 'r') as file:
            for user_line in file:
                number, telegram_id, name, sex, username, phone_number, email, answers = user_line.split(',')
                if str(self.user_id) == telegram_id:
                    print('User already registered')
                    return False
        return True

    def not_in_forms(self):
        with open(self.forms_file, 'r') as file:
            for user_line in file:
                name, sex, username, phone_number, email, a1, a2, a3, a4, a5, a6 = user_line.split(',')
                if str(self.phone_number) == phone_number:
                    print('User already registered')
                    return False
        return True

    def rewrite_user_info(self):
        data_base = []
        data_base_line = f"{self.number},{self.user_id},{self.name},{self.sex},{self.username}," \
                         f"{self.phone_number},{self.email},{self.get_str_answers()}\n"
        with open(self.base_file, 'r') as file:
            user_line_number = self.number
            for user_line in file:
                number, telegram_id, name, sex, username, phone_number, email, answers = user_line.split(',')
                if user_line_number == number:
                    data_base.append(data_base_line)
                else:
                    data_base.append(user_line)

            data_base = sort_base_by_number(data_base)
            i = data_base.index(data_base_head)
            data_base.insert(0, data_base.pop(i))
        with open(self.base_file, 'w') as file:
            for user_line in data_base:
                file.write(user_line)

    def get_welcome_message(self):
        if self.username is not None:
            message = f'''Привет, {self.username}! 
Я - чатбот Лёва, твой "второй пилот" в непредсказуемом мире отношений. Знаю много, болтаю мало!😎
А как твои дела? Пройди мой небольшой тест и мы вместе это выясним!'''
        else:
            message = f'''Привет! 
Я - чатбот Лёва, твой "второй пилот" в непредсказуемом мире отношений. Знаю много, болтаю мало!😎
А как твои дела? Пройди мой небольшой тест и мы вместе это выясним!'''
        return message

    def form_filled(self):
        print(self.phone_number, self.email, self.name)
        return self.phone_number is not None and self.email is not None and self.name is not None \
               and self.phone_number != 'None' and self.email != 'None' and self.name != 'None'

    def _get_man_result(self):
        result = 0
        answers = self.get_str_answers()
        answers_list = answers.split(" ")
        for answer in answers_list:
            try:
                result += man_points[answer]
            except KeyError:
                pass
        print(result)
        if result == 100:
            return result
        if 99 >= result >= 80:
            return 80
        if 79 >= result >= 60:
            return 60
        if 59 >= result >= 0:
            return 0

    def _get_woman_result(self):
        result = 0
        answers = self.get_str_answers()
        answers_list = answers.split(" ")
        for answer in answers_list:
            try:
                result += woman_points[answer]
            except KeyError:
                pass
        print(result)
        if result == 100:
            return result
        if 99 >= result >= 80:
            return 80
        if 79 >= result >= 60:
            return 60
        if 59 >= result >= 0:
            return 0

    def get_result_from_answers(self):
        result = None
        if self.sex == 'man':
            result = self._get_man_result()
            message = man_results[result]
            return message
        if self.sex == 'woman':
            result = self._get_woman_result()
            message = woman_results[result]
            return message
        else:
            return man_results[result]

    def get_form_message(self):
        message = f"{self.name},{self.sex},{self.username}," \
                  f"{self.phone_number},{self.email},{self.get_answers_for_form()}\n"
        return message

    def _get_str_answers_for_form(self):
        answers = self.get_str_answers()
        answers = answers.split(" ")
        answers.pop(0)
        # q1a1 q2a1 q3a1 q4a1 q5a1 q6a1
        answers_for_form = ''
        for answer in answers:
            if answer != '':
                question_n, answer_n = answer.split(":")
                answers_for_form += f"q{int(question_n[-1]) - 1}a{answer_n} "
        return answers_for_form

