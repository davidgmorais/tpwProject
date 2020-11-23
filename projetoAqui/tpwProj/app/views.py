from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.models import Category, Item, Comment, Profile, Purchase, Sell, Cart
from app.forms import Search, SignUpForm, Filters, ItemForm, CategoryForm, SubcategoryForm
from django.db.models import Q
from django.contrib.auth import login, authenticate
from datetime import datetime, timedelta
from json import dumps
from django.contrib.auth.models import User
from django.db.models import When, Case, Value, CharField, Avg, Count, Sum, F, FloatField
from django.db.models.functions import Extract


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


def catSB(request):
    return render(request, 'catSB.html', {'categories': Category.objects.all(), 'items': Item.objects.all()})


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

    tparams = {
        'items': Item.objects.all(),
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
    item = Item.objects.get(id)
    if Cart.objects.get(user=request.user):
        cart = Cart.objects.get(user=request.user)
        cartItems = cart.item | item
        cart = Cart(item=cartItems, user=request.user)
        print(cartItems)
#         cart =
#     order_item, created = Cart.objects.get_or_create(
#         item=item,
#         user=request.user,
#         qty=1,
#     )
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item.quantity += 1
#             order_item.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("core:order-summary")
#         else:
#             order.items.add(order_item)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("core:order-summary")
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(
#             user=request.user, ordered_date=ordered_date)
#         order.items.add(order_item)
#         messages.info(request, "This item was added to your cart.")
#         return redirect("core:order-summary")
#
#
# @login_required
# def remove_from_cart(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item = OrderItem.objects.filter(
#                 item=item,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             order.items.remove(order_item)
#             order_item.delete()
#             messages.info(request, "This item was removed from your cart.")
#             return redirect("core:order-summary")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("core:product", slug=slug)
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("core:product", slug=slug)
#

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
    c = Cart.objects.filter(user__email=email)
    return c


def get_cart_total(cart_items):
    return cart_items.aggregate(price=Sum((F('item__price') * (100 - F('item__discount')) / 100) * F('qty'),
                                          output_field=FloatField()))['price']

#
# def filer_by_category(query, category_id, subcategory_id=None):
#     if not isinstance(query, QuerySet):
#         return None
#     if subcategory_id is None:
#         query = query.filter(category__id=category_id)
#     else:
#         query = query.filter(category__id=category_id, sub_category__id=subcategory_id)
#     return query
#
#
# def filter_by_price(query, max_price=None, min_price=0):
#     if not isinstance(query, QuerySet):
#         return None
#
#     if max_price is None:
#         query = query.filter(price__gte=min_price)
#     else:
#         query = query.filter(price__range=[min_price, max_price])
#     return query
#
#
# def filter_by_brand(query, brand):
#     if not isinstance(query, QuerySet):
#         return None
#     return query.filter(brand__exact=brand)
#
#
# def filter_by_availability(query):
#     if not isinstance(query, QuerySet):
#         return None
#     return query.filter(quantity__gt=0)
#
#
# def filter_by_discount(query):
#     if not isinstance(query, QuerySet):
#         return None
#     return query.filter(discount__gt=0)
#
#
# def filter_by_reviews(query, stars):
#     return Item.objects.annotate(comment_avg=Avg('comment__stars')).filter(comment_avg__gte=stars)
#
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
        form = ItemForm(request.POST)
        if form.is_valid():
            item = Item.objects.get(id=item_id)
            item.name = form.cleaned_data["name"]
            item.description = form.cleaned_data["description"]
            item.price = form.cleaned_data["price"]
            item.quantity = form.cleaned_data["quantity"]
            item.brand = form.cleaned_data["brand"]
            item.category.set([int(c) for c in form.cleaned_data["category"]])
            item.discount = form.cleaned_data["discount"]
            item.save()
            return redirect("/admin/item")
    else:
        item = Item.objects.get(id=item_id)
        form = ItemForm(initial={"name": item.name,
                                 "description": item.description,
                                 "price": item.price,
                                 "brand": item.brand,
                                 "quantity": item.quantity,
                                 "category": [c.id for c in item.category.all()],
                                 "discount": item.discount
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
        form = ItemForm(request.POST)
        if form.is_valid():
            item = Item(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price=form.cleaned_data["price"],
                quantity=form.cleaned_data["quantity"],
                brand=form.cleaned_data["brand"],
                insertDate=datetime.today(),
                discount=form.cleaned_data["discount"]
            )
            item.save()
            item.category.set([int(sc) for sc in form.cleaned_data["category"]])
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
        return redirect("../../edit/")
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
        return redirect("../../")
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
            return redirect("/admin/category/")
    else:
        form = CategoryForm()
    return render(request, "AdminTemplates/add_edit.html", {"form": form, "action": "add", "type": "category"})


def approve_list(request):
    purchases = Sell.objects.all()
    return render(request, "AdminTemplates/approve_purchase.html", {"purchases": purchases})


def approve(request, sell_id):
    sell = Sell.objects.get(id=sell_id)
    sell.pendingSell = False
    sell.save()

    item = Item.objects.get(id=sell.item.id)
    item.quantity += 1
    item.save()

    profile = Profile.objects.get(user__email=sell.user.email)
    profile.money += sell.moneyReceived
    profile.save()
    return redirect("/admin/purchases")


def decline(request, sell_id):
    Sell.objects.get(id=sell_id).delete()
    return redirect("/admin/purchases")


def purchase_details(request, sell_id):
    sell = Sell.objects.get(id=sell_id)
    profit = sell.moneyReceived - sell.item.price
    return render(request, "AdminTemplates/purchase_details.html", {"details": sell, "profit": profit})


def account(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    profile = Profile.objects.get(user__email=request.user.email)
    item_cart= get_cart(request.user.email)
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
    item_cart = get_cart(request.user.email)
    t_parent = {
        "cart": item_cart,
        "total_cart": get_cart_total(item_cart),
        "money": Profile.objects.get(user__email=request.user.email).money
    }
    return render(request, "Cart/cart.html", t_parent)


def increase_cart(request, cart_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    c = Cart.objects.get(id=cart_id)
    if c.qty < c.item.quantity:
        c.qty += 1
        c.save()
    return redirect("/cart")


def decrease_cart(request, cart_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    c = Cart.objects.get(id=cart_id)
    if c.qty > 1:
        c.qty -= 1
        c.save()
    return redirect("/cart")


def remove_cart(request, cart_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    c = Cart.objects.get(id=cart_id)
    c.delete()
    return redirect("/cart")


def finalize_cart(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    c = get_cart(email=request.user.email)
    for item in c:
        if item.item.discount != 0:
            price = item.item.price * item.item.discount / 100
            discounted = True
        else:
            price = item.item.price
            discounted = False

        p = Purchase(
            item=item.item,
            user=request.user,
            price=price,
            discountedP=discounted
        )
        p.save()
        c.delete()
        return redirect("/")
