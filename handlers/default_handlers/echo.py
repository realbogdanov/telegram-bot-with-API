from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message, "😵Данный ввод не имеет специальную обработку.\n" f"Ввод: {message.text}"
    )
