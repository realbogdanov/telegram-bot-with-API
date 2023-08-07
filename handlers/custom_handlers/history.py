import time
import datetime
from loguru import logger
from keyboards.inline.keyboard_all_command import name_all_commands
from keyboards.reply.keyboard3days_data import three_days_data
from loader import bot
from telebot.types import Message
from database.common.models import Airports, Airplanes
from states.states2history import UserStates
from keyboards.inline.keyboard_with_commands import name_commands
from utils.misc.cheking2history import check_command, check_date


logger.add("logs/logs_history.log", level="ERROR", format="{time} {level} {message}", rotation="500 MB", compression="zip")


# Обработчик callback /history по нажатию кнопки в меню
@logger.catch
@bot.callback_query_handler(func=lambda call: call.data == "/history")
def callback_history(call) -> None:
	"""
	Функция обработчик callback запроса для просмотра истории поисковых запросов.

	Parameters:
	     call: Объект с информацией о callback запросе от пользователя

	Returns:
	     None

	"""
	logger.warning("Пользователь {user} начал работу с callback history".format(user=call.from_user.first_name))

	# Изменение состояния пользователя
	bot.set_state(call.from_user.id, UserStates.get_command, call.message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на get_command".format(user=call.from_user.first_name))
	good_mess = "Привет {user}! Здесь ты можешь посмотреть свою историю поисков.".format(user=call.from_user.first_name)

	# Создаем клавиатуру с командами
	keyboard_commands = name_commands()
	bot.send_message(call.message.chat.id, good_mess, reply_markup=keyboard_commands, parse_mode="HTML")
	logger.info("Пользователь {user} получил клавиатуру с командами".format(user=call.from_user.first_name))


# Обработчик команды /history
@logger.catch
@bot.message_handler(commands=['history'])
def command_history(message: Message) -> None:
	"""
	Функция обработчик сообщения для просмотра истории поисковых запросов.

	Parameters:
	     message (telebot.types.Message): Объект сообщения от пользователя.

	Returns:
	     None

	"""
	logger.warning("Пользователь {user} начал работу с командой history".format(user=message.from_user.first_name))

	# Изменение состояния пользователя
	bot.set_state(message.from_user.id, UserStates.get_command, message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на get_command".format(user=message.from_user.first_name))
	good_mess = "Привет {user}! Здесь ты можешь посмотреть свою историю поисков.".format(user=message.from_user.first_name)

	# Создаем клавиатуру с командами
	keyboard_commands = name_commands()
	bot.send_message(message.chat.id, good_mess, reply_markup=keyboard_commands, parse_mode="HTML")
	logger.info("Пользователь {user} получил клавиатуру с командами".format(user=message.from_user.first_name))


@logger.catch
@bot.callback_query_handler(func=lambda call: call, state=UserStates.get_command)
def get_command(call) -> None:
	"""
	Обработчик выбора команды для просмотра истории поисковых запросов.

	Parameters:
	    call (telebot.types.CallbackQuery): Объект callback-запроса от пользователя.

	Returns:
	    None

	"""

	# Проверяем, какую пользователь выбрал команду и возвращаем ему команду и ответ
	user_serach_command, answer_callback_query = check_command(call.data)
	logger.debug("Получен тип данных из проверочной функции check_command(): {data}".format(data=type(check_command(call.data))))
	logger.info("Пользователь {user} выбрал команду {command}".format(user=call.message.from_user.first_name,
	                                                                  command=user_serach_command))

	# Записываем в данные пользователя команду, которую он выбрал
	try:
		with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
			data["command"] = user_serach_command
			logger.info("Записалась в хранилище команда: {data}".format(data=user_serach_command))

	except Exception as e:
		logger.error("Возникла ошибка при записи данных:")
		logger.exception(e)

	bot.answer_callback_query(call.id, text=answer_callback_query)

	# Запрашиваем у пользователя количество записей, которое он хочет получить
	bot.send_message(call.message.chat.id, "Пожалуйста, введите количество записей, которое вы хотите получить.")
	logger.info("Пользователь {user} получил запрос на ввод количества записей".format(user=call.from_user.first_name))

	# Изменяем состояние пользователя
	bot.set_state(call.from_user.id, UserStates.get_count, call.message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на get_count".format(user=call.from_user.first_name))


@logger.catch
@bot.message_handler(state=UserStates.get_count)
def get_count(message: Message) -> None:
	"""
	Обработчик ввода количества записей, которое пользователь хочет получить.

    Parameters:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None
	"""

	# Проверяем ввод пользователя на число
	if message.text.isdigit():
		logger.info("Пользователь {user} ввел число {count}".format(user=message.from_user.first_name, count=message.text))

		# Записываем в данные пользователя количество записей, которое пользователь хочет получить
		try:
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				data["count"] = int(message.text)
				logger.info("Записалось в хранилище количество записей: {data}".format(data=int(message.text)))

		except Exception as e:
			logger.error("Возникла ошибка при записи данных:")
			logger.exception(e)

		# Запрашиваем у пользователя дату, с которой он хочет получить записи
		good_mess = "Пожалуйста, введите дату в следующем формате: <b>{data}</b>".format(data=datetime.datetime.now().strftime("%Y-%m-%d"))
		# Создаём клавиатуру с датами
		keyboard_data = three_days_data()
		bot.send_message(message.chat.id, good_mess, reply_markup=keyboard_data, parse_mode="HTML")
		logger.info("Пользователь {user} получил запрос на ввод даты".format(user=message.from_user.first_name))
		bot.set_state(message.from_user.id, UserStates.get_date2history, message.chat.id)
		logger.debug("Пользователь {user} изменил состояние на get_date".format(user=message.from_user.first_name))

	# Если пользователь ввел не число, то просим его ввести число
	else:
		bot.send_message(message.chat.id, "Пожалуйста, введите число.")
		logger.warning("Пользователь {user} ввел не число".format(user=message.from_user.first_name))


@logger.catch
@bot.message_handler(state=UserStates.get_date2history)
def get_date(message: Message) -> None:
	"""
	Обработчик получения даты, с которой пользователь хочет получить записи.
	И выводит пользователю записи, которые он хочет получить.

	Parameters:
		message (telebot.types.Message): Объект сообщения от пользователя.

	Returns:
		None
	"""

	# Проверяем ввод пользователя на дату
	if check_date(message.text):
		logger.info("Пользователь {user} ввел дату {date}".format(user=message.from_user.first_name, date=message.text))

		bot.send_message(message.chat.id, "Пожалуйста, подождите, идет поиск...")
		logger.info("Пользователь {user} получил сообщение о начале поиска".format(user=message.from_user.first_name))

		# Реализуем задержку для имитации поиска
		time.sleep(1)

		# Формируем данные для запроса
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			user_command = data["command"]
			user_count = data["count"]
			logger.info("Все данные из хранилища получены.")
			user_date = message.text

		# Счетчик для кол-ва записей и флаг для проверки наличия записей
		counter = 0
		found_records = False

		# Условие если пользователь выбрал команду /custom
		if user_command == "/custom":
			# Получаем данные из БД
			airplanes = Airplanes.select()
			logger.debug("Данные из ответа БД Airplanes: {response_airplanes}".format(response_airplanes=airplanes))

			# Перебираем данные из БД Airplanes
			for items in airplanes:
				# Преобразуем объект даты из БД в строку для сравнения с датой, которую ввел пользователь
				date_obj = items.date_creation
				date_str = date_obj.strftime("%Y-%m-%d")

				# Сортируем данные из БД по дате, id пользователя и команде и кол-ву записей
				if (date_str == user_date) and (items.user_id == message.from_user.id) and \
						(user_command == items.command_name) and (counter < user_count):
					logger.info("В БД Airports найдены подходящие записи.")

					try:
						# Формируем сообщение для пользователя
						mess = "Авиакомания: <b>{airline}</b>\n" \
							   "Номер рейса: <b>{flight_number}</b>\n" \
						       "Бортовой номер самолёта: <b>{aircraft_reg_number}</b>\n" \
						       "\nФактическое время вылета: <b>{fact_departure_time}</b>\n" \
						       "Код Аэропорта вылета: <b>{departure_airport_code}</b>\n" \
						       "Терминал вылета: <b>{departure_terminal}</b>\n" \
						       "\nКод Аэропорта прибытия: <b>{arrival_airport_code}</b>\n" \
						       "Терминал прибытия: <b>{arrival_terminal}</b>\n" \
						       "\nСтатус рейса: <b>{status}</b>\n" \
						       "Последня дата обновления при запросе: <b>{last_update_date}</b>".format(
							airline=items.airline_name,
							flight_number=items.flight_number,
							aircraft_reg_number=items.aircraft_reg_number,
							fact_departure_time=items.fact_time_departure,
							departure_airport_code=items.iata_departure,
							departure_terminal=items.terminal_departure,
							arrival_airport_code=items.iata_arrival,
							arrival_terminal=items.terminal_arrival,
							status=items.flight_status,
							last_update_date=items.last_update_time
						)
						bot.send_message(message.chat.id, mess, parse_mode="HTML")
						logger.info("Пользователь {user} получил сообщение с записью из БД Airplanes".format(
							user=message.from_user.first_name))

						# Реализуем задержку для имитации поиска
						time.sleep(1)

						# Увеличиваем счетчик и меняем флаг
						counter += 1
						found_records = True
						logger.info("Счетчик: {counter}".format(counter=counter))
						logger.info("Флаг: {flag}".format(flag=found_records))

					except Exception as e:
						logger.error("Не получилось сформировать сообщение для пользователя с данными из БД Airplanes:")
						logger.exception(e)

			# Если записи не найдены, отправляем сообщение об ошибке
			if not found_records:
				logger.error("Для пользователя {user} не найдено записей в БД Airplanes".format(
						user=message.from_user.first_name))
				bot.send_message(message.chat.id,
				                 "К сожалению, мы не смогли найти историю ваших поисковых запросов.\n"
				                 "Пожалуйста, убедитесь, что вы ввели правильную дату и использовали "
				                 "правильную команду для поиска.\n"
				                 "Попробуйте ввести другую дату или выполнить новый поиск.")

		# Условие если пользователь выбрал команды /high или /low
		elif (user_command == "/high") or (user_command == "/low"):
			# Получаем данные из БД
			airport = Airports.select()
			logger.debug("Данные из ответа БД Airports: {response_airport}".format(response_airport=airport))

			# Перебираем данные из БД Airports
			for items in airport:
				# Преобразуем объект даты из БД в строку для сравнения с датой, которую ввел пользователь
				date_obj = items.date_creation
				date_str = date_obj.strftime("%Y-%m-%d")

				# Сортируем данные из БД по дате, id пользователя и команде и кол-ву записей
				if (date_str == user_date) and (items.user_id == message.from_user.id) \
						and (user_command == items.command_name) and (counter < user_count):
					logger.info("В БД Airports найдены подходящие записи.")

					try:
						# Отправляем пользователю данные
						mess = "<b>Код:</b> {code_airport}\n" \
						       "<b>Название:</b> {name}\n" \
						       "<b>Местоположение:</b>  https://maps.google.com/?q={lat},{lon}".format(
								code_airport=items.iata,
								name=items.full_airport_address,
								lat=items.location_lat,
								lon=items.location_lon, )
						bot.send_message(message.chat.id, mess, parse_mode="HTML")
						logger.info("Пользователь {user} получил сообщение с записью из БД Airports".format(
							user=message.from_user.first_name))

						# Реализуем задержку для имитации поиска
						time.sleep(1)

						# Увеличиваем счетчик и меняем флаг
						counter += 1
						found_records = True
						logger.info("Счетчик: {counter}".format(counter=counter))
						logger.info("Флаг: {flag}".format(flag=found_records))

					except Exception as e:
						logger.error("Не получилось сформировать сообщение для пользователя с данными из БД Airports:")
						logger.exception(e)

			# Если записи не найдены, отправляем сообщение об ошибке
			if not found_records:
				logger.error("Для пользователя {user} не найдено записей в БД Airports".format(
						user=message.from_user.first_name))
				bot.send_message(message.chat.id,
				                 "К сожалению, мы не смогли найти историю ваших поисковых запросов.\n"
				                 "Пожалуйста, убедитесь, что вы ввели правильную дату и использовали "
				                 "правильную команду для поиска.\n"
				                 "Попробуйте ввести другую дату или выполнить новый поиск.")

		# Создаём клавиатуру навигации
		main_keyboard = name_all_commands()
		bot.send_message(message.from_user.id, "Выберите действие", reply_markup=main_keyboard)
		logger.debug("Создалась клавиатура навигации")

		# Удаляем state пользователя
		bot.delete_state(message.from_user.id, message.chat.id)
		logger.debug("Удалил state пользователя {user}".format(user=message.from_user.first_name))
		logger.warning("Конец сценария /history")

	# Если пользователь ввел неверный формат даты, то просим его ввести дату еще раз
	else:
		logger.warning("Пользователь {user} ввел неверный формат даты".format(user=message.from_user.first_name))
		bot.send_message(message.chat.id, "Вы ввели неверный формат даты, попробуйте еще раз. \nПример: <b>1996-05-12</b>",
		                 parse_mode="HTML")
