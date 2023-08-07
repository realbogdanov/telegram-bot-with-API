from telebot.handler_backends import State, StatesGroup

class UserStates(StatesGroup):
	"""Класс состояний пользователя"""
	get_flight_number = State()
	get_data2custom = State()
