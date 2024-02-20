from telebot.asyncio_handler_backends import State, StatesGroup
from config_data.config import API_KEY
from utils.misc.api_fucntions import get_chat_completion, send_chat_request
from loader import bot
from telebot.types import Message
from database.database import db, User

from loguru import logger


class UserInfoState(StatesGroup):
    write_prompt = State()


@logger.catch
@bot.message_handler(state='*', commands=['exit'])
async def any_state(message) -> None:
    """
    Отменяет состояние
    :param message: сообщение
    :return: None
    """

    logger.info(f'Пользователь: {message.chat.id} отменил состояние')
    current_state = await bot.get_state(message.chat.id)

    if current_state is None:
        return

    await bot.send_message(message.chat.id, "Вы вышли из состояния")
    await bot.delete_state(message.chat.id, message.chat.id)


@logger.catch
@bot.message_handler(state=UserInfoState.write_prompt)
async def write_prompt(message: Message) -> None:
    """
    Ставит состояние пользователя
    :param message: сообщение
    :return: None
    """
    conversation_history = [
        {'role': 'system', 'content': 'Ты бот-рассказчик, придумывающий истории по промпту человека'}]
    with db:
        user = User.get(telegram_id=message.chat.id)
        if_story, if_image = user.generate_story, user.generate_image
        state = user.state
    if await check_message(message.text) and state == 'ready' and any([if_story, if_image]):
        await make_requests(message, if_story, if_image, conversation_history)
    elif not any([if_story, if_image]):
        await bot.send_message(message.chat.id, "Вы не выбрали в настройках какую-либо генерацию.")
    elif state != 'ready':
        await bot.reply_to(message, "Подождите, идёт генерация.")


async def make_requests(message, if_story, if_image, conversation_history):
    with db:
        user = User.get(telegram_id=message.chat.id)
        user.state = 'generating'
        user.save()
    if if_image:
        content = await send_chat_request(API_KEY, message.text)
    if if_story:
        result, conversation_history = await get_chat_completion(API_KEY, message.text, conversation_history)
    if if_image:
        await bot.send_photo(message.chat.id, content)
    if if_story:
        await bot.send_message(message.chat.id, result)
    with db:
        user = User.get(telegram_id=message.chat.id)
        user.state = 'ready'
        user.save()


async def check_message(message):
    return True
