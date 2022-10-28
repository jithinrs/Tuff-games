from datetime import date, datetime, timedelta
import email
from unicodedata import name
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout,login


from django.utils import timezone

from django.db.models import Sum, Q
from authentications.models import Account
from .models import Categories, CategoryOffer, Product, Specification, SubCategory,Coupon, discount
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpResponse
from django.contrib import messages
from .form import *
from accountmanage.models import Order, OrderItem
from accountmanage.forms import newstatus
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from authentications.form import UserForm 

from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
#custom decorator

class adminrequiredmixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return render(request, '404error.html')
        if not request.user.is_authenticated:
            return redirect('adminlogin')
        elif not request.user.is_admin:
            return redirect('adminlogin')
        return super(adminrequiredmixin, self).dispatch(request, *args, **kwargs)



def admin_login(request):
    if request.user.is_authenticated:
        return redirect('adminbase')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email, is_admin = True)
        except :
            messages.error(request,"user Does not exist..")
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('adminbase') 
    
    return render(request, 'adminside/adminlogin.html')

def adminlogout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('adminlogin')
    return HttpResponse('<h1>404</h1>')


class Categorylist(adminrequiredmixin, ListView):
    model = Categories
    template_name = 'adminside/categorylist.html'
    paginate_by = 7

    def get_queryset(self):
        key = self.request.GET.get('key')
        print(key)
        object_list = self.model.objects.all().order_by('title')
        if key:
            object_list = object_list.filter(title__icontains = key)
        return object_list


class Categoryadd(adminrequiredmixin, SuccessMessageMixin, CreateView):
    # model = Categories
    form_class = Categoryform
    success_message = 'Category Added'
    # fields = "__all__"
    template_name = "adminside/categoryadd.html"


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['Subcategory'].queryset = SubCategory.objects.none()

    # def post(self, request, *args, **kwargs):
    #     self.title = self.title.title()
    #     return super(Categoryadd, self).post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance.title = self.title.title()
    #     return super(Categoryadd, self).form_valid(form)

    
    

class Categoryupdate(adminrequiredmixin ,SuccessMessageMixin, UpdateView):
    model = Categories
    form_class = Categoryform
    success_message = 'Category Updated'
    # fields = "__all__"
    template_name = "adminside/categoryupdate.html"

class SubCategorylist(adminrequiredmixin,ListView):
    model = SubCategory
    template_name = 'adminside/subcategorylist.html'
    

    def get_queryset(self):
        # test1 = SubCategory.objects.filter(category_id = slug).values()
        return super().get_queryset().filter(category_id=self.kwargs['id'])

class SubCategoryFullList(adminrequiredmixin,ListView):
    model = SubCategory
    template_name = 'adminside/subcategoryfulllist.html'
    paginate_by = 10

    def get_queryset(self):
        key = self.request.GET.get('key')
        print(key)
        object_list = self.model.objects.all().order_by('title')
        if key:
            object_list = object_list.filter(title__icontains = key)
        return object_list

class SubCategoryadd(adminrequiredmixin ,SuccessMessageMixin, CreateView):
    model = SubCategory
    success_message = 'Category Added'
    fields = "__all__"
    template_name = "adminside/subcategoryadd.html"

class SubCategoryupdate(adminrequiredmixin, SuccessMessageMixin, UpdateView):
    model = SubCategory
    success_message = 'Sub Category Updated'
    fields = "__all__"
    template_name = "adminside/subcategoryupdate.html"


class Productlist(adminrequiredmixin, ListView):
    model = Product
    template_name = 'adminside/productlist.html'
    paginate_by = 10

    def get_queryset(self):
        key = self.request.GET.get('key')
        print(key)
        object_list = self.model.objects.all().order_by('created_at')
        if key:
            object_list = object_list.filter(product_name__icontains = key)
        return object_list

class Productadd(adminrequiredmixin, SuccessMessageMixin, CreateView):
    # model = Product
    form_class = productform
    success_message = 'Product Added'
    # fields = "__all__"
    template_name = "adminside/productadd.html"


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['subcategories_id'].queryset = SubCategory.objects.none()

