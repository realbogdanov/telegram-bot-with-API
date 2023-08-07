import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def three_days_data():
	# Узнаём вчерашнюю, сегодняшнюю и завтрашнюю дату
	yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
	current_date = datetime.datetime.now()
	tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

	# Создаём клавиатуру
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
	buttons = [KeyboardButton("{}".format(yesterday.strftime("%Y-%m-%d"))),
			KeyboardButton("{}".format(current_date.strftime("%Y-%m-%d"))),
			KeyboardButton("{}".format(tomorrow.strftime("%Y-%m-%d"))),]

	keyboard.add(*buttons)

	return keyboard
