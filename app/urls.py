from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = 'home'),

    path("register/", views.register, name = 'register'),
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),

    path('orders/', views.ordersPage, name = 'orders'),
    path('update-order-status/', views.updateOrderStatus, name = 'update-order-status'),

    path('profile/<str:pk>', views.profilePage, name = 'profile'),
    path('update-user/', views.update_user, name = 'update-user'),

    path('add-address/', views.addAddress, name = 'add-address'),
    path('address-list/<str:pk>', views.addressList, name = 'address-list'),
    path('edit-address/<str:pk>', views.editAddress, name = 'edit-address'),

    path('favorite-list/<str:pk>', views.favoriteList, name = 'favorite-list'),

    path('add_product/', views.addProduct, name = "add_product"),

    path('catalog/', views.productCatalog, name = 'catalog'),
    path('filter-catalog-products/', views.filter_products, name = 'filter-catalog-products'),

    path('product/<str:pk>', views.productPage, name = 'product'),

    path('guest_cart/', views.guestCartPage, name='guest_cart'),
    path('cart/<str:pk>', views.cartPage, name = 'cart'),
    path('delete-from-cart/', views.delete_item_from_cart, name = 'delete-from-cart'),
    path('add-item-to-favorites/', views.add_item_to_favorites, name = 'add-item-to-favorites'),

    path('about/', views.about, name = 'about'),

    path('contact/', views.contactUs, name = 'contact'),

    path('privacy/', views.contactUs, name = 'privacy'),

    path('legal/', views.legalPage, name = 'legal'),

    path('terms_conditions/', views.legalPage, name = 'terms_conditions'),

    path('add_newsletter_email/<str:pk>', views.add_newsletter_email, name = 'add_newsletter_email'),

    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('checkout', views.checkout, name='checkout'),
    path('session-status/', views.session_status, name='session-status'),
    path('return.html', views.return_view, name='return_html'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe-webhook'),
]