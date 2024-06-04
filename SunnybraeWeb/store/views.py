from django.shortcuts import render, redirect
from .models import * 
from django.core.paginator import Paginator #Paginator should divide the product page so that it shows x amount of products per page rather than all the products on the page
from django.http import JsonResponse, QueryDict
import json

from .forms import LoginForm, RegisterForm, CheckoutForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Customer




# Create your views here.
def product(request): 
    query = request.GET.get('search') #check if there is a search result, if there is then filter and display that result 
    category_id = request.GET.get('category') #assign the drop down for All Categories to category_id 
    products = Product.objects.all() 
    
    if query: 
        products = Product.objects.filter(item_name__icontains=query) #get all products that contain the searched word in it 
        print(f"Search query: {query}")  # Print the search query to test to see if it is printing properly
        print("Search results:") 
        for product in products:
            print(f"- {product.item_name}")  
    
    if category_id: #get all the category_id if the user clicks on the dropdown 
        products = Product.objects.filter(category_id=category_id) 
    
    
    
    paginator = Paginator(products, 9) #limits it to x products per page 
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    # if query: #need to retain the search results when the user clicks on the next page for paginator 
    #     query_dict = QueryDict(mutable=True)
    #     query_dict['search'] = query
    #     query_string = query_dict.urlencode()
    #     for page in page_object.paginator.page_range:
    #         page_object.paginator.page(page).query_string = query_string    
    # #print(page_object.number, " PAGE OBJECT PRINTED HERE ")
    
    # if category_id:
    #     category_id_dict = QueryDict(mutable=True)
    #     category_id_dict['category'] = category_id
    #     query_string = category_id_dict.urlencode()
    #     for page in page_object.paginator.page_range:
    #         page_object.paginator.page(page).query_string = query_string  
    
    query_dict = QueryDict(mutable=True)  #need to retain the search results/ category id when the user clicks on the next page for paginator 
    if query:
        query_dict['search'] = query
    if category_id:
        query_dict['category'] = category_id
    query_string = query_dict.urlencode()

    for page in page_object.paginator.page_range: #limit the paginator to only the products which are returned in query_string 
        page_object.paginator.page(page).query_string = query_string  
    
    

    categories = Product.objects.values_list('category_id', flat=True).distinct() #list of all the distinct category_id in the product table 
    categories = sorted(categories) 
    
    context = {
        'page_object':page_object, 
        'query': query, 
        'categories':categories,  
        'selected_category': int(category_id) if category_id else None, 
        'query_string': query_string, 
    } 
    #should render the page with x products as opposed to all products 
    #print ("CONTEXT ---------------- ",  context) 
    
    return render (request, 'store/product.html', context)

def faq(request):
    context = {}
    return render (request, 'store/faq.html', context)

def checkout(request):
    
    guest_customer = Customer() 
    order = None

    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        session_checkout = request.session.get('cart', {})
        if session_checkout:
            guest_email = session_checkout.get('email')
            guest_customer, created = Customer.objects.get_or_create(email=guest_email, defaults={'name': 'Guest'})
            customer = guest_customer
    
    if customer:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    items = order.orderitem_set.all() if order else []

    if request.method == 'POST':
        form = CheckoutForm(request.POST) 
        if form.is_valid():
            checkout_info = form.save(commit=False)
            checkout_info.customer = customer
            checkout_info.order = order
            checkout_info.save()
            order.complete = True 
            order.payment_status = 'Mock Payment Completed'
            order.save() 
            
            if not request.user.is_authenticated:
                request.session['cart'] = {}
            
            return redirect('order_confirmation')
    else:
        form = CheckoutForm()  
             
    context = {'items': items, 'order': order, 'form': form}
    return render(request, 'store/checkout.html', context)



def order_confirmation(request):
    context = {}
    return render (request, 'store/order_confirmation.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user = request.user) #when a user registers have to make sure that a customer object is also created or retrieved so that that user can then shop 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        session_cart = request.session.get('cart', {}) #if user is not authenticated i.e. a guest user then get the cart from the session
        items = []
        order = {"get_cart_total":0, "get_cart_items":0}
        
        
        for productId, quantity in session_cart.items(): 
            product = Product.objects.get(item_id=productId)
            total = product.current_price * quantity
            order['get_cart_items'] += quantity
            order['get_cart_total'] += total 
            item = {
                'product':{
                    'item_id': product.item_id,
                    'item_name': product.item_name,
                    'current_price': product.current_price
                },
                'quantity': quantity,
                'get_total': total, 
            }
            items.append(item)
        
        
    context = {'items':items, 'order': order}
    return render (request, 'store/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    #print("------------------------------- data ------------------------- ", data) #check if the request is returning the correct values 
    productId = data['productId']
    action = data['action']

    #customer = request.user.customer
    #print(customer)
    
    if request.user.is_authenticated: #if the user is already registered 
        customer, created = Customer.objects.get_or_create(user=request.user)
        product = Product.objects.get(item_id=productId) #match product with the product in the database 
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #get current order for customer and if order doesnt exist then create one 
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) #get the OrderItem associated with the order if none exist then create one
        
        #actions will update the Database 
        
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
    
    else: #if user is a guest 
        session_cart = request.session.get('cart',{})
        
        #actions will only update the session which can be reset 
        if action == 'add': 
            if productId in session_cart:
                session_cart[productId] += 1
            else:
                session_cart[productId] = 1
                
        elif action == 'remove':
            if productId in session_cart:
                session_cart[productId] -= 1
                if session_cart[productId] <= 0:
                    del session_cart[productId]
        
        elif action == 'delete':
            if productId in session_cart:
                del session_cart[productId]
        
        request.session['cart'] = session_cart
        
        

    return JsonResponse('Item was added', safe=False)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product')
    else:
        form=LoginForm()
         
    return render (request, 'store/login.html', {'form':form})


def user_register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, name=user.username, email=user.email)
            login (request, user)
            return redirect('product')
    else:
        form = RegisterForm()
    return render (request, 'store/register.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('product') 

