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
    path('fileFrom/<int:fileForEncoder_id>/show_table/<str:table_name>/<str:table_type>', views.show_table, name = 'show_table'),
    path('fileFrom/<int:fileForEncoder_id>/create_file/<str:file_type>', views.create_file, name = 'create_file'),
    path('create_table', views.create_table, name = 'create_table'),
    path('create_table/add_sample', views.add_sample, name = 'add_sample'),
    path('create_table/list_samples', views.list_samples, name = 'list_samples'),
    path('<int:fileForEncoder_id>/show_table/<str:table_name>/<str:table_type>', views.show_table, name = 'show_table'),
]