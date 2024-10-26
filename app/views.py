from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from .forms import (CustomUserCreationForm,
                    PropertiesProductForm,
                    ProductCreationForm,
                    AddressForm,
                    CardForm,
                    )
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings
import logging
import json
import stripe
from .models import (AuthUser,
                     Adrese,
                     CarduriClienti,
                     Clienti,
                     Produse,
                     ProduseImagini,
                     ProprietatiProduse,
                     Categorie,
                     Colors,
                     Cosuri,
                     Domains,
                     Favorites,
                     NewsletterEmails,
                     Sizes
                     )


stripe.api_key = settings.STRIPE_SECRET_KEY

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

            customer = stripe.Customer.create(email=form.cleaned_data['email'])

            new_client = Clienti(
                nume=form.cleaned_data['first_name'],
                prenume=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            new_client.save()

            customer = stripe.Customer.create(email=new_client.email)
            # Set the stripe_customer_id to be the same as the client_id
            new_client.stripe_customer_id = new_client.client_id  # Set to client_id
            new_client.save()  # Save the client with the updated stripe_customer_id


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
    user = AuthUser.objects.get(id = pk)

    context = {'user': user}
    return render(request, 'app/profile.html', context)


def addStripe(request):
    client = Clienti.objects.get(client_id=request.user.id)

    data = json.loads(request.body)
    payment_method_id = data.get('payment_method_id')

    customer_id = client.stripe_customer_id

    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id,
    )

    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id,
        },
    )
    return JsonResponse({'success': True}, status=200)



def addCard(request):
    if request.method == 'GET':
        context = {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
        }
        return render(request, 'app/add_card.html', context)

    elif request.method == 'POST':
        try:
            print(request.user.id)
            client = Clienti.objects.get(client_id=request.user.id)
            print("Hello")
            data = json.loads(request.body)
            payment_method_id = data.get('payment_method_id')
            print(payment_method_id)
            customer_id = client.stripe_customer_id
            print(customer_id)

            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id,
            )
            print("Hello")
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
            )
            return JsonResponse({'success': True}, status=200)

        except Clienti.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Client not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def cardsPage(request, pk):
    context = {}
    return render(request, 'app/cards.html', context)

def addAddress(request):
    form = AddressForm()
    addresses = Adrese.objects.filter( client_id = request.user.id ).values_list('nume_adresa', flat = True)
    print(addresses)
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit = False)

            if address.nume_adresa in addresses:
                messages.error(request, "You can't have 2 addresses with the same name!")
                return render(request, 'app/add_address.html', {'form': form})

            address.client_id = request.user.id
            address.save()

            return redirect(reverse('address-list', kwargs={'pk': request.user.id}))

    context = {'form': form}
    return render(request, 'app/add_address.html', context)

def addressList(request, pk):
    addresses = Adrese.objects.filter(client = pk)
    context = {'addresses': addresses}
    return render(request, 'app/address_list.html', context)

def editAddress(request, pk):
    if request.method == "POST":

        address = Adrese.objects.filter(address_id = pk)

        data = {
            'nume_adresa': request.POST.get("address_name"),
            'tara': request.POST.get("address_country"),
            'judet': request.POST.get("address_state"),
            'localitate': request.POST.get("address_city"),
            'strada': request.POST.get("address_street"),
            'numar': request.POST.get("address_number"),
            'bloc': request.POST.get("address_block"),
            'scara': request.POST.get("address_stair"),
            'etaj': request.POST.get("address_floor"),
            'apartament': request.POST.get("address_apartment")
        }

        address.update(**data)
        messages.success(request, 'Address Saved')
        return redirect(reverse('address-list', kwargs={'pk': request.user.id}))

    context = {}
    return HttpResponse("Some content")

