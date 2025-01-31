from django.apps import AppConfig


app_dir = 'myApps'

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = f'{app_dir}.store'
