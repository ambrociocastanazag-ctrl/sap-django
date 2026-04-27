from django.urls import path
from django.contrib.auth import views as auth_views
from webapp import views

urlpatterns = [
    path('', views.bienvenido, name='bienvenido'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]