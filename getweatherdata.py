from weathermapkey import key
import json
import requests


class QueryError(Exception):
    pass


def get_weather_data(place, api_key=None):
    if place == '' or api_key is None:
        return # выходим из функции (возвращаем None), если не указан город или не указан API-ключ

    try:
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}')
        # получаем объект запроса

        res_data = res.json() # получаем JSON

        if res_data['cod'] != 200:
            raise QueryError(res_data['message'])
            # поднимаем исключение, если не получили информацию (должен быть код ответа 200)
            # например, не найден город, или указан неправильный API-ключ

        data = dict() # создаём пустой словарь
        # и заполняем его данными
        data['name'] = res_data['name']
        data['country'] = res_data['sys']['country']
        data['coord'] = res_data['coord']
        # timezone - в секундах от UTC, переводим в часы
        ts = res_data['timezone'] // 3600
        if ts > 0: # и делаем из этого строку UTC+(число) или UTC-(число)
            timezone_str = f'UTC+{ts}'
        else:
            timezone_str = f'UTC{ts}'
        data['timezone'] = timezone_str
        temp = res_data['main']['feels_like']
        temp_c = round(temp - 273.15, 2) # переводим температуру в градусы Цельсия
        data['feels_like'] = temp_c

        json_data = json.dumps(data) # преобразуем словaрь в JSON
        return json_data

    except QueryError as e:
        print('request failed:', e)

    except requests.exceptions.RequestException as e:
        print('request failed:', e)


if __name__ == "__main__":
    print(get_weather_data("Chicago", key))
    print(get_weather_data("Saint Petersburg", key))
    print(get_weather_data("Dhaka", key))
