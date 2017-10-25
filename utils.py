from datetime import datetime, date


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def get_token():
    return "328109625:AAECcBvUoOr-J9rjt3x-L0MgFt4wfsG5XKM"


def is_on_time(day, offset=0):
    list = ['星期一''星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    weekday = datetime.now().weekday()+offset
    return list[weekday] == day
