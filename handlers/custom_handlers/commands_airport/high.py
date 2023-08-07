import time
from loguru import logger
from keyboards.inline.keyboard_all_command import name_all_commands
from loader import bot
from telebot.types import Message
from database.common.models import db, Airports
from database.core import crud
from handlers.custom_handlers.commands_airport.high_loader import site_api, headers, params, url
from states.states2high import UserStates
from keyboards.inline.keyboard2airports_count import count_airport
from utils.misc.validate_api_data import validate_api_data

db_write = crud.record_data

logger.add("logs/logs_high.log", level="ERROR", format="{time} {level} {message}", rotation="500 MB", compression="zip")


# Обработчик callback /high по нажатию кнопки в меню
@logger.catch()
@bot.callback_query_handler(func=lambda call: call.data == "/high")
def callback_high(call) -> None:
	"""
	Функция обработчик callback запроса для поиска аэропортов в городе, который введет пользователь
	И изменение состояния пользователя на UserInfoState.search_city

    Parameters:
        call: Объект с информацией о callback запросе от пользователя

    Returns:
        None

	"""
	# Изменение состояния пользователя
	logger.warning("Пользователь {user} начал работу с callback high".format(user=call.from_user.first_name))
	bot.set_state(call.from_user.id, UserStates.search_city, call.message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на search_city".format(user=call.from_user.first_name))
	good_mess = "Привет {user}! Я готов помочь тебе найти аэропорты в городе, который ты выберешь.\n " \
	            "\nПожалуйста, <b>напиши мне название города в котором ты хочешь найти аэропорт.\n" \
	            "Или код аэропорта который ты хочешь найти (пример: DME), </b>".format(user=call.from_user.first_name)
	bot.send_message(call.message.chat.id, good_mess, parse_mode="HTML")
	logger.info("{user} получил сообщение с приветствием".format(user=call.from_user.first_name))


# Обработчик команды /high
@logger.catch()
@bot.message_handler(commands=["high"])
def command_high(message: Message) -> None:
	"""
	Функция обработчик сообщения для поиска аэропортов в городе, который введет пользователь
	И изменение состояния пользователя на UserInfoState.search_city

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None

	"""
	# Изменение состояния пользователя
	logger.warning("Пользователь {user} начал работу с command high".format(user=message.from_user.first_name))
	bot.set_state(message.from_user.id, UserStates.search_city, message.chat.id)
	logger.debug("Пользователь {user} изменил состояние на search_city".format(user=message.from_user.first_name))
	good_mess = "Привет {user}! Я готов помочь тебе найти аэропорты в городе, который ты выберешь.\n " \
	            "\nПожалуйста, <b>напиши мне название города в котором ты хочешь найти аэропорт.\n" \
	            "Или код аэропорта который ты хочешь найти (пример: DME), </b>".format(user=message.from_user.first_name)
	bot.send_message(message.chat.id, good_mess, parse_mode="HTML")
	logger.info("{user} получил сообщение с приветствием".format(user=message.from_user.first_name))


@logger.catch
@bot.message_handler(state=UserStates.search_city)
def get_city_name(message: Message) -> None:
	"""
	Функция для получения названия города от пользователя
	И изменение состояния пользователя на UserInfoState.count_airport

    Parameters:
        message (Message): Объект сообщения от пользователя

    Returns:
        None

	"""

	# Проверка длины строки
	if len(message.text) >= 3:
		logger.info("Ввод города от пользователя {user} прошёл проверку".format(user=message.from_user.first_name, ))

		# Меняем состояние пользователя
		bot.set_state(message.from_user.id, UserStates.count_airport2high, message.chat.id)
		logger.debug("Пользователь {user} изменил состояние на count_airport".format(user=message.from_user.first_name))

		good_mess = "Отлично, записал👌🏼. \n<b>Введите кол-во аэропортов для поиска</b>"

		# Создаем клавиатуру с кол-вом аэропортов
		keyboard_count_airport = count_airport()
		bot.send_message(message.chat.id, good_mess, reply_markup=keyboard_count_airport, parse_mode="HTML")
		logger.info("Пользователь {user} получил клавиатуру с кол-вом аэропортов".format(user=message.from_user.first_name))

		try:
			# Запись информации в хранилище данных
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				data["search_city"] = message.text
				logger.info("Записались в хранилище название города: {city}".format(city=message.text))

		except Exception as ex:
			logger.error("Возникла ошибка при записи данных:")
			logger.exception(ex)

	# Если длина строки < 3, то просим пользователя ввести название города еще раз
	else:
		bad_mess = "<b>Название города должно быть больше 3 символов</b>.\n" \
		           "Пожалуйста, введите название города еще раз."
		bot.send_message(message.chat.id, bad_mess, parse_mode="HTML")
		logger.warning("Пользователь {user} ввел название города длиной < 3 символов".format(
				user=message.from_user.first_name))


@logger.catch
@bot.callback_query_handler(func=lambda call:call, state=UserStates.count_airport2high)
def keyboard_click_and_get_count_airport(call) -> None:
	"""
	Функция для получения кол-ва аэропортов для поиска ближайших аэропортов
	C последующей записью в базу данных.


    Parameters:
        call: Объект с информацией о callback запросе от пользователя

    Returns:
        None

	"""

	logger.info("Пользователь {user} выбрал кол-во: {count_airport}".format(user=call.from_user.first_name,
			count_airport=call.data, ))

	# Запись и получение данных из хранилища данных
	try:
		with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
			# Получение данных из хранилища данных
			user_search_city = data["search_city"]
			user_count_airport = call.data
			logger.debug("Получили из хранилища данные: {city}, {count_airport}".format(city=user_search_city,
			                                                                            count_airport=user_count_airport, ))

			# Вывод сообщения пользователю
			good_mess = "Ваш запрос обрабатывается, и в ближайшее время вы получите результаты поиска. Пожалуйста, ожидайте."
			bot.answer_callback_query(call.id, text="Вы выбрали {count_airport}".format(count_airport=call.data, ))
			bot.send_message(call.message.chat.id, good_mess)
			logger.info("Пользователь {user} получил сообщение о том, что запрос обрабатывается".format(user=call.from_user.first_name, ))

			# Имитация поиска
			time.sleep(1)

			try:
				# Выполняем запрос к API
				search_airports_by_free_text = site_api.airports_text(method="GET", url=url, headers=headers, params=params,
				                                                      city_search=user_search_city,
				                                                      limit_search_airport=user_count_airport, )
				response_json = search_airports_by_free_text.json()
				logger.debug("Получен ответ от сервера: {response}".format(response=response_json, ))

				result_mess = response_json.get("items")
				logger.debug("Полученные данные по ключу items: {data}".format(data=result_mess, ))

				# Преобразуем полученные данные в словарь для проведения проверки на валидность
				response_dict = result_mess[0]
				logger.debug("Преобразованные данные от API из списка в словарь: {data}".format(data=response_dict))

				# Проверяем, что получен корректны ответ от сервера
				if validate_api_data(response_dict):
					information2db = []

					# Обрабатываем полученные результаты
					# выводим их пользователю и формируем данные для записи в БД
					for item in result_mess:
						iata = item.get("iata")
						full_airport_address_name = item.get("name")

						# Получение данных из ключа location
						if isinstance(item.get("location"), dict):
							lat = item.get("location").get("lat")
							lon = item.get("location").get("lon")

						mess = "<b>Код:</b> {code_airport}\n" \
						       "<b>Название:</b> {short_name}\n" \
						       "<b>Местоположение:</b>  https://maps.google.com/?q={lat},{lon}".format(code_airport=iata,
						                                                                               short_name=full_airport_address_name,
						                                                                               lat=lat, lon=lon, )

						# Записываем данные аэропорта в словарь
						# чтобы потом добавить в список для записи в БД всех аэропротов
						airport_info = {"command_name": "/high",
								"user_id":call.from_user.id,
								"user_name":call.from_user.username,
								"full_airport_address":full_airport_address_name,
								"iata":iata,
								"location_lat":lat,
								"location_lon":lon, }
						logger.debug("Информация об одном аэропорте записалась")

						# Добавил данные аэропорта в список для записи в БД
						information2db.append(airport_info)
						logger.debug("Информация записалась в список для записи в БД")

						bot.send_message(call.from_user.id, mess, parse_mode="HTML")
						logger.info("Пользователь {user} получил результат работы.".format(user=call.from_user.first_name, ))

			except Exception as ex:
				logger.error("Ошибка! получен не корректный ответ от сервера:")
				logger.exception(ex)
				# Вывод сообщения пользователю
				bot.send_message(call.from_user.id, "Ошибка: Получен не корректный ответ от сервера.\n"
				                                    "Попробуйте еще раз.")

	except Exception as ex:
		logger.error("Произошла ошибка при записи и выводе данных:")
		logger.exception(ex)
		# Вывод сообщения пользователю
		exc_mess = "К сожалению, мы не смогли найти аэропорты по вашему запросу. \n" \
		           "Пожалуйста, попробуйте выбрать другой город и повторите попытку --> /high"
		bot.send_message(call.from_user.id, exc_mess)
		logger.debug("Пользователь получил сообщение: {mess}".format(mess=exc_mess, ))

	try:
		# Записываем данные в БД
		db_write(db, Airports, information2db)
		logger.info("Данные были записаны в БД")

	except Exception as ex:
		logger.error("Произошла ошибка при записи данных в БД:")
		logger.exception(ex)

	finally:
		# Создаём клавиатуру навигации
		main_keyboard = name_all_commands()
		bot.send_message(call.from_user.id, "Выберите действие", reply_markup=main_keyboard)
		logger.debug("Создалась клавиатура навигации")

		# Удаляем состояние пользователя
		bot.delete_state(call.from_user.id, call.message.chat.id)
		logger.debug("Состояние пользователя было удалено")
		logger.warning("Конец сценария /high")
