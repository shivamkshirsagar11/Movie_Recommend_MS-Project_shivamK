from django.db import models

class Login(models.Model):
    email = models.CharField(max_length=255,null=False)
    password = models.CharField(max_length=12,null=False)
    last_visit = models.DateTimeField()

class Movies(models.Model):
    name = models.CharField(max_length=255,default=None)
    director = models.CharField(max_length=255,default=None)
    writer = models.TextField(max_length=255,default=None)
    runtimes = models.TextField(max_length=25,default=None)
    year = models.CharField(max_length=4,default=None)
    actors = models.TextField(max_length=1028,default=None)
    category = models.TextField(max_length=1028,default=None)
    synopsis = models.TextField(max_length=11028,default=None)
    poster = models.ImageField(upload_to="movie_poster",default="movie_poster/default.jpg")

    def __str__(self):
        return self.name