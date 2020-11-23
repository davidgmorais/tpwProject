from django.contrib import admin
from app.models import Category, Item, Comment, Profile, Sell, Purchase


# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Sell)
admin.site.register(Purchase)


# admin.site.register(Profile)


