from telebot.types import Message
from loader import bot
from loguru import logger
from handlers.custom_handlers.any_message import any_message_handler
from states.keyboards import main_menu


@logger.catch
@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Данная функция начинает переписку и создает в базе данных и в состояниях пользователя по id
    :param message: сообщение
    :return: None
    """

    any_message_handler(message)
    bot.reply_to(message, f"Здравствуй, {message.from_user.full_name}! Данный бот создан для создания историй по вашему запросу.")
    logger.info(f'chat_id {message.from_user.id} message text {message.text}')
    # main_menu(message)