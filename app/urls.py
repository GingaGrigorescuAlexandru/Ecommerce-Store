from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = 'home'),

    path("register/", views.register, name = 'register'),
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),

    path('profile/<str:pk>', views.profilePage, name = 'profile'),

    path('add_product/', views.addProduct, name = "add_product"),

    path('catalog/', views.productCatalog, name = 'catalog'),

    path('product/<str:pk>', views.productPage, name = 'product')
]