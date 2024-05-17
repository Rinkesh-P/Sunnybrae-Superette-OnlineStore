from django.shortcuts import render
from .models import * 
from django.core.paginator import Paginator #Paginator should divide the product page so that it shows x amount of products per page rather than all the products on the page
# Create your views here.
def product(request):
    products = Product.objects.all()
    
    paginator = Paginator(products, 6) #limits it to x products per page #setting to 6 for testing purposes 
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
        
    #context = {'products':products} 
    context = {'page_object':page_object} #should render the page with x products as opposed to all products 
    
    return render (request, 'store/product.html', context)

def faq(request):
    context = {}
    return render (request, 'store/faq.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total":0, "get_cart_items":0}
        
    context = {'items':items, 'order': order}
    return render (request, 'store/cart.html', context)
