from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from carts.models import CartItem
from carts.views import _cart_id
from store.models import Product

class StoreView (ListView):
    model = Product
    template_name = "store.html"
    context_object_name = "products"
    ordering = ["-created_date"] 
    queryset = Product.objects.all().filter(is_available=True)
    
class CategoryView (ListView):
    model = Product
    template_name = "store.html"
    context_object_name = "products"
    ordering = ["-created_date"]
    
    def get_queryset(self, *args, **kwargs):
        return Product.objects.filter(category__slug__icontains=self.kwargs.get("category_name"), is_available=True)
        
class DetailedProductView (DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = "product"
    
    def get_context_data(self,**kwargs):
        context = super(DetailedProductView, self).get_context_data(**kwargs)
        current_product = Product.objects.get(slug=self.kwargs.get("slug"))
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(self.request), product=current_product).exists()
        context['in_cart'] = in_cart
        return context


    