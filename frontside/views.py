

from logging import exception
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from accountmanage.models import Order, OrderItem, successordermod
from products.models import SubCategory, Categories, Product, Cart, discount,wishlist, Coupon, Couponuser, CategoryOffer
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from accountmanage.models import useraddress, Order, OrderItem
from accountmanage.forms import addressform, addresscheckform
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import razorpay
from django.db.models import Count,Q
from authentications.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from datetime import date
from products.form import couponcheck
# Create your views here.

client = razorpay.Client(auth=("rzp_test_6K5F5F2dkW3hkf", "juLmShGSRr7lHyIOdlYoqlrQ"))




def home(request):
    latest = Product.objects.all().order_by('-created_at')[:8]
    mostpopular = Product.objects.annotate(test = Count('productcount')).order_by('-test')[:8]
    for c in mostpopular:
        print(c.test)
        print(c.product_name)
    context = {
        'latest' : latest,
        'mostpopular' : mostpopular,
    }
    return render(request, 'userside/landingpage.html', context)

@never_cache
def shop(request):
    category = Categories.objects.filter(is_active = True)
    productss = Product.objects.filter(is_active = True)
    p = Paginator(Product.objects.all(),9)
    page = request.GET.get('page')
    pproduct = p.get_page(page)
    test = {
        'category':category,
        'productss':productss,
        'pproduct' : pproduct
        }
    return render(request, 'userside/shop.html', test)




def shopcat(request,cat_slug):
    category = Categories.objects.filter(is_active = True)
    # singlecategory = Categories.objects.get(url_slug = cat_slug)
    productss = Product.objects.filter(categories_id__url_slug__contains = cat_slug)
    p = Paginator(productss,3)
    page = request.GET.get('page')
    pproduct = p.get_page(page)
    test = {
        'category' : category,
        'productss': productss,
        'pproduct' : pproduct,
        # 'singlecategory' : singlecategory
    }
    return render(request, 'userside/shop.html', test)

def shopsubcat(request,cat_slug, subcat_slug):
    category = Categories.objects.filter(is_active = True)
    # singlecategory = Categories.objects.get(url_slug = cat_slug)
    productss = Product.objects.filter(categories_id__url_slug__contains = cat_slug, subcategories_id__url_slug__contains = subcat_slug)
    p = Paginator(productss,3)
    page = request.GET.get('page')
    pproduct = p.get_page(page)
    test = {
        'category' : category,
        'productss': productss,
        'pproduct' : pproduct,
        # 'singlecategory' : singlecategory
    }
    return render(request, 'userside/shop.html', test)



# class SingleProView(DetailView):
#     model = Product
#     template_name = 'userside/productview.html'

@never_cache
def SingleProView(request,cat_slug, subcat_slug, pro_slug):
    product = Product.objects.filter(url_slug = pro_slug, subcategories_id__url_slug = subcat_slug)
    testvalue = 0
    try:
        item = Cart.objects.get(user = request.user.id, product__url_slug = pro_slug)
        testvalue = 1
    except Exception as e:
        print(e)
        pass
    try:
        item = Cart.objects.get(session_id = _cart_id(request), product__url_slug = pro_slug)
        testvalue = 1
    except:
        pass
    tests = {
        'product' : product,
        'testvalue' : testvalue
    }
    return render(request, 'userside/productpage.html', tests)

def _cart_id(request):
    cartses = request.session.session_key

    if not cartses:
        cartses = request.session.create()
    return cartses


