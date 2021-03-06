from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken

from app.models import Category, Item, Comment, Profile, Purchase, Sell, Cart, OrderItem
from app.forms import Search, SignUpForm, ItemForm, CategoryForm, SubcategoryForm, CategoryFilter, CommentForm, \
    DeleteAccount, AddQuantityForm
from django.db.models import Q
from django.contrib.auth import login, authenticate
from datetime import datetime, timedelta
from json import dumps
from django.contrib.auth.models import User
from django.db.models import When, Case, Value, CharField, Avg, Count, Sum, F, FloatField
from django.db.models.functions import Extract, Round
from django.core.paginator import Paginator
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import CategorySerializer, ItemSerializer, OrderItemSerializer, CartSerializer, CommentSerializer, \
    PurchaseSerializer, SellSerializer, ProfileSerializer, UserSerializer
from rest_framework.authtoken.models import Token

from rest_framework import pagination

from base64 import decodestring
import re


# SERIALIZER'S VIEWS
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.root_nodes()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsAuthenticated,)
        self.authentication_classes = [TokenAuthentication]

        if request.user.username == 'admin':
            return self.create(request, *args, **kwargs)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def put(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsAuthenticated,)
        self.authentication_classes = [TokenAuthentication]

        if request.user.username == 'admin':
            return self.update(request, *args, **kwargs)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


def filterApi(result, params):
    if params.get('min'):
        result = result.filter(price__gte=params.get('min'))

    if params.get('max'):
        result = result.filter(price__lte=params.get('max'))

    if params.get('brand'):
        result = filter_by_brand(result, params.get('brand'))

    if params.get('availability'):
        result = filter_by_availability(result, params.get('availability'))

    if params.get('discount'):
        result = filter_by_discount(result, params.get('discount'))

    if params.get('reviews'):
        result = result.annotate(comment_avg=Round(Avg('comment__stars'))).filter(comment_avg=params.get('reviews'))

    if params.get('order'):
        result = order(result, params.get('order'))

    return result


class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    pagination_class = pagination.PageNumberPagination
    pagination.PageNumberPagination.page_size = 16

    def get_queryset(self):
        result = Item.objects.all()
        return filterApi(result, self.request.query_params)


class ItemView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        result = Item.objects.all()
        return filterApi(result, self.request.query_params)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsAuthenticated,)
        self.authentication_classes = [TokenAuthentication]

        if request.user.username == 'admin':
            print('i\'m admin')
            return self.create(request, *args, **kwargs)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryItemView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    pagination_class = pagination.PageNumberPagination
    pagination.PageNumberPagination.page_size = 16

    def get_queryset(self):
        slug = self.kwargs['slug']
        result = Item.objects.filter(category__slug=slug)
        return filterApi(result, self.request.query_params)


class NewItemView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    pagination_class = pagination.PageNumberPagination
    pagination.PageNumberPagination.page_size = 16

    def get_queryset(self):
        result = Item.objects.filter(insertDate__range=[datetime.today() - timedelta(days=14),
                                                        datetime.today()]).order_by("-insertDate")
        return filterApi(result, self.request.query_params)


class PromoItemView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    pagination_class = pagination.PageNumberPagination
    pagination.PageNumberPagination.page_size = 16

    def get_queryset(self):
        result = Item.objects.filter(discount__gt=0).order_by('-discount')
        return filterApi(result, self.request.query_params)


