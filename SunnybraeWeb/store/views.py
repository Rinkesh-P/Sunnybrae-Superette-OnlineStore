from django.shortcuts import render
from .models import * 
from django.core.paginator import Paginator #Paginator should divide the product page so that it shows x amount of products per page rather than all the products on the page
# Create your views here.
def product(request):
    products = Product.objects.all()
    
    paginator = Paginator(products, 60) #limits it to x products per page #setting to 6 for testing purposes 
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
        
    #context = {'products':products} 
    context = {'page_object':page_object} #should render the page with x products as opposed to all products 
    
    return render (request, 'store/product.html', context)

def faq(request):
    context = {}
    return render (request, 'store/faq.html', context)

def cart(request):
    context = {}
    return render (request, 'store/cart.html', context)
