from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Category
from .forms import OrderForm, RegistrationForm
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# 1. Головна сторінка (+ ПОШУК і ФІЛЬТРИ)
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # ПОШУК
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # ФІЛЬТР ПО КАТЕГОРІЇ
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    
    return render(request, 'store/home.html', {
        'products': products, 
        'cart_count': cart_count,
        'categories': categories, # Передаємо категорії в шаблон
    })

# ... (тут функції product_detail, cart_view, add_to_cart, remove_from_cart залишаються без змін) ...
# ... (скопіюй їх зі старого файлу або залиш як є, якщо не видаляв) ...
# Я продублюю коротко, щоб ти не заплутався, але головне - не видали їх випадково.

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'store/product_detail.html', {'product': product, 'cart_count': cart_count})

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total = quantity * product.price
        total_price += total
        cart_items.append({'product': product, 'quantity': quantity, 'total': total})
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart: cart[product_id] += 1
    else: cart[product_id] = 1
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] == 0: del cart[product_id]
    request.session['cart'] = cart
    return redirect('cart')

def checkout(request): # (Залиш функцію checkout як була)
    cart = request.session.get('cart', {})
    if not cart: return redirect('home')
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.price * quantity
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated: # Якщо увійшов - прив'язуємо
                order.buyer = request.user
            # Якщо гість, то поле buyer може бути null (треба дозволити в моделях) або вимагати вхід
            # Для простоти поки залишимо як є.
            order.total_price = total_price
            order.save()
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            request.session['cart'] = {}
            return render(request, 'store/success.html')
    else:
        form = OrderForm()
    return render(request, 'store/checkout.html', {'form': form, 'total_price': total_price})


# --- НОВІ ФУНКЦІЇ АВТОРИЗАЦІЇ ---

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Одразу входимо після реєстрації
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')