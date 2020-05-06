from django.urls import path

from . import views

app_name = 'encoder'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('choiceFileFor', views.choiceFileFor, name = 'choiceFileFor'),
    path('add_fileFOR', views.add_fileFOR, name = 'add_fileFOR'),
    path('list_filesFor', views.list_filesFor, name = 'list_filesFor'),
    path('fileFrom/<int:fileForEncoder_id>', views.fileFrom, name = 'fileFrom'),
    path('fileFrom/<int:fileForEncoder_id>/fill_names', views.fill_names, name = 'fill_names'),
    path('fileFrom/<int:fileForEncoder_id>/execute', views.execute, name = 'execute'),
]