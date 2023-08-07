from telebot.types import Message

from loader import bot


# Обработчик текстовых сообщений от пользователя с текстом "привет"
@bot.message_handler(content_types=["text"], regexp="привет".lower())
def get_user_text(message: Message):
	mess = "И тебе привет 👻 {}.".format(message.from_user.first_name)
	bot.reply_to(message, mess)
