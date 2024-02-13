import json

import requests
import uuid


def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
    Выполняет POST-запрос к эндпоинту, который выдает токен.

    :param auth_token:
    :param scope:
    :return:
    """

    rq_uid = str(uuid.uuid4())

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    payload = {
        'scope': scope
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)

    if response.status_code == requests.codes.ok:
        return response.json()['access_token']
    else:
        return None


def get_chat_completion(auth_token, user_message, conversation_history=None):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat в рамках диалога.

    :param auth_token:
    :param user_message:
    :param conversation_history:
    :return:
    """

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    payload = json.dumps({
        "model": "GigaChat:latest",
        "messages": conversation_history,
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token(auth_token)}'
    }

    # if make_post_to_api(url, headers, payload):
    response = requests.post(url, headers=headers, data=payload, verify=False)

    if response.status_code == requests.codes.ok:
        response_data = response.json()

        conversation_history.append({
            "role": "assistant",
            "content": response_data['choices'][0]['message']['content']
        })

        return response_data['choices'][0]['message']['content'], conversation_history
    else:
        return None, conversation_history


def send_chat_request(auth_token, user_message):
    """
    Отправляет POST-запрос к API GigaChat для получения ответа от модели чата.

    Параметры:
    - giga_token (str): Токен авторизации для доступа к API GigaChat.
    - user_message (str): Сообщение пользователя, которое будет обработано моделью GigaChat.

    Возвращает:
    - str: Строка сгенерированного ответа GigaChat с тэгом img
    """

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_token(auth_token)}',
    }

    payload = json.dumps({
        "model": "GigaChat:latest",
        "messages": [
            {
                "role": "user",
                "content": 'Нарисуй ' + user_message
            },
        ],
        "temperature": 0.7
    })

    response = requests.post(url, headers=headers, data=payload, verify=False)
    if response.status_code == requests.codes.ok:
        image = response.json()["choices"][0]["message"]["content"]
        load_image(image, auth_token)
    else:
        return None


def load_image(response_img_tag, auth_token):
    """
    Парсит изображение.

    :param auth_token:
    :param response_img_tag:
    :param giga_token:
    :return:
    """

    img_src = response_img_tag.split('"')[1]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_token(auth_token)}',
    }

    url = f'https://gigachat.devices.sberbank.ru/api/v1/files/{img_src}/content'

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == requests.codes.ok:
        with open('temp_image.jpg', 'wb') as file:
            file.write(response.content)
