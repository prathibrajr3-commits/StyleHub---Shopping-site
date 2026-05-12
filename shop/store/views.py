import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import (
    Product, Category, Cart, CartItem,
    Order, OrderItem, NewsletterSubscriber, ContactMessage, BlogPost
)


# ─── Helpers ────────────────────────────────────────────────────────────────

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


# ─── Pages ──────────────────────────────────────────────────────────────────

def home(request):
    featured = Product.objects.filter(is_featured=True, stock__gt=0)[:8]
    new_arrivals = Product.objects.filter(is_new_arrival=True, stock__gt=0)[:8]
    categories = Category.objects.all()
    context = {
        'featured_products': featured,
        'new_arrivals': new_arrivals,
        'categories': categories,
    }
    return render(request, 'store/index.html', context)


def shop(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()

    # Filters
    category_slug = request.GET.get('category')
    gender = request.GET.get('gender')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'newest')
    search = request.GET.get('q')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if gender:
        products = products.filter(gender=gender)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search) |
            Q(description__icontains=search)
        )

    sort_map = {
        'newest': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'rating': '-rating',
    }
    products = products.order_by(sort_map.get(sort, '-created_at'))

    active_category = None
    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()

    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'current_gender': gender,
        'current_sort': sort,
        'search_query': search,
        'total_count': products.count(),
    }
    return render(request, 'store/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).filter(stock__gt=0)[:4]
    context = {
        'product': product,
        'related_products': related,
        'sizes': product.sizes_list,
    }
    return render(request, 'store/product.html', context)


def cart_view(request):
    cart = get_or_create_cart(request)
    context = {'cart': cart}
    return render(request, 'store/cart.html', context)


def checkout(request):
    cart = get_or_create_cart(request)
    if cart.is_empty:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    if request.method == 'POST':
        return process_order(request, cart)
    context = {'cart': cart}
    return render(request, 'store/checkout.html', context)


def process_order(request, cart):
    data = request.POST
    # Validate required fields
    required = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'pincode']
    for field in required:
        if not data.get(field, '').strip():
            messages.error(request, f'{field.replace("_", " ").title()} is required.')
            return render(request, 'store/checkout.html', {'cart': cart})

    shipping = Decimal('0') if cart.total_price >= 500 else Decimal('49')
    order = Order.objects.create(
        session_key=request.session.session_key,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address'],
        city=data['city'],
        state=data['state'],
        pincode=data['pincode'],
        payment_method=data.get('payment_method', 'cod'),
        notes=data.get('notes', ''),
        subtotal=cart.total_price,
        shipping=shipping,
        total=cart.total_price + shipping,
    )

    for item in cart.items.select_related('product'):
        # Reduce stock
        product = item.product
        product.stock = max(0, product.stock - item.quantity)
        product.save(update_fields=['stock'])

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            product_price=product.price,
            size=item.size,
            quantity=item.quantity,
            subtotal=item.subtotal,
        )

    # Clear cart
    cart.items.all().delete()

    return redirect('order_success', order_number=order.order_number)


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'store/order_success.html', {'order': order})


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactMessage.objects.create(
                name=name, email=email,
                subject=subject or 'General Enquiry',
                message=message
            )
            messages.success(request, "Thanks! We'll get back to you within 24 hours.")
        else:
            messages.error(request, 'Please fill in all required fields.')
        return redirect('contact')
    return render(request, 'store/contact.html')


def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'store/blog.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related = BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3]
    return render(request, 'store/blog_detail.html', {'post': post, 'related': related})


# ─── Cart API (AJAX) ─────────────────────────────────────────────────────────

@require_POST
def cart_add(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        size = data.get('size', '')

        product = get_object_or_404(Product, id=product_id)
        if not product.is_in_stock():
            return JsonResponse({'success': False, 'error': 'Product is out of stock.'})
        if quantity < 1:
            quantity = 1
        if quantity > product.stock:
            quantity = product.stock

        cart = get_or_create_cart(request)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, size=size,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity = min(item.quantity + quantity, product.stock)
            item.save()

        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" added to cart!',
            'cart_count': cart.total_items,
            'cart_total': str(cart.total_price),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def cart_update(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))

        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if quantity <= 0:
            item.delete()
        else:
            item.quantity = min(quantity, item.product.stock)
            item.save()

        cart.refresh_from_db()
        return JsonResponse({
            'success': True,
            'item_subtotal': str(item.subtotal) if quantity > 0 else '0',
            'cart_total': str(cart.total_price),
            'cart_count': cart.total_items,
            'removed': quantity <= 0,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def cart_remove(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        cart.refresh_from_db()
        return JsonResponse({
            'success': True,
            'cart_total': str(cart.total_price),
            'cart_count': cart.total_items,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def newsletter_subscribe(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required.'})
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            return JsonResponse({'success': True, 'message': 'Subscribed! Welcome aboard 🎉'})
        else:
            subscriber.is_active = True
            subscriber.save()
            return JsonResponse({'success': True, 'message': "You're already subscribed!"})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
