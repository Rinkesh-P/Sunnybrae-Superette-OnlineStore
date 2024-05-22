from django.shortcuts import render
from .models import * 
from django.core.paginator import Paginator #Paginator should divide the product page so that it shows x amount of products per page rather than all the products on the page
from django.http import JsonResponse
import json

# Create your views here.
def product(request):
    products = Product.objects.all()
    
    paginator = Paginator(products, 9) #limits it to x products per page 
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    print(page_object.number, " PAGE OBJECT PRINTED HERE ")
    
    context = {'page_object':page_object} #should render the page with x products as opposed to all products 
    print ("CONTEXT ---------------- ",  context) 
    
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

def updateItem(request):
    data = json.loads(request.body)
    print("------------------------------- data ------------------------- ", data) #check if the request is returning the correct values 
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    #print(customer)
    
    product = Product.objects.get(item_id=productId) #match product with the product in the database 
    order, created = Order.objects.get_or_create(customer=customer, complete=False) #get current order for customer and if order doesnt exist then create one 

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) #get the OrderItem associated with the order if none exist then create one

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'delete':
        orderItem.delete()
        return JsonResponse('Item was deleted', safe=False)

    orderItem.save()

    if orderItem.quantity <= 0: #ensure that there is no items with a quanity value of zero in the cart 
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
