from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:car_id>/', views.CarDetailView.as_view(), name='post_cars'),
    path('details/', views.DetailListView.as_view(), name='detail_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/<int:id>/', views.PostDetailView.as_view(), name='post_detail'),
]