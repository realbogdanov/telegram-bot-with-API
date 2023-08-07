from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from loguru import logger


# Обработчик callback /help по нажатию кнопки в меню
@logger.catch()
@bot.callback_query_handler(func=lambda call: call.data == "/help")
def callback_help(call) -> None:
    """
    Функция обработчик callback запроса для вывода списка всех команд

    Parameters:
        call: Объект с информацией о callback запросе от пользователя

    Returns:
        None
    """
    logger.warning("Пользователь {user} начал работу с callback help".format(user=call.from_user.first_name))
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(call.message.chat.id, "\n".join(text))
    logger.info("Пользователю {user} отправилось сообщение".format(user=call.from_user.first_name))
    logger.warning("Конец callback /help")


# Обработчик команды /help
@logger.catch()
@bot.message_handler(commands=["help"])
def command_help(message: Message):
    """
    Функция обработчик сообщения запроса для вывода списка всех команд

    Parameters:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    logger.warning("Пользователь {user} начал работу с command help".format(user=message.from_user.first_name))
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, "\n".join(text))
    # bot.reply_to(message, "\n".join(text))
    logger.info("Пользователю {user} отправилось сообщение".format(user=message.from_user.first_name))
    logger.warning("Конец command /help")
