from telebot.types import Message
from loader import bot
from database.database import db, create_user, User
from loguru import logger


def any_message_handler(message: Message):
    """
    Данная функция обрабатывает неизвестные команды, выводя соответсвующее сообщение
    :param message: сообщение
    :return: None
    """

    logger.info(f'chat_id {message.from_user.id} message text {message.text}')

    with db:
        create_user(message.from_user.full_name, chat_id=message.chat.id)
        user = User.get(telegram_id=message.chat.id)
        if_story, if_image = user.generate_story, user.generate_image
        if user.keyboard:
            bot.edit_message_text(chat_id=message.chat.id, message_id=user.keyboard,
                                  text=f"Настройки сохранены:\n{'✅' if if_story else '➖'} Генерировать текст\n"
                                       f"{'✅' if if_image else '➖'} Генерировать изображения")
            user.keyboard = 0
        user.save()