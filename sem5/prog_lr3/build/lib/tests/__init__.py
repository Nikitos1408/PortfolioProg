from myweather import get_weather_data
from myweather.weathermapkey import api_key
import pytest
import json

def test_without_key():
    assert get_weather_data("moscow", "") is None, \
        "Для получения данных необходимо задать значение для api_key"

def test_in_riga():
    assert get_weather_data("Riga", api_key) is not None, \
        "Type of response is not none while using the key"

def test_type_of_res():
    assert type(get_weather_data("Riga", api_key)) is str, \
        "Type of response is not none while using the key"

def test_args_error():
    assert get_weather_data('', api_key) is None, \
        "There should be one positional argument: 'city' and one keyword argument 'key_arg'"

def test_pos_arg_error():
    assert get_weather_data('', api_key) is None, \
        "There should be one positional argument: 'city'"

def test_coords_dim():
    assert len(json.loads(get_weather_data('Riga', api_key)).get('coord')) == 2, \
        "Dimension is 2: lon and lat"

def test_temp_type():
    assert type(json.loads(get_weather_data('Riga', api_key)).get('feels_like')) is float, \
        "Error with type of feels_like attribute"