def AddToCart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=product_id)
            if(product_check):
                if(Cart.objects.filter(user = request.user.id, product = product_id)):
                    return JsonResponse({"Status" : "Product already in cart"})

                else:
                    prod_qty = int(request.POST.get('product_qty'))
            
                    if product_check.in_stock_total >= prod_qty : 
                        Cart.objects.create(user = request.user, product = product_check, product_qty = prod_qty)
                        return JsonResponse({"Status" : "product added succesfully"})
                    
                    else : 
                        return JsonResponse({"Status" : "Only" +  str(product_check.in_stock_total) + " quantity available"})

            else:
                return JsonResponse({"Status" : "No product exist"})


                
            
        else:
            product_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=product_id)

            if(product_check):
                if(Cart.objects.filter(session_id = _cart_id(request) , product = product_id)):
                    return JsonResponse({"Status" : "Product already in cart"})

                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.in_stock_total >= prod_qty : 


                        try:
                            Cart.objects.get(session_id = _cart_id(request), product = product_id )
                        except Cart.DoesNotExist:
                            Cart.objects.create(
                                product = product_check,
                                product_qty = prod_qty,
                                session_id = _cart_id(request)
                            )
                        return JsonResponse({"Status" : "product added succesfully"})

            return JsonResponse({"Status" : "Login to continue"})


    return redirect('/')

def calcprice(qty, price):
    return int(qty) * int(price)




def cart(request):
    
    try:
        cart = Cart.objects.filter(user=request.user).order_by('created_at')
    except:
        cart = Cart.objects.filter(session_id = _cart_id(request)).order_by('created_at')
    context = {'cart' : cart}
    return render(request,'userside/carttest.html', context)

def updateCart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        try:
            (Cart.objects.filter(user = request.user, product_id = prod_id))
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id =  prod_id, user = request.user)
            cart.product_qty = prod_qty
            cart.save()
            qty_now = cart.product_qty
            price = Product.objects.get(id = prod_id)
            print(price)
            pricec = price.product_max_price
            npricere = calcprice(qty_now, pricec)
            try:
                disc = discount.objects.get(product_id = prod_id)
                discp = disc.disc_percent
                dpricere = calcprice(qty_now, discp)
            except:
                dpricere = npricere
            print(dpricere)
            return JsonResponse({
                "Status" : "Updated Succesfully",
                'npricere' : npricere,
                'dpricere' : dpricere
                })
        except:
            (Cart.objects.filter(session_id = _cart_id(request), product_id = prod_id))
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id =  prod_id, session_id = _cart_id(request) )
            cart.product_qty = prod_qty
            cart.save()
            qty_now = cart.product_qty
            price = Product.objects.get(id = prod_id)
            print(price)
            pricec = price.product_max_price
            npricere = calcprice(qty_now, pricec)
            try:
                disc = discount.objects.get(product_id = prod_id)
                discp = disc.disc_percent
                dpricere = calcprice(qty_now, discp)
            except:
                dpricere = npricere
            print(dpricere)
            return JsonResponse({
                "Status" : "Updated Succesfully",
                'npricere' : npricere,
                'dpricere' : dpricere
                })
    return redirect('/')



def deleteCartItem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user = request.user, product_id = prod_id)):
            cartitem = Cart.objects.get(product_id = prod_id, user = request.user)
            cartitem.delete()
        return JsonResponse({"Status" : "Deleted Succesfully"})
    return redirect('/')

