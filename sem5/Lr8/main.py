import json
import requests
import matplotlib.dates as md
import matplotlib.pyplot as plt
import pandas as pd

api_key = '' #Вставьте сюда свой API с openweathermap :)

def getweather(api_key=None):

    city, lat, lon = 'Saint Petersburg, RU', 59.57, 30.19
    result = {"city": city, "temps": []}

    try:
        res = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast',
            params={
                'lat': lat,
                'lon': lon,
                'appid': api_key,
                'lang': 'ru',
                'units': 'metric'
            }
        )
        res.raise_for_status()
        data = res.json()

        for entry in data.get('list', []):
            result['temps'].append({
                'dt': entry['dt'],
                'temp': entry['main']['temp']
            })

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return json.dumps({'error': 'Request failed. Check API key or parameters.'})
    except KeyError as e:
        print(f"Unexpected response structure: {e}")
        return json.dumps({'error': 'Unexpected data structure.'})

    return json.dumps(result)

weather_data = getweather(api_key)

def visualise_data(json_data):
    data = json.loads(json_data)

    if 'error' in data:
        print(f"Error in weather data: {data['error']}")
        return

    city_name = data['city']
    temps_data = pd.DataFrame(data['temps'])

    if temps_data.empty:
        print("No temperature data available.")
        return

    temps_data['dt'] = pd.to_datetime(temps_data['dt'], unit='s')
    dates = temps_data['dt']
    temps = temps_data['temp']

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [3, 1]})

    # Граф1
    ax1 = axes[0]
    xfmt = md.DateFormatter('%d-%m')
    ax1.xaxis.set_major_formatter(xfmt)
    ax1.plot(dates, temps, marker='o', label="Интервал - 3ч ", alpha=0.7)
    ax1.set_title(f"{city_name}")
    ax1.set_xlabel("Дата")
    ax1.set_ylabel("Температура (°C)")
    ax1.legend()
    ax1.grid()
    ax1.tick_params(axis='x', rotation=45)

    # Граф2
    ax2 = axes[1]
    ax2.boxplot(temps, vert=True, patch_artist=True, boxprops=dict(facecolor='skyblue'))
    ax2.set_title("Распределение температуры")
    ax2.set_ylabel("Температура (°C)")

    plt.tight_layout()
    plt.show()

visualise_data(weather_data)