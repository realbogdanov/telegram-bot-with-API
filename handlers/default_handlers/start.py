from loguru import logger
from telebot.types import Message
from keyboards.inline.keyboard_all_command import name_all_commands
from loader import bot
from states.states2start import UserStates


# Обработчик команды /start
@logger.catch()
@bot.message_handler(commands=["start"])
def command_start(message: Message) -> None:
    """
    Функция обработчик команды /start
    И изменение состояния пользователя на UserStates.start_bot

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None
    """
    try:
        logger.warning("Начало command /start")
        bot.set_state(message.from_user.id, UserStates.start_bot, message.chat.id)
        logger.debug("Пользователь {user} изменил состояние на start_bot".format(user=message.from_user.first_name))

        # Создаём клавиатуру
        main_keyboard = name_all_commands()
        logger.debug("Создалась клавиатура")

        # Формируем сообщение и отправляем пользователю
        good_mess = "{user}, добро пожаловать в чат-бот Share Airplane! 🛩️\n" \
                    "\nМы рады помочь тебе с путешествиями и готовы предоставить всю необходимую информацию о перелетах. " \
                    "В нашем боте ты можешь найти ближайший аэропорт и получить информацию о статусе прошедшего или будущего рейса по его номеру и дате.\n" \
                    "\nПросто укажи свой запрос выбрав из меню нужную команду, и мы постараемся предоставить тебе актуальную информацию. " \
                    "Наша команда готова помочь тебе с любыми вопросами о перелетах, чтобы твоё путешествие было комфортным и безопасным.\n" \
                    "\nПриятного использования бота и приятных путешествий!🫶🏽️".format(user=message.from_user.first_name, )
        bot.send_message(message.chat.id, good_mess, reply_markup=main_keyboard)
        logger.debug("Отправилось сообщение с приветствием и клавиатурой")



    except Exception as e:
        logger.error("Ошибка в сценарии /start")
        logger.exception(e)

    finally:
        # Удаляем состояние пользователя
        logger.warning("Конец command /start")
        bot.delete_state(message.from_user.id, message.chat.id)


# Обработчик callback /start по нажатию кнопки в меню
@logger.catch()
@bot.callback_query_handler(func=lambda call: call.data == "/start")
def callback_start(call) -> None:
    """
    Функция обработчик callback запроса /start
    И изменение состояния пользователя на UserStates.start_bot

    Parameters:
        call: Объект с информацией о callback запросе от пользователя

    Returns:
        None
    """
    try:
        logger.warning("Начало callback /start")
        bot.set_state(call.from_user.id, UserStates.start_bot, call.message.chat.id)
        logger.debug("Пользователь {user} изменил состояние на start_bot".format(user=call.from_user.first_name))

        # Создаём клавиатуру
        main_keyboard = name_all_commands()
        logger.debug("Создалась клавиатура")

        # Формируем сообщение и отправляем пользователю
        good_mess = "{user}, добро пожаловать в чат-бот Share Airplane! 🛩️\n" \
                    "\nМы рады помочь тебе с путешествиями и готовы предоставить всю необходимую информацию о перелетах. " \
                    "В нашем боте ты можешь найти ближайший аэропорт и получить информацию о статусе прошедшего или будущего рейса по его номеру и дате.\n" \
                    "\nПросто укажи свой запрос выбрав из меню нужную команду, и мы постараемся предоставить тебе актуальную информацию. " \
                    "Наша команда готова помочь тебе с любыми вопросами о перелетах, чтобы твоё путешествие было комфортным и безопасным.\n" \
                    "\nПриятного использования бота и приятных путешествий!🫶🏽️".format(user=call.from_user.first_name, )
        bot.send_message(call.message.chat.id, good_mess, reply_markup=main_keyboard)
        logger.debug("Отправилось сообщение с приветствием и клавиатурой")



    except Exception as e:
        logger.error("Ошибка в сценарии /start")
        logger.exception(e)

    finally:
        # Удаляем состояние пользователя
        logger.warning("Конец callback /start")
        bot.delete_state(call.from_user.id)
