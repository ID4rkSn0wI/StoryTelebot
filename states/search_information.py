# from telebot.handler_backends import State, StatesGroup
# from loader import bot
# from telebot.types import Message
# from utils.misc.request_to_api import make_request_to_api
# from utils.misc import link_path
# from datetime import datetime, date
# from loguru import logger
# from database.database import db, User
#
#
# class UserInfoState(StatesGroup):
#     city = State()
#     min_price = State()
#     max_price = State()
#     check_in = State()
#     check_out = State()
#     show_photos = State()
#     how_much_photos = State()
#     how_much_hotels = State()
#     distance_to_center = State()
#     retrieve_data = State()
#
#
# @logger.catch
# @bot.message_handler(state='*', commands='выйти')
# def any_state(message) -> None:
#     """
#     Отменяет состояние
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'Пользователь: {message.chat.id} отменил состояние')
#     current_state = bot.get_state(message.chat.id)
#
#     if current_state is None:
#         return
#
#     with db:
#         user = User.get(telegram_id=message.chat.id)
#         if user.call_hotels == '':
#             bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Уточните пожалуйста:',
#                                   reply_markup=None)
#
#     bot.send_message(message.chat.id, "Вы вышли из состояния")
#     bot.delete_state(message.chat.id, message.chat.id)
#
#
# @logger.catch
# def search_city(message: Message) -> None:
#     """
#     Ставит состояние пользователя
#     :param message: сообщение
#     :return: None
#     """
#
#     bot.set_state(message.chat.id, UserInfoState.city, message.chat.id)
#     logger.info(f'Пользователь: {message.chat.id} находится в состоянии city')
#     bot.send_message(message.chat.id, 'Для выхода в меню введите /выйти')
#     bot.send_message(message.chat.id, 'Введите название страны/города на русском')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.city)
# def get_city(message: Message) -> None:
#     """
#     Состояние пользователя по отправке места для поиска отелей
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#     url = "https://hotels4.p.rapidapi.com/locations/v2/search"
#     querystring = {"query": message.text, "locale": "ru_RU", "currency": "RUB"}
#     pattern = r'(?<="CITY_GROUP",).+?[\]]'
#
#     if match(message.text) and make_request_to_api(url, querystring, pattern):
#         with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#             data['city'] = message.text
#
#         bot.set_state(message.chat.id, UserInfoState.retrieve_data, message.chat.id)
#         link_path.path(message)
#
#     elif not match(message.text):
#         bot.send_message(message.chat.id, 'Ошибка. В строке присутствуют не только буквы русского алфавита')
#
#     else:
#         bot.send_message(message.chat.id, 'Ошибка. Такого места не существует')
#
#
# @logger.catch
# def start_distance_to_center(message: Message) -> None:
#     """
#     Ставит состояние пользователя
#     :param message: сообщение
#     :return: None
#     """
#     bot.set_state(message.chat.id, UserInfoState.distance_to_center, message.chat.id)
#     logger.info(f'Пользователь: {message.chat.id} находится в состоянии distance_to_center')
#     bot.send_message(message.chat.id, 'Введите расстояние до центра в км')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.distance_to_center)
# def get_distance_to_center(message: Message) -> None:
#     """
#     Состояние пользователя по получению расстояния до центра
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#
#     try:
#         with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#             data['distance_to_center'] = float(message.text)
#
#         bot.set_state(message.chat.id, UserInfoState.min_price, message.chat.id)
#         logger.info(f'Пользователь: {message.chat.id} находится в состоянии min_price')
#         bot.send_message(message.chat.id, 'Введите минимальную стоимость отеля в рублях')
#
#     except ValueError:
#         bot.send_message(message.chat.id, 'Вы должны ввести число')
#
#
# @logger.catch
# def min_price(message: Message) -> None:
#     """
#     Ставит состояние пользователя
#     :param message: сообщение
#     :return: None
#     """
#
#     bot.set_state(message.chat.id, UserInfoState.min_price, message.chat.id)
#     bot.send_message(message.chat.id, 'Введите минимальную стоимость отеля в рублях')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.min_price)
# def get_min_price(message: Message) -> None:
#     """
#     Состояние пользователя по отправке минимальной цены отеля
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#
#     try:
#         if message.text.isdigit() and int(message.text) > 0:
#             if int(message.text) > 0:
#                 with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#                     data['min_price'] = message.text
#
#                 bot.set_state(message.chat.id, UserInfoState.max_price, message.chat.id)
#                 logger.info(f'Пользователь: {message.chat.id} находится в состоянии max_price')
#                 bot.send_message(message.chat.id, 'Введите максимальную стоимость отеля в рублях')
#
#         elif int(message.text) < 0:
#             bot.send_message(message.chat.id, 'Ошибка. Введите число большее 0')
#
#     except ValueError:
#         bot.send_message(message.chat.id, 'Ошибка. Введите число')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.max_price)
# def get_max_price(message: Message) -> None:
#     """
#     Состояние пользователя по отправке максимальной цены отеля
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#
#     try:
#         with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#             minimal_price = data['min_price']
#
#         if message.text.isdigit() and int(message.text) > int(minimal_price):
#             with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#                 data['max_price'] = message.text
#
#             bot.set_state(message.chat.id, UserInfoState.check_in, message.chat.id)
#             logger.info(f'Пользователь: {message.chat.id} находится в состоянии check_in')
#             bot.send_message(message.chat.id, 'Введите число заезда в отель в формате yyyy-mm-dd')
#
#         elif int(message.text) < int(minimal_price):
#             bot.send_message(message.chat.id, 'Ошибка. Введите число большее минимальной цены')
#
#     except ValueError:
#         bot.send_message(message.chat.id, 'Ошибка. Введите число')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.check_in)
# def get_check_in(message: Message) -> None:
#     """
#     Состояние пользователя по отправке времени заезда отеля
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#
#     try:
#         date_obj = datetime.strptime(message.text, '%Y-%m-%d').date()
#
#         if date_obj >= date.today():
#             with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#                 data['check_in'] = date_obj
#
#             bot.set_state(message.chat.id, UserInfoState.check_out, message.chat.id)
#             logger.info(f'Пользователь: {message.chat.id} находится в состоянии check_out')
#             bot.send_message(message.chat.id, 'Введите число выезда из отеля в формате yyyy-mm-dd')
#
#         else:
#             bot.send_message(message.chat.id, 'Ошибка. Дата раньше сегодняшней даты')
#
#     except ValueError:
#         bot.send_message(message.chat.id, 'Ошибка. Неверный формат ввода')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.check_out)
# def get_check_out(message: Message) -> None:
#     """
#     Состояние пользователя по отправке времени выезда отеля
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#
#     try:
#         date_obj = datetime.strptime(message.text, '%Y-%m-%d').date()
#         with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#             date_obj_2 = data['check_in']
#         subtraction = date_obj - date_obj_2
#         if subtraction.days > 0:
#             with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#                 data['check_out'] = date_obj
#             bot.set_state(message.chat.id, UserInfoState.show_photos, message.chat.id)
#             logger.info(f'Пользователь: {message.chat.id} находится в состоянии show_photos')
#             bot.send_message(message.chat.id, 'Показывать фото да/нет')
#         else:
#             bot.send_message(message.chat.id, 'Ошибка. Введите дату выезда не меньшую даты заезда')
#
#     except ValueError:
#         bot.send_message(message.chat.id, 'Ошибка. Неверный формат ввода')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.show_photos)
# def show_photos(message: Message) -> None:
#     """
#     Состояние пользователя, где запрашивается отправка фото отеля
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#
#     if message.text.lower() == 'да':
#         with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#             data['show_photos'] = True
#
#         bot.set_state(message.chat.id, UserInfoState.how_much_photos, message.chat.id)
#         logger.info(f'Пользователь: {message.chat.id} находится в состоянии how_much_photos')
#         bot.send_message(message.chat.id, 'Введите количество фото не превышающее 5')
#
#     elif message.text.lower() == 'нет':
#         with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#             data['show_photos'] = False
#
#         bot.set_state(message.chat.id, UserInfoState.how_much_hotels, message.chat.id)
#         logger.info(f'Пользователь: {message.chat.id} находится в состоянии how_much_hotels')
#         bot.send_message(message.chat.id, 'Введите количество отелей не превышающее 10')
#
#     else:
#         bot.send_message(message.chat.id, 'Ошибка. Введите да/нет')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.how_much_photos)
# def how_much_photos(message: Message) -> None:
#     """
#     Состояние пользователя по отправке количества фотографий отеля
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#
#     try:
#
#         if message.text.isdigit() and 5 >= int(message.text) > 0:
#             with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#                 data['how_much_photos'] = int(message.text)
#
#             bot.set_state(message.chat.id, UserInfoState.how_much_hotels, message.chat.id)
#             logger.info(f'Пользователь: {message.chat.id} находится в состоянии how_much_hotels')
#             bot.send_message(message.chat.id, 'Введите количество отелей не превышающее 10')
#
#         elif int(message.text) < 0:
#             bot.send_message(message.chat.id, 'Ошибка. Число меньше 0')
#
#         elif int(message.text) == 0:
#             bot.send_message(message.chat.id, 'Ошибка. Число равняется 0')
#
#         elif int(message.text) > 5:
#             bot.send_message(message.chat.id, 'Ошибка. Число больше 5')
#
#     except ValueError:
#         bot.send_message(message.chat.id, 'Ошибка. Введите число')
#
#
# @logger.catch
# @bot.message_handler(state=UserInfoState.how_much_hotels)
# def how_much_hotels(message: Message) -> None:
#     """
#     Состояние пользователя по отправке количества отелей
#     :param message: сообщение
#     :return: None
#     """
#
#     logger.info(f'chat_id: {message.chat.id} message: {message.text}')
#
#     try:
#         if message.text.isdigit() and 10 >= int(message.text) >= 0:
#             with bot.retrieve_data(message.chat.id, message.chat.id) as data:
#                 data['how_much_hotels'] = int(message.text)
#
#             bot.set_state(message.chat.id, UserInfoState.retrieve_data, message.chat.id)
#             logger.info(f'Пользователь: {message.chat.id} окончил все состояния')
#             link_path.path(message)
#
#         elif int(message.text) < 0:
#             bot.send_message(message.chat.id, 'Ошибка. Число меньше 0')
#
#         elif int(message.text) > 10:
#             bot.send_message(message.chat.id, 'Ошибка. Число больше 10')
#
#     except ValueError:
#         bot.send_message(message.chat.id, 'Ошибка. Введите число')
#
#
# @logger.catch
# def match(text):
#     alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя ')
#
#     for letter in text.lower():
#         if letter not in alphabet:
#             return False
#     return True
