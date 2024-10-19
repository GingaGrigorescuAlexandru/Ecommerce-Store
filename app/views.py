from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, PropertiesProductForm, ProductCreationForm
from django.contrib.auth.hashers import make_password
import logging
from .models import (Clienti,
                     Produse,
                     ProduseImagini,
                     ProprietatiProduse,
                     Categorie,
                     Cosuri)


def home(request):
    context = {}
    return render(request, 'app/home.html', context)


def register(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.password = make_password(user.password)
            user.save()

            new_client = Clienti(
                nume=form.cleaned_data['first_name'],
                prenume=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            new_client.save()

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration!")


    context = {'form': form}
    return render(request, 'app/register.html', context)

def loginUser(request):
    page = "login"
    form = AuthenticationForm()

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get( "username" ).lower()
        password = request.POST.get( "password" )

        try:
            user = User.objects.get( username = username )
        except:
            messages.error( request, "User doesn't exist!" )

        user = authenticate( request, username = username, password = password )
        if user is not None:
            login( request, user )
            return redirect( "home" )
        else:
            messages.error( request, "Username OR password does no exist!" )
    context = {"page": page}
    return render( request, "app/login.html", context )

def logoutUser(request):
    logout(request)
    return redirect('home')

def profilePage(request, pk):
    user = User.objects.get(id = pk)
    context = {'user': user}
    return render(request, 'app/profile.html', context)

def addProduct(request):
    formProduct = ProductCreationForm()
    formProperties = PropertiesProductForm()

    if request.method == "POST":
        formProduct = ProductCreationForm(request.POST)
        formProperties = PropertiesProductForm(request.POST)

        if all([formProduct.is_valid(), formProperties.is_valid()]):
            product = formProduct.save()

            properties = formProperties.save(commit = False)
            properties.produs = product
            properties.save()

            image_file = request.FILES.get('catalog-image-input')

            if image_file:
                image_data = image_file.read()
                product_image = ProduseImagini(produs = product,
                                               imagine_catalog = image_data)
                product_image.save()
            return redirect('catalog')

    context = {'formProduct': formProduct,
               'formProperties': formProperties}

    return render(request, 'app/add_product_page.html', context)


def productCatalog(request):
    products = Produse.objects.all()
    images = ProduseImagini.objects.all()
    cart = Cosuri.objects.filter(client = request.user.id)
    cart_product_ids = set(cart.values_list('produs', flat=True))

    products_with_images = []

    for product in products:
        try:
            image = images.get(produs = product)
            products_with_images.append((product, image.imagine_catalog))
        except ProduseImagini.DoesNotExist:
            products_with_images.append((product, None))
    context = {'products_with_images': products_with_images,
               'cart_product_ids': cart_product_ids}
    return render(request, 'app/catalog.html', context)

def productPage(request, pk):
    product = Produse.objects.get(produs_id=pk)
    product_properties = ProprietatiProduse.objects.get(produs = pk)
    product_images = ProduseImagini.objects.get(produs = pk)
    product_type = Categorie.objects.get(categorie_id = product.categorie_id)

    properties_fields = product_properties._meta.fields

    context = {'product': product,
               'product_properties': product_properties,
               'product_images': product_images,
               'product_type': product_type,
               'properties_fields': properties_fields
               }
    return render(request, 'app/product.html', context)
logger = logging.getLogger(__name__)


def cartPage(request, pk):
    cart_items = Cosuri.objects.filter(client=pk).select_related('produs')
    cart_items = cart_items.prefetch_related(
        Prefetch('produs__proprietatiproduse', queryset = ProprietatiProduse.objects.all(), to_attr = 'properties'),
        Prefetch('produs__produseimagini', queryset = ProduseImagini.objects.all(), to_attr = 'images'),
        Prefetch('produs__categorie', queryset = Categorie.objects.all(), to_attr = 'category')
    )

    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        add_product_date = request.POST.get('addProductDate')

        client_instance = get_object_or_404(Clienti, client_id=client_id)

        product_instance = get_object_or_404(Produse, produs_id=product_id)

        cart_item, created = Cosuri.objects.get_or_create(
            cos_id=str(client_id)+"#"+str(product_id),
            client=client_instance,
            produs=product_instance,
            defaults={'cantitate': quantity, 'data_adaugare': add_product_date}
        )

        if not created:
            # If the item already exists, update the quantity (or handle as needed)
            cart_item.cantitate = quantity
            cart_item.save()
            message = 'Product quantity updated in the cart!'
        else:
            # If a new item was created
            cart_item.cantitate = quantity
            message = 'Product added to the cart!'

        return JsonResponse({'message': message}, status = 200)

    context = {
        'cart_items': cart_items
    }
    return render(request, 'app/cart.html', context)