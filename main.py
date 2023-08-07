from loader import bot
from telebot.custom_filters import StateFilter
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from loguru import logger


if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    logger.add("logs/main_logs.log", level="ERROR", format="{time} {level} {message}", rotation="500 MB",
               compression="zip")
    logger.debug("Информация для отладки")
    logger.info("Информация о состоянии программы")
    logger.warning("Информация о предупреждении")
    logger.error("Информация об ошибке")
    set_default_commands(bot)
    bot.infinity_polling()
