import requests
from requests import Response, Timeout
from utils.misc import api_params
import re
import json
from loguru import logger


@logger.catch
def make_request_to_api(url: str, querystring: dict, pattern='') -> False:
    """
    Данная функция делает request в API и проверяет, чтобы всё было исправно
    :param url: ссылка для поиска
    :param querystring: параметры для поиска
    :param pattern: паттерн для поиска
    :return: False
    """

    try:
        headers = api_params.return_headers()
        response: Response = requests.get(url, headers=headers, params=querystring, timeout=30)

        if pattern != '':
            find = re.search(pattern, response.text)

            if find and response.status_code == requests.codes.ok:
                suggestions = json.loads(f"{{{find[0]}}}")

                if suggestions:
                    return True

                else:
                    return False

            else:
                return False

        elif response.status_code == requests.codes.ok:
            return True

        else:
            return False

    except ConnectionError:
        logger.warning('Сервис не работает')
        return False

    except Timeout:
        logger.warning('Ошибка TimeOut')
        return False
