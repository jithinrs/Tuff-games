from django.urls import path
from .import views

urlpatterns = [
    path('', views.admin_login, name="adminlogin"),
    path('adminlogout', views.adminlogout, name='adminlogout'),
    path('dashboard/', views.adminbase,name='adminbase'),
    path('salesreport', views.sales_report, name='salesreport'),
    path("sales_report_month/<int:id>",views.monthly_sales_report,name='sales_report_month'),
    path("sales_report_year/<int:id>",views.yearly_sales_report ,name='sales_report_year'),
    path('categorylist/', views.Categorylist.as_view(), name='categorylist'),
    path('categoryadd/', views.Categoryadd.as_view(), name='categoryadd'),
    path('category_delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category_update/<slug:pk>/', views.Categoryupdate.as_view(), name='category_update'),
    path('subcategorylist/<int:id>/', views.SubCategorylist.as_view(), name='subcategorylist'),
    path('subcategorylist/', views.SubCategoryFullList.as_view(), name='subcategoryfulllist'),
    path('subcategoryadd/', views.SubCategoryadd.as_view(), name='subcategoryadd'),
    path('subcategory_update/<slug:pk>/', views.SubCategoryupdate.as_view(), name='subcategory_update'),
    path('subcategory_delete/<int:id>/', views.subcategory_delete, name='subcategory_delete'),
    path('productlist/', views.Productlist.as_view(), name='productlist'),
    path('<slug:cat_slug>/<slug:subcat_slug>/<slug:pro_slug>', views.adminProView, name='singleproduct'),
    path('<slug:cat_slug>/<slug:subcat_slug>/<slug:pro_slug>', views.SingleProduct, name='singleproduct'),
    path('productadd/', views.Productadd.as_view(), name='productadd'),
    path('productspec/', views.Productspec.as_view(), name='productspec'),
    path('product_update/<slug:pk>/', views.Productupdate.as_view(), name='product_update'),
    path('product_delete/<int:id>/', views.product_delete, name='product_delete'),
    path('orderlist/', views.adminorder, name='orderlist'),
    path('admin_update_order/<int:id>',views.update_admin_order,name="update_admin_order"),


    path('offer-coupon', views.couponshow, name='couponshow'),
    path('add-coupon', views.addcoupon, name='addcoupon'),
    path('deletecoupon/<int:id>', views.DeleteCoupon, name='deletecoupon'),
    path('category-offers', views.category_offers, name='category_offers'),
    path('category-offers-add', views.add_category_offers, name='add_category_offers'),
    path('category-offers-delete/<int:id>/', views.category_offers_delete, name="category_offers_delete"),
    path('product-discount', views.ProductDiscount, name='product_discount'),
    path('product-discount-delete/<int:id>/', views.DeleteProductDiscount, name='product_discount_delete'),
    path('Product_discount_add', views.Product_discount_add, name='Product_discount_add'),


    path("user_display",views.userdisplay,name='user_display'),


    path('selectsubfromcat/', views.selectsubfromcat, name='selectsubfromcat'),
]