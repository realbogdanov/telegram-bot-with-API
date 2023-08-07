from typing import Tuple
from datetime import datetime


def check_command(command: str) -> Tuple[str, str] | str:
	"""
	Проверяет введенную команду на соответствие:
	:param command: str - команда, которую ввел пользователь
	:return: Tuple[str, str] | str - кортеж из команды и сообщения, которое нужно отправить пользователю
	"""

	if command == "*high":
		return "/high", "Вы выбрали \"Поиск аэропорта по городу\""
	elif command == "*low":
		return "/low", "Вы выбрали \"Поиск аэропорта по ip\""
	elif command == "*custom":
		return "/custom", "Вы выбрали \"Статус рейса по его номеру\""


def check_date(date: str) -> bool:
	"""
	Проверка строки на соответствие формату YYYY-MM-DD
	:param date: str - строка с датой
	:return: bool - True, если строка соответствует формату, иначе False
	"""

	try:
		datetime.strptime(date, '%Y-%m-%d')
		return True
	except ValueError:
		return False

