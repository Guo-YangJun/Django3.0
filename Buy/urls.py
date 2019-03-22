from django.urls import path,re_path
from Buy.views import *
urlpatterns = [
    path('about_myself/',about_myself),
    path('index/',index),
    path('contact_us/',contact_us),
    re_path('all_shop/(\d+)/',all_shop),
    path('shipin/',shipin),
    path('jd/',jd),
    path('login/',login),
    path('logout/',logout),
    path('register/',register),
    path('sendemail/',sendemail),
    path('all_seller/',all_seller),
    re_path('seller_shop/(\d+)/', seller_shop),
    re_path('jump_cart/(\d+)/', jump_cart),
    re_path('shop_detail/(\d+)/', shop_detail),
    re_path('delete/(\d+)/', delete),
    path('cart/', cart),
    path('clear/', clear),
    path('address/', address),
    path('add_address/', add_address),
    re_path('addressDel/(\d+)/', addressDel),
    re_path('addressChange/(\d+)/', addressChange),
    path('payMoney/', payMoney),

]