from telebot.types import Message
from loader import bot
from loguru import logger
from database.database import db, create_user


@bot.message_handler()
def bot_start(message: Message) -> None:
    """
    Данная функция начинает переписку и создает в базе данных и в состояниях пользователя по id
    :param message: сообщение
    :return: None
    """

    logger.info(f'chat_id {message.from_user.id} message text {message.text}')
    with db:
        create_user(message.from_user.full_name, chat_id=message.chat.id)