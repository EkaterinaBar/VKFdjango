from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('update_ex/<int:ex_id>/', views.update_ex, name="update_ex"),
    path('delete_ex/<int:ex_id>/', views.delete_ex, name="delete_ex"),
] 