def favoriteList(request, pk):
    favorite_items = Favorites.objects.filter(client = pk).select_related('product')
    favorite_products_ids = set(favorite_items.values_list('product', flat = True))

    images = ProduseImagini.objects.all()

    cart = Cosuri.objects.filter(client = request.user.id)
    cart_product_ids = set(cart.values_list('produs', flat = True))

    product_categories = Categorie.objects.all()
    product_domains = Domains.objects.all()
    product_sizes = Sizes.objects.all()
    product_colors = Colors.objects.all()

    products_with_images = []

    for product in favorite_items:
        try:
            image = images.get(produs = product.product)
            products_with_images.append((product, image.imagine_catalog))
        except ProduseImagini.DoesNotExist:
            products_with_images.append((product, None))


    context = {'products_with_images': products_with_images,
               'cart_product_ids': cart_product_ids,
               'favorite_products_ids': favorite_products_ids,
               'product_categories': product_categories,
               'product_domains': product_domains,
               'product_sizes': product_sizes,
               'product_colors': product_colors
               }

    return render(request, 'app/favorite.html', context)

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
    cart_product_ids = set(cart.values_list('produs', flat = True))


    product_categories = Categorie.objects.all()
    product_domains = Domains.objects.all()
    product_sizes = Sizes.objects.all()
    product_colors = Colors.objects.all()

    favorite_items = Favorites.objects.filter(client = request.user.id)
    favorite_products_ids = set(favorite_items.values_list('product', flat = True))


    products_with_images = []

    for product in products:
        try:
            image = images.get(produs = product)
            products_with_images.append((product, image.imagine_catalog))
        except ProduseImagini.DoesNotExist:
            products_with_images.append((product, None))

    context = {'products_with_images': products_with_images,
               'cart_product_ids': cart_product_ids,
               'favorite_products_ids': favorite_products_ids,
               'product_categories': product_categories,
               'product_domains': product_domains,
               'product_sizes': product_sizes,
               'product_colors': product_colors,
               }
    return render(request, 'app/catalog.html', context)


def filter_products(request):
    if request.method == 'POST':
        try:
            filter_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


        product_categories = filter_data.get('productCategories', [])
        selected_budget = filter_data.get('selected_budget')
        colors = filter_data.get('colors', [])
        domains = filter_data.get('domains', [])
        sizes = filter_data.get('sizes', [])

        products = Produse.objects.all()
        properties = ProprietatiProduse.objects.all()
        query = Q()

        if product_categories:
            properties = properties.filter(Category__in = product_categories)

        if colors:
            for color in colors:
                query |= Q(Culori__icontains=color)

            properties = properties.filter(query)

        if domains:
            properties = properties.filter(domeniu__in=domains)

        if sizes:
            properties = properties.filter(Dimensiune__in=sizes)

        if selected_budget:
            products = products.filter(pret_unitar__lte=selected_budget)


        product_ids = properties.values_list('produs_id', flat=True)
        products = products.filter(produs_id__in=product_ids)

        images = ProduseImagini.objects.all()

        client = Clienti.objects.get(client_id = request.user.id)

        cart = Cosuri.objects.filter(client = request.user.id)
        cart_product_ids = set(cart.values_list('produs', flat=True))

        favorite_items = Favorites.objects.filter(client = request.user.id)
        favorite_products_ids = set(favorite_items.values_list('product', flat=True))

        filtered_products_with_images = []

        for product in products:
            try:
                image = images.get(produs = product)
                filtered_products_with_images.append((product, image.imagine_catalog))
            except ProduseImagini.DoesNotExist:
                filtered_products_with_images.append((product, None))

        print(request.user.id)

        context = {
            'products_with_images': filtered_products_with_images,
            'cart_product_ids': cart_product_ids,
            'client': client,
            'favorite_products_ids': favorite_products_ids,
        }

        html_content = render_to_string('app\components\catalog_filteredProducts_component.html', context)

        return JsonResponse({'html': html_content})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def productPage(request, pk):
    product = Produse.objects.get(produs_id=pk)

    product_properties = ProprietatiProduse.objects.get(produs = pk)
    product_images = ProduseImagini.objects.get(produs = pk)
    product_type = Categorie.objects.get(categorie_id = product.categorie_id)

    favorite_items = Favorites.objects.filter(client = request.user.id)
    favorite_products_ids = set(favorite_items.values_list('product', flat = True))

    properties_fields = product_properties._meta.fields

    context = {'product': product,
               'product_properties': product_properties,
               'product_images': product_images,
               'product_type': product_type,
               'properties_fields': properties_fields,
               'favorite_products_ids': favorite_products_ids
               }
    return render(request, 'app/productPage.html', context)

