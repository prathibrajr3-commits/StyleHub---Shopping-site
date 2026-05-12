from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<str:order_number>/', views.order_success, name='order_success'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    # Cart API
    path('api/cart/add/', views.cart_add, name='cart_add'),
    path('api/cart/update/', views.cart_update, name='cart_update'),
    path('api/cart/remove/', views.cart_remove, name='cart_remove'),

    # Newsletter API
    path('api/newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