@login_required(login_url='login')
def checkout(request):
    if request.method == "POST":
        code = request.POST.get('code')
        # print(code)
        try:
            today = date.today()
            value = Coupon.objects.get(code = code)
            if not value.valid_from <= today and value.valid_to >= today:
                print("test")
                return JsonResponse({"Status" : "Coupon is not valid currently"})
                
            print(value.offer_value)
            try:
                print('helloda entharo ayi')
                test = Couponuser.objects.filter(user = request.user).exists()
                print(test)
                if test:
                    print("test")
                    current1 = Couponuser.objects.get(user = request.user)
                    if current1.coupon_code != code:
                        print("ivide ethiyo")
                        current1.coupon_code = code
                        current1.coupon_value = value.offer_value
                        current1.coupon_modal = value
                        current1.save()
                        return JsonResponse({"Status" : "Coupon changed"})
                    return JsonResponse({"Status" : "Coupon already eneterd"})

                Couponuser.objects.create(
                    user = request.user,
                    coupon_modal = value,
                    coupon_code = code,
                    coupon_value = value.offer_value   
                )
            except Exception as e:
                print("entho")
                print(e)
                pass
            return JsonResponse({"Status" : "Coupon Activated"})

        except:
            return JsonResponse({"Status" : "invalid coupon"})




    addr = useraddress.objects.filter(user_id = request.user)
    # addrtop = useraddress.objects.filter(user_id = request.user).order_by('-created_at')
    rawcart = Cart.objects.filter(user = request.user)
    for item in rawcart:
        if item.product_qty > item.product.in_stock_total:
            del_item = Cart.objects.get(id = item.id)
            del_item.delete()
    
    cartitems = Cart.objects.filter(user = request.user)
    total_price = 0
    disc_prices = 0
    for item in cartitems:
        total_price = item.total_price() + total_price
        disc_prices = item.best_offer() + disc_prices
    print(total_price)
    
    try:
        coup_value = Couponuser.objects.get(user = request.user)
        coupon_status = True
        coup_perc = coup_value.coupon_value
        coupon_codes = coup_value.coupon_code

    except Exception as e:
        coupon_codes = None
        coupon_status = False
        coup_perc = 0

    discount_red = total_price - disc_prices

    #  str(round(answer, 2))
    final_price  = int(disc_prices - disc_prices * int(coup_perc)/100)
    coup_red = disc_prices - final_price

    context = {
        'cartitems' : cartitems, 
        'total_price' : total_price,
        'disc_prices' : disc_prices,
        'discount_red' : discount_red,
        'addr' : addr,
        'final_price' : final_price,
        'coupon_status' : coupon_status,
        'coup_red' : coup_red,
        'coupon_codes' : coupon_codes,
        'coup_perc' : coup_perc
    }
    
    return render(request,'userside/checkout.html', context )

def checkout_address(request, id):
    address = useraddress.objects.get(id=id)
    context = {
        'address' : address
    }
    return render(request, 'userside/checkoutaddr.html', context)


@login_required
def placeorder(request):
    
    if request.method == 'POST':
        form = addresscheckform(request.POST)
        if form.is_valid():
            neworder = Order()
            neworder.user_id = request.user
            neworder.name = request.POST.get('name')
            neworder.email = request.POST.get('email')
            neworder.mobile = request.POST.get('mobile')
            neworder.address_1 = request.POST.get('address_1')
            neworder.address_2 = request.POST.get('address_2')
            neworder.city = request.POST.get('city')
            neworder.district = request.POST.get('district')
            neworder.state = request.POST.get('state')
            neworder.pincode = request.POST.get('pincode')

            neworder.payment_mode = request.POST.get('payment_mode')
            neworder.payment_id = request.POST.get('payment_id')


            cartitems = Cart.objects.filter(user = request.user)
            total_price = 0
            disc_prices = 0
            for item in cartitems:
                for item in cartitems:
                    total_price = item.total_price() + total_price
                    disc_prices = item.best_offer() + disc_prices
            
            try:
                coup_value = Couponuser.objects.get(user = request.user)
                coupon_status = True
                coup_perc = coup_value.coupon_value
                coupon_codes = coup_value.coupon_code

            except Exception as e:
                coupon_codes = None
                coupon_status = False
                coup_perc = 0

            discount_red = total_price - disc_prices
            final_price  = int(disc_prices - disc_prices * int(coup_perc)/100)
            coup_red = disc_prices - final_price
            neworder.total_price = final_price
            neworder.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            tracking_no = current_date + str(neworder.id)
            neworder.tracking_no = tracking_no
            neworder.save()
            
            neworderitems = Cart.objects.filter(user = request.user)
            for item in neworderitems:
                OrderItem.objects.create(
                    order_id =  neworder,
                    product_id = item.product,
                    price = item.product.product_max_price,
                    quantity = item.product_qty
                )

                orderproduct = Product.objects.filter(id=item.product_id).first()
                orderproduct.in_stock_total = orderproduct.in_stock_total - item.product_qty
                orderproduct.save()

            successordermod.objects.create(
                order_id = neworder.tracking_no
            )
            Cart.objects.filter(user = request.user).delete()
            Couponuser.objects.filter(user = request.user).delete()
            messages.success(request,'test work')

            paymode = request.POST.get('payment_mode')
            if paymode == "Paid by Razerpay":
                print("hello")
                return JsonResponse({"status" : "jtest work" , "trackno" : tracking_no})
            if paymode == "Paid by PayPal":
                print("hello")
                return JsonResponse({"status" : "paypal test work", "trackno" : tracking_no})
            if paymode == "COD":
                print("work ayennu thonunnu")
                return JsonResponse({"status" : "cod test work", "trackno" : tracking_no})
            return redirect('ordersuccess')
        else:
            print(form.errors.as_data())
    messages.success(request,'test didnot  works')
    return redirect('shop')



