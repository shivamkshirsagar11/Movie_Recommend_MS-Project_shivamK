from django.contrib import admin
from control.models import Login,Movies,Favorite,Like,Dislike,Recommend,info
# Register your models here.
admin.site.register(Login)
admin.site.register(Movies)
admin.site.register(Favorite)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Recommend)
admin.site.register(info)