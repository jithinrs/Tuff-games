from django.urls import path
from .import views

urlpatterns = [
    path('', views.useraccount, name="useraccount"),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    # path('orders', views.userorderhistory, name='userorderhistory'),
    path('orders', views.userorderhistory, name='userorderhistory'),
    path('addaddress', views.addaddress, name='useraddaddress'),
    path('deleteaddress/<int:id>', views.deladdress, name='deleteaddress'),
    path('updateaddress/<int:id>/', views.updateaddress, name='updateaddress'),
]