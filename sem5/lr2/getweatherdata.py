from owm_key import key
import json
import requests

# Это исключение будет использоваться для обозначения ошибок при запросе данных.
class QueryError(Exception):
    pass

# Функция для получения данных о погоде по названию города.
def get_weather_data(place, api_key=None):
    # Проверяем, что название города и ключ API не пустые.
    # Если одно из условий не выполнено, функция вернёт None (пустое значение).
    if place == '' or api_key is None:
        return

    try: # Начинаем блок try-except для обработки возможных ошибок.
        # Выполняем GET-запрос к API OpenWeatherMap
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}')
        # Преобразуем ответ от API в формат JSON
        res_data = res.json()

        # Проверяем код ответа API. Если код не равен 200 (успешный запрос),
        # то вызываем исключение QueryError с сообщением об ошибке из ответа API
        if res_data['cod'] != 200:
            raise QueryError(res_data['message'])

        # Создаем пустой словарь
        data = dict()
        # Извлекаем данные и сохраняем в словарь
        data['name'] = res_data['name']
        data['country'] = res_data['sys']['country']
        data['coord'] = res_data['coord']

        # Извлекаем смещение часового пояса в секундах и преобразуем его в часы.
        ts = res_data['timezone'] // 3600
        # Формируем строку с часовым поясом в формате UTC
        if ts > 0:
            timezone_str = f'UTC+{ts}'
        else:
            timezone_str = f'UTC{ts}'
        # Сохраняем строку
        data['timezone'] = timezone_str
        # Извлекаем температуру
        temp = res_data['main']['feels_like']
        #Кельвины в Цельсия
        temp_c = round(temp - 273.15, 2)
        # Сохраняем температуру
        data['feels_like'] = temp_c

        # Преобразуем словарь data в строку JSON.
        json_data = json.dumps(data)
        return json_data

    # Обрабатываем исключение QueryError, которое было вызвано, если API вернул ошибку
    except QueryError as e:
        print('request failed:', e)

    # Обрабатываем исключение requests.exceptions.RequestException, которое возникает при проблемах с сетевым запросом
    except requests.exceptions.RequestException as e:
        print('request failed:', e)

if __name__ == "__main__":
    # Вызываем функцию get_weather_data для нескольких городов и выводим результаты в консоль.
    print(get_weather_data("Chicago", api_key=key))
    print(get_weather_data("Saint Petersburg", api_key=key))
    print(get_weather_data("Dakka", api_key=key))
