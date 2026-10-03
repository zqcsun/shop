from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created', 'id']
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return self.title


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1886),
            MaxValueValidator(2030)  # Обмежено реалістичною датою
        ]
    )
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='car')
    
    class Meta:
        ordering = ['-year', 'id']

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class Detail(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='details')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.key}: {self.value}"