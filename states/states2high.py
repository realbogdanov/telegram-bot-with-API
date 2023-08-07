from telebot.handler_backends import State, StatesGroup

class UserStates(StatesGroup):
	"""Класс состояний пользователя"""
	search_city = State()
	count_airport2high = State()
