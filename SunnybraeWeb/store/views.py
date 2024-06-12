from django.shortcuts import render, redirect
from django.core.paginator import Paginator #Paginator should divide the product page so that it shows x amount of products per page rather than all the products on the page
from django.http import JsonResponse, QueryDict
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import LoginForm, RegisterForm, GuestCheckoutForm, RegisteredCheckoutForm
from .models import * 
import json




# Create your views here.


def product(request): 
    query = request.GET.get('search') #check if there is a search query, from the URL Parameters 
    category_id = request.GET.get('category') #Get the category filter from the URL Parameters 
    products = Product.objects.all() 
    
    if query: 
        products = Product.objects.filter(item_name__icontains=query) #get all products that contain the searched word in it 

    
    if category_id: #get all the category_id if the user clicks on the dropdown 
        products = Product.objects.filter(category_id=category_id) 
    
    
    
    paginator = Paginator(products, 9) #limits it to x products per page in this case 9 products per page
    page_number = request.GET.get('page') #Get current page number from the URL Parameters 
    page_object = paginator.get_page(page_number) #Get the page object for current page 
    

    
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

    
    #Return to the Product.html page the logic for searching, filtering and pagination 
    
    return render (request, 'store/product.html', context)

def faq(request):
    context = {}
    return render (request, 'store/faq.html', context)

def checkout(request):
    order = None
    customer = None 
    
    #Get the session from the cart page. 
    session_cart = request.session.get('cart', {})
    
    #Check if cart is empty or not. If empty then can't have the user checking out so warn the user. 
    if not session_cart:
        messages.warning(request, "Cart Empty. Add before continuing")
        return redirect('cart')
    
    #if user is logged in then get their customer details and get/create a incomplete order for this customer. 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        form = RegisteredCheckoutForm
        intial_form_details = {'customer': customer} #prepare the initial form details with customer information 
        
    #if its an customer that isn't logged in then, retrieve guest email if available from the session cart
    else: 
        guest_email = session_cart.get('email')
        form = GuestCheckoutForm
        intial_form_details = {}
    
        if guest_email: #if guest email is available then create/ get the Customer and incomplete Order 
            customer, created = Customer.objects.get_or_create(email=guest_email, defaults={'name': 'Guest'})
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

    #Form Submission 
    if request.method == 'POST': 
        form = form(request.POST, initial=intial_form_details)
        if form.is_valid():
            checkout_info = form.save(commit=False) #Save form but don't commit to the database 
            if not request.user.is_authenticated: 
                #if user is not authenticated eg a guest user then get their details and save it to the session and then create/get customer associated with that email
                guest_email = form.cleaned_data['guest_email']
                request.session['cart']['email'] = guest_email
                request.session.modified = True
                customer, created = Customer.objects.get_or_create(email=guest_email, defaults={'name': 'Guest'})
                if not order:
                    order, created = Order.objects.get_or_create(customer=customer, complete=False)

            #Save the Customer and Order info and save to database. 
            checkout_info.customer = customer
            checkout_info.order = order
            checkout_info.save()
            
            #If guest user then we need to create the OrderItem (relationship between order and product) for the database so that we can save it to the database and retrieve later when needed.
            if not request.user.is_authenticated:
                session_cart = request.session.get('cart', {})
                for product_id, quantity in session_cart.items(): #get the items from the current session cart 
                    if product_id != 'email':  #ignore the email key in session cart 
                        product = Product.objects.get(item_id=product_id)
                        OrderItem.objects.create(order=order, product=product, quantity=quantity) #Create the OrderItem record 
                        
            #Mark order as complete and update payment status             
            order.complete = True 
            order.payment_status = 'Mock Payment Completed'
            order.save()  
            
            return redirect('order_confirmation')
    else:
        #If the request Method isn't POST then intialise the form with with the intial details 
        form = form(initial=intial_form_details)
    
    items = order.orderitem_set.all() if order else [] #Get the order items for the order if it exists else a empty list
             
    context = {'items': items, 'order': order, 'form': form}
    return render(request, 'store/checkout.html', context)

def order_confirmation(request):
    customer = None #Set the customer to None 
    
    #If the user is logged in then get the customer details for them otherwise get the customer details from the session for a guest user
    if request.user.is_authenticated: 
        customer = request.user.customer
    else:
        session_cart = request.session.get('cart', {})
        guest_email = session_cart.get('email')
        #If a guest email is present in the session then get the customer associated with that email from the database 
        if guest_email: 
            customer = Customer.objects.get(email=guest_email) 
    
    #If customer exists then find the latest order for that customer which is complete. 
    if customer:
        order = Order.objects.filter(customer=customer, complete=True).latest('date_ordered')
    else:
        order = None

    if not request.user.is_authenticated:
        request.session['cart'] = {}
        
    context = {'order': order}
    return render(request, 'store/order_confirmation.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user = request.user) #when a user registers have to make sure that a customer object is also created or retrieved so that that user can then shop 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        #if user is not authenticated i.e. a guest user then get the cart from the session
        session_cart = request.session.get('cart', {}) 
        items = []
        order = {"get_cart_total":0, "get_cart_items":0}
        
        #Go through each item in the session cart and get its productId and quantity 
        
        for productId, quantity in session_cart.items(): 
            product = Product.objects.get(item_id=productId) #get the product from the database by matching the product id to the item_id
            total = product.current_price * quantity 
            order['get_cart_items'] += quantity #add quantity of current product to the total number of products in the cart
            order['get_cart_total'] += total #add the $total of current product to the $total of the cart 
            item = { #details of the current product 
                'product':{
                    'item_id': product.item_id,
                    'item_name': product.item_name,
                    'current_price': product.current_price
                },
                'quantity': quantity,
                'get_total': total, 
            }
            items.append(item) #append each item to the items list
        
        
    context = {'items':items, 'order': order}
    return render (request, 'store/cart.html', context)

def updateItem(request):
    data = json.loads(request.body) 
    productId = data['productId']
    action = data['action']
    
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
    #If user logs in check if the exists in the database and if they do then log them in and re direct to the product page. 
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
    #When user clicks on the register button then take the data from the form and store the information in the database then log them in and redirect to the product page. 
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
    #When user logsout redirect them back to the main page
    logout(request)
    return redirect('product') 

