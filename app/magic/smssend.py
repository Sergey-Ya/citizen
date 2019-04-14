#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

if sys.version_info[0] == 2:
    from urllib2 import urlopen, URLError
    from urllib import quote
if sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.error import URLError
    from urllib.parse import quote

servicecodes = {
    100: "Сообщение принято к отправке. На следующих строчках вы найдете идентификаторы отправленных сообщений в том же порядке, в котором вы указали номера, на которых совершалась отправка.",
    200: "Неправильный api_id",
    201: "Не хватает средств на лицевом счету",
    202: "Неправильно указан получатель",
    203: "Нет текста сообщения",
    204: "Имя отправителя не согласовано с администрацией",
    205: "Сообщение слишком длинное (превышает 8 СМС)",
    206: "Будет превышен или уже превышен дневной лимит на отправку сообщений",
    207: "На этот номер (или один из номеров) нельзя отправлять сообщения, либо указано более 100 номеров в списке получателей",
    208: "Параметр time указан неправильно",
    209: "Вы добавили этот номер (или один из номеров) в стоп-лист",
    210: "Используется GET, где необходимо использовать POST",
    211: "Метод не найден",
    220: "Сервис временно недоступен, попробуйте чуть позже.",
    300: "Неправильный token (возможно истек срок действия, либо ваш IP изменился)",
    301: "Неправильный пароль, либо пользователь не найден",
    302: "Пользователь авторизован, но аккаунт не подтвержден (пользователь не ввел код, присланный в регистрационной смс)",
}

def generate_code(phone):
    return '1234'

def send(phone):
    api_id = '03C555E6-615A-DBCF-FED4-25AAEA3731F0'
    message = 'Your code authorization: %s' % generate_code(phone)

    url = "http://sms.ru/sms/send?api_id=%s&to=%s&text=%s" % (api_id, phone, message.replace(' ', '+'))

    try:
        res = urlopen(url, timeout=10)
    except URLError as errstr:
        raise Exception("%s" % errstr)

    service_result = res.read().splitlines()
    if service_result is not None and int(service_result[0]) != 100:
        raise Exception("Unable send sms message to %s when service has returned code: %s " %
                        (phone, servicecodes[int(service_result[0])]))


def main():
    pass
    # send('89040331987')



if __name__ == "__main__":
    main()
