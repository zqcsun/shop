from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [  # Виправлено: urlpatterns замість urlspatterns
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),  # Виправлено: UserRegisterView
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.CustomerListView.as_view(), name='home'),
]