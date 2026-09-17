from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clothingproduct/', views.clothingproduct, name='clothingproduct'),
    path('electronics/', views.electronics, name='electronics'),
    path('Gaming/', views.Gaming, name='Gaming'),
    path('kidsproduct/', views.kidsproduct, name='kidsproduct'),
    path('toys/', views.toys, name='toys'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('order/', views.order, name='order'),
    path('result/', views.result, name='result'),
    path('Stationery/', views.Stationery, name='Stationery'),
    path("save-purchase/", views.save_purchase, name="save_purchase"),
    
    
    
]