# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from loader import bot
# from utils.misc import link_path
#
#
# def city_markup(cities) -> InlineKeyboardMarkup():
#     """
#     Данная функция создает клавиатуру с местами поиска отелей, чтобы пользователь уточнил нужное место
#     :param cities: места для уточнения
#     :return: InlineKeyboardMarkup()
#     """
#
#     destinations = InlineKeyboardMarkup()
#
#     for city in cities:
#         destinations.add(InlineKeyboardButton(text=city['city_name'], callback_data=f'{city["destination_id"]}'))
#
#     return destinations
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call) -> None:
#     """
#     Данная функция-обработчик выбора в клавиатуре
#     :param call: сообщение в клавиатуре
#     :return: None
#     """
#
#     if call.message and call.data:
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Записал',
#                               reply_markup=None)
#         with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
#             data['destination_id'] = call.data
#         link_path.path(call.message)
