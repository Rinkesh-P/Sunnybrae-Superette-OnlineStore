from django.shortcuts import render
from .models import * 
# Create your views here.
def product(request):
    products = Product.objects.all()
    context = {'products':products}
    return render (request, 'store/product.html', context)

def faq(request):
    context = {}
    return render (request, 'store/faq.html', context)

def cart(request):
    context = {}
    return render (request, 'store/cart.html', context)
