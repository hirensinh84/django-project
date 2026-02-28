from django.shortcuts import render, redirect
from .models import emform,rege,category,products,cart,cart_item,address,order,orderitem
from django.contrib import messages
import re
from django.conf import settings
import razorpay
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'app/index.html')

def product(request):
    products_list=products.objects.all()
    paginator = Paginator( products_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/product.html' ,{'products':products_list, 'page_obj': page_obj})

def product_detail(request, pk):
    product = products.objects.get(id=pk)
    return render(request, 'app/products_detail.html', {'product': product})    


def login(request):

    
    if request.method == 'POST':
        email = request.POST.get('l_email')
        password = request.POST.get('l_password')

        check=authenticate(request, username=email, password=password)

        if check is not None:
            auth_login(request, check)
            messages.success(request, f"Welcome back, {email}!")
            return redirect('home')
        else:
            messages.error(request,"Invalid email or password. Please try again.")
    return render(request, 'app/login.html')

def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again." )
        else:
                
            if User.objects.filter(username=email).exists():
               messages.error(request, "Email already registered! Please use a different email.")
               return render(request, 'app/registration.html')

            if User.objects.filter(email=email).exists():
               messages.error(request, "Email already registered! Please use a different email.")
               return render(request, 'app/registration.html')
        
            datacreate=User.objects.create_user(
            username=email,
            email=email,
            password=password
             )
            datacreate.first_name = first_name
            datacreate.last_name = last_name
            datacreate.save()
            messages.success(request,"Account created successfully! You can now log in.")
            return redirect('login')
    return render(request, 'app/registration.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            emform.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('home')
        except Exception as e:
            messages.error(request, "An error occurred while sending your message. Please try again.")
            return render(request, 'app/contact.html')
    return render(request, 'app/contact.html')

def about(request):
    return render(request, 'app/about.html')

def change(request):
    return render(request, 'app/change.html')
def forget(request):
    return render(request, 'app/forget_password.html')

@login_required
def oldpass_view(request):
    if request.method == 'POST':
        oldpass = request.POST.get("old_password")
        newpass = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_password")

        if newpass != confirm_new_password:
            messages.error(request, "New passwords do not match. Please try again.")
            return render(request, 'app/oldpass.html')
        else:
             user = request.user
             if user.check_password(oldpass):
               user.set_password(newpass)
               user.save()
               update_session_auth_hash(request, user)
               messages.success(request, "Password updated successfully!")
               return redirect('login')
             else:
               messages.error(request, "Old password is incorrect. Please try again.")
    return render(request, 'app/oldpass.html')

def myprofile_view(request):
    return render(request, 'app/myprofile.html')

def add_to_cart(request, pk):
    
    if not request.user.is_authenticated:
        return redirect('login')

    product1 = products.objects.get(id=pk)

    try:
        user_cart = cart.objects.get(user=request.user)
    except cart.DoesNotExist:
        user_cart = cart.objects.create(user=request.user)    

    try:
        cart_item_data = cart_item.objects.get(cart=user_cart, product=product1)
        cart_item_data.quantity += 1    
        cart_item_data.save()
    except cart_item.DoesNotExist:
        cart_item.objects.create(cart=user_cart, product=product1, quantity=1)
    return redirect('view_cart')

def view_cart(request):
    
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user_cart = cart.objects.get(user=request.user)
        all_cart_items = cart_item.objects.filter(cart=user_cart)
    except cart.DoesNotExist:
        all_cart_items = []

    grand_total = 0
    for item in all_cart_items:
        price_of_this_item = item.quantity * item.product.price
        grand_total = grand_total + price_of_this_item

    return render(request, 'app/cart.html', {
        "product": all_cart_items,
        "grand_total": grand_total
    })

def remove_cart_item(request, pk):
    
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user_cart=cart.objects.get(user=request.user)
    except cart.DoesNotExist:
        messages.error(request, "You don't have a cart.")
        return redirect('product')

    try:
        cart_item_data=cart_item.objects.get(cart=user_cart, id=pk)
        cart_item_data.delete()
        messages.success(request, "Item removed from cart.")
    except cart_item.DoesNotExist:
        messages.error(request, "Cart item not found.")
    return redirect('view_cart')

def decrease_quantity(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user_cart=cart.objects.get(user=request.user)
    except cart.DoesNotExist:
        messages.error(request, "You don't have a cart.")
        return redirect('product')

    try:
        cart_item_data=cart_item.objects.get(cart=user_cart, id=pk)
        if cart_item_data.quantity > 1:
            cart_item_data.quantity -= 1
            cart_item_data.save()
      
    except cart_item.DoesNotExist:
        messages.error(request, "Cart item not found.")
    return redirect('view_cart')

def increase_quantity(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user_cart=cart.objects.get(user=request.user)
    except cart.DoesNotExist:
        messages.error(request, "You don't have a cart.")
        return redirect('product')

    try:
        cart_item_data=cart_item.objects.get(cart=user_cart, id=pk)
        if cart_item_data.quantity< cart_item_data.product.stock:
           cart_item_data.quantity += 1
           cart_item_data.save()
    except cart_item.DoesNotExist:
        messages.error(request, "Cart item not found.")
    return redirect('view_cart')

def checkout_view(request):
    return render(request, 'app/checkout.html')

def address_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method =='POST':
        full_name=request.POST.get('full_name')
        phone_number=request.POST.get('mobile')
        address_get=request.POST.get('address_line')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
       
        address.objects.create(
            user=request.user,
            full_name=full_name,
            mobile_number=phone_number,
            address=address_get,
            city=city,
            state=state,
            pincode=pincode 
        )
        return redirect('address')
    
    user_addresses = address.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addresses': user_addresses})


def delete_address(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
       address_data=address.objects.filter(user=request.user, id=pk)
       address_data.delete()
       messages.success(request, "Address deleted successfully.")
    except address.DoesNotExist:
       messages.error(request, "Address not found.")
    return redirect('address')   


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    active_user=request.user

    user_addresses = address.objects.filter(user=request.user)
    user_cart_item=cart_item.objects.filter(cart=cart.objects.get(user=request.user))

    grand_total = 0
    for item in  user_cart_item:
        price_of_this_item = item.quantity * item.product.price
        grand_total = grand_total + price_of_this_item

    print(grand_total)



    # razorpay mate
    # connect
    client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    amount_in_paise = int(grand_total * 100)

    print(amount_in_paise)

    data={
        "amount": amount_in_paise,
        "currency": "INR",
        "payment_capture": "1"

    }

    # razorpay ma orders create
    razorpay_order=client.order.create(data=data)

    # order id create
    razorpay_order_id= razorpay_order["id"]

    context={
        "razorpay_order_id": razorpay_order_id,
        "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
        "razorpay_amount": amount_in_paise,
        "currency": "INR",
    }


    return render(request, 'app/checkout.html', {'addresses': user_addresses, 'products': user_cart_item ,'grand_total': grand_total,"context": context, "active_user": active_user})

def payment_succes_view(request):
    if request.method == 'POST':
        data=json.loads(request.body)

        payment_id=data.get("razorpay_payment_id")
        order_id=data.get("razorpay_order_id")
        signature=data.get("razorpay_signature")
        selected_addressId=data.get("address_id")

        params={
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": order_id,
            "razorpay_signature": signature
        }

        address_obj=address.objects.get(id=selected_addressId)
        user_cart=cart.objects.get(user=request.user)
        user_cart_item=cart_item.objects.filter(cart=user_cart)

        grand_total = 0
        for item in  user_cart_item:
            price_of_this_item = item.quantity * item.product.price
            grand_total = grand_total + price_of_this_item



        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature(params)
            new_order= order.objects.create(
                user=request.user,
                address_data= address_obj,
                total_amount=grand_total,
                payment_id= payment_id,
                order_id=order_id,
                signature=signature,
                payment_status=True
            )
            for item in user_cart_item:
                orderitem.objects.create(
                    order_data=new_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price

                )
            user_cart_item.delete()
            return JsonResponse({"status": "success"})
       
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "failure"})
    return redirect('app/order_detail.html')

def order_detail_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
# 
    # user_orders=order.objects.filter(user=request.user)
    return render(request, 'app/order_detail.html')

   