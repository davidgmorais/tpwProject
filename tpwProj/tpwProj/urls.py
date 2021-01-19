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
    # serializers
    path("api/category/", views.CategoryView.as_view()),
    path("api/category/<int:pk>/", views.CategoryDetailView.as_view()),
    path("api/category/<int:id>/delete/", views.api_delete_category, name="DeleteCategory"),

    path("api/item/", views.ItemView.as_view()),
    path("api/items/new", views.NewItemView.as_view()),
    path("api/items/promo", views.PromoItemView.as_view()),
    path("api/items/category/<str:slug>", views.CategoryItemView.as_view()),
    path("api/item/<int:pk>", views.ItemDetailView.as_view()),
    path("api/item/<int:id>/delete/", views.api_delete_item, name="DeleteItem"),

    path("api/search/<str:query>/", views.ItemSearch.as_view(), name="DeleteItem"),
    path('api/brands', views.brand_list),

    path("api/login", views.Login.as_view()),

    path("api/admin/stats/discount", views.discount_stats_view),
    path("api/admin/stats/category", views.purchased_cat_view),
    path("api/admin/stats/age", views.purchases_age_view),
    path("api/admin/stats/bestbuyers", views.best_buyers_view),
    path("api/admin/outofstock", views.out_of_stock_view),
    path("api/admin/purchases", views.ApproveListView.as_view()),
    path("api/admin/purchases/<int:sell_id>/decline", views.decline_view),
    path("api/admin/purchases/<int:sell_id>/approve", views.approve_view),


    path("api/orderitem/", views.OrderItemView.as_view()),
    path("api/orderitem/<int:pk>", views.OrderItemDetailView.as_view()),
    path("api/orderitem/<int:id>/delete/", views.api_delete_orderitem, name="DeleteOrderItem"),

    path("api/cart/", views.CartView.as_view()),
    path("api/cart/<int:pk>", views.CartDetailView.as_view()),
    path("api/cart/<int:id>/delete/", views.api_delete_cart, name="DeleteCart"),

    path("api/comment/", views.CommentView.as_view()),
    path("api/comment/<int:pk>", views.CommentDetailView.as_view()),
    path("api/comment/<int:id>/delete/", views.api_delete_comment, name="DeleteCart"),

    path("api/purchase/", views.PurchaseView.as_view()),
    path("api/purchase/<int:pk>", views.PurchaseDetailView.as_view()),

    path("api/sell/", views.SellView.as_view()),
    path("api/sell/<int:pk>", views.SellDetailView.as_view()),

    path("api/profiles/", views.ProfileView.as_view(), name="getProfileList"),
    path("api/profiles/<int:_id>/", views.api_get_profile, name="getProfile"),
    path("api/profiles/<int:id>/edit/", views.api_update_profiles, name="EditCategory"),
    path("api/profiles/<int:id>/delete/", views.api_delete_profiles, name="DeleteCategory"),
    path("api/profiles/add/", views.api_create_profiles, name="AddCategory"),


    # old
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
    path("admin/subcategory/add/", views.add_new_subcategory, name='addNewSubcategory'),
    # approve sells
    path("admin/purchases/", views.approve_list, name="ListPurchase"),
    path("admin/purchases/<int:sell_id>/accept/", views.approve, name="ApprovePurchase"),
    path("admin/purchases/<int:sell_id>/decline/", views.decline, name="DeclinePurchase"),
    path("admin/purchases/<int:sell_id>/", views.purchase_details, name="DetailsPurchase"),
    # out of stock items
    path("admin/outofstock/", views.manage_out_of_stock_items, name="OutOfStockItemManagement"),
    path("admin/outofstock/<int:item_id>/", views.edit_out_of_stock_items, name="OutOfStockItemEdit"),
    # account
    path("account/", views.account, name="account"),
    path("account/changepassword/", auth_views.PasswordChangeView.as_view(template_name='Account/change_password.html',
                                                                          success_url='/account/'),
         name='ChangePassword'),
    path("account/delete/", views.delete_account, name='DeleteAccount'),

    path("account/comments/add/", views.account_add_comments, name="addComments"),
    path("account/comments/edit/<int:item_id>/", views.account_edit_comments, name="editComments"),
    path("account/comments/delete/<int:item_id>/", views.account_delete_comment, name="deleteComments"),

    # cart manager
    path("cart/", views.cart, name="cart"),
    path("cart/<int:order_id>/increase/", views.increase_cart, name="increase_cart_qty"),
    path("cart/<int:order_id>/decrease/", views.decrease_cart, name="decrease_cart_qty"),
    path("cart/<int:order_id>/remove/", views.remove_cart, name="remove_from_cart"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