class Productupdate(adminrequiredmixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = productform
    success_message = 'Product Updated'
    # fields = "__all__"
    template_name = "adminside/productUpdate.html"

class Productspec(adminrequiredmixin, SuccessMessageMixin,CreateView):
    model = Specification
    success_message: str = "Specification added"
    fields = "__all__"
    template_name = "adminside/productspec.html"

@staff_member_required(login_url='adminlogin')
def userdisplay(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            user = Account.objects.filter(is_superadmin = False, email__icontains = key).order_by('first_name')
        else:
            return redirect('user_display')
    else:    
        user = Account.objects.filter(is_superadmin = False).order_by('first_name')
    p = Paginator(user,10)
    page = request.GET.get('page')
    user = p.get_page(page)
    context = {
        'user' : user,
    }

    return render(request, 'adminside/userlist.html', context)

@staff_member_required(login_url='adminlogin')
def SingleProduct(request,cat_slug, subcat_slug, pro_slug):
    product = Product.objects.filter(url_slug = pro_slug, subcategories_id__url_slug = subcat_slug)
    tests = {
        'product' : product
    }
    return render(request, 'adminside/productpage.html', tests)

@staff_member_required(login_url='adminlogin')
def category_delete(request, id):
    if request.method == 'POST':
        category_id = Categories.objects.get(pk=id)
        name = Categories.objects.filter(id=id).values('title')
        print(name)
        messages.success(request, f" {name[0]['title']} category is deleted")
        category_id.delete()
        return redirect('categorylist')

@staff_member_required(login_url='adminlogin')
def subcategory_delete(request, id):
    if request.method == 'POST':
        subcategory_id = SubCategory.objects.get(pk=id)
        subcategory_id.delete()
        return redirect('categorylist')

@staff_member_required(login_url='adminlogin')
def product_delete(request, id):
    if request.method == 'POST':
        product_id = Product.objects.get(pk=id)
       
        product_id.delete()
        return redirect('productlist')

@staff_member_required(login_url='adminlogin')
def adminbase(request):
    order = Order.objects.all().filter().order_by('-created_at')[:10]

    mostpopular = Product.objects.annotate(test = Count('productcount')).order_by('-test')[:4]
    count = []
    name = []
    for mo in mostpopular:
        x = mo.test
        count.append(x)
        y = mo.product_name
        name.append(y)

    count1 = count[0]
    count2 = count[1]
    count3 = count[2]
    count4 = count[3]

    name1 = name[0]
    name2 = name[1]
    name3 = name[2]
    name4 = name[3]

    cod = Order.objects.filter(payment_mode = "COD").count()
    razor = Order.objects.filter(payment_mode = "Paid by Razerpay").count()
    paypal = Order.objects.filter(payment_mode = "Paid by PayPal").count()

    total_products = Product.objects.all().count()
    total_users = Account.objects.all().count()

    revenue = Order.objects.all().aggregate(Sum('total_price'))
    total_revenue = revenue['total_price__sum']
    total_orders = Order.objects.all().count()

    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")

   

    f = date(2022,9,6)

    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month).count() 
    order_count_in_day =Order.objects.filter(created_at__contains = today).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week).count()

    print(today, today_date)
    print(one_week)


    today_sale = Order.objects.filter(created_at__date = today_date).count()
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at__date = new_date).count()  
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at__date = new_date).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    print(new_date)
    day_3 = Order.objects.filter(created_at__date = new_date).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at__date = new_date).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at__date = new_date).count()
    day_5_name = new_date.strftime("%A")

    print(today)


    confirmed = Order.objects.filter(status = 'Completed').count()
    canc_return = Order.objects.filter(Q(status = "Order cancelled") | Q(status = "Returned")).count()

    
    
    print(order_count_in_day,order_count_in_month,order_count_in_week)
    context = {
        "order" : order,
        "cod" : cod,
        "razor" : razor,
        "paypal" : paypal,
        "total_revenue" : total_revenue,
        "total_orders" : total_orders,
        "total_users" : total_users,
        "total_products" : total_products,
        "name1" : name1,
        "name2" : name2,
        "name3" : name3,
        "name4" : name4,
        "count1" : count1,
        "count2" : count2,
        "count3" : count3,
        "count4" : count4,
        "order_count_in_month" : order_count_in_month,
        "order_count_in_day" : order_count_in_day,
        "order_count_in_week" : order_count_in_week,
        "confirmed" : confirmed,
        "canc_return" : canc_return,
        "today_sale" : today_sale,
        "yester_day_sale" : yester_day_sale,
        "day_2": day_2,
        "day_3": day_3,
        "day_4": day_4,
        "today" : today,
        "yesterday" : yesterday,
        "day_2_name" : day_2_name,
        "day_3_name" : day_3_name,
        "day_4_name" : day_4_name,

    }
    return render(request, 'adminside/adminhome.html', context)


