from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):  # Рекомендовано додавати суфікс Form до назви
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'image', 'price']