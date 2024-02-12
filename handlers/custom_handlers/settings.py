from keyboards.inline.set_settings import create_buttons
from loader import bot
from telebot.types import Message
from loguru import logger
from database.database import User
from database.database import db, create_user
from handlers.custom_handlers.any_message import any_message_handler


@logger.catch
@bot.message_handler(commands=['settings'])
def settings(message: Message) -> None:
    """
    Данная функция позволяет пользователю настроить генерацию.
    :param message: сообщение
    :return: None
    """

    any_message_handler(message)
    logger.info(f'chat_id: {message.chat.id} message: {message.text}')
    bot.send_message(message.chat.id, 'Настройки генерации: ', reply_markup=create_buttons(message))