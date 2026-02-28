from django.urls import path
from .views import home,login,registration,contact,about,product,change,forget,logout_view,myprofile_view,oldpass_view,product_detail,product,add_to_cart,remove_cart_item,decrease_quantity,increase_quantity,view_cart,checkout_view,address_view,delete_address,payment_succes_view,order_detail_view


urlpatterns = [
    path('', home, name='home'), 
    path('home/', home, name='home'), 
    path('product/', product, name='product'), 
    path('login/', login, name='login'), 
    path('logout/', logout_view, name='logout'), 
    path('register/', registration, name='registration'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('change/', change, name='change'),
    path('forget/',forget, name='forget'),
    path('myprofile/',myprofile_view, name='myprofile'),
    path('oldpass/',oldpass_view, name='oldpass'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/',view_cart, name='view_cart'),
    path('remove_cart_item/<int:pk>/', remove_cart_item, name='remove_cart_item'),
    path('decrease_quantity/<int:pk>/', decrease_quantity, name='decrease_quantity'),
    path('increase_quantity/<int:pk>/', increase_quantity, name='increase_quantity'),
    path('checkout/<int:pk>/', checkout_view, name='checkout'),
    path('checkout/', checkout_view, name='checkout'),
    path('address/', address_view, name='address'),
    path('delete_address/<int:pk>/', delete_address, name='delete_address'),
    path('payment_success/', payment_succes_view, name='payment_success'),
    path('order_detail/', order_detail_view, name='order_detail'),
    
    
   
]