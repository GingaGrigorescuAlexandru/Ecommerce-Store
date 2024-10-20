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

    path('product/<str:pk>', views.productPage, name = 'product'),

    path('cart/<str:pk>', views.cartPage, name = 'cart'),
    path('delete-from-cart/', views.delete_item_from_cart, name = 'delete-from-cart'),
    path('add-item-to-favorites/', views.add_item_to_favorites, name = 'add-item-to-favorites')
]