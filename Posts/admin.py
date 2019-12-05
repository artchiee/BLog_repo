from django.contrib import admin

from .models import (MyPosts, Comments, Category)

# Register your models here.

admin.site.register(
    MyPosts)
admin.site.register(Category)
admin.site.register(Comments)







