from django.contrib import admin
from control.models import Login,Movies,Favorite,Like,Dislike
# Register your models here.
admin.site.register(Login)
admin.site.register(Movies)
admin.site.register(Favorite)
admin.site.register(Like)
admin.site.register(Dislike)