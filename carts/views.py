from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from carts.models import Cart, CartItem
from store.models import Product, Variation

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
    product_variation = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                #Check is key value pair from POST is present in the Variation db
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

        # color = request.POST["color"]
        # size = request.POST["size"]
        # print(color, size)

    #Gets cart, creates one if none
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
        cart_id = _cart_id(request)
        )
    cart.save()

    #Gets cart_item and increments quantity by 1 if it is a match, creates one if none
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
      
        #Check if item matches a previously added variation
        existing_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_var_list.append(list(existing_variation)) 
            id.append(item.id)


        #If true: increment quantity 
        if product_variation in existing_var_list:
           index = existing_var_list.index(product_variation)
           item_id = id[index]
           item = CartItem.objects.get(product=product, id=item_id)
           item.quantity += 1
           item.save()

        #If false: create a new cart item
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            #Add variations to each cart_item
            if len(product_variation) > 0:
                item.variations.clear() #clears previous interation's variations
                item.variations.add(*product_variation)

            item.save()

    #If matching cart_item does not exist, create one
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )

        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
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
