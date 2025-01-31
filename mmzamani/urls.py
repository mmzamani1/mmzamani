from django.contrib import admin
from django.urls import path, include

app_dir = 'myApps'

urlpatterns = [
    path('', include(f'{app_dir}.mainApp.urls')),
    path('auction/', include(f'{app_dir}.auction.urls')),
    path('weather/', include(f'{app_dir}.weather.urls')),
    path('store/', include(f'{app_dir}.store.urls')),
    path('admin/', admin.site.urls),
]
