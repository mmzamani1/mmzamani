from django.shortcuts import render
import requests
from datetime import datetime


base_url = "weather/"


def homePage(request):

    weather_url = "http://api.weatherapi.com/v1/current.json"
    forecast_url = "http://api.weatherapi.com/v1/forecast.json"
    
    apiKey = "fe21f1a61eb14e98a4c171708252701"
    latitude = 36.21
    longitude = 58.79
    nowTime = datetime.now().hour
    params = {
        'key': apiKey,
        'q': f'{latitude},{longitude}',
        'days': 4,
        'hour': nowTime,
    }
    
    weatherData = requests.get(url=weather_url, params=params).json()
    ForecastData = requests.get(url=forecast_url, params=params).json()
    
    return render(request, f"{base_url}/home.html", {
        'weatherData': weatherData,
        'forecastData': ForecastData,
    })