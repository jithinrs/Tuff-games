from datetime import date, datetime, timedelta
import email
from unicodedata import name
from django.shortcuts import render,redirect

from django.utils import timezone

from django.db.models import Sum, Q
from authentications.models import Account
from .models import Categories, Product, Specification, SubCategory,Coupon
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

# Create your views here.
#custom decorator

class adminrequiredmixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return render(request, '404error.html')
        if not request.user.is_admin:
            return render(request, '404error.html')
        return super(adminrequiredmixin, self).dispatch(request, *args, **kwargs)

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
    model = Categories
    success_message = 'Category Added'
    fields = "__all__"
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
    success_message = 'Category Updated'
    fields = "__all__"
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

class SubCategoryupdate(SuccessMessageMixin, UpdateView):
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

class Productadd(adminrequiredmixin, SuccessMessageMixin, CreateView, ProductsAddforms):
    model = Product
    success_message = 'Product Added'
    fields = "__all__"
    template_name = "adminside/productadd.html"


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['subcategories_id'].queryset = SubCategory.objects.none()

class Productupdate(SuccessMessageMixin, UpdateView):
    model = Product
    success_message = 'Product Updated'
    fields = "__all__"
    template_name = "adminside/productUpdate.html"

class Productspec(SuccessMessageMixin,CreateView):
    model = Specification
    success_message: str = "Specification added"
    fields = "__all__"
    template_name = "adminside/productspec.html"


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

def SingleProduct(request,cat_slug, subcat_slug, pro_slug):
    product = Product.objects.filter(url_slug = pro_slug, subcategories_id__url_slug = subcat_slug)
    tests = {
        'product' : product
    }
    return render(request, 'adminside/productpage.html', tests)

def category_delete(request, id):
    if request.method == 'POST':
        category_id = Categories.objects.get(pk=id)
        name = Categories.objects.filter(id=id).values('title')
        print(name)
        messages.success(request, f" {name[0]['title']} category is deleted")
        category_id.delete()
        return redirect('categorylist')

def subcategory_delete(request, id):
    if request.method == 'POST':
        subcategory_id = SubCategory.objects.get(pk=id)
        subcategory_id.delete()
        return redirect('categorylist')

def product_delete(request, id):
    if request.method == 'POST':
        product_id = Product.objects.get(pk=id)
       
        product_id.delete()
        return redirect('productlist')

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

def update_admin_order(request,id):
    if request.method == 'POST':
        instance = get_object_or_404(Order, id=id)
        status = request.POST.get('status')
        instance.status = status
        instance.save()
        return redirect('orderlist')



def sales_report(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)

        orders = Order.objects.filter(Q(created_at__lt=end_date),Q(created_at__lt=start_date)).values('oderuser__product_id__product_name','oderuser__product_id__in_stock_total',
        total = Sum('total_price'),).annotate(dcount=Sum('oderuser__quantity')).order_by()
        # total_payment_amount = Order.objects.filter(created_at__month=month).aggregate(Sum('total_price'))
    else:
        today = datetime.today()
        year = datetime.now().year
        month = today.month

        orders = Order.objects.filter(created_at__year = year,created_at__month=month).values('oderuser__product_id__product_name','oderuser__product_id__in_stock_total',
        total = Sum('total_price'),).annotate(dcount=Sum('oderuser__quantity')).order_by()
        today_date=str(date.today())
        year = today.year
        years = []
        for i in range (10):
            val = year-i
            years.append(val)
    context = {
        'orders':orders,
        'today_date' : today_date,
        'years': years
        
    }
    return render(request,'adminside/salesreport.html',context)  

def monthly_sales_report(request, id):
    orders = Order.objects.filter(created_at__month = id).values('oderuser__product_id__product_name','oderuser__product_id__in_stock_total',total = Sum('total_price'),).annotate(dcount=Sum('oderuser__quantity')).order_by()
    print(orders)
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'adminside/salesreport.html',context)  

def yearly_sales_report(request, id):
    orders = Order.objects.filter(created_at__year = id).values('oderuser__product_id__product_name','oderuser__product_id__in_stock_total',total = Sum('total_price'),).annotate(dcount=Sum('oderuser__quantity')).order_by()
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }

    return render(request,'adminside/sales-report.html',context)  


def adminProView(request,cat_slug, subcat_slug, pro_slug):
    product = Product.objects.filter(url_slug = pro_slug, subcategories_id__url_slug = subcat_slug)
    tests = {
        'product' : product
    }
    return render(request, 'adminside/adminproduct.html', tests)
    # return render(request, 'adminside/adminbaseori.html', tests)



def selectsubfromcat(request):
    pass



def couponshow(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon' : coupon
    }

    return render(request, 'adminside/coupon.html', context)

def addcoupon(request):
    form = couponform()
    if request.method == "POST":
        form = couponform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('couponshow')
        else:
            print(form.errors.as_data())
            messages.error(request,"you are a FAILURE!!")
            return redirect('couponshow')
            
    context = {
        'form' : form
    }
    return render(request, 'adminside/addcoupon.html', context)