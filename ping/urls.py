from django.urls import path
from .views import home, ping

urlpatterns = [
    path('', home, name='home'),
    path('ping/', ping, name='ping'),
]
