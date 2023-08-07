from loguru import logger

logger.add("logs/logs_validation.log", level="ERROR", format="{time} {level} {message}", rotation="500 MB", compression="zip")

def validate_api_data(response_from_api: dict) -> bool:
	"""
	Функция для проверки валидности данных от API для команды high и low

	Parameters:
	    response_from_api (dict): Данные, полученные от API

	Returns:
	    bool: True если данные валидны, иначе False
	"""

	try:
		# Проверка типа данных полученных от API, являются ли они словарем
		if not isinstance(response_from_api, dict):
			logger.error("Данные от API не являются словарем")
			return False

		logger.info("Данные от API являются словарем")

		# Определение списка обязательных ключей в ответе от API
		required_keys = ["iata", "name", "location",]

		if all(key in response_from_api for key in required_keys):
			logger.info("В ответе от API присутствуют все обязательные ключи")

			# Проверка типа данных ключей полученных от API на соответствие ожидаемым
			if ((isinstance(response_from_api[key], str) or isinstance(response_from_api[key], float))
					for key in required_keys):
				logger.info("В ответе от API все обязательные ключи имеют корректный тип данных")

				# Проверка типа данных ключа location на соответствие ожидаемому
				if isinstance(response_from_api["location"], dict):
					logger.info("В ответе от API ключ location имеет тип данных словарь")

					required_keys_location = ["lat", "lon",]

					# Проверка наличия обязательных ключей в ключе location
					if all(key in response_from_api["location"] for key in required_keys_location):
						logger.info("В ответе от API ключ location присутствуют все обязательные ключи")

						# Проверка типа данных ключей полученных от API на соответствие ожидаемым
						if all(isinstance(response_from_api["location"][key], float) for key in required_keys_location):
							logger.info("В ответе от API ключ location все обязательные ключи имеют тип данных float")
							return True

						else:
							logger.error("В ответе от API ключ location не все обязательные ключи имеют тип данных float")
							return False

			else:
				logger.error("В ответе от API не все обязательные ключи имеют тип данных строка")
				return False

		else:
			logger.error("В ответе от API отсутствуют обязательные ключи")
			return False

	except Exception as ex:
		# Если произошла ошибка при проверке данных от API
		logger.error("Произошла ошибка при проверке данных от API\n"
		             "Error: {e}".format(e=ex, ))

		return False
