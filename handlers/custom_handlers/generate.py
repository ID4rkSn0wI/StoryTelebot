from loader import bot
from telebot.types import Message

from states.write_story import UserInfoState, any_state
from loguru import logger
from handlers.custom_handlers.any_message import any_message_handler


@logger.catch
@bot.message_handler(state='*', commands=['generate'])
async def start_generating(message: Message) -> None:
    """
    Данная функция позволяет пользователю настроить генерацию.
    :param message: сообщение
    :return: None
    """

    await any_message_handler(message)
    logger.info(f'chat_id: {message.chat.id} message: {message.text}')
    await bot.send_message(message.chat.id, 'Для выхода в меню введите /exit')
    await bot.send_message(message.chat.id, 'Введите текст для истории')

    logger.info(f'Пользователь: {message.chat.id} находится в состоянии write_story')
    await bot.set_state(message.from_user.id, UserInfoState.write_prompt, message.chat.id)
