from .models import cart, cart_item

def cart_count_all(request):
    count = 0
    if request.user.is_authenticated:
        user_cart = cart.objects.filter(user=request.user).first()
        if user_cart:
            items = cart_item.objects.filter(cart=user_cart)
            for i in items:
                count += i.quantity
    return {'cart_total_count': count}