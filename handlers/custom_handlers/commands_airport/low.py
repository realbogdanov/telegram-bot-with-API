import re
import time
from loguru import logger
from keyboards.inline.keyboard_all_command import name_all_commands
from loader import bot
from telebot.types import Message
from database.common.models import db, Airports
from database.core import crud
from handlers.custom_handlers.commands_airport.low_loader import site_api, headers, params, url
from states.states2low import UserStates
from keyboards.inline.keyboard2airports_count import ip_address_site, count_airport
from utils.misc.validate_api_data import validate_api_data

db_write = crud.record_data

logger.add("logs/logs_low.log", level="ERROR", format="{time} {level} {message}", rotation="500 MB", compression="zip")


# Обработчик callback /low по нажатию кнопки в меню
@logger.catch
@bot.callback_query_handler(func=lambda call: call.data == "/low")
def callback_low(call) -> None:
	"""
	Функция обработчик callback запроса для поиска ближайших аэропортов по ip пользователя
	И изменение состояния пользователя на UserInfoState.ip_user

    Parameters:
        call: Объект с информацией о callback запросе от пользователя

    Returns:
        None
	"""
	# Изменение состояния пользователя
	logger.warning("Пользователь {user} начал работу с callback low".format(user=call.from_user.first_name))
	bot.set_state(call.from_user.id, UserStates.ip_user, call.message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на ip_user".format(user=call.from_user.first_name))

	# Вывод сообщения пользователю
	good_mess = "Привет! Мы рады приветствовать вас! 😊\n" \
	            "Мы готовы помочь вам найти ближайший аэропорт на основе вашего IP-адреса. \n" \
	            "\n<b>Пожалуйста, не волнуйтесь - мы не храним ваш IP-адрес и не используем его в каких-либо других целях, " \
	            "кроме предоставления информации о ближайшем аэропорте. Ваша конфиденциальность и безопасность для нас очень важны.</b>\n" \
	            "\n{}, <b>введите пожалуйста свой ip</b>".format(call.from_user.first_name)
	bot.send_message(call.from_user.id, good_mess, parse_mode="HTML")
	bot.send_message(call.from_user.id, text="Узнать свой ip можно нажав на кнопку", reply_markup=ip_address_site())
	picture_example_ip = open("utils/misc/pictures/you_ip.png", "rb")
	bot.send_photo(call.message.chat.id, picture_example_ip)
	logger.info("Пользователь {user} получил сообщение с запросом ip адреса и примером ip".format(user=call.from_user.first_name))


# Обработчик команды /low
@logger.catch
@bot.message_handler(commands=["low"])
def command_low(message: Message) -> None:
	"""
	Функция обработчик сообщения для поиска ближайших аэропортов по ip пользователя
	И изменение состояния пользователя на UserInfoState.ip_user

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None
	"""

	# Изменение состояния пользователя
	logger.warning("Пользователь {user} начал работу с command low".format(user=message.from_user.first_name))
	bot.set_state(message.from_user.id, UserStates.ip_user, message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на ip_user".format(user=message.from_user.first_name))

	# Вывод сообщения пользователю
	good_mess = "Привет! Мы рады приветствовать вас! 😊\n" \
	            "Мы готовы помочь вам найти ближайший аэропорт на основе вашего IP-адреса. \n" \
	            "\n<b>Пожалуйста, не волнуйтесь - мы не храним ваш IP-адрес и не используем его в каких-либо других целях, " \
	            "кроме предоставления информации о ближайшем аэропорте. Ваша конфиденциальность и безопасность для нас очень важны.</b>\n" \
	            "\n{}, <b>введите пожалуйста свой ip</b>".format(message.from_user.first_name)
	bot.send_message(message.from_user.id, good_mess, parse_mode="HTML")
	bot.send_message(message.from_user.id, text="Узнать свой ip можно нажав на кнопку", reply_markup=ip_address_site())
	picture_example_ip = open("utils/misc/pictures/you_ip.png", "rb")
	bot.send_photo(message.chat.id, picture_example_ip)
	logger.info("Пользователь {user} получил сообщение с запросом ip адреса и примером ip".format(user=message.from_user.first_name))


@logger.catch
@bot.message_handler(state=UserStates.ip_user)
def get_ip_user(message: Message) -> None:
	"""
	Функция для получения и обработки ip пользователя с последующей записью в базу данных.
	И запрос кол-ва аэропортов для поиска ближайших аэропортов.
	И изменение состояния пользователя на UserInfoState.count_airport

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None
	"""

	# Проверка на валидность ip
	pattern_search_ip = r"([0-9]{1,3}[\.]){3}[0-9]{1,3}"
	if re.search(pattern_search_ip, message.text):
		# Получение ip пользователя
		search_user_ip = re.search(pattern_search_ip, message.text)
		result_user_ip = search_user_ip.group()
		logger.debug("Пользователь {user} ввел ip: {ip}".format(user=message.from_user.first_name, ip=result_user_ip))

		# Изменение состояния пользователя
		bot.set_state(message.from_user.id, UserStates.count_airport2low, message.chat.id)
		logger.debug("Пользователь {user} изменил состояние на count_airport".format(user=message.from_user.first_name))
		good_mess = "Отлично, записал👌🏼. \n<b>Введите кол-во аэропортов</b>"

		# Реализация кнопки для выбора кол-ва аэропортов
		keyboard_count_airport = count_airport()
		bot.send_message(message.from_user.id, good_mess, reply_markup=keyboard_count_airport, parse_mode="HTML")
		logger.info("Пользователь {user} получил сообщение с запросом кол-ва аэропортов".format(user=message.from_user.first_name))

		try:
			# Запись информации в хранилище данных
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				data["ip_user"] = result_user_ip
				logger.info("Данные об ip пользователя были записаны в хранилище данных")

		except Exception as ex:
			logger.error("Произошла ошибка при записи данных в хранилище:")
			logger.exception(ex)
			# Вывод сообщения пользователю об ошибке
			error_mess = "Упс... что-то пошло не так 😔. Пожалуйста, попробуйте еще раз."
			bot.send_message(message.from_user.id, error_mess)
			logger.info("Пользователь {user} получил сообщение с ошибкой при записи данных".format(user=message.from_user.first_name))

	else:
		# Если ip не валидный
		bad_mess = "{} это не ip\n" \
		           "Введите ip адрес\n" \
		           "прим.: <u>111.222.333.444</u>".format(message.from_user.first_name)
		bot.send_message(message.from_user.id, bad_mess, parse_mode="HTML")
		logger.warning("Введён не ip, пользователь получил сообщение с ошибкой")


@logger.catch
@bot.callback_query_handler(func=lambda call:call, state=UserStates.count_airport2low)
def handler_keyboard_click_and_get_count_airport(call) -> None:
	"""
	Функция для получения кол-ва аэропортов для поиска ближайших аэропортов с последующей записью в базу данных.
	И запрос радиуса поиска аэропортов.
	И изменение состояния пользователя на UserInfoState.search_radius

    Parameters:
        call: Объект с информацией о callback запросе от пользователя

    Returns:
        None
	"""

	# Получение кол-ва аэропортов
	count = call.data

	# Вывод сообщения пользователю и получение радиуса поиска аэропортов
	logger.info("Пользователь {user} выбрал кол-во аэропортов: {count}".format(user=call.from_user.first_name, count=count))
	bot.set_state(call.from_user.id, UserStates.search_radius, call.message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на search_radius".format(user=call.from_user.first_name))
	good_mess = "Мы обнаружили несколько аэропортов, соответствующих вашему запросу. \n" \
	            "\nЧтобы мы могли точнее определить ближайшие аэропорты к вашему местоположению, <b>введите радиус поиска " \
	            "(в километрах)</b>:".format(user=call.from_user.first_name, )
	bot.send_message(call.message.chat.id, good_mess, parse_mode="HTML")
	logger.info("Пользователь {user} получил сообщение с запросом радиуса поиска аэропортов".format(user=call.from_user.first_name))

	try:
		# Запись информации в хранилище данных
		with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
			data["count_airport"] = count
			logger.info("Данные о кол-ве аэропортов были записаны")

	except Exception as ex:
		logger.error("Произошла ошибка при записи данных:")
		logger.exception(ex)
		# Вывод сообщения пользователю
		error_mess = "Упс... у нас что-то пошло не так 😔. Пожалуйста, попробуйте еще раз."
		bot.send_message(call.from_user.id, error_mess)
		logger.info("Пользователь {user} получил сообщение с ошибкой при записи данных".format(user=call.from_user.first_name))


@logger.catch
@bot.message_handler(state=UserStates.search_radius)
def get_search_radius(message: Message) -> None:
	"""
	Функция для получения радиуса поиска аэропортов с последующей записью в базу данных.
	И вывод результатов работы.

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None
	"""

	# Проверяем, является ли введенное сообщение числом
	if message.text.isdigit():
		logger.info("Пользователь {user} ввел радиус поиска аэропортов: {radius}".format(user=message.from_user.first_name,
		                                                                                 radius=message.text))
		try:
			# Записываем радиус поиска в хранилище данных
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				data["search_radius"] = message.text
				logger.info("Данные о радиусе поиска аэропортов были записаны")

				good_mess = "Спасибо за предоставленную информацию! \n" \
				            "Мы уже начали обрабатывать ваш запрос и собираем необходимую информацию о ближайших аэропортах."
				bot.send_message(message.from_user.id, good_mess)
				logger.info("Пользователь {user} получил сообщение с началом поиска результатов".format(
						user=message.from_user.first_name))

				# Получаем данные из хранилища данных
				user_ip = data["ip_user"]
				user_count_search_airport = data["count_airport"]
				user_radius_search_airport = data["search_radius"]
				logger.debug("Получены данные из хранилища данных: {ip}, {count}, {radius}".format(ip=user_ip,
				                                                                                 count=user_count_search_airport,
				                                                                                 radius=user_radius_search_airport))

				# Выполняем запрос к API
				search_airports_by_ip_address_geolocation = site_api.airports_ip(method="GET", url=url, headers=headers,
				                                                                 params=params, ip_user=user_ip,
				                                                                 radius_km=user_radius_search_airport,
				                                                                 limit_search_airport=user_count_search_airport)

				# Получаем ответ от сервера
				response_json = search_airports_by_ip_address_geolocation.json()
				logger.debug("Получен ответ от сервера: {response}".format(response=response_json, ))

				# Получаем аэропорты из ответа
				result_mess = response_json.get("items")

				# Преобразуем полученные данные в словарь для проведения проверки на валидность
				response_dict = result_mess[0]
				logger.debug("Полученные данные от API из списка: {data}".format(data=response_dict))

				# Проверяем, что получен корректны ответ от сервера
				if validate_api_data(response_dict):
					logger.debug("Получен корректный ответ от сервера")

					# Создаем список для записи в БД
					information2db = []

					# Обробатываем полученные результаты
					# выводим их пользователю и формируем данные для записи в БД
					for item in result_mess:
						iata = item.get("iata")
						full_airport_addressname = item.get("name")

						# Получение данных из ключа location
						if isinstance(item.get("location"), dict):
							lat = item.get("location").get("lat")
							lon = item.get("location").get("lon")

						mess = "<b>Код:</b> {code_airport}\n" \
						       "<b>Название:</b> {short_name}\n" \
						       "<b>Местоположение:</b>  https://maps.google.com/?q={lat},{lon}".format(code_airport=iata,
						                                  short_name=full_airport_addressname,
						                                  lat=lat,
						                                  lon=lon,)
						logger.debug("Сформировано сообщение для пользователя: {mess}".format(mess=mess))

						# Записываем данные аэропорта в словарь
						# чтобы потом добавить в список для записи в БД всех аэропротов
						airport_info = {"command_name": "/low",
								"user_id":message.from_user.id,
								"user_name":message.from_user.username,
								"full_airport_address":full_airport_addressname,
								"iata":iata,
								"location_lat":lat,
								"location_lon":lon,}
						logger.debug("Информация об аэропрте записалась в словарь")

						# Добавил данные аэропорта в список для записи в БД
						information2db.append(airport_info)
						logger.debug("Информация об аэропрте записалась в список для записи в БД")

						bot.send_message(message.from_user.id, mess, parse_mode="HTML")
						time.sleep(1)
						logger.debug("Пользователь {user} получил результат поиска.".format(
							user=message.from_user.first_name,))
				else:
					logger.debug("Получен не корректный ответ от сервера")
					bot.send_message(message.from_user.id, "У нас возникла проблема с работой сервиса.\n"
					                                       "Попробуйте пожалуйста позднее.")
					logger.info("Пользователь {user} получил сообщение об ошибке.".format(user=message.from_user.first_name,))

		except Exception as ex:
			logger.error("Произошла ошибка при записи и выводе данных:")
			logger.exception(ex)
			# Вывод сообщения пользователю
			exc_mess = "К сожалению, в процессе работы сервиса произошла ошибка. Пожалуйста, подождите немного и попробуйте еще раз. \n" \
			           "<b>Если проблема сохраняется, пожалуйста, обратитесь в нашу службу поддержки, чтобы мы могли помочь вам решить эту проблему.</b>" \
			           "Благодарим за понимание и извините за возможные неудобства."
			bot.send_message(message.from_user.id, exc_mess, parse_mode="HTML")

		try:
			# Записываем данные в БД
			db_write(db, Airports, information2db)
			logger.info("Данные были записаны в БД")

		except Exception as ex:
			logger.error("Произошла ошибка при записи данных в БД:")
			logger.exception(ex)

		# Создаём клавиатуру навигации
		main_keyboard = name_all_commands()
		bot.send_message(message.from_user.id, "Выберите действие", reply_markup=main_keyboard)
		logger.debug("Создалась клавиатура навигации")

		# Удаляем состояние пользователя
		bot.delete_state(message.from_user.id, message.chat.id)
		logger.debug("Состояние пользователя было удалено")
		logger.warning("Конец сценария /low")

	else:
		logger.warning("Пользователь ввёл не число")
		bad_mess = "{user} ваше сообщение должно состоять только из цифр.".format(user=message.from_user.first_name)
		bot.send_message(message.from_user.id, bad_mess)
		logger.info("Пользователь {user} получил сообщение об ошибке.".format(user=message.from_user.first_name,))
