from django.db import models
from users.models import Profile  

class Category(models.Model):
    rating = models.IntegerField(default=0, null=True)

    def __str__(self):
        return str(self.rating)


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(null=True, blank=True, upload_to='books/')  
    title = models.CharField(max_length=255)
    pages = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True, default='-')
    genre = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return f'{self.title} - {self.pages} pages'