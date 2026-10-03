from django.db import models
from posts.models import Detail  # Виправлено: видалено імпорт Car з цього ж файлу


class Car(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    
    # Встановлюємо ForeignKey на модель Detail з додатку posts
    detail_for = models.ForeignKey(
        Detail, 
        on_delete=models.CASCADE, 
        related_name='cars'
    )
    
    available = models.BooleanField(default=True)  # Виправлено одрук (avalible -> available)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Автомобіль'
        verbose_name_plural = 'Автомобілі'

    def __str__(self):
        return self.name