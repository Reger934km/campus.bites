from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import MenuItem, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .templatetags.cart_extras import get_item


def home(request):
    return render(request, 'canteen/home.html')
def about(request):
    return render(request, 'canteen/about.html')

def contact(request):
    return render(request, 'canteen/contact.html')

form = UserCreationForm()
for field in form.fields.values():
    field.help_text = ''



@login_required
def menu(request):
    items = MenuItem.objects.all()
    cart_items = {}
    if request.user.is_authenticated:
        user_cart_items = CartItem.objects.filter(user=request.user)
        cart_items = {item.item.id: item for item in user_cart_items}
    return render(request, 'canteen/menu.html', {'items': items, 'cart_items': cart_items})

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    action = request.POST.get('action')
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)

    if action == 'add':
        cart_item.quantity = 1
    elif action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return redirect('menu')
    cart_item.save()
    return redirect('menu')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'canteen/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def checkout_view(request):
    return render(request, 'canteen/checkout.html')

@login_required
def place_order(request):
    # Get cart items for the current user
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    # Calculate total price
    total_price = sum(item.total_price() for item in cart_items)
    
    # Clear cart after order placement
    cart_items.delete()
    
    messages.success(request, f'Order placed successfully! Total: ₹{total_price}')
    return redirect('menu')

def serve_media(request, path):
    """Custom view to serve media files in production"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read())
            
        # Set appropriate content type based on file extension
        if path.endswith('.jpg') or path.endswith('.jpeg'):
            response['Content-Type'] = 'image/jpeg'
        elif path.endswith('.png'):
            response['Content-Type'] = 'image/png'
        elif path.endswith('.gif'):
            response['Content-Type'] = 'image/gif'
        else:
            response['Content-Type'] = 'application/octet-stream'
            
        return response
    else:
        return HttpResponse('File not found', status=404)

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'canteen/profile.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in user after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})














# Create your views here.
