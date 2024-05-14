from django.shortcuts import render

# Create your views here.
def product(request):
    context = {}
    return render (request, 'store/product.html', context)

def faq(request):
    context = {}
    return render (request, 'store/faq.html', context)

def cart(request):
    context = {}
    return render (request, 'store/cart.html', context)
