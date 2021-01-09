from app.models import Category, Cart, Item, Comment, Purchase, Sell, OrderItem, Profile
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField


# Nested Serializers: https://django.cowhite.com/blog/create-and-update-django-rest-framework-nested-serializers/
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.ListSerializer(source="children", child=RecursiveField())

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "subcategories")
        extra_kwargs = {
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        print(validated_data)
        subcategories_data = validated_data.pop('children')
        cat_slug = validated_data['name'].replace(" ", "").lower()
        category = Category.objects.create(
            name=validated_data['name'],
            slug=cat_slug,
        )
        print("Hello")
        for subcategory_data in subcategories_data:
            print(subcategory_data)
            Category.objects.create(parent=category, name=subcategory_data['name'],
                                    slug=cat_slug+subcategory_data['name'].replace(" ", "").lower(),)
        return category

    def update(self, instance, validated_data):
        print(instance.children)
        print(validated_data)
        subcategories_data = validated_data.pop('children')

        subcategories = instance.children.all()
        subcategories = list(subcategories)
        print(subcategories)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        for subcategory_data in subcategories_data:
            subcategory = subcategories.pop(0)
            subcategory.name = subcategory_data.get('name', subcategory.name)
            subcategory.save()
        return instance


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'specifications', 'price', 'brand',
                  'quantity', 'insertDate', 'discount', 'picture', 'sellMoney', 'category')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'cart', 'item', 'qty')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user')
        extra_kwargs = {
            'user': {'read_only': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'item', 'user', 'text', 'stars')


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('id', 'item', 'user', 'price', 'discountedP')


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = ('id', 'item', 'user', 'moneyReceived', 'pendingSell', 'accepted')
        extra_kwargs = {
            'money': {'read_only': True},
        }


# Ainda está mal
# https://www.youtube.com/watch?v=Wo0AXv7B0iE
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'first_name', 'last_name', 'birthdate', 'money')

