from weathermapkey import key
import getweatherdata
import pytest


def test_without_key():
    assert getweatherdata.get_weather_data(
        "moscow") is None, \
        " Для получения данных необходимо задать значение для api_key "


def test_in_riga():
    assert getweatherdata.get_weather_data("Riga",
                                           api_key=key) is not None, \
        " Type of response is not none while using the key "


def test_type_of_res():
    assert type(getweatherdata.get_weather_data("Riga",
                                                api_key=key)) is str, \
        " Type of response is not none while using the key "


def test_args_error():
    assert getweatherdata.get_weather_data(
        '') is None, \
        " There should be one positional argument: 'city' and one keyword argument 'key_arg'"


def test_pos_arg_error():
    assert getweatherdata.get_weather_data('',
                                           api_key=key) is None, \
        " There should be one positional argument: 'city' "


def test_coords_dim():
    import json

    assert len(
        json.loads(getweatherdata.get_weather_data('Riga', api_key=key)).get('coord')) == 2, \
        " Dimension is 2: lon and lat "


def test_temp_type():
    import json

    assert type(json.loads(getweatherdata.get_weather_data('Riga', api_key=key)).get(
        'feels_like')) is float, \
        " Error with type of feels_like attribute "


inp_params_1 = "city, api_key, expected_country"
exp_params_countries = [("Chicago", key, 'US'), ("Saint Petersburg", key, 'RU'), ("Dakka", key, 'BD'),
                        ("Minsk", key, 'BY'), ("Kioto", key, 'JP'), ("Anchorage", key, 'US'), ("Havana", key, 'CU')]


@pytest.mark.parametrize(inp_params_1, exp_params_countries)
def test_countries(city, api_key, expected_country):
    import json

    assert json.loads(getweatherdata.get_weather_data(city, api_key=key)).get('country',
                                                                              'NoValue') == expected_country, \
        " Error with country code "


#
#
inp_params_2 = "city, api_key, expected_time"
exp_params_timezones = [("Chicago", key, 'UTC-5'), ("Saint Petersburg", key, 'UTC+3'), ("Dakka", key, 'UTC+6'),
                        ("Minsk", key, 'UTC+3'), ("Kioto", key, 'UTC+9'),
                        ("Anchorage", key, 'UTC-8'), ("Havana", key, 'UTC-4')]


@pytest.mark.parametrize(inp_params_2, exp_params_timezones)
def test_utc_time(city, api_key, expected_time):
    import json
    assert json.loads(getweatherdata.get_weather_data(city, api_key=key)).get('timezone',
                                                                              'NoValue') == expected_time, \
        " Error with timezone "


inp_params_3 = 'field'
exp_fields = ['name', 'country', 'coord', 'timezone', 'feels_like']

@pytest.mark.parametrize(inp_params_3, exp_fields)
def test_data_fields(field):
    import json

    assert json.loads(getweatherdata.get_weather_data('Dakka', api_key=key)).get(field) is not None, \
        'Отсутствует значение в JSON'


inp_params_4 = 'city'
cities = ['Chicago', 'Saint Petersburg', 'Dhaka']

@pytest.mark.parametrize(inp_params_4, cities)
def test_data_fields(city):
    import json

    assert json.loads(getweatherdata.get_weather_data(city, api_key=key)).get('feels_like') < 150, \
        'Значение температуры должно возаращаться в градусах Цельсия'


inp_params_5 = 'city, coord'
exp_fields = [('Chicago', {'lon': -87.65, 'lat': 41.85}),
              ('Saint Petersburg', {'lon': 30.2642, 'lat': 59.8944}),
              ('Dhaka', {'lon': 90.4074, 'lat': 23.7104})]

@pytest.mark.parametrize(inp_params_5, exp_fields)
def test_data_fields(city, coord):
    import json

    assert json.loads(getweatherdata.get_weather_data(city, api_key=key)).get('coord') == coord, \
        'Значение температуры должно возаращаться в градусах Цельсия'
