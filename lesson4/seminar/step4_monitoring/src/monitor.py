# Импортируем библиотеки для мониторинга
import requests  # для отправки запросов
import time  # Для замера задержки
import os  # для определения файла изображения

def monitor_health(api_url):
    '''
    GET-запрос для оценки состояния.

    Параметры:
    - api_url (str): ссылка на API-сервис
    '''
    # Начальное время
    start = time.time()
    try:
        response = requests.get(f'{api_url}/health')
        # Проверяем, прошёл ли запрос и какая была задержка
        latency = time.time() - start
        status = response.status_code

        # Выводим данные, если всё ок
        data = response.json() if response.ok else response.text
        return {
            "endpoint": "/health",
            "status_code": status,
            "latency": latency,
            "response": data,
            "error": None
        }
    except Exception as e:
        print(f'Ошибка запроса: {e}')


def get_mime_type(filename):
    '''
    Определяет файловое расширение изображения.

    '''
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        return "image/jpeg"
    elif ext == ".png":
        return "image/png"
    # Можно добавить другие типы по необходимости
    return "application/octet-stream"

def monitor_predict(api_url, img_path):
    '''
    Делает post-запрос к сервису.
    
    '''
    start = time.time()
    try:
        # Открываем файл 
        with open(img_path, 'rb') as f:
            files = {'file': (img_path, f, 'image/jpeg')}
            response = requests.post(f'{api_url}/predict', files=files)

        # Измеряем задержку
        latency = time.time() - start
        status = response.status_code

        # Возвращаем результат
        data = response.json() if response.ok else response.text
        return {
            "endpoint": "/predict",
            "status_code": status,
            "latency": latency,
            "response": data,
            "error": None
        }
    except Exception as e:
        latency = time.time() - start
        return {
            "endpoint": "/predict",
            "status_code": None,
            "latency": latency,
            "response": None,
            "error": str(e)
        }

def get_alert_level(value, warning, critical):
    if value is None:
        return "grey"
    elif value >= critical:
        return "red"
    elif value >= warning:
        return "yellow"
    else:
        return "green"