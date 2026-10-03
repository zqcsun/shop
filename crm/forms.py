from django import forms
from .models import Customer, Item, Order  # Виправлено: Item замість Items


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['items', 'quantity']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item  # Виправлено: Item замість Items
        fields = ['name', 'description', 'price', 'counts']