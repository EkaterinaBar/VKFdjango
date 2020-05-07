from django.urls import path

from . import views

app_name = 'vkfsys'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('induction', views.induction, name = 'induction'),
    path('induction/create_table', views.create_table, name = 'create_table'),
]