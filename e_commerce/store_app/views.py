from django.shortcuts import render
from django.http import JsonResponse
import json
from django.db.models import Q
from .models import *

# Create your views here.

def home(request):
    return render(request, 'pages/home.html')

def shopping_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context= {'items': items, 'order': order}
    return render(request, 'pages/shopping_cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        
    context= {'items': items, 'order': order}
    return render(request, 'pages/checkout.html', context)

def tee_shirts(request):
    products = Product.objects.filter(price__lt=20)
    context = {'products' : products}
    return render(request, 'pages/tee_shirts.html', context)

def hoodies(request):
    products = Product.objects.filter(price__gte=50)
    context = {'products' : products}
    return render(request, 'pages/hoodies.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added.', safe=False)


def product_by_id(request,id):
    product = Product.objects.get(id = id)
    return render(request, 'pages/product.html', {'product': product})

def search(request):
    query = request.GET.get('q')
    print('q')
    products = Product.objects.filter(Q(name__icontains=query) | Q(digital__icontains=query) | Q(price__icontains=query)) if query else []
    context = {'products': products, 'query': query}
    return render(request, 'pages/search.html', context)