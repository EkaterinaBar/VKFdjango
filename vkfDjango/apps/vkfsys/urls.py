from django.urls import path

from . import views

app_name = 'vkfsys'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('induction', views.induction, name = 'induction'),
    path('induction/create_table', views.create_table, name = 'create_table'),
    path('induction/create_table/show_table/<int:ex_id>', views.show_table, name = 'show_table'),
    path('induction/create_table/ct_return/<int:ex_id>', views.ct_return, name = 'ct_return'),
    path('induction/create_table/for_add_hyps/<int:ex_id>', views.for_add_hyps, name = 'for_add_hyps'),
    path('induction/create_table/add_hyps/<int:ex_id>', views.add_hyps, name = 'add_hyps'),
    path('induction/create_table/choice_test/<int:ex_id>', views.choice_test, name = 'choice_test'),
    path('prediction/<int:ex_id>', views.prediction, name = 'prediction'),
    path('list_exs', views.list_exs, name = 'list_exs'),
    
]