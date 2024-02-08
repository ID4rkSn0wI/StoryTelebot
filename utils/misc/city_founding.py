import requests
import json
import re
from utils.misc import api_params
from typing import List


def city_found(city) -> List:
    """
    Данная функция уточняет место поиска отелей
    url - ссылка для поиска
    querystring - параметры для поиска
    headers - токен и ссылка сайта для поисков
    :param city: место для поиска
    :return: List
    """

    headers = api_params.return_headers()
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    response = requests.get(url, headers=headers, params=querystring, timeout=10)
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)

    if find and response.status_code == requests.codes.ok:
        suggestions = json.loads(f"{{{find[0]}}}")
    else:
        suggestions = {}

    cities = list()

    for dest_id in suggestions['entities']:
        clear_destination = re.sub(r"<.{5,24}>", '', dest_id['caption'])
        cities.append({'city_name': clear_destination, 'destination_id': dest_id['destinationId']})
    return cities
