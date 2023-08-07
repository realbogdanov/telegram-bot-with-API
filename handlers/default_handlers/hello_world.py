from telebot.types import Message
from keyboards.inline.keyboard_all_command import name_all_commands
from loader import bot
from loguru import logger


# Обработчик callback /hello_world по нажатию кнопки в меню
@logger.catch()
@bot.callback_query_handler(func=lambda call: call.data == "/hello_world")
def callback_hello_world(call) -> None:
	"""
	Функция обработчик callback запроса для тестовой проверки бота

	Parameters:
		call: Объект с информацией о callback запросе от пользователя

	Returns:
		None
	"""
	logger.warning("Пользователь {user} начал работу с callback hello_world (TEST COMMAND)".format(user=call.from_user.first_name))
	mess = "Я работаю!\nПривет {}".format(call.from_user.full_name)
	bot.send_message(call.message.chat.id, mess)
	logger.info("Пользователю {user} отправилось сообщение".format(user=call.from_user.first_name))

	# Создаём клавиатуру навигации
	main_keyboard = name_all_commands()
	bot.send_message(call.from_user.id, "Выберите действие", reply_markup=main_keyboard)
	logger.debug("Создалась клавиатура навигации")
	logger.warning("Конец callback /hello_world")


# Обработчик команды /hello_world
@logger.catch()
@bot.message_handler(commands=["hello_world"])
def command_hello_world(message: Message) -> None:
	"""
	Функция обработчик сообщения запроса для тестовой проверки бота

	Parameters:
		message (telebot.types.Message): Объект сообщения от пользователя.

	Returns:
		None
	"""
	logger.warning(
		"Пользователь {user} начал работу с command hello_world (TEST COMMAND)".format(user=message.from_user.first_name))
	mess = "Я работаю!\nПривет {}".format(message.from_user.full_name)
	bot.send_message(message.chat.id, mess)
	logger.info("Пользователю {user} отправилось сообщение".format(user=message.from_user.first_name))

	# Создаём клавиатуру навигации
	main_keyboard = name_all_commands()
	bot.send_message(message.from_user.id, "Выберите действие", reply_markup=main_keyboard)
	logger.debug("Создалась клавиатура навигации")
	logger.warning("Конец command /hello_world")
