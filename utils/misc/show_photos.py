import requests
from utils.misc import request_to_api, api_params
import json
from telebot.types import InputMediaPhoto
from loguru import logger
from typing import List


@logger.catch
def return_photos(hotel_id, how_much_photos) -> List:
    """
    Данная функция возвращает список с ссылками на фотографии отеля
    :param hotel_id: id отеля
    :param how_much_photos: кол-во фотографий
    :return: List
    """

    urls = []
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    headers = api_params.return_headers()

    if request_to_api.make_request_to_api(url, querystring):

        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        suggestions = json.loads(response.text)

        for hotel_image in suggestions['hotelImages'][:how_much_photos]:
            urls.append(InputMediaPhoto(hotel_image["baseUrl"].replace('{size}', 'e')))
    return urls
