from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.database import db, User
from loader import bot
from loguru import logger


@logger.catch
def create_buttons(message) -> InlineKeyboardMarkup():
    """
    Данная функция создает клавиатуру с местами поиска отелей, чтобы пользователь уточнил нужное место
    :return: InlineKeyboardMarkup()
    """
    with db:
        user = User.get(telegram_id=message.chat.id)
        if_story, if_image = user.generate_story, user.generate_image
        user.save()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f"{'✅' if if_story else '➖'} Генерировать текст", callback_data='1'))
    keyboard.add(InlineKeyboardButton(text=f"{'✅' if if_image else '➖'} Генерировать изображения", callback_data='2'))
    return keyboard


@logger.catch
@bot.callback_query_handler(func=lambda call: True)
def callback_keyboard(call) -> None:
    """
    Данная функция-обработчик выбора в клавиатуре
    :param call: сообщение в клавиатуре
    :return: None
    """

    if call.message and call.data:
        with db:
            user = User.get(telegram_id=call.message.chat.id)
            if_story, if_image = user.generate_story, user.generate_image
            if call.data == '1':
                user.generate_story = not if_story
            if call.data == '2':
                user.generate_image = not if_image
            user.save()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Настройки генерации:', reply_markup=create_buttons(call.message))
