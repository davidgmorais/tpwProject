from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.models import Category, Item, Comment, Profile, Purchase, Sell, Cart, OrderItem
from app.forms import Search, SignUpForm, Filters, ItemForm, CategoryForm, SubcategoryForm, CategoryFilter
from django.db.models import Q, Max
from django.contrib.auth import login, authenticate
from datetime import datetime, timedelta
from json import dumps
from django.contrib.auth.models import User
from django.db.models import When, Case, Value, CharField, Avg, Count, Sum, F, FloatField
from django.db.models.functions import Extract, Round


def home(request):
    tparams = {
        'discountedItems': Item.objects.filter(discount__gt=0).order_by('-discount')[:4],
        'biggestDiscount': Item.objects.filter(discount__gt=0).order_by('-discount')[0].discount,
        'newestItems': Item.objects.filter(insertDate__range=[datetime.today() - timedelta(days=14),
                                                                datetime.today()]).order_by("-insertDate")[:4],
        'categories': Category.objects.all(),
    }
    #'bestsellerItems': Item.objects.all().annotate(comment_avg=Avg('comment__stars'))[:4],

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
    return render(request, 'signup.html', {'form': form})


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
                print(items)
            if 'price' in request.GET:
                items = filter_by_price(items, form.cleaned_data['price'])
    else:
        form = CategoryFilter()

    try:
        c = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        c = Cart(user=request.user)
        c.save()

    tparams = {
        'items': items,
        'categories': [cat for cat in Category.objects.all() if cat.parent is None],
        'form': form,
        'cart': c
    }

    return render(request, 'itemList.html', tparams)


def itemListCat(request, slug):
    tparams = {
        'items': Item.objects.filter(category__slug=slug),
    }
    return render(request, 'itemList.html', tparams)


def itemListNew(request):

    tparams = {
        'items': Item.objects.filter(insertDate__range=[
            datetime.today() - timedelta(days=14), datetime.today()]).order_by("-insertDate")
    }
    return render(request, 'itemListNew.html', tparams)


def itemListPromos(request):
    tparams = {
        'items': Item.objects.filter(discount__gt=0).order_by('-discount')
    }
    return render(request, 'itemListPromos.html', tparams)


def item(request, id):
    items = Item.objects.get(id=id)
    tparams = {
        'item': items,
        'comments': Comment.objects.filter(item=items)
    }
    return render(request, 'itemPage.html', tparams)


def search(request):
    if 'query' in request.POST:
        form = Search(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            results = Item.objects.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__name=query)
                    # Q(category__parent=query) ID
                ).distinct()

        return render(request, 'searchResults.html', {'items': results, 'query': query})

    else:
        form = Search()
    return render(request, 'itemList.html', {'items': Item.objects.all()})


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
    return Item.objects.all().annotate(comment_avg=Avg('comment__stars')).values().order_by("-quantity")[:top]


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



#
# def search(search_term):
#     return Item.objects.filter(name__contains=search_term)


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
    }
    if request.user.is_authenticated:
        t_params["profile"] = Profile.objects.get(user=request.user)
        item_cart = get_cart(request.user.email)
        t_params["cart"] = item_cart
        t_params["total_cart"] = get_cart_total(item_cart)

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
        "purchased_cat": dumps(list(purchased_cat()))
    }
    return render(request, "AdminTemplates/dashboard.html", t_params)


def manage_items(request):
    return render(request, "AdminTemplates/managment_table.html", {"table": get_items(), "type": "item"})


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
            item.category = Category.objects.get(id=form.cleaned_data["category"][0])
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
                category=Category.objects.get(id=form.cleaned_data["category"][0]),
                picture=request.FILES["picture"]
            )
            item.save()
            print(item)
            return redirect("/admin/item")
    else:
        form = ItemForm()
    return render(request, "AdminTemplates/add_edit.html", {"form": form, "action": "add", "type": "item"})


def manage_category(request):
    return render(request, "AdminTemplates/managment_table.html", {"table": get_categories(), "type": "category"})


def edit_category(request, category_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category.objects.get(slug=str(category_id) + "-00")
            category.name = form.cleaned_data["category"]
            category.save()
            return redirect("/admin/category")
    else:
        form = CategoryForm(initial={"category": Category.objects.get(slug=str(category_id) + "-00").name})

    t_params = {
        "form": form,
        "subcategory_list": get_subcategories(category_id),
        "action": "edit",
    }
    return render(request, "AdminTemplates/cat_add_edit.html", t_params)


def delete_subcategory(request, category_id, subcategory_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    if 'delete' in request.POST:
        sc = Category.objects.get(slug=str(category_id) + "-" + str(subcategory_id))
        sc.delete()
        return redirect("admin/category")
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
    return render(request, "AdminTemplates/add_edit.html", {"form": form, "action": "add", "type": "subcategory"})


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


def delete_category(request, category_id):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("/login")

    if 'delete' in request.POST:
        c = Category.objects.get(id=category_id)
        c.delete()
        return redirect("admin/category")
    else:
        return render(request, "AdminTemplates/delete.html")


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
    profile.money += sell.moneyReceived
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


def account(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    profile = Profile.objects.get(user__email=request.user.email)
    item_cart = get_cart(request.user.email)
    t_params = {
        "profile": profile,
        "purchases": Purchase.objects.filter(user__email=profile.user.email).order_by("-id"),
        "sells": Sell.objects.filter(user__email=profile.user.email).order_by("-id"),
        "cart": item_cart,
        "total_cart": get_cart_total(item_cart),
    }
    return render(request, "Account/account.html", t_params)


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
            "money": Profile.objects.get(user__email=request.user.email).money
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
