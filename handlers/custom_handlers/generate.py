from database.database import User, db
from loader import bot
from telebot.types import Message

from states.keyboards import generate_and_settings
from states.write_story import UserInfoState, any_state
from loguru import logger
from handlers.custom_handlers.any_message import any_message_handler


@logger.catch
@bot.message_handler(state='*', commands=['generate'])
def start_generating(message: Message) -> None:
    """
    Данная функция позволяет пользователю настроить генерацию.
    :param message: сообщение
    :return: None
    """

    any_message_handler(message)
    logger.info(f'chat_id: {message.chat.id} message: {message.text}')
    # generate_and_settings(message)
    bot.send_message(message.chat.id, 'Введите текст для истории')

    logger.info(f'Пользователь: {message.chat.id} находится в состоянии write_story')
    bot.set_state(message.from_user.id, UserInfoState.write_prompt, message.chat.id)
