from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    # path('shop/subcat/<int:id>', views.shopcat, name='shopcat'),
    path('shop/<slug:cat_slug>/', views.shopcat, name='shopcat'),
    path('shop/<slug:cat_slug>/<slug:subcat_slug>', views.shopsubcat, name='shopsubcat'),
    path('addtocart/<int:id>', views.AddToCart, name='addtocart'),
    # path('<slug:url_slug>/', views.SingleProView, name='productview'),
    path('<slug:cat_slug>/<slug:subcat_slug>/<slug:pro_slug>', views.SingleProView, name='productview'),

    path('cart/',views.cart,name='cart'),
    path('add-to-cart',views.AddToCart,name='addtocart'),
    path('update-cart', views.updateCart, name='updatecart'),
    path('delete-cart-item', views.deleteCartItem, name='deleteCartItem'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkoutaddress/<int:id>', views.checkout_address, name='checkoutaddress'),
    path('checkout/add_address',  views.checkoutaddaddr, name='add_checkout_addr'),
    path('wishlist', views.wish_list, name='wish_list'),
    path('place-order', views.placeorder, name='placeorder'),
    path('proceed-to-pay', views.razorpay, name = 'razorpaycheck'),
    path('ordersuccess', views.successpage, name='ordersuccess'),
    path('add-address', views.checkoutaddaddr, name='checkoutaddaddr'),
    path('cancel_order/<int:id>', views.cancelorder, name='cancel_order'),
    path('return_order/<int:id>', views.returnorder, name='return_order'),


    path('testing',views.testing, name='testing'),
]