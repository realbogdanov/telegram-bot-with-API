from telebot.handler_backends import State, StatesGroup

class UserStates(StatesGroup):
	"""Класс состояний"""
	ip_user = State()
	count_airport2low = State()
	search_radius = State()
