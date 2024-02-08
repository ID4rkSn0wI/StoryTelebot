from config_data import config


def return_headers():
    """
    Данная функция хранит в себе headers для request, чтобы все было сохранно
    """

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.API_KEY
    }
    return headers
