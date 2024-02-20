from telebot.types import Message
from loader import bot
from loguru import logger
from database.database import db, create_user
from handlers.custom_handlers.any_message import any_message_handler


@bot.message_handler(commands=['start'])
async def bot_start(message: Message) -> None:
    """
    Данная функция начинает переписку и создает в базе данных и в состояниях пользователя по id
    :param message: сообщение
    :return: None
    """

    await any_message_handler(message)
    await bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    logger.info(f'chat_id {message.from_user.id} message text {message.text}')
