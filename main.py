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
        if len(args) == 0:
            query(get_stu_nums(update.message.from_user.id), offset, update)
        else:
            query(args, offset, update)
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
        for job in chat_data['jobs']:
            job.schedule_removal()
        del chat_data['jobs']
        update.message.reply_text('订阅已取消')
    except(IndexError, ValueError):
        traceback.print_exc()


def alarm(bot, job):
    if job.name == 'morning_job':
        today(bot, job.context, {}, 0)
        pass
    elif job.name == 'night_job':
        tomorrow(bot, job.context, {})
        pass


def subscribe(bot, update, args, job_queue, chat_data):
    try:
        morning_job = job_queue.run_daily(alarm, get_today_by_hour(7, 0), name='morning_job',
                                          context=update)
        night_job = job_queue.run_daily(alarm, get_today_by_hour(22, 0), name='night_job',
                                        context=update)
        chat_data['jobs'] = [morning_job, night_job]
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
