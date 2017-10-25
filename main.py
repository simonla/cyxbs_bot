#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from network import get_courses
from utils import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Let me serve you, my lord')


def today(bot, update):
    text = str(update.message.text).split(" ")
    if len(text) == 2:
        stu_num = text[1]
    else:
        update.message.reply_text("error: no student number")
        return

    if is_number(stu_num) and len(stu_num) == 10:
        update.message.reply_text(get_courses(stu_num))
    else:
        update.message.reply_text("error: not a student number")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(get_token())
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("today", today))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
