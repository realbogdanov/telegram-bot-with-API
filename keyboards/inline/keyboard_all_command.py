from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def name_all_commands() -> InlineKeyboardMarkup:
	"""
	Создание кнопок с названиями всех команд

	Returns:
		InlineKeyboardMarkup: Объект клавиатуры с кнопками
	"""
	button_start = InlineKeyboardButton(text="🏁Начать работу🏁", callback_data="/start")
	button_low = InlineKeyboardButton(text="Поиск аэропорта по ip", callback_data="/low")
	button_high = InlineKeyboardButton(text="Поиск аэропорта по городу", callback_data="/high")
	button_custom = InlineKeyboardButton(text="✈️Статус рейса по его номеру✈️", callback_data="/custom")
	button_history = InlineKeyboardButton(text="🗄История поисков🗄", callback_data="/history")
	button_help = InlineKeyboardButton(text="🆘Список всех команд🆘", callback_data="/help")
	button_test = InlineKeyboardButton(text="👨🏼‍💻ТЕСТ👨🏼‍💻", callback_data="/hello_world")

	# Формирование клавиатуры
	keyboard_commands = InlineKeyboardMarkup(row_width=2).add(button_start)
	keyboard_commands.add(button_low, button_high)
	keyboard_commands.add(button_custom, button_history)
	keyboard_commands.add(button_help)
	keyboard_commands.add(button_test)

	return keyboard_commands
