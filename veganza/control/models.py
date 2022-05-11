from django.db import models

class Login(models.Model):
    email = models.CharField(max_length=255,null=False)
    password = models.CharField(max_length=12,null=False)
    last_visit = models.DateTimeField()

class Movies(models.Model):
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    actors = models.TextField(max_length=1028)
    category = models.TextField(max_length=1028)
    synopsis = models.TextField(max_length=11028)
    poster = models.ImageField(upload_to="movie_poster",default="movie_poster/default.jpg")