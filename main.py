#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from db import bind_stu, get_stu_nums, query
from key import get_token, get_test_token
from network import get_courses
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
            args = filter(lambda x: is_stu_num(x), args)
            query(args, offset, update)
    except (IndexError, ValueError):
        traceback.print_exc()


def tomorrow(bot, update, args):
    today(bot, update, args, offset=1)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def bind(bot, update, args):
    try:
        args = filter(lambda x: is_stu_num(x), args)
        bind_stu(update.message.from_user.id, args)
        update.message.reply_text('绑定成功了喵')
        return
    except (IndexError, ValueError):
        traceback.print_exc()


def unsubscribe(bot, update, args, job_queue, chat_data):
    try:

    except(IndexError, ValueError):
        traceback.print_exc()


def alarm(bot, job):
    pass


def subscribe(bot, update, args, job_queue, chat_data):
    try:
        morning_job = job_queue.run_daily(alarm, get_today_by_hour(7))
        night_job = job_queue.run_daily(alarm, get_today_by_hour(22))
        chat_data['job'] = [morning_job, night_job]
    except (IndexError, ValueError):
        traceback.print_exc()


def main():
    updater = Updater(get_test_token())
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
