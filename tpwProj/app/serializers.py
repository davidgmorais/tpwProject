import six
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from app.models import Category, Cart, Item, Comment, Purchase, Sell, OrderItem, Profile
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

import re
import base64
import uuid
import imghdr


# Nested Serializers: https://django.cowhite.com/blog/create-and-update-django-rest-framework-nested-serializers/
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.ListSerializer(source="children", child=RecursiveField())

    class Meta:
        model = Category
        fields = ("id", "parent", "name", "slug", "subcategories")
        # extra_kwargs = {
        #     'slug': {'read_only': True},
        # }

    def create(self, validated_data):
        print(validated_data)
        subcategories_data = validated_data.pop('children')
        cat_slug = validated_data['name'].replace(" ", "").lower()
        if 'parent' in validated_data:
            parent = validated_data['parent']
            category = Category.objects.create(
                name=validated_data['name'],
                parent=parent,
                slug=cat_slug,
            )

        else:
            category = Category.objects.create(
                name=validated_data['name'],
                slug=cat_slug,
            )

        print("Hello")
        for subcategory_data in subcategories_data:
            print(subcategory_data)
            Category.objects.create(parent=category, name=subcategory_data['name'],
                                    slug=cat_slug + subcategory_data['name'].replace(" ", "").lower(), )
        return category

    def update(self, instance, validated_data):
        print(instance.children)
        print(validated_data)
        subcategories_data = validated_data.pop('children')

        subcategories = instance.children.all()
        subcategories = list(subcategories)
        print(subcategories)
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('name', instance.name).replace(" ", "").lower()
        instance.save()

        for subcategory_data in subcategories_data:
            subcategory = subcategories.pop(0)
            subcategory.name = subcategory_data.get('name', subcategory.name)
            subcategory.save()
        return instance


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            else:
                raise serializers.ValidationError()

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                raise serializers.ValidationError()

            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            file_extension = imghdr.what(file_name, decoded_file)
            file_extension = "jpg" if file_extension == "jpeg" else file_extension
            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)


class ItemSerializer(serializers.ModelSerializer):
    picture = Base64ImageField(
        max_length=None, use_url=True,
    )

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
    item = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Sell
        fields = ('id', 'item', 'user', 'moneyReceived', 'pendingSell', 'accepted')
        extra_kwargs = {
            'money': {'read_only': True},
        }

    def get_item(self, sell):
        serializer = ItemSerializer(sell.item)
        return serializer.data

    def get_user(self, sell):
        print(sell.user)
        serializer = ProfileSerializer(Profile.objects.get(id=sell.user.id))
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = User(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user


# Ainda está mal
# https://www.youtube.com/watch?v=Wo0AXv7B0iE
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'first_name', 'last_name', 'birthdate', 'money')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile = Profile.objects.get(user_id=user.id)
        profile.first_name = validated_data.pop('first_name')
        profile.last_name = validated_data.pop('last_name')
        profile.birthdate = validated_data.pop('birthdate')
        profile.money = 0
        profile.save()
        return profile
