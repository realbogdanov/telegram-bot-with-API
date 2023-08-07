from telebot.handler_backends import State, StatesGroup

class UserStates(StatesGroup):
	"""Класс состояний пользователя"""
	get_command = State()
	get_count = State()
	get_date2history = State()
