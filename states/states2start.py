from telebot.handler_backends import State, StatesGroup

class UserStates(StatesGroup):
	"""Класс состояний пользователя"""
	start_bot = State()
