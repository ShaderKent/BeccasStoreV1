from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from carts.models import Cart, CartItem
from store.models import Product

TAX_RATE = 0.07

class CartView (TemplateView):
    model = Cart
    template_name = "cart.html"
    context_object_name = "carts"
    ordering = ["-created_date"]


#Gets current cart ID (session_id) / Makes one if not present
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    #Gets cart, creates one if none
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
        cart_id = _cart_id(request)
        )
    cart.save()

    #Gets cart_item and increments quantity by 1, creates one if none
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()

    #Sends user to their cart page
    return redirect("carts:cart")

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product  = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("carts:cart")

def delete_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product  = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("carts:cart")

def clear_cart(request):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    try:
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            cart_item.delete()
    except: 
        pass
    return redirect("carts:cart")

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.sub_total()
            quantity += cart_item.quantity

        tax = total * TAX_RATE
        grand_total = total + tax
        formatted_tax = f"{tax:10.2f}"
        formatted_total = f"{total:10.2f}"
        formatted_grand_total = f"{grand_total:10.2f}"
    except:
        pass

    context = { 
        "tax": formatted_tax,
        "total": formatted_total,
        "grand_total": formatted_grand_total,
        "quantity": quantity,
        "cart_items": cart_items,
    }

    return render(request, "cart.html", context)
