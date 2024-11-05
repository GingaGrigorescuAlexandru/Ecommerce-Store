from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
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
from django.contrib.auth import password_validation, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
import boto3
from django.core.files.base import ContentFile
import io
import base64
import logging
import json
import stripe
import ast
from .modules import send_confirmation_email
from .models import (AuthUser,
                     Adrese,
                     Comenzi,
                     Clienti,
                     Produse,
                     ProduseComenzi,
                     ProduseImagini,
                     ProprietatiProduse,
                     Categorie,
                     Colors,
                     Cosuri,
                     Domains,
                     Favorites,
                     NewsletterEmails,
                     Reviews,
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

            new_client = Clienti(
                username=form.cleaned_data['username'],
                nume=form.cleaned_data['last_name'],
                prenume=form.cleaned_data['first_name'],
                email=form.cleaned_data['email'],
            )
            new_client.save()

            customer = stripe.Customer.create(
                name = new_client.nume + ' ' + new_client.prenume,
                email = new_client.email
            )

            new_client.stripe_customer_id = customer.id
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
    user = AuthUser.objects.get(id = pk)

    context = {'user': user}
    return render(request, 'app/profile.html', context)



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

def update_user(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        try:
            client = Clienti.objects.get(client_id = request.user.id)
            client.prenume = last_name
            client.nume = first_name
            client.username = username
            client.email = email
            client.numar_telefon = phone_number
            client.save()

            user = AuthUser.objects.get(id = request.user.id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number

            if password:
                try:
                    password_validation.validate_password(password, user=user)
                    user.password = make_password(password)
                    user.save()
                    messages.info(request, 'Password updated successfully. Please log in again.')
                    logout(request)
                    return JsonResponse({'status': 'redirect', 'url': '/login/'})
                except ValidationError as e:
                    return JsonResponse({'status': 'error', 'message': 'The password did not meet the requirements!'}, status=400)

            user.save()

            return JsonResponse({'status': 'success', 'message': 'Clienti updated successfully!'})
        except Clienti.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Clienti not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'}, status=400)

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

def product_image_view(request, product_id):
    try:
        image_record = ProduseImagini.objects.get(produs = product_id)
        return HttpResponse(image_record.imagine_catalog, content_type="image/png")
    except ProduseImagini.DoesNotExist:
        return HttpResponse(status=404)

def addProduct(request):
    formProduct = ProductCreationForm()
    formProperties = PropertiesProductForm()

    if request.method == "POST":
        formProduct = ProductCreationForm(request.POST)
        formProperties = PropertiesProductForm(request.POST)

        if all([formProduct.is_valid(), formProperties.is_valid()]):
            product = formProduct.save()

            category = product.categorie.nume_categorie

            properties = formProperties.save(commit = False)
            properties.produs = product
            properties.Category = category
            properties.save()

            image_file = request.FILES.get('catalog-image-input')
            image = ProduseImagini(
                produs = product,
                imagine_catalog = image_file.name,
            )
            image.save()

            if image_file:
                s3 = boto3.client('s3')
                s3.upload_fileobj(image_file, 'stomagia', image_file.name)

                sanitized_filename = image_file.name.replace(" ", "%20")
                image_url = f'https://stomagia.s3.amazonaws.com/{sanitized_filename}'

            print(image_url)
            print(image_url)
            print(image_url)

            stripe_product = stripe.Product.create(
                name = product.nume,
                description = category,
                images = [image_url],
            )


            stripe_price = stripe.Price.create(
                product = stripe_product.id,
                unit_amount = int(product.pret_unitar * 100),
                currency = "ron",
            )

            # Save Stripe IDs to your database model if needed
            product.stripe_product_id = stripe_product.id
            product.stripe_price_id = stripe_price.id
            product.save()

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
            print(image.imagine_catalog)
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

    product_colors = product_properties.Culori

    if product_colors.startswith("[") and product_colors.endswith("]"):
        product_colors_list = ast.literal_eval(product_colors)
    else:
        product_colors_list = [product_colors]

    cleaned_colors = [color.strip().strip("'") for color in product_colors_list]

    product_images = ProduseImagini.objects.get(produs = pk)

    product_type = Categorie.objects.get(categorie_id = product.categorie_id)

    favorite_items = Favorites.objects.filter(client = request.user.id)
    favorite_products_ids = set(favorite_items.values_list('product', flat = True))

    properties_fields = product_properties._meta.fields

    review_posts = Reviews.objects.filter(product = pk).select_related('client')


    if request.method == 'POST':
        data = json.loads(request.body)

        review_body = data.get('input_review')
        nr_of_stars = data.get('nr_of_stars')
        client_instance = get_object_or_404(Clienti, client_id = request.user.id)
        product_instance = get_object_or_404(Produse, produs_id = pk)

        Reviews.objects.create(
            client = client_instance,
            product = product_instance,
            body = review_body,
            nr_stars = nr_of_stars
        )

        return JsonResponse({'message': 'Review added successfully!'})

    context = {'product': product,
               'product_properties': product_properties,
               'product_colors': cleaned_colors,
               'product_images': product_images,
               'product_type': product_type,
               'properties_fields': properties_fields,
               'favorite_products_ids': favorite_products_ids,
               'review_posts': review_posts
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
            cart_item.cantitate = quantity
            cart_item.save()
            message = 'Product quantity updated in the cart!'
        else:
            cart_item.cantitate = quantity
            message = 'Product added to the cart!'

        return JsonResponse({'message': message}, status = 200)

    context = {
        'cart_items_with_totals': cart_items_with_totals,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'total_price': round(total_price, 2)
    }
    return render(request, 'app/cart.html', context)


def guestCartPage(request):
    cart_items_with_totals = []
    total_price = 0.0

    cart = request.session.get('guest_cart', {})

    for product_id, details in cart.items():
        try:
            product_instance = Produse.objects.get(produs_id=product_id)
            product_price = product_instance.pret_unitar
            quantity = details['quantity']
            item_total_price = product_price * quantity
            total_price += item_total_price

            cart_items_with_totals.append({
                'item': {
                    'produs': product_instance,
                    'cantitate': quantity,
                },
                'item_total_price': item_total_price,
                'product_price': product_price,
                'quantity': quantity,
            })
        except Produse.DoesNotExist:
            continue

    # Handle adding/updating items in the session-based cart
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        add_product_date = request.POST.get('addProductDate')

        # Update session cart data
        if product_id in cart:
            cart[product_id]['quantity'] += quantity
            message = 'Product quantity updated in the cart!'
        else:
            cart[product_id] = {
                'quantity': quantity,
                'addProductDate': add_product_date
            }
            message = 'Product added to the cart!'

        request.session['guest_cart'] = cart

        return JsonResponse({'message': message}, status=200)

    context = {
        'cart_items_with_totals': cart_items_with_totals,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'total_price': round(total_price, 2)
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
    print("HEEEEEEEEEEEEEELLLLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOO")
    if request.method == "POST":
        data = json.loads(request.body)
        new_email = data.get("newsletter-email-input")
        client = NewsletterEmails.objects.filter(client = pk).first()
        client_instance = get_object_or_404(Clienti, client_id = pk)

        if client:
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



stripe.api_key = settings.STRIPE_SECRET_KEY
@csrf_exempt
def create_checkout_session(request):
    try:
        # Query the items from the cart and the owner of the cart info
        cart_items = Cosuri.objects.filter(client = request.user.id).select_related('produs')
        client = Clienti.objects.filter(client_id = request.user.id)

        # Fetch the price, quantity and name of the products for checkout and email template
        stripe_items = []
        item_names = []
        for item in cart_items:
            stripe_items.append({
                'price': item.produs.stripe_price_id,
                'quantity': item.cantitate,
            })

            # Fetch the product details from Stripe to get the name/description
            product = stripe.Product.retrieve(item.produs.stripe_product_id)
            item_names.append(product['name'])  # Add product name to the list

        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            line_items=stripe_items,
            customer_email=client.first().email,
            mode='payment',
            phone_number_collection={"enabled": True},
            billing_address_collection='auto',
            shipping_address_collection={
                'allowed_countries': ['RO'],
            },
            return_url=settings.YOUR_DOMAIN + '/return.html?session_id={CHECKOUT_SESSION_ID}',  # Return URL after checkout
            metadata={
                'item_names': ','.join(item_names)  # Store item names as a comma-separated string
            }
        )

        return JsonResponse({'clientSecret': session.client_secret})  # Return the session ID for client redirection
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def checkout(request):
    context = {'STRIPE_SECRET_KEY': settings.STRIPE_SECRET_KEY}
    return render(request, 'app/checkout.html', context)


@csrf_exempt
def session_status(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return HttpResponse("Session ID missing", status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return JsonResponse({
            'status': session.status,
            'customer_email': session.customer_details.email
        })
    except Exception as e:
        return HttpResponse(str(e), status=500)


def return_view(request):
    session_id = request.GET.get('session_id')  # Get the session ID from the URL
    session = stripe.checkout.Session.retrieve(session_id)  # Retrieve the session details from Stripe

    if session.payment_status == 'paid':
        return render(request, 'app/return.html', {'session': session})
    else:
        # Handle payment failure or other statuses
        return render(request, 'app/return.html', {'error': 'Payment not successful.'})



@csrf_exempt
def stripe_webhook(request):

    # Retrieve the raw body of the request, which contains the payload from Stripe
    payload = request.body
    # Retrieve the Stripe signature header from the request metadata
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    # Retrieve the webhook secret from the settings for verifying the Stripe signature
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)


    if event['type'] == 'checkout.session.completed':
        # Extract the session object from the event data
        session = event['data']['object']

        # Get the customer's email from the session
        customer_email = session.get('customer_email')

        client_instance = get_object_or_404(Clienti, email=customer_email)

        # Create an order entry in the Database
        order = Comenzi(
            client = client_instance,
            data_plasare = datetime.now(),
            status = 'Processing'
        )
        order.save()

        # Query the Cart, Products, ProductImages, ProductProperties and ProductCategories together
        cart_items = Cosuri.objects.filter(client=client_instance).select_related('produs')
        cart_items = cart_items.prefetch_related(
            Prefetch('produs__proprietatiproduse', queryset=ProprietatiProduse.objects.all(), to_attr='properties'),
            Prefetch('produs__produseimagini', queryset=ProduseImagini.objects.all(), to_attr='images'),
            Prefetch('produs__categorie', queryset=Categorie.objects.all(), to_attr='category')
        )

        total_price = 0.0
        cart_items_with_totals = []

        # Create a list with relevant order info for easy access
        for item in cart_items:
            product_price = item.produs.pret_unitar
            quantity = item.cantitate

            item_total_price = product_price * quantity
            print(item.produs.images.imagine_catalog)
            print(item.produs.images.imagine_catalog)
            print(item.produs.images.imagine_catalog)
            print(item.produs.images.imagine_catalog)
            print(item.produs.images.imagine_catalog)
            print(item.produs.images.imagine_catalog)

            total_price += item_total_price

            cart_items_with_totals.append({
                'item': item,
                'item_total_price': item_total_price,
                'product_price': product_price,
                'quantity': quantity,
                'item_image': item.produs.images.imagine_catalog,
            })

        # Create entries in the OrderProducts table
        for item in cart_items_with_totals:
            print("HELLLLO")
            print(item['item_image'])
            product = get_object_or_404(Produse, produs_id = item['item'].produs.produs_id)
            order_product = ProduseComenzi(
                comanda = order,
                produs = product,
                cantitate_comanda = item['quantity']
            )
            order_product.save()

        # Retrieve the necessary addresses for storage and informing the user via email
        billing_address = session.get('customer_details', {}).get('address')
        shipping_address = session.get('shipping_details', {}).get('address')

        # Get values from the address dictionaries
        billing_address_info = billing_address.values()
        shipping_address_info = shipping_address.values()

        # Send the confirmation email to the provided address, if it exists
        if customer_email:
            send_confirmation_email(customer_email,
                                    cart_items_with_totals,
                                    total_price,
                                    client_instance,
                                    billing_address_info,
                                    shipping_address_info)

        # Delete the Cart entries that the customer paid for
        Cosuri.objects.filter(client=client_instance).delete()

    return JsonResponse({'status': 'success'}, status=200)