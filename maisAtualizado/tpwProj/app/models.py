from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    money = models.FloatField(blank=True, null=True, default=None)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    specifications = models.CharField(max_length=10000, null=True)
    price = models.FloatField()
    brand = models.CharField(max_length=30)
    quantity = models.IntegerField()
    insertDate = models.DateField()
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    discount = models.FloatField()
    picture = models.ImageField(upload_to='images/', blank=True, null=True)
    sellMoney = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def items(self):
        return self.orderitem_set.all()

    def total(self):
        total = 0
        for i in self.orderitem_set.all():
            total += i.get_final_price()
        return total


class OrderItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} x {self.qty}"

    def get_total_item_price(self):
        return self.qty * self.item.price

    def get_total_discount_item_price(self):
        return self.qty * (self.item.price * (1 - self.item.discount / 100))

    def get_final_price(self):
        if self.item.discount != 0:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    stars = models.IntegerField()

    def __str__(self):
        return self.item.name


class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    discountedP = models.BooleanField()

    def __str__(self):
        return self.item.name


class Sell(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moneyReceived = models.FloatField(null=True)
    pendingSell = models.BooleanField()
    accepted = models.BooleanField()

    def __str__(self):
        return self.item.name
