from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def name_commands():
	"""Создание кнопок с названиями команд"""
	button_high = InlineKeyboardButton(text="Поиск аэропорта по городу", callback_data="*high")
	button_low = InlineKeyboardButton(text="Поиск аэропорта по ip", callback_data="*low")
	button_custom = InlineKeyboardButton(text="Статус рейса по его номеру", callback_data="*custom")
	keyboard_commands = InlineKeyboardMarkup(row_width=2)
	keyboard_commands.add(button_high, button_low, button_custom)
	return keyboard_commands
