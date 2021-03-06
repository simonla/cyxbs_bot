from datetime import datetime, timedelta

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
    return (datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone('Asia/Shanghai')).weekday() + offset) % 7 == day


def is_stu_num(stu_num):
    return is_number(stu_num) and len(str(stu_num)) == 10


def error_hint_bind(update):
    update.message.reply_text('Usage: /bind <your student number> \n\nps. You can bind more than one student number')


def error_hint_query(update):
    update.message.reply_text("Usage: /(today|tomorrow) <your student number> \n\n "
                              "Or you can go first to bind your student number by command /bind ")


def reply(update, arr):
    for stu in arr:
        update.message.reply_text('%s\n\n没有课喵 睡个懒觉哦(●ˇ∀ˇ●)' % (stu['hint'],)) \
            if stu['course'] == '' \
            else update.message.reply_text('%s\n\n' % (stu['hint'],) + stu['course'])


def get_today_by_hour(hour, time_min=0):
    today = datetime.utcnow() + timedelta(hours=8)
    return datetime(today.year, today.month, today.day, hour, time_min)


def get_tomorrow_by_hour(hour, time_min=0):
    tomorrow = datetime.utcnow() + timedelta(days=1) + timedelta(hours=8)
    return datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, time_min)


def get_week(week, offset):
    now_week = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).weekday()
    return week + 1 if now_week + offset >= 7 else week


def check_time(uncheck_datetime):
    return uncheck_datetime.timestamp() >= (datetime.utcnow() + timedelta(hours=8)).timestamp()
