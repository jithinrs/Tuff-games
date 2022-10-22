from django.urls import path
from .import views

app_name='accountmanage'

urlpatterns = [
    path('', views.useraccount, name="useraccount"),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    # path('orders', views.userorderhistory, name='userorderhistory'),
    path('orders', views.userorderhistory, name='userorderhistory'),
    path('userorderdetails/<str:track>', views.user_order_details, name='userorderdetails'),
    path('addaddress', views.addaddress, name='useraddaddress'),
    path('deleteaddress/<int:id>/', views.delete_address, name='delete_addressss'),
    path('updateaddress/<int:id>/', views.update_address, name='updateaddress'),
]