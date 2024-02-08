from telebot.handler_backends import State, StatesGroup

from config_data.config import API_KEY
from utils.misc.api_fucntions import get_chat_completion, send_chat_request
from loader import bot
from telebot.types import Message
from database.database import db, User

from loguru import logger


class UserInfoState(StatesGroup):
    write_prompt = State()


@logger.catch
@bot.message_handler(state='*', commands='exit')
def any_state(message) -> None:
    """
    Отменяет состояние
    :param message: сообщение
    :return: None
    """

    logger.info(f'Пользователь: {message.chat.id} отменил состояние')
    current_state = bot.get_state(message.chat.id)

    if current_state is None:
        return

    bot.send_message(message.chat.id, "Вы вышли из состояния")
    bot.delete_state(message.chat.id, message.chat.id)


@logger.catch
@bot.message_handler(state=UserInfoState.write_prompt)
def write_prompt(message: Message) -> None:
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
    if check_message(message.text) and state == 'ready' and any([if_story, if_image]):
        with db:
            user = User.get(telegram_id=message.chat.id)
            user.state = 'generating'
            user.save()
        if if_image:
            send_chat_request(API_KEY, message.text)
        if if_story:
            result, conversation_history = get_chat_completion(API_KEY, message.text, conversation_history)
        if if_image:
            with open('temp_image.jpg', 'rb') as image:
                bot.send_photo(message.chat.id, image)
        if if_story:
            bot.send_message(message.chat.id, result)
        with db:
            user = User.get(telegram_id=message.chat.id)
            user.state = 'ready'
            user.save()
    elif not any([if_story, if_image]):
        bot.send_message(message.chat.id, "Вы не выбрали в настройках какую-либо генерацию.")
    elif state != 'ready':
        bot.reply_to(message, "Подождите, идёт генерация.")


def check_message(message):
    return True
