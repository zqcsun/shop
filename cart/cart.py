from decimal import Decimal
from django.conf import settings
from .models import Item

CART_SESSION_ID = getattr(settings, 'CART_SESSION_ID', 'cart')


class Cart:
    def __init__(self, request):
        """
        Ініціалізація кошика з об'єкта request.
        """
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        
        if not cart:
            # Зберігаємо порожній кошик у сесії
            cart = self.session[CART_SESSION_ID] = {}
            
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Додавання товару до кошика або оновлення його кількості.
        """
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Повідомляємо сесію про те, що вона була змінена, щоб зберегти дані.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Видалення товару з кошика.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебір елементів у кошику та отримання товарів з бази даних.
        """
        product_ids = self.cart.keys()
        products = Item.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # Безпечна перевірка на випадок, якщо товар видалено з БД
            if 'product' not in item:
                continue
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Підрахунок загальної кількості товарів у кошику.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Підрахунок загальної вартості всіх товарів у кошику.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Очищення кошика в сесії.
        """
        if CART_SESSION_ID in self.session:
            del self.session[CART_SESSION_ID]
            self.cart = {}
            self.save()