def success_order(request):
    order_number = request.GET.get('order_number')
    test =  successordermod.objects.get(order_id = order_number,)
    print(test)
    # transID = request.GET.get('payment_id')
    print("ivide ethiyo")
    try:
        test =  successordermod.objects.get(order_id = order_number, status = False)
        test.status = True
        test.save()
        order = Order.objects.get(tracking_no = order_number)
        items = OrderItem.objects.filter(order_id = order.id)
        print("what happended")
        context = {
            # "status" : order_number
            'obj' : order,
            'items' : items
        }
        return render(request, 'userside/ordersuccess.html', context)
    except Exception as e: 
        print(e)
        return redirect('home') 

def successpage(request):
    order = Order.objects.filter(user_id = request.user).order_by('-created_at')[:1]
    ordert = Order.objects.filter(user_id = request.user).last()
    items = OrderItem.objects.filter(order_id = ordert.id)
    print(order)
    context = {
        'order' : order,
        'items' : items
    }
    return render(request, 'userside/ordersuccess.html', context)
    





def testsubmit(request):
    if request.method == 'POST':
        return redirect('shop')



def wish_list(request):
    pass


def razorpay(request):
    cartitems = Cart.objects.filter(user = request.user)
    total_price = 0
    disc_prices = 0
    for item in cartitems:
        try:
            disc_pr = discount.objects.get(product_id = item.product_id)
            disc_prices = disc_prices + int(item.product_qty) * int(item.product.product_max_price) * (1 - int(disc_pr.disc_percent)/100)
        except:
            disc_prices = disc_prices + int(item.product_qty) * int(item.product.product_max_price)
            total_price = total_price + int(item.product.product_max_price) * int(item.product_qty)
    DATA = {
        "amount": 1000,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }
    client1 = client.order.create(data=DATA)
    print(client1)
    return JsonResponse({
        'total_price' : disc_prices,
        'client' : client1
    })





def checkoutaddaddr(request):
    if request.method == "POST":
        form = addressform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "update succesful")
            return  redirect('checkout')
        else:
            print(form.errors.as_data())
            messages.error(request,"you are a FAILURE!!")
    data = Account.objects.filter(email = request.user)
    context = {
        'data' : data
    }
    return render(request,'userside/addcheckoutaddr.html', context)
    


def cancelorder(request, id):
    if request.method == "POST":
        current_order = Order.objects.get(id = id)
        print("podare")
        if current_order.status != ("Order cancelled" or "Returned" or "Out for Delivery"):
            current_order.status = "Order cancelled"
            print("poda")
            current_order.save()
    return redirect('accountmanage:userorderhistory')

def returnorder(request,id):
    if request.method == "POST":
        current_order = Order.objects.get(id = id)
        current_order.status = "Returned"
        current_order.save()
    return redirect('accountmanage:userorderhistory')
    
        






















def testing(request):
    d = date(2022,9,9)
    print(d)
    f = date.today()

    if request.method == "POST":
        test = request.POST.get('key')
        product = Product.objects.filter(Q(product_name__icontains = test) | Q(brand__icontains = test))
        context = {
            "product": product
        }
        return render(request, 'userside/test.html', context)

    product = Product.objects.all()
    print(product)
    coup = Coupon.objects.filter(valid_to__gt = f)
    coup1 = Coupon.objects.get(code = "testing")
    print(coup1.valid_from)
    if not coup1.valid_from <= f and coup1.valid_to >= f:
        print("work aya")
    if coup:
        print("poda")
    for c in coup:
        print(c.valid_to)
    context = {
        'product' : product
    }
    return render(request, 'userside/test.html', context)