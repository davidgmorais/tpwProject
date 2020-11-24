"""tpwProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path
from app import views

urlpatterns = [
    path('djangoadmin/', admin.site.urls),
    path('', views.home, name="HomePage"),

    path('items/', views.itemList, name="ItemsPage"),
    path('items/<int:id>/', views.item, name="item"),
    path('items/<int:id>/addtocart', views.add_to_cart, name="addToCart"),
    path('items/<int:id>/sell', views.sell_item, name="sellItem"),
    path('items/<slug:slug>/', views.itemListCat, name="ItemsPageCat"),
    path('itemsNew/', views.itemListNew, name="ItemsPageNew"),
    path('itemsPromos/', views.itemListPromos, name="ItemsPagePromos"),

    path('search/', views.search, name="search"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', views.registration, name='registration'),

    path("admin/", views.admin, name="Admin"),
    path("admin/item/", views.manage_items, name="ItemManagement"),
    path("admin/item/<int:item_id>/edit/", views.edit_item, name="EditItem"),
    path("admin/item/<int:item_id>/delete/", views.delete_item, name="DeleteItem"),
    path("admin/item/add/", views.add_item, name="AddItem"),
    # category CRUD
    path("admin/category/", views.manage_category, name="CategoryManagement"),
    path("admin/category/<int:category_id>/edit/", views.edit_category, name="EditCategory"),
    path("admin/category/<int:category_id>/delete/", views.delete_category, name="DeleteCategory"),
    path("admin/category/add/", views.add_category, name="AddCategory"),
    # subcategory CRUD
    path("admin/category/<int:category_id>/edit/<int:subcategory_id>/", views.edit_subcategory, name="EditSC"),
    path("admin/category/<int:category_id>/delete/<int:subcategory_id>/", views.delete_subcategory, name="DeleteSC"),
    path("admin/category/<int:category_id>/add/", views.add_subcategory, name="AddSC"),
    # approve sells
    path("admin/purchases/", views.approve_list, name="ListPurchase"),
    path("admin/purchases/<int:sell_id>/accept", views.approve, name="ApprovePurchase"),
    path("admin/purchases/<int:sell_id>/decline", views.decline, name="DeclinePurchase"),
    path("admin/purchases/<int:sell_id>/", views.purchase_details, name="DetailsPurchase"),
    # account
    path("account/", views.account, name="account"),
    path("account/changepassword", auth_views.PasswordChangeView.as_view(template_name='Account/change_password.html',
                                                                         success_url='/account/'),
         name='ChangePassword'),
    # path("account/transactions"),
    # cart manager
    path("cart/", views.cart, name="cart"),
    path("cart/<int:order_id>/increase", views.increase_cart, name="increase_cart_qty"),
    path("cart/<int:order_id>/decrease", views.decrease_cart, name="decrease_cart_qty"),
    path("cart/<int:order_id>/remove", views.remove_cart, name="remove_from_cart"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)