logger = logging.getLogger(__name__)


def cartPage(request, pk):
    cart_items = Cosuri.objects.filter(client=pk).select_related('produs')
    cart_items = cart_items.prefetch_related(
        Prefetch('produs__proprietatiproduse', queryset = ProprietatiProduse.objects.all(), to_attr = 'properties'),
        Prefetch('produs__produseimagini', queryset = ProduseImagini.objects.all(), to_attr = 'images'),
        Prefetch('produs__categorie', queryset = Categorie.objects.all(), to_attr = 'category')
    )

    total_price = 0.0

    cart_items_with_totals = []

    for item in cart_items:
        product_price = item.produs.pret_unitar
        quantity = item.cantitate

        item_total_price = product_price * quantity

        total_price += item_total_price

        cart_items_with_totals.append({
            'item': item,
            'item_total_price': item_total_price,
            'product_price': product_price,
            'quantity': quantity,
        })

    if request.method == 'POST':
        print('Trying to add to cart')
        client_id = request.POST.get('client_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        add_product_date = request.POST.get('addProductDate')

        client_instance = get_object_or_404(Clienti, client_id=client_id)

        product_instance = get_object_or_404(Produse, produs_id=product_id)

        cart_item, created = Cosuri.objects.get_or_create(
            cos_id = str(client_id) + "#" + str(product_id),
            client = client_instance,
            produs = product_instance,
            defaults = {'cantitate': quantity, 'data_adaugare': add_product_date}
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
        'cart_items_with_totals': cart_items_with_totals,
        'total_price': total_price
    }
    return render(request, 'app/cart.html', context)


def about(request):
    return render(request, 'app/about.html')

def contactUs(request):
    return render(request, 'app/contact.html')

def privacyPolicy(request):
    return render(request, 'app/privacy.html')

def termsConditions(request):
    return render(request, 'app/terms_conditions.html')

def legalPage(request):
    return render(request, 'app/legal.html')

def delete_item_from_cart(request):

    if request.method == "POST":
        client_id = request.POST.get('client_id')
        product_id = request.POST.get('product_id')

        cos_id = str(client_id) + "#" + str(product_id)

        product_cos = Cosuri.objects.get(cos_id = cos_id)
        product_cos.delete()

        return JsonResponse({'message': 'Item successfully deleted'}, status = 200)

    context = {}
    return JsonResponse({'message': 'Invalid request'}, status = 400)

def add_item_to_favorites(request):
    if request.method == "POST":
        print("Trying to add to favorites")
        client_id = request.POST.get("client_id")
        product_id = request.POST.get("product_id")

        client_instance = get_object_or_404(Clienti, client_id=client_id)
        product_instance = get_object_or_404(Produse, produs_id=product_id)

        favorite_id = f"{client_id}#{product_id}"

        favorite_item, created = Favorites.objects.get_or_create(
            favorite=favorite_id,
            client = client_instance,
            product = product_instance
        )

        return JsonResponse({'message': "Added product to favorites list"}, status=200)

    return JsonResponse({'message': "Invalid request method"}, status=400)\

def add_newsletter_email(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        new_email = data.get("newsletter-email-input")

        client = NewsletterEmails.objects.filter(client = pk).first()
        client_instance = get_object_or_404(Clienti, client_id = pk)

        if client:
            # Update the existing record's email
            client.email = new_email
            client.save()
            return JsonResponse({'message': 'Email successfully updated!'}, status=200)
        else:
            NewsletterEmails.objects.create(
                client = client_instance,
                email = new_email
            )
            return JsonResponse({'message': 'Email successfully added!'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)

