from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from database.database import db, create_user
from loguru import logger
from handlers.custom_handlers.any_message import any_message_handler


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Данная функция выводит все команды бота
    :param message: сообщение
    :return: None
    """

    any_message_handler(message)
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
    logger.info(f'chat_id {message.from_user.id} message text {message.text}')
