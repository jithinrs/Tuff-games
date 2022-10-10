from django.shortcuts import render, redirect

from accountmanage.models import Order,OrderItem, userpic
from .forms import *
from .views import *
from django.contrib import messages
from authentications.models import Account
from authentications.form import userupdateform
from django.views.generic import CreateView, ListView, UpdateView
from .models import *
from django.core.paginator import Paginator


# Create your views here.


def useraccount(request):
    test = addressform()
    addr = useraddress.objects.filter(user_id = request.user)
    image = userpic.objects.filter(user_id = request.user)
    if image is not None:
        flag = 1
    else:
        flag = 2
    account = Account.objects.get(email = request.user)
    tests = {
        'account' : account,
        'image' : image,
        'addr' : addr,
        'flag' : flag
    }
    
    return render(request, 'useraccount/accounthome.html', tests)

def updateprofile(request):
    id = Account.objects.get(id = request.user.id)
    if request.method == "POST":
        form = userupdateform(request.POST, instance = id)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated succesfully')
            return redirect('useraccount')
    else:
        form = userupdateform(instance=id)
        context = {
            'form' : form
        }
    return render(request, 'useraccount/updateprofile.html', context)

def addaddress(request):
    if request.method == "POST":
        form = addressform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "update succesful")
            return  redirect('useraccount')
        else:
            print(form.errors.as_data())
            messages.error(request,"you are a FAILURE!!")
    data = Account.objects.filter(email = request.user)
    context = {
        'data' : data
    }
    return render(request, 'useraccount/useraddaddress.html', context)

def updateaddress(request,id):
    addr = useraddress.objects.get(id=id)
    form = addressform(instance = addr)
    print(form)
    if request.method == 'POST':     
        form = addressform(request.POSt, instance = addr)
        if form.is_valid():
            form.save()
            return redirect('useraccount')
        else:
            print(form.errors.as_data())
    return render(request,'useraccount/userupdateaddress.html', {'form' : form})


# def userorderhistory(request):
#     ord = Order.objects.filter(user_id = request.user)
#     test = []
#     for obj in ord:

#         pro = OrderItem.objects.filter(order_id = obj.id)
#         test.append(pro)

#     print(test[1][0].price)
#     context = {
#         'test' : test
#     }
#     return render(request, 'useraccount/userorder.html', context)



# class useroderhistory(ListView):
#     model = Order
#     template_name = 'useraccount/userorder.html'

#     ordering = ['-created_at']

def userorderhistory(request):
    orderhistorys = Order.objects.filter(user_id = request.user).order_by('-created_at')

    p = Paginator(Order.objects.filter(user_id = request.user).order_by('-created_at'),5)
    page = request.GET.get('page')
    orderhistory = p.get_page(page)

    context = {
        'orderhistory' : orderhistory,
        'orderhistorys' : orderhistorys
    }
    return render(request, 'useraccount/userorder.html', context)


def deladdress(request, id):
    
    address=useraddress.objects.get(id = id)
    print(address)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('useraccount')