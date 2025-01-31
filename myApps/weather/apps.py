from django.apps import AppConfig


app_dir = 'myApps'

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = f'{app_dir}.weather'
