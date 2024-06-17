from django.db import models
from django.contrib.auth.models import User

"""

Models for the database to use, Customer, Order, OrderItem and CheckoutInfo 


"""

#Customer class where each customer will be linked to a single User
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name


#Poduct class to represent a Product in the database 
class Product(models.Model):
    item_id = models.IntegerField(null=False, blank=True, primary_key=True)
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    category_id = models.IntegerField()
    current_price = models.FloatField()
    
    def __str__(self):
        print(f"Product: {self.item_name}")
        return self.item_name

#Order class to represent an order that a customer makes. 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    shipping_status = models.CharField(max_length=50, null=True, default='Pending')
    payment_status = models.CharField(max_length=50, null=True, default='Pending')
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

#OrderItem class to represent an item in an Order, 
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.current_price * self.quantity
        return total 

#CheckoutInfo used to represent the Checkout information for an order when a customer goes to checkout. 
class CheckoutInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    suburb = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)