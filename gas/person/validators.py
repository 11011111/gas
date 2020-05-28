from django.forms import ValidationError

def user_password(value):
    """
    Проверка пароля на базовую безопастность
    :param value: принимаемый пароль
    :return: value, если он прошел проверку
    """
    #     Кол-во символов больше 8
    #     Пароль содержит не только цифры
    err = [len(value) < 8, value.isdigit()]
    if any(err):
        raise ValidationError('Password isn\'t correct.')
    return value
