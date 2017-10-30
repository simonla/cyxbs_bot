#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from db import bind_stu, get_stu_nums, query
from key import get_token, get_test_token
from network import get_courses, get_name_by_stu_num
from utils import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Let me serve you, my lord')


def today(bot, update, args, offset=0):
    try:
        query(get_stu_nums(update.message.from_user.id), offset, update) if len(args) == 0 else query(args, offset,
                                                                                                      update)
    except (IndexError, ValueError):
        traceback.print_exc()


def tomorrow(bot, update, args):
    today(bot, update, args, offset=1)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def bind(bot, update, args):
    try:
        args = list(filter(lambda x: is_stu_num(x), args))
        if len(args) == 0:
            error_hint_bind(update)
            return
        bind_stu(update.message.from_user.id, args)
        update.message.reply_text('绑定成功了喵')
        return
    except (IndexError, ValueError):
        traceback.print_exc()


def unsubscribe(bot, update, args, job_queue, chat_data):
    try:
        if 'jobs' not in chat_data:
            return
        for job in chat_data['jobs']:
            job.schedule_removal()
        del chat_data['jobs']
        if args[0] != 'no_text':
            update.message.reply_text('订阅已取消')
    except(IndexError, ValueError):
        traceback.print_exc()


def subscribe(bot, update, args, job_queue, chat_data):
    try:
        unsubscribe(bot, update, ['no_text'], job_queue, chat_data)
        morning_time = args[0] if len(args) >= 1 else 7
        night_time = args[1] if len(args) >= 2 else 22
        datetime_morning = get_today_by_hour(int(morning_time), 0)
        datetime_night = get_tomorrow_by_hour(int(night_time), 0)
        chat_data['jobs'] = []
        if check_time(datetime_morning):
            morning_job = job_queue.run_daily(lambda bot, job: today(bot, job.context, {}, 0),
                                              datetime_morning,
                                              context=update)
            chat_data['jobs'].append(morning_job)
        if check_time(datetime_night):
            night_job = job_queue.run_daily(lambda bot, job: tomorrow(bot, job.context, {}),
                                            datetime_night,
                                            context=update)
            chat_data['jobs'].append(night_job)
        update.message.reply_text('订阅成功\n\n'
                                  '你目前的时间设定是 %s 点和 %s 点\n\n'
                                  '默认7点和22点提醒，可以自定义，比如设置8点和20点提醒，'
                                  '就可以使用 /subscribe 8 20' % (
                                      morning_time, night_time))
    except (IndexError, ValueError):
        traceback.print_exc()


def main():
    updater = Updater(get_token())
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("today", today, pass_args=True))
    dp.add_handler(CommandHandler("tomorrow", tomorrow, pass_args=True))
    dp.add_handler(CommandHandler("bind", bind, pass_args=True))
    dp.add_handler(CommandHandler("subscribe", subscribe, pass_job_queue=True, pass_args=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe, pass_job_queue=True, pass_args=True, pass_chat_data=True))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
