from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    counts = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    def is_available(self):
        return self.counts > 0

    def total_price(self, quantity):
        return self.price * Decimal(quantity)


class Order(models.Model):
    POST_USE = [
        ('UK', 'UkrPost'),
        ('NW', 'NewPost'),
    ]
    PAID_USE = [
        ('card', 'Card'),
        ('delivery', 'Delivery'),
    ]

    discount = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    post = models.CharField(max_length=2, choices=POST_USE, default='NW')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.CharField(max_length=10, choices=PAID_USE, default='card')
    payable = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order #{self.id}'

    def get_total_cost_discount(self):
        # Змінено з self.product.all() на self.items.all() для зрозумілості
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_discount()
        discount_percent = Decimal(self.discount or 0)
        return total_cost * (discount_percent / Decimal(100))

    def get_total_cost(self):
        return self.get_total_cost_discount() - self.get_discount()


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderProduct #{self.pk}"

    def get_cost(self):
        return self.price * Decimal(self.quantity)