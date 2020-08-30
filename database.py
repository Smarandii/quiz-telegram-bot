from models import User


def get_user(telegram_id_need_to_be_found):
    base = 'users.csv'
    with open(base, 'r') as file:
        for user_line in file:
            number, telegram_id, name, sex, username, phone_number, email, answers = user_line.split(',')
            if str(telegram_id_need_to_be_found) == telegram_id:
                print('User founded')
                return User(telegram_id=telegram_id, username=username, number=number,
                            phone_number=phone_number, email=email, sex=sex, name=name, answers=answers)