class ItemDetailView(generics.RetrieveUpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def put(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsAuthenticated,)
        self.authentication_classes = [TokenAuthentication]

        if request.user.username == 'admin':
            return self.update(request, *args, **kwargs)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class OrderItemView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def post(self, request, *args, **kwargs):
        try:
            orderItem = OrderItem.objects.get(item__id=request.data['item'])
            orderItem.qty += 1
            orderItem.save()
            return Response(status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            serializer = OrderItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(validated_data=request.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderItemDetailView(generics.RetrieveUpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']

        try:
            c = Cart.objects.get(user__id=pk)
        except Cart.DoesNotExist:
            c = Cart(user=User.objects.get(id=pk))
            c.save()
        return Response(CartSerializer(c, many=False).data)


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



class PurchaseView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class PurchaseDetailView(generics.RetrieveUpdateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SellView(generics.ListCreateAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer


class SellDetailView(generics.RetrieveUpdateAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ApproveListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    queryset = Sell.objects.all()
    serializer_class = SellSerializer


class ItemSearch(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        query = self.kwargs['query']
        return Item.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name=query)
        ).distinct()


@api_view(['GET'])
def brand_list(request):
    brands = [i['brand'] for i in Item.objects.all().values('brand').distinct()]
    return Response(status=status.HTTP_200_OK, data=brands)


# SERIALIZER'S ADMIN VIEWS
@api_view(['PUT'])
def decline_view(request, sell_id):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    if request.user.username == 'admin':
        sell = Sell.objects.get(id=sell_id)
        sell.pendingSell = False
        sell.accepted = False
        sell.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def approve_view(request, sell_id):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    if request.user.username == 'admin':
        sell = Sell.objects.get(id=sell_id)
        sell.pendingSell = False
        sell.accepted = True
        sell.save()

        item = Item.objects.get(id=sell.item.id)
        item.quantity += 1
        item.save()

        profile = Profile.objects.get(user__email=sell.user.email)
        if profile.money is None:
            profile.money = sell.moneyReceived
        profile.money += sell.moneyReceived
        profile.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def discount_stats_view(request):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    if request.user.username == 'admin':
        stats = Purchase.objects.aggregate(Discounted=Count(Case(When(discountedP=True, then=Value(1)))),
                                           FullPrice=Count(Case(When(discountedP=False, then=Value(1)))))
        return Response(status=status.HTTP_200_OK, data=stats)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def purchased_cat_view(request):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    if request.user.username == 'admin':
        categories = Category.objects.values('parent').annotate(purchases=Count('item__purchase')).order_by(
            '-purchases')
        for c in categories:
            if c['parent'] is not None:
                c['name'] = Category.objects.get(id=c['parent']).name
        return Response(status=status.HTTP_200_OK, data=categories)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def purchases_age_view(request):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    if request.user.username == 'admin':
        age_groups = Profile.objects.annotate(Age=datetime.today().year - Extract('birthdate', 'year'),
                                              AgeGroup=Case(When(Age__gte=65, then=Value('over 65')),
                                                            When(Age__range=[41, 65], then=Value('41-65')),
                                                            When(Age__range=[18, 40], then=Value('18-40')),
                                                            When(Age__lt=18, then=Value('under 18')),
                                                            output_field=CharField()),
                                              ).values('AgeGroup').annotate(purchases=Count('user__purchase__item'))
        return Response(status=status.HTTP_200_OK, data=age_groups)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def best_buyers_view(request):
    if request.user.username == 'admin':
        users = Profile.objects.annotate(purchases=Count('user__purchase'))
        if len(users) >= 5:
            users = users[:5]
        serializer = ProfileSerializer(users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def out_of_stock_view(request):
    if request.user.username == 'admin':
        items = Item.objects.filter(quantity=0)
        serializer = ItemSerializer(items, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# SERIALIZER'S DELETE VIEWS
@api_view(['DELETE'])
def api_delete_category(request, id):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    if request.user.username == 'admin':
        try:
            cat = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
def api_delete_item(request, id):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    if request.user.username == 'admin':
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
def api_delete_orderitem(request, id):

    try:
        orderItem = OrderItem.objects.get(id=id)
        print(orderItem);
    except OrderItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not request.user or request.user.id != orderItem.cart.user.id:
        print(request.user.id)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    orderItem.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def api_delete_cart(request, id):
    try:
        cart = Cart.objects.get(id=id)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def api_delete_comment(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# SERIALIZER'S PROFILE VIEWS
@api_view(['GET'])
def api_get_profiles(request):
    print(request.GET)
    profs = Profile.objects.all()
    serializer = ProfileSerializer(profs, many=True)
    return Response(serializer.data)


class ProfileView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_get_profile(request, _id):
    print(request.GET)
    try:
        prof = Profile.objects.get(id=_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSerializer(prof)
    return Response(serializer.data)


@api_view(['POST'])
def api_create_profiles(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_update_profiles(request, id):
    try:
        prof = Profile.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSerializer(prof, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def api_delete_profiles(request, id):
    print(request)
    try:
        prof = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    prof.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Collapse all: CTRL + SHIFT + -
def home(request):
    biggest_discount = Item.objects.filter(discount__gt=0).order_by('-discount')
    if len(biggest_discount) > 0:
        biggestDiscount = biggest_discount[0].discount
    else:
        biggestDiscount = 0

    tparams = {
        'discountedItems': Item.objects.filter(discount__gt=0).order_by('-discount')[:4],
        'biggestDiscount': biggestDiscount,
        'newestItems': Item.objects.filter(insertDate__range=[datetime.today() - timedelta(days=14),
                                                              datetime.today()]).order_by("-insertDate")[:4],
        'categories': Category.objects.all(),
    }

    if request.user.is_authenticated:
        try:
            c = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            c = Cart(user=request.user)
            c.save()
        tparams['cart'] = c

    # 'bestsellerItems': Item.objects.all().annotate(comment_avg=Avg('comment__stars'))[:4],

    return render(request, 'homePage.html', tparams)


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.birthdate = form.cleaned_data.get('birthdate')

            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('HomePage')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'categories': Category.objects.all(), })


def order(items, mode):
    if mode == "1":
        items = items.order_by("-insertDate")
    elif mode == "2":
        items = items.annotate(true_price=F('price') * (100 - F('discount')) / 100).order_by("true_price")
    elif mode == "3":
        items = items.annotate(true_price=F('price') * (100 - F('discount')) / 100).order_by("-true_price")
    elif mode == "4":
        items = items.annotate(purchase_qty=Count('purchase')).order_by('-purchase_qty')
    elif mode == "5":
        items = items.order_by('-discount')

    return items


def itemList(request):
    items = Item.objects.all()
    if request.method == 'GET':
        form = CategoryFilter(request.GET)
        print(request.GET)
        if form.is_valid():
            if 'categories' in request.GET:
                items = filer_by_category(items, form.cleaned_data['categories'])
            if 'brand' in request.GET:
                items = filter_by_brand(items, form.cleaned_data['brand'])
            if 'availability' in request.GET:
                items = filter_by_availability(items, form.cleaned_data['availability'])
            if 'discounted' in request.GET:
                items = filter_by_discount(items, form.cleaned_data['discounted'])
            if 'reviews' in request.GET:
                items = filter_by_reviews(items, form.cleaned_data['reviews'])
            if 'price' in request.GET:
                items = filter_by_price(items, form.cleaned_data['price'])
            if 'order' in request.GET:
                items = order(items, form.cleaned_data['order'])
    else:
        form = CategoryFilter()
    paginator = Paginator(items, 16)
    page_nr = request.GET.get('page')
    items = paginator.get_page(page_nr)

    tparams = {
        'items': items,
        'categories': [cat for cat in Category.objects.all() if cat.parent is None],
        'form': form,
        'title': "All Items",
        'categories': Category.objects.all(),

    }

    if request.user.is_authenticated:
        try:
            c = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            c = Cart(user=request.user)
            c.save()
        tparams['cart'] = c
        tparams['categories'] = Category.objects.all()

    return render(request, 'Items/itemList.html', tparams)


def itemListCat(request, slug):
    items = Item.objects.filter(category__slug=slug)

    if request.method == 'GET':
        form = CategoryFilter(request.GET)
        print(request.GET)
        if form.is_valid():
            if 'categories' in request.GET:
                items = filer_by_category(items, form.cleaned_data['categories'])
            if 'brand' in request.GET:
                items = filter_by_brand(items, form.cleaned_data['brand'])
            if 'availability' in request.GET:
                items = filter_by_availability(items, form.cleaned_data['availability'])
            if 'discounted' in request.GET:
                items = filter_by_discount(items, form.cleaned_data['discounted'])
            if 'reviews' in request.GET:
                items = filter_by_reviews(items, form.cleaned_data['reviews'])
            if 'price' in request.GET:
                items = filter_by_price(items, form.cleaned_data['price'])
            if 'order' in request.GET:
                items = order(items, form.cleaned_data['order'])
    else:
        form = CategoryFilter()

    paginator = Paginator(items, 16)
    page_nr = request.GET.get('page')
    items = paginator.get_page(page_nr)

    c = Category.objects.get(slug=slug)
    tparams = {
        'items': items,
        'form': form,
        'title': c.name,
        'categories': Category.objects.all(),
    }

    if request.user.is_authenticated:
        try:
            c = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            c = Cart(user=request.user)
            c.save()
        tparams['cart'] = c
        tparams['categories'] = Category.objects.all()

    return render(request, 'Items/itemList.html', tparams)


def itemListNew(request):
    items = Item.objects.filter(insertDate__range=[datetime.today() - timedelta(days=14),
                                                   datetime.today()]).order_by("-insertDate")
    if request.method == 'GET':
        form = CategoryFilter(request.GET)
        print(request.GET)
        if form.is_valid():
            if 'categories' in request.GET:
                items = filer_by_category(items, form.cleaned_data['categories'])
            if 'brand' in request.GET:
                items = filter_by_brand(items, form.cleaned_data['brand'])
            if 'availability' in request.GET:
                items = filter_by_availability(items, form.cleaned_data['availability'])
            if 'discounted' in request.GET:
                items = filter_by_discount(items, form.cleaned_data['discounted'])
            if 'reviews' in request.GET:
                items = filter_by_reviews(items, form.cleaned_data['reviews'])
            if 'price' in request.GET:
                items = filter_by_price(items, form.cleaned_data['price'])
            if 'order' in request.GET:
                items = order(items, form.cleaned_data['order'])
    else:
        form = CategoryFilter()

    paginator = Paginator(items, 16)
    page_nr = request.GET.get('page')
    items = paginator.get_page(page_nr)

    tparams = {
        'items': items,
        'categories': [cat for cat in Category.objects.all() if cat.parent is None],
        'form': form,
        'title': "New in",
        'categories': Category.objects.all(),
    }

    if request.user.is_authenticated:
        try:
            c = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            c = Cart(user=request.user)
            c.save()
        tparams['cart'] = c
        tparams['categories'] = Category.objects.all()

    return render(request, 'Items/itemList.html', tparams)


def itemListPromos(request):
    items = Item.objects.filter(discount__gt=0).order_by('-discount')
    if request.method == 'GET':
        form = CategoryFilter(request.GET)
        print(request.GET)
        if form.is_valid():
            if 'categories' in request.GET:
                items = filer_by_category(items, form.cleaned_data['categories'])
            if 'brand' in request.GET:
                items = filter_by_brand(items, form.cleaned_data['brand'])
            if 'availability' in request.GET:
                items = filter_by_availability(items, form.cleaned_data['availability'])
            if 'discounted' in request.GET:
                items = filter_by_discount(items, form.cleaned_data['discounted'])
            if 'reviews' in request.GET:
                items = filter_by_reviews(items, form.cleaned_data['reviews'])
            if 'price' in request.GET:
                items = filter_by_price(items, form.cleaned_data['price'])
            if 'order' in request.GET:
                items = order(items, form.cleaned_data['order'])
    else:
        form = CategoryFilter()

    paginator = Paginator(items, 16)
    page_nr = request.GET.get('page')
    items = paginator.get_page(page_nr)

    tparams = {
        'items': items,
        'categories': [cat for cat in Category.objects.all() if cat.parent is None],
        'form': form,
        'title': "Promos",
        'categories': Category.objects.all(),
    }

    if request.user.is_authenticated:
        try:
            c = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            c = Cart(user=request.user)
            c.save()
        tparams['cart'] = c
        tparams['categories'] = Category.objects.all()

    return render(request, 'Items/itemList.html', tparams)


def item(request, id):
    items = Item.objects.get(id=id)
    tparams = {
        'item': items,
        'comments': Comment.objects.filter(item=items),
        'categories': Category.objects.all(),
    }
    return render(request, 'Items/itemPage.html', tparams)


def search(request):
    if 'query' in request.POST:
        form = Search(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            results = Item.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name=query)
            ).distinct()
            return render(request, 'Items/searchResults.html',
                          {'items': results, 'query': query, 'categories': Category.objects.all(), 'form': form})
    else:
        form1 = Search()
    return render(request, 'Items/itemList.html',
                  {'items': Item.objects.all(), 'categories': Category.objects.all(), 'form': form1})


@login_required
def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return redirect("/")

    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return redirect("/")

    try:
        c = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        c = Cart(user=request.user)
        c.save()

    try:
        order_item = OrderItem.objects.get(item__id=id)
        if order_item.qty < order_item.item.quantity:
            order_item.qty += 1
            order_item.save()
    except OrderItem.DoesNotExist:
        order_item = OrderItem(item=item, qty=1, cart_id=c.id)
        order_item.save()

    return redirect("/cart")


def sell_item(request, id):
    if not request.user.is_authenticated:
        return redirect("/login")
    item = Item.objects.get(id=id)
    sell = Sell(
        item=item,
        user=request.user,
        moneyReceived=item.sellMoney,
        pendingSell=True,
        accepted=False
    )
    sell.save()
    return redirect("/account")


def get_items():
    return Item.objects.all()


def get_promos():
    return Item.objects.annotate(comment_avg=Avg('comment__stars')).values().filter(discount__gt=0)


def get_new_items(day_range=14):
    return Item.objects.annotate(comment_avg=Avg('comment__stars')).values().filter(insertDate__range=[
        datetime.today() - timedelta(days=day_range),
        datetime.today()
    ]).order_by("-insertDate")


def get_top_promo():
    promos = Item.objects.annotate(comment_avg=Avg('comment__stars')).values().filter(discount__gt=0).order_by(
        '-discount')
    if len(promos) > 0:
        return promos[0]


def get_bestsellers(top=10):
    if top < 1:
        return None
    b_sellers = Item.objects.all().items.annotate(purchase_qty=Count('purchase')).order_by('-purchase_qty')[:top]
    if top >= len(b_sellers):
        return b_sellers
    return b_sellers[:top]


def get_categories():
    category_dic = dict()
    categories = [c for c in Category.objects.all() if c.parent is None]
    for c in categories:
        category_dic[c] = get_subcategories(c.id)
    return category_dic


def get_subcategories(cat_id):
    subcategories = [sc for sc in Category.objects.all() if sc.parent is not None and sc.parent.id == cat_id]
    return subcategories


def get_pending():
    s = Sell.objects.filter(pendingSell=True)
    return s


def get_cart(email):
    return OrderItem.objects.filter(cart__user__email=email)


def get_cart_total(cart_items):
    return cart_items.aggregate(price=Sum((F('item__price') * (100 - F('item__discount')) / 100) * F('qty'),
                                          output_field=FloatField()))['price']


def filer_by_category(query, slug):
    category_id = slug.split("-")[0]
    return query.filter(category__slug__contains=(category_id + "-"))


def filter_by_price(query, list):
    query = Q(true_price__range=[list[0].split("-")[0], list[0].split("-")[1]])
    for pair in list[1:]:
        if "+" in pair:
            query.add(Q(true_price__gt=pair.split("+")[0]), Q.OR)
        else:
            query.add(Q(true_price__range=[pair.split("-")[0], pair.split("-")[1]]), Q.OR)

    items = Item.objects.annotate(true_price=F('price') * (100 - F('discount')) / 100) \
        .filter(query)
    return items


def filter_by_brand(query, brand):
    return query.filter(brand__exact=brand)


def filter_by_availability(query, availability_flag):
    if availability_flag == "1":
        return query.filter(quantity__gt=0)
    return query.filter(quantity__exact=0)


def filter_by_discount(query, discounted_flag):
    if discounted_flag == "1":
        return query.filter(discount__gt=0)
    return query.filter(discount__exact=0)


def filter_by_reviews(query, star_list):
    query = Q(comment_avg__lte=int(star_list[0]), comment_avg__gt=int(star_list[0]) - 1)
    for i in star_list[1:]:
        query.add(Q(comment_avg__lte=int(i), comment_avg__gt=int(i) - 1), Q.OR)
    print(query)
    return Item.objects.annotate(comment_avg=Round(Avg('comment__stars'))).filter(query)


def purchased_cat():
    categories = Category.objects.values('parent').annotate(purchases=Count('item__purchase')).order_by('-purchases')
    for c in categories:
        if c['parent'] is not None:
            c['name'] = Category.objects.get(id=c['parent']).name
    return categories


# users with more purchases
def best_buyers(top=1):
    users = User.objects.annotate(purchases=Count('purchase'))
    if len(users) >= top:
        return users[:top]
    return users


# users with more sells
def best_sellers(top=1):
    users = User.objects.annotate(sells=Count('sell'))
    if len(users) >= top:
        return users[:top]


# number of purchases per age group
def purchases_age():
    age_groups = Profile.objects.annotate(Age=datetime.today().year - Extract('birthdate', 'year'),
                                          AgeGroup=Case(When(Age__gte=65, then=Value('over 65')),
                                                        When(Age__range=[41, 65], then=Value('41-65')),
                                                        When(Age__range=[18, 40], then=Value('18-40')),
                                                        When(Age__lt=18, then=Value('under 18')),
                                                        output_field=CharField()),
                                          ).values('AgeGroup').annotate(purchases=Count('user__purchase__item'))
    return age_groups


# ratio between discounted and full price purchases
def discount_stats():
    return Purchase.objects.aggregate(Discounted=Count(Case(When(discountedP=True, then=Value(1)))),
                                      FullPrice=Count(Case(When(discountedP=False, then=Value(1)))))


# Create your views here.
def home_page(request):
    t_params = {
        "deal_of_day": get_top_promo(),
        "new_in": get_new_items(7)[:4],
        "promos": get_promos()[:4],
        "best_sellers": get_bestsellers(10),
        "products": get_items()[:8],
        'categories': Category.objects.all(),
    }
    if request.user.is_authenticated:
        t_params["profile"] = Profile.objects.get(user=request.user)
        item_cart = get_cart(request.user.email)
        t_params["cart"] = item_cart
        t_params["total_cart"] = get_cart_total(item_cart)
        t_params["categories"] = Category.objects.all()

    return render(request, 'index.html', t_params)


def admin(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")
    t_params = {
        "items": get_new_items(7),

        "category": dict(list(get_categories().items())[:5]),
        "pending": get_pending(),
        "purchase_age": dumps(list(purchases_age())),
        "best_buyers": best_buyers(5),
        "discount_stats": dumps(discount_stats()),
        "purchased_cat": dumps(list(purchased_cat())),
        "out_of_stock": Item.objects.filter(quantity=0)
    }
    return render(request, "AdminTemplates/dashboard.html", t_params)


def manage_out_of_stock_items(request):
    return render(request, "AdminTemplates/out_of_stock.html",
                  {"table": Item.objects.filter(quantity=0), "type": "itemList"})


def edit_out_of_stock_items(request, item_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    if request.method == "POST":
        form = AddQuantityForm(request.POST)
        if form.is_valid():
            item = Item.objects.get(id=item_id)
            qty = form.cleaned_data["quantity"]
            item.quantity = qty
            item.save()
            return redirect("/admin/outofstock")
    else:
        item = Item.objects.get(id=item_id)
        form = ItemForm(initial={"quantity": item.quantity})

    return render(request, "AdminTemplates/out_of_stock.html", {"form": form, "type": "item", "item": item})


def manage_items(request):
    return render(request, "AdminTemplates/managment_table.html", {"table": get_items(), "type": "item"})


def add_item(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = Item(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                specifications=form.cleaned_data["specification"],
                price=form.cleaned_data["price"],
                quantity=form.cleaned_data["quantity"],
                brand=form.cleaned_data["brand"],
                insertDate=datetime.today(),
                discount=form.cleaned_data["discount"],
                sellMoney=form.cleaned_data["sellMoney"],
                category=Category.objects.get(id=form.cleaned_data["category"]),
                picture=request.FILES["picture"]
            )
            item.save()
            print(item)
            return redirect("/admin/item")
    else:
        form = ItemForm()
    return render(request, "AdminTemplates/add_edit.html", {"form": form, "action": "add", "type": "item"})


def edit_item(request, item_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = Item.objects.get(id=item_id)
            item.name = form.cleaned_data["name"]
            item.description = form.cleaned_data["description"]
            item.price = form.cleaned_data["price"]
            item.quantity = form.cleaned_data["quantity"]
            item.brand = form.cleaned_data["brand"]
            item.category = Category.objects.get(id=form.cleaned_data["category"])
            item.discount = form.cleaned_data["discount"]
            item.sellMoney = form.cleaned_data["sellMoney"]
            item.specifications = form.cleaned_data["specification"]
            item.picture = request.FILES["picture"]
            item.save()
            return redirect("/admin/item")
    else:
        item = Item.objects.get(id=item_id)
        form = ItemForm(initial={"name": item.name,
                                 "description": item.description,
                                 "price": item.price,
                                 "brand": item.brand,
                                 "quantity": item.quantity,
                                 "category": item.category,
                                 "discount": item.discount,
                                 "sellMoney": item.sellMoney,
                                 "specification": item.specifications,
                                 "picture": item.picture
                                 })
    return render(request, "AdminTemplates/add_edit.html", {"form": form, "action": "edit", "type": "item"})


def delete_item(request, item_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")
    if 'delete' in request.POST:
        item = Item.objects.get(id=item_id)
        item.delete()
        return redirect("/admin/item/")
    else:
        return render(request, "AdminTemplates/delete.html")


# CATEGORIES
def manage_category(request):
    return render(request, "AdminTemplates/managment_table.html", {"table": get_categories(), "type": "category"})


def add_category(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            c = Category(
                name=form.cleaned_data["category"],
                slug=0,
                parent=None
            )
            c.save()
            c.slug = str(c.id) + "-00"
            c.save()
            return redirect("/admin/category")
    else:
        form = CategoryForm()
    return render(request, "AdminTemplates/add_edit.html", {"form": form, "action": "add", "type": "category"})


def edit_category(request, category_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category.objects.get(id=category_id)
            category.name = form.cleaned_data["category"]
            category.save()
            return redirect("/admin/category")
    else:
        form = CategoryForm(initial={"category": Category.objects.get(id=category_id).name})

    t_params = {
        "form": form,
        "subcategory_list": get_subcategories(category_id),
        "action": "edit",
    }
    return render(request, "AdminTemplates/cat_add_edit.html", t_params)


def delete_category(request, category_id, subcategory_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    if 'delete' in request.POST:
        c = Category.objects.get(id=category_id)
        c.delete()
        return redirect("/admin/category")
    else:
        return render(request, "AdminTemplates/delete.html")


def add_subcategory(request, category_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    if request.method == "POST":
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            sc = Category(
                name=form.cleaned_data["subcategory"],
                slug=0,
                parent=Category.objects.get(id=category_id)
            )
            sc.save()
            sc.slug = str(category_id) + "-" + str(sc.id)
            sc.save()
            return redirect("/admin/category/" + str(category_id) + "/edit/")
    else:
        form = SubcategoryForm()
    return render(request, "AdminTemplates/add_edit.html", {"form": form, "action": "add", "type": "subcategory",
                                                            "parentCat": Category.objects.get(id=category_id)})


def add_new_subcategory(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    print(request.method)
    if request.method == "POST":
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            parent = Category.objects.get(id=form.cleaned_data['parent'])
            sc = Category(
                name=form.cleaned_data["subcategory"],
                slug=0,
                parent=parent
            )
            sc.save()
            sc.slug = str(parent.id) + "-" + str(sc.id)
            sc.save()
            return redirect("/admin/category/" + str(parent.id) + "/edit/")
    else:
        form = SubcategoryForm()
    return render(request, "AdminTemplates/add_new_subcategory.html", {"form": form})


def edit_subcategory(request, category_id, subcategory_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    if request.method == "POST":
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            sc = Category.objects.get(slug=str(category_id) + "-" + str(subcategory_id))
            sc.name = form.cleaned_data["subcategory"]
            sc.save()
            return redirect("/admin/category/" + str(category_id) + "/edit/")
    else:
        form = SubcategoryForm(initial={
            "subcategory": Category.objects.get(slug=str(category_id) + "-" + str(subcategory_id)).name
        })
    return render(request, "AdminTemplates/add_edit.html", {"form": form, "action": "edit", "type": "subcategory"})


def delete_subcategory(request, category_id, subcategory_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    if 'delete' in request.POST:
        sc = Category.objects.get(slug=str(category_id) + "-" + str(subcategory_id))
        sc.delete()
        return redirect("/admin/category")
    else:
        return render(request, "AdminTemplates/delete.html")


# Sells Admin
def approve_list(request):
    purchases = Sell.objects.all()
    return render(request, "AdminTemplates/approve_purchase.html", {"purchases": purchases})


def approve(request, sell_id):
    sell = Sell.objects.get(id=sell_id)
    sell.pendingSell = False
    sell.accepted = True
    sell.save()

    item = Item.objects.get(id=sell.item.id)
    item.quantity += 1
    item.save()

    profile = Profile.objects.get(user__email=sell.user.email)
    print(profile.money)
    if profile.money is None:
        profile.money = sell.moneyReceived
    profile.money += sell.moneyReceived
    print(profile.money)
    profile.save()
    return redirect("/admin/purchases")


def decline(request, sell_id):
    sell = Sell.objects.get(id=sell_id)
    sell.pendingSell = False
    sell.accepted = False
    sell.save()
    return redirect("/admin/purchases")


def purchase_details(request, sell_id):
    sell = Sell.objects.get(id=sell_id)
    profit = sell.moneyReceived - sell.item.price
    return render(request, "AdminTemplates/purchase_details.html", {"details": sell, "profit": profit})


# ACOUNT
def account(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    profile = Profile.objects.get(user__email=request.user.email)
    item_cart = get_cart(request.user.email)

    t_params = {
        "profile": profile,
        "purchases": Purchase.objects.filter(user__email=profile.user.email).order_by("-id"),
        "sells": Sell.objects.filter(user__email=profile.user.email).order_by("-id"),
        "comments": Comment.objects.filter(user__email=profile.user.email),
        "cart": item_cart,
        "total_cart": get_cart_total(item_cart),
        "categories": Category.objects.all(),
    }
    return render(request, "Account/account.html", t_params)


def delete_account(request):
    if not request.user.is_authenticated:
        redirect('/')

    if request.method == "POST":
        form = DeleteAccount(request.POST)
        if form.is_valid():
            try:
                user = authenticate(username=request.user.username, password=form.cleaned_data['password'])
                if user is not None:
                    user.delete()
                    return redirect('/')
            except User.DoesNotExist:
                return redirect('/')

    else:
        form = DeleteAccount()

    return render(request, "Account/delete_account.html", {"form": form, "categories": Category.objects.all()})


def account_add_comments(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            item = Item.objects.get(name=form.cleaned_data['item'])
            purchases = []
            for x in Purchase.objects.filter(user__email=request.user.email):
                purchases.append(x.item)

            if item in purchases:
                try:
                    cc = Comment.objects.get(item=item)
                    cc.delete()
                except Comment.DoesNotExist:
                    print("does not exist")

                c = Comment(
                    user=request.user,
                    item=item,
                    stars=form.cleaned_data["stars"],
                    text=form.cleaned_data["comment"],
                )
                c.save()
                return redirect("/account")
    else:
        form = CommentForm()
    return render(request, "Account/add_edit_comment.html",
                  {"form": form, "action": "add", "categories": Category.objects.all()})


def account_edit_comments(request, item_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.filter(user=request.user).get(item=item_id)
            comment.stars = form.cleaned_data["stars"]
            comment.text = form.cleaned_data["comment"]
            comment.save()
            return redirect("/account")
    else:
        comment = Comment.objects.filter(user=request.user).get(item=item_id)
        form = CommentForm(initial={
            "stars": comment.stars,
            "comment": comment.text})
    print(form.errors)
    return render(request, "Account/add_edit_comment.html",
                  {"form": form, "action": "edit", "categories": Category.objects.all(),
                   'item': Item.objects.get(id=item_id)})


def account_delete_comment(request, item_id):
    if not request.user.is_authenticated:
        return redirect("/login")
    if 'delete' in request.POST:
        comment = Comment.objects.get(item=Item.objects.get(id=item_id))
        comment.delete()
        return redirect("/account")
    else:
        return render(request, "Account/delete_comment.html", {"categories": Category.objects.all()})


# CART
def cart(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if 'done' in request.GET:  # shopping finalized
        c = Cart.objects.get(user__email=request.user.email)
        for item in c.orderitem_set.all():
            if item.item.discount != 0:
                price = item.get_final_price()
                discounted = True
            else:
                price = item.get_final_price()
                discounted = False

            # decrease item quantity
            i = Item.objects.get(id=item.item.id)
            i.quantity -= item.qty

            # make purchases
            p = Purchase(
                item=item.item,
                user=request.user,
                price=price,
                discountedP=discounted
            )

            # update user's money
            if 'discount' in request.GET:
                profile = Profile.objects.get(user__email=request.user.email)
                if profile.money > c.total():
                    profile.money -= c.total()
                else:
                    profile.money = 0
                profile.save()

            # save changes
            i.save()
            p.save()
        c.delete()
        return redirect("/")

    else:  # show cart
        try:
            c = Cart.objects.get(user__email=request.user.email)
        except Cart.DoesNotExist:
            c = Cart(user=request.user)
            c.save()

        t_parent = {
            "cart": c,
            "money": Profile.objects.get(user__email=request.user.email).money,
            'categories': Category.objects.all(),
        }
        return render(request, "Cart/cart.html", t_parent)


def increase_cart(request, order_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    order_item = OrderItem.objects.get(id=order_id)
    if order_item.qty < order_item.item.quantity:
        order_item.qty += 1
        order_item.save()
    return redirect("/cart")


def decrease_cart(request, order_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    order_item = OrderItem.objects.get(id=order_id)
    if order_item.qty > 1:
        order_item.qty -= 1
        order_item.save()
    return redirect("/cart")


def remove_cart(request, order_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    order_item = OrderItem.objects.get(id=order_id)
    order_item.delete()
    return redirect("/cart")
