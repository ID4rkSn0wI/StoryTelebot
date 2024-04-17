import asyncio
import json
from json import JSONDecodeError
from threading import Semaphore, Thread

from telebot.handler_backends import State, StatesGroup
from config_data.config import API_KEY, DEFAULT_COMMANDS
from states.keyboards import main_menu
from utils.misc.api_fucntions import get_chat_completion, send_chat_request
from loader import bot
from telebot.types import Message
from database.database import db, User
import handlers
from loguru import logger


semaphore = Semaphore(1)


class UserInfoState(StatesGroup):
    write_prompt = State()


@logger.catch
@bot.message_handler(state='*', commands=['exit'])
def any_state(message) -> None:
    """
    Отменяет состояние
    :param message: сообщение
    :return: None
    """

    logger.info(f'Пользователь: {message.chat.id} вышел в главное меню')
    current_state = bot.get_state(message.chat.id)

    if current_state is None:
        return

    bot.send_message(message.chat.id, "Вы вышли в главное меню")
    main_menu(message)
    bot.delete_state(message.chat.id, message.chat.id)


@logger.catch
@bot.message_handler(state=UserInfoState.write_prompt)
def write_prompt(message: Message) -> None:
    """
    Ставит состояние пользователя
    :param message: сообщение
    :return: None
    """

    logger.info(f'Пользователь: {message.chat.id} запросил истоию про {message.text}')
    # if message.text == 'Выйти в главное меню':
    #     any_state(message)
    #     return
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
        state = user.ready_state
    if (check_message(message.text) and state == 'ready' and any([if_story, if_image]) and
            message.text not in list(map(lambda x: '/' + x[0], DEFAULT_COMMANDS))):
        cur_message = bot.send_message(message.chat.id, "Ожидайте очереди!")
        logger.info(f'Пользователь: {message.chat.id} ожидает очереди')
        make_requests(message, if_story, if_image, conversation_history, cur_message.id, history)
    elif message.text in list(map(lambda x: '/' + x[0], DEFAULT_COMMANDS)):
        any_state(message)
        if message.text == '/start':
            handlers.default_handlers.start.bot_start(message)
        elif message.text == '/help':
            handlers.default_handlers.help.bot_help(message)
        elif message.text == '/settings':
            handlers.custom_handlers.settings.settings(message)
    elif not any([if_story, if_image]):
        bot.send_message(message.chat.id, "Вы не выбрали в настройках какую-либо генерацию.")
    elif state != 'ready':
        bot.reply_to(message, "У вас идёт генерация, подождите.")
    elif not check_message(message.text):
        bot.send_message(message.chat.id, "Неверный формат ввода текста.")


@logger.catch
def make_requests(message, if_story, if_image, conversation_history, previous_message_id, history):
    semaphore.acquire()
    with db:
        user = User.get(telegram_id=message.chat.id)
        user.ready_state = 'generating'
        user.save()
    bot.delete_message(message.chat.id, previous_message_id)
    message_id = bot.send_message(message.chat.id, "Идёт процесс генерации 🔳🔳🔳🔳🔳🔳🔳🔳🔳🔳 0%")
    message_id = message_id.id
    if if_story:
        bot.edit_message_text("Идёт процесс генерации ⬜️⬜️⬜️🔳🔳🔳🔳🔳🔳🔳 30%", message.chat.id, message_id)
    logger.info(f'Пользователь: {message.chat.id} отправил запрос текста')
    result, conversation_history = get_chat_completion(API_KEY, message.text, conversation_history)
    logger.info(f'Пользователь: {message.chat.id} получил запрос текста')
    if if_story:
        bot.edit_message_text("Идёт процесс генерации ⬜️⬜️⬜️⬜️⬜️🔳🔳🔳🔳🔳 50%", message.chat.id, message_id)
    if if_image:
        bot.edit_message_text("Идёт процесс генерации ⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳🔳 80%", message.chat.id, message_id)
        logger.info(f'Пользователь: {message.chat.id} отправил запрос изображения')
        content = send_chat_request(API_KEY, result)
        logger.info(f'Пользователь: {message.chat.id} получил запрос изображения')
        bot.edit_message_text("Идёт процесс генерации ⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ 100%", message.chat.id, message_id)
        if content:
            bot.send_photo(message.chat.id, content)
        else:
            bot.send_message(message.chat.id, "ОШИБКА. Не удалось сгенерировать изображение по вашему запросу")
    semaphore.release()
    if if_story:
        if result:
            bot.send_message(message.chat.id, result)
        else:
            bot.send_message(message.chat.id, "ОШИБКА. Не удалось сгенерировать историю по вашему запросу")
    with db:
        user = User.get(telegram_id=message.chat.id)
        user.ready_state = 'ready'
        user.save()
    history.setdefault(f"{message.chat.id},{message.from_user.id}", [])
    history[f"{message.chat.id},{message.from_user.id}"] = conversation_history
    with open("request_history.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(history, indent=4, ensure_ascii=False))
    bot.delete_message(message.chat.id, message_id)
    return conversation_history


def check_message(message):
    if '!' not in message and '?' not in message:
        return True
    return False
