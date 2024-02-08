import requests
from utils.misc import request_to_api, show_photos, api_params
import re
from loader import bot
import json
from datetime import datetime
from database.database import User, db
from telebot.types import Message
from loguru import logger


@logger.catch
def send_hotel(message: Message) -> None:
    """
    Данная функция выводит отели
    :param message: сообщение
    :return: None
    """

    hotel_names = []
    url = "https://hotels4.p.rapidapi.com/properties/list"

    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        destination_id = data['destination_id']
        check_in = datetime.strptime(str(data['check_in']), '%Y-%m-%d').date()
        check_out = datetime.strptime(str(data['check_out']), '%Y-%m-%d').date()
        show_photo = data['show_photos']
        how_much_hotels = data['how_much_hotels']
        how_much_photos = data.get('how_much_photos', 0)
        querystring = {"destinationId": destination_id, "pageNumber": "1", "pageSize": "25",
                       "checkIn": check_in,
                       "checkOut": check_out, "adults1": "1", "priceMin": data['min_price'],
                       "priceMax": data['max_price'],
                       "sortOrder": data['sort'], "locale": "ru_RU", "currency": "RUB"}
        need_distance_to_center = data.get('distance_to_center', False)

    headers = api_params.return_headers()
    pattern = '(?<=,)"results":.+(?=,"pagination")'
    bot.send_message(message.chat.id, 'Подождите. Идет поиск отелей')

    if request_to_api.make_request_to_api(url, querystring):
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        find = re.search(pattern, response.text)

        if find:
            suggestions = json.loads(f"{{{find[0]}}}")
            days = check_out - check_in
            days = days.days

            for hotel in suggestions['results'][:how_much_hotels]:
                price = hotel['ratePlan']['price']['current']
                exact_price = hotel['ratePlan']['price']['exactCurrent']
                distance_to_center = '0 км'
                hotel_id = hotel['id']

                for landmark in hotel['landmarks']:
                    if landmark['label'] == 'Центр города':
                        distance_to_center = float(landmark['distance'][:-3].replace(',', '.'))
                    break

                full_price = int(exact_price * days)
                hotel_url = 'https://www.hotels.com/ho' + str(hotel_id)
                street_address = hotel['address'].get('streetAddress', False)
                if not street_address:
                    street_address = hotel['name']
                hotel_name = hotel['name']

                if show_photo:
                    photo_urls = show_photos.return_photos(hotel['id'], how_much_photos)
                    if photo_urls is not None or photo_urls != []:
                        bot.send_media_group(message.chat.id, photo_urls)
                    else:
                        bot.send_message(message.chat.id, 'У данного места нет фотографий')

                if need_distance_to_center:
                    if need_distance_to_center >= distance_to_center:
                        bot.send_message(message.chat.id,
                                         f"Название: {hotel_name}"
                                         f"\nАдрес: {street_address}"
                                         f"\nРасстояние до центра: {distance_to_center} км"
                                         f"\nЦена за ночь: {price}"
                                         f"\nЦена за время отдыха: {full_price} RUB"
                                         f"\nСсылка на отель: {hotel_url}"
                                         )
                        hotel_names.append(hotel['name'])

                    else:
                        bot.send_message(message.chat.id,
                                         f"У отеля {hotel_name}"
                                         f"\nПо адресу: {street_address}"
                                         f"\nРасстояние до центра больше, чем вы написали: {distance_to_center} км"
                                         f"\nЦена за ночь: {price}"
                                         f"\nЦена за время отдыха: {full_price} RUB"
                                         f"\nСсылка на отель: {hotel_url}"
                                         )
                else:
                    bot.send_message(message.chat.id,
                                     f"Название: {hotel_name}"
                                     f"\nАдрес: {street_address}"
                                     f"\nРасстояние до центра: {distance_to_center} км"
                                     f"\nЦена за ночь: {price}"
                                     f"\nЦена за время отдыха: {full_price} RUB"
                                     f"\nСсылка на отель: {hotel_url}"
                                     )
                    hotel_names.append(hotel['name'])
        else:
            bot.send_message(message.from_user.id, 'Ничего не найдено. Вы ввели не валидные данные для данного места '
                                                   '(цена или недоступность данного места)')
    else:
        bot.send_message(message.from_user.id, 'Ошибка. Длительность запроса превысила 15 секунд')

    with db:
        user = User.get(telegram_id=message.chat.id)
        date = datetime.today().date()
        time = datetime.today().time().replace(microsecond=0)
        total_time = datetime.combine(date, time)
        user.history.append([user.call_hotels, total_time, hotel_names])
        user.call_hotels = ''
        user.save()
        bot.delete_state(message.chat.id, message.chat.id)
