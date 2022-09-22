import requests


def get_meteo(ville: str):
    """
    Description:
    :param ville:
    :return:
    """
    url_forecast = "http://api.openweathermap.org/data/2.5/forecast?q=" + ville + "&APPID=beb97c1ce62559bba4e81e28de8be095"
    r_forecast = requests.get(url_forecast)
    data = r_forecast.json()
    # Météo
    meteo = data["list"][1]
    t = meteo['main']['temp']
    humidity = meteo['main']['humidity']
    temps = meteo['weather'][0]['description']
    res = "{} :\n" \
          "La température moyenne est de {} degrés Celsius\n" \
          "Taux d'humidité {}%\n" \
          "Conditions climatiques {}\n\n".format(ville.strip(), round(t - 273.15), humidity, temps)
    return res