@staff_member_required(login_url='adminlogin')
def adminorder(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            order = Order.objects.all().filter(tracking_no__icontains = key).order_by('-created_at')
        else:
            return redirect('orderlist')
    else:
        order = Order.objects.all().filter().order_by('-created_at')

    p = Paginator(order, 10)
    page = request.GET.get('page')
    orders = p.get_page(page)

    form = newstatus()
    context = {
        'form' : form,
        'orders' : orders
    }
    return render(request, 'adminside/orderlist.html', context)

@staff_member_required(login_url='adminlogin')
def update_admin_order(request,id):
    if request.method == 'POST':
        instance = get_object_or_404(Order, id=id)
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('orderlist')


@staff_member_required(login_url='adminlogin')
def sales_report(request):
    today = datetime.today()
    year = datetime.now().year
    month = today.month
    today_date=str(date.today())
    year = today.year
    years = []


    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)

        orders = Order.objects.filter(Q(created_at__lt=end_date),Q(created_at__lt=start_date)).values('oderuser__product_id__product_name','oderuser__product_id__in_stock_total',
        total = Sum('total_price'),).annotate(dcount=Sum('oderuser__quantity')).order_by()
        # total_payment_amount = Order.objects.filter(created_at__month=month).aggregate(Sum('total_price'))
    else:
       

        orders = Order.objects.filter(created_at__year = year,created_at__month=month).values('oderuser__product_id__product_name','oderuser__product_id__in_stock_total',
        total = Sum('total_price'),).annotate(dcount=Sum('oderuser__quantity')).order_by()
        for i in range (10):
            val = year-i
            years.append(val)
    context = {
        'orders':orders,
        'today_date' : today_date,
        'years': years
        
    }
    return render(request,'adminside/salesreport.html',context)  

@staff_member_required(login_url='adminlogin')
def monthly_sales_report(request, id):
    orders = Order.objects.filter(created_at__month = id).values('oderuser__product_id__product_name','oderuser__product_id__in_stock_total',total = Sum('total_price'),).annotate(dcount=Sum('oderuser__quantity')).order_by()
    print(orders)
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'adminside/sales-report-table.html',context)  

@staff_member_required(login_url='adminlogin')
def yearly_sales_report(request, id):
    orders = Order.objects.filter(created_at__year = id).values('oderuser__product_id__product_name','oderuser__product_id__in_stock_total',total = Sum('total_price'),).annotate(dcount=Sum('oderuser__quantity')).order_by()
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }

    return render(request,'adminside/sales-report-table.html',context)  


@staff_member_required(login_url='adminlogin')
def adminProView(request,cat_slug, subcat_slug, pro_slug):
    product = Product.objects.filter(url_slug = pro_slug, subcategories_id__url_slug = subcat_slug)
    tests = {
        'product' : product
    }
    return render(request, 'adminside/adminproduct.html', tests)
    # return render(request, 'adminside/adminbaseori.html', tests)


@staff_member_required(login_url='adminlogin')
def selectsubfromcat(request):
    pass


@staff_member_required(login_url='adminlogin')
def couponshow(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon' : coupon
    }

    return render(request, 'adminside/offer_management/coupon.html', context)

@staff_member_required(login_url='adminlogin')
def category_offers(request):
    disc_category = Categories.objects.all()
    context = {
        'disc_category' : disc_category
    }
    return render(request, 'adminside/offer_management/category_offers.html', context)

@staff_member_required(login_url='adminlogin')
def add_category_offers(request):
    if request.method == 'POST' :
        category_name = request.POST.get('category_name')
        category_offer = request.POST.get('category_offer')
        category = Categories.objects.get(title = category_name)
        category.category_offer =  category_offer
        category.save()
        messages.success(request,'Added Category offer success fully')
        return redirect('category_offers')


    
@staff_member_required(login_url='adminlogin')

def category_offers_delete(request, id):
    if request.method=="POST":
        try:
            delete_cat = Categories.objects.get(id = id)
            delete_cat.category_offer = 0
            delete_cat.save()
            return redirect('category_offers')
        except:
            return redirect('category_offers')

@staff_member_required(login_url='adminlogin')
def addcoupon(request):
    form = couponform()
    if request.method == "POST":
        form = couponform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('couponshow')
        else:
            print(form.errors.as_data())
            messages.error(request,"Enter correct data")
            return redirect('couponshow')
            
    context = {
        'form' : form
    }
    return render(request, 'adminside/offer_management/addcoupon.html', context)

def UpdateCoupon(request, id):
    pass
@staff_member_required(login_url='adminlogin')
def DeleteCoupon(request, id):
    if request.method == "POST":
        coup = Coupon.objects.get(id = id)
        coup.delete()
        return redirect('couponshow')

@staff_member_required(login_url='adminlogin')
def ProductDiscount(request):
    disc = Product.objects.all()
    context = {
        'disc' : disc
    }
    return render(request, 'adminside/offer_management/product_discount.html', context)

@staff_member_required(login_url='adminlogin')
def DeleteProductDiscount(request, id):
    if request.method == "POST":
        disc = discount.objects.get(id = id)
        disc.delete()
        return redirect('product_discount')

@staff_member_required(login_url='adminlogin')
def Product_discount_add(request):
    if request.method == 'POST' :
        category_name = request.POST.get('product_name')
        category_offer = request.POST.get('product_offer')
        product = Product.objects.get(product_name = category_name)
        product.product_offer =  category_offer
        product.save()
        messages.success(request,'Added Product offer success fully')
        return redirect('product_discount')