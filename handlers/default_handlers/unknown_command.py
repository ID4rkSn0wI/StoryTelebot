from telebot.types import Message
from loader import bot
from loguru import logger
from handlers.custom_handlers.any_message import any_message_handler


@logger.catch
@bot.message_handler(func=lambda message: True)
async def bot_echo(message: Message):
    """
    Данная функция обрабатывает неизвестные команды, выводя соответсвующее сообщение
    :param message: сообщение
    :return: None
    """

    await any_message_handler(message)
    await bot.reply_to(message,
                       f"Неизвестная команда: {message.text}\nДля помощи по поиску команд введите команду /help")
    logger.info(f'chat_id {message.from_user.id} message text {message.text}')
