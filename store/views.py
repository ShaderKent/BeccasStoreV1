from django.views.generic import ListView
from .models import Product

class StoreView (ListView):
    model = Product
    template_name = "store.html"
    context_object_name = "products"
    # Displays in reverse id order, first 30 products of the list of all
    queryset = Product.objects.all().order_by("-id").filter(is_available=True)


