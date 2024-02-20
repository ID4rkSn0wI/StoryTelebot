from telebot.types import Message
from loader import bot
from loguru import logger
from handlers.custom_handlers.any_message import any_message_handler


@logger.catch
@bot.message_handler(commands=['start'])
async def bot_start(message: Message) -> None:
    """
    Данная функция начинает переписку и создает в базе данных и в состояниях пользователя по id
    :param message: сообщение
    :return: None
    """

    await any_message_handler(message)
    await bot.reply_to(message, f"Здравствуй, {message.from_user.full_name}! Данный бот создан для создания историй по вашему запросу.")
    logger.info(f'chat_id {message.from_user.id} message text {message.text}')