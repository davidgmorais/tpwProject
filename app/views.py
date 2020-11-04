from django.db.models import QuerySet, When, Case, Value, CharField, Avg, Count
from django.db.models.functions import Extract
from django.shortcuts import render
from django.http import HttpResponse
from app.models import Category, SubCategory, Item, User, Purchase
from datetime import datetime, timedelta


def get_items():
    return Item.objects.all()


def get_promos():
    return Item.objects.filter(discount__gt=0)


def get_new_items(day_range=14):
    return Item.objects.filter(insertDate__range=[
        datetime.today() - timedelta(days=day_range),
        datetime.today()
    ])


def get_top_promo():
    promos = Item.objects.filter(discount__gt=0).order_by('-discount')
    if len(promos) > 0:
        return promos[0]


def get_bestsellers(top=10):
    if top < 1:
        return None
    return Item.objects.all().order_by("-quantity")[:top]


def get_categories():
    category_dic = dict()
    categories = Category.objects.all()
    for c in categories:
        subcategories = SubCategory.objects.filter(category_id=c.id)
        category_dic[c] = subcategories
    return category_dic


def filer_by_category(query, category_id, subcategory_id=None):
    if not isinstance(query, QuerySet):
        return None
    if subcategory_id is None:
        query = query.filter(category__id=category_id)
    else:
        query = query.filter(category__id=category_id, sub_category__id=subcategory_id)
    return query


def filter_by_price(query, max_price=None, min_price=0):
    if not isinstance(query, QuerySet):
        return None

    if max_price is None:
        query = query.filter(price__gte=min_price)
    else:
        query = query.filter(price__range=[min_price, max_price])
    return query


def filter_by_brand(query, brand):
    if not isinstance(query, QuerySet):
        return None
    return query.filter(brand__exact=brand)


def filter_by_availability(query):
    if not isinstance(query, QuerySet):
        return None
    return query.filter(quantity__gt=0)


def filter_by_discount(query):
    if not isinstance(query, QuerySet):
        return None
    return query.filter(discount__gt=0)


def filter_by_reviews(query, stars):
    return Item.objects.annotate(comment_avg=Avg('comment__stars')).filter(comment_avg__gte=stars)


def search(search_term):
    return Item.objects.filter(name__contains=search_term)


# categories with more purchased associated
def most_purchased_cat(top=1):
    categories = Category.objects.values('name').annotate(purchases=Count('item__purchase')).order_by('-purchases')
    if len(categories) >= top:
        return categories[:top]


# categories with less purchased associated
def less_purchased_cat(top=1):
    categories = Category.objects.values('name').annotate(purchases=Count('item__purchase')).order_by('purchases')
    if len(categories) >= top:
        return categories[:top]


# users with more purchases
def best_buyers(top=1):
    users = User.objects.annotate(purchases=Count('purchase'))
    if len(users) >= top:
        return users[:top]


# users with more sells
def best_sellers(top=1):
    users = User.objects.annotate(sells=Count('sell'))
    if len(users) >= top:
        return users[:top]


# number of purchases per age group
def purchases_age():
    age_groups = User.objects.annotate(Age=Extract('birthdate', 'year') - datetime.today().year,
                                       AgeGroup=Case(When(Age__gte=65, then=Value('over 65')),
                                                     When(Age__lt=18, then=Value('under 18')),
                                                     When(Age__range=[18, 40], then=Value('18-40')),
                                                     When(Age__range=[41, 65], then=Value('41-65')),
                                                     output_field=CharField()),
                                       purchases=Count('purchase__item')
                                       ).values('AgeGroup', 'purchases')
    return age_groups


# ratio between discounted and full price purchases
def discount_stats():
    return Purchase.objects.aggregate(Discounted=Count(Case(When(discountedP=True, then=Value(1)))),
                                      FullPrice=Count(Case(When(discountedP=False, then=Value(1)))))


# Create your views here.
def home_page(request):
    # list categories and subcategories
    category_dic = get_categories()

    # TODO: delete this
    # show categories on site
    template = "<ul>"
    for c in category_dic.keys():
        template = template + "<li>" + str(c.id) + " ->" + c.name + "</li>" + "<ul>"
        for sc in category_dic[c]:
            template = template + "<li>" + str(sc.id) + " ->" + sc.name + "</li>"
        template = template + "</ul>"
    template = template + "</ul>"

    # list all items
    items = get_items()
    print("Items: ", items)

    # list items with discount
    promos = get_promos()
    print("Discounted: ", promos)

    # list new items
    new_in = get_new_items(day_range=7)
    print("What's new: ", new_in)

    # list top promotion of the day
    top_promo = get_top_promo()
    print("Top promo of the day: ", top_promo)

    # list best sellers
    best_selling_items = get_bestsellers(top=2)
    print("Top 2 product(s): ", best_selling_items)

    return HttpResponse(template)
