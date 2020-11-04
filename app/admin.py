from django.contrib import admin
from app.models import Category, SubCategory, Item, Comment, User, Sell, Purchase

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Sell)
admin.site.register(Purchase)