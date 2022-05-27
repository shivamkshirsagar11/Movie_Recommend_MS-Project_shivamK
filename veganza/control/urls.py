from . import views
from django.urls import path

urlpatterns = [
    path('', views.index,name='Lost_Home'),
    path('addto', views.addto,name='addto'),
    path('like', views.like,name='like'),
    path('dislike', views.dislike,name='dislike'),
    path('watch', views.watch,name='watch'),
    path('reset', views.reset,name='reset'),
    path('movie', views.movie,name='movie'),
    path('recommend', views.recommend,name='recommend'),
    path('process-movie', views.process,name='process-movie'),
]