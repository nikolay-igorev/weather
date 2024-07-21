import requests
from django.shortcuts import render
import openmeteo_requests

import requests_cache
import pandas as pd
from django.template.context_processors import csrf
from django.views.generic import FormView
from retry_requests import retry
from geopy.geocoders import Nominatim

from weather.forms import WeatherForm
from api.models import WeatherRequest
from geopy.geocoders import Nominatim


def get_weather(city):
    """
    Метод получения погоды из OpenMeteo
    :param city: название города
    :return: температура и вероятность осадков
    """
    url = "https://api.open-meteo.com/v1/forecast"

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(city)
    lat = location.raw['lat']
    lon = location.raw['lon']
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "precipitation"]
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ), "temperature_2m": hourly_temperature_2m, "precipitation": hourly_precipitation}
    hourly_dataframe = pd.DataFrame(data=hourly_data)

    temperature = round(hourly_dataframe["temperature_2m"].iloc[0], 1)
    precipitation = hourly_dataframe["precipitation"].iloc[0] * 10

    return temperature, precipitation


def index(request):
    """View получения погода"""
    city = ''
    context = {}
    form = ''
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        city = form.data['city']
        context['form'] = form
    else:
        form = WeatherForm()
        context['form'] = form

    if city:
        context['city'] = city

        try:
            context['temperature'], context['precipitation'] = get_weather(city)
            WeatherRequest.objects.create(city=city)

        except AttributeError:
            context['error'] = f'"{city}" is wrong city name'

    return render(request, 'home.html', context)
