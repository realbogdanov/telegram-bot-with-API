import telebot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: telebot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
