from django.urls import path
from .import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('register/',views.Register,name='register'),
    path('login/',views.Login,name='login'),
    path('verify_loginotp/',views.verify_loginotp,name='verify_loginotp'),
    path('otplogin', views.loginotp, name='otplogin'),
    path('logout/',views.Logout,name='logout'),
    path('verify/', views.verify_code ,name='verify'),
    path("user_block/<int:id>/<int:flag>",views.user_block,name='user_block'),
]