import asyncio
import json
from json import JSONDecodeError

from telebot.asyncio_handler_backends import State, StatesGroup
from config_data.config import API_KEY, DEFAULT_COMMANDS
from utils.misc.api_fucntions import get_chat_completion, send_chat_request
from loader import bot
from telebot.types import Message
from database.database import db, User
import handlers
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
        {'role': 'system', 'content': 'Ты рассказываешь придуманные и необычные истории по тексту пользователя'}
    ]
    with open('request_history.json', encoding='utf-8') as f:
        try:
            history = json.load(f)
        except JSONDecodeError:
            history = {}
    if f"{message.chat.id},{message.from_user.id}" in history:
        conversation_history = history[f"{message.chat.id},{message.from_user.id}"]
    with db:
        user = User.get(telegram_id=message.chat.id)
        if_story, if_image = user.generate_story, user.generate_image
        state = user.state
    if (await check_message(message.text) and state == 'ready' and any([if_story, if_image]) and
            message.text not in list(map(lambda x: '/' + x[0], DEFAULT_COMMANDS))):
        cur_message = await bot.send_message(message.chat.id, "Ожидайте очереди!")
        conversation_history = await make_requests(message, if_story, if_image, conversation_history, cur_message.id)
        history.setdefault(f"{message.chat.id},{message.from_user.id}", [])
        history[f"{message.chat.id},{message.from_user.id}"].extend(conversation_history)
        with open("request_history.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(history, indent=4, ensure_ascii=False))
    elif message.text in list(map(lambda x: '/' + x[0], DEFAULT_COMMANDS)):
        await any_state(message)
        if message.text == '/start':
            await handlers.default_handlers.start.bot_start(message)
        elif message.text == '/help':
            await handlers.default_handlers.help.bot_help(message)
        elif message.text == '/settings':
            await handlers.custom_handlers.settings.settings(message)
    elif not any([if_story, if_image]):
        await bot.send_message(message.chat.id, "Вы не выбрали в настройках какую-либо генерацию.")
    elif state != 'ready':
        await bot.reply_to(message, "У вас идёт генерация, подождите.")
    elif not await check_message(message.text):
        await bot.send_message(message.chat.id, "Неверный формат ввода текста.")


@logger.catch
async def make_requests(message, if_story, if_image, conversation_history, previous_message_id):
    with db:
        user = User.get(telegram_id=message.chat.id)
        user.state = 'generating'
        user.save()
    await bot.delete_message(message.chat.id, previous_message_id)
    message_id = await bot.send_message(message.chat.id, "Идёт процесс генерации 🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳 0%")
    message_id = message_id.id
    if if_story:
        await bot.edit_message_text("Идёт процесс генерации ⬜️⬜️⬜️🔳🔳🔳🔳🔳🔳🔳 30%", message.chat.id, message_id)
    result, conversation_history = await get_chat_completion(API_KEY, message.text, conversation_history)
    if if_story:
        await bot.edit_message_text("Идёт процесс генерации ⬜️⬜️⬜️⬜️⬜️🔳🔳🔳🔳🔳 50%", message.chat.id, message_id)
    if if_image:
        await bot.edit_message_text("Идёт процесс генерации ⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳🔳 80%", message.chat.id, message_id)
        content = await send_chat_request(API_KEY, result)
        await bot.edit_message_text("Идёт процесс генерации ⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ 100%", message.chat.id, message_id)
        if content:
            await bot.send_photo(message.chat.id, content)
        else:
            await bot.send_message(message.chat.id, "ОШИБКА. Не удалось сгенерировать изображение по вашему запросу")
    if if_story:
        if result:
            await bot.send_message(message.chat.id, result)
        else:
            await bot.send_message(message.chat.id, "ОШИБКА. Не удалось сгенерировать историю по вашему запросу")
    with db:
        user = User.get(telegram_id=message.chat.id)
        user.state = 'ready'
        user.save()
    await bot.delete_message(message.chat.id, message_id)
    return conversation_history


async def check_message(message):
    if '!' not in message and '?' not in message:
        return True
    return False
