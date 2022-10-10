from products.models import *
from .views import _cart_id

def menulinks(request):
    links = Product.objects.all ()
    return dict(links = links)


# def cartcount(request):
    
#     try:
#         rawcart = Cart.objects.filter(user = request.user)
#         count = 0
#         for item in rawcart:
#             count = count + 1*int(item.product_qty)
        
#         return dict(count = count)
#     except:
#         count = 0
#         return dict(count = count)

# def cartcount(request):

#     try:
#         cart =  Cart.objects.filter(session_id = _cart_id(request))
#         if request.user.is_authenticated:
#             rawcart = Cart.objects.filter(user = request.user)
#             count = 0
#         else:
#             rawcart = Cart.objects.filter(user = request.user)

#             for item in rawcart:
#                 count = count + 1*int(item.product_qty)
        
#             return dict(count = count)
        
#     except:
#         pass

def cartcount(request):
    
    try:
        rawcart = Cart.objects.filter(user = request.user)
        count = 0
        for item in rawcart:
            count = count + 1*int(item.product_qty)
        
        return dict(count = count)
    except:
        rawcart = Cart.objects.filter(session_id = _cart_id(request))
        count = 0
        for item in rawcart:
            count = count + 1*int(item.product_qty)
        return dict(count = count)