from django.urls import path

from . import views

app_name = 'vkfsys'
urlpatterns = [
    path('', views.index, name = 'index'),
]