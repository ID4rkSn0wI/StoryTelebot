from telebot.types import Message, ReplyKeyboardMarkup

from database.database import db, User
from handlers.custom_handlers.generate import start_generating
from loader import bot
from loguru import logger
from handlers.custom_handlers.any_message import any_message_handler
from states.write_story import any_state


@logger.catch
@bot.message_handler(func=lambda message: True)
def unknown_command(message: Message):
    """
    Данная функция обрабатывает неизвестные команды, выводя соответсвующее сообщение
    :param message: сообщение
    :return: None
    """

    any_message_handler(message)
    # with db:
    #     user = User.get(telegram_id=message.chat.id)
    #     state = user.state
    # if state == 'main' and message.text == 'Начать генерацию':
    #     start_generating(message)
    # elif state == 'settings' and message.text == 'Выйти в главное меню':
    #     any_state(message)
    # else:
    #     keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bot.reply_to(message,
                       f"Неизвестная команда: {message.text}\nДля помощи по поиску команд введите команду /help")
    logger.info(f'chat_id {message.from_user.id} message text {message.text}')
