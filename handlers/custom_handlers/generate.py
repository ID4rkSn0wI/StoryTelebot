from loader import bot
from telebot.types import Message

from states.write_story import UserInfoState
from loguru import logger
from database.database import User
from database.database import db, create_user
from handlers.custom_handlers.any_message import any_message_handler


@bot.message_handler(commands=['generate'])
def start_generating_generate(message: Message) -> None:
    """
    Данная функция позволяет пользователю настроить генерацию.
    :param message: сообщение
    :return: None
    """

    any_message_handler(message)
    logger.info(f'chat_id: {message.chat.id} message: {message.text}')
    logger.info(f'Пользователь: {message.chat.id} находится в состоянии write_story')
    bot.send_message(message.chat.id, 'Для выхода в меню введите /выйти')
    bot.send_message(message.chat.id, 'Введите промпт')

    with db:
        user = create_user(name=message.from_user.full_name, chat_id=message.chat.id)
        user.save()

    bot.set_state(message.chat.id, UserInfoState.write_prompt, message.chat.id)
