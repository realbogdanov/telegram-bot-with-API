import re
import time
import datetime
from loguru import logger
from keyboards.inline.keyboard_all_command import name_all_commands
from keyboards.reply.keyboard3days_data import three_days_data
from loader import bot
from telebot.types import Message
from database.common.models import db, Airplanes
from database.core import crud
from handlers.custom_handlers.commands_flight.custom_lader import site_api, headers, params, generate_url
from states.states2custom import UserStates
from utils.misc.cheking2history import check_date

db_write = crud.record_data

logger.add("logs/logs_custom.log", level="ERROR", format="{time} {level} {message}", rotation="500 MB", compression="zip")


# Обработчик callback /custom по нажатию кнопки в меню
@logger.catch
@bot.callback_query_handler(func=lambda call: call.data == "/custom")
def callback_custom(call) -> None:
	"""
	Функция обработчик callback запроса для поиска рейса, по номеру рейса и дате
	И изменение состояния пользователя на UserState.get_flight_number

    Parameters:
        call: Объект с информацией о callback запросе от пользователя

    Returns:
        None
	"""

	logger.warning("Пользователь {user} начал работу с callback custom".format(user=call.from_user.first_name))
	# Изменение состояния пользователя
	bot.set_state(call.from_user.id, UserStates.get_flight_number, call.message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на get_flight_number".format(user=call.from_user.first_name))
	good_mess = "Привет {user}! 👋 \n" \
	            "В этой команде ты можешь получить информацию о статусе прошедшего или будущего рейса по его " \
	            "номеру рейса и дате.✈️📅\n" \
	            "\nВведи пожалуйста номер искомого рейса в формате <b>KL1395</b> или <b>Klm 1395</b>".format(user=call.from_user.first_name)
	bot.send_message(call.message.chat.id, good_mess, parse_mode="HTML")
	logger.info("Пользователь {user} получил сообщение с приветствием".format(user=call.from_user.first_name,))


# Обработчик команды /custom
@logger.catch
@bot.message_handler(commands=["custom"])
def command_custom(message: Message) -> None:
	"""
	Функция обработчик сообщения для поиска рейса, по номеру рейса и дате
	И изменение состояния пользователя на UserState.get_flight_number

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None
	"""

	logger.warning("Пользователь {user} начал работу с командой custom".format(user=message.from_user.first_name))
	# Изменение состояния пользователя
	bot.set_state(message.from_user.id, UserStates.get_flight_number, message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на get_flight_number".format(user=message.from_user.first_name))
	good_mess = "Привет {user}! 👋 \n" \
	            "В этой команде ты можешь получить информацию о статусе прошедшего или будущего рейса по его " \
	            "номеру рейса и дате.✈️📅\n" \
	            "\nВведи пожалуйста номер искомого рейса в формате <b>KL1395</b> или <b>Klm 1395</b>".format(user=message.from_user.first_name)
	bot.send_message(message.chat.id, good_mess, parse_mode="HTML")
	logger.info("Пользователь {user} получил сообщение с приветствием".format(user=message.from_user.first_name,))


@logger.catch
@bot.message_handler(state=UserStates.get_flight_number)
def get_flight_number(message: Message) -> None:
	"""
	Функция обработчик сообщения для получения номера рейса, который хочет найти пользователь
	И изменение состояния пользователя на UserState.get_data

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None
	"""

	# Задаём паттерн поиска номера рейса
	flight_number_pattern = r"[A-Za-z]{1,3}\s?\d+"

	# Поиск номера рейса в строке
	if re.search(flight_number_pattern, message.text):
		search_flight_number = re.search(flight_number_pattern, message.text)
		logger.debug("В строке был обнаружен номер рейса {flight_number}".format(flight_number=search_flight_number))
		logger.debug("Пользователь {user} ввел номер рейса {flight_number}".format(user=message.from_user.first_name,
		                                                                           flight_number=message.text))
		# Изменение состояния пользователя
		bot.set_state(message.from_user.id, UserStates.get_data2custom, message.chat.id)
		logger.debug("Пользователь {user} изменил состояние на get_data".format(user=message.from_user.first_name))

		# Запрашиваем дату рейса
		good_mess = "Введи дату рейса в формате <b>{data}</b>".format(data=datetime.datetime.now().strftime("%Y-%m-%d"))

		# Создаём клавиатуру с датами
		keyboard_data = three_days_data()
		bot.send_message(message.chat.id, good_mess, reply_markup=keyboard_data, parse_mode="HTML")

		# Запись данных в хранилище
		try:
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				data["flight_number"] = message.text
				logger.info("Данные о номере рейса были записаны в хранилище")

		except Exception as e:
			logger.error("Ошибка записи данных в хранилище:")
			logger.exception(e)

	# Если номер рейса не найден в строке
	else:
		bad_mess = "Номер рейса введен не верно! Попробуй еще раз.\n" \
		           "Пример <b>KL1395</b> или <b>Klm 1395</b>"
		bot.send_message(message.chat.id, bad_mess, parse_mode="HTML")
		logger.warning("Пользователь {user} ввел неверный номер рейса".format(user=message.from_user.first_name))


@logger.catch
@bot.message_handler(state=UserStates.get_data2custom)
def get_data(message: Message) -> None:
	"""
	Функция обработчик сообщения для получения даты рейса, который хочет найти пользователь
	И удаление состояния пользователя

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None
	"""

	# Проверяем ввод даты на корректность
	if check_date(message.text):
		logger.info("Пользователь {user} ввел дату рейса {date}".format(user=message.from_user.first_name,
		                                                                date=message.text))

		# Получение данных из хранилища данных
		try:
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				flight_number = data["flight_number"]

				# Формируем сообщение для пользователя
				good_mess = "Ваш запрос обрабатывается, и в ближайшее время вы получите результаты поиска. Пожалуйста, ожидайте."
				bot.send_message(message.chat.id, good_mess, parse_mode="HTML")

				logger.info("Пользователь {user} получил сообщение о том, что запрос обрабатывается".format(
					user=message.from_user.first_name, ))

				# Имитация обработки запроса
				time.sleep(1)

				# Формируем url для запроса к API
				url = generate_url(flight_number=flight_number, data_search=message.text)
				logger.debug("Сформированный url для запроса к API: {url}".format(url=url))

				# Выполнение запроса к API
				try:
					search_flight_status = site_api.flight_status(method="GET", url=url, headers=headers,
					                                              params=params, )
					response_json = search_flight_status.json()
					logger.debug("Получен ответ от API: {response}".format(response=response_json, ))

					# Преобразуем полученные данные в словарь для проведения проверки на валидность
					response_dict = response_json[0]
					logger.debug("Преобразованные данные от API из списка в словарь: {data}".format(data=response_dict))

					# Получаем данные от API
					try:
						photo_url = response_dict.get("aircraft", {}).get("image", {}).get("url", "Нет фото")
						logger.debug("Получена ссылка на фото самолета: {photo_url}".format(photo_url=photo_url))
						airline = response_dict.get("airline", {}).get("name", "Нет данных")
						logger.debug("Получено название авиакомпании: {airline}".format(airline=airline))
						flight_number = response_dict.get("number", "Нет данных")
						logger.debug("Получен номер рейса: {flight_number}".format(flight_number=flight_number))
						aircraft_reg_number = response_dict.get("aircraft", {}).get("reg", "Нет данных")
						logger.debug("Получен регистрационный номер самолета: {aircraft_reg_number}".format(aircraft_reg_number=aircraft_reg_number))
						aircraft_model = response_dict.get("aircraft", {}).get("model", "Нет данных")
						logger.debug("Получена модель самолета: {aircraft_model}".format(aircraft_model=aircraft_model))
						scheduled_time_departure = response_dict.get("departure", {}).get("scheduledTimeLocal", "Нет данных")
						logger.debug("Получено запланированное время вылета: {scheduled_time_departure}".format(scheduled_time_departure=scheduled_time_departure))
						fact_time_departure = response_dict.get("departure", {}).get("runwayTimeLocal", "Нет данных")
						logger.debug("Получено фактическое время вылета: {actual_time_departure}".format(actual_time_departure=fact_time_departure))
						revised_time_departure = response_dict.get("departure", {}).get("revisedTime", {}).get("local", "Нет данных")
						logger.debug("Получено пересмотренное время вылета: {revised_time_departure}".format(revised_time_departure=revised_time_departure))
						departure_airport_code = response_dict.get("departure", {}).get("airport", {}).get("iata", "Нет данных")
						logger.debug("Получен код аэропорта вылета: {departure_airport_code}".format(departure_airport_code=departure_airport_code))
						departure_airport_full_name = response_dict.get("departure", {}).get("airport", {}).get("name", "Нет данных")
						logger.debug("Получено полное название аэропорта вылета: {departure_airport_full_name}".format(departure_airport_full_name=departure_airport_full_name))
						departure_terminal = response_dict.get("departure", {}).get("terminal", "Нет данных")
						logger.debug("Получен терминал вылета: {departure_terminal}".format(departure_terminal=departure_terminal))
						check_in_desk = response_dict.get("departure", {}).get("checkInDesk", "Нет данных")
						logger.debug("Получен номер стойки регистрации: {check_in_desk}".format(check_in_desk=check_in_desk))
						departure_gate = response_dict.get("departure", {}).get("gate", "Нет данных")
						logger.debug("Получен номер выхода на посадку: {departure_gate}".format(departure_gate=departure_gate))
						scheduled_time_arrival = response_dict.get("arrival", {}).get("scheduledTimeLocal", "Нет данных")
						logger.debug("Получено запланированное время прилета: {scheduled_time_arrival}".format(scheduled_time_arrival=scheduled_time_arrival))
						fact_time_arrival = response_dict.get("arrival", {}).get("runwayTimeLocal", "Нет данных")
						logger.debug("Получено фактическое время прилета: {fact_time_arrival}".format(fact_time_arrival=fact_time_arrival))
						arrival_airport_code = response_dict.get("arrival", {}).get("airport", {}).get("iata", "Нет данных")
						logger.debug("Получен код аэропорта прилета: {arrival_airport_code}".format(arrival_airport_code=arrival_airport_code))
						arrival_airport_full_name = response_dict.get("arrival", {}).get("airport", {}).get("name", "Нет данных")
						logger.debug("Получено название аэропорта прилета: {arrival_airport_name}".format(arrival_airport_name=arrival_airport_full_name))
						arrival_terminal = response_dict.get("arrival", {}).get("terminal", "Нет данных")
						logger.debug("Получен терминал прилета: {arrival_terminal}".format(arrival_terminal=arrival_terminal))
						flight_status = response_dict.get("status", "Нет данных")
						logger.debug("Получен статус рейса: {flight_status}".format(flight_status=flight_status))
						last_update = response_dict.get("lastUpdatedUtc", "Нет данных")
						logger.debug("Получено время последнего обновления: {last_update}".format(last_update=last_update))

						# Формируем сообщение
						result_mess_for_user = "Авиакомпания: <b>{airline}</b>\n" \
											   "Номер рейса: <b>{flight_number}</b>\n" \
						                       "Бортовой номер самолета: <b>{aircraft}</b>\n" \
						                       "Тип самолета: <b>{aircraft_type}</b>\n" \
												"\n<b>Все время указано в формате локального времени аэропорта</b>\n" \
											"<u>Корректировка времени +/- относительно UTC</u>\n" \
											"\nЗапланированное время вылета: <b>{scheduled_departure}</b>\n" \
											"Пересмотренное время вылета: <b>{revised_departure}</b>\n" \
											"Фактическое время вылета: <b>{fact_departure}</b>\n" \
											"Код аэропорта вылета: <b>{departure_airport_code}</b>\n" \
											"Полное название аэропорта вылета: <b>{departure_airport_name}</b>\n" \
											"Терминал вылета: <b>{departure_terminal}</b>\n" \
											"Стойка регистрации вылета: <b>{check_in_desk}</b>\n" \
											"Гейт вылета: <b>{departure_gate}</b>\n\n" \
											"\n Запланированное время прибытия: <b>{scheduled_arrival}</b>\n" \
											"Фактическое время прибытия: <b>{fact_arrival}</b>\n" \
											"Код аэропорта прибытия: <b>{arrival_airport_code}</b>\n" \
											"Полное название аэропорта прибытия: <b>{arrival_airport_name}</b>\n" \
											"Терминал прибытия: <b>{arrival_terminal}</b>\n\n" \
											"\nСтатус рейса: <b>{status}</b>\n" \
											"Последнее обновление: <b>{last_update}</b>\n".format(
							airline=airline,
							flight_number=flight_number,
							aircraft=aircraft_reg_number,
							aircraft_type=aircraft_model,
							scheduled_departure=scheduled_time_departure,
							fact_departure=fact_time_departure,
							revised_departure=revised_time_departure,
							departure_airport_code=departure_airport_code,
							departure_airport_name=departure_airport_full_name,
							departure_terminal=departure_terminal,
							check_in_desk=check_in_desk,
							departure_gate=departure_gate,
							scheduled_arrival=scheduled_time_arrival,
							fact_arrival=fact_time_arrival,
							arrival_airport_code=arrival_airport_code,
							arrival_airport_name=arrival_airport_full_name,
							arrival_terminal=arrival_terminal,
							status=flight_status,
							last_update=last_update,
						)

						# Отправляем сообщение и фото пользователю
						bot.send_photo(message.chat.id, photo=photo_url)
						bot.send_message(message.chat.id, result_mess_for_user, parse_mode="HTML")

						# Записываем данные в БД
						logger.debug("Начало записи данных БД")
						try:
							information2db = []

							# Формируем данные в словарь
							data2db = {
									"command_name": "/custom",
									"user_id": message.from_user.id,
									"user_name": message.from_user.username,
									"airline_name": airline,
									"flight_number": flight_number,
									"aircraft_reg_number": aircraft_reg_number,
									"iata_departure": departure_airport_code,
									"terminal_departure": departure_terminal,
									"gate_departure": departure_gate,
									"revised_time_departure": revised_time_departure,
									"fact_time_departure": fact_time_departure,
									"iata_arrival": arrival_airport_code,
									"terminal_arrival": arrival_terminal,
									"flight_status": flight_status,
									"last_update_time": last_update,
							}

							logger.debug("Сформирован словарь для записи в БД: {data2db}".format(data2db=data2db))

							# Добавляем словарь в список
							information2db.append(data2db)
							logger.debug("Сформирован список для записи в БД: {information2db}".format(information2db=information2db))

							# Отправляем список собранных данные в БД
							db_write(db, Airplanes, information2db)
							logger.info("Данные были записаны в БД")

						except Exception as e:
							logger.error("Ошибка при записи данных в БД:")
							logger.exception(e)

					except Exception as e:
						logger.error("Пользователь не получил информацию, ошибка при получении данных от API:")
						logger.exception(e)
						# Вывод сообщения пользователю
						bot.send_message(message.chat.id, "Мы не смогли найти для вас информацию, попробуйте позже.")

				except AttributeError as e:
					logger.error("Ошибка при выполнении запроса к API:")
					logger.exception(e)
					# Вывод сообщения пользователю
					bot.send_message(message.chat.id, "Упс... у нас что-то с сервером.\n"
					                                  "Мы уже разбираемся, попробуйте позже.")

		except Exception as e:
			logger.error("Ошибка при получении данных в хранилище:")
			logger.exception(e)

		# Создаём клавиатуру навигации
		main_keyboard = name_all_commands()
		bot.send_message(message.from_user.id, "Выберите действие", reply_markup=main_keyboard)
		logger.debug("Создалась клавиатура навигации")

		# Удаляем состояние пользователя
		bot.delete_state(message.from_user.id, message.chat.id)
		logger.debug("Состояние пользователя было удалено")
		logger.warning("Конец сценария /custom")


	# Если дата введена верно
	else:
		bad_mess = "Дата введена не верно! Попробуй еще раз.\n" \
		           "Пример <b>{data}</b>".format(data=datetime.datetime.now().strftime("%Y-%m-%d"))
		bot.send_message(message.chat.id, bad_mess, parse_mode="HTML")
		logger.warning("Пользователь {user} ввел неверную дату".format(user=message.from_user.first_name))
