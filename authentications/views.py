from itertools import product
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import Account
from.form import RegistrtationForm
from django.contrib import messages,auth
from .verify import send_otp, verify_otp
from .form import *
from .models import *
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from products.models import Cart
from frontside.views import _cart_id


# Create your views here.
def Register(request):
    if request.method=='POST':
        
        form=RegistrtationForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name  = request.POST['last_name']
            email      = request.POST['email']
            # gender     = request.POST['gender']
            mobile     = request.POST['mobile']
            password   = request.POST['password']

            request.session['first_name'] = first_name
            request.session['last_name']  = last_name
            request.session['email']      = email
            # request.session['gender']     = gender
            request.session['mobile']     = mobile
            request.session['password']   = password
            
            # print("mobile: ",mobile)
            send_otp(mobile)
            return redirect(verify_code)
        else:
            messages.error(request,"Enter correct data")
            return render(request,'signup.html')

    form=RegistrtationForm()
    # context ={'form':form}
    return render(request,'signup.html')

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email)
        except :
            messages.error(request,"user Does not exist..")
        user = authenticate(request,email=email,password=password)
        # if user is not None:
        #     print("teste2")
        #     try:
        #         cart = Cart.objects.filter(session_id = _cart_id(request)).exist()
        #         print("test1")
        #         if cart:
        #             for item in cart:
        #                 try:
        #                     carter = Cart.objects.get(product = item.product, user = user)
        #                     carter.product_qty =+ 1
        #                     carter.save()
        #                 except:
        #                     item.user = user
        #                     item.save()



        #     except:
        #         pass

        if user is not None:
            print("teste2")
            try:
                cart = Cart.objects.filter(session_id = _cart_id(request)).exists()
                print("test1")
                print(cart)
                if cart:
                    print("poda")
                    cart = Cart.objects.filter(session_id = _cart_id(request))
                    for item in cart:
                        try:
                            carter = Cart.objects.get(product = item.product, user = user)
                            carter.product_qty =+ 1
                            carter.save()
                        except:
                            print("naari")
                            item.user = user
                            item.save()



            except:
                pass





            auth.login(request,user)
            return redirect('home') 
        else:
            # messages.error(request,'user does not exist..')
            return redirect('login')
    return render(request,'signin.html')





def loginotp(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        request.session['mobile'] = mobile
        try :
            user = Account.objects.get(mobile = mobile)
        except:
            messages.error(request, 'mobile is not registered')
            return redirect('otplogin')
    
        send_otp(mobile)
        return redirect(verify_loginotp)
    return render(request, 'otplogin.html')

def verify_loginotp(request):
    if request.method =='POST':
        otp_check = request.POST.get('otp')
        mobile=request.session['mobile']

        verify=verify_otp(mobile,otp_check)
        user = Account.objects.get(mobile = mobile)
        if verify:
            mobile  = request.session['mobile']
            print('podapatti')
            try:
                cart = Cart.objects.filter(session_id = _cart_id(request)).exists()
                print("test1")
                print(cart)
                if cart:
                    print("poda")
                    cart = Cart.objects.filter(session_id = _cart_id(request))
                    for item in cart:
                        try:
                            carter = Cart.objects.get(product = item.product, user = user)
                            carter.product_qty =+ 1
                            carter.save()
                        except:
                            print("naari")
                            item.user = user
                            item.save()



            except:
                pass
        #     user = authenticate(request,mobile = mobile)
        # if user is not None:
            print(user)
            login(request,user)
            return redirect('home') 
        else:
            # messages.error(request,'user does not exist..')
            messages.error(request,'Incorrect OTP')
            return redirect('verify_loginotp')
    return render(request,'verify.html')



def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return HttpResponse('<h1>404</h1>')

def verify_code(request):
    if  request.method == 'POST':
        otp_check = request.POST.get('otp')
        mobile=request.session['mobile']

        verify=verify_otp(mobile,otp_check)

        if  verify:
            messages.success(request,'account has created successfuly please login now') 

            first_name = request.session['first_name']
            last_name  = request.session['last_name']
            email      = request.session['email']
            # gender     = request.session['gender']
            mobile     = request.session['mobile']
            password   = request.session['password']

            user = Account.objects.create_user(
                first_name =  first_name,
                last_name  =  last_name,
                email      =  email,
                # gender     =  gender,
                mobile     =  mobile,
                password   =  password
            )
            user.is_verified = True
            user.save()
            messages.success(request,'Registration Successful')
            return redirect('login')
        
        else:
            messages.error(request,'Incorrect OTP')
            return redirect ('verify')
        
    return render(request,'verify.html')


def home(request):
    return render(request, 'home.html')




def user_block(request,id,flag):
    if request.method == 'POST':
         person = Account.objects.get( id = id)
         if flag ==1:
            person.is_active = False
            person.save()
         else: 
            person.is_active = True
            person.save()
         return redirect('user_display')