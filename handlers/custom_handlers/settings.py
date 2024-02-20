from database.database import db, User
from keyboards.inline.set_settings import create_buttons
from loader import bot
from telebot.types import Message
from loguru import logger
from handlers.custom_handlers.any_message import any_message_handler


@logger.catch
@bot.message_handler(commands=['settings'])
async def settings(message: Message) -> None:
    """
    Данная функция позволяет пользователю настроить генерацию.
    :param message: сообщение
    :return: None
    """

    await any_message_handler(message)
    logger.info(f'chat_id: {message.chat.id} message: {message.text}')
    keyboard_id = await bot.send_message(message.chat.id, 'Настройки генерации: ', reply_markup=await create_buttons(message))
    keyboard_id = keyboard_id.id
    with db:
        user = User.get(telegram_id=message.chat.id)
        user.keyboard = keyboard_id
        user.save()
