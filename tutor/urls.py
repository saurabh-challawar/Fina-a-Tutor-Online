from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutors, name='all'),
    path('<int:pk>/detail/', views.details, name='detail'),
    path('favourites/', views.favourites, name='favourites'),
    path('register_client/', views.registerClientPage, name='register_client'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('update_favourites/', views.updateFavs, name='update_favourites')
]