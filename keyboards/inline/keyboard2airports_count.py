from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создание кнопки для вывода пользователю сайта с его ip адресом
def ip_address_site():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("Узнать свой ip", url="https://ifconfig.me/"))
	return keyboard


def count_airport():
	keyboard = InlineKeyboardMarkup(row_width=2)
	buttons = [InlineKeyboardButton(text=str(number), callback_data= str(number)) for number in range(1, 5)]
	keyboard.add(*buttons)
	return keyboard
