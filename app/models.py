from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField()
    email = models.EmailField()
    password = models.CharField(max_length=15)
    money = models.ImageField()

    def __str__(self):
        return self.first_name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    price = models.FloatField()
    brand = models.CharField(max_length=30)
    quantity = models.IntegerField()
    insertDate = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)
    discount = models.FloatField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    stars = models.IntegerField()

    def __str__(self):
        return self.item


class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    discountedP = models.BooleanField()

    def __str__(self):
        return self.item


class Sell(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moneyReceived = models.FloatField()
    pendingSell = models.BooleanField()

    def __str__(self):
        return self.item
