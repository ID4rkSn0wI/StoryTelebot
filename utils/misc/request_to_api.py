import requests
from requests import Response, Timeout
from loguru import logger


@logger.catch
def make_get_to_api(url: str, request_headers: dict) -> False:
    """
    Данная функция делает request в API и проверяет, чтобы всё было исправно
    :param url: ссылка для поиска
    :param request_headers: headers
    :return: False
    """

    try:
        response: Response = requests.get(url, headers=request_headers, verify=False, timeout=30)

        if response.status_code == requests.codes.ok:
            return True

        else:
            return False

    except ConnectionError:
        logger.warning('Сервис не работает')
        return False

    except Timeout:
        logger.warning('Ошибка TimeOut')
        return False


@logger.catch
def make_post_to_api(url: str, request_headers: dict, data: str) -> False:
    """
    Данная функция делает request в API и проверяет, чтобы всё было исправно
    :param url: ссылка для поиска
    :param request_headers: headers
    :param data: data
    :return: False
    """

    try:
        response: Response = requests.post(url, headers=request_headers, data=data, verify=False, timeout=30)

        if response.status_code == requests.codes.ok:
            return True

        else:
            return False

    except ConnectionError:
        logger.warning('Сервис не работает')
        return False

    except Timeout:
        logger.warning('Ошибка TimeOut')
        return False
