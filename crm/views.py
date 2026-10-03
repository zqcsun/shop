from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

from .models import Customer, Item, Order, OrderProduct
from .forms import CustomerForm, OrderForm, ItemForm
from .cart import Cart  # Переконайтеся, що файл cart.py знаходиться в цій ж папці


class UserLoginView(LoginView):  # Виправлено: UserLoginView замість UserLoginViews
    template_name = 'crm/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class UserRegisterView(CreateView):
    template_name = 'crm/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class CustomerListView(ListView):
    model = Customer
    template_name = 'crm/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'crm/customer_detail.html'
    context_object_name = 'customer'


class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'crm/customer_create.html'
    form_class = CustomerForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Прив'язуємо користувача через форму
        return super().form_valid(form)


class OrderDetailView(DetailView):  # Перейменовано з OrderViews для ясності
    model = Order
    template_name = 'crm/order_detail.html'  # Вказано назву шаблону
    context_object_name = 'order'


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':  # Виправлено: 'POST' у верхньому регістрі
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)  # Виправлено: commit=False замість context=False
            order.save()
            
            for item in cart:
                OrderProduct.objects.create(  # Виправлено: OrderProduct та метод create
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],  # Виправлено: quantity
                    price=item['price']         # Виправлено: price
                )
                
            cart.clear()
            
            if order.paid == 'delivery':  # Виправлено: delivery
                return redirect('order_done')
            else:
                request.session['order_id'] = order.id  # Виправлено: session
                return redirect(reverse('process'))
    else:
        form = OrderForm()

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'crm/order_create.html', context)  # Додано шлях до шаблону


def order_done(request):
    return render(request, 'crm/order_done.html')  # Додано шлях до шаблону