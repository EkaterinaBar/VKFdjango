from django.urls import path

from . import views

app_name = 'encoder'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('choiceFileFor', views.choiceFileFor, name = 'choiceFileFor'),
    path('add_fileFOR', views.add_fileFOR, name = 'add_fileFOR'),
]