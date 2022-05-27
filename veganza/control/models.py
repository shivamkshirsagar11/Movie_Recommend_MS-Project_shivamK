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
    poster = models.ImageField(upload_to="movie_poster",default="movie_poster/default.jpg",null=True,blank=True)
    watch = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    backposter = models.URLField(default='N/A',null=True,blank=True)
    wikilink = models.URLField(default='N/A',null=True,blank=True)
    rating = models.CharField(default=0,max_length=15)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    name = models.CharField(max_length=255,default=None)
    mid = models.IntegerField(default=None)

    def __str__(self): return self.name

class Like(models.Model):
    name = models.CharField(max_length=255,default=None)
    mid = models.IntegerField(default=None)

    def __str__(self): return self.name

class Dislike(models.Model):
    name = models.CharField(max_length=255,default=None)
    mid = models.IntegerField(default=None)

    def __str__(self): return self.name
class Recommend(models.Model):
    mid = models.IntegerField(default=None)

    def __str__(self): return 'Movie Id: '+str(self.mid)