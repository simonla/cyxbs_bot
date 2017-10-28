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


def is_on_time(day, offset=0):
    week_list = ['星期一''星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    weekday = (datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone('Asia/Shanghai')).weekday() + offset) % 7
    return week_list[weekday] == day


def is_stu_num(stu_num):
    return is_number(stu_num) and len(str(stu_num)) == 10


def error_hint_bind(update):
    update.message.reply_text('eg: /bind <your student number> \n\nps. You can bind more than one student number')


def error_hint_query(update):
    update.message.reply_text("eg: /(today|tomorrow) <your student number> \n\n "
                              "Or you can go first to bind your student number by command /bind ")


def reply(update, arr):
    for stu in arr:
        if stu['course'] == '':
            update.message.reply_text('%s，没有课喵，睡个懒觉哦(●ˇ∀ˇ●)' % (str(stu['stu_num']),))
        else:
            update.message.reply_text('👌 Hi, %s:\n\n' % (str(stu['stu_num']),) + stu['course'])


def get_today_by_hour(hour, min=0):
    today = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone('Asia/Shanghai'))
    return datetime(today.year, today.month, today.day, hour, min)


def get_tomorrow_by_hour(hour, min=0):
    tomorrow = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone('Asia/Shanghai')) + timedelta(days=1)
    return datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, min)
