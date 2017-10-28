#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from db import bind_stu, get_stu_nums
from key import get_token
from network import get_courses
from utils import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Let me serve you, my lord')


def today(bot, update, args, offset=0):
    try:
        if is_number(int(args[0])) and is_stu_num(args[0]):
            stu = args[0]
            reply(update, [{'stu_num': stu, 'course': get_courses(int(args[0]), offset=offset)}])
            return
        stu_ids = get_stu_nums(update.message.from_user.id)
        reply_arr = []
        for stu in stu_ids:
            if len(args) == 0 and is_stu_num(stu):
                reply_arr.append({'stu_num': stu, 'course': get_courses(stu, offset=offset)})
        reply(update, reply_arr)
        return
    except (IndexError, ValueError):
        update.message.reply_text("eg: /(today|tomorrow) <your student number> \n\n "
                                  "Or you can go first to bind your student number by command /bind ")


def tomorrow(bot, update, args):
    today(bot, update, args, offset=1)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def bind(bot, update, args):
    try:
        for arg in args:
            if not is_stu_num(arg):
                bind_err(update)
                return
        bind_stu(update.message.from_user.id, args)
        update.message.reply_text('绑定成功了喵')
        return

    except (IndexError, ValueError):
        bind_err(update)


def main():
    updater = Updater(get_token())
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("today", today, pass_args=True))
    dp.add_handler(CommandHandler("tomorrow", tomorrow, pass_args=True))
    dp.add_handler(CommandHandler("bind", bind, pass_args=True))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
