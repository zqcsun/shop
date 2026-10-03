from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

from .models import Post, Car, Detail
from .forms import CreatePostForm  # Оновлено відповідно до форм


class PostListView(ListView):
    model = Post
    template_name = 'posts/postlist.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(active=True)
        car_id = self.kwargs.get('car_id') or self.kwargs.get('cars_id')
        if car_id:
            posts = posts.filter(car_id=car_id)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/postdetail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'  # Явно вказуємо назву параметра id з urls.py


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/postcreate.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('post_list')  # Виправлено назву url

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.active = True
        post.save()
        return super().form_valid(form)


class CarListView(ListView):
    model = Car
    template_name = 'posts/carlist.html'
    context_object_name = 'cars'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = Detail.objects.all()
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = 'posts/cardetail.html'
    context_object_name = 'car'
    pk_url_kwarg = 'car_id'  # Додано для збігу з urls.py


class CarCreateView(CreateView):
    model = Car
    template_name = 'posts/carcreate.html'
    fields = ['make', 'model', 'year', 'post']  # Якщо немає окремої форми
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        car = form.save(commit=False)
        car.driver = self.request.user  # Виправлено: driver замість author
        car.save()
        return super().form_valid(form)


class DetailListView(ListView):
    model = Detail
    template_name = 'posts/detlist.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.all()
        return context