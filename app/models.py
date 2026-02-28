from django.db import models
from django.contrib.auth.models import User

class rege(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30,unique=True)
    password=models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class emform(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    subject=models.CharField(max_length=30)
    message=models.TextField()    

    def __str__(self):
        return self.first_name


class category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class products(models.Model):
    category=models.ForeignKey(category, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description=models.TextField()
    stock = models.IntegerField(default=0)
    image=models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)

    def __str__(self):  
        return self.name
    
    @property
    def double_price(self):
        return self.price * 2


class cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    
    def __str__(self):
        return f"Cart of {self.user.username}"
    

class cart_item(models.Model):
    cart=models.ForeignKey(cart, on_delete=models.CASCADE)
    product=models.ForeignKey(products, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)


    @property
    def total_product_price(self):
        return self.product.price * self.quantity
    
    


    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart}"
    

class address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15)
    address=models.TextField()
    city=models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode=models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)


class order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    address_data=models.ForeignKey(address, on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2)
    payment_id=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100)
    signature=models.CharField(max_length=100)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending') 
    created_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} for {self.user.username}"
    
class orderitem(models.Model):
    order_data=models.ForeignKey(order, on_delete=models.CASCADE)    
    product=models.ForeignKey(products, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price = models.FloatField()


    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.order_data}"

   


   






