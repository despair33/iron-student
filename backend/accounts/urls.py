from django.urls import path
from . import views
from .views import students

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),
    path('students/', students, name='students'),
]
