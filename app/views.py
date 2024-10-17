from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, PropertiesProductForm, ProductCreationForm
from .models import Clienti, Produse, ProduseImagini

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

            print("All good til here")
            image_file = request.FILES.get('catalog-image-input')
            print("Got the image file")
            print(image_file)
            if image_file:
                image_data = image_file.read()
                print("Got the image data")
                product_image = ProduseImagini(produs = product,
                                               imagine_catalog = image_data)
                print("Instantiated the product image")
                product_image.save()
                print("FINALLY, saved the product image")
            return redirect('catalog')

    context = {'formProduct': formProduct,
               'formProperties': formProperties}

    return render(request, 'app/add_product_page.html', context)


def productCatalog(request):
    products = Produse.objects.all()
    images = ProduseImagini.objects.all()
    products_with_images = []

    for product in products:
        try:
            image = images.get(produs = product)
            products_with_images.append((product, image.imagine_catalog))
        except ProduseImagini.DoesNotExist:
            products_with_images.append((product, None))
    context = {'products_with_images': products_with_images}
    return render(request, 'app/catalog.html', context)