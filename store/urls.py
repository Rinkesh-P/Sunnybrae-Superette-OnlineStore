from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.product, name='product'),
    path('cart/',views.cart, name='cart'),
    path('faq/',views.faq, name="faq"),
    path('register/',views.user_register, name="register"),
    path('login/',views.user_login, name="login"),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('logout/', views.user_logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name = 'order_confirmation'),
    
]