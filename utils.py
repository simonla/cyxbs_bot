from datetime import datetime, date, timedelta, timezone

import pytz as pytz


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
    week_list = ['星期一''星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    print('befo')
    print(datetime.utcnow().now())
    print('afte')
    print(datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')))
    weekday = (datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone('Asia/Shanghai')).weekday() + offset) % 7
    return week_list[weekday] == day


def is_stu_num(stu_num):
    return len(str(stu_num)) == 10


def bind_err(update):
    update.message.reply_text('eg: /bind <your student number> \n\nps. You can bind more than one student number')


def reply(update, text, stu):
    if text == '':
        update.message.reply_text('%s，没有课喵，睡个懒觉哦(●ˇ∀ˇ●)' % (str(stu),))
    else:
        update.message.reply_text('👌 Hi, %s:\n\n' % (str(stu),) + text)
